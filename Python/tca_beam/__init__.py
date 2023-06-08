try:
    import importlib.metadata as importlib_metadata
    __version__ = importlib_metadata.version("tca-beam")
except ModuleNotFoundError:
    import importlib_metadata

