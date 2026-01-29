# PyPI 发布指南

本文档详细说明如何将 `deep-solutions` 包发布到 PyPI（Python Package Index）。

## 目录
- [前置准备](#前置准备)
- [配置 PyPI 账户](#配置-pypi-账户)
- [构建包](#构建包)
- [测试发布（TestPyPI）](#测试发布testpypi)
- [正式发布到 PyPI](#正式发布到-pypi)
- [发布后验证](#发布后验证)
- [版本管理](#版本管理)
- [常见问题](#常见问题)

---

## 前置准备

### 1. 确保项目结构正确

发布前请检查项目结构：

```
deep-solutions/
├── src/
│   └── deep_solutions/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
├── docs/
├── pyproject.toml
├── README.md
├── LICENSE
└── CHANGELOG.md
```

### 2. 安装构建和发布工具

```bash
# 激活开发环境
conda activate deep-solutions

# 安装构建工具
pip install --upgrade build twine
```

### 3. 更新版本信息

在发布前更新以下文件中的版本号：

**pyproject.toml**:
```toml
[project]
version = "0.1.0"  # 更新版本号
```

**src/deep_solutions/__init__.py**:
```python
__version__ = "0.1.0"  # 保持一致
```

**CHANGELOG.md**:
```markdown
## [0.1.0] - 2026-01-28

### Added
- 初始发布
- 核心功能实现
```

---

## 配置 PyPI 账户

### 1. 注册账户

- **PyPI 正式环境**: https://pypi.org/account/register/
- **TestPyPI 测试环境**: https://test.pypi.org/account/register/

> 建议先注册两个账户，这样可以先在 TestPyPI 测试。

### 2. 生成 API Token

#### PyPI 正式环境:
1. 登录 https://pypi.org/
2. 进入 Account settings → API tokens
3. 点击 "Add API token"
4. 填写 Token name (例如: "deep-solutions")
5. Scope 选择 "Entire account" 或指定项目
6. 复制生成的 token（以 `pypi-` 开头）

#### TestPyPI 测试环境:
1. 登录 https://test.pypi.org/
2. 重复上述步骤
3. 复制 token

### 3. 配置本地凭证

创建或编辑 `~/.pypirc` 文件：

```bash
nano ~/.pypirc
```

添加以下内容：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

设置文件权限（仅您可读）：

```bash
chmod 600 ~/.pypirc
```

---

## 构建包

### 1. 清理旧的构建文件

```bash
# 删除旧的 dist 和 build 目录
rm -rf dist/ build/ src/*.egg-info
```

### 2. 运行构建

```bash
# 在项目根目录执行
python -m build
```

构建成功后，`dist/` 目录会包含：

```
dist/
├── deep_solutions-0.1.0-py3-none-any.whl   # Wheel 格式（推荐）
└── deep_solutions-0.1.0.tar.gz             # Source distribution
```

### 3. 检查构建产物

```bash
# 使用 twine 检查包的完整性
twine check dist/*
```

应该显示：

```
Checking dist/deep_solutions-0.1.0-py3-none-any.whl: PASSED
Checking dist/deep_solutions-0.1.0.tar.gz: PASSED
```

---

## 测试发布（TestPyPI）

**强烈建议先在 TestPyPI 测试，确认无误后再发布到正式 PyPI。**

### 1. 上传到 TestPyPI

```bash
twine upload --repository testpypi dist/*
```

或者直接指定 URL：

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### 2. 验证上传

访问 https://test.pypi.org/project/deep-solutions/ 查看包页面。

### 3. 测试安装

在新的虚拟环境中测试安装：

```bash
# 创建测试环境
conda create -n test-install python=3.10
conda activate test-install

# 从 TestPyPI 安装（需要指定额外索引以获取依赖）
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    deep-solutions

# 测试导入
python -c "from deep_solutions import hello_world; print(hello_world())"
```

### 4. 测试通过后清理

```bash
conda deactivate
conda remove -n test-install --all
```

---

## 正式发布到 PyPI

### 1. 最终检查清单

- [ ] 所有测试通过 (`pytest`)
- [ ] 代码质量检查通过 (`black`, `flake8`, `mypy`)
- [ ] README.md 完整且格式正确
- [ ] CHANGELOG.md 已更新
- [ ] 版本号已更新且一致
- [ ] LICENSE 文件存在
- [ ] 已在 TestPyPI 测试成功
- [ ] Git 仓库已提交所有更改

### 2. 创建 Git Tag

```bash
# 确保所有更改已提交
git add .
git commit -m "chore: prepare for release v0.1.0"

# 创建版本标签
git tag -a v0.1.0 -m "Release version 0.1.0"

# 推送到远程（包括标签）
git push origin main --tags
```

### 3. 上传到 PyPI

```bash
# 上传到正式 PyPI
twine upload dist/*
```

如果配置正确，应该显示：

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading deep_solutions-0.1.0-py3-none-any.whl
Uploading deep_solutions-0.1.0.tar.gz
...
View at:
https://pypi.org/project/deep-solutions/0.1.0/
```

---

## 发布后验证

### 1. 查看包页面

访问 https://pypi.org/project/deep-solutions/ 确认：
- 版本号正确
- README 渲染正常
- 元数据完整（作者、许可证、链接等）
- 依赖列表正确

### 2. 测试安装

```bash
# 新建环境测试
conda create -n verify-install python=3.10
conda activate verify-install

# 从 PyPI 安装
pip install deep-solutions

# 验证版本
python -c "import deep_solutions; print(deep_solutions.__version__)"

# 运行示例代码
python -c "from deep_solutions import hello_world; print(hello_world())"

# 清理
conda deactivate
conda remove -n verify-install --all
```

### 3. 更新文档

在 README.md 中更新徽章和安装说明，确保引用正确的版本。

---

## 版本管理

### 语义化版本规范

遵循 [SemVer](https://semver.org/) 规范：`MAJOR.MINOR.PATCH`

- **MAJOR** (主版本): 不兼容的 API 更改
- **MINOR** (次版本): 向后兼容的功能添加
- **PATCH** (补丁): 向后兼容的 Bug 修复

示例：
- `0.1.0` → `0.1.1`: Bug 修复
- `0.1.1` → `0.2.0`: 新增功能
- `0.9.0` → `1.0.0`: 稳定版本发布
- `1.0.0` → `2.0.0`: 破坏性更改

### 发布新版本流程

```bash
# 1. 更新代码和测试
git checkout -b release/v0.2.0

# 2. 更新版本号
# - pyproject.toml: version = "0.2.0"
# - src/deep_solutions/__init__.py: __version__ = "0.2.0"

# 3. 更新 CHANGELOG.md
# 记录新增功能、修复和更改

# 4. 提交更改
git add .
git commit -m "chore: bump version to 0.2.0"
git push origin release/v0.2.0

# 5. 合并到 main
git checkout main
git merge release/v0.2.0

# 6. 创建标签
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags

# 7. 重新构建并发布
rm -rf dist/
python -m build
twine check dist/*
twine upload --repository testpypi dist/*  # 先测试
twine upload dist/*  # 正式发布
```

---

## 常见问题

### Q1: 上传失败："File already exists"

**原因**: PyPI 不允许覆盖已发布的版本。

**解决方案**:
1. 更新版本号（如 `0.1.0` → `0.1.1`）
2. 重新构建和上传

```bash
# 更新版本号后
rm -rf dist/
python -m build
twine upload dist/*
```

### Q2: README 在 PyPI 上渲染不正确

**原因**: Markdown 语法不兼容或文件编码问题。

**解决方案**:
1. 使用 `twine check` 验证
2. 使用标准 Markdown 语法
3. 避免复杂的 HTML 或扩展语法

```bash
twine check dist/*
```

### Q3: 依赖安装失败

**原因**: `pyproject.toml` 中的依赖配置错误。

**解决方案**:
1. 检查依赖版本约束
2. 在测试环境验证
3. 使用 `pip install -e .` 本地测试

### Q4: 如何撤回已发布的版本？

**PyPI 不支持删除或撤回版本**，但可以：
1. 发布新的修复版本
2. 在项目页面添加警告说明
3. 联系 PyPI 管理员处理严重问题

### Q5: 如何发布预发布版本？

使用预发布标识符：

```toml
# pyproject.toml
version = "0.2.0rc1"  # Release Candidate
version = "0.2.0a1"   # Alpha
version = "0.2.0b1"   # Beta
version = "1.0.0.dev1"  # Development
```

用户可以通过 `pip install --pre deep-solutions` 安装预发布版本。

### Q6: 构建时出现 "No module named 'setuptools'"

**解决方案**:

```bash
pip install --upgrade setuptools wheel
```

---

## 自动化发布（可选）

### 使用 GitHub Actions 自动发布

创建 `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

在 GitHub 仓库设置中添加 `PYPI_API_TOKEN` secret。

---

## 总结

完整的发布流程：

1. **开发阶段**: 编写代码、测试、文档
2. **准备发布**: 更新版本号、CHANGELOG
3. **构建包**: `python -m build`
4. **检查**: `twine check dist/*`
5. **测试发布**: `twine upload --repository testpypi dist/*`
6. **测试安装**: 从 TestPyPI 安装测试
7. **正式发布**: `twine upload dist/*`
8. **验证**: 从 PyPI 安装验证
9. **标记版本**: `git tag` 并推送
10. **更新文档**: 更新 README 和文档链接

---

**恭喜！** 您已经成功将包发布到 PyPI。现在任何人都可以通过 `pip install deep-solutions` 安装您的包了！🎉

如果有任何问题，请查看：
- [PyPI 官方文档](https://packaging.python.org/)
- [Twine 文档](https://twine.readthedocs.io/)
- [项目 Issues](https://github.com/FrostyHec/deep-solutions/issues)
