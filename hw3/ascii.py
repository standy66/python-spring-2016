#!/usr/bin/env python3
import argparse
import sys


def print_picture(picture, file=sys.stdout):
    for i in range(len(picture)):
        for j in range(len(picture[i])):
            print(picture[i][j], end="", file=file)
        print(file=file)


def crop(picture, left=0, right=0, top=0, bottom=0):
    return [[picture[i][j]
            for j in range(left, len(picture[i]) - right)]
            for i in range(top, len(picture) - bottom)]


def expose(picture, value):
    levels = "@%#*+=-:. "
    inv_levels = dict([(k, v) for (v, k) in enumerate(levels)])
    res = [[0 for j in range(len(picture[i]))] for i in range(len(picture))]
    for i in range(len(picture)):
        for j in range(len(picture[i])):
            new_val = min(max(inv_levels[picture[i][j]] + value, 0), 9)
            res[i][j] = levels[new_val]
    return res


def transpose(picture):
    return list(map(list, zip(*picture)))


def rotate_cw(picture):
    return transpose(picture)[::-1]


def rotate(picture, degrees):
    if (degrees % 90 != 0):
        raise ValueError("degrees should be divisible by 90")
    times = (((degrees % 360) + 360) % 360) // 90
    res = picture
    for i in range(times):
        res = rotate_cw(res)
    return res


def rotate_ccw(picture):
    return rotate(picture, -90)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["crop", "expose", "rotate"])
    parser.add_argument("-l", "--left", type=int, default=0)
    parser.add_argument("-r", "--right", type=int, default=0)
    parser.add_argument("-t", "--top", type=int, default=0)
    parser.add_argument("-b", "--bottom", type=int, default=0)
    parser.add_argument("value", default=None, nargs="?", type=int)
    args = parser.parse_args(input().split())
    picture = list(map(lambda x: x.rstrip("\r\n"), sys.stdin.readlines()))

    if (args.action == "crop"):
        if (args.value):
            parser.print_help()
            sys.exit(1)
        picture = crop(picture, left=args.left, right=args.right, top=args.top,
                       bottom=args.bottom)
        print_picture(picture)
    elif (args.action == "expose"):
        if (args.top or args.left or args.right or args.bottom):
            parser.print_help()
            sys.exit(1)
        picture = expose(picture, args.value)
        print_picture(picture)
    elif (args.action == "rotate"):
        if (args.top or args.left or args.right or args.bottom):
            parser.print_help()
            sys.exit(1)
        if (args.value % 90 != 0):
            parser.print_help()
            sys.exit(1)
        picture = rotate(picture, args.value)
        print_picture(picture)

if __name__ == "__main__":
    main()
