"""
Tests for utils module.
"""

from deep_solutions import format_output


def test_format_output_default():
    """Test format_output with default prefix."""
    result = format_output("test data")
    assert result == "Result: test data"


def test_format_output_custom_prefix():
    """Test format_output with custom prefix."""
    result = format_output("test data", prefix="Output")
    assert result == "Output: test data"


def test_format_output_various_types():
    """Test format_output with different data types."""
    assert format_output(123) == "Result: 123"
    assert format_output([1, 2, 3]) == "Result: [1, 2, 3]"
    assert format_output({"key": "value"}) == "Result: {'key': 'value'}"
