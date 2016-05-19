import sys
import functools


def inexhaustible(func):
    @functools.wraps(func)
    def new(*args, **kwargs):
        class Temp:
            def __iter__(self):
                return iter(func(*args, **kwargs))
        return Temp()
    return new

exec(sys.stdin.read())
