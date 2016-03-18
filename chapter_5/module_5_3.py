#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest


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
    >>> kmp = KMP('rab')
    >>> kmp.search('abacadabrabracabracadabrabrabracad')
    8
    >>> kmp.count('abacadabrabracabracadabrabrabracad')
    3
    >>> kmp.search_all('abacadabrabracabracadabrabrabracad')
    [8, 23, 26]
    >>> kmp2 = KMP('abracadabra')
    >>> kmp2.search('abacadabrabracabracadabrabrabracad')
    14
    >>> kmp2.count('abacadabrabracabracadabrabrabracad')
    1
    >>> kmp2.search_all('abacadabrabracabracadabrabrabracad')
    [14]
    >>> kmp3 = KMP('bcara')
    >>> kmp3.search('abacadabrabracabracadabrabrabracad')
    34
    >>> kmp3.count('abacadabrabracabracadabrabrabracad')
    0
    >>> kmp3.search_all('abacadabrabracabracadabrabrabracad')
    []
    >>> kmp4 = KMP('rabrabracad')
    >>> kmp4.search('abacadabrabracabracadabrabrabracad')
    23
    >>> kmp5 = KMP('abacad')
    >>> kmp5.search('abacadabrabracabracadabrabrabracad')
    0
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

    # 5.3.8 practice
    def count(self, txt):
        counter = 0
        p_index = t_index = 0
        while t_index < len(txt) and p_index < len(self._pat):
            p_index = self._dfa[ord(txt[t_index])][p_index]
            t_index += 1
            if p_index == len(self._pat):
                counter += 1
                p_index = 0
        return counter

    # 5.3.8 practice
    def search_all(self, txt):
        positions = []
        p_index = t_index = 0
        while t_index < len(txt) and p_index < len(self._pat):
            p_index = self._dfa[ord(txt[t_index])][p_index]
            t_index += 1
            if p_index == len(self._pat):
                positions.append(t_index - len(self._pat))
                p_index = 0
        return positions


class BoyerMoore(object):

    '''
    >>> bm = BoyerMoore('NEEDLE')
    >>> bm.search('FINDINAHAYSTACKNEEDLE')
    15
    >>> bm = BoyerMoore('rab')
    >>> bm.search('abacadabrabracabracadabrabrabracad')
    8
    >>> bm.count('abacadabrabracabracadabrabrabracad')
    3
    >>> bm.search_all('abacadabrabracabracadabrabrabracad')
    [8, 23, 26]
    >>> bm2 = BoyerMoore('abracadabra')
    >>> bm2.search('abacadabrabracabracadabrabrabracad')
    14
    >>> bm2.count('abacadabrabracabracadabrabrabracad')
    1
    >>> bm2.search_all('abacadabrabracabracadabrabrabracad')
    [14]
    >>> bm3 = BoyerMoore('bcara')
    >>> bm3.search('abacadabrabracabracadabrabrabracad')
    34
    >>> bm3.count('abacadabrabracabracadabrabrabracad')
    0
    >>> bm3.search_all('abacadabrabracabracadabrabrabracad')
    []
    >>> bm4 = BoyerMoore('rabrabracad')
    >>> bm4.search('abacadabrabracabracadabrabrabracad')
    23
    >>> bm5 = BoyerMoore('abacad')
    >>> bm5.search('abacadabrabracabracadabrabrabracad')
    0
    '''

    def __init__(self, pattern):
        self._pat = pattern
        self._right = [-1] * 256
        for index, char in enumerate(pattern):
            self._right[ord(char)] = index

    def search(self, txt):
        txt_len = len(txt)
        pat_len = len(self._pat)
        skip = index = 0
        while index <= txt_len - pat_len:
            skip = 0
            for j in range(pat_len - 1, -1, -1):
                if self._pat[j] != txt[index + j]:
                    skip = j - self._right[ord(txt[index + j])]
                    if skip < 1:
                        skip = 1
                    break
            if skip == 0:
                return index
            index += skip
        return txt_len

    # 5.3.9 practice
    def count(self, txt):
        txt_len = len(txt)
        pat_len = len(self._pat)
        skip = index = counter = 0
        while index <= txt_len - pat_len:
            skip = 0
            for j in range(pat_len - 1, -1, -1):
                if self._pat[j] != txt[index + j]:
                    skip = j - self._right[ord(txt[index + j])]
                    if skip < 1:
                        skip = 1
                    break
            if skip == 0:
                counter += 1
                skip = 1
            index += skip
        return counter

    # 5.3.9 practice
    def search_all(self, txt):
        txt_len = len(txt)
        pat_len = len(self._pat)
        skip = index = 0
        positions = []
        while index <= txt_len - pat_len:
            skip = 0
            for j in range(pat_len - 1, -1, -1):
                if self._pat[j] != txt[index + j]:
                    skip = j - self._right[ord(txt[index + j])]
                    if skip < 1:
                        skip = 1
                    break
            if skip == 0:
                positions.append(index)
                skip = 1
            index += skip
        return positions


class RabinKarp(object):

    '''
    >>> rk = RabinKarp('rab')
    >>> rk.search('abacadabrabracabracadabrabrabracad')
    8
    >>> rk.count('abacadabrabracabracadabrabrabracad')
    3
    >>> rk.search_all('abacadabrabracabracadabrabrabracad')
    [8, 23, 26]
    >>> rk2 = RabinKarp('abracadabra')
    >>> rk2.search('abacadabrabracabracadabrabrabracad')
    14
    >>> rk2.count('abacadabrabracabracadabrabrabracad')
    1
    >>> rk2.search_all('abacadabrabracabracadabrabrabracad')
    [14]
    >>> rk3 = RabinKarp('bcara')
    >>> rk3.search('abacadabrabracabracadabrabrabracad')
    34
    >>> rk3.count('abacadabrabracabracadabrabrabracad')
    0
    >>> rk3.search_all('abacadabrabracabracadabrabrabracad')
    []
    >>> rk4 = RabinKarp('rabrabracad')
    >>> rk4.search('abacadabrabracabracadabrabrabracad')
    23
    >>> rk5 = RabinKarp('abacad')
    >>> rk5.search('abacadabrabracabracadabrabrabracad')
    0
    '''

    def __init__(self, pattern):
        self._pat = pattern
        self._pat_len = len(pattern)
        self._q = 997
        self._rm = 1
        for i in range(1, self._pat_len):
            self._rm = (256 * self._rm) % self._q
        self._pat_hash = self._hash(pattern, self._pat_len)

    def check(self, i, txt=None):
        # 5.3.12 practice, implement LasVegas version check method.
        if txt:
            for j in range(self._pat_len):
                if not self._pat[j] != txt[i + j]:
                    return False
        return True

    def _hash(self, txt, length):
        result = 0
        for i in range(length):
            result = (256 * result + ord(txt[i])) % self._q
        return result

    def search(self, txt):
        txt_len = len(txt)
        txt_hash = self._hash(txt, self._pat_len)
        if self._pat_hash == txt_hash and self.check(0):
            return 0

        for i in range(self._pat_len, txt_len):
            txt_hash = (txt_hash + self._q - self._rm * ord(txt[i - self._pat_len])
                        % self._q) % self._q
            txt_hash = (txt_hash * 256 + ord(txt[i])) % self._q
            if self._pat_hash == txt_hash:
                if self.check(i - self._pat_len + 1):
                    return i - self._pat_len + 1
        return txt_len

    # 5.3.10 practice
    def search_all(self, txt):
        txt_len = len(txt)
        txt_hash = self._hash(txt, self._pat_len)
        positions = []
        if self._pat_hash == txt_hash and self.check(0):
            positions.append(0)

        for i in range(self._pat_len, txt_len):
            txt_hash = (txt_hash + self._q - self._rm * ord(txt[i - self._pat_len])
                        % self._q) % self._q
            txt_hash = (txt_hash * 256 + ord(txt[i])) % self._q
            if self._pat_hash == txt_hash:
                if self.check(i - self._pat_len + 1):
                    positions.append(i - self._pat_len + 1)
        return positions

    # 5.3.10 practice
    def count(self, txt):
        txt_len = len(txt)
        txt_hash = self._hash(txt, self._pat_len)
        count = 0
        if self._pat_hash == txt_hash and self.check(0):
            count += 1

        for i in range(self._pat_len, txt_len):
            txt_hash = (txt_hash + self._q - self._rm * ord(txt[i - self._pat_len])
                        % self._q) % self._q
            txt_hash = (txt_hash * 256 + ord(txt[i])) % self._q
            if self._pat_hash == txt_hash:
                if self.check(i - self._pat_len + 1):
                    count += 1
        return count


# 5.3.1 practice, brute force string search algorithm with specific interfaces.
class Brute(object):

    '''
    >>> brute = Brute('rab')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    8
    >>> brute.count('abacadabrabracabracadabrabrabracad')
    3
    >>> [i for i in brute.search_all('abacadabrabracabracadabrabrabracad')]
    [8, 23, 26]
    >>> brute = Brute('abracadabra')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    14
    >>> [i for i in brute.search_all('abacadabrabracabracadabrabrabracad')]
    [14]
    >>> brute.count('abacadabrabracabracadabrabrabracad')
    1
    >>> brute = Brute('bcara')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    34
    >>> brute.count('abacadabrabracabracadabrabrabracad')
    0
    >>> brute.search_all('abacadabrabracabracadabrabrabracad')
    []
    >>> brute = Brute('rabrabracad')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    23
    >>> brute = Brute('abacad')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    0
    '''

    def __init__(self, pattern):
        self._pat = pattern
        self._pat_len = len(pattern)

    def search(self, txt):
        txt_len = len(txt)
        for i in range(txt_len - self._pat_len + 1):
            j = 0
            while j < self._pat_len:
                if txt[j + i] != self._pat[j]:
                    break
                j += 1
            if j == self._pat_len:
                return i
        return txt_len

    # 5.3.7 practice
    def count(self, txt):
        counter = 0
        txt_len = len(txt)
        for i in range(txt_len - self._pat_len + 1):
            j = 0
            while j < self._pat_len:
                if txt[j + i] != self._pat[j]:
                    break
                j += 1
            if j == self._pat_len:
                counter += 1
        return counter

    # 5.3.7 practice
    def search_all(self, txt):
        positions = []
        txt_len = len(txt)
        for i in range(txt_len - self._pat_len + 1):
            j = 0
            while j < self._pat_len:
                if txt[j + i] != self._pat[j]:
                    break
                j += 1
            if j == self._pat_len:
                positions.append(i)
        return positions


# 5.3.4 practice, counting consecutive empty spaces,
# the running would be proportional to O(n)
def empty_space(txt, count):
    '''
    >>> empty_space('   xxxx   ', 3)
    0
    >>> empty_space('xxx   xxxXXXXXX   Xxxx', 3)
    3
    >>> empty_space('xxxx   ', 3)
    4
    >>> empty_space('xxx  ', 3)
    4
    '''

    index, length = 0, len(txt)
    while index < length - count + 1:
        if txt[index] == ' ':
            i = 0
            while i < count:
                if txt[i + index] != ' ':
                    index += i
                    break
                i += 1
            if i == count:
                return index
        index += 1
    return length - 1


# 5.3.5 practice, implement brute force
# algorithm comparing substring from right to left.
class BruteForceRL(object):

    '''
    >>> brute = BruteForceRL('rab')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    8
    >>> brute = BruteForceRL('abracadabra')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    14
    >>> brute = BruteForceRL('bcara')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    34
    >>> brute = BruteForceRL('rabrabracad')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    23
    >>> brute = BruteForceRL('abacad')
    >>> brute.search('abacadabrabracabracadabrabrabracad')
    0
    '''

    def __init__(self, pattern):
        self._pat = pattern
        self._pat_len = len(pattern)

    def search(self, txt):
        txt_len = len(txt)
        for i in range(txt_len - self._pat_len + 1):
            j = self._pat_len - 1
            while j >= 0:
                if txt[j + i] != self._pat[j]:
                    break
                j -= 1
            if j == -1:
                return i
        return txt_len

if __name__ == '__main__':
    doctest.testmod()
