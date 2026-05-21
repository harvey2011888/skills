"""
Windows C 盘清理工具

用于扫描和清理 Windows 系统 C 盘的常见占用空间的文件和文件夹。
支持 Win7 / Win8 / Win8.1 / Win10 / Win11。
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
    format_selection_table,
    interactive_select,
    scan_only,
    clean_by_indices,
)

__version__ = '2.0.0'
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
    'format_selection_table',
    'interactive_select',
    'scan_only',
    'clean_by_indices',
]