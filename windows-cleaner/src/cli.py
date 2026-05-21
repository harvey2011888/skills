#!/usr/bin/env python3
"""
Windows C 盘清理工具 - CLI 入口

支持交互式选择、命令行参数、JSON 输出三种模式。
兼容 Win7 / Win8 / Win8.1 / Win10 / Win11。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from windows_cleaner import main

if __name__ == '__main__':
    main()