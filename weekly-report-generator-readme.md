# 📅 周报/月报自动生成器

> **SOLO 技能创作赛参赛作品** - 从 Git 提交记录、任务系统、文档变更中提取工作成果，自动生成结构化周报/月报

## ✨ 核心特性

- 🤖 **自动化收集** - 从 Git、任务系统、文档中自动提取工作内容
- ⚡ **一键生成** - 一条命令生成完整周报，时间从 60 分钟缩短到 5 分钟
- 📊 **数据驱动** - 基于真实的提交记录和任务数据，内容详实
- 🔧 **灵活配置** - 支持周报/月报、自定义日期范围、个性化模板
- 📦 **零依赖** - 仅使用 Python 标准库，开箱即用

## 🚀 快速开始

### 5 秒生成周报

```bash
# 安装（如果需要）
# 确保已安装 Python 3.7+ 和 Git

# 生成周报
python src/cli.py --author "你的名字" --team "你的团队" --output examples/weekly_report.md
```

### 查看生成的报告

打开 `examples/weekly_report.md` 即可看到完整的周报！

## 📁 文件说明

### 核心文件 (src/)
- `weekly_report_generator.py` - 核心库（432 行）
- `cli.py` - 命令行工具（112 行）
- `test_report.py` - 测试脚本（180 行）

### 文档文件 (docs/)
- `QUICKSTART.md` - **5 分钟快速上手指南** ⭐ 推荐从这里开始
- `README_SKILL.md` - 完整使用文档
- `PROJECT_SUMMARY.md` - 项目总结和技术架构

### 示例文件 (examples/)
- `sample_report.md` - 示例周报
- `weekly_report.md` - 周报模板
- `order-api_weekly_report.md` - Order-API 项目周报示例

### 配置文件 (config/)
- `config.example.json` - 配置文件示例
- `tasks.example.json` - 任务文件示例

### 脚本文件 (scripts/)
- `demo.sh` - 演示脚本

## 💻 使用方式

### 方式一：命令行工具

```bash
# 基础用法
python src/cli.py --author "张三" --team "开发组" --output report.md

# 生成月报
python src/cli.py --type monthly --output monthly_report.md

# 指定日期范围
python src/cli.py --start-date 2026-05-01 --end-date 2026-05-31

# 使用配置文件
python src/cli.py --config config.json --output report.md
```

### 方式二：Python 代码

```python
from src.weekly_report_generator import ReportGenerator, ReportConfig

config = ReportConfig(
    report_type="weekly",
    author_name="张三",
    team_name="开发团队",
    highlights=["完成核心功能开发"],
    challenges=["需要优化数据库"],
    plans=["推进新功能"]
)

generator = ReportGenerator(config)
report = generator.generate()

with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(report)
```

### 方式三：运行演示

```bash
# 运行完整演示
./scripts/demo.sh

# 运行测试
python src/test_report.py
```

## 📊 生成的报告示例

```markdown
# 周报 (2026-05-06 ~ 2026-05-13)

**汇报人**: 张三
**团队**: 开发团队

---

## 代码提交

- **总提交数**: 15
- **最活跃日期**: 2026-05-09

### 主要提交

- `a1b2c3d4` 实现用户认证功能 (张三，2026-05-09)
- `e5f6g7h8` 优化数据库查询性能 (张三，2026-05-08)

## 任务完成情况

- **完成任务数**: 5
- **进行中任务数**: 2

### 已完成任务

- ✅ [TASK-001] [high] 实现用户登录功能
- ✅ [TASK-002] [medium] 优化数据库查询

## 文档更新

### 技术文档

- 📄 docs/api.md (2026-05-09)

## 工作亮点

- ✨ 完成了核心功能模块开发
- ✨ 优化了系统性能，响应速度提升 50%

## 遇到的问题与挑战

- ⚠️ 跨团队协作需要加强

## 下周/下月计划

- 📌 继续推进 XX 功能开发
- 📌 准备技术分享
```

## 🎯 参赛信息

**比赛名称**：一切皆可 Skill｜SOLO 技能创作赛

**参赛赛道**：Skill 创作赛道

**比赛时间**：2026 年 5 月 12 日 - 2026 年 6 月 12 日

**参赛宣言**：用自动化解放生产力，让周报不再成为负担！

## 🏆 核心优势

| 标准 | 优势 |
|------|------|
| **实用性** | ⭐⭐⭐⭐⭐ 解决真实痛点，节省 55 分钟/周 |
| **创新性** | ⭐⭐⭐⭐ 自动化数据收集，多源整合 |
| **完成度** | ⭐⭐⭐⭐⭐ 功能完整，文档详尽，可直接使用 |
| **易用性** | ⭐⭐⭐⭐⭐ 零依赖，多种使用方式 |
| **可扩展性** | ⭐⭐⭐⭐ 模块化设计，易于扩展 |

## 📋 项目统计

- **代码行数**: 724 行（核心代码 + 测试）
- **文档行数**: ~2100 行（完整使用文档）
- **测试覆盖**: 4 个测试场景全部通过
- **依赖**: 零依赖（仅使用 Python 标准库）

## 🔧 技术架构

```
┌─────────────────────────────────────┐
│      周报/月报自动生成器            │
├─────────────────────────────────────┤
│  输入层                             │
│  - Git 仓库                         │
│  - 任务文件 (JSON/Markdown)         │
│  - 用户配置                         │
├─────────────────────────────────────┤
│  处理层                             │
│  - GitExtractor                     │
│  - TaskExtractor                    │
│  - DocumentChangeTracker            │
├─────────────────────────────────────┤
│  生成层                             │
│  - ReportGenerator                  │
│  - 模板系统                         │
├─────────────────────────────────────┤
│  输出层                             │
│  - Markdown 报告                    │
└─────────────────────────────────────┘
```

## 📚 文档导航

### 新手入门
1. 先看 [docs/QUICKSTART.md](docs/QUICKSTART.md) - 5 分钟快速上手
2. 运行 `python src/test_report.py` 查看测试效果
3. 运行 `./scripts/demo.sh` 体验完整功能

### 深入学习
1. 阅读 [docs/README_SKILL.md](docs/README_SKILL.md) - 完整功能说明
2. 查看 [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - 技术架构详解
3. 参考配置示例和任务示例

## ❓ 常见问题

### Q: 需要安装什么依赖？
A: 零依赖！只需要 Python 3.7+ 和 Git。

### Q: 如何在 Windows 上使用？
A: 确保安装了 Git for Windows，然后使用命令提示符或 PowerShell 运行。

### Q: 能集成 Jira/Trello 吗？
A: 当前版本支持 JSON 和 Markdown 格式的任务文件。可以通过导出功能将 Jira/Trello 任务导出为 JSON 格式。

### Q: 如何自定义报告模板？
A: 继承 `ReportGenerator` 类，重写各个 `_generate_*_section` 方法即可。

### Q: 支持定时自动生成吗？
A: 可以结合 cron（Linux/Mac）或 Task Scheduler（Windows）定时执行。也提供了 GitHub Actions 示例。

## 🤝 贡献与反馈

欢迎提出宝贵意见！

- 功能建议：还需要集成哪些数据源？
- 使用体验：哪些地方可以优化？
- Bug 报告：遇到问题请详细描述

## 📄 许可证

MIT License

## 🙏 致谢

感谢 SOLO 技能创作赛提供这个平台！

---

**最后更新**: 2026-05-21

**状态**: ✅ 完成开发，准备参赛
