# Tox 本地测试指南

## 什么是 Tox？

Tox 是一个通用的虚拟环境管理和测试命令行工具，用于：
- 在多个 Python 版本中自动化测试
- 确保本地和 CI 环境一致
- 隔离测试环境，避免污染

## 安装

```bash
# 方式 1: 随 dev 依赖一起安装
pip install -e ".[dev]"

# 方式 2: 单独安装
pip install tox tox-gh
```

## 基本用法

### 1. 快速测试（当前 Python 版本）

```bash
# 使用当前激活的 Python 版本运行测试
tox -e py
```

### 2. 测试特定 Python 版本

```bash
# Python 3.8
tox -e py38

# Python 3.9
tox -e py39

# Python 3.10
tox -e py310

# Python 3.11
tox -e py311

# Python 3.12
tox -e py312
```

### 3. 全矩阵测试（所有版本）

```bash
# 运行所有支持的 Python 版本
tox

# 或明确指定
tox -e py38,py39,py310,py311,py312
```

**注意：** 需要在系统中安装相应的 Python 版本。如果某个版本缺失，tox 会跳过（因为配置了 `skip_missing_interpreters = true`）。

### 4. 并行运行（加速）

```bash
# 使用 auto 自动检测 CPU 核心数
tox -p auto

# 或指定并行数量
tox -p 4
```

### 5. 其他测试任务

```bash
# 代码格式和 Lint 检查
tox -e lint

# 类型检查
tox -e type

# 构建包
tox -e build

# 文档构建（需要先创建 docs 目录）
tox -e docs
```

### 6. 传递额外参数给 pytest

```bash
# 只运行特定测试
tox -e py38 -- tests/test_core.py

# 运行特定测试函数
tox -e py38 -- tests/test_core.py::test_hello_world

# 显示详细输出
tox -e py38 -- -v

# 停在第一个失败处
tox -e py38 -- -x

# 组合使用
tox -e py38 -- -vx tests/test_core.py
```

## 常见工作流

### 开发中快速验证

```bash
# 1. 修改代码
# 2. 快速测试当前环境
tox -e py

# 或使用我们的快速检查脚本
bash scripts/check.sh
```

### 提交前完整验证

```bash
# 在本地运行全矩阵测试（如果安装了所有版本）
tox -p auto

# 或至少测试最小和最新版本
tox -e py38,py312
```

### PR 前模拟 CI

```bash
# 模拟 PR CI（仅测试 Python 3.8）
tox -e py38,lint,type

# 或使用我们的 CI 模拟脚本
bash scripts/ci-local.sh
```

### 发布前完整测试

```bash
# 运行所有检查
tox -e lint,type,py38,py39,py310,py311,py312,build
```

## 管理多个 Python 版本

### 使用 pyenv（推荐）

```bash
# 安装 pyenv
curl https://pyenv.run | bash

# 安装多个 Python 版本
pyenv install 3.8.18
pyenv install 3.9.18
pyenv install 3.10.13
pyenv install 3.11.7
pyenv install 3.12.1

# 在项目目录设置多个版本
cd /path/to/deep-solutions
pyenv local 3.8.18 3.9.18 3.10.13 3.11.7 3.12.1

# 验证
pyenv versions

# 现在 tox 可以找到所有版本
tox
```

### 使用 Conda

```bash
# 创建多个环境
conda create -n py38 python=3.8
conda create -n py39 python=3.9
conda create -n py310 python=3.10
conda create -n py311 python=3.11
conda create -n py312 python=3.12

# 在每个环境中运行测试
conda activate py38
tox -e py38

conda activate py39
tox -e py39

# ... 依此类推
```

### 使用 Docker（最简单）

```bash
# 使用不同的 Python 镜像
docker run -v $(pwd):/app -w /app python:3.8 pip install tox && tox -e py38
docker run -v $(pwd):/app -w /app python:3.9 pip install tox && tox -e py39
# ...
```

## Tox 配置说明

我们的 `tox.ini` 配置了以下环境：

| 环境 | 用途 | 命令 |
|------|------|------|
| `py38-py312` | 运行测试 | `tox -e py38` |
| `lint` | 代码格式检查 | `tox -e lint` |
| `type` | 类型检查 | `tox -e type` |
| `build` | 构建包 | `tox -e build` |
| `docs` | 构建文档 | `tox -e docs` |

## CI 集成

### GitHub Actions

我们的 CI 使用 `tox-gh` 插件，自动根据 GitHub Actions 的 Python 版本选择对应的 tox 环境。

在 CI 中：
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.8"
- run: tox
# 自动运行 py38 环境
```

### 差异化测试策略

我们的 CI 采用差异化策略：

**PR / 普通 push:**
- 只测试 Python 3.8（最小支持版本）
- 快速反馈（< 3 分钟）
- 运行命令：`tox -e py38,lint,type`

**main 分支合并后:**
- 全矩阵测试 Python 3.8-3.12
- 完整回归测试
- 运行命令：`tox -e py38,py39,py310,py311,py312`

## 性能优化

### 1. 重用虚拟环境

```bash
# tox 会自动缓存虚拟环境
# 只有依赖变化时才重新创建

# 强制重新创建
tox -r

# 强制重新创建特定环境
tox -r -e py38
```

### 2. 并行执行

```bash
# 自动检测 CPU 核心数
tox -p auto

# 在 4 核 CPU 上大约快 4 倍
```

### 3. 跳过某些步骤

```bash
# 不安装包（如果只是运行 lint）
tox -e lint --skip-pkg-install

# 不安装依赖（如果已经安装）
tox -e py38 --skip-install
```

## 故障排查

### 问题 1: Python 版本未找到

```
ERROR: InterpreterNotFound: python3.10
```

**解决：**
1. 安装缺失的 Python 版本（pyenv/conda）
2. 或跳过该版本（已配置 `skip_missing_interpreters`）

### 问题 2: 依赖冲突

```
ERROR: Could not find a version that satisfies the requirement ...
```

**解决：**
```bash
# 清理缓存并重建
tox -r -e py38
```

### 问题 3: 测试失败但 pytest 直接运行正常

```bash
# 可能是环境隔离问题
# 重新创建环境
tox -r -e py38

# 查看详细日志
tox -e py38 -v
```

### 问题 4: 权限问题

```
PermissionError: [Errno 13] Permission denied: '.tox/...'
```

**解决：**
```bash
# 删除 .tox 目录
rm -rf .tox

# 重新运行
tox
```

## 最佳实践

### 1. 提交前检查清单

```bash
# ✅ 代码格式
tox -e lint

# ✅ 类型检查  
tox -e type

# ✅ 测试通过（至少最小版本）
tox -e py38

# ✅ 构建检查
tox -e build
```

### 2. 开发工作流

```bash
# 开发时：快速迭代
pytest  # 或 tox -e py

# 提交前：完整验证
bash scripts/ci-local.sh

# 发布前：全面测试
tox
```

### 3. 性能建议

- 日常开发用 `pytest` 或 `bash scripts/check.sh`（更快）
- 提交前用 `tox -e py38` 确保兼容性
- 重大变更用 `tox` 全矩阵测试
- PR 前用 `bash scripts/ci-local.sh` 模拟 CI

## 与其他工具对比

| 工具 | 用途 | 何时使用 |
|------|------|---------|
| `pytest` | 直接运行测试 | 日常开发，快速迭代 |
| `bash scripts/check.sh` | 代码质量检查 | 提交前快速验证 |
| `bash scripts/ci-local.sh` | 完整 CI 模拟 | PR 前最终检查 |
| `tox` | 多版本测试 | 确保兼容性，发布前 |
| `tox -p` | 并行多版本测试 | 完整回归测试 |

## 总结

✅ **日常开发**: `pytest` 或 `bash scripts/check.sh`

✅ **提交前**: `tox -e py38` 或 `bash scripts/ci-local.sh`

✅ **发布前**: `tox` 或 `tox -p auto`

✅ **CI 策略**: PR 测试 3.8，main 测试全矩阵

---

更多信息请查看：
- Tox 官方文档: https://tox.wiki/
- tox-gh 文档: https://github.com/tox-dev/tox-gh
- 项目 CI 配置: `.github/workflows/ci.yml`
