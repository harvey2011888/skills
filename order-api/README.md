# Order API

订单管理系统 API 服务

## 📁 项目结构

```
order-api/
├── api/                    # API 路由定义
├── cli/                    # 命令行工具
├── docs/                   # 文档
├── etc/                    # 配置文件
├── font/                   # 字体文件（用于 PDF 生成）
├── internal/               # 内部包（私有实现）
│   ├── config/            # 配置管理
│   ├── handler/           # HTTP 处理器
│   ├── middleware/        # 中间件
│   ├── model/             # 数据模型
│   ├── repository/        # 数据访问层
│   ├── service/           # 业务逻辑层
│   └── ...
├── lang/                   # 国际化文件
├── pkg/                    # 公共包（可复用）
├── script/                 # 脚本文件
├── sql/                    # SQL 脚本
├── tools/                  # 工具程序
├── ts/                     # TypeScript 相关
├── vendor/                 # Go 依赖（vendor 模式）
├── .env                    # 环境变量配置
├── .gitignore              # Git 忽略规则
├── CONTRIBUTING.md         # 贡献指南
├── Dockerfile              # Docker 构建配置
├── go.mod                  # Go 模块定义
├── go.sum                  # Go 依赖校验
├── hubbuy.go               # 主程序入口
└── build.sh                # 构建脚本
```

## 🚀 快速开始

### 环境要求
- Go 1.19+
- MySQL 8.0+
- Docker（可选）

### 本地开发

```bash
# 安装依赖
go mod download

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库等信息

# 运行服务
go run hubbuy.go

# 或者使用脚本构建
./build.sh
```

### Docker 部署

```bash
# 构建镜像
docker build -t order-api .

# 运行容器
docker run -p 8080:8080 order-api
```

## 📝 开发规范

请参考 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解：
- Git 提交规范
- 分支管理策略
- 代码审查流程

## 🔧 配置说明

主要配置项在 `etc/` 目录下，环境变量在 `.env` 文件中配置。

### 数据库配置
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=order_db
```

### 服务配置
```env
SERVER_PORT=8080
SERVER_MODE=debug  # debug, release, test
```

## 📊 API 文档

API 文档位于 `docs/` 目录，或使用 Swagger UI 访问 `/swagger/index.html`

## 🧪 测试

```bash
# 运行单元测试
go test ./...

# 运行测试并生成覆盖率报告
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## 📦 构建

```bash
# 本地构建
go build -o order-api hubbuy.go

# 交叉编译（Linux）
GOOS=linux GOARCH=amd64 go build -o order-api hubbuy.go
```

## 👥 贡献者

当前主要贡献者：
- xiaochen
- micro
- Torch
- harvey2011888

## 📄 许可证

私有项目，请勿外传。
