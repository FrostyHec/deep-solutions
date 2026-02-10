# 参数搜索设计文档

## 概述

`parameter_search` 模块提供了一个框架无关的参数空间探索库，并附带 PyTorch DataLoader 优化封装。帮助开发者通过穷举搜索找到最优配置（如 `batch_size`、`num_workers`），内置指标收集和分析功能。

## 架构

### 三层设计

```
┌─────────────────────────────────────────────────────┐
│  第三层: PyTorch 封装 (pytorch/)                     │  ← 框架相关
│  DataLoaderParamSelector                            │
├─────────────────────────────────────────────────────┤
│  第二层: Epoch 实现 & 分析器                          │  ← 可复用组件
│  timed_epoch, simple_epoch                          │
│  BestParamAnalyzer, ChartAnalyzer                   │
├─────────────────────────────────────────────────────┤
│  第一层: 核心引擎 (core/) + 工具 (utils/)             │  ← 框架无关
│  ParamSearcher, SearchResult                        │
│  Timer, MetricsCollector, MetricsRecord             │
└─────────────────────────────────────────────────────┘
```

### 模块结构

```
src/deep_solutions/parameter_search/
├── __init__.py              # 顶层 API: ParamSearcher, SearchResult, Timer
├── core/
│   ├── __init__.py
│   └── searcher.py          # ParamSearcher (itertools.product), SearchResult
├── utils/
│   ├── __init__.py
│   ├── timer.py             # Timer (start/stop/laps/stats)
│   ├── metrics.py           # MetricsCollector, MetricsRecord
│   └── decorators.py        # @public_api 装饰器
├── epochs/
│   ├── __init__.py
│   └── basic.py             # timed_epoch(), simple_epoch()
├── analyzers/
│   ├── __init__.py
│   ├── base.py              # BaseAnalyzer (ABC)
│   ├── best_param.py        # BestParamAnalyzer
│   └── chart.py             # ChartAnalyzer (matplotlib)
└── pytorch/
    ├── __init__.py
    └── dataloader.py         # DataLoaderParamSelector
```

### 设计模式

| 模式 | 应用位置 | 目的 |
|------|---------|------|
| **策略模式** | ParamSearcher 中的 `init_func`, `epoch_func` | 运行时切换初始化和评估逻辑 |
| **模板方法** | BaseAnalyzer.analyze() | 定义分析器接口，子类实现具体逻辑 |
| **工厂方法** | `timed_epoch()`, `simple_epoch()` | 创建配置好的 epoch 函数 |
| **装饰器** | `@public_api` | 标记公开 API 入口 |

---

## 快速开始

### 1. 版本检查

```python
import deep_solutions
print(deep_solutions.get_library_version())
```

### 2. DataLoader 参数优化（最简单）

```python
from torch.utils.data import TensorDataset
import torch
from deep_solutions.tools.parameter_search.pytorch import DataLoaderParamSelector

# 创建数据集
dataset = TensorDataset(torch.randn(10000, 784), torch.randint(0, 10, (10000,)))

# 查找最优参数
selector = DataLoaderParamSelector(
    dataset=dataset,
    search_space={
        "batch_size": [32, 64, 128, 256],
        "num_workers": [0, 2, 4, 8],
    },
    repeats=3,              # 3 次取平均
    batches_per_run=50,     # 每次处理 50 个 batch
    chart_path="speed.png", # 保存可视化图表
)
result = selector.run()

print(f"最优配置: {result['best_config']}")
print(f"最优吞吐量: {result['best_throughput']:.1f} samples/s")
```

### 3. 自定义参数搜索（高级用法）

```python
from deep_solutions.tools.parameter_search import ParamSearcher
from deep_solutions.tools.parameter_search.epochs import timed_epoch
from deep_solutions.tools.parameter_search.analyzers import BestParamAnalyzer, ChartAnalyzer

# 定义每个配置的初始化方式
def init_func(config):
    model = create_model(lr=config["lr"], hidden=config["hidden_size"])
    return model

# 定义每个 epoch 要测量什么
def run_func(config, model):
    # 处理数据并返回样本数量
    return train_one_batch(model)

# 使用计时功能创建 epoch 函数
epoch_func = timed_epoch(run_func, repeats=5)

# 执行搜索
searcher = ParamSearcher(
    init_func=init_func,
    epoch_func=epoch_func,
    num_epochs=3,
)
result = searcher.search(
    search_space={
        "lr": [0.001, 0.01, 0.1],
        "hidden_size": [64, 128, 256],
    },
    fixed_config={"dropout": 0.1},
)

# 分析结果
analyzer = BestParamAnalyzer("throughput", maximize=True)
best = analyzer.analyze(result)
print(f"最优: {best['best_config']} -> {best['best_value']:.1f}")

# 可视化
chart = ChartAnalyzer(
    metric_name="throughput",
    x_param="lr",
    group_param="hidden_size",
    save_path="results.png",
)
chart.analyze(result)
```

### 4. 自定义 Epoch 函数

```python
from deep_solutions.tools.parameter_search.epochs import simple_epoch

def my_eval(config, init_result):
    """完全自定义的指标计算。"""
    loss = evaluate_model(init_result, config)
    return {"loss": loss, "accuracy": 1.0 - loss}

epoch_func = simple_epoch(my_eval)
```

### 5. 自定义分析器

```python
from deep_solutions.tools.parameter_search.analyzers import BaseAnalyzer
from deep_solutions.tools.parameter_search.core import SearchResult

class TopKAnalyzer(BaseAnalyzer):
    """返回 Top-K 配置。"""
    
    def __init__(self, metric_name, k=3):
        self._metric = metric_name
        self._k = k
    
    def analyze(self, result: SearchResult):
        records = sorted(
            result.records,
            key=lambda r: r.metrics.get(self._metric, 0),
            reverse=True,
        )
        return {
            "top_k": [
                {"config": r.config, "value": r.metrics[self._metric]}
                for r in records[:self._k]
            ]
        }
```

---

## API 参考

### 核心 API (`parameter_search`)

| 类/函数 | 描述 |
|---------|------|
| `ParamSearcher(init_func, epoch_func, num_epochs, cleanup_func)` | 通用参数搜索器 |
| `SearchResult` | 搜索结果容器，提供 `get_best()`、`records`、`to_list()` |
| `Timer` | 精确计时器，支持多次记录和统计 |

### Epoch 实现 (`parameter_search.epochs`)

| 函数 | 描述 |
|------|------|
| `timed_epoch(run_func, repeats)` | 创建吞吐量测量 epoch |
| `simple_epoch(eval_func)` | 透传 epoch，用于自定义指标 |

### 分析器 (`parameter_search.analyzers`)

| 类 | 描述 |
|----|------|
| `BaseAnalyzer` | 自定义分析器的抽象基类 |
| `BestParamAnalyzer(metric_name, maximize)` | 查找最优配置 |
| `ChartAnalyzer(metric_name, x_param, group_param, ...)` | 生成图表 |

### PyTorch (`parameter_search.pytorch`)

| 类 | 描述 |
|----|------|
| `DataLoaderParamSelector(dataset, search_space, ...)` | 一键 DataLoader 优化 |

---

## 数据格式

### 搜索空间

```python
search_space = {
    "param_name": [value1, value2, ...],  # 要尝试的值列表
}
```

### 指标输出

每个 epoch 函数返回：
```python
{"metric_name": float_value, ...}
```

### SearchResult 记录

```python
[
    {
        "config": {"batch_size": 32, "num_workers": 4},
        "metrics": {"throughput": 5000.0, "mean_time": 0.02},
        "timestamp": "2026-02-10T10:00:00"
    },
    ...
]
```

---

## 扩展指南

1. **自定义 Epoch**: 编写函数 `(config, init_result) -> Dict[str, float]`
2. **自定义分析器**: 继承 `BaseAnalyzer` 并实现 `analyze()`
3. **自定义初始化/清理**: 向 `ParamSearcher` 提供可调用对象
4. **新框架支持**: 参照 `DataLoaderParamSelector` 使用 `ParamSearcher` 创建封装

---

## 依赖

| 依赖 | 是否必需 | 用途 |
|------|---------|------|
| numpy | 是（核心） | 已包含在 deep-solutions |
| matplotlib | 可选（`[viz]`） | 图表生成 |
| torch | 可选（`[pytorch]`） | DataLoader 优化 |

安装可选依赖：
```bash
pip install deep-solutions[viz]       # 图表可视化
pip install deep-solutions[pytorch]   # DataLoader 优化
```

---

## 相关文档

- [项目结构](../../devs/zh-CN_project_structure.md)
- [开发者指南](../../devs/zh-CN_developers_guide.md)
- [代码规范](../../devs/zh-CN_code_standards.md)
