#!/usr/bin/env python
# coding=utf-8

"""
example of using py.test
"""


def fib(n):
    """return the nth number in Fibonacci sequence.

    Args:
        n: a non-negative integer

    Return:
        the nth number in Fibonacci sequence, starting with 1, 1, ...

    """
    if n <= 0:
        return -1
    i = j = 1
    for _ in range(n - 1):
        i, j = j, i + j
    return i


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5


def test_fib_bad_input():
    assert fib(0) == -1
    assert fib(-34) == -1
