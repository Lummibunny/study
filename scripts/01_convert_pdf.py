#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_convert_pdf.py — 使用 LlamaParse（LlamaIndex 官方 AI 解析服务）将论文 PDF
解析为高质量结构化 Markdown，输出到 papers_md/。

相比纯文本提取（pypdf/pdfplumber），LlamaParse 能正确还原：
  - 双栏排版 → 正常阅读顺序
  - 表格 → Markdown 表格
  - 公式/标题/段落 → 正确的 Markdown 结构

【需要配置】LlamaParse 的 API key（llx- 开头）：
  1. 在 https://cloud.llamaindex.ai 注册并创建 API key
  2. 在项目根目录创建 .env 文件，写入:
       LLAMA_CLOUD_API_KEY=llx-你的key
  3. 或直接在命令行传入环境变量

用法:
    python 01_convert_pdf.py                     # 转换 papers/ 下全部 PDF（每篇一个 .md）
    python 01_convert_pdf.py --chunk-pages 10    # 每 10 页切分为一个 chunk 文件
    python 01_convert_pdf.py --file xxx.pdf      # 只转换指定文件
    python 01_convert_pdf.py --force             # 强制重新转换
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# 项目根目录（脚本在 scripts/ 下）
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

PAPERS_DIR = ROOT / "papers"
OUTPUT_DIR = ROOT / "papers_md"

PDF_EXTS = {".pdf", ".PDF"}


def get_parser():
    from llama_parse import LlamaParse

    api_key = os.getenv("LLAMA_CLOUD_API_KEY", "").strip()
    if not api_key:
        print("[错误] 未配置 LLAMA_CLOUD_API_KEY。")
        print("       1. 到 https://cloud.llamaindex.ai 注册并创建 API key")
        print("       2. 在项目根目录创建 .env 文件:")
        print("          LLAMA_CLOUD_API_KEY=llx-你的key")
        sys.exit(1)

    return LlamaParse(
        api_key=api_key,
        result_type="markdown",     # 输出 Markdown
        language="ch_sim",          # 简体中文（en/ch_sim/ch_tra/ja/ko 等）
        verbose=False,
        # LlamaParse 默认按页返回文档（split_by_page=True），
        # 每个 Document 即一页，便于后续按页数切 chunk
    )


def write_chunk(out_path: Path, pdf_name: str, pages: list) -> bool:
    """将若干页合并写为一个 Markdown 文件"""
    md_text = "\n\n".join(p for p in pages if p and p.strip())
    if not md_text.strip():
        return False
    header = (
        f"<!--\n"
        f"source_pdf: {pdf_name}\n"
        f"-->\n\n"
    )
    out_path.write_text(header + md_text.strip() + "\n", encoding="utf-8")
    print(f"  [完成] -> {out_path.name} ({len(md_text)} 字符)")
    return True


def convert_one(parser, pdf_path: Path, force: bool, chunk_pages: int | None) -> bool:
    print(f"  [解析中] {pdf_path.name} ...")
    try:
        documents = parser.load_data(str(pdf_path))
    except Exception as e:
        print(f"  [失败] {pdf_path.name}: {e}")
        return False

    # LlamaParse 按页返回，每页一个 Document
    pages = [(d.text or "") for d in documents]
    pages = [p.strip() for p in pages]
    if not any(pages):
        print(f"  [失败] {pdf_path.name}: 解析结果为空")
        return False

    # 从页文本里提取页码（LlamaParse 通常带 page_label，兜底用序号）
    total_pages = len(pages)
    print(f"  [信息] {pdf_path.name}: 共 {total_pages} 页")

    if chunk_pages is None or chunk_pages >= total_pages:
        # 不切分，整篇一个文件
        out_path = OUTPUT_DIR / (pdf_path.stem + ".md")
        if out_path.exists() and not force:
            print(f"  [跳过] 已存在: {out_path.name}")
            return False
        return write_chunk(out_path, pdf_path.name, pages)

    # 按 chunk_pages 页切分
    ok = True
    for start in range(0, total_pages, chunk_pages):
        end = min(start + chunk_pages, total_pages)
        chunk = pages[start:end]
        # 文件名: 原名_页码范围.md，如 xxx_p001-010.md
        suffix = f"p{start+1:03d}-{end:03d}"
        out_path = OUTPUT_DIR / f"{pdf_path.stem}_{suffix}.md"
        if out_path.exists() and not force:
            print(f"  [跳过] 已存在: {out_path.name}")
            continue
        if not write_chunk(out_path, pdf_path.name, chunk):
            print(f"  [失败] 第 {start+1}-{end} 页为空，跳过")
            ok = False
    return ok


def main():
    parser = argparse.ArgumentParser(description="LlamaParse 论文 PDF -> Markdown")
    parser.add_argument("--file", type=str, default=None, help="只解析指定的 PDF 文件")
    parser.add_argument("--force", action="store_true", help="强制重新解析所有文件")
    parser.add_argument(
        "--chunk-pages", type=int, default=None,
        help="按每 N 页切分为一个 Markdown 文件（默认不切分，整篇一个文件）",
    )
    args = parser.parse_args()

    if args.chunk_pages is not None and args.chunk_pages < 1:
        print("[错误] --chunk-pages 必须 >= 1")
        sys.exit(1)

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
        sys.exit(0)

    chunk_desc = f"，每 {args.chunk_pages} 页一个 chunk" if args.chunk_pages else "，整篇一个文件"
    print(f"找到 {len(files)} 个 PDF 文件{chunk_desc}，初始化 LlamaParse...\n")
    parser = get_parser()

    ok = 0
    for f in files:
        if convert_one(parser, f, args.force, args.chunk_pages):
            ok += 1
    print(f"\n完成: 成功 {ok}/{len(files)} 篇。Markdown 输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
