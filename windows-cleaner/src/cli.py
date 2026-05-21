#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows C 盘清理工具 - CLI 入口
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from windows_cleaner import main

if __name__ == '__main__':
    main()
