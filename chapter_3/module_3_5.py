#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import collections.abc
import random


# 3.5.8 practice, implement a LinearProbingHashTable which supports multiple values.
class LinearProbingHT(object):

    """
    >>> ht = LinearProbingHT()
    >>> for index, s in enumerate('SEARCHEXAMPLE'):
    ...     ht.put(s, index)
    ...
    >>> val = ht.get('E')
    >>> val in [1, 6, 12]
    True
    >>> val2 = ht.get('A')
    >>> val2 in [2, 8]
    True
    >>> ht.delete('E')
    >>> ht.get('E')
    >>>
    """

    def __init__(self):
        self._len = 16
        self._size = 0
        self._keys = [None] * self._len
        self._vals = [None] * self._len

    def __hash(self, key):
        return hash(key) & 0x7fffffff % self._len

    def __resize(self, size):
        tmp = LinearProbingHT()
        for i in range(self._len):
            if self._keys[i] is not None:
                for item in self._vals[i]:
                    tmp.put(self._keys[i], item)
        self._keys = tmp._keys
        self._vals = tmp._vals
        self._size = tmp._size

    def __contains(self, key):
        return self._keys[self.__hash(key)] is not None

    def put(self, key, value):
        assert isinstance(key, collections.abc.Hashable)

        if self._size >= self._len / 2:
            self.__resize(self._len * 2)

        index = self.__hash(key)
        while self._keys[index]:
            if self._keys[index] == key:
                self._vals[index].append(value)
                return
            index = (index + 1) % self._len

        self._keys[index], self._vals[index] = key, [value]
        self._size += 1

    def get(self, key):
        index = self.__hash(key)
        while self._keys[index]:
            if self._keys[index] == key:
                return random.choice(self._vals[index])
            index = (index + 1) % self._len
        return None

    def delete(self, key):
        if not self.__contains(key):
            return

        index = self.__hash(key)
        while self._keys[index] != key:
            index = (index + 1) % self._len

        self._keys[index] = self._vals[index] = None

        index = (index + 1) % self._len

        while self._keys[index]:
            k, v = self._keys[index], self._vals[index]
            self._keys[index] = self._vals[index] = None
            self._size -= 1
            self.put(k, v)
            index = (index + 1) % self._len

        self._size -= 1

        if self._size and self._size == self._len / 8:
            self.__resize(self._len / 2)

    def keys(self):
        for index, k in enumerate(self._keys):
            if k:
                yield k


if __name__ == '__main__':
    doctest.testmod()
