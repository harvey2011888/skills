import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class CleanItem:
    name: str
    path: str
    size: int
    file_count: int
    is_safe: bool
    requires_admin: bool
    description: str
    win_versions: List[str]

@dataclass
class ScanResult:
    timestamp: str
    total_size: int
    total_files: int
    items: List[CleanItem]
    system_drive: str
    windows_version: str

@dataclass
class CleanResult:
    timestamp: str
    cleaned_size: int
    cleaned_files: int
    failed_items: List[Dict]
    items_cleaned: List[str]
    before_size: int
    before_files: int

class SystemInfo:

    _win_version_cache = None

    @staticmethod
    def get_system_drive() -> str:
        return os.environ.get('SystemDrive', 'C:')

    @staticmethod
    def get_windows_dir() -> str:
        return os.environ.get('Windir', 'C:\\Windows')

    @staticmethod
    def get_temp_dir() -> str:
        return os.environ.get('TEMP', os.environ.get('TMP', ''))

    @staticmethod
    def get_user_profile() -> str:
        return os.environ.get('USERPROFILE', '')

    @staticmethod
    def get_program_data() -> str:
        return os.environ.get('ProgramData', '')

    @staticmethod
    def get_local_appdata() -> str:
        return os.environ.get('LOCALAPPDATA', '')

    @staticmethod
    def get_appdata() -> str:
        return os.environ.get('APPDATA', '')

    @staticmethod
    def is_admin() -> bool:
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    @staticmethod
    def get_windows_version() -> Tuple[int, int, int, str]:
        if SystemInfo._win_version_cache is not None:
            return SystemInfo._win_version_cache
        try:
            result = subprocess.run(
                ['cmd', '/c', 'ver'],
                capture_output=True, text=True, shell=True
            )
            output = result.stdout.strip()
            import re
            match = re.search(r'(\d+)\.(\d+)\.(\d+)', output)
            if match:
                major, minor, build = int(match.group(1)), int(match.group(2)), int(match.group(3))
            else:
                match_legacy = re.search(r'Version\s+(\d+)\.(\d+)', output)
                if match_legacy:
                    major, minor, build = int(match_legacy.group(1)), int(match_legacy.group(2)), 0
                else:
                    major, minor, build = 10, 0, 0
        except Exception:
            major, minor, build = 10, 0, 0

        if major >= 10 and build >= 22000:
            friendly = 'Windows 11'
        elif major >= 10:
            friendly = 'Windows 10'
        elif major == 6 and minor >= 3:
            friendly = 'Windows 8.1'
        elif major == 6 and minor >= 2:
            friendly = 'Windows 8'
        elif major == 6 and minor >= 1:
            friendly = 'Windows 7'
        elif major == 6 and minor == 0:
            friendly = 'Windows Vista'
        elif major == 5 and minor >= 1:
            friendly = 'Windows XP'
        else:
            friendly = f'Windows {major}.{minor}.{build}'

        SystemInfo._win_version_cache = (major, minor, build, friendly)
        return SystemInfo._win_version_cache

    @staticmethod
    def get_all_browser_cache_paths() -> Dict[str, str]:
        local = SystemInfo.get_local_appdata()
        roaming = SystemInfo.get_appdata()
        paths = {}

        browsers = [
            ('Chrome', local, 'Google', 'Chrome', 'User Data', 'Default', 'Cache', 'Cache_Data'),
            ('Chrome Code Cache', local, 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache'),
            ('Chrome GPU Cache', local, 'Google', 'Chrome', 'User Data', 'Default', 'GPUCache'),
            ('Edge', local, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache', 'Cache_Data'),
            ('Edge Code Cache', local, 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
            ('Edge GPU Cache', local, 'Microsoft', 'Edge', 'User Data', 'Default', 'GPUCache'),
            ('Firefox', local, 'Mozilla', 'Firefox', 'Profiles'),
            ('Opera', roaming, 'Opera Software', 'Opera Stable', 'Cache', 'Cache_Data'),
            ('Brave', local, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Cache', 'Cache_Data'),
            ('Vivaldi', local, 'Vivaldi', 'User Data', 'Default', 'Cache', 'Cache_Data'),
            ('Chromium', local, 'Chromium', 'User Data', 'Default', 'Cache', 'Cache_Data'),
            ('360安全浏览器', roaming, '360se6', 'User Data', 'Default', 'Cache'),
            ('360极速浏览器', local, '360Chrome', 'Chrome', 'User Data', 'Default', 'Cache'),
            ('QQ浏览器', local, 'Tencent', 'QQBrowser', 'User Data', 'Default', 'Cache'),
            ('搜狗浏览器', local, 'SogouExplorer', 'User Data', 'Default', 'Cache'),
            ('微信内置浏览器', roaming, 'Tencent', 'WeChat', 'radium', 'user data', 'default', 'Cache'),
        ]

        for name, *parts in browsers:
            path = os.path.join(*parts)
            if os.path.exists(path):
                paths[name] = path

        return paths

class DiskAnalyzer:

    @staticmethod
    def get_dir_size(path: str) -> Tuple[int, int]:
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
                    except (OSError, FileNotFoundError, PermissionError):
                        continue
        except PermissionError:
            pass

        return total_size, file_count

    @staticmethod
    def format_size(size_bytes: int) -> str:
        if size_bytes == 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    @staticmethod
    def get_disk_usage(path: str) -> Tuple[int, int, int]:
        total, used, free = 0, 0, 0
        try:
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            total_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(path), None,
                ctypes.pointer(total_bytes), ctypes.pointer(free_bytes)
            )
            total = total_bytes.value
            free = free_bytes.value
            used = total - free
        except Exception:
            pass
        return total, used, free

class FileCleaner:

    PROTECTED_PATTERNS = [
        'ntuser.dat', 'ntuser.ini', 'desktop.ini', 'thumbs.db',
        'bootmgr', 'boot', 'system32', 'syswow64',
        'pagefile.sys', 'swapfile.sys', 'hiberfil.sys',
    ]

    @staticmethod
    def is_safe_to_delete(filepath: str) -> bool:
        filepath_lower = filepath.lower()
        windows_dir = os.environ.get('Windir', 'C:\\Windows').lower()

        for pattern in FileCleaner.PROTECTED_PATTERNS:
            if pattern in filepath_lower:
                if windows_dir in filepath_lower:
                    return False

        return True

    @staticmethod
    def safe_delete_file(filepath: str) -> bool:
        if not FileCleaner.is_safe_to_delete(filepath):
            return False
        try:
            os.remove(filepath)
            return True
        except (OSError, PermissionError):
            return False

    @staticmethod
    def safe_delete_directory(dirpath: str) -> Tuple[int, int, List[str]]:
        if not os.path.exists(dirpath):
            return 0, 0, []

        deleted_count = 0
        deleted_size = 0
        failed = []

        try:
            for current_root, dirnames, filenames in os.walk(dirpath, topdown=True):
                dirnames[:] = [d for d in dirnames if not FileCleaner._is_protected_dir(d)]
                for filename in filenames:
                    filepath = os.path.join(current_root, filename)
                    try:
                        size = os.path.getsize(filepath)
                        if FileCleaner.safe_delete_file(filepath):
                            deleted_count += 1
                            deleted_size += size
                    except (OSError, FileNotFoundError, PermissionError):
                        continue

            for current_root, dirnames, filenames in os.walk(dirpath, topdown=False):
                for dirname in dirnames:
                    try:
                        os.rmdir(os.path.join(current_root, dirname))
                    except (OSError, FileNotFoundError, PermissionError):
                        continue
            try:
                os.rmdir(dirpath)
            except OSError:
                pass

        except Exception as e:
            failed.append({'path': dirpath, 'error': str(e)})

        return deleted_count, deleted_size, failed

    @staticmethod
    def _is_protected_dir(dirname: str) -> bool:
        protected = ['system32', 'syswow64', 'boot', 'winre', 'winsxs']
        return dirname.lower() in protected

class CleanerScanner:

    ALL_WIN = ['Win7', 'Win8', 'Win8.1', 'Win10', 'Win11']

    def __init__(self):
        self.system_info = SystemInfo()

    def get_clean_items(self) -> List[CleanItem]:
        items = []
        analyzer = DiskAnalyzer()
        system_drive = self.system_info.get_system_drive()
        windows_dir = self.system_info.get_windows_dir()
        user_profile = self.system_info.get_user_profile()
        temp_dir = self.system_info.get_temp_dir()
        program_data = self.system_info.get_program_data()
        local_appdata = self.system_info.get_local_appdata()
        _, _, _, ver_friendly = self.system_info.get_windows_version()

        is_win10_plus = ver_friendly in ('Windows 10', 'Windows 11')

        def add(name, path, safe, admin, desc, versions=None):
            if versions is None:
                versions = self.ALL_WIN
            size, count = analyzer.get_dir_size(path)
            items.append(CleanItem(
                name=name, path=path, size=size, file_count=count,
                is_safe=safe, requires_admin=admin, description=desc,
                win_versions=versions
            ))

        if temp_dir:
            add("临时文件", temp_dir, True, False,
                "应用程序和安装程序的临时文件")

        add("系统临时文件", os.path.join(windows_dir, 'Temp'), True, True,
            "Windows 系统的临时文件")

        add("Windows 更新缓存",
            os.path.join(windows_dir, 'SoftwareDistribution', 'Download'),
            True, True, "Windows Update 下载的安装包缓存，更新后可安全清理")

        if is_win10_plus:
            add("传递优化文件",
                os.path.join(windows_dir, 'SoftwareDistribution', 'DeliveryOptimization'),
                True, True, "Windows 10/11 传递优化(P2P)缓存",
                versions=['Win10', 'Win11'])

        add("预读取文件", os.path.join(windows_dir, 'Prefetch'), True, True,
            "应用程序启动预读取缓存，可安全清理")

        add("回收站",
            os.path.join(system_drive, '$Recycle.Bin'), True, True,
            "系统回收站中的已删除文件")

        if is_win10_plus:
            add("缩略图缓存",
                os.path.join(local_appdata, 'Microsoft', 'Windows', 'Explorer'),
                True, False, "文件夹缩略图和图标缓存，可安全清理",
                versions=['Win10', 'Win11'])

        add("系统日志", os.path.join(windows_dir, 'Logs'), True, True,
            "Windows 系统和应用程序的日志文件")

        add("安装日志", os.path.join(windows_dir, 'Panther'), True, True,
            "Windows 安装/升级过程中产生的日志")

        add("错误报告",
            os.path.join(program_data, 'Microsoft', 'Windows', 'WER'), True, True,
            "Windows 错误报告存档")

        if is_win10_plus:
            add("DirectX 着色器缓存",
                os.path.join(local_appdata, 'D3DSCache'), True, False,
                "DirectX 着色器编译缓存，可安全清理",
                versions=['Win10', 'Win11'])

        windows_old = os.path.join(system_drive, 'Windows.old')
        if os.path.exists(windows_old):
            add("旧版 Windows", windows_old, True, True,
                "升级 Windows 后保留的旧版本文件，确认不需要回滚后可清理")

        dump_files = [
            ('系统内存转储', os.path.join(windows_dir, 'MEMORY.DMP')),
            ('小型内存转储', os.path.join(windows_dir, 'Minidump')),
            ('系统错误转储', os.path.join(windows_dir, 'LiveKernelReports')),
        ]
        for dump_name, dump_path in dump_files:
            size, count = analyzer.get_dir_size(dump_path)
            if size > 0:
                items.append(CleanItem(
                    name=dump_name, path=dump_path, size=size, file_count=count,
                    is_safe=True, requires_admin=True,
                    description="系统崩溃时产生的调试文件，可安全清理",
                    win_versions=self.ALL_WIN
                ))

        browser_paths = self.system_info.get_all_browser_cache_paths()
        for browser_name, cache_path in browser_paths.items():
            size, count = analyzer.get_dir_size(cache_path)
            if size > 0:
                items.append(CleanItem(
                    name=f"{browser_name} 缓存",
                    path=cache_path, size=size, file_count=count,
                    is_safe=True, requires_admin=False,
                    description=f"{browser_name} 浏览器的网页缓存",
                    win_versions=self.ALL_WIN
                ))

        add("下载文件夹", os.path.join(user_profile, 'Downloads'), False, False,
            "用户下载目录，包含可能重要的文件，清理前请确认")

        add("最近文档",
            os.path.join(user_profile, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Recent'),
            True, False, "最近打开的文件快捷方式列表，可安全清理")

        nvidia_cache = os.path.join(local_appdata, 'NVIDIA', 'DXCache')
        if os.path.exists(nvidia_cache):
            items.append(CleanItem(
                name="NVIDIA DX缓存", path=nvidia_cache, size=0, file_count=0,
                is_safe=True, requires_admin=False,
                description="NVIDIA 显卡 DirectX 缓存",
                win_versions=self.ALL_WIN
            ))
            items[-1].size, items[-1].file_count = analyzer.get_dir_size(nvidia_cache)

        nvidia_cache2 = os.path.join(local_appdata, 'NVIDIA', 'GLCache')
        if os.path.exists(nvidia_cache2):
            items.append(CleanItem(
                name="NVIDIA GL缓存", path=nvidia_cache2, size=0, file_count=0,
                is_safe=True, requires_admin=False,
                description="NVIDIA 显卡 OpenGL 缓存",
                win_versions=self.ALL_WIN
            ))
            items[-1].size, items[-1].file_count = analyzer.get_dir_size(nvidia_cache2)

        ie_cache = os.path.join(local_appdata, 'Microsoft', 'Windows', 'INetCache')
        if os.path.exists(ie_cache):
            items.append(CleanItem(
                name="Internet Explorer 缓存", path=ie_cache, size=0, file_count=0,
                is_safe=True, requires_admin=False,
                description="IE 浏览器的临时互联网文件",
                win_versions=self.ALL_WIN
            ))
            items[-1].size, items[-1].file_count = analyzer.get_dir_size(ie_cache)

        return items

    def scan(self) -> ScanResult:
        items = self.get_clean_items()
        total_size = sum(item.size for item in items)
        total_files = sum(item.file_count for item in items)

        return ScanResult(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_size=total_size,
            total_files=total_files,
            items=items,
            system_drive=self.system_info.get_system_drive(),
            windows_version=self.system_info.get_windows_version()[3]
        )

class CleanerExecutor:

    def __init__(self):
        self.system_info = SystemInfo()
        self.file_cleaner = FileCleaner()
        self.disk_analyzer = DiskAnalyzer()

    def clean_items(self, items: List[CleanItem], dry_run: bool = False) -> CleanResult:
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
                    'error': '需要管理员权限，请以管理员身份运行',
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
            items_cleaned=items_cleaned,
            before_size=sum(item.size for item in items),
            before_files=sum(item.file_count for item in items),
        )

def format_safe_badge(is_safe: bool) -> str:
    return "✅ 安全" if is_safe else "⚠️  需确认"

def format_admin_badge(requires_admin: bool) -> str:
    return "🔒 需管理员" if requires_admin else "🔓 无需管理员"

def format_selection_table(items: List[CleanItem]) -> str:
    analyzer = DiskAnalyzer()
    lines = [
        f"{'编号':<5} {'清理项目':<22} {'占用空间':<12} {'文件数':<10} {'安全性':<12} {'权限':<14}",
        "-" * 85,
    ]
    for i, item in enumerate(items, 1):
        lines.append(
            f"{i:<5} {item.name:<22} {analyzer.format_size(item.size):<12} "
            f"{item.file_count:<10} {format_safe_badge(item.is_safe):<12} "
            f"{format_admin_badge(item.requires_admin):<14}"
        )
    return "\n".join(lines)

def format_scan_report(result: ScanResult) -> str:
    analyzer = DiskAnalyzer()
    lines = [
        "=" * 65,
        "  Windows C 盘清理 - 扫描报告",
        "=" * 65,
        f"  扫描时间:   {result.timestamp}",
        f"  系统版本:   {result.windows_version}",
        f"  系统盘符:   {result.system_drive}",
        f"  总计占用:   {analyzer.format_size(result.total_size)}",
        f"  文件总数:   {result.total_files:,}",
        f"  可清理项:   {len([i for i in result.items if i.size > 0])} 项",
        "",
    ]

    if result.total_size > 0:
        total_disk, used_disk, free_disk = analyzer.get_disk_usage(
            result.system_drive + "\\"
        )
        if total_disk > 0:
            lines.append(f"  磁盘总量:   {analyzer.format_size(total_disk)}")
            lines.append(f"  已使用:     {analyzer.format_size(used_disk)}")
            lines.append(f"  可用空间:   {analyzer.format_size(free_disk)}")
            lines.append("")

    lines.append("-" * 65)
    lines.append(format_selection_table(result.items))
    lines.append("=" * 65)
    return "\n".join(lines)

def format_clean_report(result: CleanResult) -> str:
    analyzer = DiskAnalyzer()
    lines = [
        "=" * 65,
        "  Windows C 盘清理 - 清理报告",
        "=" * 65,
        f"  清理时间:      {result.timestamp}",
        f"  清理前占用:    {analyzer.format_size(result.before_size)} ({result.before_files:,} 个文件)",
        f"  已清理大小:    {analyzer.format_size(result.cleaned_size)}",
        f"  已清理文件:    {result.cleaned_files:,}",
        f"  成功清理:      {len(result.items_cleaned)} 项",
    ]

    if result.failed_items:
        lines.append(f"  清理失败:      {len(result.failed_items)} 项")
    lines.append("")

    if result.items_cleaned:
        lines.append("  已清理项目:")
        lines.append("  " + "-" * 55)
        for i, name in enumerate(result.items_cleaned, 1):
            lines.append(f"    {i}. {name}")

    if result.failed_items:
        lines.append("")
        lines.append("  清理失败项:")
        lines.append("  " + "-" * 55)
        for i, failed in enumerate(result.failed_items, 1):
            lines.append(f"    {i}. {failed.get('item', '未知')}")
            lines.append(f"       路径: {failed.get('path', '未知')}")
            lines.append(f"       原因: {failed.get('error', '未知错误')}")

    lines.append("")
    lines.append("=" * 65)
    return "\n".join(lines)

def interactive_select(items: List[CleanItem]) -> List[CleanItem]:
    analyzer = DiskAnalyzer()
    print("\n" + "=" * 65)
    print("  Windows C 盘清理 - 交互式选择")
    print("=" * 65)
    print(f"\n  共发现 {len(items)} 个可清理项目:\n")
    print(format_selection_table(items))
    print()

    item_map = {}
    for i, item in enumerate(items, 1):
        item_map[str(i)] = item
        item_map[item.name] = item

    print("  操作说明:")
    print("    - 输入编号 (如: 1,3,5)  选择指定项目")
    print("    - 输入项目名称           选择指定项目")
    print("    - 输入 all               选择所有安全项目")
    print("    - 输入 safe              选择所有安全项目")
    print("    - 输入 q                 退出")
    print()

    while True:
        try:
            choice = input("  请输入要清理的项目编号或名称: ").strip()
        except (EOFError, KeyboardInterrupt):
            return []

        if choice.lower() in ('q', 'quit', 'exit'):
            return []

        if choice.lower() in ('all', 'safe'):
            return [item for item in items if item.is_safe]

        if choice.lower() == 'all-force':
            return list(items)

        parts = [p.strip() for p in choice.replace(',', ' ').split()]
        selected = []
        not_found = []

        for part in parts:
            if not part:
                continue
            if part in item_map:
                selected.append(item_map[part])
            else:
                not_found.append(part)

        if not_found:
            print(f"\n  ⚠️  未识别的项目: {', '.join(not_found)}")
            print(f"  请输入正确的编号或名称，或输入 q 退出\n")
            continue

        if not selected:
            print("\n  ⚠️  未选择任何项目，请重新输入\n")
            continue

        print("\n  已选择以下项目:")
        for i, item in enumerate(selected, 1):
            print(f"    {i}. {item.name} ({analyzer.format_size(item.size)})")

        try:
            confirm = input("\n  确认清理以上项目？(y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return []

        if confirm in ('y', 'yes', '是'):
            return selected
        else:
            print("\n  已取消，请重新选择\n")
            continue

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Windows C 盘清理工具 - 支持 Win7/8/8.1/10/11',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cli.py --scan                   扫描可清理项目
  python cli.py --scan --json            扫描并输出 JSON
  python cli.py --clean "临时文件"       清理指定项目
  python cli.py --clean-all              清理所有安全项目
  python cli.py --interactive            交互式选择模式
  python cli.py --list                   列出所有清理项（简洁格式）
  python cli.py --all --dry-run          模拟运行，不实际删除
        """
    )
    parser.add_argument('--scan', '-s', action='store_true', help='扫描可清理项目')
    parser.add_argument('--clean', '-c', nargs='+', help='清理指定项目（用项目名称，空格分隔）')
    parser.add_argument('--clean-all', '--all', '-a', action='store_true', help='清理所有安全项目')
    parser.add_argument('--clean-all-force', action='store_true', help='清理所有项目（包括需确认的）')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式选择清理模式')
    parser.add_argument('--dry-run', '--dry', '-d', action='store_true', help='模拟运行，不实际删除文件')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--list', '-l', action='store_true', help='仅列出清理项（简洁格式）')

    args = parser.parse_args()

    if args.list:
        scanner = CleanerScanner()
        result = scanner.scan()
        print(format_selection_table(result.items))
        return

    if args.scan:
        scanner = CleanerScanner()
        result = scanner.scan()
        if args.json:
            print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
        else:
            print(format_scan_report(result))
        return

    if args.interactive:
        scanner = CleanerScanner()
        result = scanner.scan()

        print(format_scan_report(result))
        selected = interactive_select(result.items)

        if not selected:
            print("\n  未选择任何项目，取消清理。")
            return

        executor = CleanerExecutor()
        clean_result = executor.clean_items(selected, dry_run=args.dry_run)

        if args.json:
            print(json.dumps(asdict(clean_result), indent=2, ensure_ascii=False))
        else:
            print(format_clean_report(clean_result))
        return

    if args.clean or args.clean_all or args.clean_all_force:
        scanner = CleanerScanner()
        all_items = scanner.scan().items

        if args.clean_all_force:
            items_to_clean = all_items
        elif args.clean_all:
            items_to_clean = [item for item in all_items if item.is_safe]
        else:
            items_to_clean = [item for item in all_items if item.name in args.clean]
            not_found = [c for c in args.clean if not any(item.name == c for item in all_items)]
            if not_found:
                print(f"警告: 未找到以下清理项: {', '.join(not_found)}")
                print(f"可用的清理项: {', '.join(item.name for item in all_items)}")

        if not items_to_clean:
            print("未选择任何可清理项目。")
            return

        executor = CleanerExecutor()
        clean_result = executor.clean_items(items_to_clean, dry_run=args.dry_run)

        if args.json:
            print(json.dumps(asdict(clean_result), indent=2, ensure_ascii=False))
        else:
            print(format_clean_report(clean_result))
        return

    parser.print_help()

def scan_only():
    scanner = CleanerScanner()
    result = scanner.scan()
    return result

def clean_by_indices(indices: List[int], dry_run: bool = False):
    scanner = CleanerScanner()
    result = scanner.scan()
    items = result.items
    selected = []
    for idx in indices:
        if 1 <= idx <= len(items):
            selected.append(items[idx - 1])
    if not selected:
        return None
    executor = CleanerExecutor()
    return executor.clean_items(selected, dry_run=dry_run)

if __name__ == '__main__':
    main()