# books-to-stock-analysis-skill

[中文说明](README.md)

An installable **meta-skill (skill generator)** for Codex and other agents that support the Agent Skills format.

This project does not analyze stocks, fetch market data, connect to brokers, or execute trades. Its only responsibility is to help an AI agent convert a stock-market, investing, trading, financial-analysis, or investor-biography book into a new set of installable Agent Skills.

```text
Install this meta-skill
        ↓
Give the agent a book
        ↓
The agent reads text and directly understands page images, charts, and diagrams
        ↓
It extracts concepts, principles, strategies, patterns, risks, counterexamples, and biographical insights
        ↓
It verifies, deduplicates, adds boundaries, and quarantines low-confidence material
        ↓
It emits a portable, installable Skill Pack
```

> This project does not provide investment advice, validate profitability, fetch live prices, connect to a brokerage account, or execute trades.

## Product scope

The repository itself is an installable skill:

```text
books-to-stock-analysis-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── assets/
```

Once installed, Codex or another Agent Skills-compatible agent can invoke it to turn a new user-provided book into new skills.

## Codex installation and invocation

Install:

```text
$skill-installer install the skill from:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

Restart Codex after installation, or use it in the next session.

Invoke:

```text
$books-to-stock-analysis-skill
Convert /path/to/my-trading-book.pdf into installable Agent Skills.
Write the output to ./generated-skills/my-trading-book.
```

Natural-language invocation also works:

```text
Use $books-to-stock-analysis-skill to convert this trading book
into an installable skill pack.
```

> Codex recommends the explicit `$skill-name` marker. Some other agent clients may expose `/skill-name`, but that syntax is not guaranteed by this project.

## Accepted inputs

Any local source the host agent can read:

- PDF
- EPUB
- DOCX
- Markdown
- TXT
- page images or rendered books
- multi-file source collections
- books combined with interviews, shareholder letters, or course notes

## Supported book categories

### Technical analysis and short-term trading

Possible outputs include:

- candlestick-pattern skills
- moving-average and trend skills
- volume-price skills
- breakout and false-breakout skills
- swing and limit-up research skills
- entry, invalidation, exit, and risk skills

### Trading systems and risk management

Possible outputs include:

- position-sizing skills
- stop and exit skills
- market-regime skills
- trading-discipline skills
- anti-pattern and risk-veto skills

### Value investing and financial analysis

Possible outputs include:

- business-quality skills
- moat checklists
- financial-quality skills
- capital-allocation skills
- valuation frameworks
- downside-risk checklists

### Investor biographies, interviews, and shareholder letters

Biographical material is not forced into mechanical buy/sell formulas. It can become:

- investment-principle skills
- decision-framework skills
- circle-of-competence skills
- mistake-review skills
- psychology and discipline skills
- historical-context comparison skills
- limits-of-the-author's-view skills

## No OCR dependency

The project does not depend on Tesseract, PaddleOCR, or another OCR engine.

The agent follows this order:

1. Read the native text layer when the PDF, EPUB, or DOCX contains one.
2. Render pages containing charts, tables, annotations, or scanned content.
3. Use the host agent's multimodal capability to inspect the page image directly.
4. Convert visual content into structured evidence and skill workflows.
5. Record page numbers, figure identifiers, captions, and visual-confidence metadata.

For a large image-only book, cost and speed depend on the host agent's visual and context capabilities. If the host cannot inspect images, it must stop and report the missing capability rather than silently ignoring them.

## No mandatory human review

The default workflow does not require a person to review every candidate. This does not mean “no validation.”

The automated release gate performs:

1. structure mapping
2. multi-type extraction
3. source verification
4. text-figure consistency checks
5. deduplication and conflict analysis
6. counterexample and boundary completion
7. skill compilation
8. trigger and adversarial test generation
9. manifest, provenance, and format validation
10. low-confidence quarantine

Outputs are separated into:

- `installable/`: skills that pass the automated release gate
- `provisional/`: useful material with unresolved parameters or weak support
- `rejected/`: duplicate, unverifiable, purely narrative, or unsuitable candidates

The intended meaning of “no human review” is:

> The agent performs extraction, verification, and release gating automatically; uncertain material does not enter the default installable set.

## Output structure

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

Every first-level directory under `installable/` is an independently installable skill.

## Generated skill types

| Type | Purpose |
|---|---|
| `router` | Book-level entry point that routes requests to child skills |
| `concept` | Defines terminology and the author's intended meaning |
| `principle` | Provides principles and decision checklists |
| `pattern` | Describes candlestick, volume-price, trend, and visual analysis workflows |
| `strategy` | Defines prerequisites, triggers, filters, invalidation, exit, and risk |
| `risk_rule` | Checks liquidity, sizing, volatility, chasing, and stop risks |
| `anti_pattern` | Detects false breakouts, traps, and invalid setups |
| `market_regime` | Describes the market context in which a method applies |
| `fundamental` | Covers financials, business quality, valuation, and management |
| `decision_framework` | Converts the author's reasoning into a repeatable workflow |
| `biography_case` | Captures decisions, mistakes, principles, and historical context |
| `psychology` | Provides cognitive-bias and trading-discipline checks |

## Requirements for an installable skill

Every skill in `installable/` must contain:

- a clear `name` and `description`
- explicit trigger scenarios
- required inputs and tools
- repeatable steps
- an output contract
- applicability and non-applicability boundaries
- risks and counterexamples
- chapter and page references
- visual evidence when the source is image-based
- confidence metadata
- positive, negative, ambiguous, and adversarial trigger tests
- no guaranteed-return or deterministic investment claims

A strategy skill additionally requires:

- prerequisites
- required conditions
- confirmations
- vetoes
- invalidation
- exit or stop-using conditions
- required market-data fields
- unresolved-parameter declarations

## Typical workflow

```text
$books-to-stock-analysis-skill
Convert ./books/new-book.pdf into skills.
Requirements:
- write to ./generated-skills/new-book
- preserve chapter and page provenance
- inspect candlestick charts and page images directly
- do not use OCR
- do not analyze current stocks
- do not validate returns
- quarantine low-confidence candidates automatically
```

The agent should:

1. Check file access and image-inspection capability.
2. Build the source inventory, chapter structure, and page map.
3. Mark image-heavy, table-heavy, and strategy-heavy pages.
4. Read text and visual pages in bounded batches.
5. Build a candidate knowledge graph.
6. Detect the book category and appropriate skill types.
7. Merge duplicates while preserving multiple sources.
8. Keep undefined parameters explicit rather than inventing thresholds.
9. Generate skills.
10. Run the automated quality gate.
11. Separate installable, provisional, and rejected outputs.
12. Write a final generation report.

## Deterministic validation and packaging

After generation, run:

```bash
python scripts/validate_pack.py ./generated-skills/my-trading-book
python scripts/package_skills.py ./generated-skills/my-trading-book
```

The validator checks structure, skill frontmatter, provenance, trigger tests, visual-coverage declarations, guaranteed-return language, and accidental source-book inclusion. It does not understand the source and does not replace the agent's source and visual verification.

## Safety and copyright

Default export policy:

- Do not reproduce the full book.
- Do not export long continuous passages.
- Do not export source page images by default.
- Preserve provenance through chapter, page, and concise derived descriptions.
- Represent image content as structured descriptions or independently reconstructed diagrams.
- Keep commercial book files local to the user.
- Treat generated trading methods as structured representations of an author's ideas, not evidence of profitability.

## Out of scope

- live market data
- stock scanning
- backtesting
- using generated skills to analyze stocks
- installing generated outputs for the user
- broker connectivity
- automatic order execution
- portfolio management

## Repository refocus

The existing Trading Skill IR, safe DSL, and example evaluator can remain as optional output-validation utilities, but they should no longer be the primary product entry point.

The new primary path is:

```text
SKILL.md
  → book reading and visual understanding
  → automated extraction and verification
  → skill-pack compilation and validation
```

See:

- [`docs/OPTIMIZATION_DESIGN.md`](docs/OPTIMIZATION_DESIGN.md)
- [`references/OUTPUT_SPEC.md`](references/OUTPUT_SPEC.md)

> This README describes the target version, not a claim that every feature is already implemented. Releases should state the currently available stage clearly.

## License

Apache License 2.0.

The license covers original code and documentation in this repository. It does not cover user-provided books, images, data, or third-party content.
