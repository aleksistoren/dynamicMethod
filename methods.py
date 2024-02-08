from method_controller import MethodController


@MethodController.register_method('example_method')
def example_method(d):
    res = []
    for key, val in d.items():
        res.append(f'{key}: {val}')
    return res

@MethodController.register_method('example_method2')
def example_method2(d):
    res = []
    for key, val in d.items():
        res.append(f'{key} -> {val}')
    return res