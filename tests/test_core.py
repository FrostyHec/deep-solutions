"""
Tests for core module.
"""

from deep_solutions import DeepSolution, hello_world


def test_hello_world():
    """Test hello_world function."""
    result = hello_world()
    assert result == "Hello from deep-solutions!"
    assert isinstance(result, str)


def test_deep_solution_init():
    """Test DeepSolution initialization."""
    solution = DeepSolution("test")
    assert solution.name == "test"

    default_solution = DeepSolution()
    assert default_solution.name == "default"


def test_deep_solution_process():
    """Test DeepSolution process method."""
    solution = DeepSolution("my_solution")
    result = solution.process("data")
    assert result == "Processing data with my_solution"
