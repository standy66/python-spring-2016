#! /usr/bin/env python3

p = float(input())
xs = map(lambda x: float(x), str(input()).split(' '))
ans = (sum(map(lambda x: abs(x) ** p, xs))) ** (1.0 / p)
print(ans)
