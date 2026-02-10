"""Tests for the dynamic API discovery mechanism."""

from deep_solutions._utils.api_discovery import (
    discover_public_apis,
    get_public_api_names,
)


class TestApiDiscovery:
    """Test the dynamic API discovery functionality."""

    def test_discover_public_apis_from_tools(self):
        """Test that discover_public_apis finds all @public_api decorated items."""
        apis = discover_public_apis("deep_solutions.tools")

        # Should find APIs from helloworld
        assert "hello_world" in apis
        assert "DeepSolution" in apis
        assert "format_output" in apis

        # Should find APIs from parameter_search
        assert "DataLoaderParamSelector" in apis

        # Should be callable/usable
        assert callable(apis["hello_world"])
        result = apis["hello_world"]()
        assert result == "Hello from deep-solutions!"

    def test_get_public_api_names(self):
        """Test that get_public_api_names returns sorted list of API names."""
        names = get_public_api_names("deep_solutions.tools")

        # Should be a list
        assert isinstance(names, list)

        # Should include expected APIs
        assert "hello_world" in names
        assert "DeepSolution" in names
        assert "format_output" in names
        assert "DataLoaderParamSelector" in names

        # Should be sorted
        assert names == sorted(names)

    def test_package_level_imports(self):
        """Test that APIs are available at package level via dynamic discovery."""
        import deep_solutions

        # Should be able to access APIs directly
        assert hasattr(deep_solutions, "hello_world")
        assert hasattr(deep_solutions, "DeepSolution")
        assert hasattr(deep_solutions, "format_output")
        assert hasattr(deep_solutions, "DataLoaderParamSelector")

        # Should be callable
        assert callable(deep_solutions.hello_world)
        result = deep_solutions.hello_world()
        assert result == "Hello from deep-solutions!"

    def test_from_import_works(self):
        """Test that 'from deep_solutions import ...' works with dynamic APIs."""
        # This should not raise ImportError
        from deep_solutions import DataLoaderParamSelector, DeepSolution, hello_world

        assert callable(hello_world)
        assert callable(DeepSolution)
        assert callable(DataLoaderParamSelector)

    def test_all_exports_include_dynamic_apis(self):
        """Test that __all__ includes dynamically discovered APIs."""
        import deep_solutions

        # Should include static exports
        assert "__version__" in deep_solutions.__all__
        assert "get_library_version" in deep_solutions.__all__

        # Should include dynamic APIs
        assert "hello_world" in deep_solutions.__all__
        assert "DeepSolution" in deep_solutions.__all__
        assert "format_output" in deep_solutions.__all__
        assert "DataLoaderParamSelector" in deep_solutions.__all__
