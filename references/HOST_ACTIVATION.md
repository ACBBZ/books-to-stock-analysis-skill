# Host Activation

Generated skills must be usable without asking the user to perform a second manual installation.

The meta-skill uses two activation layers:

1. **Native activation** — copy accepted child skills into the active host's recognized skill directory.
2. **Same-session routing** — immediately load the generated router and manifest, so the parent meta-skill can use child skills even if the host has not refreshed its native skill index yet.

## Resolve bundled tools

Resolve `<skill-base>` as the directory containing the loaded parent `SKILL.md`.

Never assume the current working directory is the repository or installed Skill directory. Invoke bundled scripts with absolute paths derived from `<skill-base>`:

```bash
python "<skill-base>/scripts/validate_pack.py" "<pack>"
python "<skill-base>/scripts/activate_pack.py" "<pack>" \
  --host "<openclaw|hermes|claude-code>" \
  --workspace "<workspace>"
```

Do not tell the user to install each generated child skill.

Every activated child skill keeps the same directory name as its `name` frontmatter. Existing different content is not overwritten unless `--force` is explicitly selected.

## OpenClaw

Default project target:

```text
<workspace>/.agents/skills/<skill-name>/SKILL.md
```

Global activation can target:

```text
$OPENCLAW_STATE_DIR/skills/
```

or, when `OPENCLAW_STATE_DIR` is unset:

```text
~/.openclaw/skills/
```

The parent meta-skill keeps the generated router loaded because native slash-command discovery can depend on the host's active Skill snapshot.

Invocation:

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

When Hermes exposes `skill_manage`, the meta-skill may use it instead of raw file copying. It must still load the generated router immediately for the current session.

A project-scoped alternative is:

```text
<workspace>/.agents/skills/
```

Hermes must have that absolute path configured under `skills.external_dirs` in `~/.hermes/config.yaml`.

When installed from a direct `SKILL.md` URL, all relative bundled references and scripts listed by the parent Skill must be present. Missing resources are an incomplete installation error.

Invocation:

```text
/books-to-stock-analysis-skill
```

## Claude Code

Default project target:

```text
<workspace>/.claude/skills/<skill-name>/SKILL.md
```

Global activation can target:

```text
~/.claude/skills/
```

Claude Code normally hot-loads changes beneath existing personal and project Skill roots. If native discovery has not refreshed, the parent meta-skill remains the same-session fallback.

Invocation:

```text
/books-to-stock-analysis-skill
```

## Same-session routing

After native activation, the meta-skill must:

1. Open `<pack>/manifest.yaml`.
2. Locate the book-level router under `<pack>/installable/`.
3. Open the router's `SKILL.md`.
4. Keep the router and child-Skill index available for follow-up requests.
5. When a follow-up matches a child Skill, open that child's `SKILL.md` and required references.
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

- Validate the complete pack before activation.
- Reject symlinks inside generated child skills.
- Do not copy original books into host Skill directories.
- Do not overwrite a different existing Skill unless replacement is explicit.
- Preserve provenance, trigger tests, and supporting references.
- Do not write to more than one host root unless the user asks for multi-host activation.
