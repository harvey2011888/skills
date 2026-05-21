# Git 提交规范

## 📋 提交信息格式

### 标准格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型说明（Type）
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具/配置更新

### Scope 说明
按模块分类，例如：
- `order`: 订单模块
- `refund`: 退款模块
- `api`: API 接口
- `db`: 数据库相关
- `config`: 配置文件

### Subject 要求
- 简洁明了，50 字以内
- 使用祈使句："add" 而不是 "added"
- 首字母不要大写
- 末尾不加句号

## ✅ 好的提交示例

```bash
# 新功能
feat(order): 添加订单筛选功能，支持按时间范围查询

# 修复 bug
fix(refund): 修复退款列表筛选条件失效的问题

# 接口更新
feat(api): 新增 v3 接口返回预缴税字段

# 性能优化
refactor(db): 优化订单查询 SQL，添加索引

# 配置更新
chore(config): 更新接口限流配置
```

## ❌ 避免的提交

```bash
# 太模糊
1
调整
add
提交
更新
测试

# 没有说明具体内容
修复问题
结构调整
```

## 🌿 分支管理策略

### 分支命名
- `main`: 主分支，随时可部署
- `feature/xxx`: 新功能分支
- `bugfix/xxx`: Bug 修复分支
- `hotfix/xxx`: 紧急修复分支

### 开发流程
1. 从 `main` 创建功能分支
2. 在功能分支上开发
3. 提交前确保代码通过测试
4. 推送到远程并创建 Pull Request
5. Code Review 后合并到 `main`

## 🔧 本地配置建议

### 配置 Git 模板
```bash
# ~/.gitmessage
feat: 
```

### 设置默认编辑器
```bash
git config --global core.editor "vim"
```

### 配置用户信息
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 📝 提交前检查清单

- [ ] 代码是否通过本地测试？
- [ ] 是否添加了必要的单元测试？
- [ ] 提交信息是否清晰描述了变更内容？
- [ ] 是否遵循了项目的代码规范？
- [ ] 是否有敏感信息（密码、Token）被提交？
