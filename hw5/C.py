import sys
import functools


def takes(*types):
    def decorator(func):
        @functools.wraps(func)
        def new(*args):
            for type_, arg in zip(types, args):
                if not isinstance(arg, type_):
                    raise TypeError("type({}) is not {}".format(arg, type_))
            return func(*args)
        return new
    return decorator

exec(sys.stdin.read())
