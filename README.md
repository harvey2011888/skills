# 🎯 SOLO Skills 仓库

> 存放所有 SOLO 技能创作赛开发的 Skills

## 📦 包含的 Skills

### Windows C 盘清理 🆕

**目录**: [windows-cleaner/](windows-cleaner/)

智能扫描和清理 Windows 系统 C 盘的临时文件、缓存、日志等，先列出可清理项目供用户选择，确认后执行并生成清理报告。支持 Win7 / Win8 / Win8.1 / Win10 / Win11。

#### 核心特性
- 🔍 智能扫描 - 覆盖 20+ 种清理项（临时文件、更新缓存、浏览器缓存、系统转储等）
- 🛡️ 安全清理 - 内置白名单保护，自动跳过 System32 等关键系统目录
- 📋 交互式选择 - 扫描后列出清单，用户选择要清理的项目后才执行
- 📊 详细报告 - 清理前后对比、成功/失败明细，一目了然
- 🌐 全版本兼容 - 支持 Win7 / Win8 / Win8.1 / Win10 / Win11
- 📦 零依赖 - 仅使用 Python 标准库，开箱即用

#### 快速开始

```bash
# 进入目录
cd windows-cleaner

# 扫描可清理项目
python src/cli.py --scan

# 交互式选择清理
python src/cli.py --interactive

# 清理所有安全项目
python src/cli.py --clean-all
```

#### 项目统计
- **代码行数**: 760 行（核心代码 + CLI）
- **清理项数**: 20+ 种常见占用空间项目
- **浏览器覆盖**: 16 款浏览器（Chrome/Edge/Firefox/360/QQ/搜狗/微信等）
- **依赖**: 零依赖（仅使用 Python 标准库）

---

### 周报/月报自动生成器

**目录**: [weekly-report-generator/](weekly-report-generator/)

从 Git 提交记录、任务系统、文档变更中提取工作成果，自动生成结构化周报/月报。

#### 核心特性
- 🤖 自动化收集 - 从 Git、任务系统、文档中自动提取工作内容
- ⚡ 一键生成 - 一条命令生成完整周报，时间从 60 分钟缩短到 5 分钟
- 📊 数据驱动 - 基于真实的提交记录和任务数据，内容详实
- 🔧 灵活配置 - 支持周报/月报、自定义日期范围、个性化模板
- 📦 零依赖 - 仅使用 Python 标准库，开箱即用

#### 快速开始

```bash
# 进入目录
cd weekly-report-generator

# 生成周报
python src/cli.py --author "你的名字" --team "你的团队" --output examples/weekly_report.md

# 查看文档
cat weekly-report-generator/README.md
```

#### 项目统计
- **代码行数**: 724 行（核心代码 + 测试）
- **文档行数**: ~2100 行（完整使用文档）
- **依赖**: 零依赖（仅使用 Python 标准库）

---

## 📚 文档导航

### Windows C 盘清理
- [README](windows-cleaner/README.md) - 项目总览
- [SKILL](windows-cleaner/SKILL.md) - SOLO Skill 交互流程说明

### 周报/月报自动生成器
- [README](weekly-report-generator/README.md) - 项目总览
- [快速上手](weekly-report-generator/docs/QUICKSTART.md) - 5 分钟快速上手
- [完整文档](weekly-report-generator/docs/README_SKILL.md) - 详细使用说明
- [技术架构](weekly-report-generator/docs/PROJECT_SUMMARY.md) - 技术架构详解

---

## 🔧 项目结构

```
.
├── windows-cleaner/                  # Windows C 盘清理工具 🆕
│   ├── SKILL.md                     # SOLO Skill 定义
│   ├── README.md                    # 项目文档
│   ├── src/                         # 源代码
│   │   ├── windows_cleaner.py       # 核心清理逻辑
│   │   ├── cli.py                   # 命令行入口
│   │   └── __init__.py              # 包初始化
│   └── test_cleaner.py              # 测试脚本
├── weekly-report-generator/          # 周报/月报自动生成器
│   ├── SKILL.md                     # SOLO Skill 定义
│   ├── README.md                    # 项目文档
│   ├── src/                         # 源代码
│   │   ├── weekly_report_generator.py
│   │   ├── cli.py
│   │   └── test_report.py
│   ├── config/                      # 配置文件
│   │   ├── config.example.json
│   │   └── tasks.example.json
│   ├── scripts/                     # 脚本
│   │   └── demo.sh
│   ├── docs/                        # 文档
│   │   ├── README_SKILL.md
│   │   ├── QUICKSTART.md
│   │   └── PROJECT_SUMMARY.md
│   └── examples/                    # 示例
│       ├── sample_report.md
│       ├── weekly_report.md
│       └── order-api_weekly_report.md
└── README.md                        # 本文件
```

---

## 🤝 贡献与反馈

欢迎提出宝贵意见！

- 功能建议：还需要开发哪些 Skill？
- 使用体验：哪些地方可以优化？
- Bug 报告：遇到问题请详细描述

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-05-21