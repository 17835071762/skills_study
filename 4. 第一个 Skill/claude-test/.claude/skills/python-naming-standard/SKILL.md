---
name: python-naming-standard
description: 当用户要求重构、审查或编写 Python 代码时，应用内部命名规范：内部辅助函数以 `_internal_` 前缀命名，并对不符合规则的代码提出修改建议。
---

## 指令
1. 所有的内部辅助函数必须以 `_internal_` 前缀命名。
2. 如果发现不符合此规则的代码，请自动提出修改建议。


## 参考示例
- 正确：`def _internal_calculate_risk():`
- 错误：`def _calculate_risk():`
