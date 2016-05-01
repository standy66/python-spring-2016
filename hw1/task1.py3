#! /usr/bin/env python3

n = eval(input())
fib = [0, 1]
for i in range(2, n + 1):
    fib.append(fib[-1] + fib[-2])
print(fib[n])
