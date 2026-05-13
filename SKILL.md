---
name: 周报月报自动生成器
description: 从 Git 提交记录、任务系统、文档变更中自动提取工作成果，一键生成结构化周报/月报
version: 1.0.0
author: 参赛者
tags:
  - 效率工具
  - 周报
  - Git
  - 自动化
category: 效率提升
---

# 周报/月报自动生成器

## 技能说明

这是一个智能周报/月报生成助手，可以从你的 Git 提交记录、任务系统、文档变更中提取工作成果，自动生成结构化的周报或月报。

## 核心功能

- **自动收集 Git 提交** - 分析代码提交记录，统计提交数量、文件修改情况
- **任务系统集成** - 支持 JSON/Markdown 格式的任务文件，自动提取完成情况
- **文档变更追踪** - 追踪技术文档、API 文档、README 等的更新情况
- **智能分类汇总** - 自动分类整理工作内容，生成结构化报告
- **灵活配置** - 支持周报/月报、自定义日期范围、个性化模板
- **零依赖** - 仅使用 Python 标准库，开箱即用

## 使用场景

- 开发者需要定期提交周报/月报
- 技术团队负责人需要收集团队成员的工作汇报
- 项目经理需要追踪项目进展和文档更新
- 任何需要定期总结工作成果的场景

## 使用方式

### 方式一：对话使用

直接向 SOLO 提问：

```
帮我生成本周的周报
```

```
生成 5 月份的月报，包含 Git 提交和任务完成情况
```

```
我想看上周的工作总结，从 5 月 6 日到 5 月 12 日
```

### 方式二：命令行工具

如果你下载了完整的 Skill 包，可以使用命令行：

```bash
# 生成周报
python cli.py --author "你的名字" --team "你的团队" --output weekly_report.md

# 生成月报
python cli.py --type monthly --output monthly_report.md

# 指定日期范围
python cli.py --start-date 2026-05-01 --end-date 2026-05-31

# 使用配置文件
python cli.py --config config.json --output report.md
```

### 方式三：Python 代码调用

```python
from weekly_report_generator import ReportGenerator, ReportConfig

# 创建配置
config = ReportConfig(
    report_type="weekly",
    author_name="张三",
    team_name="开发团队",
    highlights=[
        "完成了用户认证模块",
        "优化了数据库查询性能"
    ],
    challenges=["跨团队协作需要加强"],
    plans=["推进新功能开发"]
)

# 生成报告
generator = ReportGenerator(config)
report = generator.generate()

# 保存报告
with open("weekly_report.md", "w", encoding="utf-8") as f:
    f.write(report)
```

## 配置说明

### 配置文件示例 (config.json)

```json
{
  "report_type": "weekly",
  "git_repo_path": ".",
  "include_git": true,
  "include_tasks": true,
  "include_documents": true,
  "author_name": "你的名字",
  "team_name": "你的团队",
  "highlights": [
    "完成了核心功能模块的开发",
    "优化了系统性能，响应速度提升 50%"
  ],
  "challenges": [
    "某个技术难点需要进一步研究"
  ],
  "plans": [
    "继续推进 XX 功能的开发",
    "准备技术分享"
  ]
}
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `report_type` | string | "weekly" | 报告类型：weekly(周报) 或 monthly(月报) |
| `git_repo_path` | string | "." | Git 仓库路径 |
| `include_git` | boolean | true | 是否包含 Git 提交记录 |
| `include_tasks` | boolean | true | 是否包含任务信息 |
| `include_documents` | boolean | true | 是否包含文档变更 |
| `author_name` | string | "" | 汇报人姓名 |
| `team_name` | string | "" | 团队名称 |
| `highlights` | array | [] | 工作亮点列表 |
| `challenges` | array | [] | 遇到的挑战列表 |
| `plans` | array | [] | 下阶段计划列表 |

## 任务文件格式

### JSON 格式 (tasks.json)

```json
{
  "tasks": [
    {
      "id": "TASK-001",
      "title": "实现用户登录功能",
      "status": "completed",
      "priority": "high",
      "description": "完成用户登录、注册功能",
      "completed_date": "2026-05-10"
    },
    {
      "id": "TASK-002",
      "title": "编写 API 文档",
      "status": "pending",
      "priority": "medium"
    }
  ]
}
```

### Markdown 格式 (TODO.md)

```markdown
# 任务列表

- [x] 实现用户登录功能 (high)
- [ ] 编写 API 文档 (medium)
- [x] 优化数据库查询 (high)
```

## 输出示例

生成的周报包含以下部分：

1. **代码提交** - Git 提交统计、主要提交列表、文件类型分布
2. **任务完成情况** - 完成/进行中任务统计、详细任务列表
3. **文档更新** - 技术文档、API 文档、README 等更新情况
4. **工作亮点** - 本周/本月的主要工作成果
5. **遇到的问题与挑战** - 需要解决的困难
6. **下周/下月计划** - 下一步工作计划

## 系统要求

- Python 3.7+
- Git 已安装并配置
- 仅需 Python 标准库（零依赖）

## 快速开始

1. **确保环境就绪**
   ```bash
   python --version  # 确保 Python 3.7+
   git --version     # 确保 Git 已安装
   ```

2. **生成周报**
   ```bash
   python cli.py --author "张三" --team "开发组" --output weekly_report.md
   ```

3. **查看报告**
   打开生成的 `weekly_report.md` 文件查看完整周报

## 高级用法

### 集成到 CI/CD

在 GitHub Actions 中自动生成周报：

```yaml
name: Weekly Report
on:
  schedule:
    - cron: '0 9 * * 5'  # 每周五上午 9 点

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Weekly Report
        run: |
          python cli.py --output weekly_report.md
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: weekly-report
          path: weekly_report.md
```

### 自定义模板

继承 `ReportGenerator` 类创建自定义生成器：

```python
from weekly_report_generator import ReportGenerator

class CustomReportGenerator(ReportGenerator):
    def _generate_git_section(self, commits, stats):
        # 自定义 Git 提交部分的生成逻辑
        pass
```

## 常见问题

### Q: 需要安装什么依赖？
A: 零依赖！只需要 Python 3.7+ 和 Git。

### Q: 提示"未找到 git 命令"怎么办？
A: 请安装 Git：
- Windows: 下载 [Git for Windows](https://gitforwindows.org/)
- macOS: `xcode-select --install`
- Linux: `sudo apt-get install git`

### Q: 生成的报告是空的怎么办？
A: 检查：
1. 当前目录是否是 Git 仓库（包含 `.git` 文件夹）
2. 指定日期范围内是否有提交记录
3. 使用 `--start-date` 和 `--end-date` 指定正确的日期范围

### Q: 能集成 Jira/Trello 吗？
A: 当前版本支持 JSON 和 Markdown 格式的任务文件。可以通过导出功能将 Jira/Trello 任务导出为 JSON 格式后使用。

### Q: 如何自定义报告模板？
A: 继承 `ReportGenerator` 类，重写各个 `_generate_*_section` 方法即可自定义模板。

## 技术架构

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

## 项目统计

- **代码行数**: 724 行（核心代码 + 测试）
- **文档行数**: 2100+ 行（完整使用文档）
- **测试覆盖**: 4 个测试场景全部通过
- **依赖**: 零依赖（仅使用 Python 标准库）

## 更新日志

### v1.0.0 (2026-05-13)
- ✨ 初始版本发布
- ✨ 支持 Git 提交记录提取
- ✨ 支持任务系统集成
- ✨ 支持文档变更追踪
- ✨ 支持周报/月报生成

## 贡献与反馈

欢迎提出宝贵意见：

- 功能建议：还需要集成哪些数据源？
- 使用体验：哪些地方可以优化？
- Bug 报告：遇到问题请详细描述

## 许可证

MIT License

## 致谢

感谢 SOLO 技能创作赛提供这个平台！

---

**参赛宣言**：用自动化解放生产力，让周报不再成为负担！
