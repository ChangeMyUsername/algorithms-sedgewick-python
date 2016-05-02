#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
from basic_data_struct import Bag
from collections import defaultdict
import random
import doctest


M_SIZE = 6


class Entry(object):

    def __init__(self, key, value, node):
        self._key = key
        self._value = value
        self._next_node = node

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def next_node(self):
        return self._next_node


class Node(object):

    def __init__(self, k):
        self._m_size = k
        self._children = [None] * M_SIZE

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, new_children):
        self._children = new_children

    @property
    def m_size(self):
        return self._m_size

    @m_size.setter
    def m_size(self, size):
        self._m_size = size


class BTree(object):

    '''
    >>> btree = BTree()
    >>> data = {"www.cs.princeton.edu": "128.112.136.12",
    ...         "www.cs.princeton.edu": "128.112.136.11",
    ...         "www.princeton.edu":    "128.112.128.15",
    ...         "www.yale.edu":         "130.132.143.21",
    ...         "www.simpsons.com":     "209.052.165.60",
    ...         "www.apple.com":        "17.112.152.32",
    ...         "www.amazon.com":       "207.171.182.16",
    ...         "www.ebay.com":        "66.135.192.87",
    ...         "www.cnn.com":          "64.236.16.20",
    ...         "www.google.com":       "216.239.41.99",
    ...         "www.nytimes.com":      "199.239.136.200",
    ...         "www.microsoft.com":    "207.126.99.140",
    ...         "www.dell.com":         "143.166.224.230",
    ...         "www.slashdot.org":     "66.35.250.151",
    ...         "www.espn.com":         "199.181.135.201",
    ...         "www.weather.com":      "63.111.66.11",
    ...         "www.yahoo.com":        "216.109.118.65"}
    >>> for k, v in data.items():
    ...     btree.put(k, v)
    ...
    >>> btree.get("www.yahoo.com")
    216.109.118.65
    >>> btree.get("www.slashdot.org")
    66.35.250.151
    >>> btree.get("www.cs.princeton.edu")
    128.112.136.11
    >>> btree.size() == len(data) - 1
    True
    '''

    def __init__(self):
        self._root = Node(0)
        self._size = 0
        self._height = 0

    def size(self):
        return self._size

    def height(self):
        return self._height

    def put(self, key, value):
        u = self._insert(self._root, key, value, self._height)
        self._size += 1
        if not u:
            return
        tmp = Node(2)
        tmp.children[0] = Entry(self._root.children[0].key, None, self._root)
        tmp.children[1] = Entry(u.children[0].key, None, u)
        self._root = tmp
        self._height += 1

    def _insert(self, node, key, value, height):
        pos = 0
        new_entry = Entry(key, value, None)
        # external node
        if height == 0:
            while pos < node.m_size:
                if node.children[pos] and key < node.children[pos].key:
                    break
                pos += 1
        else:
            while pos < node.m_size:
                if pos + 1 == node.m_size or key < node.children[pos + 1].key:
                    u = self._insert(node.children[pos + 1], key, value, height - 1)
                    if not u:
                        return None
                    new_entry.key = u.children[0].key
                    new_entry.next_node = u
                    break
                pos += 1

        for i in range(node.m_size, pos, -1):
            node.children[i] = node.children[i - 1]
        node.children[pos] = new_entry
        node.m_size += 1
        if node.m_size < M_SIZE:
            return None
        return self._split(node)

    def _split(self, node):
        new_size = int(M_SIZE / 2)
        split_node = Node(new_size)
        node._m_size = new_size
        for i in range(new_size):
            split_node._children[i] = node._children[new_size + i]
        return split_node

    def get(self, key):
        return self._search(self._root, key, self._height)

    def _search(self, node, key, height):
        if height == 0:
            for i in range(node.m_size):
                if node.children[i].key == key:
                    return node.children[i].value
        else:
            for i in range(node.m_size):
                if i + 1 == node.m_size or key < node.children[i + 1].key:
                    return self._search(node.children[i].next_node, key, height - 1)
        return None


class QuickThreeWay(object):

    def sort(self, lst):
        random.shuffle(lst)
        self.__sort(lst, 0, len(lst) - 1)

    def __sort(self, lst, low, high):
        if high <= low:
            return

        lt, i, gt, val = low, low + 1, high, lst[low]
        while i <= gt:
            if lst[i] < val:
                lst[lt], lst[i] = lst[i], lst[lt]
                lt += 1
                i += 1
            elif lst[i] > val:
                lst[gt], lst[i] = lst[i], lst[gt]
                gt -= 1
            else:
                i += 1
        self.__sort(lst, low, lt - 1)
        self.__sort(lst, gt + 1, high)


class SuffixArray(object):

    def __init__(self, s):
        self._length = len(s)
        self._suffixes = []
        for i in range(self._length):
            self._suffixes.append(s[i:self._length])
        qtw = QuickThreeWay()
        qtw.sort(self._suffixes)

    def length(self):
        return self._length

    def select(self, index):
        return self._suffixes[index]

    def lcp(self, index):
        return self._lcp(self._suffixes[index], self._suffixes[index - 1])

    def _lcp(self, s1, s2):
        min_len = min(len(s1), len(s2))
        for i in range(min_len):
            if s1[i] != s2[i]:
                return i
        return min_len

    def rank(self, key):
        low, high = 0, self._length
        while low <= high:
            mid = (low + high) // 2
            if self._suffixes[mid] > key:
                high = mid - 1
            elif self._suffixes[mid] < key:
                low = mid + 1
            else:
                return mid


class LRS(object):

    '''

    '''

    @staticmethod
    def run(input_string):
        sa = SuffixArray(input_string)
        length = len(input_string)
        lrs = ''
        for i in range(length):
            tmp_len = sa.lcp(i)
            if tmp_len > len(lrs):
                lrs = sa.select(i)[0:tmp_len]
        return lrs


class FlowEdge(object):

    '''
    >>> edge = FlowEdge(1, 2, 2.0, 1)
    >>> edge
    1->2 1/2.0
    '''

    def __init__(self, start, end, capacity,
                 flow=None, edge=None):
        if edge:
            self._start = edge.start
            self._end = edge.end
            self._capacity = edge.capacity
            self._flow = edge.flow
            return
        self._start = start
        self._end = end
        self._capacity = capacity
        self._flow = flow

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def capacity(self):
        return self._capacity

    @property
    def flow(self):
        return self._flow

    def other(self, vertex):
        if vertex == self.start:
            return self._end
        elif vertex == self._end:
            return self._start
        raise RuntimeError('Illegal endpoint')

    def add_residual_flow_to(self, vertex, delta):
        if vertex == self._start:
            self._flow -= delta
        elif vertex == self._end:
            self._flow += delta
        raise RuntimeError('Illegal endpoint')

    def __repr__(self):
        return '{}->{} {}/{}'.format(
            self._start, self._end, self._flow, self._capacity)


class FlowNetwork(object):

    def __init__(self):
        self._adj = defaultdict(Bag)
        self._vertices_size = 0
        self._edges_size = 0

    def vertices_size(self):
        return self._vertices_size

    def edges_size(self):
        return self._edges_size

    def add_edge(self, edge):
        self._edges_size += 1
        self._adj[edge.start].add(edge)
        self._adj[edge.end].add(edge)

    def adj_edges(self, vertex):
        return self._adj[vertex]

    def edges(self):
        for v in self._adj:
            for edge in self._adj[v]:
                if edge.end != v:
                    yield edge

    def __repr__(self):
        s = '{} vertices, {} edges\n'.format(self._vertices_size, self._edges_size)
        for v in self._adj:
            tmp = '{}: {}'.format(v, ', '.join(e for e in self._adj[v] if e.end != v))
            s += tmp


if __name__ == '__main__':
    doctest.testmod()
