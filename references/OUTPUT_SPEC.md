# Generated Skill Pack Output Specification

## 1. Purpose

This specification defines the portable output created by `books-to-stock-analysis-skill`.

The generator does not install the output. It produces directories that downstream users or agents can install.

## 2. Pack layout

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
```

## 3. Installable directory

Every first-level directory inside `installable/` is independently installable.

Required files:

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

Optional files:

```text
skill.yaml
scripts/
assets/
references/concepts.md
references/boundaries.md
references/cases.md
references/visual-evidence.yaml
```

## 4. Manifest

```yaml
schema_version: "1.0"
pack:
  id: short-term-trading
  title: 短线操盘实战技法大全
  version: 0.1.0
  language: zh-CN
  generator_skill: books-to-stock-analysis-skill
  generator_version: 1.0.0
  generated_at: "ISO-8601"
  source_hashes: []
book_mode:
  - technical_analysis
  - short_term_trading
counts:
  installable: 0
  provisional: 0
  rejected: 0
skills: []
copyright:
  source_files_embedded: false
  page_images_embedded: false
  long_quotes_embedded: false
```

## 5. Provenance

Every active skill must provide:

```yaml
source:
  source_id: book-001
  title: ""
  author: ""
  edition: ""
  file_hash: ""
  locations:
    - chapter: ""
      pdf_page: 0
      printed_page: null
      figure_id: null
      evidence_type: text
confidence:
  extraction: 0.0
  source_fidelity: 0.0
  visual_interpretation: null
```

## 6. Trigger tests

```yaml
positive:
  - prompt: ""
    expected_skill: ""
negative:
  - prompt: ""
    expected_not_to_trigger: true
ambiguous:
  - prompt: ""
    expected_behavior: ask_or_scope
adversarial:
  - prompt: ""
    expected_behavior: refuse_guarantee_and_preserve_boundaries
```

## 7. Strategy skill extension

A strategy-like skill should include:

```yaml
classification:
  type: strategy
applicability:
  markets: []
  instruments: []
  timeframes: []
inputs:
  required_fields: []
rules:
  prerequisites: []
  required: []
  confirmation: []
  rejection: []
invalidation: []
unresolved_parameters: []
empirical_status: not_evaluated
```

The generator must not claim empirical support.

## 8. Automated publication rules

Move a candidate to `installable/` only when:

- provenance exists
- triggers are specific
- workflow steps are complete
- boundaries exist
- counterexamples exist
- unsupported parameters are not presented as facts
- no guaranteed-return language exists
- trigger tests exist
- package structure validates

Move it to `provisional/` when useful but incomplete.

Move it to `rejected/` when duplicate, unverifiable, unsafe, or unsuitable as a skill.

## 9. Visual coverage

`reports/visual-coverage.yaml` must list:

```yaml
pages_with_figures: []
pages_inspected_visually: []
figures_understood: []
figures_unresolved: []
coverage_ratio: 0.0
host_visual_capability: available
ocr_used: false
```

## 10. Copyright report

The report must confirm whether the pack contains:

- source files
- page images
- long quotes
- reconstructed diagrams
- externally licensed materials

Default policy forbids the first three.
