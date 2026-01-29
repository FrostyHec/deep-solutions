# 项目结构说明

本文档详细介绍 `deep-solutions` 项目的目录结构、依赖管理和开发环境要求。

## 目录
- [目录结构](#目录结构)
- [核心目录说明](#核心目录说明)
- [依赖管理](#依赖管理)
- [Python 版本要求](#python-版本要求)
- [配置文件说明](#配置文件说明)

---

## 目录结构

```
deep-solutions/
├── src/                         # 源代码目录 (src-layout)
│   └── deep_solutions/          # 主包
│       ├── __init__.py          # 公共 API 入口
│       ├── _version.py          # 版本号 (自动生成)
│       ├── core.py              # 核心功能模块
│       └── utils.py             # 工具函数模块
│
├── tests/                       # 测试目录
│   ├── __init__.py
│   ├── test_core.py             # core 模块测试
│   └── test_utils.py            # utils 模块测试
│
├── docs/                        # 文档目录
│   ├── developers_guide.md      # 开发者入门指南
│   ├── project_structure.md     # 本文档
│   ├── code_standards.md        # 代码规范
│   ├── local_testing.md         # 本地测试指南
│   ├── ci_workflow.md           # CI 工作流说明
│   └── publishing.md            # PyPI 发布指南
│
├── scripts/                     # 脚本目录
│   ├── check.sh                 # 开发检查脚本
│   └── ci-local.sh              # CI 本地模拟脚本
│
├── .github/                     # GitHub 配置
│   └── workflows/               # GitHub Actions 工作流
│       ├── ci.yml               # CI 检查流程
│       ├── report.yml           # 测试报告发布
│       ├── publish.yml          # PyPI 发布
│       └── publish-test.yml     # TestPyPI 发布
│
├── .nonpublic/                  # 非公开文件（不在文档范围内）
│
├── pyproject.toml               # 项目配置 & 依赖定义
├── tox.ini                      # Tox 多版本测试配置
├── environment.yml              # Conda 环境配置
├── README.md                    # 项目说明
├── LICENSE                      # Apache 2.0 许可证
└── CHANGELOG.md                 # 更改日志
```

---

## 核心目录说明

### `src/deep_solutions/` - 源代码

采用 **src-layout** 布局，这是 Python 包的推荐结构：

- **优势**: 强制从安装的包导入，避免直接导入源码目录的问题
- **`__init__.py`**: 定义公共 API，所有对外暴露的类/函数都在这里导出
- **`_version.py`**: 由 `setuptools-scm` 自动生成，包含版本信息

```python
# 添加新模块的导出方式 (src/deep_solutions/__init__.py)
from .your_module import YourClass, your_function

__all__ = [
    "YourClass",
    "your_function",
    # ... 其他导出
]
```

### `tests/` - 测试目录

- 测试文件以 `test_` 开头
- 测试函数以 `test_` 开头
- 使用 pytest 框架

### `scripts/` - 脚本目录

| 脚本 | 用途 |
|------|------|
| `check.sh` | 开发时一键检查（格式化 + lint + 类型检查 + 测试） |
| `ci-local.sh` | 模拟完整 CI 流程（适合提交 PR 前验证） |

### `.github/workflows/` - CI/CD 工作流

| 工作流 | 触发条件 | 用途 |
|--------|----------|------|
| `ci.yml` | PR / Push to main | 代码质量检查和测试 |
| `report.yml` | CI 完成后 | 发布测试报告到 PR |
| `publish.yml` | 手动触发 | 发布到 PyPI |
| `publish-test.yml` | 手动触发 | 发布到 TestPyPI |

---

## 依赖管理

### 依赖分类

项目依赖在 `pyproject.toml` 中定义：

#### 核心依赖 (dependencies)

运行时必需的依赖：

```toml
dependencies = [
    "numpy>=1.17.0",
    "scipy>=1.5.0",
]
```

#### 开发依赖 (optional-dependencies.dev)

开发时需要的工具：

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",        # 测试框架
    "pytest-cov>=4.0.0",    # 测试覆盖率
    "ruff>=0.4.0",          # 代码格式化 & Lint
    "mypy>=1.0.0",          # 类型检查
    "build>=0.10.0",        # 包构建
    "twine>=4.0.0",         # 包发布
    "tox>=4.0.0",           # 多版本测试
    "tox-gh>=1.0.0",        # GitHub Actions 集成
]
```

#### 文档依赖 (optional-dependencies.docs)

构建文档需要的依赖：

```toml
docs = [
    "sphinx>=6.0.0",
    "sphinx-rtd-theme>=1.2.0",
]
```

### 安装方式

```bash
# 仅安装核心依赖
pip install .

# 安装核心 + 开发依赖（推荐开发时使用）
pip install -e ".[dev]"

# 安装所有依赖
pip install -e ".[dev,docs]"
```

### 添加新依赖

1. 编辑 `pyproject.toml` 中相应的依赖列表
2. 重新安装：`pip install -e ".[dev]"`

> **注意**: 不要在 `environment.yml` 中添加 Python 包，它仅用于管理 Python 版本。

---

## Python 版本要求

### 支持的版本

| Python 版本 | 状态 |
|-------------|------|
| 3.8 | ✅ 支持（开发版本） |
| 3.9 | ✅ 支持 |
| 3.10 | ✅ 支持 |
| 3.11 | ✅ 支持 |
| 3.12 | ✅ 支持 |
| 3.13 | ✅ 支持 |

### ⚠️ 开发必须使用 Python 3.8

**原因**：

1. **兼容性保证**: Python 3.8 是最低支持版本，只有在 3.8 下运行正确的代码才能保证向上兼容
2. **语法限制**: 避免使用高版本才有的语法特性（如 `match-case`、`|` 类型联合）
3. **类型注解**: 使用 `typing` 模块兼容旧版本，而不是内置类型注解

**不兼容示例**：

```python
# ❌ Python 3.10+ 语法 - 不要使用
def process(data: list[int] | None) -> dict[str, int]:
    match data:
        case None:
            return {}

# ✅ Python 3.8+ 语法 - 使用这种方式
from typing import Optional, List, Dict

def process(data: Optional[List[int]]) -> Dict[str, int]:
    if data is None:
        return {}
```

### 配置开发环境

```bash
# 创建 Python 3.8 环境
conda create -n deep-solutions python=3.8 -y
conda activate deep-solutions

# 安装依赖
pip install -e ".[dev]"
```

---

## 配置文件说明

### `pyproject.toml`

项目核心配置文件，包含：

| 部分 | 说明 |
|------|------|
| `[build-system]` | 构建系统配置（setuptools） |
| `[project]` | 包元数据（名称、版本、描述、依赖等） |
| `[tool.setuptools_scm]` | 版本号自动管理配置 |
| `[tool.ruff]` | Ruff 格式化和 Lint 配置 |
| `[tool.pytest.ini_options]` | pytest 配置 |
| `[tool.mypy]` | mypy 类型检查配置 |

### `tox.ini`

多版本测试配置：

```ini
[tox]
envlist = py38,py39,py310,py311,py312
```

### `environment.yml`

Conda 环境配置（仅 Python 版本）：

```yaml
name: deep-solutions
dependencies:
  - python=3.8
```

---

## 版本号管理

项目使用 **setuptools-scm** 自动管理版本号：

- **版本来源**: Git Tag（如 `v1.0.0`）
- **自动生成**: `src/deep_solutions/_version.py`
- **运行时读取**: 通过 `importlib.metadata`

```python
# 在代码中获取版本
import deep_solutions
print(deep_solutions.__version__)
```

### 版本号规范

遵循 [Semantic Versioning](https://semver.org/)：

```
vMAJOR.MINOR.PATCH

- MAJOR: 不兼容的 API 变更
- MINOR: 向后兼容的功能新增
- PATCH: 向后兼容的问题修复

示例:
- v1.0.0     - 正式版本
- v1.0.0rc1  - Release Candidate
- v1.0.0a1   - Alpha
- v1.0.0b1   - Beta
```

---

## 相关文档

- [开发者入门指南](./developers_guide.md)
- [代码规范](./code_standards.md)
- [本地测试指南](./local_testing.md)
