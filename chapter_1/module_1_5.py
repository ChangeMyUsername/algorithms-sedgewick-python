# !/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random


class UnionFind(object):

    '''
    union find implementation, the algorithm is a little bit like tree algorithm but not the same.
    >>> uf = UnionFind(10)
    >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
    ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
    >>> for i, j in connections:
    ...     uf.union(i, j)
    ...
    >>> uf.connected(1, 4)
    False
    >>> uf.connected(8, 4)
    True
    >>> uf.connected(1, 5)
    True
    >>> uf.connected(1, 7)
    True
    '''

    def __init__(self, size):
        self._id = [i for i in range(size)]
        self._count = size

    def count(self):
        return self._count

    def find(self, node):
        root = node
        while root != self._id[root]:
            root = self._id[root]
        # 1.5.12 practice
        while node != root:
            new_node = self._id[node]
            self._id[node] = root
            node = new_node
        return root

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        p_root = self.find(p)
        q_root = self.find(q)
        if p_root == q_root:
            return
        self._id[p_root] = q_root
        self._count -= 1


class WeightedUnionFind(object):

    '''
    weighted union find algorithm, put the smaller tree into the larger tree, lower the tree size.
    >>> wuf = WeightedUnionFind(10)
    >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4),
    ... (2, 1), (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
    >>> for i, j in connections:
    ...     wuf.union(i, j)
    ...
    >>> wuf.connected(1, 4)
    False
    >>> wuf.connected(8, 4)
    True
    >>> wuf.connected(1, 5)
    True
    >>> wuf.connected(1, 7)
    True
    '''

    def __init__(self, size):
        self._count = size
        self._id = [i for i in range(size)]
        self._size = [1] * size

    def count(self):
        return self._count

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def find(self, node):
        root = node
        while root != self._id[root]:
            root = self._id[root]
        # 1.5.13 practice
        while node != root:
            new_node = self._id[node]
            self._id[node] = root
            node = new_node
        return root

    def union(self, p, q):
        p_root = self.find(p)
        q_root = self.find(q)
        if p_root == q_root:
            return
        if self._size[p_root] < self._size[q_root]:
            self._id[p_root] = q_root
            self._size[q_root] += self._size[p_root]
        else:
            self._id[q_root] = p_root
            self._size[p_root] += self._size[q_root]
        self._count -= 1


# 1.5.14 practice
class HeightedUnionFind(object):

    '''
    heighted union find algorithm,
    put the shorter tree into taller tree,
    the tree's height won't be taller than log(n).
    >>> huf = HeightedUnionFind(10)
    >>> connections = [(9, 0), (3, 4), (5, 8), (7, 2), (2, 1), (5, 7), (0, 3), (4, 2)]
    >>> for i, j in connections:
    ...     huf.union(i, j)
    ...
    >>> huf.connected(9, 3)
    True
    >>> huf.connected(0, 1)
    True
    >>> huf.connected(9, 8)
    True
    '''

    def __init__(self, size):
        self._id = [i for i in range(size)]
        self._height = [1] * size
        self._count = size

    def count(self):
        return self._count

    def find(self, node):
        while node != self._id[node]:
            node = self._id[node]
        return node

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        p_root = self.find(p)
        q_root = self.find(q)
        if p_root == q_root:
            return
        if self._height[p_root] < self._height[q_root]:
            self._id[p_root] = q_root
        elif self._height[p_root] > self._height[q_root]:
            self._id[q_root] = p_root
        else:
            self._id[q_root] = p_root
            self._height[p_root] += 1
        self._count -= 1


# 1.5.17 practice
def erdos_renyi(size):
    '''
    >>> erdos_renyi(1000)
    '''
    uf = UnionFind(size)
    while uf.count() > 1:
        a = random.randint(0, size - 1)
        b = random.randint(0, size - 1)
        if a == b:
            continue
        if not uf.connected(a, b):
            uf.union(a, b)

if __name__ == '__main__':
    doctest.testmod()
