#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报/月报自动生成器 - 测试脚本
"""

import os
import sys
from datetime import datetime, timedelta
from weekly_report_generator import (
    GitExtractor,
    TaskExtractor,
    DocumentChangeTracker,
    ReportGenerator,
    ReportConfig,
    GitCommit,
    TaskItem
)


def test_git_extractor():
    """测试 Git 提取器"""
    print("=" * 60)
    print("测试 Git 提取器")
    print("=" * 60)
    
    extractor = GitExtractor(".")
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    commits = extractor.get_commits(start_date, end_date)
    
    if commits:
        print(f"✓ 找到 {len(commits)} 条提交记录")
        print(f"  最新提交：{commits[0].message[:50]}")
        print(f"  提交者：{commits[0].author}")
        
        stats = extractor.get_commit_stats(commits)
        print(f"  总提交数：{stats.get('total_commits', 0)}")
        if stats.get('most_active_day'):
            print(f"  最活跃日期：{stats['most_active_day']}")
    else:
        print("⚠ 未找到提交记录（这可能是正常的，如果仓库没有最近的提交）")
    
    print()


def test_task_extractor():
    """测试任务提取器"""
    print("=" * 60)
    print("测试任务提取器")
    print("=" * 60)
    
    extractor = TaskExtractor()
    
    test_json = """
    {
      "tasks": [
        {
          "id": "TASK-001",
          "title": "测试任务 1",
          "status": "completed",
          "priority": "high"
        },
        {
          "id": "TASK-002",
          "title": "测试任务 2",
          "status": "pending",
          "priority": "medium"
        }
      ]
    }
    """
    
    with open("test_tasks.json", "w", encoding="utf-8") as f:
        f.write(test_json)
    
    tasks = extractor.extract_from_file("test_tasks.json")
    
    if tasks:
        print(f"✓ 成功提取 {len(tasks)} 个任务")
        for task in tasks:
            status_icon = "✅" if task.status == "completed" else "🔄"
            print(f"  {status_icon} [{task.id}] {task.title} ({task.priority})")
    else:
        print("✗ 任务提取失败")
    
    os.remove("test_tasks.json")
    print()


def test_document_tracker():
    """测试文档追踪器"""
    print("=" * 60)
    print("测试文档变更追踪器")
    print("=" * 60)
    
    tracker = DocumentChangeTracker(".")
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    changes = tracker.track_changes(start_date, end_date)
    
    if changes:
        print(f"✓ 找到 {len(changes)} 个文档变更")
        categorized = tracker.categorize_documents(changes)
        for category, docs in categorized.items():
            if docs:
                print(f"  {category}: {len(docs)} 个文件")
    else:
        print("⚠ 未找到文档变更（这可能是正常的）")
    
    print()


def test_report_generation():
    """测试报告生成"""
    print("=" * 60)
    print("测试报告生成")
    print("=" * 60)
    
    config = ReportConfig(
        report_type="weekly",
        author_name="测试用户",
        team_name="开发团队",
        highlights=[
            "完成了核心功能开发",
            "优化了系统性能"
        ],
        challenges=[
            "需要进一步优化数据库查询"
        ],
        plans=[
            "继续推进新功能开发",
            "准备技术分享"
        ]
    )
    
    generator = ReportGenerator(config)
    report = generator.generate()
    
    if report:
        print("✓ 报告生成成功")
        print("\n报告预览（前 500 字）：")
        print("-" * 60)
        print(report[:500])
        print("...")
        print("-" * 60)
    else:
        print("✗ 报告生成失败")
    
    print()


def test_full_workflow():
    """测试完整工作流"""
    print("=" * 60)
    print("测试完整工作流")
    print("=" * 60)
    
    config = ReportConfig(
        report_type="weekly",
        git_repo_path=".",
        include_git=True,
        include_tasks=True,
        include_documents=True,
        author_name="开发者",
        team_name="技术部",
        highlights=[],
        challenges=[],
        plans=[]
    )
    
    generator = ReportGenerator(config)
    report = generator.generate()
    
    print("✓ 完整工作流执行成功")
    print(f"  生成的报告长度：{len(report)} 字符")
    print()
    
    return report


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "周报/月报生成器 - 测试套件" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        test_git_extractor()
        test_task_extractor()
        test_document_tracker()
        test_report_generation()
        test_full_workflow()
        
        print("=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 测试过程中出现错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
