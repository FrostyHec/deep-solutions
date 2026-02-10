"""
Proof of Concept: DataLoader Parameter Selection

This script demonstrates how to use the DataLoaderParamSelector tool to find
optimal batch_size and num_workers parameters for a PyTorch DataLoader.

Expected Output:
    The script will:
    1. Test combinations of batch_size=[16, 32, 64] and num_workers=[0, 2, 4]
    2. Measure throughput (samples/second) for each combination
    3. Print the best configuration found
    4. Generate a chart showing performance across parameters (if matplotlib available)
    
    Example output:
        Testing DataLoader configurations...
        Configuration: {'batch_size': 16, 'num_workers': 0}
        Configuration: {'batch_size': 16, 'num_workers': 2}
        ...
        
        Best Configuration Found:
        batch_size: 64
        num_workers: 4
        throughput: 1523.4 samples/sec
        
        Chart saved to: poc_dataloader_performance.png
"""

import sys
from pathlib import Path

# Add src to path for local development
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    import torch
    from torch.utils.data import TensorDataset
except ImportError:
    print("ERROR: PyTorch is not installed.")
    print("Install with: pip install torch")
    sys.exit(1)

from deep_solutions.tools.parameter_search.pytorch import DataLoaderParamSelector


def create_dummy_dataset(n_samples: int = 1000) -> TensorDataset:
    """
    Create a simple dummy dataset for testing.
    
    Args:
        n_samples: Number of samples to generate.
        
    Returns:
        TensorDataset with random tensors.
    """
    # Create random features and labels
    features = torch.randn(n_samples, 28, 28)  # Simulate image data
    labels = torch.randint(0, 10, (n_samples,))  # 10 classes
    return TensorDataset(features, labels)


def main():
    """Run the DataLoader parameter selection POC."""
    print("=" * 60)
    print("DataLoader Parameter Selection POC")
    print("=" * 60)
    print()
    
    # Create a test dataset
    print("Creating dummy dataset (1000 samples, 28x28 images)...")
    dataset = create_dummy_dataset(n_samples=1000)
    print(f"Dataset created: {len(dataset)} samples")
    print()
    
    # Define search space
    search_space = {
        "batch_size": [16, 32, 64],
        "num_workers": [0, 2, 4],
    }
    
    print("Search Space:")
    for param, values in search_space.items():
        print(f"  {param}: {values}")
    print()
    
    # Configure selector - save chart in poc/param_selector/ directory
    chart_path = str(Path(__file__).parent / "poc_dataloader_performance.png")
    selector = DataLoaderParamSelector(
        dataset=dataset,
        search_space=search_space,
        repeats=2,  # Repeat each config 2 times for averaging
        batches_per_run=20,  # Test with 20 batches per run
        fixed_params={"pin_memory": False},  # Fixed parameter
        chart_path=chart_path,  # Save visualization
    )
    
    # Run the search
    print("Running parameter search...")
    print("(This may take a minute...)")
    print()
    
    results = selector.run()
    
    # Display results
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print()
    
    best_config = results["best_config"]
    best_throughput = results["best_throughput"]
    
    print("Best Configuration Found:")
    for param, value in best_config.items():
        print(f"  {param}: {value}")
    print(f"  throughput: {best_throughput:.1f} samples/sec")
    print()
    
    # Show all tested configurations
    print("All Tested Configurations:")
    search_result = results["search_result"]
    for i, record in enumerate(search_result.records, 1):
        config_str = ", ".join(f"{k}={v}" for k, v in record.config.items())
        throughput = record.metrics.get("throughput", 0)
        print(f"  {i}. {config_str:40s} -> {throughput:8.1f} samples/sec")
    print()
    
    # Chart info
    if "chart" in results:
        chart_info = results["chart"]
        print(f"Performance chart saved to: {chart_info['chart_path']}")
        print("  (Open this file to visualize the results)")
    else:
        print("Note: Install matplotlib to generate performance charts")
        print("  pip install matplotlib")
    print()
    
    print("=" * 60)
    print("POC Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
