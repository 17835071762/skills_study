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