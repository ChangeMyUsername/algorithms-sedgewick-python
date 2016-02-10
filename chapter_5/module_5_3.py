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

    '''
    >>> kmp = KMP('AACAA')
    >>> kmp.search('AABRAACADABRAACAADABRA')
    12
    '''

    def __init__(self, pattern):
        self._pat = pattern
        arr = [0] * len(pattern)
        self._dfa = [arr[:] for _ in range(256)]
        self._dfa[ord(pattern[0])][0] = 1

        x = 0
        for j in range(1, len(pattern)):
            for c in range(256):
                self._dfa[c][j] = self._dfa[c][x]
            self._dfa[ord(pattern[j])][j] = j + 1
            x = self._dfa[ord(pattern[j])][x]

    def search(self, txt):
        p_index = t_index = 0
        while t_index < len(txt) and p_index < len(self._pat):
            p_index = self._dfa[ord(txt[t_index])][p_index]
            t_index += 1
        if p_index == len(self._pat):
            return t_index - len(self._pat)
        return len(txt)


class BoyerMoore(object):

    '''
    >>> bm = BoyerMoore('NEEDLE')
    >>> bm.search('FINDINAHAYSTACKNEEDLE')
    15
    '''

    def __init__(self, pattern):
        self._pat = pattern
        self._right = [-1] * 256
        for index, char in enumerate(pattern):
            self._right[ord(char)] = index

    def search(self, text):
        txt_len = len(text)
        pat_len = len(self._pat)
        skip = index = 0
        while index <= txt_len - pat_len:
            skip = 0
            for j in range(pat_len - 1, -1, -1):
                if self._pat[j] != text[index + j]:
                    skip = j - self._right[ord(text[index + j])]
                    if skip < 1:
                        skip = 1
                    break
            if skip == 0:
                return index
            index += skip
        return txt_len

if __name__ == '__main__':
    doctest.testmod()
