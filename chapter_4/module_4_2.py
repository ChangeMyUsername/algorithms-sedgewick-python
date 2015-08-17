#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import copy
import doctest
from collections import defaultdict
from basic_data_struct import Bag


class Digragh(object):

    """
      Directed graph implementation. Every edges is directed, so if v is
    reachable from w, w might not be reachable from v.There would ba an
    assist data structure to mark all available vertices, because
    self._adj.keys() is only for the vertices which outdegree is not 0.
    Directed graph is almost the same with Undirected graph,many codes
    from Gragh can be reusable.
    >>> graph = Digragh()
    >>> test_data = [(4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
    ...              (11, 12), (12, 9), (9, 10), (9, 11), (8, 9), (10, 12),
    ...              (11, 4), (4, 3), (3, 5), (7, 8), (8, 7), (5, 4), (0, 5),
    ...              (6, 4), (6, 9), (7, 6)]
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> graph.vertex_size()
    13
    >>> graph.edge_size()
    22
    >>> [i for i in graph.get_adjacent_vertices(2)]
    [0, 3]
    >>> [j for j in graph.get_adjacent_vertices(6)]
    [9, 4, 0]
    >>> [v for v in graph.vertices()]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    >>> graph
    13 vertices, 22 edges
    0: 5 1
    2: 0 3
    3: 5 2
    4: 3 2
    5: 4
    6: 9 4 0
    7: 6 8
    8: 7 9
    9: 11 10
    10: 12
    11: 4 12
    12: 9
    <BLANKLINE>
    >>>
    """

    def __init__(self, graph=None):
        self._edge_size = 0
        self._adj = defaultdict(Bag)
        self._vertices = set()

        if graph:
            self._adj = copy.deepcopy(graph._adj)
            self._vertex_size = graph.vertex_size()
            self._edge_size = graph.edge_size()

    def vertex_size(self):
        return len(self._vertices)

    def edge_size(self):
        return self._edge_size

    def add_edge(self, start, end):
        self._vertices.add(start)
        self._vertices.add(end)
        self._adj[start].add(end)
        self._edge_size += 1

    def get_adjacent_vertices(self, vertex):
        return self._adj[vertex]

    def vertices(self):
        return self._vertices

    def reverse(self):
        reverse_graph = Digragh()
        for vertex in self.vertices():
            for adjacent_vertext in self.get_adjacent_vertices(vertex):
                reverse_graph.add_edge(adjacent_vertext, vertex)
        return reverse_graph

    def has_edge(self, start, end):
        edge = next((i for i in self._adj[start] if i == end), None)
        return edge is not None

    def __repr__(self):
        s = str(len(self._vertices)) + ' vertices, ' + str(self._edge_size) + ' edges\n'
        for k in self._adj:
            try:
                lst = ' '.join([vertex for vertex in self._adj[k]])
            except TypeError:
                lst = ' '.join([str(vertex) for vertex in self._adj[k]])
            s += '{}: {}\n'.format(k, lst)
        return s


class DirectedDFS(object):

    """
    """

    def __init__(self, graph, start=None, sources=None):
        self._marked = defaultdict(bool)
        if start:
            self.dfs(graph, start)
        elif sources:
            for vertex in sources:
                if not self._marked[vertex]:
                    self.dfs(graph, vertex)

    def dfs(self, graph, vertex):
        self._marked[vertex] = True
        for adjacent_vertext in graph.get_adjacent_vertices(vertex):
            if not self._marked[adjacent_vertext]:
                self.dfs(graph, adjacent_vertext)

    def marked(self, vertex):
        return self._marked[vertex]

if __name__ == '__main__':
    doctest.testmod()
