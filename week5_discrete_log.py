#!/usr/bin/python3
# -*- coding: utf-8 -*-
# python_version: 3.4.0
__author__ = "Ryan Hu"
__date__ = "2015-2-16"

"""
Given prime p. Let g and h be integers in [0, p-1] given h = g ** x (mod p) where 1 <= x <= 2 ** 40. Our goal is to find
x. More precisely, the input to this program is P, G, H and the output is x. The trivial algorithm for this program is
to try all 2 ** 40 possible values of x until the correct one is found, which runs in time 2 ** 40. In this project, we
will implement an algorithm that runs in time roughly 2 ** 20 using a meet in the middle attack.
gmpy2 package is required to perform multiple-precision integer arithmetic
"""

from gmpy2 import mpz
from gmpy2 import divm
from gmpy2 import powmod
import doctest
import time

# Global variable for unit test, use gmpy2 mpz type that support multiple-precision integers arithmetic
P = mpz(13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171)
G = mpz(11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568)
H = mpz(3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333)


def discrete_log(p, g, h, max_x=2 ** 40):
    """
    (mpz, mpz, mpz) -> mpz

    Given prime p and integer g, h in [0, p-1] which fit the equation that h = g ** x (mod p) where 1 <= x <= 2 ** 40.
    Return the discrete log, i.e. x
    Here this program use a trick to avoid brute force computation of all max_x possibilities. Instead the time consumed
    is O(max_x ** 0.5). Let b equals max_x ** 0.5 and x = x0 * b + x1 where x0, x1 are in the range [0, b-1]. Then
    h = g ** x (mod p) = g ** (x0 * b + x1) (mod p) = g ** (x0 * b) * g ** x1 (mod p). By moving the g ** x1 to left,
    we obtain h / g ** x1 = g ** (x0 * b) (mod p). For every possible x1 in [0, b-1], we hash the left as key and x1 as
    value to a hash table. Then for every possible x0, we calculate if the right is in this hash table. If so, we get
    the right pair of x0 and x1 as x can be calculated.

    >>> discrete_log(mpz(1073676287), mpz(1010343267), mpz(857348958))
    1026831

    :param p: a multi-precision prime
    :param g: a multi-precision integer
    :param h: a multi-precision integer
    :param max_x: the max possible number of x
    :return: the discrete log x
    """
    b = int(max_x ** 0.5)
    hash_table = {}
    for x1 in range(b):
        temp = divm(h, powmod(g, x1, p), p)
        hash_table[temp] = x1
    for x0 in range(b):
        temp = powmod(g, x0 * b, p)
        if temp in hash_table:
            x1 = hash_table[temp]
            break
    x = x0 * b + x1
    return x


if __name__ == "__main__":
    doctest.testmod()
    start_time = time.time()
    print("the outcome is:", discrete_log(P, G, H))
    elapsed_time = time.time() - start_time
    print("The program ran for %s seconds" % elapsed_time)