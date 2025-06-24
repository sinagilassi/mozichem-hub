# import libs
import types
from typing import Dict, Callable, Any, Set
# local


class RegistryMixin:
    """
    Used to introduce new functions to the Mozichem Hub.
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the Registry instance.
        """
        # A dictionary to hold registered methods
        self._methods = {}

    @property
    def methods(self) -> Dict[str, Dict[str, Callable[..., Any | str | Set]]]:
        """
        Get the registered methods.

        Returns
        -------
        dict
            A dictionary of registered methods.
        """
        return self._methods

    def tool(self, name=None, tags=None):
        """
        Decorator to register a custom function.
        """
        def decorator(func):
            method_name = name or func.__name__
            bound_method = types.MethodType(func, self)
            setattr(self, method_name, bound_method)

            # Add the method to the registry
            self._methods[method_name] = {
                'fn': bound_method,
                'name': method_name,
                'description': func.__doc__ or '',
                'tags': set(tags or [])
            }

            # return
            return bound_method
        return decorator

    def tool_call(self, name, *args, **kwargs):
        """
        Call a registered method by its name with given arguments.
        """
        if name in self._methods:
            return self._methods[name](*args, **kwargs)
        raise AttributeError(f"Method '{name}' not registered.")
