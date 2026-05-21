#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows C 盘清理工具 - 测试脚本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from windows_cleaner import (
    CleanerScanner,
    CleanerExecutor,
    SystemInfo,
    DiskAnalyzer,
    FileCleaner,
)

def test_system_info():
    """测试系统信息获取"""
    print("测试: 系统信息获取")
    print("-" * 40)

    info = SystemInfo()
    print(f"系统盘符: {info.get_system_drive()}")
    print(f"Windows 目录: {info.get_windows_dir()}")
    print(f"用户临时目录: {info.get_temp_dir()}")
    print(f"用户目录: {info.get_user_profile()}")
    print(f"管理员权限: {info.is_admin()}")

    browsers = info.get_browser_cache_paths()
    print(f"浏览器缓存路径:")
    for name, path in browsers.items():
        print(f"  - {name}: {path}")

    print()

def test_disk_analyzer():
    """测试磁盘分析"""
    print("测试: 磁盘分析")
    print("-" * 40)

    analyzer = DiskAnalyzer()

    # 测试大小格式化
    test_sizes = [1024, 1024*1024, 1024*1024*1024, 1024*1024*1024*2.5]
    print("大小格式化测试:")
    for size in test_sizes:
        print(f"  {size} 字节 = {analyzer.format_size(size)}")

    print()

def test_scanner():
    """测试扫描功能"""
    print("测试: 扫描功能")
    print("-" * 40)

    scanner = CleanerScanner()
    result = scanner.scan()

    print(f"扫描时间: {result.timestamp}")
    print(f"系统盘符: {result.system_drive}")
    print(f"总计占用: {DiskAnalyzer.format_size(result.total_size)}")
    print(f"文件总数: {result.total_files}")
    print()

    print("清理项列表:")
    for i, item in enumerate(result.items, 1):
        print(f"  {i}. {item.name}")
        print(f"     大小: {DiskAnalyzer.format_size(item.size)}")
        print(f"     文件数: {item.file_count}")
        print(f"     需要管理员: {'是' if item.requires_admin else '否'}")
        print()

def test_cleaner_executor():
    """测试清理执行器"""
    print("测试: 清理执行器")
    print("-" * 40)

    scanner = CleanerScanner()
    executor = CleanerExecutor()

    # 获取扫描结果
    scan_result = scanner.scan()

    # 只获取安全项
    safe_items = [item for item in scan_result.items if item.is_safe]

    print(f"找到 {len(safe_items)} 个安全清理项")
    print()

    # 模拟运行
    print("执行模拟清理 (--dry-run):")
    clean_result = executor.clean_items(safe_items, dry_run=True)

    print(f"  清理时间: {clean_result.timestamp}")
    print(f"  清理项目数: {len(clean_result.items_cleaned)}")
    print(f"  清理大小: {DiskAnalyzer.format_size(clean_result.cleaned_size)}")
    print(f"  清理文件数: {clean_result.cleaned_files}")

    if clean_result.failed_items:
        print(f"  失败项数: {len(clean_result.failed_items)}")

    print()

def test_file_cleaner():
    """测试文件清理器"""
    print("测试: 文件清理器")
    print("-" * 40)

    cleaner = FileCleaner()

    # 测试安全检查
    test_paths = [
        "C:\\Windows\\System32\\somefile.dll",
        "C:\\Users\\User\\AppData\\Local\\Temp\\test.tmp",
        "C:\\Windows\\Temp\\old_file.log",
    ]

    print("安全检查测试:")
    for path in test_paths:
        safe = cleaner.is_safe_to_delete(path)
        print(f"  {path}")
        print(f"    安全删除: {'是' if safe else '否'}")
        print()

def main():
    """主测试函数"""
    print("=" * 60)
    print("Windows C 盘清理工具 - 测试套件")
    print("=" * 60)
    print()

    try:
        test_system_info()
        test_disk_analyzer()
        test_scanner()
        test_cleaner_executor()
        test_file_cleaner()

        print("=" * 60)
        print("所有测试完成!")
        print("=" * 60)

    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
