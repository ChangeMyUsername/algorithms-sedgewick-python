#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import pprint


def lsd_sort(string_list, width):
    """
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
    r = 256
    aux = [None] * length

    for i in range(width - 1, -1, -1):
        count = [0] * (r + 1)

        for j in range(length):
            count[ord(string_list[j][i]) + 1] += 1

        for k in range(r - 1):
            count[k + 1] += count[k]

        for p in range(length):
            aux[count[ord(string_list[p][i])]] = string_list[p]
            count[ord(string_list[p][i])] += 1

        for n in range(length):
            string_list[n] = aux[n]


if __name__ == '__main__':
    doctest.testmod()
