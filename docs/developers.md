# 开发者贡献指南

欢迎为 `deep-solutions` 项目贡献代码！本文档将指导您如何设置开发环境并开始贡献。

## 目录
- [环境准备](#环境准备)
- [安装依赖](#安装依赖)
- [开发工作流](#开发工作流)
- [测试](#测试)
- [代码规范](#代码规范)
- [提交更改](#提交更改)

---

## 环境准备

### 1. 克隆仓库

```bash
git clone https://github.com/FrostyHec/deep-solutions.git
cd deep-solutions
```

### 2. 创建 Conda 环境

我们使用 **Pip-in-Conda** 策略来管理依赖：
- Conda 只管理 Python 版本和 pip
- 所有包依赖由 `pyproject.toml` 统一管理
- 这样确保开发环境和发布包的依赖完全一致

```bash
# 创建 Conda 环境（只包含 Python 3.8+ 和 pip）
conda env create -f environment.yml

# 激活环境
conda activate deep-solutions
```

> **项目需求**：
> - ✅ 最低 Python 版本：**3.8**
> - ✅ 推荐 Python 版本：**3.10+**
> - ✅ 支持版本：3.8, 3.9, 3.10, 3.11, 3.12, 3.13

> **为什么这样做？**
> - ✅ 单一依赖源：所有依赖在 `pyproject.toml` 中管理
> - ✅ 避免冲突：不会出现 conda 和 pip 依赖不一致的问题
> - ✅ 发布可靠：开发环境和最终发布的包使用完全相同的依赖

---

## 安装依赖

### 开发模式安装（推荐）

激活 Conda 环境后，使用 pip 从 `pyproject.toml` 安装所有依赖：

```bash
# 确保已激活 conda 环境
conda activate deep-solutions

# 以可编辑模式安装包及所有开发依赖
pip install -e ".[dev]"
```

这个命令会：
- 以可编辑模式（`-e`）安装 `deep-solutions` 包（代码修改立即生效）
- 安装所有核心依赖（numpy, scipy 等）
- 安装所有开发工具（pytest, ruff, mypy, build, twine）

### 仅安装核心依赖

如果您只需要运行代码而不进行开发：

```bash
pip install -e .
```

### 安装文档依赖

如果需要构建文档：

```bash
pip install -e ".[docs]"
```

### 安装所有依赖

```bash
pip install -e ".[dev,docs]"
```

> **注意**: 所有依赖都在 `pyproject.toml` 中定义，`environment.yml` 只负责创建基础的 Python + pip 环境。

---

## 开发工作流

### 1. 创建功能分支

```bash
git checkout -b feature/your-feature-name
```

### 2. 编写代码

- 将新功能添加到 `src/deep_solutions/` 目录
- 确保代码有适当的文档字符串
- 更新 `src/deep_solutions/__init__.py` 以暴露公共 API（如果需要）

### 3. 编写测试

- 在 `tests/` 目录下添加对应的测试文件
- 测试文件应以 `test_` 开头
- 确保测试覆盖率达标

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_core.py

# 运行测试并查看覆盖率
pytest --cov=deep_solutions --cov-report=html

# 查看详细覆盖率报告
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## 代码规范

我们使用 **Ruff** 作为统一的代码格式化和 Lint 工具（替代 black/isort/flake8），以及 **mypy** 进行类型检查。

### 1. Ruff - 代码格式化

```bash
# 格式化所有代码
ruff format src/ tests/

# 检查格式但不修改
ruff format --check src/ tests/
```

### 2. Ruff - 代码 Lint 检查

```bash
# 检查代码问题
ruff check src/ tests/

# 自动修复可修复的问题
ruff check --fix src/ tests/
```

### 3. MyPy - 类型检查

```bash
# 运行类型检查
mypy src/
```

### 一键运行所有检查 ⭐

我们提供了一个便捷脚本，一次运行所有检查（推荐在提交前使用）：

```bash
# 运行完整检查流程
./scripts/check.sh
```

该脚本会依次执行：
1. **格式化代码** (`ruff format`)
2. **Lint 检查** (`ruff check`)
3. **类型检查** (`mypy`)
4. **运行测试** (`pytest`)

如果任何步骤失败，脚本会停止并报告错误。

---

## 提交更改

### 1. 提交前检查清单

- [ ] 代码已格式化（`ruff format`）
- [ ] 通过 Lint 检查（`ruff check`）
- [ ] 通过类型检查（`mypy`）
- [ ] 添加了必要的测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 更新了 CHANGELOG.md

### 2. 快速检查（推荐）

```bash
# 一键完成所有检查
./scripts/check.sh
```

### 3. 提交代码

```bash
# 添加更改
git add .

# 提交更改（使用有意义的提交信息）
git commit -m "feat: add new feature X"
git commit -m "fix: resolve issue #123"
git commit -m "docs: update developer guide"

# 推送到远程仓库
git push origin feature/your-feature-name
```

### 3. 创建 Pull Request

1. 访问 GitHub 仓库
2. 点击 "New Pull Request"
3. 选择您的功能分支
4. 填写 PR 描述，说明您的更改
5. 等待代码审查

---

## 项目结构

```
deep-solutions/
├── src/
│   └── deep_solutions/          # 主包源码
│       ├── __init__.py          # 公共 API 入口
│       ├── core.py              # 核心功能
│       └── utils.py             # 工具函数
├── tests/                       # 测试文件
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── docs/                        # 文档
│   └── developers.md            # 本文档
├── .nonpublic/                  # 非公开文件
│   └── prompts/                 # 开发提示文档
├── pyproject.toml               # 项目配置和依赖
├── environment.yml              # Conda 环境配置
├── CHANGELOG.md                 # 更改日志
├── README.md                    # 项目说明
└── LICENSE                      # 许可证
```

---

## 常见问题

### Q: 如何更新依赖？

编辑 `pyproject.toml` 中的 `dependencies` 或 `optional-dependencies` 部分，然后运行：

```bash
pip install -e ".[dev]" --upgrade
```

**注意**: 不要在 `environment.yml` 中添加 Python 包依赖，它只用于管理 Python 版本。

### Q: 如何添加新的公共 API？

1. 在相应模块中实现功能（如 `src/deep_solutions/core.py`）
2. 在 `src/deep_solutions/__init__.py` 中导入并添加到 `__all__` 列表
3. 添加文档字符串和类型注解
4. 编写测试

### Q: 测试失败怎么办？

1. 查看错误信息，定位问题
2. 修复代码或测试
3. 重新运行测试确认修复
4. 如果是环境问题，尝试重新创建 conda 环境

### Q: 如何在本地测试安装？

```bash
# 构建包
python -m build

# 在新环境中测试安装
conda create -n test-env python=3.10
conda activate test-env
pip install dist/deep_solutions-*.whl

# 验证版本
python -c "import deep_solutions; print(deep_solutions.__version__)"
```

---

## 发版指南

为了维护项目的质量和可靠性，所有发版都通过 GitHub Actions 工作流进行自动化处理。

### 快速概览

- **项目支持 Python 版本**：3.8+ （包含 3.8, 3.9, 3.10, 3.11, 3.12, 3.13）
- **发版方式**：手动触发 GitHub Actions 工作流
- **版本管理**：通过 Git Tag 和 setuptools-scm 自动管理
- **发布渠道**：TestPyPI（测试）和 PyPI（正式）

### 详细发版流程

请参考 [发布指南](./发布指南.md) 了解：
- 如何生成和配置 API Token
- 如何在 GitHub Actions 中手动触发发布工作流
- 不同版本类型的发布方式（正式版、RC、Alpha/Beta 等）
- 发布后的验证和问题排查

### 版本号规范

本项目遵循 [Semantic Versioning](https://semver.org/) 和 [PEP 440](https://peps.python.org/pep-0440/)：

```
v MAJOR.MINOR.PATCH [pre-release] [build-metadata]

例如：
- v1.0.0          # 正式发布
- v1.0.0rc1       # Release Candidate
- v1.0.0a1        # Alpha
- v1.0.0b1        # Beta
- v1.0.0.post1    # 后续修复
- v1.0.0.dev1     # 开发版本
```

### 版本号管理原理

详见 [版本号管理方案](../.nonpublic/prompts/dev/v0.0.1/A001_repo_init/A004_版本号管理方案.md)：
- Git Tag 是唯一的版本源
- 使用 `setuptools-scm` 自动生成版本号
- 使用 `importlib.metadata` 在运行时读取版本
- 不需要手动维护 `__version__`

---

## 获取帮助

如果您有任何问题或需要帮助：

1. 查看 [GitHub Issues](https://github.com/FrostyHec/deep-solutions/issues)
2. 创建新的 Issue 描述您的问题
3. 参与 Discussions 讨论
4. 参考 [发布指南](./发布指南.md) 了解发版相关问题

感谢您的贡献！ 🎉
