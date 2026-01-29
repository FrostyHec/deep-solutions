"""
deep-solutions: A Python package for deep learning solutions.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version

from .core import DeepSolution, hello_world
from .utils import format_output


def _get_package_version() -> str:
    """获取包版本号，优先从已安装的包元数据读取。"""
    try:
        return get_version(__name__)
    except PackageNotFoundError:
        # 未安装时（仅克隆源码），从 setuptools-scm 生成的文件读取
        try:
            from ._version import version as scm_version

            return str(scm_version)
        except ImportError:
            return "0.0.0.dev0"


__version__: str = _get_package_version()

# Public API - explicitly list what should be exposed
__all__ = [
    "__version__",
    "hello_world",
    "DeepSolution",
    "format_output",
]
