# Windows C 盘清理工具 v2.0

智能扫描和清理 Windows 系统 C 盘的临时文件、缓存、日志等，释放磁盘空间。

支持 Win7 / Win8 / Win8.1 / Win10 / Win11。

## 快速开始

### 扫描 C 盘

```bash
python src/cli.py --scan
```

### 交互式选择清理

```bash
python src/cli.py --interactive
```

### 清理所有安全项目

```bash
python src/cli.py --clean-all
```

### 清理指定项目

```bash
python src/cli.py --clean "临时文件" "Chrome 缓存" "Edge 缓存"
```

### 模拟运行（不删除）

```bash
python src/cli.py --clean-all --dry-run
```

## 项目结构

```
windows-cleaner/
├── src/
│   ├── __init__.py           # 包初始化
│   ├── windows_cleaner.py    # 核心清理逻辑
│   └── cli.py                # 命令行入口
├── test_cleaner.py           # 测试脚本
├── SKILL.md                  # 技能说明文档
└── README.md                 # 本文件
```

## 功能特性

- **交互式选择**: 先扫描再列出，用户选择后执行清理
- **全版本兼容**: Win7 / Win8 / Win8.1 / Win10 / Win11
- **智能扫描**: 20+ 种清理项目，覆盖临时文件、缓存、日志、转储等
- **安全清理**: 多层白名单保护，跳过系统关键文件
- **详细报告**: 清理前后对比、成功/失败明细
- **零依赖**: 仅使用 Python 标准库

## 支持的清理项

| 类型 | 项目 |
|------|------|
| 系统临时 | 临时文件、系统临时文件、预读取文件、安装日志、系统日志 |
| 更新相关 | Windows 更新缓存、传递优化文件(Win10/11) |
| 缓存 | 缩略图缓存、DirectX 着色器缓存、NVIDIA DX/GL 缓存、IE 缓存 |
| 浏览器缓存 | Chrome/Edge/Firefox/Opera/Brave/Vivaldi/Chromium/360/QQ/搜狗/微信 |
| 转储文件 | 系统内存转储、小型转储、错误转储 |
| 其他 | 回收站、错误报告、旧版 Windows、最近文档、下载文件夹 |

详细说明请查看 [SKILL.md](SKILL.md)