#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from collections import defaultdict
from abc import ABCMeta
from basic_data_struct import Bag, IndexMinPQ, Stack

INFINITE_NUMBER = float('inf')


class DirectedEdge(object):

    """
      Weighted Digraph Edge object.
    """

    def __init__(self, start, end, weight):
        self._start = start
        self._end = end
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w):
        self._weight = w

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = end

    def __repr__(self):
        return '{}->{} {}'.format(self._start, self._end, self._weight)


class EdgeWeightedDigraph(object):

    """
    >>> test_data = ((4, 5, 0.35), (5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28), (7, 5, 0.28),
    ...              (5, 1, 0.32), (0, 4, 0.38), (0, 2, 0.26), (7, 3, 0.39), (1, 3, 0.29),
    ...              (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93))
    >>> ewd = EdgeWeightedDigraph()
    >>> for a, b, weight in test_data:
    ...     edge = DirectedEdge(a, b, weight)
    ...     ewd.add_edge(edge)
    ...
    >>> ewd.vertices_size()
    8
    >>> ewd.edges_size()
    15
    >>> [edge for edge in ewd.adjacent_edges(5)]
    [5->1 0.32, 5->7 0.28, 5->4 0.35]
    >>> [edge for edge in ewd.adjacent_edges(7)]
    [7->3 0.39, 7->5 0.28]
    >>> ewd
    8 vertices, 15 edges
    0: 0->2 0.26, 0->4 0.38
    1: 1->3 0.29
    2: 2->7 0.34
    3: 3->6 0.52
    4: 4->7 0.37, 4->5 0.35
    5: 5->1 0.32, 5->7 0.28, 5->4 0.35
    6: 6->4 0.93, 6->0 0.58, 6->2 0.4
    7: 7->3 0.39, 7->5 0.28
    <BLANKLINE>
    """

    def __init__(self):
        self._vertices = set()
        self._edges_size = 0
        self._adj = defaultdict(Bag)

    def add_edge(self, edge):
        self._adj[edge.start].add(edge)
        self._vertices.add(edge.start)
        self._vertices.add(edge.end)
        self._edges_size += 1

    def adjacent_edges(self, vertex):
        return self._adj[vertex]

    def edges(self):
        result = Bag()
        for v in self._vertices:
            for edge in self._adj[v]:
                result.add(edge)
        return result

    def vertices_size(self):
        return len(self._vertices)

    def edges_size(self):
        return self._edges_size

    def __repr__(self):
        print_str = '{} vertices, {} edges\n'.format(
            len(self._vertices), self._edges_size)
        edge_str = '{}->{} {}'
        for v in self._vertices:
            edges = ', '.join(
                edge_str.format(edge.start, edge.end, edge.weight) for edge in self._adj[v])
            print_str += '{}: {}\n'.format(v, edges)
        return print_str


class ShortestPath(metaclass=ABCMeta):

    def relax_edge(self, edge):
        start, end = edge.start, edge.end
        if self._dist_to[end] > self._dist_to[start] + edge.weight:
            self._dist_to[end] = self._dist_to[start] + edge.weight
            self._edge_to[end] = edge

    def relax_vertex(self, graph, vertex):
        for edge in graph.adjacent_edges(vertex):
            end = edge.end
            if self._dist_to[end] > self._dist_to[vertex] + edge.weight:
                self._dist_to[end] = self._dist_to[vertex] + edge.weight
                self._edge_to[end] = edge

    def dist_to(self, vertex):
        return self._dist_to[vertex]

    def has_path_to(self, vertex):
        return self._dist_to[vertex] < INFINITE_NUMBER

    def path_to(self, vertex):
        if not self.has_path_to(vertex):
            return None
        path = Stack()
        edge = self._edge_to[vertex]
        while edge:
            path.push(edge)
            edge = self._edge_to[edge.start]
        return path

if __name__ == '__main__':
    doctest.testmod()
