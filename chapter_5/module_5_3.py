#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest


def brute_force_search(pattern, txt):
    '''
    >>> test_data = 'ABACADABRAC'
    >>> pattern = 'ABRA'
    >>> brute_force_search(pattern, test_data)
    6
    >>> pattern2 = 'ACNOTEXIST'
    >>> brute_force_search(pattern2, test_data)
    11
    '''
    assert pattern != '' and txt != '' and pattern is not None and txt is not None

    for i in range(len(txt) - len(pattern)):
        j = 0
        while j < len(pattern):
            if txt[j + i] != pattern[j]:
                break
            j += 1
        if j == len(pattern):
            return i
    return len(txt)


def brute_force_backward_search(pattern, txt):
    '''
    >>> test_data = 'ABACADABRAC'
    >>> pattern = 'ABRA'
    >>> brute_force_backward_search(pattern, test_data)
    6
    >>> pattern2 = 'ACNOTEXIST'
    >>> brute_force_backward_search(pattern2, test_data)
    11
    '''
    assert pattern != '' and txt != '' and pattern is not None and txt is not None

    p_index = t_index = 0
    while p_index < len(pattern) and t_index < len(txt):
        if txt[t_index] == pattern[p_index]:
            p_index += 1
        else:
            t_index -= p_index
            p_index = 0
        t_index += 1

    if p_index == len(pattern):
        return t_index - len(pattern)
    return len(txt)


class KMP(object):

    def __init__(self, pattern):
        self._pat = pattern
        self._dfa = [[0] * 256] * len(pattern)
        self._dfa[chr(pattern[0])][0] = 1

        x, j = 0, 1
        while j < len(pattern):
            for c in range(256):
                self._dfa[c][j] = self._dfa[c][x]
            self._dfa[ord(pattern[j])][j] = j + 1
            x = self._dfa[ord(pattern[j])][x]
            j += 1

if __name__ == '__main__':
    doctest.testmod()
