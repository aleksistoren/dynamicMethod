import inspect


class MethodController:
    methods = {}
    ignore_current = False

    @staticmethod
    def register_method(name):
        def decorator(func):
            if name not in MethodController.methods:
                MethodController.methods[name] = func, None
            return func

        return decorator

    @staticmethod
    def get_current_version(name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not MethodController.ignore_current and name in MethodController.methods:
                    MethodController.ignore_current = True
                    result = MethodController.methods[name](*args, **kwargs)
                    MethodController.ignore_current = False
                    return result
                else:
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def get_method_code(name):
        method = MethodController.methods.get(name, None)
        if method is None:
            return None
        if method[1]:
            return method[1]
        return inspect.getsource(method[0])


    @staticmethod
    def get_method(name):
        return MethodController.methods.get(name)[0]


