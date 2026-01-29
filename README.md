# deep-solutions

A library that provides useful tools and standard solutions for deep learning tasks.

[![PyPI version](https://badge.fury.io/py/deep-solutions.svg)](https://badge.fury.io/py/deep-solutions)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://pypi.org/project/deep-solutions/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## 📦 Installation

Install from PyPI:

```bash
pip install deep-solutions
```

Install from source (for development):

```bash
git clone https://github.com/FrostyHec/deep-solutions.git
cd deep-solutions
pip install -e ".[dev]"
```

## 🚀 Quick Start

```python
from deep_solutions import hello_world, DeepSolution, format_output

# Simple function
message = hello_world()
print(message)  # Output: Hello from deep-solutions!

# Use DeepSolution class
solution = DeepSolution("my_solution")
result = solution.process("data")
print(result)  # Output: Processing data with my_solution

# Format output
formatted = format_output("result data", prefix="Output")
print(formatted)  # Output: Output: result data
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Developer Guide](docs/developers_guide.md) | How to clone, setup environment, and contribute |
| [Project Structure](docs/project_structure.md) | Directory structure, dependency management, Python version requirements |
| [Code Standards](docs/code_standards.md) | Commit conventions, PR workflow, merge requirements |
| [Local Testing Guide](docs/local_testing.md) | Using check.sh, tox, pytest, etc. |
| [CI Workflow](docs/ci_workflow.md) | GitHub Actions CI/CD documentation |
| [Publishing Guide](docs/publishing.md) | How to publish to PyPI |

> **Note**: Chinese documentation is available in [docs/zh-CN/](docs/zh-CN/)

## 🛠️ Development

### Setup Development Environment

We use the **Pip-in-Conda** strategy for dependency management:
- Conda manages only Python version and pip
- All package dependencies are managed in `pyproject.toml`
- This ensures development and production dependencies are always in sync

```bash
# Create conda environment (only Python + pip)
conda env create -f environment.yml

# Activate environment
conda activate deep-solutions

# Install package with all dependencies from pyproject.toml
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=deep_solutions --cov-report=html
```

### Code Quality

```bash
# Format code (using Ruff)
ruff format src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Run all checks at once
./scripts/check.sh
```

## 📝 Features

- **Core Functionality**: Essential deep learning utilities
- **Easy to Use**: Simple and intuitive API
- **Well Tested**: Comprehensive test coverage
- **Type Hints**: Full type annotation support
- **Extensible**: Easy to extend with new features

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please see our [Developer Guide](docs/developers_guide.md) for details.

> **⚠️ Important**: Development must be done in **Python 3.8** environment. See [Project Structure](docs/project_structure.md#python-version-requirements) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run checks before commit (`./scripts/check.sh`)
4. Commit your changes (`git commit -m 'feat: add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

**Merge Requirements**: PRs must pass all CI checks and receive at least one review approval.

## 📧 Contact

- **Author**: ZDHuang
- **GitHub**: [@FrostyHec](https://github.com/FrostyHec)
- **Repository**: [deep-solutions](https://github.com/FrostyHec/deep-solutions)

## 🔗 Links

- [PyPI Package](https://pypi.org/project/deep-solutions/)
- [GitHub Repository](https://github.com/FrostyHec/deep-solutions)
- [Issue Tracker](https://github.com/FrostyHec/deep-solutions/issues)

---

**Note**: This project is in active development - the API may change in future releases.
