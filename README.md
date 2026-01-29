# deep-solutions

A library that provides useful tools and standard solutions for deep learning tasks.

[![PyPI version](https://badge.fury.io/py/deep-solutions.svg)](https://badge.fury.io/py/deep-solutions)
[![Python Version](https://img.shields.io/pypi/pyversions/deep-solutions)](https://pypi.org/project/deep-solutions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

- [Developer Guide](docs/developers.md) - How to contribute to this project
- [PyPI Publishing Guide](docs/pypi_publishing.md) - How to publish to PyPI
- [API Exposure Guide](.nonpublic/prompts/dev/v0.0.1/repo_init/A002_API暴露方案.md) - Best practices for API design

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
# Format code
black src/ tests/
isort src/ tests/

# Check code quality
flake8 src/ tests/
mypy src/
```

## 📝 Features

- **Core Functionality**: Essential deep learning utilities
- **Easy to Use**: Simple and intuitive API
- **Well Tested**: Comprehensive test coverage
- **Type Hints**: Full type annotation support
- **Extensible**: Easy to extend with new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please see our [Developer Guide](docs/developers.md) for details on how to contribute.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

- **Author**: ZDHuang
- **GitHub**: [@FrostyHec](https://github.com/FrostyHec)
- **Repository**: [deep-solutions](https://github.com/FrostyHec/deep-solutions)

## 🔗 Links

- [PyPI Package](https://pypi.org/project/deep-solutions/)
- [GitHub Repository](https://github.com/FrostyHec/deep-solutions)
- [Issue Tracker](https://github.com/FrostyHec/deep-solutions/issues)

---

**Note**: This is version 0.1.0 - the API may change in future releases.
