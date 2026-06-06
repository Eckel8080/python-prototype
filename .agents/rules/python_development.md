---
name: python-development-rules
description: Coding standards and guidelines for Python projects using pytest, pip, and venv.
---

# Python + pytest 开发规范

本规范适用于本项目的所有 Python 代码编写及测试用例开发。AI 助手在协助编写代码时必须严格遵守本规范。

---

## 1. 技术栈与运行环境

- **Python 版本**：最低支持 `Python 3.11+`。充分利用 3.11+ 的现代特性（例如 `X | Y` 类型联合语法，`typing.Self`，`ExceptionGroup` 等）。
- **包管理器**：使用传统的 `pip` 配合 `requirements.txt`。
- **环境管理**：使用内置的 `venv` 虚拟环境。默认环境目录为项目根目录下的 `.venv/`。
- **Web 核心框架**：使用 **FastAPI** 作为 Web 开发框架，配合 **Uvicorn** 异步网关。
- **数据校验**：使用 **Pydantic v2** 处理数据模型和校验。
- **Lint 与格式化**：使用 `ruff`。代码提交前必须通过 `ruff check` 和 `ruff format` 的验证。
- **代码风格**：严格遵循 PEP 8 风格指南。

---

## 2. 目录结构规范

项目应采用如下标准结构（在开始开发时逐步建立）：
```text
<project_root>/
├── .agents/
│   └── rules/
│       └── python_development.md  # 本规则文件
├── .venv/                         # 虚拟环境目录（已在 .gitignore 中排除）
├── src/                           # 源代码目录
│   └── my_project/
│       ├── __init__.py
│       ├── main.py                # 应用程序入口及全局配置挂载
│       ├── core/                  # 核心配置、安全与全局依赖
│       │   ├── __init__.py
│       │   └── config.py          # 基于 Pydantic 的配置加载
│       ├── api/                   # API 路由 (Controllers)
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       └── users.py       # 用户相关路由端点
│       ├── schemas/               # 数据校验模型 (Pydantic)
│       │   ├── __init__.py
│       │   └── user.py            # 用户输入输出模型
│       └── services/              # 业务逻辑服务层
│           ├── __init__.py
│           └── user.py            # 用户业务逻辑
├── tests/                         # 测试用例目录
│   ├── conftest.py                # 全局 fixtures
│   ├── test_api.py                # 接口路由集成测试
│   └── test_main.py               # 基础功能测试
├── .gitignore                     # Git 忽略配置
├── DEVELOPMENT.md                 # 开发者本地指南
└── requirements.txt               # 项目依赖声明
```

---

## 3. 代码风格与质量约束

### 3.1 命名规范
- **包名与模块名**：采用小写字母。包名尽量不使用下划线（但为了提高可读性允许使用，例如 `my_project`），且**绝对禁止使用连字符**（例如 `my-project` 会导致 Python 导入语法错误）。
- **类名**：采用 `PascalCase`（例如 `UserManager`）。
- **函数、方法、变量**：采用 `snake_case`（例如 `get_user_by_id`）。
- **常量**：全大写加下划线 `UPPER_CASE_SNAKE`（例如 `MAX_RETRY_COUNT`）。

### 3.2 类型提示 (Type Hints)
- **要求**：所有新编写的函数和方法**必须**显式声明参数和返回值的类型提示。
- **避免 Any**：严禁无理由滥用 `typing.Any`。若无法确定类型，应使用具体的联合类型或 `object`。
- **示例**：
  ```python
  def get_user_status(user_id: int) -> str | None:
      ...
  ```

### 3.3 注释与 Docstring
- **语言**：注释、Docstring 以及说明文档一律使用**中文（简体）**。
- **格式**：公共类、模块、公开函数必须使用 **Google 风格** 的 Docstring。
- **示例**：
  ```python
  def calculate_tax(price: float, rate: float = 0.08) -> float:
      """计算商品含税价格。

      Args:
          price: 商品不含税原价。
          rate: 税率，默认为 0.08。

      Returns:
          计算出来的含税价格。

      Raises:
          ValueError: 当价格或税率小于 0 时抛出。
      """
      if price < 0 or rate < 0:
          raise ValueError("价格和税率不能为负数")
      return price * (1 + rate)
  ```

---

## 4. pytest 测试规范

### 4.1 测试命名与组织
- **测试文件**：必须以 `test_` 开头（例如 `test_auth.py`）。
- **测试类**：必须以 `Test` 开头，且不包含 `__init__` 方法。
- **测试函数/方法**：必须以 `test_` 开头。

### 4.2 编写模式：Arrange-Act-Assert (AAA)
每个测试用例应通过空行划分为三个清晰的部分：
1. **Arrange**：准备测试数据、Mock 对象及上下文环境。
2. **Act**：调用被测函数或方法。
3. **Assert**：断言结果是否符合预期。

**示例**：
```python
def test_calculate_tax_success():
    # Arrange
    price = 100.0
    rate = 0.1
    
    # Act
    result = calculate_tax(price, rate)
    
    # Assert
    assert result == 110.0
```

### 4.3 Fixture 规范
- **类型提示**：Fixture 函数必须声明返回值类型。
- **作用域**：根据需要合理声明 `scope`（如 `function`、`module`、`session` 等），避免不必要的重复初始化。
- **共享**：跨模块共享的 fixture 必须放置在 `conftest.py` 中。
- **示例**：
  ```python
  import pytest
  from typing import Generator
  
  @pytest.fixture(scope="function")
  def db_connection() -> Generator[DbConn, None, None]:
      # Arrange / Setup
      conn = DbConn()
      conn.connect()
      yield conn
      # Clean up / Teardown
      conn.close()
  ```

### 4.4 Mock 规范
- **隔离性**：测试应当与外部服务隔离。对于所有网络请求、数据库写操作、外部 API 调用，**必须**进行 Mock。
- **工具**：优先使用 `unittest.mock` 或 `pytest-mock`（推荐使用 `mocker` fixture）。
- **示例**：
  ```python
  def test_fetch_user_profile(mocker):
      # Arrange
      mock_get = mocker.patch("requests.get")
      mock_get.return_value.json.return_value = {"name": "Alice"}
      
      # Act
      profile = user_service.fetch_profile(123)
      
      # Assert
      assert profile["name"] == "Alice"
      mock_get.assert_called_once_with("https://api.example.com/users/123")
  ```

### 4.5 Web API 测试规范
- **测试客户端**：使用 FastAPI 提供的 `fastapi.testclient.TestClient` 对 HTTP 路由进行同步集成测试，或对于异步端点使用 `httpx.AsyncClient`。
- **依赖覆盖**：在测试需要隔离外部资源（例如数据库 Session 或认证依赖）时，通过 `app.dependency_overrides` 替换真实的依赖。
- **示例**：
  ```python
  from fastapi.testclient import TestClient
  from my_project.main import app
  from my_project.services.user import UserService

  client = TestClient(app)

  def test_get_user_by_id_api(mocker):
      # Arrange
      mock_user = {"id": 1, "username": "test_user", "email": "test@example.com"}
      mocker.patch.object(UserService, "get_user_by_id", return_value=mock_user)
      
      # Act
      response = client.get("/api/v1/users/1")
      
      # Assert
      assert response.status_code == 200
      assert response.json()["username"] == "test_user"
  ```

---

## 5. AI 开发原则 (AI Development Rules)

当 AI 助手生成或重构代码时，应满足以下条件：
1. **测试先行或同步**：修改或添加业务逻辑时，必须提供对应的 pytest 测试用例或更新现有用例。
2. **保持现有文档与注释完整性**：除非显式要求，否则不要删除现有的中文注释和 docstring。
3. **格式化验证**：在修改完 Python 代码后，若环境配置了 ruff，应建议或自行运行 `ruff` 检查以保证代码质量。

---

## 6. Web 框架规范 (FastAPI)

### 6.1 接口路由与端点设计
- **路由版本控制**：API 路由必须包含版本号前缀（例如 `/api/v1`），并通过 `APIRouter` 进行模块化组织。
- **显式契约声明**：在定义路由端点时，**必须**显式指定 `response_model`（响应 Schema）和 `status_code`（成功时的 HTTP 状态码），例如 `@router.post("/", response_model=UserResponse, status_code=201)`。
- **无状态设计**：API 端点保持无状态，以方便横向扩展。

### 6.2 Pydantic 数据模型与校验
- **输入校验与输出过滤**：所有向客户端暴露的输入体和输出响应**必须**定义对应的 Pydantic 模型。严禁将原始的数据库模型（如 SQLAlchemy 模型）直接返回给客户端。
- **强类型与校验属性**：合理使用 Pydantic 的 `Field` 进行字段长度、格式、大小的强约束，如 `Field(..., min_length=3, max_length=50)`，从而自动拦截不合规请求并返回 422 错误。

### 6.3 业务逻辑分层 (Separation of Concerns)
- **极简的路由层 (Thin Controllers)**：路由函数只负责接收 HTTP 请求、提取参数、进行依赖注入校验（如认证），然后立即调用 Service 层处理业务逻辑，最后将结果返回。严禁在路由函数中直写数据库 SQL/ORM 查询或复杂的计算。
- **服务层 (Thick Services)**：所有的业务逻辑、计算规则、事务以及数据库交互逻辑，必须封装在 `services/` 模块的类或函数中。

### 6.4 依赖注入 (Dependency Injection)
- **统一生命周期管理**：推荐使用 FastAPI 的 `Depends` 实现依赖注入，例如获取数据库连接、第三方服务 Client、权限校验和当前登录用户等。
- **示例**：
  ```python
  from fastapi import Depends
  from my_project.services.user import UserService
  
  def get_user_service() -> UserService:
      return UserService()
  
  @router.get("/{user_id}", response_model=UserResponse)
  def read_user(user_id: int, service: UserService = Depends(get_user_service)):
      user = service.get_user_by_id(user_id)
      return user
  ```

### 6.5 全局异常处理
- **优雅的错误展示**：严禁将原始代码报错（如 Traceback 或数据库 Exception）直接反馈给客户端。
- **自定义异常与捕获**：
  - 正常的业务逻辑错误，应当抛出带有统一属性的自定义异常（例如 `BusinessException`）。
  - 在 `main.py` 中注册全局异常处理器，拦截这些异常，并统一返回标准化 JSON 格式，如 `{"detail": "错误信息", "error_code": "USER_NOT_FOUND"}`。
  - 对于未预料的系统级异常，由全局处理器捕获，记录日志，并统一向外部返回 500 状态码，避免敏感信息泄露。

### 6.6 异步编程 (async / await)
- **谨慎选择 `async def` 与 `def`**：
  - 如果接口内的操作（如网络 IO、第三方 HTTP 请求、支持异步的数据库驱动）全都是异步的，请使用 `async def`。
  - 如果接口内包含了阻塞性的操作（例如使用了同步的数据库驱动、进行了密集 CPU 计算、使用了 `requests` 库），应使用 `def`。FastAPI 会自动在独立的外部线程池中执行同步端点，防止阻塞主事件循环。
- **异步安全性**：在异步函数中，严禁调用未经特殊处理的同步阻塞 IO 函数。
