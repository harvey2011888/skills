"""
Windows C 盘清理工具

用于扫描和清理 Windows 系统 C 盘的常见占用空间的文件和文件夹。
"""

from .windows_cleaner import (
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
)

__version__ = '1.0.0'
__author__ = 'SOLO'

__all__ = [
    'CleanerScanner',
    'CleanerExecutor',
    'SystemInfo',
    'DiskAnalyzer',
    'FileCleaner',
    'ScanResult',
    'CleanResult',
    'CleanItem',
    'format_scan_report',
    'format_clean_report',
]
