import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class CleanItem:
    """清理项"""
    name: str
    path: str
    size: int
    file_count: int
    is_safe: bool
    requires_admin: bool
    description: str

@dataclass
class ScanResult:
    """扫描结果"""
    timestamp: str
    total_size: int
    total_files: int
    items: List[CleanItem]
    system_drive: str

@dataclass
class CleanResult:
    """清理结果"""
    timestamp: str
    cleaned_size: int
    cleaned_files: int
    failed_items: List[Dict]
    items_cleaned: List[str]

class SystemInfo:
    """系统信息获取"""

    @staticmethod
    def get_system_drive() -> str:
        """获取系统盘符"""
        return os.environ.get('SystemDrive', 'C:')

    @staticmethod
    def get_windows_dir() -> str:
        """获取 Windows 目录"""
        return os.environ.get('Windir', 'C:\\Windows')

    @staticmethod
    def get_temp_dir() -> str:
        """获取用户临时目录"""
        return os.environ.get('TEMP', os.environ.get('TMP', ''))

    @staticmethod
    def get_user_profile() -> str:
        """获取用户目录"""
        return os.environ.get('USERPROFILE', '')

    @staticmethod
    def is_admin() -> bool:
        """检查是否具有管理员权限"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

    @staticmethod
    def get_browser_cache_paths() -> Dict[str, str]:
        """获取浏览器缓存路径"""
        user_profile = SystemInfo.get_user_profile()
        local_app_data = os.environ.get('LOCALAPPDATA', '')

        return {
            'Chrome': os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            'Firefox': os.path.join(local_app_data, 'Mozilla', 'Firefox', 'Profiles'),
            'Edge': os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
        }

class DiskAnalyzer:
    """磁盘分析工具"""

    @staticmethod
    def get_dir_size(path: str) -> tuple[int, int]:
        """
        计算目录大小和文件数量
        返回: (大小字节数, 文件数量)
        """
        if not os.path.exists(path):
            return 0, 0

        total_size = 0
        file_count = 0

        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                        file_count += 1
                    except (OSError, FileNotFoundError):
                        continue
        except PermissionError:
            pass

        return total_size, file_count

    @staticmethod
    def format_size(size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

class FileCleaner:
    """文件清理工具"""

    PROTECTED_PATTERNS = [
        'ntuser.dat',
        'ntuser.ini',
        'desktop.ini',
        'thumbs.db',
        'bootmgr',
        'boot',
        'system32',
    ]

    @staticmethod
    def is_safe_to_delete(filepath: str) -> bool:
        """检查文件是否安全删除"""
        filepath_lower = filepath.lower()

        for pattern in FileCleaner.PROTECTED_PATTERNS:
            if pattern in filepath_lower:
                windows_dir = os.environ.get('Windir', 'C:\\Windows').lower()
                if windows_dir in filepath_lower:
                    return False

        return True

    @staticmethod
    def safe_delete_file(filepath: str) -> bool:
        """安全删除文件"""
        if not FileCleaner.is_safe_to_delete(filepath):
            return False

        try:
            os.remove(filepath)
            return True
        except (OSError, PermissionError):
            return False

    @staticmethod
    def safe_delete_directory(dirpath: str) -> tuple[int, int, List[str]]:
        """
        安全删除目录
        返回: (删除的文件数, 删除的大小, 失败列表)
        """
        if not os.path.exists(dirpath):
            return 0, 0, []

        deleted_count = 0
        deleted_size = 0
        failed = []

        try:
            for dirpath, dirnames, filenames in os.walk(dirpath):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        size = os.path.getsize(filepath)
                        if FileCleaner.safe_delete_file(filepath):
                            deleted_count += 1
                            deleted_size += size
                    except (OSError, FileNotFoundError):
                        continue

            for dirpath, dirnames, filenames in os.walk(dirpath, topdown=False):
                for dirname in dirnames:
                    try:
                        os.rmdir(os.path.join(dirpath, dirname))
                    except (OSError, FileNotFoundError):
                        continue

            try:
                os.rmdir(dirpath)
            except OSError:
                pass

        except Exception as e:
            failed.append({'path': dirpath, 'error': str(e)})

        return deleted_count, deleted_size, failed

class CleanerScanner:
    """清理扫描器"""

    def __init__(self):
        self.system_info = SystemInfo()
        self.disk_analyzer = DiskAnalyzer()

    def get_clean_items(self) -> List[CleanItem]:
        """获取所有可清理项"""
        items = []
        system_drive = self.system_info.get_system_drive()
        windows_dir = self.system_info.get_windows_dir()
        user_profile = self.system_info.get_user_profile()
        temp_dir = self.system_info.get_temp_dir()
        browser_paths = self.system_info.get_browser_cache_paths()

        # 1. 用户临时文件
        if temp_dir:
            size, count = self.disk_analyzer.get_dir_size(temp_dir)
            items.append(CleanItem(
                name="用户临时文件",
                path=temp_dir,
                size=size,
                file_count=count,
                is_safe=True,
                requires_admin=False,
                description="用户应用程序的临时文件"
            ))

        # 2. Windows 临时文件
        windows_temp = os.path.join(windows_dir, 'Temp')
        size, count = self.disk_analyzer.get_dir_size(windows_temp)
        items.append(CleanItem(
            name="Windows 临时文件",
            path=windows_temp,
            size=size,
            file_count=count,
            is_safe=True,
            requires_admin=True,
            description="Windows 系统的临时文件"
        ))

        # 3. Windows 更新缓存
        update_cache = os.path.join(system_drive, 'Windows', 'SoftwareDistribution', 'Download')
        size, count = self.disk_analyzer.get_dir_size(update_cache)
        items.append(CleanItem(
            name="Windows 更新缓存",
            path=update_cache,
            size=size,
            file_count=count,
            is_safe=True,
            requires_admin=True,
            description="Windows 更新下载的缓存文件"
        ))

        # 4. Prefetch 文件
        prefetch = os.path.join(windows_dir, 'Prefetch')
        size, count = self.disk_analyzer.get_dir_size(prefetch)
        items.append(CleanItem(
            name="预读取文件",
            path=prefetch,
            size=size,
            file_count=count,
            is_safe=True,
            requires_admin=True,
            description="系统预读取文件，可安全清理"
        ))

        # 5. 回收站
        recycle_bin = os.path.join(system_drive, '$Recycle.Bin')
        size, count = self.disk_analyzer.get_dir_size(recycle_bin)
        items.append(CleanItem(
            name="回收站",
            path=recycle_bin,
            size=size,
            file_count=count,
            is_safe=True,
            requires_admin=True,
            description="已删除的文件"
        ))

        # 6. Windows 日志文件
        windows_logs = os.path.join(windows_dir, 'Logs')
        size, count = self.disk_analyzer.get_dir_size(windows_logs)
        items.append(CleanItem(
            name="Windows 日志",
            path=windows_logs,
            size=size,
            file_count=count,
            is_safe=True,
            requires_admin=True,
            description="Windows 系统日志文件"
        ))

        # 7. Windows 错误报告
        wer_path = os.path.join(os.environ.get('ProgramData', ''), 'Microsoft', 'Windows', 'WER')
        size, count = self.disk_analyzer.get_dir_size(wer_path)
        items.append(CleanItem(
            name="错误报告",
            path=wer_path,
            size=size,
            file_count=count,
            is_safe=True,
            requires_admin=True,
            description="Windows 错误报告文件"
        ))

        # 8. 浏览器缓存
        for browser_name, cache_path in browser_paths.items():
            if os.path.exists(cache_path):
                size, count = self.disk_analyzer.get_dir_size(cache_path)
                if size > 0:
                    items.append(CleanItem(
                        name=f"{browser_name} 缓存",
                        path=cache_path,
                        size=size,
                        file_count=count,
                        is_safe=True,
                        requires_admin=False,
                        description=f"{browser_name} 浏览器的缓存文件"
                    ))

        # 9. 用户下载目录
        downloads = os.path.join(user_profile, 'Downloads')
        size, count = self.disk_analyzer.get_dir_size(downloads)
        items.append(CleanItem(
            name="下载文件夹",
            path=downloads,
            size=size,
            file_count=count,
            is_safe=False,
            requires_admin=False,
            description="下载文件夹（谨慎清理）"
        ))

        return items

    def scan(self) -> ScanResult:
        """执行扫描"""
        items = self.get_clean_items()
        total_size = sum(item.size for item in items)
        total_files = sum(item.file_count for item in items)

        return ScanResult(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_size=total_size,
            total_files=total_files,
            items=items,
            system_drive=self.system_info.get_system_drive()
        )

class CleanerExecutor:
    """清理执行器"""

    def __init__(self):
        self.system_info = SystemInfo()
        self.file_cleaner = FileCleaner()
        self.disk_analyzer = DiskAnalyzer()

    def clean_items(self, items: List[CleanItem], dry_run: bool = False) -> CleanResult:
        """执行清理"""
        cleaned_size = 0
        cleaned_files = 0
        items_cleaned = []
        failed_items = []

        for item in items:
            if dry_run:
                items_cleaned.append(item.name)
                continue

            if item.requires_admin and not self.system_info.is_admin():
                failed_items.append({
                    'path': item.path,
                    'error': '需要管理员权限',
                    'item': item.name
                })
                continue

            count, size, errors = self.file_cleaner.safe_delete_directory(item.path)

            if count > 0:
                cleaned_files += count
                cleaned_size += size
                items_cleaned.append(item.name)

            for error in errors:
                error['item'] = item.name
                failed_items.append(error)

        return CleanResult(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            cleaned_size=cleaned_size,
            cleaned_files=cleaned_files,
            failed_items=failed_items,
            items_cleaned=items_cleaned
        )

def format_scan_report(result: ScanResult) -> str:
    """格式化扫描报告"""
    analyzer = DiskAnalyzer()
    lines = [
        "=" * 60,
        "Windows C 盘清理 - 扫描报告",
        "=" * 60,
        f"扫描时间: {result.timestamp}",
        f"系统盘符: {result.system_drive}",
        f"总计占用: {analyzer.format_size(result.total_size)}",
        f"文件总数: {result.total_files}",
        "",
        "详细清理项:",
        "-" * 60,
    ]

    for i, item in enumerate(result.items, 1):
        lines.append(f"{i}. {item.name}")
        lines.append(f"   路径: {item.path}")
        lines.append(f"   大小: {analyzer.format_size(item.size)}")
        lines.append(f"   文件数: {item.file_count}")
        lines.append(f"   需要管理员: {'是' if item.requires_admin else '否'}")
        lines.append(f"   安全清理: {'是' if item.is_safe else '否（谨慎）'}")
        lines.append(f"   说明: {item.description}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)

def format_clean_report(result: CleanResult) -> str:
    """格式化清理报告"""
    analyzer = DiskAnalyzer()
    lines = [
        "=" * 60,
        "Windows C 盘清理 - 清理报告",
        "=" * 60,
        f"清理时间: {result.timestamp}",
        f"已清理大小: {analyzer.format_size(result.cleaned_size)}",
        f"已清理文件: {result.cleaned_files}",
        "",
        "已清理项目:",
        "-" * 60,
    ]

    for i, item_name in enumerate(result.items_cleaned, 1):
        lines.append(f"{i}. {item_name}")

    if result.failed_items:
        lines.append("")
        lines.append("清理失败项:")
        lines.append("-" * 60)
        for i, failed in enumerate(result.failed_items, 1):
            lines.append(f"{i}. {failed.get('item', '未知')}")
            lines.append(f"   路径: {failed.get('path', '未知')}")
            lines.append(f"   原因: {failed.get('error', '未知错误')}")

    lines.append("=" * 60)
    return "\n".join(lines)

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='Windows C 盘清理工具')
    parser.add_argument('--scan', action='store_true', help='扫描可清理项目')
    parser.add_argument('--clean', nargs='+', help='清理指定项目（用项目名称）')
    parser.add_argument('--clean-all', action='store_true', help='清理所有安全项目')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际删除')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')

    args = parser.parse_args()

    scanner = CleanerScanner()
    executor = CleanerExecutor()

    if args.scan:
        result = scanner.scan()

        if args.json:
            print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
        else:
            print(format_scan_report(result))

    elif args.clean or args.clean_all:
        all_items = scanner.scan().items

        if args.clean_all:
            items_to_clean = [item for item in all_items if item.is_safe]
        else:
            items_to_clean = [item for item in all_items if item.name in args.clean]

        result = executor.clean_items(items_to_clean, dry_run=args.dry_run)

        if args.json:
            print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
        else:
            print(format_clean_report(result))

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
