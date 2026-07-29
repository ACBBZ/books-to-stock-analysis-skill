# books-to-stock-analysis-skill

[English](README_EN.md)

一个面向 **OpenClaw、Hermes Agent 和 Claude Code** 的可安装元 Skill。它让 AI Agent 读取股票、投资、交易、财务分析或投资人物类书籍，并将其中的知识自动转换成可直接使用的新 Skills。

```text
书籍
→ Agent 阅读文字并直接理解 K 线图、表格和页面图片
→ 提取概念、原则、战法、风险、反例和人物经验
→ 自动校验、去重并隔离低置信度内容
→ 生成并激活新的 Agent Skills
```

项目不获取行情、不回测收益、不连接券商，也不执行交易。

## 主要作用

- 将技术分析、短线交易和交易系统书籍拆成战法、图形、风险和反模式 Skills
- 将价值投资和财务分析书籍拆成公司质量、估值、财务和决策框架 Skills
- 将投资人物传记、访谈和股东信拆成投资原则、能力圈、错误案例和心理纪律 Skills
- 直接理解书中的图表和图片，不依赖 OCR
- 保留章节、页码、图形和来源信息
- 不把作者未定义的模糊参数擅自改成精确数字

## 生成后直接使用

生成流程默认会自动激活通过质量门的 Skills，用户不需要再次逐个安装：

- **OpenClaw**：写入当前工作区的 `.agents/skills/`
- **Claude Code**：写入当前项目的 `.claude/skills/`
- **Hermes Agent**：写入 `$HERMES_HOME/skills/` 或 `~/.hermes/skills/`

在当前会话中，元 Skill 会立即读取新生成的 Router Skill 和子 Skills。宿主支持热加载时，它们也会立即成为原生斜杠命令；否则会在后续会话中自动被发现，无需再次安装。

## 安装

### OpenClaw

```bash
openclaw skills install git:ACBBZ/books-to-stock-analysis-skill@main \
  --as books-to-stock-analysis-skill
```

### Hermes Agent

```bash
hermes skills install \
  https://raw.githubusercontent.com/ACBBZ/books-to-stock-analysis-skill/main/SKILL.md \
  --name books-to-stock-analysis-skill --now
```

### Claude Code

安装到个人 Skills：

```bash
git clone https://github.com/ACBBZ/books-to-stock-analysis-skill.git \
  ~/.claude/skills/books-to-stock-analysis-skill
```

也可以安装到当前项目：

```bash
git clone https://github.com/ACBBZ/books-to-stock-analysis-skill.git \
  .claude/skills/books-to-stock-analysis-skill
```

## 使用示例

OpenClaw、Hermes 和 Claude Code 都可以使用斜杠命令调用：

```text
/books-to-stock-analysis-skill

把 /path/to/短线操盘实战技法大全.pdf 拆成 Agent Skills。
保留章节和页码来源，直接理解书中的 K 线图和图片，不使用 OCR。
生成完成后立即激活，让当前 Agent 可以直接使用这些 Skills。
```

处理人物传记：

```text
/books-to-stock-analysis-skill

把 /path/to/investor-biography.pdf 转换为 Skills。
重点提取投资原则、决策流程、成功与失败案例、能力圈和风险观，
不要强行生成买卖公式，并在生成后立即激活。
```

## 输出与激活

```text
generated-skills/<book-slug>/
├── BOOK_OVERVIEW.md
├── INDEX.md
├── GLOSSARY.md
├── manifest.yaml
├── installable/     # 已通过质量门的 Skills
├── provisional/     # 有价值但仍含不确定内容
├── rejected/        # 重复或无法验证的候选
└── reports/         # 来源、图片覆盖、质量、版权和激活报告
```

元 Skill 会自动执行：

```bash
python scripts/validate_pack.py ./generated-skills/<book-slug>
python scripts/activate_pack.py ./generated-skills/<book-slug> \
  --host openclaw   # 或 hermes / claude-code
```

详细的宿主激活规则见 [`references/HOST_ACTIVATION.md`](references/HOST_ACTIVATION.md)。

## 边界

本项目不提供投资建议，不验证策略收益，不分析当前股票，不获取实时行情，不连接券商，也不执行交易。

## License

Apache License 2.0。许可证只覆盖本仓库的原创代码和文档，不覆盖用户提供的书籍、图片或第三方内容。