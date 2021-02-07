__all__ = ['lead', 'contact']

# This works at runtime, but it doesn't work for intellisense
# import os, pkgutil
# __all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))