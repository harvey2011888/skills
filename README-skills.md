# 🎯 SOLO Skills 仓库

> 存放所有 SOLO 技能创作赛开发的 Skills

## 📦 包含的 Skills

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

### 周报/月报自动生成器
- [README](weekly-report-generator/README.md) - 项目总览
- [快速上手](weekly-report-generator/docs/QUICKSTART.md) - 5 分钟快速上手
- [完整文档](weekly-report-generator/docs/README_SKILL.md) - 详细使用说明
- [技术架构](weekly-report-generator/docs/PROJECT_SUMMARY.md) - 技术架构详解

---

## 🔧 项目结构

```
.
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
