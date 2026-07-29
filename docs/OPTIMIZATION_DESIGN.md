# books-to-stock-analysis-skill Optimization Design

## 1. Product definition

`books-to-stock-analysis-skill` is an installable Skill for Codex, OpenClaw, Hermes Agent, and Claude Code.

It converts a user-provided investing source into new Agent Skills and activates accepted child Skills automatically for the current host.

```text
investing source
  -> source and capability inventory
  -> chapter/page/figure map
  -> direct text and visual reading
  -> candidate knowledge extraction
  -> independent source verification
  -> deduplication, boundaries, and conflict handling
  -> child-Skill compilation
  -> automated quality gate
  -> host-native activation
  -> same-session use
```

The user installs only this Skill. Generated child Skills do not require a second manual installation step.

## 2. Supported hosts

### Codex

- Skill installation: tell Codex to install the GitHub repository, or use `$skill-installer` with the repository URL.
- Generated project Skills: `<workspace>/.agents/skills/`.
- Global generated Skills: `~/.agents/skills/`.
- Invocation after native discovery: `$books-to-stock-analysis-skill`.
- A new session or restart may be required to refresh the native Skill list.

### OpenClaw

- Skill installation: Git Skill installation.
- Generated project Skills: `<workspace>/.agents/skills/`.
- Global generated Skills: `$OPENCLAW_STATE_DIR/skills/` or `~/.openclaw/skills/`.
- Invocation: `/books-to-stock-analysis-skill`.

### Hermes Agent

- Skill installation: direct `SKILL.md` URL or another Hermes source.
- Generated Skills: `$HERMES_HOME/skills/` or `~/.hermes/skills/`.
- Optional project sharing: `.agents/skills/` configured through `skills.external_dirs`.
- Invocation: `/books-to-stock-analysis-skill`.

### Claude Code

- Skill installation: clone into `~/.claude/skills/` or project `.claude/skills/`.
- Generated project Skills: `<workspace>/.claude/skills/`.
- Global generated Skills: `~/.claude/skills/`.
- Invocation: `/books-to-stock-analysis-skill`.

## 3. Direct-use requirement

Generated Skills must be usable without asking the user to install them.

The design uses two mechanisms:

### Native activation

Accepted child-Skill directories are copied into the active host's native Skill root.

```bash
python scripts/activate_pack.py <pack> \
  --host <codex|openclaw|hermes|claude-code> \
  --workspace <workspace>
```

### Same-session routing

Some hosts snapshot their Skill catalog. Therefore the parent Skill must immediately load:

- the generated pack manifest
- the book-level router Skill
- the child-Skill index

When a follow-up request matches a generated child Skill, the parent opens and follows that child `SKILL.md` directly. Native host invocation is preferred after the host refreshes its catalog.

This lets the same agent continue using generated knowledge during the generation session.

## 4. Scope

The project owns:

- book and source reading
- direct page-image understanding without OCR
- candidate extraction
- source and visual verification
- Skill generation
- quality classification
- host activation
- same-session routing
- optional pack validation and packaging

The project does not own:

- current stock analysis
- live market data
- profitability backtesting
- broker integration
- order execution
- portfolio management

Generated child Skills may describe what data a downstream agent requires, but this project does not fetch or evaluate that data.

## 5. Source types

Supported sources include:

- PDF
- EPUB
- DOCX
- Markdown
- TXT
- page images
- multi-file collections
- books combined with interviews, shareholder letters, or course notes

## 6. No OCR policy

The generator does not call OCR engines.

Reading order:

1. Read native text layers when present.
2. Identify pages containing charts, tables, annotations, or scanned content.
3. Render and inspect those pages with the host agent's visual capability.
4. Convert visual content into structured evidence.
5. Record visual coverage and unresolved pages.

If the host cannot inspect required images, visual-dependent candidates must not enter the accepted set.

## 7. Knowledge taxonomy

Generated units may be:

- `router`
- `concept`
- `principle`
- `pattern`
- `strategy`
- `risk_rule`
- `anti_pattern`
- `market_regime`
- `fundamental`
- `decision_framework`
- `biography_case`
- `psychology`
- `reference_only`

Narrative books and biographies must not be forced into mechanical buy/sell strategies.

## 8. Automatic validation

No mandatory line-by-line human review is required, but accepted Skills must pass independent automatic checks:

1. source mapping
2. candidate extraction
3. source re-reading
4. visual re-check when applicable
5. deduplication and conflict analysis
6. boundary and counterexample completion
7. trigger and adversarial tests
8. structural validation
9. copyright checks
10. activation checks

Results are separated into:

- `installable/` — accepted and eligible for automatic activation
- `provisional/` — useful but incomplete or weakly supported
- `rejected/` — duplicate, unverifiable, unsafe, or unsuitable

## 9. Output model

```text
generated-skills/<book-slug>/
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

Every accepted child Skill requires:

```text
<skill-name>/
├── SKILL.md
├── references/provenance.yaml
└── tests/trigger-tests.yaml
```

Host-specific metadata files are optional. Portable `SKILL.md` is the source of truth.

## 10. Activation targets

| Host | Project target | Global target |
|---|---|---|
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| OpenClaw | `.agents/skills/` | `$OPENCLAW_STATE_DIR/skills/` or `~/.openclaw/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Hermes Agent | `.agents/skills/` with `external_dirs` | `$HERMES_HOME/skills/` or `~/.hermes/skills/` |

Default behavior:

- Codex: project target
- OpenClaw: project target
- Claude Code: project target
- Hermes: global Hermes Skill store

The activation tool refuses to overwrite different existing content unless `--force` is explicit and rejects symlinks in generated Skills.

## 11. Portable frontmatter

Generated `SKILL.md` files should use common AgentSkills fields and optional host metadata:

```yaml
---
name: skill-name
description: A precise description of what triggers this Skill and its boundaries.
version: 0.1.0
user-invocable: true
platforms: [macos, linux, windows]
metadata: {"hermes":{"tags":["investing","book-derived"]},"openclaw":{"tags":["investing","book-derived"]}}
---
```

The cross-host validator only requires `name` and `description`.

## 12. Safety and copyright

Generated and activated Skills must not:

- include the source book
- include source page scans by default
- contain long continuous quotations
- promise returns
- claim certainty
- present a method match as an automatic trade instruction
- imply empirical validation
- connect to a broker or submit an order

Source books remain outside host Skill directories.

## 13. Required reports

### Generation report

Records source files, book mode, counts, warnings, and unresolved parameters.

### Visual coverage report

Records pages and figures inspected directly and declares `ocr_used: false`.

### Quality report

Records accepted, provisional, and rejected candidates with reasons.

### Copyright report

Records whether source files, page images, long quotes, or reconstructed diagrams are included.

### Activation report

Records host, target root, activated Skills, unchanged Skills, and warnings.

## 14. Verification

Required deterministic commands:

```bash
pytest -q
python scripts/validate_pack.py <pack>
python scripts/activate_pack.py <pack> --host <host> --workspace <workspace>
python scripts/package_skills.py <pack>
```

Packaging is optional. Activation is part of the normal generation workflow.

## 15. Success criteria

The project succeeds when:

1. the Skill is installable on Codex, OpenClaw, Hermes, and Claude Code
2. the agent can read book text and directly inspect images without OCR
3. accepted child Skills preserve provenance and boundaries
4. low-confidence material is quarantined
5. generated Skills are activated automatically
6. the same agent can use them in the current session through the generated router
7. future sessions discover them through the host's native Skill directory
8. no second manual child-Skill installation is required
