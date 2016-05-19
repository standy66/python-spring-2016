import sys


def unique(iterable):
    initialzed = False
    prev = None
    for x in iterable:
        if not initialzed:
            initialzed = True
            prev = x
            yield x
        elif prev != x:
            prev = x
            yield x


exec(sys.stdin.read())
