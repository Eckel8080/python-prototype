# 项目开发指南 (DEVELOPMENT)

本指南旨在帮助开发者快速配置本项目的本地开发环境，了解如何编写代码、运行测试并进行代码规范校验。

---

## 1. 快速开始

本项目使用 Python 3.11+，并采用现代 Python 包管理与运行工具 **`uv`**（配合 `pyproject.toml`）进行项目的虚拟环境与依赖管理。

### Step 1: 克隆/进入项目目录
确保你已在项目根目录下：
```bash
cd d:/Projects/Test
```

### Step 2: 创建虚拟环境
在项目根目录下创建一个 `.venv` 的虚拟环境：
```bash
uv venv
```

### Step 3: 同步依赖并初始化开发环境
同步安装项目运行及开发所需的全部依赖：
```bash
# 此命令将自动基于 pyproject.toml 及 uv.lock 在本地同步安装所有依赖
uv sync --native-tls
```

---

## 2. 运行测试

本项目使用 `pytest` 作为测试框架。依据项目规范，测试已被拆分为**单元测试**与**集成测试**。

### 运行所有测试
在根目录运行：
```bash
uv run pytest
```

### 打印详细输出与标准输出
```bash
uv run pytest -v -s
```

### 仅运行指定目录/文件
- **只运行单元测试**：`uv run pytest tests/unit`
- **只运行集成测试**：`uv run pytest tests/integration`
- **运行指定测试类/方法**：`uv run pytest tests/unit/services/test_user.py::TestUserService::test_create_user_success`

---

## 3. 运行开发服务器

在已安装依赖的状态下，可以通过以下命令启动本地 Web 服务：

```bash
uv run uvicorn src.my_project.app:app --reload
```

### 调试与 API 文档
启动服务后，可以通过浏览器访问以下页面：
- **交互式 API 文档 (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **备用 API 文档 (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 4. 代码格式化与 Lint

我们使用 `ruff` 工具进行极速的 Lint 静态检查和代码格式化，使用 `pyright` 进行类型检查。

### 运行 Lint 检查与自动修复
```bash
# 检查代码中的规范和语法问题
uv run ruff check .

# 自动修复可修复的静态检查问题并格式化
uv run ruff check --fix .
uv run ruff format .
```

### 运行静态类型检查
```bash
uv run pyright
```

---

## 5. 开发规范与 DoD (完成定义)

在编写代码时，请严格遵守 [`.agents/rules/python_development.md`](file:///d:/Projects/Test/.agents/rules/python_development.md) 规则：
1. **类型提示 (Type Hints)**：所有公开方法和函数必须声明完整的参数及返回值类型，新代码在 Pyright 下应当通过严格检查。
2. **测试分层**：
   - 核心业务逻辑应写入单元测试 `tests/unit/` 且避免任何真实 HTTP 链路和网络依赖。
   - API 路由端点行为放在集成测试 `tests/integration/` 中，使用数据工厂生成 payload，并断言响应。
3. **中文文档**：所有代码注释和 Docstrings 一律使用**中文（简体）**。
4. **测试覆盖**：新增或修改的核心业务代码应达到高分支覆盖，任何代码在合并主分支前必须通过全部质量门禁。
