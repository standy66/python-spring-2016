#! /usr/bin/env python3
import sys
import re

max_width = int(input())

text = []
for line in sys.stdin:
    words = line.split(" ")
    text.extend(words)

cur_width = 0
for word in text:
    if (cur_width == 0):
        print(word, end="")
        if (word[-1] == "\n"):
            cur_width = 0
        else:
            cur_width += len(word)
    else:
        if (cur_width + len(word) + 1 <= max_width):
            print(" " + word, end="")
            if (word[-1] == "\n"):
                cur_width = 0
            else:
                cur_width += 1 + len(word)
        else:
            print("")
            print(word, end="")
            if (word[-1] == "\n"):
                cur_width = 0
            else:
                cur_width = len(word)
