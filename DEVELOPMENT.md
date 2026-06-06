# 项目开发指南 (DEVELOPMENT)

本指南旨在帮助开发者快速配置本项目的本地开发环境，了解如何编写代码、运行测试并进行代码规范校验。

---

## 1. 快速开始

本项目使用 Python 3.11+、内置的 `venv` 进行虚拟环境管理，并使用 `pip` 进行包管理。

### Step 1: 克隆/进入项目目录
确保你已在项目根目录下：
```bash
cd d:/Projects/Test
```

### Step 2: 创建虚拟环境
在项目根目录下创建一个名为 `.venv` 的虚拟环境：
```bash
# Windows
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```

### Step 3: 激活虚拟环境
根据你的操作系统激活虚拟环境：
- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (CMD)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```

### Step 4: 安装项目依赖
安装项目运行及开发所需的全部依赖：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> [!NOTE]
> 如果你是首次初始化项目且 `requirements.txt` 尚未创建，可以先安装核心开发工具并保存：
> ```bash
> pip install pytest pytest-mock ruff
> pip freeze > requirements.txt
> ```

---

## 2. 运行测试

本项目使用 `pytest` 作为测试框架。

### 运行所有测试
在激活虚拟环境的状态下，在根目录运行：
```bash
pytest
```

### 常用 pytest 命令参数
- **打印详细输出**：`pytest -v`
- **打印标准输出 (print语句)**：`pytest -s`
- **运行指定文件**：`pytest tests/test_main.py`
- **运行指定测试类/方法**：`pytest tests/test_main.py::TestClass::test_method`

---

## 3. 运行开发服务器

在激活虚拟环境且已安装依赖的状态下，可以在根目录下运行以下命令启动本地 Web 服务：

```bash
uvicorn src.my_project.main:app --reload
```

### 调试与 API 文档
启动服务后，可以通过浏览器访问以下页面：
- **交互式 API 文档 (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **备用 API 文档 (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 4. 代码格式化与 Lint

我们使用 `ruff` 代替传统的 black、flake8 和 isort，它提供极速的 Linting 和格式化。

### 运行 Lint 检查
检查代码中是否存在不规范的语法或风格问题：
```bash
ruff check
```

### 自动修复 Lint 问题并格式化代码
自动修复可修复的 Lint 错误，并对代码进行排版格式化：
```bash
# 修复 lint 并格式化
ruff check --fix
ruff format
```

---

## 5. 开发规范摘要

在编写代码时，请遵守 [`.agents/rules/python_development.md`](file:///d:/Projects/Test/.agents/rules/python_development.md) 规则：
1. **类型提示 (Type Hints)**：所有公开的方法和函数必须声明完整的参数及返回值类型。
2. **测试同行**：任何新增的业务逻辑（位于 `src/`）必须有对应的单元测试用例（位于 `tests/`）。
3. **中文文档**：所有代码注释和 Docstrings 一律使用**中文（简体）**。
4. **接口规范**：新写的 API 应定义 Pydantic 输入输出 Schema，并将复杂业务逻辑写入服务层（Services）。

