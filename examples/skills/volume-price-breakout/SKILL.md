---
name: volume-price-breakout
description: 当需要判断股票是否符合本项目定义的量价突破状态，并展示支持证据、反证和否决条件时使用。
---

# 目标

调用确定性运行时评估 `skill.yaml`，不要根据自然语言自行估算技术指标。

# 流程

1. 确认数据截至时间和复权方式。
2. 准备 `skill.yaml` 声明的观察字段。
3. 调用 `books-to-stock-skill evaluate` 或 Python `SkillEvaluator`。
4. 报告匹配状态、匹配分数、支持证据和反证。
5. 明确匹配分数不是未来收益概率。

# 禁止行为

- 不输出收益保证。
- 不把 `partial_match` 描述成确定买点。
- 不隐藏基准环境、过度延伸或数据不足等反证。
- 不连接券商或提交订单。
