# 论文 Markdown 清洗工具

把论文 PDF 批量转换为**结构化 Markdown**（带标题/作者/年份元数据头），供 AI 直接阅读或后续使用。

## 用法

### 1. 放入论文 PDF

把 PDF 放进 `papers/` 文件夹，文件名建议格式：

```
papers/
├── 2024_缑迅杰_大规模群体决策模型.pdf
├── 2025_缑迅杰_公众参与应急决策综述.pdf
└── ...
```

### 2. 转换

```bash
pip install -r requirements.txt          # 安装依赖（pypdf + pdfplumber）

python scripts/01_convert_pdf.py          # 转换 papers/ 下全部 PDF
python scripts/01_convert_pdf.py --file 某篇.pdf   # 只转换指定文件
python scripts/01_convert_pdf.py --force          # 强制重新转换
```

### 3. 输出

每篇论文在 `papers_md/` 生成一个同名 `.md` 文件，格式如下：

```markdown
---
source_pdf: "2024_Gou_xxx.pdf"
title: "Gou xxx"
authors: ""
year: "2024"
journal: ""
---

# 论文标题

> 作者 | 年份

## 正文

...全文内容...
```

`papers_md/` 目录即是最终的 Markdown 知识库，可直接供 AI 读取。

## 说明

- 只做**本地文本提取**，不调用任何云端 API，不下载模型，不上传数据。
- 支持文本型 PDF；扫描版（图片型）PDF 无法直接提取文字，需要先 OCR。
- 转换失败的文件会跳过并在终端提示，不影响其他文件。
