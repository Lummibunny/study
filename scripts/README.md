# 论文 Markdown 解析工具（LlamaParse）

使用 **LlamaParse**（LlamaIndex 官方 AI 文档解析服务）把论文 PDF 解析为**高质量结构化 Markdown**，输出到 `papers_md/` 供 AI 直接阅读或上传至 LlamaIndex 平台。

## 为什么用 LlamaParse

论文 PDF 通常包含双栏排版、表格、公式、复杂标题层级。传统纯文本提取（pypdf/pdfplumber）会把这些拆得乱七八糟，无法阅读。LlamaParse 用 AI 理解页面布局，输出**正确的阅读顺序和 Markdown 结构**（表格转成 Markdown 表格、标题层级保留、公式可读）。

## 前置条件：LlamaParse API key

1. 注册 https://cloud.llamaindex.ai （免费额度可用）
2. 创建 API key（`llx-` 开头）
3. 在项目根目录创建 `.env` 文件：
   ```
   LLAMA_CLOUD_API_KEY=llx-你的key
   ```

## 用法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 放入论文 PDF

把 PDF 放进 `papers/` 文件夹：

```
papers/
├── 2024_Gou_xxx.pdf
├── 2025_Gou_yyy.pdf
└── ...
```

### 3. 解析为 Markdown

```bash
python scripts/01_convert_pdf.py          # 解析 papers/ 下全部 PDF
python scripts/01_convert_pdf.py --file 某篇.pdf   # 只解析指定文件
python scripts/01_convert_pdf.py --force          # 强制重新解析
```

### 4. 输出

`papers_md/` 目录下每篇一个 `.md` 文件，即为最终知识库，可上传至 LlamaIndex 或直接供 AI 读取。

## 目录结构

```
study/
├── papers/        # 存放论文 PDF
├── papers_md/     # LlamaParse 解析出的 Markdown
├── scripts/
│   └── 01_convert_pdf.py
├── requirements.txt
├── .env           # 放 LLAMA_CLOUD_API_KEY（自行创建）
└── README.md
```
