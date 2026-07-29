# Host Activation

Generated Skills must be usable without asking the user to perform a second manual installation.

The Skill uses two activation layers:

1. **Native activation** — copy accepted child Skills into the active host's recognized Skill directory.
2. **Same-session routing** — immediately load the generated router and manifest, so the parent Skill can use child Skills even if the host has not refreshed its native Skill index yet.

## Resolve bundled tools

Resolve `<skill-base>` as the directory containing the loaded parent `SKILL.md`.

Never assume the current working directory is the repository or installed Skill directory. Invoke bundled scripts with absolute paths derived from `<skill-base>`:

```bash
python "<skill-base>/scripts/validate_pack.py" "<pack>"
python "<skill-base>/scripts/activate_pack.py" "<pack>" \
  --host "<codex|openclaw|hermes|claude-code>" \
  --workspace "<workspace>"
```

## Common rule

Do not tell the user to install each generated child Skill.

Every activated child Skill keeps the same directory name as its `name` frontmatter. Existing different content is not overwritten unless `--force` is explicitly selected.

## Codex

Default project target:

```text
<workspace>/.agents/skills/<skill-name>/SKILL.md
```

Global target:

```text
~/.agents/skills/<skill-name>/SKILL.md
```

Codex discovers project Skills under `.agents/skills`. After native discovery, invoke a generated Skill with:

```text
$<skill-name>
```

A new Codex session or restart may be required before a newly written Skill appears in the native Skills list. Until then, the parent Skill must keep the generated router loaded and use the child Skills through same-session routing.

Install this repository in Codex by telling Codex:

```text
Install this Skill for me:
https://github.com/ACBBZ/books-to-stock-analysis-skill
```

or with the built-in installer:

```text
$skill-installer install https://github.com/ACBBZ/books-to-stock-analysis-skill
```

## OpenClaw

Default project target:

```text
<workspace>/.agents/skills/<skill-name>/SKILL.md
```

OpenClaw recognizes project-agent Skills under `.agents/skills`. The parent Skill must also keep the generated router loaded for the current session because native slash-command discovery can depend on the active Skill snapshot.

Global activation can target:

```text
$OPENCLAW_STATE_DIR/skills/
```

or, when `OPENCLAW_STATE_DIR` is unset:

```text
~/.openclaw/skills/
```

OpenClaw invocation:

```text
/books-to-stock-analysis-skill
```

## Hermes Agent

Default target:

```text
$HERMES_HOME/skills/<skill-name>/SKILL.md
```

or, when `HERMES_HOME` is unset:

```text
~/.hermes/skills/<skill-name>/SKILL.md
```

Hermes uses this directory as its primary Skill store. When the host exposes `skill_manage`, the parent Skill may use it instead of raw file copying. The parent Skill must still load the generated router immediately for the current session.

A project-scoped alternative is:

```text
<workspace>/.agents/skills/
```

but Hermes must have that absolute path configured under `skills.external_dirs` in `~/.hermes/config.yaml`.

Hermes invocation:

```text
/books-to-stock-analysis-skill
```

## Claude Code

Default project target:

```text
<workspace>/.claude/skills/<skill-name>/SKILL.md
```

Claude Code monitors existing personal and project Skill roots for changes and normally hot-loads new child Skills in the current session. If the top-level `.claude/skills` directory did not exist when the session started, the parent Skill remains the same-session fallback.

Global activation can target:

```text
~/.claude/skills/
```

Claude Code invocation:

```text
/books-to-stock-analysis-skill
```

## Same-session routing

After native activation, the parent Skill must:

1. Open `<pack>/manifest.yaml`.
2. Locate the book-level router under `<pack>/installable/`.
3. Open the router's `SKILL.md`.
4. Keep the router and child-Skill index available for follow-up requests.
5. When a follow-up matches a child Skill, open that child's `SKILL.md` and required references.
6. Follow it directly even if the host has not yet exposed a native command.

This is not a second installation. It is the continuation of the same generation workflow.

## Activation report

Write `<pack>/reports/activation-report.yaml`:

```yaml
schema_version: "1.0"
host: codex
target_root: "/workspace/.agents/skills"
activated:
  - book-router
  - volume-price-breakout
unchanged: []
warnings: []
```

## Safety

- Reject symlinks inside generated child Skills.
- Do not copy original books into host Skill directories.
- Do not overwrite a different existing Skill unless replacement is explicit.
- Preserve provenance, trigger tests, and supporting references.
- Do not write to more than one host root unless the user asks for multi-host activation.
