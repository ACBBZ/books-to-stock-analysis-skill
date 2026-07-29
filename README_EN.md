# books-to-stock-analysis-skill

[中文说明](README.md)

An installable meta-skill for **OpenClaw, Hermes Agent, and Claude Code**. It lets an AI agent read stock-market, investing, trading, financial-analysis, or investor-biography books and convert their knowledge into new skills that the same agent can use directly.

```text
Book
→ agent reads text and directly understands charts, tables, and page images
→ extracts concepts, principles, strategies, risks, counterexamples, and biographical insights
→ verifies, deduplicates, and quarantines low-confidence material
→ generates and activates new Agent Skills
```

The project does not fetch market data, backtest profitability, connect to brokers, or execute trades.

## What it does

- turns technical-analysis and trading books into strategy, pattern, risk, and anti-pattern skills
- turns value-investing and financial-analysis books into quality, valuation, financial, and decision-framework skills
- turns investor biographies, interviews, and shareholder letters into principle, mistake, circle-of-competence, and psychology skills
- inspects charts and page images directly without an OCR dependency
- preserves chapter, page, figure, and source provenance
- keeps source-undefined parameters explicit instead of inventing precise thresholds

## Generated skills are immediately usable

The generation workflow automatically activates every skill that passes the quality gate. Users do not need to install the generated skills one by one:

- **OpenClaw:** writes to the active workspace's `.agents/skills/`
- **Claude Code:** writes to the current project's `.claude/skills/`
- **Hermes Agent:** writes to `$HERMES_HOME/skills/` or `~/.hermes/skills/`

During the current session, the meta-skill immediately loads the generated router and child skills. Hosts with live reload also expose them as native slash commands immediately; otherwise they are discovered automatically in later sessions without another install step.

## Install

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

Install as a personal skill:

```bash
git clone https://github.com/ACBBZ/books-to-stock-analysis-skill.git \
  ~/.claude/skills/books-to-stock-analysis-skill
```

Or install it for the current project:

```bash
git clone https://github.com/ACBBZ/books-to-stock-analysis-skill.git \
  .claude/skills/books-to-stock-analysis-skill
```

## Usage

OpenClaw, Hermes, and Claude Code can all invoke it as a slash command:

```text
/books-to-stock-analysis-skill

Convert /path/to/my-trading-book.pdf into Agent Skills.
Preserve chapter and page provenance, inspect charts directly, and do not use OCR.
Activate the generated skills so the current agent can use them immediately.
```

Investor-biography example:

```text
/books-to-stock-analysis-skill

Convert /path/to/investor-biography.pdf into Skills.
Focus on principles, decisions, successes, failures, circle of competence,
and risk philosophy. Do not force the material into mechanical trading rules.
Activate the accepted skills after generation.
```

## Output and activation

```text
generated-skills/<book-slug>/
├── BOOK_OVERVIEW.md
├── INDEX.md
├── GLOSSARY.md
├── manifest.yaml
├── installable/     # skills that passed the quality gate
├── provisional/     # useful but still uncertain candidates
├── rejected/        # duplicate or unverifiable candidates
└── reports/         # provenance, visual coverage, quality, copyright, and activation reports
```

The meta-skill automatically runs:

```bash
python scripts/validate_pack.py ./generated-skills/<book-slug>
python scripts/activate_pack.py ./generated-skills/<book-slug> \
  --host openclaw   # or hermes / claude-code
```

See [`references/HOST_ACTIVATION.md`](references/HOST_ACTIVATION.md) for host-specific activation behavior.

## Boundaries

This project does not provide investment advice, validate profitability, analyze current stocks, fetch live market data, connect to brokers, or execute trades.

## License

Apache License 2.0. The license covers original code and documentation in this repository, not user-provided books, images, or third-party content.