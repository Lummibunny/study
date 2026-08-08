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
    python 01_convert_pdf.py                  # 转换 papers/ 下全部 PDF
    python 01_convert_pdf.py --file xxx.pdf   # 只转换指定文件
    python 01_convert_pdf.py --force          # 强制重新转换
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
        language="ch",              # 中英文论文
        verbose=False,
    )


def convert_one(parser, pdf_path: Path, force: bool) -> bool:
    out_path = OUTPUT_DIR / (pdf_path.stem + ".md")
    if out_path.exists() and not force:
        print(f"  [跳过] 已存在: {out_path.name}")
        return False

    print(f"  [解析中] {pdf_path.name} ...")
    try:
        documents = parser.load_data(str(pdf_path))
    except Exception as e:
        print(f"  [失败] {pdf_path.name}: {e}")
        return False

    # LlamaParse 返回文档列表，拼接所有页面文本
    md_text = "\n\n".join(doc.text for doc in documents if doc.text)

    # 加个简单的文件头，标注来源
    header = (
        f"<!--\n"
        f"source_pdf: {pdf_path.name}\n"
        f"-->\n\n"
    )
    md_text = header + md_text.strip() + "\n"

    out_path.write_text(md_text, encoding="utf-8")
    print(f"  [完成] -> {out_path.name} ({len(md_text)} 字符)")
    return True


def main():
    parser = argparse.ArgumentParser(description="LlamaParse 论文 PDF -> Markdown")
    parser.add_argument("--file", type=str, default=None, help="只解析指定的 PDF 文件")
    parser.add_argument("--force", action="store_true", help="强制重新解析所有文件")
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
        sys.exit(0)

    print(f"找到 {len(files)} 个 PDF 文件，初始化 LlamaParse...\n")
    parser = get_parser()

    ok = 0
    for f in files:
        if convert_one(parser, f, args.force):
            ok += 1
    print(f"\n完成: 成功 {ok}/{len(files)} 篇。Markdown 输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
