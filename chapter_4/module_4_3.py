#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import copy
from collections import defaultdict
from basic_data_struct import Bag, Queue, MinPQ


class Edge(object):

    """
    minimum spanning tree edge representation.
    """

    def __init__(self, vertex_a, vertex_b, weight):
        self._vertex_a = vertex_a
        self._vertex_b = vertex_b
        self._weight = weight

    def either(self):
        return self._vertex_a

    def other(self, vertex):
        if vertex not in (self._vertex_a, self._vertex_b):
            return None
        return self._vertex_a if vertex == self._vertex_b else self._vertex_b

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w):
        self._weight = w

    def __cmp__(self, other):
        if self._weight < other.weight:
            return -1
        elif self._weight > other.weight:
            return 1
        return 0

    def __repr__(self):
        return "{}-{} {}".format(self._vertex_a, self._vertex_b, self._weight)


class EdgeWeightedGraph(object):

    """
      Undirected graph with weighted edge implementation, a new class named Edge will
    represent a weighted edge.
    >>> test_data = ((4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 5, 0.32),
    ...              (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19), (0, 2, 0.26), (1, 2, 0.36),
    ...              (1, 3, 0.29), (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58),
    ...              (6, 4, 0.93))
    >>> ewg = EdgeWeightedGraph()
    >>> for a, b, weight in test_data:
    ...    edge = Edge(a, b, weight)
    ...    ewg.add_edge(edge)
    ...
    >>> ewg.edges_size()
    16
    >>> ewg.vertices_size()
    8
    >>> [e for e in ewg.adjacent_edges(5)]
    [1-5 0.32, 5-7 0.28, 4-5 0.35]
    >>> ewg
    8 vertices, 16 edges.
    0: 6-0 0.58, 0-2 0.26, 0-4 0.38, 0-7 0.16
    1: 1-3 0.29, 1-2 0.36, 1-7 0.19, 1-5 0.32
    2: 6-2 0.4, 2-7 0.34, 1-2 0.36, 0-2 0.26, 2-3 0.17
    3: 3-6 0.52, 1-3 0.29, 2-3 0.17
    4: 6-4 0.93, 0-4 0.38, 4-7 0.37, 4-5 0.35
    5: 1-5 0.32, 5-7 0.28, 4-5 0.35
    6: 6-4 0.93, 6-0 0.58, 3-6 0.52, 6-2 0.4
    7: 2-7 0.34, 1-7 0.19, 0-7 0.16, 5-7 0.28, 4-7 0.37
    <BLANKLINE>
    """

    def __init__(self, graph=None):
        self._adj = defaultdict(Bag)
        self._edges_size = 0

        if graph:
            self._adj = copy.deepcopy(graph._adj)
            self._edges_size = graph.edges_size()

    def edges_size(self):
        return self._edges_size

    def vertices_size(self):
        return len(self._adj.keys())

    def add_edge(self, edge):
        a = edge.either()
        b = edge.other(a)
        self._adj[a].add(edge)
        self._adj[b].add(edge)
        self._edges_size += 1

    def adjacent_edges(self, vertex):
        return self._adj[vertex]

    def vertices(self):
        return self._adj.keys()

    def edges(self):
        result = Bag()
        for v in self.vertices():
            for edge in self.adjacent_edges(v):
                if edge.other(v) != v:
                    result.add(edge)
        return result

    def __repr__(self):
        print_string = '{} vertices, {} edges.\n'.format(
            self.vertices_size(), self.edges_size())
        for v in self.vertices():
            try:
                lst = ', '.join([vertex for vertex in self._adj[v]])
            except TypeError:
                lst = ', '.join([str(vertex) for vertex in self._adj[v]])
            print_string += '{}: {}\n'.format(v, lst)
        return print_string


class LazyPrimMST(object):

    def __init__(self, graph, start_vertex):
        self._pq = MinPQ()
        self._marked = defaultdict(bool)
        self._mst = Queue()
        self.visit(graph. start_vertex)
        while not self._pq.is_empty():
            edge = self._pq.del_min()
            a = edge.either()
            b = edge.other(a)
            if self._marked[a] and self._marked[b]:
                continue
            self._mst.enqueue(edge)
            if not self._marked[a]:
                self.visit(graph, a)
            if not self._marked(b):
                self.visit(graph, b)

    def visit(self, graph, vertex):
        self._marked[vertex] = True
        for edge in graph.adjacent_edges(vertex):
            if not self._marked(edge.other(vertex)):
                self._pq.insert(edge)

    def edges(self):
        return self._mst

if __name__ == '__main__':
    doctest.testmod()
