# Windows C 盘清理工具

智能扫描和清理 Windows 系统 C 盘的临时文件、缓存、日志等，释放磁盘空间。

## 快速开始

### 扫描 C 盘

```bash
python src/cli.py --scan
```

### 清理所有安全项目

```bash
python src/cli.py --clean-all
```

### 清理指定项目

```bash
python src/cli.py --clean "用户临时文件" "Chrome 缓存"
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
└── SKILL.md                  # 技能说明文档
```

## 功能特性

- 智能扫描多种占用空间项目
- 安全清理，内置白名单保护
- 支持选择性清理
- 详细的扫描和清理报告
- 零依赖，仅使用 Python 标准库

## 支持的清理项

1. 用户临时文件
2. Windows 临时文件
3. Windows 更新缓存
4. 预读取文件
5. 回收站
6. Windows 日志
7. 错误报告
8. 浏览器缓存（Chrome、Firefox、Edge）
9. 下载文件夹

详细说明请查看 [SKILL.md](SKILL.md)
