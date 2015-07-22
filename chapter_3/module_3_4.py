#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import string
import collections.abc


class Pair(object):

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val


class SeperateChainingHT(object):

    """
      Sperated hash table with chaining method, if one key-value node
    put into the position already exists another nodes, just make all
    these nodes as a linked list, and the new node append to the linked list.
    >>> test_str = 'SEARCHEXAMPLE'
    >>> ht = SeperateChainingHT()
    >>> for index, s in enumerate(test_str):
    ...     ht.put(s, index)
    ...
    >>> ht.put(['a', 'b'], 999)
    Traceback (most recent call last):
     ...
    AssertionError
    >>> ht.get('L')
    11
    >>> ht.get('S')
    0
    >>> ht.get('E')
    12
    >>> ht.delete('H')
    >>> ht.get('H')
    >>>
    """

    def __init__(self):
        self.__init(997)

    def __init(self, size):
        self._len = size
        self._size = 0
        self._st = [[]] * self._len

    def __hash(self, key):
        return hash(key) & 0x7fffffff % self._len

    def put(self, key, value):

        assert isinstance(key, collections.abc.Hashable)

        slot = self._st[self.__hash(key)]
        item = next((i for i in slot if i.key == key), None)
        if not item:
            slot.append(Pair(key, value))
        else:
            item.value = value

    def get(self, key):
        slot = self._st[self.__hash(key)]
        item = next((i for i in slot if i.key == key), None)
        return item.value if item else None

    # 3.4.9 practice, implement a delete function for Seperate-Chaining hash table
    def delete(self, key):
        slot = self._st[self.__hash(key)]
        item = next((i for i in slot if i.key == key), None)
        if item:
            slot.remove(item)

    def keys(self):
        results = []
        for k in self._st:
            if k:
                results.extend(k)
        return results


class LinearProbingHT(object):

    """
      Hash table with linear-probing strategy, when collision happens, which means
    hashed index is occupied by other element,
    then go to the next index, check the slot is available or not.
      This strategy need to make sure the list is 1/2 empty, because if the list has
    more than 1/2 * len elements, the performance of insertion will be decreased.
    >>> test_str = 'SEARCHEXAMPLE'
    >>> ht = LinearProbingHT()
    >>> for index, s in enumerate(test_str):
    ...     ht.put(s, index)
    ...
    >>> ht.put(['a', 'b'], 999)
    Traceback (most recent call last):
     ...
    AssertionError
    >>> ht.get('L')
    11
    >>> ht.get('S')
    0
    >>> ht.get('E')
    12
    >>> ht.delete('H')
    >>> ht.get('H')
    >>>
    """

    def __init__(self):
        self._len = 16  # the length of the list
        self._size = 0  # the amount of the variables
        self._keys = [None] * self._len
        self._vals = [None] * self._len

    def __hash(self, key):
        return hash(key) & 0x7fffffff % self._len

    def __resize(self, size):
        tmp = LinearProbingHT()
        for i in range(self._len):
            if self._keys[i] is not None:
                tmp.put(self._keys[i], self._vals[i])
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
                self._vals[index] = value
                return
            index = (index + 1) % self._len

        self._keys[index], self._vals[index] = key, value
        self._size += 1

    def get(self, key):
        index = self.__hash(key)
        while self._keys[index]:
            if self._keys[index] == key:
                return self._vals[index]
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

    # 3.4.19 practice
    def keys(self):
        for index, k in enumerate(self._keys):
            if k:
                yield self._vals[index]


# 3.4.4 practice
def find_complete_hash_number(hash_string):
    def unique_index(a, m, hash_string):
        index = set()
        for s in hash_string:
            hash_index = (a * string.ascii_uppercase.index(s)) % m
            if hash_index not in index:
                index.add(hash_index)
            else:
                return False
        return True

    for m in range(len(hash_string), 100000):
        for a in range(1, 1001):
            if unique_index(a, m, hash_string):
                return a, m
    return None, None


if __name__ == '__main__':
    doctest.testmod()
    # print(find_complete_hash_number('SEARCHXMPL'))
