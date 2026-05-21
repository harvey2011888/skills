# Windows C盘清理 Skill 计划

## 1. 目标概述

创建一个 SOLO Skill，用于清理 Windows 系统 C 盘的常见占用空间的文件和文件夹，帮助用户释放磁盘空间。

## 2. 功能设计

### 核心清理功能

| 清理项 | 路径/规则 | 说明 |
|--------|-----------|------|
| 临时文件 | `%TEMP%`、`C:\Windows\Temp` | 用户和系统临时文件 |
| Windows 更新缓存 | `C:\Windows\SoftwareDistribution\Download` | 更新后残留文件 |
| 回收站 | `$Recycle.Bin` | 已删除文件 |
| Prefetch 文件 | `C:\Windows\Prefetch` | 系统预读取文件 |
| 浏览器缓存 | Chrome/Firefox/Edge 默认缓存目录 | 浏览器缓存 |
| 日志文件 | `C:\Windows\Logs`、`C:\Windows\Panther` | 系统日志 |
| Windows 错误报告 | `C:\ProgramData\Microsoft\Windows\WER` | 错误报告文件 |

### 用户交互流程

1. **扫描阶段**：统计各类清理项的占用空间
2. **预览阶段**：展示清理项清单及大小，由用户确认
3. **执行阶段**：执行选中的清理操作
4. **报告阶段**：展示清理结果（释放空间总量）

## 3. 技术实现

### 文件结构

```
windows-cleaner/
├── index.ts           # Skill 主入口
├── commands/
│   ├── scan.ts        # 扫描命令
│   ├── clean.ts       # 清理命令
│   └── preview.ts     # 预览命令
├── utils/
│   ├── disk-analyzer.ts   # 磁盘分析工具
│   ├── file-cleaner.ts    # 文件清理工具
│   └── system-info.ts     # 系统信息获取
└── types/
    └── index.ts       # 类型定义
```

### 核心模块

#### DiskAnalyzer
- 递归计算目录大小
- 过滤系统关键文件
- 并行扫描提升性能

#### FileCleaner
- 安全删除（跳过系统关键文件）
- 删除确认机制
- 错误处理与回滚

## 4. 安全机制

1. **白名单保护**：跳过 Windows 系统目录中的关键文件
2. **权限检查**：确认管理员权限
3. **用户确认**：删除前必须用户确认
4. **选择性清理**：用户可选择清理项

## 5. 实现步骤

1. 创建 Skill 目录结构和基础配置
2. 实现 `types/index.ts` - 类型定义
3. 实现 `utils/system-info.ts` - 系统信息获取
4. 实现 `utils/disk-analyzer.ts` - 磁盘分析
5. 实现 `utils/file-cleaner.ts` - 文件清理
6. 实现 `commands/scan.ts` - 扫描命令
7. 实现 `commands/preview.ts` - 预览命令
8. 实现 `commands/clean.ts` - 清理命令
9. 实现 `index.ts` - 主入口
10. 测试与优化

## 6. 注意事项

- 仅支持 Windows 系统
- 部分清理项需要管理员权限
- 跳过正在使用的文件
- 保留最近日期的系统文件
