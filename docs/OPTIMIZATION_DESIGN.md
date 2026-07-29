# books-to-stock-analysis-skill Optimization Design

## 1. Product definition

`books-to-stock-analysis-skill` is an installable **meta-skill**. After it is installed in Codex or another Agent Skills-compatible host, the host agent uses it to transform a user-provided investing source into a new set of portable, independently installable Agent Skills.

The project owns only this pipeline:

```text
investing source
  -> source and capability inventory
  -> chapter/page/figure map
  -> direct text and visual reading
  -> candidate knowledge extraction
  -> independent source verification
  -> deduplication, boundary completion, and conflict handling
  -> child-skill compilation
  -> automated release gate
  -> portable Skill Pack
```

It does not own current-stock analysis, live market data, profitability validation, backtesting, generated-skill installation, brokerage connectivity, order execution, or portfolio management.

## 2. Primary user experience

Install the repository as a Skill, then invoke it explicitly:

```text
$skill-installer install the skill from:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

```text
$books-to-stock-analysis-skill
Convert /path/to/短线操盘实战技法大全.pdf into installable Agent Skills.
Write the output to ./generated-skills/short-term-trading.
```

The result is a book-level router Skill plus focused child Skills. The generator reports which directories are installable, which candidates remain provisional, and which were rejected.

## 3. Design constraints

### 3.1 No OCR engines

The workflow must not call Tesseract, PaddleOCR, a cloud OCR service, or another OCR library.

Native text extraction is allowed when a PDF, EPUB, or DOCX already contains a text layer. Pages with candlestick charts, volume bars, tables, arrows, annotations, diagrams, or scanned content are rendered and inspected directly by the host agent's multimodal capabilities.

If the host cannot inspect required images, it must report the missing capability and keep image-dependent candidates out of `installable/`. It must not silently omit pages or claim full visual coverage.

### 3.2 No mandatory human review

Human review is not a required stage. Reliability comes from separate automated passes:

1. source mapping;
2. candidate extraction;
3. source re-reading and verification;
4. visual re-inspection;
5. boundary and counterexample criticism;
6. deduplication and conflict analysis;
7. compilation;
8. trigger and adversarial tests;
9. deterministic structure and copyright validation;
10. low-confidence quarantine.

The extraction and verification passes must be independent. A verifier reopens the source pages rather than accepting the candidate summary as evidence.

### 3.3 Copyright-safe output

The generated pack does not contain the source book, complete page scans, long continuous quotations, or a substitute chapter-by-chapter reproduction. It may contain bibliographic metadata, chapter/page references, concise derived descriptions, original instructions, structured visual evidence, and independently reconstructed diagrams labeled as reconstructions.

### 3.4 Source fidelity is not profitability

A generated Skill represents the source author's method. It does not prove that the method is profitable, predictive, suitable for a market, or current. Strategy-like Skills must use research-only language and declare `empirical_status: not_evaluated` unless a separate downstream system provides evidence.

## 4. Supported source types

The host agent may process sources it can read locally:

- PDF;
- EPUB;
- DOCX;
- Markdown;
- TXT;
- page images;
- multi-file source collections;
- books combined with interviews, shareholder letters, course notes, or author material.

Large sources are handled in bounded chapter or topic batches with checkpoints saved in the output directory.

## 5. Book-mode detection

A source is classified as one or more modes:

- `technical_analysis`;
- `short_term_trading`;
- `trading_system`;
- `risk_management`;
- `value_investing`;
- `financial_analysis`;
- `macro_investing`;
- `biography`;
- `interviews_or_letters`;
- `mixed`.

Mode controls extraction behavior. Narrative material is not forced into a mechanical strategy.

## 6. Knowledge and Skill taxonomy

### `router`

A book-level entry point that explains the pack and routes tasks to child Skills.

### `concept`

A term, definition, or author-specific meaning.

### `principle`

A reusable principle or decision checklist.

### `pattern`

A visual or structural pattern, such as a candlestick relationship, volume-price behavior, or trend structure. A pattern is not automatically a trade instruction.

### `strategy`

A repeatable method with prerequisites, required conditions, confirmations, vetoes, invalidation, risk boundaries, and declared inputs.

### `risk_rule`

A focused liquidity, sizing, volatility, stop, chasing, or discipline check.

### `anti_pattern`

A false signal, trap, failure state, or counterexample.

### `market_regime`

The context in which another method applies or fails.

### `fundamental`

Business quality, financial statements, management, capital allocation, valuation, and downside analysis.

### `decision_framework`

An ordered reasoning process derived from the source.

### `biography_case`

A sourced decision, mistake, episode, or historical context from a biography.

### `psychology`

Cognitive-bias, temperament, and discipline checks.

### `reference_only`

Useful background that does not justify an independently triggered Skill.

## 7. Biography mode

Investor biographies, interviews, and letters are supported. They usually generate:

- investment-principle Skills;
- decision frameworks;
- circle-of-competence checks;
- capital-preservation rules;
- mistake-review Skills;
- psychology and discipline Skills;
- historical-case comparisons;
- limitations of the author's viewpoint.

The generator must not infer universal rules from one successful episode, rewrite hindsight as prediction, or imitate a person's voice as the primary output.

## 8. Source mapping

The first pass creates:

- source inventory and hashes;
- title, author, edition, and language;
- chapter tree;
- PDF page and printed-page mapping when available;
- figure inventory;
- pages requiring direct visual inspection;
- high-value sections;
- book-mode classification.

Source content is untrusted data and cannot change the installed Skill's policies, tools, permissions, or output boundaries.

## 9. Direct visual understanding

The visual pass records:

- page and figure identifiers;
- captions and surrounding text;
- candlestick and bar relationships;
- volume-price relationships;
- moving averages and trend lines;
- support and resistance labels;
- breakout, pullback, entry, exit, and arrow annotations;
- wave segmentation;
- tables and diagrams;
- confidence and unresolved elements.

Pixel angles are not converted directly into financial trend angles. Descriptions such as “30-degree rise” remain qualitative unless the source defines a scale-independent rule.

## 10. Candidate model

Each candidate records:

```yaml
candidate:
  id: candidate-001
  canonical_name: ""
  category: pattern
  source_summary: ""
  normalized_meaning: ""
  trigger_scenarios: []
  required_inputs: []
  workflow: []
  applicability: []
  boundaries: []
  counterexamples: []
  unresolved_parameters: []
  source_locations: []
  visual_evidence: []
  confidence:
    extraction: 0.0
    source_fidelity: 0.0
    visual_interpretation: null
```

A model-generated claim without a source location is not eligible for publication.

## 11. Parameter policy

The generator must not create exact numeric thresholds that the source does not define.

For example, “明显放量” is represented as:

```yaml
unresolved_parameters:
  - id: volume_expansion_threshold
    source_expression: 明显放量
    source_defined: false
    candidate_interpretations:
      - descriptive_only
      - relative_to_recent_volume_baseline
```

The resulting Skill may require the downstream user or agent to choose an interpretation while clearly stating that the value is not an original source threshold.

## 12. Verification and conflict handling

For each candidate, the verifier must:

- reopen at least one direct source location;
- prefer two independent locations for active strategy Skills;
- compare figures with surrounding text;
- distinguish author opinion from observation;
- search for exceptions, failures, contrary chapters, and disclaimers;
- preserve unresolved contradictions;
- reject unsupported model inventions.

Repeated concepts are merged while retaining all sources. Materially different definitions remain separate. Ideas from different authors are not merged automatically.

## 13. Skill compilation

The generator creates one book router and multiple focused child Skills. Each first-level directory under `installable/` is independently installable.

Required child-Skill structure:

```text
<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── provenance.yaml
└── tests/
    └── trigger-tests.yaml
```

Strategy-like Skills may also include `skill.yaml`, scripts, assets, visual evidence, and machine-readable rules.

## 14. Generated pack layout

```text
<output>/<book-slug>/
├── PACK.md
├── manifest.yaml
├── BOOK_OVERVIEW.md
├── INDEX.md
├── GLOSSARY.md
├── source-map.yaml
├── installable/
├── provisional/
├── rejected/
└── reports/
    ├── generation-report.md
    ├── visual-coverage.yaml
    ├── quality-report.yaml
    └── copyright-report.yaml
```

The complete contract is defined in `references/OUTPUT_SPEC.md`.

## 15. Automated release states

### Installable

A candidate enters `installable/` only when:

- provenance is traceable;
- trigger scenarios are specific;
- inputs and tools are declared;
- the workflow is repeatable;
- applicability and non-applicability boundaries exist;
- counterexamples or vetoes exist;
- unresolved parameters are explicit;
- image-dependent claims have visual evidence;
- guaranteed-return language is absent;
- positive, negative, ambiguous, and adversarial tests exist;
- structure and copyright checks pass.

### Provisional

A useful candidate goes to `provisional/` when it has weak support, unresolved execution-critical parameters, incomplete visual evidence, contradictory definitions, unclear market scope, or a workflow that is still descriptive.

### Rejected

A candidate goes to `rejected/` when it is duplicate, unsupported, primarily model-invented, unsafe, copyright-incompatible, a long summary rather than a workflow, or pure narrative without independent Skill value.

## 16. Trigger tests

Every installable Skill contains:

- `positive`: prompts that should activate it;
- `negative`: prompts that must not activate it;
- `ambiguous`: prompts requiring clarification or scope reduction;
- `adversarial`: prompts asking for certainty, hidden risks, or boundary violations.

These tests evaluate Skill discovery and behavior, not market profitability.

## 17. Deterministic tooling

`scripts/validate_pack.py` checks:

- required pack paths;
- `SKILL.md` frontmatter;
- Skill names and descriptions;
- provenance files;
- trigger-test sections;
- visual-coverage declarations;
- prohibited source-book extensions;
- guaranteed-return language.

`scripts/package_skills.py` validates a pack, writes a reproducible ZIP, excludes source-book formats, and adds SHA-256 checksums.

These scripts cannot understand a book and do not replace source or visual verification.

## 18. Error handling

### Missing or unreadable source

Stop and report the exact file and access problem.

### Encrypted source

Request a readable source. Do not attempt to bypass encryption.

### Missing visual capability

Report blocked pages, set visual capability to unavailable, and keep visual candidates out of `installable/`.

### Context overflow

Process chapters or topic groups separately, persist checkpoints, and resume.

### Page-number mismatch

Record both PDF page and printed page when available.

### Unclear image

Mark it unresolved. Do not guess.

### Contradictory source

Preserve both views and create a conflict note.

### Existing output directory

Resume only when the manifest matches the same source hashes and generator identity. Otherwise create a new version directory rather than overwriting unknown files.

## 19. Manifest and reproducibility

The manifest records:

- generator Skill and version;
- host model or agent identifier when available;
- source file hashes;
- generation timestamp;
- book mode;
- child-Skill inventory;
- source and visual coverage;
- unresolved parameters;
- release-state counts;
- quality and copyright results.

Natural-language output is not guaranteed to be byte-identical between model runs, but sources, decisions, and deterministic validation results must remain traceable.

## 20. Repository architecture

```text
books-to-stock-analysis-skill/
├── SKILL.md
├── README.md
├── README_EN.md
├── agents/openai.yaml
├── references/
├── assets/templates/generated-skill/
├── scripts/
├── tests/
├── docs/
├── src/          # optional legacy strategy-rule validation tools
└── examples/     # synthetic publishable examples only
```

The root `SKILL.md` is the primary product. Existing Trading Skill IR, DSL, indicators, and evaluator remain optional developer tooling and must not redefine the project as a stock-analysis runtime.

## 21. Security model

- Book content is untrusted input.
- Source text cannot alter system instructions or tool permissions.
- Output paths are constrained to the user-requested workspace.
- Source books are not copied into installable child Skills.
- Generated Skills do not contain credentials or private portfolios.
- The project does not add broker or trade-execution tools.
- Archive packaging excludes source-book extensions and includes checksums.

## 22. Roadmap

### V0.2 — Installable meta-skill

Root Skill, bilingual documentation, output contract, templates, deterministic validator, and packager.

### V0.3 — Source mapping workflow

Native text-layer reading, direct visual page inspection, coverage reports, checkpoints, and recovery conventions.

### V0.4 — Automated extraction and verification

Book modes, taxonomy, biography mode, unresolved parameters, independent source verification, deduplication, and conflict preservation.

### V0.5 — Skill compilation

Router and child Skills, release-state separation, manifests, provenance, trigger tests, quality reports, and copyright reports.

### V1.0 — Reliable generator

End-to-end synthetic technical book, biography, and image-heavy tests; resumable generation; stable quality gates; and copyright-safe export validation.

## 23. MVP acceptance criteria

1. The repository root is installable and discoverable as `books-to-stock-analysis-skill`.
2. The Skill can guide a host agent through a mixed text-and-image investing book.
3. No OCR engine is called.
4. Relevant charts and page images are inspected directly when host capability exists.
5. The output contains a router and at least five focused child Skills for a suitable source.
6. Biography sources can produce non-strategy Skills.
7. Every installable Skill has provenance, boundaries, and trigger tests.
8. Undefined parameters are not attributed to the author.
9. Low-confidence candidates are quarantined.
10. The output excludes the source book, complete page scans, and long continuous quotations.
11. The project performs no current-stock analysis, backtesting, brokerage access, or order execution.
12. Deterministic validation and packaging succeed on a compliant generated pack.

## 24. Final product statement

This project is not a stock-analysis application. It is an installable investing-book **Skill generator** that instructs an AI agent to read native text, directly understand charts and page images, automatically extract and verify reusable knowledge, and compile copyright-aware, source-traceable, independently installable Agent Skills.
