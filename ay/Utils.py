import types


def resolve(x):
    return x() if isinstance(x, types.FunctionType) else x