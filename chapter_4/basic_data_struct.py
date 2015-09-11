#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

"""
    copy from module_1_3.py, this is for avoiding package import problems.
"""


class Node(object):

    def __init__(self, val):
        self._val = val
        self.next_node = None

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, node):
        self._next_node = node


class Stack(object):

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def push(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def pop(self):
        if self._first:
            old = self._first
            self._first = self._first.next_node
            self._size -= 1
            return old.val
        return None

    # 1.3.7 practice
    def peek(self):
        if self._first:
            return self._first.val
        return None


class Queue(object):

    def __init__(self, q=None):
        self._first = None
        self._last = None
        self._size = 0
        if q:
            for item in q:
                self.enqueue(item)

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def enqueue(self, val):
        old_last = self._last
        self._last = Node(val)
        self._last.next_node = None
        if self.is_empty():
            self._first = self._last
        else:
            old_last.next_node = self._last
        self._size += 1

    def dequeue(self):
        if not self.is_empty():
            val = self._first.val
            self._first = self._first.next_node
            if self.is_empty():
                self._last = None
            self._size -= 1
            return val
        return None


class Bag(object):

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node is not None:
            yield node.val
            node = node.next_node

    def __contains__(self, item):
        tmp = self._first
        while tmp:
            if tmp == item:
                return True
        return False

    def add(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size


class MinPQ(object):

    def __init__(self, data=None):
        self._pq = []
        if data:
            for item in data:
                self.insert(data)

    def is_empty(self):
        return len(self._pq) == 0

    def size(self):
        return len(self._pq)

    def swim(self, pos):
        while pos > 0 and self._pq[(pos - 1) // 2] > self._pq[pos]:
            self._pq[(pos - 1) // 2], self._pq[pos] = self._pq[pos], self._pq[(pos - 1) // 2]
            pos = (pos - 1) // 2

    def sink(self, pos):
        length = len(self._pq) - 1
        while 2 * pos + 1 <= length:
            index = 2 * pos + 1
            if index < length and self._pq[index] > self._pq[index + 1]:
                index += 1
            if self._pq[pos] <= self._pq[index]:
                break
            self._pq[index], self._pq[pos] = self._pq[pos], self._pq[index]
            pos = index

    def insert(self, val):
        self._pq.append(val)
        self.swim(len(self._pq) - 1)

    def del_min(self):
        min_val = self._pq[0]
        last_index = len(self._pq) - 1
        self._pq[0], self._pq[last_index] = self._pq[last_index], self._pq[0]
        self._pq.pop(last_index)
        self.sink(0)
        return min_val

    def min_val(self):
        return self._pq[0]


class DisjointNode(object):

    def __init__(self, parent, size=1):
        self._parent = parent
        self._size = size

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        assert val > 0
        self._size = val


class GenericUnionFind(object):

    """
    >>> guf = GenericUnionFind()
    >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4),
    ...                (2, 1), (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
    >>> for i, j in connections:
    ...     guf.union(i, j)
    ...
    >>> guf.connected(1, 4)
    False
    >>> guf.connected(8, 4)
    True
    >>> guf.connected(1, 5)
    True
    >>> guf.connected(1, 7)
    True
    """

    def __init__(self, tuple_data=None):
        self._id = {}
        if tuple_data:
            for a, b in tuple_data:
                self.union(a, b)

    def count(self):
        pass

    def connected(self, p, q):
        return self.find(p) and self.find(q) and self.find(p) == self.find(q)

    def find(self, node):
        if node not in self._id:
            return None
        tmp = node
        while self._id[tmp].parent != tmp:
            tmp = self._id[tmp].parent
        return self._id[tmp].parent

    def union(self, p, q):
        p_root = self.find(p)
        q_root = self.find(q)

        if p_root == q_root:
            if p_root is None and q_root is None:
                self._id[p] = DisjointNode(q)
                self._id[q] = DisjointNode(q, 2)
                return
            return

        if p_root is None:
            self._id[p] = DisjointNode(q_root, 1)
            self._id[q_root].size += 1
            return

        if q_root is None:
            self._id[q] = DisjointNode(p_root, 1)
            self._id[p_root].size += 1
            return

        if self._id[p_root].size < self._id[q_root].size:
            self._id[p_root].parent = q_root
            self._id[q_root].size += self._id[p_root].size
        else:
            self._id[q_root].parent = p_root
            self._id[p_root].size += self._id[q_root].size


class EdgeConnectedComponent(object):

    """
    >>> g = Graph()
    >>> test_data = [(0, 5), (4, 3), (0, 1), (9, 12), (6, 4), (5, 4), (0, 2),
    ...              (11, 12), (9, 10), (0, 6), (7, 8), (9, 11), (5, 3)]
    >>> for a, b in test_data:
    ...     g.add_edge(a, b)
    ...
    >>> ecc = ConnectedComponent(g)
    >>> cc.connected(0, 8)
    False
    >>> cc.connected(0, 4)
    True
    >>> cc.connected(0, 9)
    False
    >>> cc.vertex_id(0)
    0
    >>> cc.vertex_id(7)
    1
    >>> cc.vertex_id(11)
    2
    >>> cc.count()
    3
    """

    def __init__(self, graph):
        self._marked = defaultdict(bool)
        self._id = defaultdict(int)
        self._count = 0

        for edge in graph.edges():
            if not self._marked[edge.other()]:
                self.dfs(graph, edge.other())
                self._count += 1

    def dfs(self, graph, vertex):
        self._marked[vertex] = True
        self._id[vertex] = self._count
        for edge in graph.adjacent_edges(vertex):
            if not self._marked[edge.either(vertex)]:
                self.dfs(graph, edge.either(vertex))

    def connected(self, vertex_1, vertex_2):
        return self._id[vertex_1] == self._id[vertex_2]

    def vertex_id(self, vertex):
        return self._id[vertex]

    def count(self):
        return self._count

    def get_components(self):
        for k, v in groupby(sorted(self._id), key=itemgetter(1)):
            yield tuple(v)

if __name__ == '__main__':
    doctest.testmod()
