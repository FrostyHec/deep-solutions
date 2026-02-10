"""Tests for helloworld tool."""

from deep_solutions.tools.helloworld import DeepSolution, format_output, hello_world


def test_hello_world() -> None:
    """Test hello_world function."""
    result = hello_world()
    assert isinstance(result, str)
    assert "Hello" in result
    assert "deep-solutions" in result


def test_deep_solution_init() -> None:
    """Test DeepSolution initialization."""
    sol = DeepSolution("test_solution")
    assert sol.name == "test_solution"

    # Test default name
    sol_default = DeepSolution()
    assert sol_default.name == "default"


def test_deep_solution_process() -> None:
    """Test DeepSolution process method."""
    sol = DeepSolution("my_solver")
    result = sol.process("test_data")
    assert isinstance(result, str)
    assert "test_data" in result
    assert "my_solver" in result


def test_format_output_default() -> None:
    """Test format_output with default prefix."""
    result = format_output("success")
    assert result == "Result: success"


def test_format_output_custom_prefix() -> None:
    """Test format_output with custom prefix."""
    result = format_output(42, prefix="Answer")
    assert result == "Answer: 42"


def test_format_output_various_types() -> None:
    """Test format_output handles various data types."""
    assert format_output(123) == "Result: 123"
    assert format_output([1, 2, 3]) == "Result: [1, 2, 3]"
    assert format_output({"key": "value"}) == "Result: {'key': 'value'}"


def test_public_api_decorator_applied() -> None:
    """Verify @public_api decorator is applied to functions and classes."""
    # Check that docstrings are marked with [PUBLIC API]
    assert "[PUBLIC API]" in (hello_world.__doc__ or "")
    assert "[PUBLIC API]" in (DeepSolution.__doc__ or "")
    assert "[PUBLIC API]" in (format_output.__doc__ or "")
