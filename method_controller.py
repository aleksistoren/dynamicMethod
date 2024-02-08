class MethodController:
    methods = {}

    @staticmethod
    def register_method(name):
        def decorator(func):
            MethodController.methods[name] = func
            return func

        return decorator

    @staticmethod
    def get_method(name):
        return MethodController.methods.get(name, None)
