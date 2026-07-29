# Generated Skill Pack Output Specification

## 1. Purpose

This specification defines the output created by `books-to-stock-analysis-skill`.

The pack is portable, and accepted child Skills are activated automatically for the current Codex, OpenClaw, Hermes Agent, or Claude Code host. Users must not be asked to install generated Skills one by one.

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
    ├── generation-report.md
    ├── visual-coverage.yaml
    ├── quality-report.yaml
    ├── copyright-report.yaml
    └── activation-report.yaml
```

`installable/` contains the canonical accepted child-Skill sources. The activation step copies them into the current host's native Skill root.

## 3. Child Skill layout

Every first-level directory inside `installable/` is an independent Agent Skill.

Required files:

```text
<skill-name>/
├── SKILL.md
├── references/
│   └── provenance.yaml
└── tests/
    └── trigger-tests.yaml
```

Optional files:

```text
skill.yaml
agents/
scripts/
assets/
references/concepts.md
references/boundaries.md
references/cases.md
references/visual-evidence.yaml
```

`SKILL.md` is the portable source of truth. Host-specific files such as `agents/openai.yaml` are optional and must not be required for Codex, OpenClaw, Hermes, or Claude Code compatibility.

## 4. Portable SKILL.md frontmatter

Recommended frontmatter:

```yaml
---
name: volume-price-breakout
description: Explain exactly what tasks should trigger this source-grounded Skill and when it should not be used.
version: 0.1.0
user-invocable: true
platforms: [macos, linux, windows]
metadata: {"hermes":{"tags":["investing","book-derived"]},"openclaw":{"tags":["investing","book-derived"]}}
---
```

Only `name` and `description` are required by the pack validator. Additional fields improve host behavior but must remain parseable by AgentSkills-compatible hosts.

## 5. Manifest

```yaml
schema_version: "1.1"
pack:
  id: short-term-trading
  title: 短线操盘实战技法大全
  version: 0.1.0
  language: zh-CN
  generator_skill: books-to-stock-analysis-skill
  generator_version: 0.3.2
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
activation:
  requested: true
  host: codex
  scope: project
  same_session_router: true
copyright:
  source_files_embedded: false
  page_images_embedded: false
  long_quotes_embedded: false
```

## 6. Provenance

Every accepted child Skill must provide:

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

## 7. Trigger tests

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

## 8. Strategy extension

A strategy-like Skill should include:

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

## 9. Automated publication rules

Move a candidate to `installable/` only when:

- provenance exists
- triggers are specific
- workflow steps are complete
- boundaries and counterexamples exist
- unsupported parameters are not presented as facts
- no guaranteed-return language exists
- trigger tests exist
- package structure validates

Move it to `provisional/` when useful but incomplete.

Move it to `rejected/` when duplicate, unverifiable, unsafe, or unsuitable as a Skill.

## 10. Activation

After validation, call:

```bash
python scripts/activate_pack.py <pack> \
  --host <codex|openclaw|hermes|claude-code> \
  --workspace <workspace>
```

Default targets:

| Host | Default target |
|---|---|
| Codex | `<workspace>/.agents/skills/` |
| OpenClaw | `<workspace>/.agents/skills/` |
| Claude Code | `<workspace>/.claude/skills/` |
| Hermes Agent | `$HERMES_HOME/skills/` or `~/.hermes/skills/` |

The parent Skill must immediately load the book-level router and manifest after activation. This allows same-session use even if native host discovery has not refreshed yet.

`reports/activation-report.yaml` must record:

```yaml
schema_version: "1.0"
host: codex
target_root: "/workspace/.agents/skills"
activated: []
unchanged: []
warnings: []
```

See `references/HOST_ACTIVATION.md` for full behavior.

## 11. Visual coverage

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

## 12. Copyright report

The report must confirm whether the pack contains:

- source files
- page images
- long quotes
- reconstructed diagrams
- externally licensed materials

Default policy forbids source files, page images, and long quotes inside activated child-Skill directories.
