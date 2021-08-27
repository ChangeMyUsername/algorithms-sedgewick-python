#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from typing import Generator, MutableSequence

from common import CT


def rank(mseq: MutableSequence[CT], k: CT) -> CT:
    """Return the `k` rank element of `seq`

    Args:
        seq (MutableSequence[CT]): input sequence
        k (CT): element index

    Returns:
        CT: element in sequence

    >>> import random
    >>> seq = [i for i in range(10)]
    >>> random.shuffle(seq)
    >>> [rank(seq, i) for i in range(10)]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    def partition(seq: MutableSequence[CT], low: int, high: int) -> int:
        """Quick sort partition process, return pivot's changed position
        after partition.

        Args:
            seq (MutableSequence[CT]): input array
            low (int): start index
            high (int): end index

        Returns:
            int: index of pivot
        """
        i, j = low + 1, high
        val = seq[low]
        while 1:
            while i < high and seq[i] <= val:
                i += 1
            while j > low and seq[j] >= val:
                j -= 1
            if i >= j:
                break
            seq[i], seq[j] = seq[j], seq[i]

        seq[low], seq[j] = seq[j], seq[low]
        return j

    low, high = 0, len(mseq) - 1
    while high > low:
        j = partition(mseq, low, high)
        if j == k:
            return mseq[k]
        elif j > k:
            high = j - 1
        elif j < k:
            low = j + 1
    return mseq[k]


# 2.5.4 practice, return a sorted and non-duplicated-item list
def dedup(seq: MutableSequence[CT]) -> Generator[CT, None, None]:
    """Return a new sorted and deduplicated sequence from `seq`.

    Args:
        seq (MutableSequence[CT]): input sequence

    Yields:
        Generator[CT]: generator with unique element

    >>> lst = [i for i in dedup([2, 1, 3, 1, 1, 3, 2, 3, 4, 7])]
    >>> lst
    [1, 2, 3, 4, 7]
    >>> lst2 = [i for i in dedup([1, 1])]
    >>> lst2
    [1]
    >>> lst3 = [i for i in dedup([2, 1, 1, 4, 3, 5])]
    >>> lst3
    [1, 2, 3, 4, 5]
    """
    assert seq and len(seq) >= 2

    new_list = sorted(seq)
    val, count, length = new_list[0], 1, len(new_list)
    for i in range(1, length):
        if new_list[i] == val:
            if i == length - 1:
                yield new_list[i]
            count += 1
        else:
            count = 1
            val = new_list[i]
            yield new_list[i - count]
    if count == 1:
        yield new_list[length - 1]


# 2.5.10 practice, implement a version class with __cmp__
class Version(object):

    """
    >>> lst = [Version(i) for i in ['115.1.1', '115.10.1', '115.10.2']]
    >>> lst.sort()
    >>> lst
    [Version(115.1.1), Version(115.10.1), Version(115.10.2)]
    """

    def __init__(self, version):
        self._version = version

    def __eq__(self, other):
        return self._version == other._version

    def __lt__(self, other):
        return self._version < other._version

    def __repr__(self):
        return 'Version({})'.format(self._version)

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, val):
        assert all(i.isdigit() for i in val.split('.'))
        self._version = val


# 2.5.14 practice, implement a domain class with __cmp__,
# compare the reversed order domain.
class Domain(object):

    """
    >>> test_list = ['cs.princeton.edu', 'cs.harvard.edu', 'mail.python.org', 'cs.mit.edu']
    >>> lst = [Domain(i) for i in test_list]
    >>> lst.sort()
    >>> lst
    [Domain(cs.harvard.edu), Domain(cs.mit.edu), Domain(cs.princeton.edu), Domain(mail.python.org)]
    """

    def __init__(self, domain):
        self._domain = domain
        self._cmp_domain = '.'.join(reversed(self._domain.split('.')))

    def __eq__(self, other):
        return self._cmp_domain == other._cmp_domain

    def __lt__(self, other):
        return self._cmp_domain < other._cmp_domain

    def __repr__(self):
        return 'Domain({})'.format(self._domain)

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, val):
        self._domain = val
        self._cmp_domain = '.'.join(reversed(self._domain.split('.')))


# 2.5.16 practice, construct object which
# order by the name with a new alphabet order
class California(object):

    """
    >>> seq = [California(name) for name
    ... in ('RISBY', 'PATRICK', 'DAMIEN', 'GEORGE')]
    >>> seq.sort()
    >>> seq
    [California(RISBY), California(GEORGE), California(PATRICK), California(DAMIEN)]
    """
    alphabet = ('R', 'W', 'Q', 'O', 'J', 'M', 'V', 'A',
                'H', 'B', 'S', 'G', 'Z', 'X', 'N',
                'T', 'C', 'I', 'E', 'K', 'U', 'P', 'D', 'Y', 'F', 'L')

    def __init__(self, name):
        self._name = name
        self._cmp_tuple = tuple(California.alphabet.index(i)
                                for i in self._name)

    def __eq__(self, other):
        return self._cmp_tuple == other._cmp_tuple

    def __lt__(self, other):
        return self._cmp_tuple < other._cmp_tuple

    def __repr__(self):
        return 'California({})'.format(self._name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val
        self._cmp_tuple = tuple(California.alphabet.index(i)
                                for i in self._name)


# 2.5.19 practice, kendall tau algorithm implementation
class KendallTau(object):

    """
    >>> klt = KendallTau()
    >>> klt.kendall_tau_count((0, 3, 1, 6, 2, 5, 4), (1, 0, 3, 6, 4, 2, 5))
    4
    """

    def kendall_tau_count(self, origin_list, count_list):
        lst = [origin_list.index(count_list[i])
               for i in range(len(count_list))]
        aux = lst[:]
        return self.count(lst, aux, 0, len(lst) - 1)

    def count(self, lst, aux, low, high):
        if low >= high:
            return 0
        mid = (low + high) // 2
        lc = self.count(lst, aux, low, mid)
        rc = self.count(lst, aux, mid + 1, high)
        mc = self.merge_count(lst, aux, low, mid, high)
        return lc + rc + mc

    def merge_count(self, lst, aux, low, mid, high):
        aux[low:high + 1] = lst[low:high + 1]
        count, left, right = 0, low, mid + 1
        for j in range(low, high + 1):
            if left > mid:
                lst[j] = aux[right]
                right += 1
            elif right > high:
                lst[j] = aux[left]
                left += 1
            elif aux[left] < aux[right]:
                lst[j] = aux[left]
                left += 1
            else:
                lst[j] = aux[right]
                right += 1
                count += mid - left + 1
        return count


if __name__ == '__main__':
    doctest.testmod()
