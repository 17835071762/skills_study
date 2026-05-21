您说得对，文档确实缺少了关键信息：**Skill 应该放在哪里才能被 Claude Code 识别**。我来修正这个问题。

---

# Skills 脚本扩展

除了在 `SKILL.md` 中编写指令外，你还可以通过 `scripts` 目录为技能添加可执行代码。

## 为什么使用脚本

- 封装复杂逻辑，避免在 `SKILL.md` 中写大量代码
- 提供经过测试的可靠实现
- 让代理可以重复使用相同的工具和函数

## 前置条件：Skill 放在哪里？

**这是最重要的一步！** Claude Code 只认以下两个位置：

| 类型             | 路径                                | 说明             |
| ---------------- | ----------------------------------- | ---------------- |
| **项目级 Skill** | `项目根目录/.claude/skills/技能名/` | 只对当前项目生效 |
| **用户级 Skill** | `~/.claude/skills/技能名/`          | 对所有项目生效   |

> ⚠️ **注意**：`技能名` 文件夹的名称必须与 `SKILL.md` 中的 `name` 字段一致。

### 示例：创建项目级 Skill

假设你的项目在 `C:\my-project`：

```
C:\my-project\
├── .claude\                    ← 创建这个文件夹
│   └── skills\                 ← 创建这个文件夹
│       └── json-validator\     ← 技能文件夹，名称与 name 一致
│           ├── SKILL.md
│           └── scripts\
│               └── validate_schema.py
└── (你的其他项目文件)
```

### 快速创建命令

```bash
cd C:\my-project
mkdir .claude\skills\json-validator\scripts
# 然后把 SKILL.md 和脚本放进去
```

## 脚本目录结构

```
my-skill/
├── SKILL.md
└── scripts/
    ├── process.py
    └── helper.js
```

## 完整示例：JSON 数据验证技能

### 第一步：创建正确的目录结构

```bash
# 进入你的项目目录
cd C:\Users\MECHREUO\Desktop\skills

# 创建 Claude Code 识别的技能目录
mkdir .claude\skills\json-validator\scripts
```

### 第二步：创建脚本文件

**文件位置**：`.claude/skills/json-validator/scripts/validate_schema.py`

```python
#!/usr/bin/env python3
"""
JSON Schema 验证脚本

依赖：pip install jsonschema
用法：python scripts/validate_schema.py --schema schema.json --data data.json
"""

import json
import sys
import argparse

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print(json.dumps({"valid": False, "error": "缺少 jsonschema 库，请运行: pip install jsonschema"}))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='JSON Schema 验证')
    parser.add_argument('--schema', required=True)
    parser.add_argument('--data', required=True)
    args = parser.parse_args()

    with open(args.schema, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        validate(instance=data, schema=schema)
        print(json.dumps({"valid": True, "message": "验证通过"}))
        sys.exit(0)
    except ValidationError as e:
        print(json.dumps({
            "valid": False,
            "message": "验证失败",
            "error": {"path": ".".join(str(p) for p in e.path), "message": e.message}
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 第三步：创建 SKILL.md

**文件位置**：`.claude/skills/json-validator/SKILL.md`

```markdown
---
name: json-validator
description: 根据 JSON Schema 验证 JSON 数据文件。当用户需要验证 JSON 数据或检查 JSON 格式时使用。
---

# JSON Schema 验证

## 使用方法

```bash
python scripts/validate_schema.py --schema <schema文件> --data <数据文件>
```

## 示例

```bash
python scripts/validate_schema.py --schema user-schema.json --data user.json
```

## 输出格式

成功：`{"valid": true, "message": "验证通过"}`

失败：`{"valid": false, "message": "验证失败", "error": {...}}`
```

### 第四步：测试

```bash
# 在项目根目录下
cd C:\Users\MECHREUO\Desktop\skills
claude
```

然后在 Claude Code 中输入：

```
用 json-validator 验证 json-test/user-valid.json
```

## 常见错误

| 错误             | 原因     | 解决                                   |
| ---------------- | -------- | -------------------------------------- |
| Skill 没有被加载 | 目录不对 | 检查是否在 `.claude/skills/技能名/` 下 |
| 找不到脚本       | 路径不对 | 使用 `scripts/xxx.py`，不要用绝对路径  |
| 脚本报错         | 缺少依赖 | 先运行 `pip install jsonschema`        |

## 脚本编写规范

| 要点           | 说明                                  |
| -------------- | ------------------------------------- |
| **位置正确**   | 放在 `.claude/skills/技能名/scripts/` |
| **自包含**     | 在脚本中检查依赖                      |
| **结构化输出** | 使用 JSON 格式输出                    |
| **避免交互**   | 所有输入通过命令行参数传入            |

---

**核心要点**：Skill 必须放在 `.claude/skills/技能名/` 目录下，Claude Code 才能识别。