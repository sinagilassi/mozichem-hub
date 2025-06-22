# import libs
import types
# local


class Registry:
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

    def mozi_function(self, name=None):
        """
        Decorator to register a custom function.
        """
        def decorator(func):
            method_name = name or func.__name__
            bound_method = types.MethodType(func, self)
            setattr(self, method_name, bound_method)
            self._methods[method_name] = bound_method
            return bound_method
        return decorator

    def mozi_call(self, name, *args, **kwargs):
        """
        Call a registered method by its name with given arguments.
        """
        if name in self._methods:
            return self._methods[name](*args, **kwargs)
        raise AttributeError(f"Method '{name}' not registered.")
