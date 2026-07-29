# Automated Quality Gate

Human review is not mandatory, so publication requires a strict automated gate.

## Installable requirements

A candidate may enter `installable/` only when all checks pass:

- source locations are present and readable;
- the name and description are specific;
- trigger scenarios are explicit;
- required inputs and tools are declared;
- the workflow is repeatable;
- applicability and non-applicability boundaries exist;
- counterexamples, vetoes, or failure states exist;
- undefined numeric parameters remain unresolved rather than invented;
- image-dependent claims have visual evidence and coverage records;
- no guaranteed-return or deterministic investment language is present;
- positive, negative, ambiguous, and adversarial trigger tests exist;
- the output follows `OUTPUT_SPEC.md`;
- copyright checks pass.

## Provisional conditions

Place a candidate in `provisional/` when it is useful but one or more of the following remains:

- only one weak source location;
- unclear or contradictory author definitions;
- unresolved parameters that materially affect execution;
- incomplete visual evidence;
- uncertain applicability by market or timeframe;
- a descriptive idea that cannot yet be made repeatable.

## Rejected conditions

Place a candidate in `rejected/` when it is:

- duplicate without additional value;
- unsupported by the source;
- created primarily by model invention;
- unsafe or framed as guaranteed profit;
- a long summary rather than a reusable workflow;
- copyright-incompatible;
- pure narrative without an independently useful decision process.

## Independent verification passes

The extraction pass and verification pass must be separate. The verifier must reopen source pages instead of validating only the candidate summary. A boundary critic must actively search for exceptions, contrary chapters, failed examples, and author disclaimers.
