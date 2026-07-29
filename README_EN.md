# books-to-stock-analysis-skill

[中文说明](README.md)

An installable **meta-skill** for Codex and other AI agents. It helps an agent turn stock-market, investing, trading, financial-analysis, or investor-biography books into new installable Agent Skills.

It is not a stock-analysis or trading system. Its only job is:

```text
Book
→ agent reads text and understands charts, tables, and page images
→ extracts concepts, principles, strategies, risks, counterexamples, and biographical insights
→ verifies, deduplicates, and quarantines low-confidence material
→ generates a portable Skill Pack
```

## What it can process

- technical analysis, short-term trading, and trading systems
- candlesticks, moving averages, trends, volume-price patterns, breakouts, and risk control
- value investing, financial analysis, and valuation frameworks
- investor biographies, interviews, shareholder letters, and case studies

Biographies are not forced into buy/sell formulas. They can become skills for investment principles, decision frameworks, mistakes, circle of competence, and trading psychology.

## Highlights

- the repository itself is installable as a Skill
- supports PDF, EPUB, DOCX, Markdown, TXT, and page images
- no OCR dependency; the agent directly inspects charts and images
- no mandatory line-by-line human review; automated quality gates classify results
- preserves chapter, page, figure, and source provenance
- undefined parameters remain explicit instead of being invented
- separates outputs into `installable`, `provisional`, and `rejected`
- does not export the full source book, long passages, or page scans by default

## Install in Codex

Use the Skill Installer in Codex:

```text
$skill-installer install the skill from:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

Restart Codex after installation, or use it in a new session.

## Usage examples

### Convert a trading book

```text
$books-to-stock-analysis-skill

Convert /path/to/my-trading-book.pdf into installable Agent Skills.
Write the output to ./generated-skills/my-trading-book.
Preserve chapter and page provenance, inspect charts directly, and do not use OCR.
```

### Convert an investor biography

```text
$books-to-stock-analysis-skill

Convert /path/to/investor-biography.pdf into Skills.
Focus on principles, decision processes, successes, failures, circle of competence,
and risk philosophy. Do not force the material into mechanical trading rules.
```

### Process multiple sources

```text
$books-to-stock-analysis-skill

Turn the books, interviews, and shareholder letters under ./sources/
into one Skill Pack. Preserve differences and conflicts between authors.
```

## Output

```text
generated-skills/<book-slug>/
├── BOOK_OVERVIEW.md
├── INDEX.md
├── GLOSSARY.md
├── manifest.yaml
├── installable/     # independently installable skills
├── provisional/     # useful but still uncertain candidates
├── rejected/        # duplicate or unverifiable candidates
└── reports/         # provenance, visual coverage, quality, and copyright reports
```

Validate and package the generated output:

```bash
python scripts/validate_pack.py ./generated-skills/<book-slug>
python scripts/package_skills.py ./generated-skills/<book-slug>
```

See [`docs/OPTIMIZATION_DESIGN.md`](docs/OPTIMIZATION_DESIGN.md) for the full design and [`references/OUTPUT_SPEC.md`](references/OUTPUT_SPEC.md) for the output specification.

## Boundaries

This project does not provide investment advice, validate profitability, analyze current stocks, fetch live market data, connect to brokers, or execute trades.

## License

Apache License 2.0. The license covers original code and documentation in this repository, not user-provided books, images, or third-party content.
