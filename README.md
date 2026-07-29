# books-to-stock-analysis-skill

[English](README_EN.md)

一个可安装到 Codex 及其他兼容 Agent Skills 标准的 **元 Skill（Skill Generator）**。

它的职责不是分析股票，也不是连接行情或券商，而是让 AI Agent 将一本股票、投资、交易或投资人物类书籍，拆解并编译成一组新的、可安装的 Agent Skills。

```text
安装本项目 Skill
        ↓
向 Agent 提供一本书
        ↓
Agent 阅读文字并直接理解页面图片、K 线图和示意图
        ↓
抽取概念、原则、战法、图形、风险、反例和人物经验
        ↓
自动验证、去重、补齐边界并隔离低置信度内容
        ↓
输出新的可安装 Skill Pack
```

> 本项目不提供投资建议，不验证策略收益，不获取实时行情，不连接券商，也不执行交易。

## 核心定位

本仓库本身就是一个可安装 Skill：

```text
books-to-stock-analysis-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── assets/
```

安装后，Codex 或其他支持 Agent Skills 的 Agent 可以调用它，把用户提供的新书转换为新的 Skills。

## Codex 安装与调用

安装：

```text
$skill-installer install the skill from:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

安装完成后重启 Codex，或在下一个会话中使用。

调用：

```text
$books-to-stock-analysis-skill
把 /path/to/短线操盘实战技法大全.pdf 拆成可安装的 Agent Skills，
输出到 ./generated-skills/short-term-trading。
```

也可以使用自然语言：

```text
Use $books-to-stock-analysis-skill to convert this trading book
into an installable skill pack.
```

> Codex 推荐使用 `$skill-name` 显式调用 Skill。部分其他 Agent 客户端可能使用 `/skill-name`，但这不是本项目保证的统一调用语法。

## 输入范围

支持由 Agent 能够读取的本地资料：

- PDF
- EPUB
- DOCX
- Markdown
- TXT
- 图片或按页渲染的书籍
- 多文件资料集
- 书籍与作者访谈、股东信、课程讲义的组合

## 支持的书籍类型

### 技术分析与短线交易

可生成：

- K 线形态 Skill
- 均线与趋势 Skill
- 量价关系 Skill
- 突破与假突破 Skill
- 波段与涨停研究 Skill
- 入场、失效、退出和风险 Skill

### 交易系统与风险管理

可生成：

- 仓位管理 Skill
- 止损与退出 Skill
- 市场环境 Skill
- 交易纪律 Skill
- 反模式和风险否决 Skill

### 价值投资与财务分析

可生成：

- 公司质量分析 Skill
- 护城河检查 Skill
- 财务质量 Skill
- 资本配置 Skill
- 估值框架 Skill
- 风险清单 Skill

### 投资人物传记、访谈和股东信

不会强行把传记编成买卖公式，而是生成：

- 投资原则 Skill
- 决策框架 Skill
- 能力圈 Skill
- 错误案例 Skill
- 心理纪律 Skill
- 历史情境对照 Skill
- 人物观点边界 Skill

## 不使用 OCR

本项目不依赖 Tesseract、PaddleOCR 或其他 OCR 引擎。

Agent 按以下顺序读取书籍：

1. 有原生文本层时，读取 PDF、EPUB 或 DOCX 的文本结构。
2. 渲染包含图形、表格、K 线图、注释或扫描内容的页面。
3. 由 Agent 的多模态能力直接理解页面图像。
4. 将图片内容转换为结构化视觉证据和 Skill 工作流。
5. 记录页面、图号、图注和视觉判断置信度。

对于完全扫描且页数很大的书籍，速度和成本取决于 Agent 的视觉能力与上下文限制。Agent 无法读取图片时必须停止并报告能力缺失，不得静默跳过图片。

## 无人工审阅模式

项目默认不要求人工逐条审核，但这不等于不做验证。

自动发布门包括：

1. 结构分析
2. 多类型知识抽取
3. 来源复核
4. 图文一致性检查
5. 去重与冲突检查
6. 反例和边界补全
7. Skill 编译
8. 触发测试和对抗测试
9. Manifest、来源和格式校验
10. 低置信度隔离

输出分为：

- `installable/`：通过自动发布门的 Skills
- `provisional/`：仍含未解决参数或弱来源的 Skills
- `rejected/`：重复、无法验证、纯叙事或不适合成为 Skill 的候选

因此“不人工审阅”的正确含义是：

> Agent 自动完成提取、复核和质量门控；不确定内容不会混入默认可安装 Skills。

## 输出结构

```text
generated-skills/<book-slug>/
├── PACK.md
├── manifest.yaml
├── BOOK_OVERVIEW.md
├── INDEX.md
├── GLOSSARY.md
├── source-map.yaml
├── installable/
│   ├── <book-slug>/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/
│   ├── <book-slug>-volume-breakout/
│   │   ├── SKILL.md
│   │   ├── skill.yaml
│   │   ├── references/
│   │   └── tests/
│   └── <book-slug>-risk-management/
├── provisional/
├── rejected/
└── reports/
    ├── generation-report.md
    ├── visual-coverage.yaml
    ├── quality-report.yaml
    └── copyright-report.yaml
```

`installable/` 下每个一级目录都是一个独立、可安装的 Skill。

## 生成的 Skill 类型

| 类型 | 作用 |
|---|---|
| `router` | 书籍总入口，理解用户意图并路由到子 Skill |
| `concept` | 解释术语、定义和作者语义 |
| `principle` | 提供原则和决策检查清单 |
| `pattern` | 描述 K 线、量价、趋势和图形识别流程 |
| `strategy` | 提供前置、触发、过滤、失效、退出和风险流程 |
| `risk_rule` | 检查流动性、仓位、波动、追高和止损风险 |
| `anti_pattern` | 识别假突破、诱多、顶部滞涨等反例 |
| `market_regime` | 描述战法适用的市场环境 |
| `fundamental` | 财务、商业模式、估值和管理层分析 |
| `decision_framework` | 将作者的方法论变成可重复执行的决策流程 |
| `biography_case` | 提取人物经历、错误、原则和历史背景 |
| `psychology` | 提供认知偏差与交易纪律检查 |

## 一个发布 Skill 必须包含什么

每个 `installable` Skill 至少需要：

- 清晰的 `name` 和 `description`
- 明确的触发场景
- 所需输入和工具
- 可重复执行的步骤
- 输出格式
- 适用范围和不适用情况
- 风险和反例
- 来源章节与页码
- 图片来源时的视觉证据
- 置信度
- 正向、反向、模糊和对抗触发测试
- 不包含保证收益、必涨或确定性投资结论

策略型 Skill 还需要：

- 前置条件
- 必要条件
- 确认条件
- 否决条件
- 失效条件
- 退出或停止使用条件
- 所需市场数据字段
- 未解决参数说明

## 典型工作流

```text
$books-to-stock-analysis-skill
把 ./books/new-book.pdf 拆成 Skills。
要求：
- 输出到 ./generated-skills/new-book
- 保留章节和页码来源
- 直接理解书中的 K 线图和图片
- 不使用 OCR
- 不生成行情分析结果
- 不验证收益
- 自动隔离低置信度候选
```

Agent 应依次执行：

1. 检查文件访问和图片理解能力。
2. 建立书籍清单、章节结构和页码映射。
3. 标记图片密集、表格密集和关键战法页面。
4. 对文字与视觉页面分批阅读。
5. 构建候选知识图谱。
6. 自动判断书籍类型和 Skill 类型。
7. 合并重复内容，保留多处来源。
8. 明确未定义参数，不擅自发明阈值。
9. 生成 Skills。
10. 自动执行质量门。
11. 输出可安装、临时和拒绝结果。
12. 生成最终报告。

## 确定性校验与打包

生成结束后可运行：

```bash
python scripts/validate_pack.py ./generated-skills/short-term-trading
python scripts/package_skills.py ./generated-skills/short-term-trading
```

校验器检查目录结构、Skill frontmatter、来源文件、触发测试、视觉覆盖声明、禁止收益保证表达和是否误打包原始书籍。它不理解书籍内容，不能替代 Agent 的来源与图片复核。

## 安全与版权

默认导出策略：

- 不复制整本书。
- 不导出连续长篇原文。
- 不默认导出原始页面图片。
- 使用页码、章节和简短派生说明进行来源追溯。
- 图片内容输出为结构化描述或自行重建的示意说明。
- 商业书籍文件留在用户本地，不进入本仓库。
- 生成的交易方法只表示作者知识的结构化表达，不表示历史有效性。

## 项目边界

不属于核心范围：

- 实时行情
- 股票扫描
- 回测
- 使用生成的 Skill 分析股票
- 自动安装生成结果
- 券商连接
- 自动下单
- 投资组合管理

## 当前仓库重构方向

当前版本中的 Trading Skill IR、安全 DSL 和示例执行器可以保留为可选输出校验工具，但不再作为产品主入口。

主入口改为：

```text
SKILL.md
  → 书籍读取与视觉理解
  → 自动知识抽取与复核
  → Skill Pack 编译与校验
```

完整方案见：

- [`docs/OPTIMIZATION_DESIGN.md`](docs/OPTIMIZATION_DESIGN.md)
- [`references/OUTPUT_SPEC.md`](references/OUTPUT_SPEC.md)

> 本 README 描述的是目标版本，不表示仓库当前已经完成全部功能。Release Notes 应明确标注每个阶段的可用能力。

## License

Apache License 2.0。

该许可证覆盖本仓库的原创代码和文档，不覆盖用户提供的书籍、图片、数据或第三方内容。
