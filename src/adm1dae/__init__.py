__version__ = "0.1.0"
__all__ = ["simulate"]

def simulate(*args, **kwargs):
    from .simulate import simulate as _simulate
    return _simulate(*args, **kwargs)