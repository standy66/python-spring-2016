#! /usr/bin/env python3
import sys

d = dict()
for line in sys.stdin:
    for c in line:
        char = c.lower()
        if char.isalpha():
            if (char in d):
                d[char] += 1
            else:
                d[char] = 1
res = sorted(d.items(), key=lambda x: (-x[1], x[0]))
for (letter, count) in res:
    print(letter + ": " + str(count))
