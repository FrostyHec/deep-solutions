# Parameter Search Design Document

## Overview

The `parameter_search` module provides a framework-agnostic parameter space exploration library with a PyTorch DataLoader optimization wrapper. It helps developers find optimal configurations (e.g., `batch_size`, `num_workers`) through exhaustive search with built-in metrics collection and analysis.

## Architecture

### Three-Layer Design

```
┌─────────────────────────────────────────────────────┐
│  Layer 3: PyTorch Wrapper (pytorch/)                │  ← Framework-specific
│  DataLoaderParamSelector                            │
├─────────────────────────────────────────────────────┤
│  Layer 2: Epochs & Analyzers                        │  ← Reusable components
│  timed_epoch, simple_epoch                          │
│  BestParamAnalyzer, ChartAnalyzer                   │
├─────────────────────────────────────────────────────┤
│  Layer 1: Core Engine (core/) + Utils (utils/)      │  ← Framework-agnostic
│  ParamSearcher, SearchResult                        │
│  Timer, MetricsCollector, MetricsRecord             │
└─────────────────────────────────────────────────────┘
```

### Module Structure

```
src/deep_solutions/parameter_search/
├── __init__.py              # Top-level API: ParamSearcher, SearchResult, Timer
├── core/
│   ├── __init__.py
│   └── searcher.py          # ParamSearcher (itertools.product), SearchResult
├── utils/
│   ├── __init__.py
│   ├── timer.py             # Timer (start/stop/laps/stats)
│   ├── metrics.py           # MetricsCollector, MetricsRecord
│   └── decorators.py        # @public_api decorator
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

### Design Patterns

| Pattern | Where | Purpose |
|---------|-------|---------|
| **Strategy** | `init_func`, `epoch_func` in ParamSearcher | Swap initialization and evaluation logic at runtime |
| **Template Method** | BaseAnalyzer.analyze() | Define analyzer interface, subclasses implement specifics |
| **Factory** | `timed_epoch()`, `simple_epoch()` | Create configured epoch functions |
| **Decorator** | `@public_api` | Mark public API entries for discoverability |

---

## Quick Start

### 1. Version Check

```python
import deep_solutions
print(deep_solutions.get_library_version())
```

### 2. DataLoader Parameter Optimization (Easiest)

```python
from torch.utils.data import TensorDataset
import torch
from deep_solutions.parameter_search.pytorch import DataLoaderParamSelector

# Create your dataset
dataset = TensorDataset(torch.randn(10000, 784), torch.randint(0, 10, (10000,)))

# Find optimal parameters
selector = DataLoaderParamSelector(
    dataset=dataset,
    search_space={
        "batch_size": [32, 64, 128, 256],
        "num_workers": [0, 2, 4, 8],
    },
    repeats=3,              # Average over 3 runs
    batches_per_run=50,     # Process 50 batches per run
    chart_path="speed.png", # Save visualization
)
result = selector.run()

print(f"Best config: {result['best_config']}")
print(f"Best throughput: {result['best_throughput']:.1f} samples/s")
```

### 3. Custom Parameter Search (Advanced)

```python
from deep_solutions.parameter_search import ParamSearcher
from deep_solutions.parameter_search.epochs import timed_epoch
from deep_solutions.parameter_search.analyzers import BestParamAnalyzer, ChartAnalyzer

# Define how to initialize resources for each config
def init_func(config):
    model = create_model(lr=config["lr"], hidden=config["hidden_size"])
    return model

# Define what to measure each epoch
def run_func(config, model):
    # Process data and return sample count
    return train_one_batch(model)

# Create epoch function with timing
epoch_func = timed_epoch(run_func, repeats=5)

# Search
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

# Analyze
analyzer = BestParamAnalyzer("throughput", maximize=True)
best = analyzer.analyze(result)
print(f"Best: {best['best_config']} -> {best['best_value']:.1f}")

# Visualize
chart = ChartAnalyzer(
    metric_name="throughput",
    x_param="lr",
    group_param="hidden_size",
    save_path="results.png",
)
chart.analyze(result)
```

### 4. Custom Epoch Function

```python
from deep_solutions.parameter_search.epochs import simple_epoch

def my_eval(config, init_result):
    """Fully custom metrics computation."""
    loss = evaluate_model(init_result, config)
    return {"loss": loss, "accuracy": 1.0 - loss}

epoch_func = simple_epoch(my_eval)
```

### 5. Custom Analyzer

```python
from deep_solutions.parameter_search.analyzers import BaseAnalyzer
from deep_solutions.parameter_search.core import SearchResult

class TopKAnalyzer(BaseAnalyzer):
    """Return top-K configurations."""
    
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

## API Reference

### Core API (`parameter_search`)

| Class/Function | Description |
|----------------|-------------|
| `ParamSearcher(init_func, epoch_func, num_epochs, cleanup_func)` | Generic parameter searcher |
| `SearchResult` | Container for search results with `get_best()`, `records`, `to_list()` |
| `Timer` | Precision timer with lap tracking and statistics |

### Epochs (`parameter_search.epochs`)

| Function | Description |
|----------|-------------|
| `timed_epoch(run_func, repeats)` | Create throughput-measuring epoch |
| `simple_epoch(eval_func)` | Pass-through epoch for custom metrics |

### Analyzers (`parameter_search.analyzers`)

| Class | Description |
|-------|-------------|
| `BaseAnalyzer` | Abstract base for custom analyzers |
| `BestParamAnalyzer(metric_name, maximize)` | Find optimal config |
| `ChartAnalyzer(metric_name, x_param, group_param, ...)` | Generate charts |

### PyTorch (`parameter_search.pytorch`)

| Class | Description |
|-------|-------------|
| `DataLoaderParamSelector(dataset, search_space, ...)` | One-call DataLoader optimization |

---

## Data Formats

### Search Space

```python
search_space = {
    "param_name": [value1, value2, ...],  # List of values to try
}
```

### Metrics Output

Each epoch function returns:
```python
{"metric_name": float_value, ...}
```

### SearchResult Records

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

## Extension Guide

1. **Custom Epochs**: Write a function `(config, init_result) -> Dict[str, float]`
2. **Custom Analyzers**: Subclass `BaseAnalyzer` and implement `analyze()`
3. **Custom Init/Cleanup**: Provide callables to `ParamSearcher`
4. **New Frameworks**: Create a wrapper like `DataLoaderParamSelector` using `ParamSearcher`

---

## Dependencies

| Dependency | Required | Purpose |
|------------|----------|---------|
| numpy | Yes (core) | Already in deep-solutions |
| matplotlib | Optional (`[viz]`) | Chart generation |
| torch | Optional (`[pytorch]`) | DataLoader optimization |

Install optional dependencies:
```bash
pip install deep-solutions[viz]       # For chart visualization
pip install deep-solutions[pytorch]   # For DataLoader optimization
```

---

## Related Documentation

- [Project Structure](../../devs/en-US_project_structure.md)
- [Developer Guide](../../devs/en-US_developers_guide.md)
- [Code Standards](../../devs/en-US_code_standards.md)
