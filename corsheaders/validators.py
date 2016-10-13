def return_type(*require_type):
    def check_type(func):
        def decorator_wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)
            return_value_type = type(return_value)
            if not return_value_type in require_type:
                raise TypeError("%s type should be one in %s " % (func.__name__, require_type))
            return return_value
        return decorator_wrapper
    return check_type