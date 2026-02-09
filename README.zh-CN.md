# deep-solutions

一个为深度学习任务提供实用工具和标准解决方案的库。

[![PyPI version](https://badge.fury.io/py/deep-solutions.svg)](https://badge.fury.io/py/deep-solutions)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://pypi.org/project/deep-solutions/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> **Note**: [English README](README.md) is the primary documentation.

## 📦 安装

从 PyPI 安装：

```bash
pip install deep-solutions
```

从源码安装（用于开发）：

```bash
git clone https://github.com/FrostyHec/deep-solutions.git
cd deep-solutions
pip install -e ".[dev]"
```

## 🚀 快速开始

```python
from deep_solutions import hello_world, DeepSolution, format_output

# 简单函数
message = hello_world()
print(message)  # 输出: Hello from deep-solutions!

# 使用 DeepSolution 类
solution = DeepSolution("my_solution")
result = solution.process("data")
print(result)  # 输出: Processing data with my_solution

# 格式化输出
formatted = format_output("result data", prefix="Output")
print(formatted)  # 输出: Output: result data
```

## 📚 文档

| 文档 | 内容 |
|------|------|
| [贡献指南](docs/zh-CN/devs/zh-CN_contributing.md) | **新手开始** — 分步指南 |
| [开发者入门指南](docs/zh-CN/devs/zh-CN_developers_guide.md) | 如何克隆项目、配置环境、开始贡献 |
| [项目结构说明](docs/zh-CN/devs/zh-CN_project_structure.md) | 目录结构、依赖管理、Python 版本要求 |
| [代码规范](docs/zh-CN/devs/zh-CN_code_standards.md) | 提交规范、PR 流程、合并要求 |
| [本地测试指南](docs/zh-CN/devs/zh-CN_local_testing.md) | check.sh、tox、pytest 等使用方法 |
| [CI 工作流](docs/zh-CN/devs/zh-CN_ci_workflow.md) | GitHub Actions CI/CD 说明 |
| [发布指南](docs/zh-CN/devs/zh-CN_publishing.md) | 如何发布到 PyPI |
| [提交规范](docs/zh-CN/devs/zh-CN_commit_conventions.md) | Conventional Commits 规范 |
| [语言规范](docs/zh-CN/devs/zh-CN_language_guidelines.md) | 代码和文档语言要求 |
| [Agent 开发指南](docs/zh-CN/devs/zh-CN_agent.md) | 面向开发者和 AI 代理的技术参考 |

## 🛠️ 开发

### 设置开发环境

我们使用 **Pip-in-Conda** 策略进行依赖管理：
- Conda 只管理 Python 版本和 pip
- 所有包依赖在 `pyproject.toml` 中管理
- 确保开发和生产依赖始终同步

```bash
# 创建 conda 环境（仅 Python + pip）
conda env create -f environment.yml

# 激活环境
conda activate deep-solutions

# 从 pyproject.toml 安装包及所有依赖
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有测试
pytest

# 带覆盖率运行
pytest --cov=deep_solutions --cov-report=html
```

### 代码质量

```bash
# 格式化代码（使用 Ruff）
ruff format src/ tests/

# Lint 检查
ruff check src/ tests/

# 类型检查
mypy src/

# 一次运行所有检查
./scripts/check.sh
```

## 📝 特性

- **核心功能**: 基础深度学习工具
- **易于使用**: 简单直观的 API
- **测试完善**: 全面的测试覆盖
- **类型提示**: 完整的类型注解支持
- **可扩展**: 易于扩展新功能

## 📄 许可证

本项目采用 Apache License 2.0 - 详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎贡献！请查看我们的 [贡献指南](docs/zh-CN/devs/zh-CN_contributing.md) 了解详情。

> **⚠️ 重要**: 开发必须在 **Python 3.8** 环境下进行。详见 [项目结构说明](docs/zh-CN/devs/zh-CN_project_structure.md#python-版本要求)。

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交前运行检查 (`./scripts/check.sh`)
4. 提交更改 (`git commit -m 'feat: add amazing feature'`)
5. 推送到分支 (`git push origin feature/amazing-feature`)
6. 创建 Pull Request

**合并要求**: PR 必须通过所有 CI 检查并获得至少一个 review 批准。

## 📧 联系方式

- **作者**: ZDHuang
- **GitHub**: [@FrostyHec](https://github.com/FrostyHec)
- **仓库**: [deep-solutions](https://github.com/FrostyHec/deep-solutions)

## 🔗 链接

- [PyPI 包](https://pypi.org/project/deep-solutions/)
- [GitHub 仓库](https://github.com/FrostyHec/deep-solutions)
- [Issue 追踪](https://github.com/FrostyHec/deep-solutions/issues)

---

**注意**: 本项目正在积极开发中 - API 可能在未来版本中更改。
