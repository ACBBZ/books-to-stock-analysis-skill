# books-to-stock-analysis-skill

[中文说明](README.md)

An AI Agent Skill for **Codex, OpenClaw, Hermes Agent, and Claude Code**.

It lets an agent read stock-market, investing, trading, financial-analysis, or investor-biography books, convert their knowledge, methods, charts, and cases into new Skills, and automatically activate the results that pass quality checks so the current agent can continue using them.

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
- Value investing and financial analysis: business-quality, financial-metric, valuation, moat, and decision-framework Skills
- Investor biographies, interviews, and shareholder letters: principle, circle-of-competence, mistake-case, psychology, and historical-context Skills
- Image-heavy books: the agent inspects charts and page images directly without an OCR dependency

Every Skill that passes quality checks preserves chapter, page, figure, and source provenance. Parameters not defined by the author remain explicit instead of being converted into invented numeric thresholds.

## Installation

Tell Codex, OpenClaw, Hermes Agent, or Claude Code:

```text
Install this Skill for me:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

The agent should install the complete Skill directory using the current host's native installer or Skill location.

In Codex, you can also use the built-in Skill Installer:

```text
$skill-installer install https://github.com/ACBBZ/books-to-stock-analysis-skill
```

Start a new Codex session or restart Codex after installation so the Skill appears in the available Skills list.

## Convert a book into Skills

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

When the host supports explicit Skill invocation, use:

```text
/books-to-stock-analysis-skill
```

In Codex, use:

```text
$books-to-stock-analysis-skill
```

## Use the generated Skills

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

### Let the agent select child Skills

```text
Use the Skills generated from the short-term trading book.
Combine them with the latest 120 trading days of OHLCV data for 600519
and the relevant benchmark-index data available to you.
Determine whether the stock matches the book's volume-breakout or rising-wave methods.

Report:
1. Skills used
2. supporting evidence
3. contradictions and risks
4. invalidation conditions
5. source chapters and pages
```

The book router selects the relevant trend, volume-price, false-breakout, and risk Skills.

### Name a generated Skill explicitly

```text
Use the short-term-trading-volume-breakout Skill.
Analyze the stock_data.csv file I uploaded against the book's volume-price breakout method.
List every satisfied condition, failed condition, contradiction, and source page.
```

### Analyze a chart image

```text
Use the generated rising-wave and false-breakout Skills to analyze my daily chart image.
First list features that can be confirmed visually.
Then list every condition that still requires numeric market data.
```

### Use Skills generated from an investor biography

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

## Automatic activation

Skills that pass quality checks are written to the current host's Skill location:

- **Codex:** `.agents/skills/` in the current project, or `~/.agents/skills/` in global mode
- **OpenClaw:** `.agents/skills/` in the active workspace
- **Claude Code:** `.claude/skills/` in the current project
- **Hermes Agent:** `$HERMES_HOME/skills/` or `~/.hermes/skills/`

During the current session, this Skill immediately loads the generated router and child Skills. If the host has not refreshed its native Skill index, this Skill continues routing to them, so the user does not need to install them again.

## Boundaries

This project does not provide investment advice, guarantee that any method works, predict profitability, connect to brokers, or execute trades. Generated Skills are structured representations of book knowledge. Their analysis depends on data quality, market context, and the downstream agent's available tools.

## License

Apache License 2.0. The license covers original code and documentation in this repository, not user-provided books, images, data, or third-party content.
