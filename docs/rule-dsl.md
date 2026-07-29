# Rule DSL

The MVP rule DSL uses familiar expression syntax while avoiding dynamic Python execution. Expressions are parsed into an AST and interpreted recursively with a strict whitelist.

## Supported

```text
close > recent_high
volume_ratio >= 1.5 and benchmark_up
not overextended
(close - ma20) / atr14 < 2.0
registered_function(value, 20)
```

## Rejected

```text
unknown_function()
object.__class__
values[0]
[x for x in values]
lambda x: x
```

The evaluator resolves only names supplied in the observation mapping. Missing names cause an explicit `ExpressionError`; they do not default to zero or false.

A host application may register deterministic, side-effect-free, look-ahead-safe, and resource-bounded functions through `SafeExpressionEvaluator(functions=...)`.
