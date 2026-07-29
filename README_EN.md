# books-to-stock-analysis-skill

[中文说明](README.md)

An AI Agent meta-skill for **OpenClaw, Hermes Agent, and Claude Code**.

It lets an agent read stock-market, investing, trading, financial-analysis, or investor-biography books, convert their knowledge, methods, charts, and cases into new Skills, and activate the accepted Skills automatically so the same agent can continue using them.

```text
Book
→ agent reads text and directly understands candlestick charts, tables, and page images
→ extracts concepts, principles, strategies, risks, counterexamples, and biographical insights
→ validates, deduplicates, and quarantines low-confidence material
→ generates and activates new Agent Skills
→ agent applies the new Skills to market, financial, or user-provided data
```

This project does not fetch live market data, backtest profitability, connect to brokers, or execute trades. The data available to generated Skills depends on the current agent's tools, APIs, and user-provided files.

## What it can generate

- Technical analysis, short-term trading, and trading systems: candlestick, moving-average, trend, volume-price, breakout, stop, risk, and anti-pattern Skills
- Value investing and financial analysis: business quality, financial metrics, valuation, moat, and decision-framework Skills
- Investor biographies, interviews, and shareholder letters: principles, circle of competence, mistake cases, psychology, and historical-context Skills
- Image-heavy books: the agent inspects charts and page images directly without an OCR dependency

Every Skill that passes the quality gate preserves chapter, page, figure, and source provenance. Parameters not defined by the author remain explicit instead of being converted into invented numeric thresholds.

## Installation

You do not need to find a host-specific command first. Tell OpenClaw, Hermes Agent, or Claude Code:

```text
Install this Skill for me:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

A Chinese prompt works as well:

```text
帮我安装这个 Skill：
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

The agent should install it using the current host's native Skill directory or installer. After installation, invoke it with natural language or the slash command supported by the host.

## Using books-to-stock-analysis-skill

Upload a book or provide a local path, then tell the agent:

```text
Use books-to-stock-analysis-skill to convert my uploaded trading book into Agent Skills.

Requirements:
- extract concepts, strategies, candlestick patterns, volume-price rules, trend analysis, risks, and counterexamples
- inspect charts and page images directly without OCR
- preserve chapter, page, figure, and source provenance
- do not invent parameters the author did not define
- activate accepted Skills automatically so the current agent can use them immediately
```

When slash commands are supported:

```text
/books-to-stock-analysis-skill

Convert /path/to/book.pdf into Skills and activate them immediately.
```

## Using the generated Skills

After generation, the agent receives a book-level router and several child Skills, for example:

```text
short-term-trading-practical-techniques       # book router
short-term-trading-volume-breakout            # volume-price breakout
short-term-trading-rising-wave                # rising trend and pullbacks
short-term-trading-false-breakout             # false breakouts
short-term-trading-risk-management            # risk and stops
short-term-trading-discipline                 # trading discipline
```

Actual names are listed in the generated `manifest.yaml` and `reports/activation-report.yaml`.

### Option 1: let the agent select child Skills

```text
Use the Skills generated from the short-term trading book.
Combine them with the last 120 trading days of OHLCV data for 600519
and the relevant benchmark-index data available to you.
Determine whether the stock matches the book's volume-breakout or rising-wave methods.

Report:
1. Skills used
2. supporting evidence
3. contradictions and risks
4. invalidation conditions
5. source chapters and pages
```

The router selects the relevant trend, volume-price, false-breakout, and risk Skills.

### Option 2: name a generated Skill explicitly

```text
Use the short-term-trading-volume-breakout Skill.
Analyze the stock_data.csv file I uploaded against the book's volume-price breakout method.
List every satisfied condition, failed condition, contradiction, and source page.
Do not return only a final verdict.
```

### Option 3: analyze a chart image

```text
Use the generated rising-wave and false-breakout Skills to analyze my daily chart image.
First list features that can be confirmed visually.
Then list every condition that still requires numeric market data.
```

### Option 4: use Skills generated from an investor biography

```text
Use the decision-framework and mistake-case Skills generated from this investor biography.
Assess whether this company is inside the author's circle of competence,
and check the analysis for overconfidence, herding, or ignored downside risks.
```

## Data requirements

Generated Skills do not contain live market data. To apply them, the agent needs one or more of:

- connected market-data, financial-data, or search tools
- user-uploaded CSV, Excel, JSON, financial statements, or research material
- a stock symbol, analysis date, and timeframe
- candlestick, volume, or other chart images

When required data is missing, the Skill should return `insufficient data` rather than invent a conclusion.

## Generated and activated output

```text
generated-skills/<book-slug>/
├── BOOK_OVERVIEW.md
├── INDEX.md
├── GLOSSARY.md
├── manifest.yaml
├── installable/     # Skills that passed the quality gate and were activated
├── provisional/     # useful but still uncertain candidates
├── rejected/        # duplicate, low-quality, or unverifiable candidates
└── reports/         # provenance, visual coverage, quality, copyright, and activation reports
```

During the current session, the meta-skill loads the generated router and child Skills immediately. Hosts with live reload expose them as native Skills; otherwise the meta-skill continues routing to them during the same session, so the user does not need to install them again.

## Boundaries

This project does not provide investment advice, guarantee that any method works, predict profitability, connect to brokers, or execute trades. Generated Skills are structured representations of book knowledge. Their analysis depends on data quality, market context, and the downstream agent's available tools.

## License

Apache License 2.0. The license covers original code and documentation in this repository, not user-provided books, images, data, or third-party content.
