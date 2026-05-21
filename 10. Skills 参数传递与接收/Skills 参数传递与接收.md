# Skills 参数传递与接收

## 核心概念

Skills **不像传统函数**那样接收显式参数，它通过 **Claude 的对话上下文**来感知输入信息。

## 前置条件：Skill 的正确位置

**这是最重要的一步！** 必须放在正确位置 Claude Code 才能识别。

```
你的项目文件夹/
└── .claude/
    └── skills/
        └── csv-analyzer/           # 技能名（与 SKILL.md 中的 name 一致）
            ├── SKILL.md            # 技能描述文件
            └── scripts/
                └── analyze.py      # 可执行脚本
```

## 完整实例：CSV 文件分析 Skill

这个 Skill 可以：读取 CSV 文件，分析指定列，输出统计摘要。

---

### 第一步：创建目录结构

在 PowerShell 中执行：

```powershell
# 进入你的项目目录
cd C:\Users\MECHREUO\Desktop\skills

# 创建技能目录
New-Item -ItemType Directory -Path ".claude\skills\csv-analyzer\scripts" -Force
```

---

### 第二步：创建 SKILL.md（完整内容）

**文件路径**：`.claude\skills\csv-analyzer\SKILL.md`

```markdown
---
name: csv-analyzer
description: 分析 CSV 文件，输出统计摘要。当用户提到 CSV、表格数据、分析文件时使用。
---

# CSV 文件分析器

## 功能说明

这个技能可以分析 CSV 文件，输出数据预览和统计信息。

## 输入要求

从对话中获取以下信息：
- **文件路径**：CSV 文件的路径（必填）
- **分析列**：要分析的列名（可选，不填则分析所有数值列）
- **显示行数**：预览显示多少行，默认 10 行

## 执行命令

```bash
python scripts/analyze.py <文件路径> --col <列名> --limit <行数>
```

## 输出示例

当用户执行分析后，脚本会输出如下内容：

```
文件：data.csv
总行数：4
列名：name, age, city

前 5 行数据：
  name  age city
0   张三   25   北京
1   李四   30   上海

统计摘要：
            age
count   4.00000
mean   29.50000
std     4.20317
min    25.00000
max    35.00000
```

## 使用说明

1. 用户提供 CSV 文件路径
2. 用户可选择指定分析列和显示行数
3. 运行上述命令
4. 将输出结果返回给用户
```

---

### 第三步：创建 analyze.py 脚本（完整内容）

**文件路径**：`.claude\skills\csv-analyzer\scripts\analyze.py`

```python
#!/usr/bin/env python3
"""
CSV 文件分析脚本

功能：读取 CSV 文件，输出数据预览和统计摘要
依赖：pip install pandas
用法：python analyze.py <文件路径> [--col 列名] [--limit 行数]
"""

import sys
import os
import argparse

# 检查 pandas 是否安装
try:
    import pandas as pd
except ImportError:
    print("错误：缺少 pandas 库")
    print("请运行：pip install pandas")
    sys.exit(1)


def validate_file(file_path):
    """验证文件是否存在且格式正确"""
    if not file_path:
        print("错误：未提供文件路径")
        return False

    if not os.path.exists(file_path):
        print(f"错误：文件不存在 → {file_path}")
        return False

    if not file_path.lower().endswith(('.csv', '.txt')):
        print(f"错误：文件格式不支持，期望 .csv，实际 → {file_path}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description="CSV 文件分析脚本")
    parser.add_argument("file", help="CSV 文件路径")
    parser.add_argument("--col", help="指定分析的列名（可选）")
    parser.add_argument("--limit", type=int, default=10,
                        help="显示的行数，默认 10")
    parser.add_argument("--verbose", action="store_true",
                        help="显示详细信息")

    args = parser.parse_args()

    if not validate_file(args.file):
        sys.exit(1)

    if args.verbose:
        print(f"[INFO] 正在读取文件：{args.file}", file=sys.stderr)

    try:
        df = pd.read_csv(args.file)
    except Exception as e:
        print(f"错误：无法读取文件 → {e}")
        sys.exit(1)

    # 输出基本信息
    print(f"\n文件：{args.file}")
    print(f"总行数：{len(df)}")
    print(f"列名：{', '.join(df.columns.tolist())}")

    # 按列筛选
    if args.col:
        if args.col not in df.columns:
            print(f"错误：列 '{args.col}' 不存在")
            print(f"可用的列：{', '.join(df.columns.tolist())}")
            sys.exit(1)
        df = df[[args.col]]

    # 输出数据预览
    print(f"\n前 {args.limit} 行数据：")
    print(df.head(args.limit).to_string())

    # 统计摘要
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        print("\n统计摘要：")
        print(df[numeric_cols].describe())
    else:
        print("\n注意：没有找到数值列，无法生成统计摘要")

    print("\n分析完成！")


if __name__ == "__main__":
    main()
```

---

### 第四步：测试脚本（手动验证）

```powershell
# 安装依赖
pip install pandas

# 创建测试 CSV 文件
cd C:\Users\MECHREUO\Desktop\skills
@"
name,age,city
张三,25,北京
李四,30,上海
王五,28,广州
赵六,35,深圳
"@ | Out-File -FilePath "data.csv" -Encoding utf8

# 运行脚本
python .claude\skills\csv-analyzer\scripts\analyze.py data.csv --verbose
```

---

### 第五步：在 Claude Code 中使用

```powershell
cd C:\Users\MECHREUO\Desktop\skills
claude
```

然后输入：

```
用 csv-analyzer 分析 data.csv 文件
```

---

## 最终目录结构

```
C:\Users\MECHREUO\Desktop\skills\
│
├── .claude\
│   └── skills\
│       └── csv-analyzer\
│           ├── SKILL.md
│           └── scripts\
│               └── analyze.py
│
├── data.csv                    # 测试数据
│
└── (你的其他文件)
```

---

## 关键点总结

| 要点           | 说明                                                 |
| -------------- | ---------------------------------------------------- |
| **Skill 位置** | 必须在 `.claude/skills/技能名/` 下                   |
| **参数获取**   | Claude 从对话上下文中提取文件路径、列名等            |
| **脚本参数**   | 使用 `argparse` 接收命令行参数                       |
| **输出示例**   | 放在 SKILL.md 的代码块中，让 Claude 知道预期输出格式 |
| **依赖检查**   | 在脚本中检查 pandas 并提示安装                       |