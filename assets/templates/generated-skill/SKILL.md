---
name: generated-skill-name
description: Describe the exact tasks that should trigger this generated skill and the boundaries that distinguish it from neighboring skills.
version: 0.1.0
user-invocable: true
platforms: [macos, linux, windows]
metadata: {"hermes":{"tags":["investing","book-derived"]},"openclaw":{"tags":["investing","book-derived"]}}
---

# Goal

State the reusable capability derived from the source.

# Use when

- Add specific trigger scenarios.

# Required inputs

- Declare every input the downstream agent must obtain.

# Workflow

1. Follow a repeatable sequence.
2. Preserve source-defined boundaries.
3. Surface missing information and unresolved parameters.
4. Report counterexamples and invalidation conditions.

# Output

Define the required output structure.

# Boundaries

- Do not claim guaranteed returns.
- Do not turn a method match into an automatic trade instruction.
- Do not attribute invented thresholds to the author.

# Sources

Load `references/provenance.yaml` when source verification is needed.
