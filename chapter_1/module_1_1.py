#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from typing import List, Tuple, Union


def gcd(p: int, q: int) -> int:
    """Calculate greatest common divisor of two numbers.
    Args:
        p (int): integer input
        q (int): integer input
    Returns:
        int: greatest common divider, if p or q is 0, then return non-zero one

    >>> gcd(6, 4)
    2
    >>> gcd(7, 5)
    1
    >>> gcd(10, 5)
    5
    """
    if p == q == 0:
        return 0
    if p == 0 or q == 0:
        return p if q == 0 else q
    return p if q == 0 else gcd(q, p % q)


def is_prime(number: int) -> bool:
    """Determine whether a number is prime.

    Args:
        number (int): input integer

    Returns:
        bool: True if `number` is prime else False

    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(4)
    False
    >>> is_prime(101)
    True
    >>> is_prime(65535)
    False
    """
    if number < 2:
        return False
    i = 2
    while i * i <= number:
        if number % i == 0:
            return False
        i += 1
    return True


def sqrt(number: int) -> float:
    """Calculate the square of given number (Newton's method).

    Args:
        number (int): input integer

    Raises:
        ValueError: raises if number is negative

    Returns:
        float: the square value of `number`

    >>> sqrt(4)
    2.0
    >>> sqrt(9)
    3.0
    >>> sqrt(1)
    1
    >>> sqrt(256)
    16.0
    """
    if number < 0:
        raise ValueError('input number must be positive.')
    err = 1e-15
    t = number
    while abs(t - number / t) > err * t:
        t = float(number / t + t) / 2
    return t


def harmonic(number: int) -> float:
    """Calculate the harmonic number of the given number.

    Args:
        number (int): input integer

    Returns:
        float: harmonic number

    >>> harmonic(2)
    1.5
    >>> harmonic(3)
    1.8333333333333333
    """
    return sum([1 / i for i in range(1, number + 1)])


def binary_search(
        key: int, list_or_tuple: Union[List[int], Tuple[int]]) -> int:
    """Search value `key` in the given `list_or_tuple`.
       If `list_or_tuple` contains `key`, then return the index of `key`,
       else return -1 to indicate that no such `key` in `list_or_tuple`.

    Args:
        key (int): value to search
        list_or_tuple (Union[List[int], Tuple[int]]):
            ascending order list or tuple

    Returns:
        int: index value or -1

    >>> binary_search(3, [1, 2, 3, 4, 5])
    2
    >>> binary_search(1, [1, 2, 3, 4, 5, 6, 7, 9])
    0
    >>> binary_search(9, [1, 2, 3, 4, 5, 6, 7, 9])
    7
    >>> binary_search(999, [1, 2, 3, 4, 5, 6, 7, 9])
    -1
    """

    assert isinstance(key, int)
    assert isinstance(list_or_tuple, (list, tuple))

    low, high = 0, len(list_or_tuple) - 1
    while low <= high:
        mid = int((high + low) / 2)
        if list_or_tuple[mid] == key:
            return mid
        elif list_or_tuple[mid] > key:
            high = mid - 1
        else:
            low = mid + 1
    return -1


def sort3num(a: int, b: int, c: int) -> Tuple[int]:
    """Sort three numbers and return tuple.

    Args:
        a (int): input integer
        b (int): input integer
        c (int): input integer

    Returns:
        Tuple[int]: sorted tuple

    >>> sort3num(3, 2, 1)
    (1, 2, 3)
    """
    if a > b:
        a, b = b, a
    if a > c:
        a, c = c, a
    if b > c:
        b, c = c, b
    return a, b, c


# 1.1.9 practice, code from the book
def int2bin(val: int) -> str:
    """Convert integer number to binary format string.

    Args:
        val (int): input integer

    Returns:
        str: binary format string of input

    >>> int2bin(10)
    '1010'
    >>> int2bin(2000)
    '11111010000'
    """
    result = ""
    while val > 0:
        result = str(val % 2) + result
        val = int(val / 2)
    return result


# 1.1.15 practice, primitive implementation
def histogram(arr: Union[List[int], Tuple[int]], target: int) -> List[int]:
    """

    Args:
        arr (Union[List[int], Tuple[int]]): input array with integer values
        target (int): the lenght of M-sized array

    Returns:
        List[int]: M-sized array

    >>> histogram([1, 2, 3, 3, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10], 4)
    [0, 1, 1, 6]
    >>> histogram([1, 2, 3, 4, 5], 6)
    [0, 1, 1, 1, 1, 1]
    """
    result = [0] * target
    for i in range(target):
        result[i] = arr.count(i)
    return result


# 1.1.16 practice
def exR1(number: int) -> str:
    if number <= 0:
        return ''
    return exR1(number - 3) + str(number) + exR1(number - 2) + str(number)


# 1.1.29 practice
def rank(key: int, list_or_tuple: Union[List[int], Tuple[int]]) -> int:
    """Return the rank of `key` in `list_or_tuple`, `list_or_tuple` might contains
       duplicated values.

    Args:
        key (int): key to be ranked
        list_or_tuple (Union[List[int], Tuple[int]]):
            list or tuple in ascending order

    Returns:
        int: the rank of given `key` in `list_or_tuple`

    >>> rank(3, [1, 2, 3, 3, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10])
    2
    >>> rank(4, [1, 2, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5])
    4
    """

    assert isinstance(key, int)
    assert isinstance(list_or_tuple, (list, tuple))

    low, high = 0, len(list_or_tuple) - 1
    while low <= high:
        mid = int((high + low) / 2)
        if list_or_tuple[mid] == key:
            index = mid
            while list_or_tuple[index] == key:
                index -= 1
            return index + 1
        elif list_or_tuple[mid] > key:
            high = mid - 1
        else:
            low = mid + 1
    return -1


# 1.1.30 practice
def bool_array(length: int) -> List[List[int]]:
    """Create a two-dimension array with boolean value,
       given arr[i][j], if i and j greatest common divisor is 1,
       then arr[i][j] is True, otherwise False

    Args:
        length (int): length of N x N array

    Returns:
        List[List[int]]: a boolean array

    >>> bool_array(2)
    [[False, True], [True, True]]
    """
    return [[gcd(col, row) == 1
             for col in range(length)]
            for row in range(length)]


if __name__ == '__main__':
    doctest.testmod()
