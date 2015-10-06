#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import pprint
from collections import defaultdict


def lsd_sort(string_list, width):
    """
      LSD (least significant digit) algorithm implementation. This algorithm can sort
    strings with certain length. LSD algorithm need to access arrays about ~7WN + 3WR times
    (W is string's length, N is the number of all strings, R is the number of all
    characters in the strings). The cost of space is proportional to N + R.
    >>> test_data = ['bed', 'bug', 'dad', 'yes', 'zoo', 'now', 'for', 'tip', 'ilk',
    ...              'dim', 'tag', 'jot', 'sob', 'nob', 'sky', 'hut', 'men', 'egg',
    ...              'few', 'jay', 'owl', 'joy', 'rap', 'gig', 'wee', 'was', 'wad',
    ...              'fee', 'tap', 'tar', 'dug', 'jam', 'all', 'bad', 'yet']
    >>> lsd_sort(test_data, 3)
    >>> pp = pprint.PrettyPrinter(width=41, compact=True)
    >>> pp.pprint(test_data)
    ['all', 'bad', 'bed', 'bug', 'dad',
     'dim', 'dug', 'egg', 'fee', 'few',
     'for', 'gig', 'hut', 'ilk', 'jam',
     'jay', 'jot', 'joy', 'men', 'nob',
     'now', 'owl', 'rap', 'sky', 'sob',
     'tag', 'tap', 'tar', 'tip', 'wad',
     'was', 'wee', 'yes', 'yet', 'zoo']
    """

    length = len(string_list)
    radix = 256
    aux = [None] * length

    for i in range(width - 1, -1, -1):
        count = [0] * (radix + 1)

        for j in range(length):
            count[ord(string_list[j][i]) + 1] += 1

        for k in range(radix - 1):
            count[k + 1] += count[k]

        for p in range(length):
            aux[count[ord(string_list[p][i])]] = string_list[p]
            count[ord(string_list[p][i])] += 1

        for n in range(length):
            string_list[n] = aux[n]


class MSD(object):

    """
      MSD(most significant digit) algorithm implementation. MSD can handle strings with
    different length. Because a recursive process exists, so just in case that maximum
    recursion depth exceeded, MSD switch to insertion sort when handling small arrays.
    The performance will be not fine when most of input strings are the same. And the cost
    of space is very expensive because each recursion sort need to create a counting array,
    and some of recursions is unnessesary.
    >>> test_data = ['she', 'sells', 'seashells', 'by', 'the', 'sea', 'shore',
    ...              'the', 'shells', 'she', 'sells', 'are', 'surely', 'seashells']
    >>> msd = MSD()
    >>> msd.sort(test_data)
    >>> pp = pprint.PrettyPrinter(width=41, compact=True)
    >>> pp.pprint(test_data)
    ['are', 'by', 'sea', 'seashells',
     'seashells', 'sells', 'sells', 'she',
     'she', 'shells', 'shore', 'surely',
     'the', 'the']
    """

    def __init__(self):
        self._radix = 256
        self._switch_2_insertion_length = 20

    def char_at(self, s, index):
        return ord(s[index]) if index < len(s) else -1

    def _insertion_sort(self, lst, start, end, index):
        for i in range(start, end + 1):
            tmp = i
            while tmp > start and lst[tmp][index:] < lst[tmp - 1][index:]:
                lst[tmp - 1], lst[tmp] = lst[tmp], lst[tmp - 1]
                tmp -= 1

    def sort(self, string_list):
        length = len(string_list)
        aux = [None] * length
        self._sort(string_list, 0, length - 1, 0, aux)

    def _sort(self, string_list, start, end, index, aux):
        if end <= start + self._switch_2_insertion_length:
            self._insertion_sort(string_list, start, end, index)
            return

        count = [0] * (self._radix + 2)

        for i in range(start, end + 1):
            count[self.char_at(string_list[i], index) + 2] += 1

        for r in range(self._radix + 1):
            count[r + 1] += count[r]

        for j in range(start, end + 1):
            v = self.char_at(string_list[j], index) + 1
            aux[count[v]] = string_list[j]
            count[v] += 1

        for n in range(start, end + 1):
            string_list[n] = aux[n - start]

        for r in range(self._radix):
            self._sort(string_list, start + count[r], start + count[r + 1] - 1, index + 1, aux)


class Quick3String(object):

    """
      Quick Three Way algorithm for string sorting purpose. This is almost the
    same as Quick Three Way, but it takes ith character of each string as comparison.
    It's really helpful when large repetive strings as input strings.
    >>> test_data = ['she', 'sells', 'seashells', 'by', 'the', 'sea', 'shore',
    ...              'the', 'shells', 'she', 'sells', 'are', 'surely', 'seashells']
    >>> q3s = Quick3String()
    >>> q3s.sort(test_data)
    >>> pp = pprint.PrettyPrinter(width=41, compact=True)
    >>> pp.pprint(test_data)
    ['are', 'by', 'sea', 'seashells',
     'seashells', 'sells', 'sells', 'she',
     'she', 'shells', 'shore', 'surely',
     'the', 'the']
    """

    def char_at(self, s, index):
        return ord(s[index]) if index < len(s) else -1

    def sort(self, string_list):
        self._sort(string_list, 0, len(string_list) - 1, 0)

    def _sort(self, string_list, start, end, index):
        if start >= end:
            return

        lt, gt, val, i = start, end, self.char_at(string_list[start], index), start + 1

        while i <= gt:
            tmp = self.char_at(string_list[i], index)
            if tmp < val:
                string_list[i], string_list[lt] = string_list[lt], string_list[i]
                lt += 1
            elif tmp > val:
                string_list[i], string_list[gt] = string_list[gt], string_list[i]
                gt -= 1
                continue
            i += 1

        self._sort(string_list, start, lt - 1, index)

        if val > 0:
            self._sort(string_list, lt, gt, index + 1)
        self._sort(string_list, gt + 1, end, index)


# 5.1.1 practice
def simple_radix_sort(strings):
    count = defaultdict(int)
    for s in strings:
        count[s] += 1


if __name__ == '__main__':
    doctest.testmod()
