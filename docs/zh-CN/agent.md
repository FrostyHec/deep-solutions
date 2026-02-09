# Agent 开发指南

本指南为 AI 代理（及开发者）提供了关于 `deep-solutions` 项目的完整贡献和维护信息。

## 目录
1. [项目工程结构](#项目工程结构)
2. [代码格式与开发规范](#代码格式与开发规范)
3. [本地测试指南](#本地测试指南)
4. [维护与发布指南](#维护与发布指南)

---

## 项目工程结构

### 0. 目录布局

```
deep-solutions/
├── src/deep_solutions/       # 主要包源代码
├── tests/                    # 单元测试
├── docs/                     # 文档（双语：English + zh-CN/）
├── scripts/                  # 开发工具脚本
├── .github/workflows/        # CI/CD 工作流
├── pyproject.toml            # 项目元数据与工具配置
├── environment.yml           # Conda 环境规范
├── tox.ini                   # Tox 多版本测试配置
├── README.md                 # 英文 README
├── README.zh-CN.md           # 中文 README
└── CHANGELOG.md              # 发布历史
```

| 目录 | 用途 |
|-----|------|
| `src/deep_solutions/` | 主要包模块（core、utils 等） |
| `tests/` | pytest 单元测试 |
| `docs/` | 双语文档（英文基础 + `zh-CN/` 翻译） |
| `scripts/` | 开发脚本：`check.sh`、`ci-local.sh`、`check_language.py` |
| `.github/workflows/` | GitHub Actions：CI、发布、测试报告 |
| `pyproject.toml` | 项目配置：依赖、工具设置（ruff、mypy、pytest） |
| `environment.yml` | Conda 环境文件用于开发设置 |
| `tox.ini` | 多 Python 版本测试（3.8-3.12） |

### 0.1. 包分布：`src/deep_solutions/`

```
src/deep_solutions/
├── __init__.py               # 公开 API：hello_world、DeepSolution、format_output
├── core.py                   # 核心类：DeepSolution；函数：hello_world
├── utils.py                  # 工具函数：format_output 及辅助函数
└── _version.py               # setuptools-scm 自动生成（勿编辑）
```

| 模块 | 内容 | 用途 |
|-----|------|------|
| `core.py` | `DeepSolution` 类、`hello_world()` | 深度学习解决方案的核心功能 |
| `utils.py` | `format_output()`、辅助函数 | 格式化和处理的工具函数 |
| `__init__.py` | 公开 API 导出 | 定义 `__all__` 和版本管理 |

---

### 0.2. 开发环境

#### 项目概览

- **语言**: Python 3.8+（最小：3.8，最大测试：3.13）
- **包管理器**: Conda + pip
- **构建系统**: setuptools 配合 setuptools-scm（从 Git 标签自动版本控制）
- **代码质量**: Ruff（格式+检查）、mypy（类型检查）、pytest（测试）
- **CI/CD**: GitHub Actions（CI、发布、测试报告）

#### 依赖信息

**核心依赖**（运行时）：
```
numpy >= 1.17.0
scipy >= 1.5.0
```

**开发依赖**（可选）：
```
pytest >= 7.0.0          # 单元测试
pytest-cov >= 4.0.0      # 覆盖率报告
ruff >= 0.4.0            # 格式化 + 检查
mypy >= 1.0.0            # 类型检查
build >= 0.10.0          # 构建包
twine >= 4.0.0           # 发布到 PyPI
tox >= 4.0.0             # 多版本测试
commitizen >= 3.0.0      # 约定式提交
pre-commit >= 3.0.0      # Git hooks
```

#### 开发环境搭建

**第 1 步：克隆仓库**
```bash
git clone https://github.com/FrostyHec/deep-solutions.git
cd deep-solutions
```

**第 2 步：创建 Conda 环境**
```bash
conda env create -f environment.yml
conda activate deep-solutions
```

**第 3 步：以可编辑模式安装包**
```bash
pip install -e ".[dev]"
```

**第 4 步：验证设置**
```bash
python -c "import deep_solutions; print(f'Version: {deep_solutions.__version__}')"
python -m pytest tests/ -v
```

#### 更新依赖

？，【TODO】合适的操作应该是什么？

---

## 代码格式与开发规范

### 语言政策

- **源代码**: 仅英文（不允许中文）
  - 注释、文档字符串、变量名必须为英文
  - 函数参数和返回值需要类型提示

- **文档**: 双语（英文基础 + 中文翻译）
  - 主文档位于 `docs/*.md`（英文）
  - 翻译版本位于 `docs/zh-CN/*.md`（中文）
  - 详见 `docs/language_guidelines.md`

- **Git 提交**: 仅英文（约定式提交格式）
  - 格式：`type(scope): subject`（例如 `feat(core): add new solver`）
  - 详见 `docs/commit_conventions.md`

### 代码风格与标准

**格式化**（Ruff）：
- 行长：88 字符
- 引号风格：双引号（`"`）
- 缩进：4 个空格

**检查**（Ruff）：
- 无未使用的导入
- PEP 8 兼容
- 启用 Bugbear 检查
- 启用推导式检查

**类型提示**（mypy）：
- 所有公开函数必须提供
- 目标 Python 3.8 兼容性
- 示例：
  ```python
  def process_data(x: List[int]) -> Dict[str, float]:
      """处理整数列表。"""
      return {"mean": sum(x) / len(x)}
  ```

**文档字符串**：
- 使用 Google 风格文档字符串
- 包含 Args、Returns、Raises 部分
- 示例：
  ```python
  def hello_world() -> str:
      """返回问候信息。
      
      返回:
          一个简单的问候字符串。
      """
      return "Hello from deep-solutions!"
  ```

### 何时允许使用中文

✅ **允许**：
- `docs/zh-CN/` 目录中的文档
- 中文文档文件中的注释
- 面向用户的错误消息（可本地化），但需要使用适当的 i18n 框架

❌ **不允许**：
- 源代码（`.py` 文件）
- Git 提交消息
- GitHub Issue/PR 标题
- 代码注释

---

## 本地测试指南

### 一键运行所有检查

```bash
# 使用 bash 脚本
bash scripts/check.sh

# 或手动按顺序运行：
ruff format --check src/ tests/     # 1. 格式检查
ruff check src/ tests/               # 2. 检查代码质量
mypy src/                            # 3. 类型检查
python scripts/check_language.py     # 4. 语言检查
pytest                               # 5. 单元测试
```

### 运行单元测试

```bash
# 运行所有测试并生成覆盖率
pytest

# 运行特定测试文件
pytest tests/test_core.py

# 详细输出
pytest -v

# 运行匹配模式的测试
pytest -k "test_hello" -v
```

### 运行代码格式检查（Ruff）

```bash
# 检查格式
ruff format --check src/ tests/

# 自动修复格式
ruff format src/ tests/

# 检查代码质量
ruff check src/ tests/

# 自动修复检查问题
ruff check --fix src/ tests/
```

### 运行类型检查（mypy）

```bash
# 类型检查
mypy src/

# 详细类型检查输出
mypy src/ --show-error-codes
```

### 运行语言检查

```bash
# 检查源代码中的中文字符
python scripts/check_language.py -v
```

### 多版本测试（tox）

对多个 Python 版本进行测试（3.8-3.12）：

```bash
# 运行所有 Python 版本
tox

# 运行特定 Python 版本
tox -e py38

# 运行并生成覆盖率报告
tox -- --cov=deep_solutions
```

### 覆盖率报告

查看测试覆盖率：
```bash
pytest --cov=deep_solutions --cov-report=html
# 在浏览器中打开 htmlcov/index.html
```

---

## 维护与发布指南

### 版本管理

项目使用 **setuptools-scm** 从 Git 标签自动生成版本。

**版本格式**：`v<major>.<minor>.<patch>`（例如 `v1.0.0`、`v0.2.1`）

### 发布清单

#### 第 1 步：准备发布

1. **确保所有检查通过**：
   ```bash
   bash scripts/check.sh
   ```

2. **更新 CHANGELOG.md**：
   ```bash
   git log v<last-version>..HEAD --oneline
   # 手动在 CHANGELOG.md 中的"未发布"下添加条目
   git add CHANGELOG.md
   git commit -m "docs: update changelog for v<new-version>"
   ```

3. **验证 CI 通过**：检查 main 分支上的 GitHub Actions 状态

#### 第 2 步：创建版本标签

```bash
# 使用 Commitizen（推荐）
cz bump --bump-message "release: v{new_version}"

# 或手动
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

这将触发：
- CI 工作流验证标签
- setuptools-scm 生成版本
- `src/deep_solutions/_version.py` 更新

#### 第 3 步：构建与测试（TestPyPI）

**使用 CI**：推送标签 → GitHub Actions 自动：
1. 运行 `Publish to TestPyPI` 工作流（手动分发可用）
2. 测试安装
3. 创建 GitHub Release 草稿

**手动**（备选，一般避免使用）：
```bash
# 构建分发
python -m build

# 上传到 TestPyPI（先测试！）
twine upload -r testpypi dist/*

# 从 TestPyPI 测试安装
pip install -i https://test.pypi.org/simple/ deep-solutions==<version>
python -c "import deep_solutions; print(deep_solutions.__version__)"
```

#### 第 4 步：发布到 PyPI（生产环境）

**使用 CI**：
1. 前往 GitHub Actions → "Publish to PyPI" 工作流
2. 点击"Run workflow"
3. 确认 CI 通过，然后发布
4. 创建带有资产的 GitHub Release

**手动**（备选，一般避免使用）：
```bash
# 上传到生产 PyPI
twine upload dist/*

# 验证安装
pip install --upgrade deep-solutions
```

### CI 工作流

| 工作流 | 触发条件 | 用途 |
|-------|--------|------|
| `CI` | PR / 推送到 main | 检查、类型检查、测试（PR 仅 3.8，main 完整矩阵） |
| `Test Report` | CI 完成后 | 解析测试结果，在 PR 中发布粘性注释 |
| `Publish to TestPyPI` | 手动分发 | 构建并发布到 TestPyPI 进行测试 |
| `Publish to PyPI` | 手动分发 | 构建并发布到生产 PyPI，创建 Release |

### 常用命令参考

| 命令 | 用途 |
|-----|------|
| `conda activate deep-solutions` | 激活开发环境 |
| `pip install -e ".[dev]"` | 以可编辑模式安装包（含开发依赖） |
| `bash scripts/check.sh` | 运行所有本地检查（格式、检查、类型、语言、测试） |
| `bash scripts/ci-local.sh` | 本地模拟 CI 管道 |
| `pytest` | 运行单元测试 |
| `ruff format src/ tests/` | 自动修复代码格式 |
| `ruff check --fix src/ tests/` | 自动修复检查问题 |
| `mypy src/` | 类型检查 |
| `tox` | 在 Python 3.8-3.12 上测试 |
| `git tag -a v1.0.0 -m "Release v1.0.0"` | 创建发布标签 |
| `python -m build` | 构建分发（wheel + sdist） |
| `twine upload dist/*` | 上传到 PyPI |

---

## 其他资源

- **[开发者指南](developers_guide.md)** - 详细的设置和贡献工作流
- **[代码标准](code_standards.md)** - PR 工作流、合并要求
- **[提交约定](commit_conventions.md)** - 约定式提交格式
- **[项目结构](project_structure.md)** - 依赖管理详情
- **[CI 工作流](ci_workflow.md)** - GitHub Actions 管道详情
- **[本地测试](local_testing.md)** - 综合测试指南
- **[发布指南](publishing.md)** - 发布流程深潜
- **[语言指南](language_guidelines.md)** - 语言政策

