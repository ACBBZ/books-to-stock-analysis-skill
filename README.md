# books-to-stock-analysis-skill

[English](README_EN.md)

一个可以安装到 Codex 等 AI Agent 的**元 Skill**：让 Agent 把股票、投资、交易、财务分析或投资人物类书籍，拆解成一组新的、可安装的 Agent Skills。

它不是股票分析工具，也不获取行情、回测收益或连接券商。它只负责：

```text
书籍
→ Agent 阅读文字并理解 K 线图、表格和页面图片
→ 提取概念、原则、战法、风险、反例和人物经验
→ 自动校验、去重并隔离低置信度内容
→ 生成可安装的 Skill Pack
```

## 适合处理的内容

- 技术分析、短线交易和交易系统
- K 线、均线、趋势、量价、突破和风险控制
- 价值投资、财务分析和估值框架
- 投资人物传记、访谈、股东信和投资案例

人物传记不会被强行转换成买卖公式，而会生成投资原则、决策框架、错误案例、能力圈和心理纪律等 Skills。

## 特点

- 仓库本身可作为 Skill 安装
- 支持 PDF、EPUB、DOCX、Markdown、TXT 和页面图片
- 不依赖 OCR；由 Agent 直接理解书中的图表和图片
- 不要求人工逐条审阅，通过自动质量门筛选结果
- 保留章节、页码、图形和来源信息
- 不明确的参数不会被擅自改成精确数字
- 输出区分 `installable`、`provisional` 和 `rejected`
- 默认不复制整本书、长篇原文或原始页面图片

## 安装到 Codex

在 Codex 中使用 Skill Installer：

```text
$skill-installer install the skill from:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

安装后重新启动 Codex，或在新会话中使用。

## 使用示例

### 将一本交易书拆成 Skills

```text
$books-to-stock-analysis-skill

把 /path/to/短线操盘实战技法大全.pdf 拆成可安装的 Agent Skills。
输出到 ./generated-skills/short-term-trading。
保留章节和页码来源，直接理解书中的 K 线图和图片，不使用 OCR。
```

### 处理投资人物传记

```text
$books-to-stock-analysis-skill

把 /path/to/investor-biography.pdf 转换为 Skills。
重点提取投资原则、决策流程、成功与失败案例、能力圈和风险观，
不要强行生成买卖公式。
```

### 处理多份资料

```text
$books-to-stock-analysis-skill

把 ./sources/ 下的书籍、访谈和股东信整理成一个 Skill Pack。
保留不同作者观点的差异和冲突。
```

## 输出

```text
generated-skills/<book-slug>/
├── BOOK_OVERVIEW.md
├── INDEX.md
├── GLOSSARY.md
├── manifest.yaml
├── installable/     # 可独立安装的 Skills
├── provisional/     # 有价值但仍含不确定内容
├── rejected/        # 重复或无法验证的候选
└── reports/         # 来源、图片覆盖、质量和版权报告
```

生成后可以执行结构校验和打包：

```bash
python scripts/validate_pack.py ./generated-skills/<book-slug>
python scripts/package_skills.py ./generated-skills/<book-slug>
```

详细设计见 [`docs/OPTIMIZATION_DESIGN.md`](docs/OPTIMIZATION_DESIGN.md)，输出规范见 [`references/OUTPUT_SPEC.md`](references/OUTPUT_SPEC.md)。

## 边界

本项目不提供投资建议，不验证策略收益，不分析当前股票，不获取实时行情，不连接券商，也不执行交易。

## License

Apache License 2.0。许可证只覆盖本仓库的原创代码和文档，不覆盖用户提供的书籍、图片或第三方内容。
