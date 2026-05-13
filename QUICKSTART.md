# 快速开始 - 周报/月报自动生成器

## 5 分钟快速上手

### 步骤 1：确认环境

确保你已经安装了 Python 3.7+ 和 Git：

```bash
python --version
git --version
```

### 步骤 2：下载 Skill 文件

你需要以下文件：

- `weekly_report_generator.py` - 核心库
- `cli.py` - 命令行工具
- `config.example.json` - 配置文件示例

### 步骤 3：基础使用

#### 方式 A：生成简单周报

```bash
# 进入你的项目目录
cd /path/to/your/project

# 运行命令生成周报
python /path/to/cli.py --output weekly_report.md
```

#### 方式 B：生成带个人信息的周报

```bash
python /path/to/cli.py \
  --author "张三" \
  --team "后端开发组" \
  --output weekly_report.md
```

#### 方式 C：生成月报

```bash
python /path/to/cli.py \
  --type monthly \
  --author "张三" \
  --output monthly_report.md
```

### 步骤 4：使用配置文件（推荐）

1. 复制示例配置文件：

```bash
cp config.example.json config.json
```

2. 编辑 `config.json`，填写你的信息：

```json
{
  "report_type": "weekly",
  "author_name": "张三",
  "team_name": "后端开发组",
  "highlights": [
    "完成了用户认证模块开发",
    "优化了数据库查询性能"
  ],
  "challenges": [
    "跨团队协作需要加强"
  ],
  "plans": [
    "推进新功能开发",
    "准备技术分享"
  ]
}
```

3. 使用配置文件生成周报：

```bash
python /path/to/cli.py --config config.json --output weekly_report.md
```

### 步骤 5：查看生成的报告

打开生成的 `weekly_report.md` 文件，你会看到类似这样的内容：

```markdown
# 周报 (2026-05-06 ~ 2026-05-13)

**汇报人**: 张三
**团队**: 后端开发组

---

## 代码提交

- **总提交数**: 15
- **最活跃日期**: 2026-05-09

### 主要提交

- `a1b2c3d4` 实现用户认证功能 (张三，2026-05-09)
- `e5f6g7h8` 优化数据库查询性能 (张三，2026-05-08)

## 任务完成情况

本周暂无任务记录。

## 文档更新

本周暂无文档更新。

## 工作亮点

- ✨ 完成了用户认证模块开发
- ✨ 优化了数据库查询性能

## 遇到的问题与挑战

- ⚠️ 跨团队协作需要加强

## 下周/下月计划

- 📌 推进新功能开发
- 📌 准备技术分享
```

### 步骤 6：添加任务管理（可选）

如果你想让周报包含任务完成情况：

1. 创建 `tasks.json` 文件：

```json
{
  "tasks": [
    {
      "id": "TASK-001",
      "title": "实现用户登录功能",
      "status": "completed",
      "priority": "high",
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

2. 将文件放在项目根目录

3. 重新运行生成命令，周报会自动包含任务信息

## 常用命令速查

```bash
# 生成周报
python cli.py --output weekly_report.md

# 生成月报
python cli.py --type monthly --output monthly_report.md

# 指定日期范围
python cli.py --start-date 2026-05-01 --end-date 2026-05-31

# 指定作者和团队
python cli.py --author "张三" --team "后端组"

# 使用配置文件
python cli.py --config config.json --output report.md

# 只使用 Git 提交（不使用任务和文档）
python cli.py --no-tasks --no-docs

# 生成到指定目录
python cli.py --output /path/to/output/report.md
```

## 常见问题

### Q1: 提示 "未找到 git 命令"

**解决方案**：安装 Git

- Windows: 下载并安装 [Git for Windows](https://gitforwindows.org/)
- macOS: `xcode-select --install`
- Linux: `sudo apt-get install git` 或 `sudo yum install git`

### Q2: 生成的报告是空的

**可能原因**：
1. 当前目录不是 Git 仓库
2. 指定日期范围内没有提交记录

**解决方案**：
- 确保在项目根目录（包含 `.git` 文件夹）运行
- 使用 `--start-date` 和 `--end-date` 指定正确的日期范围

### Q3: 如何自定义周报内容？

**解决方案**：使用配置文件，在 `highlights`、`challenges`、`plans` 数组中填写你的内容

### Q4: 能集成到 CI/CD 吗？

**可以**！参考 GitHub Actions 示例：

```yaml
name: Weekly Report
on:
  schedule:
    - cron: '0 9 * * 5'
jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Weekly Report
        run: python cli.py --output weekly_report.md
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          path: weekly_report.md
```

## 下一步

- 查看完整文档：[README_SKILL.md](README_SKILL.md)
- 查看参赛帖子：[参赛帖子.md](参赛帖子.md)
- 查看配置示例：[config.example.json](config.example.json)
- 查看任务文件示例：[tasks.example.json](tasks.example.json)

---

**祝你使用愉快！如有问题欢迎反馈。**
