# CI/CD 工作流使用指南

## 概述

本项目采用 **双 Runner 安全模型** 来处理 Pull Request 的测试和报告，确保来自 fork 的 PR 也能安全地运行测试并获得反馈。

## 工作流架构

```mermaid
graph TB
  subgraph PR测试 — 快速反馈
    A1[PR 触发]-->A2[Lint + Type Check]
    A2-->A3[Test Python 3.8 only]
    A3-->A4[Build Check]
  end

  subgraph Main分支 — 完整回归
    B1[Push to main]-->B2[Lint + Type Check]
    B2-->B3[Test Python 3.8-3.12 全矩阵]
    B3-->B4[Build Check]
  end

  subgraph 测试报告
    C1[workflow_run 触发]-->C2[下载 artifact]
    C2-->C3[发布 Check Run]
  end
```

## 差异化测试策略

我们采用 **差异化测试策略** 以平衡速度和覆盖度：

| 触发场景 | Python 版本 | 时长 | 目的 |
|---------|------------|------|------|
| **PR / 普通 push** | 仅 3.8 (最小版本) | < 3 分钟 | 快速反馈，验证基本兼容性 |
| **Push to main** | 3.8, 3.9, 3.10, 3.11, 3.12 | ~5-7 分钟 | 完整回归，确保所有版本兼容 |

### 为什么这样设计？

✅ **快速反馈**: PR 开发过程中，只需验证最小版本即可快速迭代

✅ **资源节省**: 减少 80% 的 CI 时间和计算资源消耗

✅ **充分测试**: main 分支合并后仍会进行全矩阵测试，确保质量

✅ **早发现问题**: Python 3.8 兼容性最严格，通过则大概率全部通过

## 工作流文件

### 1. `.github/workflows/ci.yml` - 主测试流程

**触发条件：**
- Pull Request (opened, synchronize, reopened)
- Push to main 分支

**权限：** `contents: read`（只读，安全运行 fork PR 代码）

**任务：**
1. **lint** - 代码格式和 Lint 检查（Ruff）
2. **type-check** - 类型检查（MyPy）
3. **test** - 运行测试
   - **PR**: 仅 Python 3.8
   - **main**: Python 3.8-3.12 全矩阵
   - 生成 JUnit XML 报告
   - 生成覆盖率报告（仅 3.12）
   - 上传为 artifact（保留 1 天）
4. **build** - 构建检查（验证包可以正常构建）

**性能优化：**
- ✅ 依赖缓存（pip cache）
- ✅ 并行测试（matrix 策略）
- ✅ 自动取消旧任务（concurrency）
- ✅ 覆盖率仅在 Python 3.12 上传

**特点：**
- ✅ 可安全运行来自 fork 的代码
- ✅ 不暴露任何 secrets
- ✅ PR 快速反馈（< 3 分钟）
- ✅ main 分支完整测试（~5-7 分钟）

### 2. `.github/workflows/report.yml` - 测试报告发布

**触发条件：** CI workflow 完成后（无论成功或失败）

**权限：**
- `checks: write` - 创建 Check Run
- `pull-requests: write` - 在 PR 中评论
- `actions: read` - 读取 workflow run

**任务：**
- 下载 CI 生成的测试报告
- 使用 `dorny/test-reporter` 发布到 PR
- **PR**: 仅为 Python 3.8 创建 Check Run
- **main**: 为所有版本创建 Check Run

**特点：**
- ✅ 运行在主仓库上下文（受信任代码）
- ✅ 只处理静态数据（junit XML），不执行 PR 代码
- ✅ 即使 artifact 被篡改，也只是解析失败，不会执行恶意代码
- ✅ 动态适应测试策略（PR vs main）

## 安全模型说明

### 为什么不用 `pull_request_target`？

`pull_request_target` 虽然可以给 fork PR 写权限，但存在安全风险：
- ❌ Workflow 在 **主仓库上下文** 运行，拥有写权限
- ❌ 如果 checkout PR 代码并执行，可能导致：
  - Secrets 泄露
  - 恶意代码注入
  - Runner 被攻击

### 双 Runner 模型的优势

**Runner A（测试）：**
- ✅ 执行所有来自 fork 的代码
- ✅ 无写权限，无 secrets
- ✅ 即使被攻破，攻击者也无法窃取机密

**Runner B（报告）：**
- ✅ 运行在主仓库上下文，可使用写权限
- ✅ 只处理静态文件（junit XML）
- ✅ 不执行 PR 代码，只解析数据

## 使用方式

### 开发者视角

1. **创建 PR**：Push 代码到分支并创建 Pull Request

2. **自动触发测试**：
   - CI workflow 自动运行
   - 在 PR 的 "Checks" 标签页可以看到进度

3. **查看测试结果**：
   - CI 完成后，Test Report workflow 自动运行
   - 几分钟后，PR 界面会出现 Check Run 报告
   - 点击 "Details" 可查看详细的测试失败信息

4. **测试失败处理**：
   - 查看 Check Run 的详细信息定位问题
   - 修复后 push 代码，自动重新触发测试

### Fork 贡献者视角

外部贡献者的 PR 会：
- ✅ 自动运行所有测试
- ✅ 获得测试结果反馈（Check Run）
- ✅ 完全安全，无需担心权限问题

## 本地测试

在提交 PR 前，建议先在本地运行：

### 快速检查（推荐日常使用）

```bash
# 运行所有代码质量检查（format, lint, type-check, test）
bash scripts/check.sh
```

### 使用 Tox 进行多版本测试

我们使用 Tox 统一本地和 CI 的测试环境：

```bash
# 安装 tox
pip install -e ".[dev]"

# 测试当前 Python 版本
tox -e py

# 测试特定版本
tox -e py38

# 全矩阵测试（如果安装了所有版本）
tox

# 并行运行（推荐）
tox -p auto

# 只运行 lint 和 type check
tox -e lint,type
```

**详细指南**: 查看 `docs/tox_guide.md` 了解：
- 如何安装多个 Python 版本
- Tox 的高级用法
- 性能优化技巧
- 故障排查

### 完整 CI 模拟

```bash
# 模拟 CI 的所有步骤（包括构建检查）
bash scripts/ci-local.sh
```

这个脚本会：
1. ✅ 检查代码格式（Ruff format）
2. ✅ 运行 Linter（Ruff check）
3. ✅ 类型检查（MyPy）
4. ✅ 运行测试并生成报告
5. ✅ 构建包并验证

### 仅运行测试

```bash
# 仅运行测试并生成报告
pytest --junitxml=pytest-report.xml --cov=deep_solutions --cov-report=xml --cov-report=term-missing
```

## 故障排查

### 问题 1: Test Report workflow 没有运行

**可能原因：**
- CI workflow 还在运行中（需要等待完成）
- CI workflow 被取消（不会触发 report）

**解决方案：**
- 等待 CI 完成
- 确保 CI 至少有一个 job 完成（无论成功或失败）

### 问题 2: Check Run 创建失败

**错误信息：** `HttpError: Resource not accessible by integration`

**原因：** 在 `pull_request` 上下文中，GITHUB_TOKEN 没有写权限

**解决方案：** 已通过双 Runner 模型解决 ✅

### 问题 3: Artifact 下载失败

**可能原因：**
- Artifact 名称不匹配
- Workflow run ID 错误
- Artifact 已过期（默认保留 1 天）

**解决方案：**
- 检查 artifact 名称格式：`pytest-results-{python-version}-{run-id}`
- 确保在 1 天内运行 report workflow

## 维护建议

### 定期检查

1. **GitHub Actions 用量**：
   - 查看 Settings → Billing → Actions usage
   - 关注 artifact 存储用量

2. **更新依赖**：
   ```bash
   # 更新 GitHub Actions
   # 定期检查 actions/checkout, actions/setup-python 等的新版本
   ```

### 优化建议

1. **减少 artifact 大小**：
   - 只上传必要的报告文件
   - 已设置 retention-days: 1

2. **并行优化**：
   - test job 使用 matrix 并行运行 5 个 Python 版本
   - 总运行时间约 2-3 分钟

3. **缓存优化**（可选）：
   ```yaml
   - name: Cache pip packages
     uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
   ```

## 相关资源

- [GitHub Actions 安全最佳实践](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [dorny/test-reporter 文档](https://github.com/dorny/test-reporter)
- [workflow_run 触发器文档](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_run)
