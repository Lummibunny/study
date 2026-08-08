#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_convert_pdf.py — 将 papers/ 目录下的论文 PDF 转换为结构化 Markdown
输出到 papers_md/ 目录，每篇一个 .md 文件，带 YAML 元数据头，AI 可直接读取。

用法:
    python 01_convert_pdf.py                 # 转换 papers/ 下全部 PDF
    python 01_convert_pdf.py --file xxx.pdf  # 只转换指定文件
    python 01_convert_pdf.py --force         # 强制重新转换（默认跳过已转换的）
"""

import argparse
import os
import re
import sys
from pathlib import Path

# 项目根目录（脚本在 scripts/ 下）
ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "papers"
OUTPUT_DIR = ROOT / "papers_md"

PDF_EXTS = {".pdf", ".PDF"}


def extract_text_pypdf(pdf_path: Path) -> str:
    """使用 pypdf 提取纯文本（快速，适合文本型 PDF）"""
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    return "\n\n".join(pages)


def extract_text_pdfplumber(pdf_path: Path) -> str:
    """使用 pdfplumber 提取（更稳，适合排版复杂的论文）"""
    import pdfplumber
    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n\n".join(pages)


def clean_text(text: str) -> str:
    """清理提取出的文本：去掉多余空白、合并孤行"""
    # 统一换行符
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # 去掉每行首尾空白
    lines = [ln.strip() for ln in text.split("\n")]
    # 合并被 PDF 断行的英文单词（如 "deci-\nsion" -> "decision"）
    merged = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if (
            ln
            and merged
            and re.search(r"[A-Za-z]-$", merged[-1])
            and re.match(r"^[a-z]", ln)
        ):
            merged[-1] = merged[-1][:-1] + ln
        else:
            merged.append(ln)
        i += 1
    text = "\n".join(merged)
    # 压缩连续空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def guess_metadata(pdf_path: Path, text: str) -> dict:
    """
    从文件名与正文第一页启发式提取元数据（标题/作者/年份）
    文件名建议格式: 2024_作者_标题关键词.pdf 或 标题.pdf
    """
    meta = {
        "source_pdf": pdf_path.name,
        "title": "",
        "authors": "",
        "year": "",
        "journal": "",
    }
    # 从文件名解析
    stem = pdf_path.stem
    parts = re.split(r"[_\-—]", stem)
    if parts and re.fullmatch(r"\d{4}", parts[0]):
        meta["year"] = parts[0]
        meta["title"] = " ".join(parts[1:]).strip()
    else:
        meta["title"] = stem
    # 从正文首页提取标题/作者（粗粒度）
    head = text[:3000].replace("\n", " ")
    # 年份
    if not meta["year"]:
        m = re.search(r"\b(19|20)\d{2}\b", head)
        if m:
            meta["year"] = m.group(0)
    return meta


def build_markdown(meta: dict, text: str) -> str:
    """组装带元数据头的 Markdown 文档"""
    header = [
        "---",
        f"source_pdf: \"{meta['source_pdf']}\"",
        f"title: \"{meta['title']}\"",
        f"authors: \"{meta['authors']}\"",
        f"year: \"{meta['year']}\"",
        f"journal: \"{meta['journal']}\"",
        "---",
        "",
        f"# {meta['title']}",
        "",
    ]
    if meta["year"] or meta["authors"]:
        info = " | ".join(
            [x for x in (meta["authors"], meta["year"], meta["journal"]) if x]
        )
        if info:
            header.append(f"> {info}")
            header.append("")
    header.append("## 正文")
    header.append("")
    body = text
    return "\n".join(header) + "\n\n" + body + "\n"


def convert_one(pdf_path: Path, force: bool) -> bool:
    out_path = OUTPUT_DIR / (pdf_path.stem + ".md")
    if out_path.exists() and not force:
        print(f"  [跳过] 已存在: {out_path.name}")
        return False
    print(f"  [转换] {pdf_path.name} ...")
    # 先用 pypdf，失败或文本过少则退回 pdfplumber
    text = ""
    try:
        text = extract_text_pypdf(pdf_path)
    except Exception as e:
        print(f"    pypdf 失败: {e}")
    if len(text.strip()) < 200:
        try:
            text = extract_text_pdfplumber(pdf_path)
        except Exception as e:
            print(f"    pdfplumber 失败: {e}")
    if len(text.strip()) < 200:
        print(f"  [警告] 未能提取有效文本: {pdf_path.name}（可能是扫描版 PDF）")
        return False
    text = clean_text(text)
    meta = guess_metadata(pdf_path, text)
    md = build_markdown(meta, text)
    out_path.write_text(md, encoding="utf-8")
    print(f"  [完成] -> {out_path.name} ({len(text)} 字符)")
    return True


def main():
    parser = argparse.ArgumentParser(description="论文 PDF -> Markdown 转换器")
    parser.add_argument("--file", type=str, default=None, help="只转换指定的 PDF 文件")
    parser.add_argument("--force", action="store_true", help="强制重新转换所有文件")
    args = parser.parse_args()

    PAPERS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    if args.file:
        pdf = Path(args.file)
        if not pdf.exists():
            print(f"[错误] 文件不存在: {pdf}")
            sys.exit(1)
        files = [pdf]
    else:
        files = sorted(
            [p for p in PAPERS_DIR.iterdir() if p.suffix in PDF_EXTS],
            key=lambda p: p.name,
        )

    if not files:
        print(f"[提示] papers/ 目录下没有 PDF 文件。")
        print(f"       请将论文 PDF 放入: {PAPERS_DIR}")
        print(f"       文件名建议格式: 2024_作者_标题.pdf")
        sys.exit(0)

    print(f"找到 {len(files)} 个 PDF 文件，开始转换...\n")
    ok = 0
    for f in files:
        if convert_one(f, args.force):
            ok += 1
    print(f"\n完成: 成功 {ok}/{len(files)} 篇。Markdown 输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
