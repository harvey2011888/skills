#!/usr/bin/env python3
"""
Windows C 盘清理工具 - 测试脚本
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from windows_cleaner import (
    CleanerScanner,
    CleanerExecutor,
    SystemInfo,
    DiskAnalyzer,
    FileCleaner,
    ScanResult,
    CleanResult,
    CleanItem,
    format_scan_report,
    format_clean_report,
    format_selection_table,
    scan_only,
    clean_by_indices,
)

def test_system_info():
    print("=" * 60)
    print(" 测试: 系统信息获取")
    print("=" * 60)
    print()

    info = SystemInfo()
    major, minor, build, friendly = info.get_windows_version()
    print(f"  系统盘符:     {info.get_system_drive()}")
    print(f"  Windows 目录: {info.get_windows_dir()}")
    print(f"  用户目录:     {info.get_user_profile()}")
    print(f"  临时目录:     {info.get_temp_dir()}")
    print(f"  ProgramData:  {info.get_program_data()}")
    print(f"  LocalAppData: {info.get_local_appdata()}")
    print(f"  Roaming:      {info.get_appdata()}")
    print(f"  Windows 版本: {friendly} ({major}.{minor}.{build})")
    print(f"  管理员权限:   {'是' if info.is_admin() else '否'}")
    print()

def test_disk_analyzer():
    print("=" * 60)
    print(" 测试: 磁盘分析")
    print("=" * 60)
    print()

    analyzer = DiskAnalyzer()

    test_sizes = [0, 512, 1024, 1024*1024, 1024*1024*1024, 1024*1024*1024*2.5]
    print("  大小格式化:")
    for size in test_sizes:
        print(f"    {size:>15,} 字节 = {analyzer.format_size(size)}")
    print()

def test_scanner():
    print("=" * 60)
    print(" 测试: 扫描功能")
    print("=" * 60)
    print()

    scanner = CleanerScanner()
    result = scanner.scan()

    print(f"  扫描时间: {result.timestamp}")
    print(f"  系统版本: {result.windows_version}")
    print(f"  系统盘符: {result.system_drive}")
    print(f"  总计占用: {DiskAnalyzer.format_size(result.total_size)}")
    print(f"  文件总数: {result.total_files:,}")
    print(f"  清理项数: {len(result.items)}")
    print()

    print("  清理项列表 (前10个):")
    print("-" * 85)
    for i, item in enumerate(result.items[:10], 1):
        safe = "安全" if item.is_safe else "需确认"
        admin = "需管理员" if item.requires_admin else "无需管理员"
        versions = ", ".join(item.win_versions)
        print(f"  {i:>2}. {item.name:<20} | {DiskAnalyzer.format_size(item.size):>10} | {item.file_count:>5} 文件 | {safe:<6} | {admin:<8} | {versions}")
    if len(result.items) > 10:
        print(f"  ... 还有 {len(result.items) - 10} 项")
    print()

def test_format_selection_table():
    print("=" * 60)
    print(" 测试: 选择表格格式化")
    print("=" * 60)
    print()

    scanner = CleanerScanner()
    result = scanner.scan()
    print(format_selection_table(result.items))
    print()

def test_format_scan_report():
    print("=" * 60)
    print(" 测试: 扫描报告格式化")
    print("=" * 60)
    print()

    scanner = CleanerScanner()
    result = scanner.scan()
    print(format_scan_report(result))
    print()

def test_cleaner_simulated():
    print("=" * 60)
    print(" 测试: 清理执行 (模拟)")
    print("=" * 60)
    print()

    scanner = CleanerScanner()
    executor = CleanerExecutor()

    result = scanner.scan()
    safe_items = [item for item in result.items if item.is_safe]
    print(f"  找到 {len(safe_items)} 个安全清理项")
    print()

    clean_result = executor.clean_items(safe_items, dry_run=True)
    print(f"  清理时间:      {clean_result.timestamp}")
    print(f"  清理前总大小:  {DiskAnalyzer.format_size(clean_result.before_size)}")
    print(f"  清理前文件数:  {clean_result.before_files:,}")
    print(f"  清理项目数:    {len(clean_result.items_cleaned)}")
    print(f"  清理大小:      {DiskAnalyzer.format_size(clean_result.cleaned_size)}")
    print(f"  清理文件数:    {clean_result.cleaned_files:,}")
    print(f"  失败项数:      {len(clean_result.failed_items)}")
    print()

def test_file_cleaner():
    print("=" * 60)
    print(" 测试: 文件清理器安全检测")
    print("=" * 60)
    print()

    cleaner = FileCleaner()
    windows_dir = SystemInfo.get_windows_dir()

    test_paths = [
        os.path.join(windows_dir, 'System32', 'kernel32.dll'),
        os.path.join(windows_dir, 'Temp', 'test123.tmp'),
        os.path.join(windows_dir, 'bootmgr'),
        os.path.join(SystemInfo.get_temp_dir(), 'myapp.tmp'),
        os.path.join(windows_dir, 'System32', 'desktop.ini'),
    ]

    print("  路径安全检查:")
    for path in test_paths:
        safe = cleaner.is_safe_to_delete(path)
        status = "✅ 安全" if safe else "❌ 受保护"
        print(f"    {status}  |  {path}")
    print()

def test_programmatic_api():
    print("=" * 60)
    print(" 测试: 编程接口")
    print("=" * 60)
    print()

    print("  scan_only() ...")
    result = scan_only()
    print(f"    返回 {len(result.items)} 个清理项")
    print(f"    总大小: {DiskAnalyzer.format_size(result.total_size)}")
    print()

    if len(result.items) >= 3:
        print("  clean_by_indices([1, 2, 3], dry_run=True) ...")
        clean_result = clean_by_indices([1, 2, 3], dry_run=True)
        if clean_result:
            print(f"    选中: {clean_result.items_cleaned}")
            print(f"    成功: {len(clean_result.items_cleaned)} 项")
        else:
            print("    未找到项目")
    print()

def test_cross_browser_paths():
    print("=" * 60)
    print(" 测试: 浏览器缓存路径检测")
    print("=" * 60)
    print()

    paths = SystemInfo.get_all_browser_cache_paths()
    if paths:
        print(f"  检测到 {len(paths)} 个浏览器缓存路径:")
        for name, path in paths.items():
            exists = os.path.exists(path)
            status = "✅ 存在" if exists else "❌ 不存在"
            print(f"    {status}  |  {name}: {path}")
    else:
        print("  未检测到任何浏览器缓存路径")
    print()

def main():
    print()
    print("=" * 60)
    print("  Windows C 盘清理工具 - 完整测试套件 v2.0")
    print("=" * 60)

    tests = [
        test_system_info,
        test_disk_analyzer,
        test_file_cleaner,
        test_scanner,
        test_format_selection_table,
        test_cross_browser_paths,
        test_cleaner_simulated,
        test_programmatic_api,
    ]

    for test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"  ❌ {test_func.__name__} 失败: {e}")
            import traceback
            traceback.print_exc()
            return 1

    try:
        print("=" * 60)
        print(" 测试: 扫描报告格式化")
        print("=" * 60)
        test_format_scan_report()
    except Exception:
        pass

    print("=" * 60)
    print("  所有测试完成！")
    print("=" * 60)
    return 0

if __name__ == '__main__':
    sys.exit(main())