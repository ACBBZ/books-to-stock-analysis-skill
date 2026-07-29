# TradeSkillForge Design

## 1. Purpose

TradeSkillForge compiles reviewed knowledge from stock-trading books into portable Agent Skills and deterministic analysis rules. The output is not a book summary. Each published skill must declare what it means, which market data it needs, when it applies, what invalidates it, how it is tested, and where it came from.

The project is a greenfield implementation. Public projects may inform general architectural choices, but their source code, prompts, and repository structures are not copied or forked.

## 2. Product boundary

The default mode is `research_only`.

The platform may:

- parse user-provided books in a private workspace;
- extract candidate concepts, patterns, strategies, risks, and counterexamples;
- compile reviewed knowledge into a Trading Skill IR;
- calculate deterministic technical features;
- evaluate skills against point-in-time stock data;
- produce reports containing evidence, contradictions, invalidation conditions, and provenance;
- run event studies and backtests with explicit assumptions.

The platform does not, by default:

- connect to a broker;
- submit orders;
- promise returns;
- treat a book claim as empirically valid;
- publish uploaded books or full page scans;
- let an LLM estimate indicators when deterministic tools are available.

## 3. Core principles

1. **Structure over summary.** Skills express triggers, boundaries, and workflows.
2. **Dual representation.** Agent-facing instructions and machine-facing rules coexist.
3. **Deterministic calculation.** Code computes indicators and conditions; models explain results.
4. **Evidence first.** Every result records the evaluated condition and observed outcome.
5. **Explicit uncertainty.** `insufficient_data`, `partial_match`, `conflicting_signals`, and `rejected` are valid outputs.
6. **Provenance.** Rules reference book, edition, pages, figures, extraction method, and review state.
7. **Fidelity is not validity.** `source_fidelity_score` and empirical support are separate.
8. **Human publication gate.** Automatically extracted trading rules remain drafts until reviewed.
9. **No look-ahead.** Features and tests must honor an explicit analysis timestamp.
10. **Copyright-aware exports.** Public packs contain derived rules and minimal references, not source books.

## 4. Target architecture

```text
Private book files
  -> page/layout/figure ingestion
  -> source fragments
  -> candidate knowledge extraction
  -> normalization and missing-parameter detection
  -> human review
  -> Trading Skill IR registry
  -> skill compiler
       -> SKILL.md package
       -> deterministic detector package
  -> market-data and feature engine
  -> skill runtime
  -> risk critic and report synthesis
  -> event study/backtest
  -> empirical rating
```

The Trading Skill IR is the source of truth. `SKILL.md`, JSON Schema, Python detectors, APIs, and reports are compilation targets.

## 5. Knowledge taxonomy

- `concept`: trend, support, resistance, volume-price divergence.
- `principle`: follow the trend, preserve capital, respect invalidation.
- `pattern`: double bottom, long lower shadow, volume breakout.
- `strategy`: prerequisites, trigger, filters, rejection, exit, and risk.
- `risk_rule`: liquidity, position size, volatility, stop and chase limits.
- `anti_pattern`: false breakout, high-volume stagnation, failed limit-up.
- `market_regime`: bull, bear, range, recovery, distribution.
- `execution_guideline`: market-open, close, auction, and order-timing constraints.
- `psychology`: discipline and decision checklists that do not directly create signals.

Only a unit with observable variables, clear applicability, invalidation, and testable examples should be promoted to an executable strategy.

## 6. Trading Skill IR

A skill document contains:

- identity and semantic version;
- classification and intents;
- market, instrument, timeframe, and regime scope;
- data contract and minimum history;
- required features;
- prerequisite, required, confirmation, and rejection rules;
- entry, invalidation, exit, and risk metadata in later schema versions;
- output states;
- source fragments and fidelity score;
- review and empirical status.

The MVP schema is implemented in `domain/models.py` and exported as `schemas/trading-skill.schema.json`.

## 7. Rule DSL

The rule language is deliberately smaller than Python. It supports constants, observation names, arithmetic, comparisons, boolean logic, and direct calls to registered pure functions. It rejects attribute access, arbitrary indexing, comprehensions, lambdas, imports, and unknown functions.

Expressions are parsed into an AST and interpreted recursively. They are never passed to Python dynamic execution functions. Hosts registering functions are responsible for determinism, bounded resources, and look-ahead safety.

## 8. Book ingestion design

A later ingestion service will create a page model containing blocks, reading order, headings, paragraphs, tables, figures, captions, and page-number mappings. Source fragments will follow semantic boundaries such as a named technique, a chart plus its explanation, or a risk warning rather than fixed token lengths.

Figure processing will identify candlesticks, volume bars, moving averages, trend lines, arrows, support/resistance labels, and captions. Visual descriptions such as “30-degree rise” will not use screenshot pixel angles. They will be normalized into log-price slope, return per unit time, ATR-normalized slope, trend duration, regression fit, and drawdown.

Book content is untrusted input and cannot change tool permissions or runtime policy.

## 9. Extraction and review

Specialized extractors propose concepts, principles, patterns, strategies, risks, and counterexamples. A candidate records its original statement, normalized statement, observable variables, assumptions, missing parameters, confidence, and source references.

The review workflow supports approve, revise, reject, merge, split, downgrade to concept, mark obsolete, and require empirical validation. Missing thresholds remain explicitly unresolved; the model must not silently invent them.

Publication lifecycle:

```text
draft -> extracted -> normalized -> reviewed -> compiled -> tested -> published -> deprecated
```

Only published skills are selected by default routing.

## 10. Market data and features

A standard bar schema will include symbol, market, timestamp, timeframe, OHLC, volume, amount, turnover, VWAP, previous close, adjustment factor, trade status, price limits, source, and ingestion time.

Every analysis records a data snapshot checksum and as-of timestamp. A-share market rules such as trading calendar, suspension, ST treatment, price limits, ex-rights events, and T+1 constraints belong in a versioned `MarketProfile`, not inside individual book skills.

The feature engine is deterministic, cacheable, serializable, and independently tested. The MVP implements SMA, rolling high, volume ratio, ATR, and normalized log-price slope.

## 11. Runtime and skill composition

The runtime evaluates in this order:

1. data and prerequisite gates;
2. required conditions;
3. rejection vetoes;
4. weighted confirmation conditions;
5. evidence and contradiction collection;
6. structured result generation.

Future orchestration roles are:

- `SkillRouter`: selects applicable published skills;
- `DataPlanner`: resolves required symbols, benchmarks, fields, and timeframes;
- `TechnicalEvaluator`: calls deterministic detectors;
- `RiskCritic`: finds contradictions, invalidation, data issues, and overfitting risks;
- `ReportSynthesizer`: writes an evidence-based research report.

Skills form a graph with prerequisite, confirmation, conflict, and veto edges. Conflicting results are reported, not averaged away.

## 12. Result semantics

The MVP returns:

- `matched`: all required and confirmation rules pass;
- `partial_match`: required rules pass but some confirmations fail;
- `not_matched`: one or more required rules fail;
- `rejected`: a veto rule is true;
- `insufficient_data`: a prerequisite fails.

`match_score` measures correspondence to the skill definition. It is not a probability of future return unless a separate probability-calibration process has been completed and documented.

## 13. Testing and empirical validation

Each published skill should eventually include positive, negative, boundary, missing-data, adversarial, and regime-conflict cases. Core properties include scale invariance for normalized patterns, deterministic replay, rejection of future data, and stable output for identical inputs.

Empirical validation is layered:

1. detector conformance;
2. human-labeled pattern validation;
3. event study;
4. strategy backtest with entries, exits, costs, and tradability;
5. robustness across periods, markets, industries, parameters, and costs.

Backtests must address look-ahead bias, survivorship bias, point-in-time constituents, corporate actions, suspensions, price-limit execution, slippage, multiple testing, sample separation, and walk-forward evaluation.

Empirical ratings are `unvalidated`, `descriptive_only`, `weak_evidence`, `mixed_evidence`, `supported`, `robust`, or `deprecated`.

## 14. Security and governance

- Private book formats and data directories are ignored by Git.
- Document parsers run with file-size and resource limits.
- Rule execution uses a whitelist and no arbitrary code execution.
- Secrets, brokerage credentials, and private portfolios are not accepted in public issues.
- Every analysis can export an audit bundle containing request, data manifest, skill manifest, rule results, agent trace, report, and checksums.
- Skill versions, parameter profiles, market profiles, data snapshots, model IDs, and prompt versions are recorded.

A future brokerage extension must be a separate opt-in module with human confirmation, position and loss limits, idempotent orders, pre-trade checks, reconciliation, audit logs, and an emergency stop.

## 15. Repository layout

```text
src/books_to_stock_analysis_skill/
  domain/       # Trading Skill IR
  dsl/          # safe expression interpretation
  features/     # deterministic indicators
  io/           # JSON/YAML adapters
  runtime/      # evaluation and evidence
examples/       # synthetic, publishable skill packs
schemas/        # machine-readable contracts
tests/          # unit and integration tests
docs/           # architecture, safety, DSL, and roadmap
```

## 16. Delivery milestones

- **M1:** IR, DSL, deterministic runtime, CLI, example, CI — current release.
- **M2:** versioned market data, detector registry, A-share market profile, look-ahead tests.
- **M3:** private PDF/page/figure ingestion and source-fragment store.
- **M4:** review workbench, unresolved parameters, compilation, publication gates.
- **M5:** event studies, walk-forward backtests, costs, and empirical ratings.
- **M6:** multi-skill routing, veto graph, risk critic, reports, and audit replay.

The project succeeds when a skill has a source, a precise definition, declared data, explicit boundaries, counterexamples, deterministic execution, tests, and reproducible evidence.
