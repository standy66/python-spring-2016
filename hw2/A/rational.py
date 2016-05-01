#! /usr/bin/env python
import sys
import math


class Rational(object):
    def __gcd(self, x, y):
        if (y == 0):
            return x
        else:
            return self.__gcd(y, x % y)

    def __init__(self, num=0, denom=1):
        gcd = self.__gcd(num, denom)
        self.num = num / gcd
        self.denom = denom / gcd

    def __add__(self, other):
        return Rational(self.num * other.denom + self.denom * other.num,
                        self.denom * other.denom)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Rational(self.num * other.num, self.denom * other.denom)

    def __div__(self, other):
        return Rational(self.num * other.denom, self.denom * other.num)

    def __neg__(self):
        return Rational(-self.num, self.denom)

    def __eq__(self, other):
        return self.num * other.denom == other.num * self.denom

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return str(self.num) + "/" + str(self.denom)

exec(sys.stdin.read())
