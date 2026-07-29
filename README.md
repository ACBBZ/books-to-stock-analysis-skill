# books-to-stock-analysis-skill

[English](README_EN.md)

一个面向 **OpenClaw、Hermes Agent 和 Claude Code** 的 AI Agent 元 Skill。

它让 Agent 读取股票、投资、交易、财务分析或投资人物类书籍，把书中的知识、方法、图形和案例转换成新的 Skills，并在生成完成后自动激活，让当前 Agent 可以继续使用这些 Skills。

```text
书籍
→ Agent 阅读文字并直接理解 K 线图、表格和页面图片
→ 提取概念、原则、战法、风险、反例和人物经验
→ 自动校验、去重并隔离低置信度内容
→ 生成并激活新的 Agent Skills
→ Agent 使用新 Skills 结合行情、财务或用户提供的数据进行分析
```

本项目不获取行情、不回测收益、不连接券商，也不执行交易。生成后的 Skill 如何获得数据，取决于当前 Agent 已连接的工具、API 和用户提供的文件。

## 可以生成什么

- 技术分析、短线交易和交易系统：K 线、均线、趋势、量价、突破、止损、风险和反模式 Skills
- 价值投资和财务分析：公司质量、财务指标、估值、护城河和决策框架 Skills
- 投资人物传记、访谈和股东信：投资原则、能力圈、错误案例、心理纪律和历史情境 Skills
- 图片密集型书籍：由 Agent 直接理解图表和页面图片，不依赖 OCR

每个通过质量门的 Skill 会保留章节、页码、图形和来源信息。作者没有明确给出的参数不会被擅自改成精确数字。

## 安装

不需要先查找特定宿主命令。直接把下面这句话发给 OpenClaw、Hermes Agent 或 Claude Code：

```text
帮我安装这个 Skill：
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

也可以使用英文：

```text
Install this Skill for me:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

Agent 应根据当前宿主的 Skill 目录和安装能力完成安装。安装后可以使用自然语言或宿主支持的斜杠命令调用。

## 使用 books-to-stock-analysis-skill

上传书籍或给出本地文件路径，然后告诉 Agent：

```text
使用 books-to-stock-analysis-skill，
把我上传的《短线操盘实战技法大全》拆成 Agent Skills。

要求：
- 提取知识点、战法、K 线图形、量价关系、走势分析、风险规则和反例
- 直接理解书中的图片和图表，不使用 OCR
- 保留章节、页码和图形来源
- 不擅自发明作者没有定义的参数
- 生成完成后自动激活，让当前 Agent 可以直接使用
```

宿主支持斜杠命令时，也可以这样调用：

```text
/books-to-stock-analysis-skill

把 /path/to/book.pdf 拆成 Skills，生成后立即激活。
```

## 生成后的 Skill 如何使用

生成完成后，Agent 会得到一个书籍 Router Skill 和若干子 Skills，例如：

```text
short-term-trading-practical-techniques       # 书籍总入口
short-term-trading-volume-breakout            # 量价突破
short-term-trading-rising-wave                # 上升浪与回调
short-term-trading-false-breakout             # 假突破
short-term-trading-risk-management            # 风险与止损
short-term-trading-discipline                 # 交易纪律
```

实际名称以生成结果中的 `manifest.yaml` 和 `reports/activation-report.yaml` 为准。

### 方式一：让 Agent 自动选择子 Skill

```text
使用刚刚从《短线操盘实战技法大全》生成的 Skills，
结合你能访问的 600519 最近 120 个交易日 K 线、成交量和上证指数数据，
判断当前是否符合书中的量价突破或上升浪战法。

请输出：
1. 使用了哪些 Skills
2. 支持证据
3. 反证和风险
4. 战法失效条件
5. 对应的书籍章节和页码
```

书籍 Router 会根据问题选择量价、趋势、假突破和风险等子 Skills。

### 方式二：明确指定生成的 Skill

```text
使用 short-term-trading-volume-breakout Skill，
分析我上传的 stock_data.csv 是否符合书中的量价突破条件。
不要只给结论，要逐项列出满足条件、未满足条件、反证和来源页码。
```

### 方式三：分析图表或走势截图

```text
使用刚生成的上升浪和假突破 Skills，
分析我上传的日 K 线图。
先说明图中可以确认的特征，再列出无法仅凭图片确认、仍需要行情数据的条件。
```

### 方式四：使用人物传记生成的 Skill

```text
使用刚刚从这本投资人物传记生成的决策框架和错误案例 Skills，
分析这家公司是否落在作者的能力圈内，
并检查当前判断是否存在过度自信、从众或忽略下行风险的问题。
```

## 数据要求

生成的 Skills 不自带实时行情。Agent 使用它们进行分析时，需要以下一种或多种输入：

- Agent 已连接的行情、财务或搜索工具
- 用户上传的 CSV、Excel、JSON、财报或研究资料
- 用户提供的股票代码、分析日期和时间周期
- K 线图、成交量图或其他页面图片

缺少关键数据时，Skill 应明确输出“数据不足”，而不是编造结论。

## 生成与激活结果

```text
generated-skills/<book-slug>/
├── BOOK_OVERVIEW.md
├── INDEX.md
├── GLOSSARY.md
├── manifest.yaml
├── installable/     # 已通过质量门并自动激活的 Skills
├── provisional/     # 有价值但仍含不确定内容
├── rejected/        # 重复、低质量或无法验证的候选
└── reports/         # 来源、图片覆盖、质量、版权和激活报告
```

当前会话中，元 Skill 会立即加载新生成的 Router 和子 Skills。宿主支持热加载时，它们也会成为原生 Skill；否则元 Skill 会继续在当前会话中完成路由，不需要用户再次安装。

## 边界

本项目不提供投资建议，不保证任何策略有效，不分析未来收益，不连接券商，也不执行交易。生成的 Skills 是对书籍知识的结构化表达，实际分析结果取决于数据质量、市场环境和下游 Agent 的工具能力。

## License

Apache License 2.0。许可证只覆盖本仓库的原创代码和文档，不覆盖用户提供的书籍、图片、数据或第三方内容。
