# 周报/月报自动生成器

> 一个智能的周报/月报生成工具，从 Git 提交记录、任务系统、文档变更中提取工作成果，自动生成结构化的周报或月报。

## 📋 目录

- [功能特点](#-功能特点)
- [快速开始](#-快速开始)
- [使用方式](#-使用方式)
- [配置说明](#-配置说明)
- [示例输出](#-示例输出)
- [高级用法](#-高级用法)
- [常见问题](#-常见问题)

## ✨ 功能特点

- **自动收集 Git 提交** - 分析代码提交记录，统计提交数量、文件修改情况
- **任务系统集成** - 支持 JSON/Markdown 格式的任务文件，自动提取完成情况
- **文档变更追踪** - 追踪技术文档、API 文档、README 等的更新情况
- **智能分类汇总** - 自动分类整理工作内容，生成结构化报告
- **灵活配置** - 支持周报/月报、自定义日期范围、个性化模板
- **多格式输出** - 支持 Markdown、HTML、纯文本等格式

## 🚀 快速开始

### 1. 基础使用

生成默认周报（自动计算本周日期范围）：

```bash
python cli.py
```

生成月报：

```bash
python cli.py --type monthly
```

### 2. 指定日期范围

```bash
python cli.py --start-date 2026-05-01 --end-date 2026-05-31
```

### 3. 使用配置文件

```bash
python cli.py --config config.json --output weekly_report.md
```

## 💻 使用方式

### 方式一：命令行工具

```bash
# 生成周报并保存到文件
python cli.py --output weekly_report.md

# 生成月报，指定作者和团队
python cli.py --type monthly --author "张三" --team "后端开发组"

# 只使用 Git 提交记录
python cli.py --no-tasks --no-docs

# 使用自定义配置
python cli.py --config my_config.json --repo /path/to/repo
```

### 方式二：Python 代码调用

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

### 方式三：作为 Skill 使用

在 SOLO 中配置此 Skill 后，可以直接对话：

```
帮我生成本周的周报，包含 Git 提交和任务完成情况
```

## ⚙️ 配置说明

### 配置文件示例 (config.json)

```json
{
  "report_type": "weekly",
  "git_repo_path": ".",
  "include_git": true,
  "include_tasks": true,
  "include_documents": true,
  "output_format": "markdown",
  "language": "zh",
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
| `output_format` | string | "markdown" | 输出格式：markdown, html, text |
| `author_name` | string | "" | 汇报人姓名 |
| `team_name` | string | "" | 团队名称 |
| `highlights` | array | [] | 工作亮点列表 |
| `challenges` | array | [] | 遇到的挑战列表 |
| `plans` | array | [] | 下阶段计划列表 |

### 任务文件格式

#### JSON 格式 (tasks.json)

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
    }
  ]
}
```

#### Markdown 格式 (TODO.md)

```markdown
# 任务列表

- [x] 实现用户登录功能 (high)
- [ ] 编写 API 文档 (medium)
- [x] 优化数据库查询 (high)
```

## 📄 示例输出

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
- `i9j0k1l2` 修复登录页面 bug (张三，2026-05-07)

### 文件类型分布

- .py: 8 次修改
- .js: 5 次修改
- .md: 2 次修改

## 任务完成情况

- **完成任务数**: 5
- **进行中任务数**: 2

### 已完成任务

- ✅ [TASK-001] [high] 实现用户登录功能
- ✅ [TASK-002] [medium] 优化数据库查询性能

### 进行中任务

- 🔄 [TASK-003] [low] 编写 API 文档

## 文档更新

### 技术文档

- 📄 docs/api.md (2026-05-09)
- 📄 docs/guide.md (2026-05-08)

## 工作亮点

- ✨ 完成了核心功能模块的开发
- ✨ 优化了系统性能，响应速度提升 50%

## 遇到的问题与挑战

- ⚠️ 跨团队协作沟通成本较高

## 下周/下月计划

- 📌 继续推进 XX 功能的开发
- 📌 准备技术分享：XXX 主题
```

## 🔧 高级用法

### 1. 集成到 CI/CD

在 GitHub Actions 中自动生成本周报告：

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

### 2. 自定义模板

继承 `ReportGenerator` 类创建自定义生成器：

```python
from weekly_report_generator import ReportGenerator

class CustomReportGenerator(ReportGenerator):
    def _generate_git_section(self, commits, stats):
        # 自定义 Git 提交部分的生成逻辑
        pass
```

### 3. 批量生成

为团队成员批量生成报告：

```python
team_members = ["张三", "李四", "王五"]

for member in team_members:
    config = ReportConfig(author_name=member)
    generator = ReportGenerator(config)
    report = generator.generate()
    
    with open(f"{member}_weekly_report.md", "w", encoding="utf-8") as f:
        f.write(report)
```

## ❓ 常见问题

### Q: 没有 Git 仓库怎么办？

A: 可以使用 `--no-git` 参数禁用 Git 提交记录功能，只使用任务和文档信息。

### Q: 如何集成 Jira/Trello 等任务系统？

A: 可以编写适配器从这些系统导出任务为 JSON 格式，然后使用 `TaskExtractor` 加载。

### Q: 能自动生成工作亮点吗？

A: 当前版本需要手动填写亮点，但可以基于 Git 提交和任务完成情况智能推荐（计划中功能）。

### Q: 如何修改报告模板？

A: 可以继承 `ReportGenerator` 类，重写各个 `_generate_*_section` 方法来自定义模板。

### Q: 支持哪些日期格式？

A: 推荐使用 `YYYY-MM-DD` 格式，如 `2026-05-13`。

## 📝 更新日志

### v1.0.0 (2026-05-13)
- ✨ 初始版本发布
- ✨ 支持 Git 提交记录提取
- ✨ 支持任务系统集成
- ✨ 支持文档变更追踪
- ✨ 支持周报/月报生成

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
