"""
Template/example tool for demonstrating package structure.

This module serves as a placeholder and reference implementation showing
how to structure tools within the deep-solutions package.
"""

from deep_solutions._utils.decorators import public_api


@public_api
def hello_world() -> str:
    """
    A simple example function demonstrating the @public_api decorator.

    This function serves as a template for creating user-facing APIs.

    Returns:
        str: A greeting message.

    Example:
        >>> from deep_solutions.tools.helloworld import hello_world
        >>> hello_world()
        'Hello from deep-solutions!'
    """
    return "Hello from deep-solutions!"


@public_api
class DeepSolution:
    """
    Template class demonstrating tool structure.

    This class serves as a reference for creating well-structured,
    user-facing tools in the deep-solutions package.
    """

    def __init__(self, name: str = "default"):
        """
        Initialize a DeepSolution instance.

        Args:
            name: Name of the solution.
        """
        self.name = name

    def process(self, data):
        """
        Process data using the solution.

        Args:
            data: Input data to process.

        Returns:
            str: Processed data description.

        Example:
            >>> sol = DeepSolution("my_solution")
            >>> sol.process("test_data")
            'Processing test_data with my_solution'
        """
        return f"Processing {data} with {self.name}"
