#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报/月报自动生成器 - 命令行入口
"""

import argparse
import json
import sys
from pathlib import Path
from weekly_report_generator import ReportGenerator, ReportConfig


def main():
    parser = argparse.ArgumentParser(
        description="周报/月报自动生成器 - 从 Git 提交记录、任务系统、文档变更中提取工作成果"
    )
    
    parser.add_argument(
        "--type",
        choices=["weekly", "monthly"],
        default="weekly",
        help="报告类型：weekly(周报) 或 monthly(月报)"
    )
    
    parser.add_argument(
        "--start-date",
        help="报告起始日期 (YYYY-MM-DD)，不填则自动计算"
    )
    
    parser.add_argument(
        "--end-date",
        help="报告结束日期 (YYYY-MM-DD)，默认为今天"
    )
    
    parser.add_argument(
        "--repo",
        default=".",
        help="Git 仓库路径，默认为当前目录"
    )
    
    parser.add_argument(
        "--config",
        help="配置文件路径 (JSON 格式)"
    )
    
    parser.add_argument(
        "--output",
        help="输出文件路径，默认输出到控制台"
    )
    
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="不包含 Git 提交记录"
    )
    
    parser.add_argument(
        "--no-tasks",
        action="store_true",
        help="不包含任务信息"
    )
    
    parser.add_argument(
        "--no-docs",
        action="store_true",
        help="不包含文档变更"
    )
    
    parser.add_argument(
        "--author",
        help="汇报人姓名"
    )
    
    parser.add_argument(
        "--team",
        help="团队名称"
    )
    
    args = parser.parse_args()
    
    config = ReportConfig(
        report_type=args.type,
        start_date=args.start_date,
        end_date=args.end_date,
        git_repo_path=args.repo,
        include_git=not args.no_git,
        include_tasks=not args.no_tasks,
        include_documents=not args.no_docs,
        author_name=args.author or "",
        team_name=args.team or ""
    )
    
    if args.config:
        try:
            with open(args.config, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            config.highlights = data.get("highlights", [])
            config.challenges = data.get("challenges", [])
            config.plans = data.get("plans", [])
            
            if "author_name" in data and not config.author_name:
                config.author_name = data["author_name"]
            if "team_name" in data and not config.team_name:
                config.team_name = data["team_name"]
        except Exception as e:
            print(f"读取配置文件失败：{e}", file=sys.stderr)
    
    generator = ReportGenerator(config)
    report = generator.generate()
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已生成并保存到：{args.output}")
    else:
        print("\n" + "="*60)
        print(report)
        print("="*60)


if __name__ == "__main__":
    main()
