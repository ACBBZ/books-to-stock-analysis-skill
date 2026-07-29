# Host Activation

Generated skills must be usable without asking the user to perform a second manual installation.

The meta-skill therefore uses two activation layers:

1. **Native activation** — copy accepted child skills into the active host's recognized skill directory.
2. **Same-session routing** — immediately load the generated router and manifest, so the parent meta-skill can use child skills even if the host has not refreshed its native skill index yet.

## Common rule

After a pack passes validation:

```bash
python scripts/activate_pack.py <pack> \
  --host <openclaw|hermes|claude-code> \
  --workspace <workspace>
```

Do not tell the user to install each generated child skill.

Every activated child skill keeps the same directory name as its `name` frontmatter. Existing different content is not overwritten unless `--force` is explicitly selected.

## OpenClaw

Default project target:

```text
<workspace>/.agents/skills/<skill-name>/SKILL.md
```

OpenClaw recognizes project-agent skills under `.agents/skills`. The meta-skill must also keep the generated router loaded for the current session because native slash-command discovery can depend on the active skill snapshot.

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

Hermes uses this directory as its primary skill store. When the host exposes `skill_manage`, the meta-skill may use it instead of raw file copying. The parent meta-skill must still load the generated router immediately for the current session.

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

Claude Code monitors existing personal and project skill roots for changes and normally hot-loads new child skills in the current session. If the top-level `.claude/skills` directory did not exist when the session started, the parent meta-skill remains the same-session fallback.

Global activation can target:

```text
~/.claude/skills/
```

Claude Code invocation:

```text
/books-to-stock-analysis-skill
```

## Same-session routing

After native activation, the meta-skill must:

1. Open `<pack>/manifest.yaml`.
2. Locate the book-level router under `<pack>/installable/`.
3. Open the router's `SKILL.md`.
4. Keep the router and child-skill index available for follow-up requests.
5. When a follow-up matches a child skill, open that child's `SKILL.md` and required references.
6. Follow it directly even if the host has not yet exposed a native slash command.

This is not a second installation. It is the continuation of the same generation workflow.

## Activation report

Write `<pack>/reports/activation-report.yaml`:

```yaml
schema_version: "1.0"
host: claude-code
target_root: "/workspace/.claude/skills"
activated:
  - book-router
  - volume-price-breakout
unchanged: []
warnings: []
```

## Safety

- Reject symlinks inside generated child skills.
- Do not copy original books into host skill directories.
- Do not overwrite a different existing skill unless replacement is explicit.
- Preserve provenance, trigger tests, and supporting references.
- Do not write to more than one host root unless the user asks for multi-host activation.
