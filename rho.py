#!/usr/bin/env python

# 
# a basic implementation of the Pollard rho factorization
# Written by Mark VandeWettering <mvandewettering@gmail.com>
#

import sys
import locale
import random

class FactorError(Exception):
    def __init__(self, value):
        self.value = value 
    def __str__(self):
        return repr(self.value)

def miller_rabin_pass(a, n):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1

    a_to_power = pow(a, d, n)
    if a_to_power == 1:
        return True
    for i in range(s-1):
        if a_to_power == n - 1:
            return True
        a_to_power = (a_to_power * a_to_power) % n
    return a_to_power == n - 1

def isprime(n):
    for repeat in range(20):
        a = 0
        while a == 0:
            a = random.randrange(n)
        if not miller_rabin_pass(a, n):
            return False
    return True



def gcd(a, b):
    while b != 0:
        a, b = b, a%b
    return a 

def findfactor(n):
    for c in range(1, 50):
        x = y = random.randint(1, n-1)
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        while True:
            t = gcd(n, abs(x-y))
            if t == 1:
                x = (x * x + c) % n
                y = (y * y + c) % n
                y = (y * y + c) % n
            elif t == n:
                break
            else:
                return t
    raise FactorError("couldn't find a factor.")
	
def factor(n):
    r = []
    while True:
        if isprime(n):
            r.append(n)
            break
        try:
            f = findfactor(n)
            r.append(f)
            n = n // f
        except FactorError as msg:
            r.append(n)
            break
    r.sort()
    return r 

def doit(n):
    flist = factor(n)
    print(f"{n:,} =")
    for f in flist:
        print(f"\t{f:,}")

locale.setlocale(locale.LC_ALL, "")

#
# factor Jevon's number (see https://brainwagon.org/blog/on-factoring-by-jevons-the-principles-of-science/)
#
doit(8616460799)
