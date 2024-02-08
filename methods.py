from method_controller import MethodController


#def apply_decorators(name):
#    return MethodController.get_method(name)


@MethodController.get_current_version('example_method')
@MethodController.register_method('example_method')
def example_method(d):
    res = []
    for key, val in d.items():
        res.append(f'{key}: {val}')
    return res


#example_method = apply_decorators('example_method')


@MethodController.get_current_version('example_method2')
@MethodController.register_method('example_method2')
def example_method2(d):
    res = []
    for key, val in d.items():
        res.append(f'{key} -> {val}')
    return res
