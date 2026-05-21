#!/usr/bin/env python3
"""
JSON Schema 验证脚本

功能：根据 JSON Schema 验证 JSON 数据文件
依赖：pip install jsonschema
用法：python scripts/validate_schema.py --schema schema.json --data data.json
"""

import json
import sys
import argparse

# 尝试导入 jsonschema 库
try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("错误：缺少 jsonschema 库", file=sys.stderr)
    print("请运行：pip install jsonschema", file=sys.stderr)
    sys.exit(1)


def load_json_file(filepath):
    """加载 JSON 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到文件 {filepath}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：{filepath} 不是有效的 JSON 文件", file=sys.stderr)
        print(f"详细信息：{e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='根据 JSON Schema 验证 JSON 数据')
    parser.add_argument('--schema', required=True, help='Schema 文件路径')
    parser.add_argument('--data', required=True, help='JSON 数据文件路径')
    parser.add_argument('--verbose', action='store_true', help='显示详细信息')

    args = parser.parse_args()

    # 加载文件
    schema = load_json_file(args.schema)
    data = load_json_file(args.data)

    if args.verbose:
        print(f"Schema: {args.schema}", file=sys.stderr)
        print(f"Data: {args.data}", file=sys.stderr)

    # 执行验证
    try:
        validate(instance=data, schema=schema)
        # 验证成功，输出 JSON 格式结果
        result = {
            "valid": True,
            "message": "验证通过"
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    except ValidationError as e:
        # 验证失败，输出详细的错误信息
        result = {
            "valid": False,
            "message": "验证失败",
            "error": {
                "path": ".".join(str(p) for p in e.path) if e.path else "根节点",
                "message": e.message,
                "schema_path": ".".join(str(p) for p in e.schema_path)
            }
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()