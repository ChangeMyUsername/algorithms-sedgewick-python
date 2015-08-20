#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import copy
import doctest
from collections import defaultdict
from basic_data_struct import Bag, Stack, Queue


class Digragh(object):

    """
      Directed graph implementation. Every edges is directed, so if v is
    reachable from w, w might not be reachable from v.There would ba an
    assist data structure to mark all available vertices, because
    self._adj.keys() is only for the vertices which outdegree is not 0.
    Directed graph is almost the same with Undirected graph,many codes
    from Gragh can be reusable.
    >>> # 4.2.6 practice
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

        # 4.2.3 practice, generate graph from another graph.
        if graph:
            self._adj = copy.deepcopy(graph._adj)
            self._vertex_size = graph.vertex_size()
            self._edge_size = graph.edge_size()

    def vertex_size(self):
        return len(self._vertices)

    def edge_size(self):
        return self._edge_size

    def add_edge(self, start, end):
        # 4.2.5 practice, parallel edge and self cycle are not allowed
        if self.has_edge(start, end) or start == end:
            return
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

    # 4.2.4 practice, add has_edge method for Digraph
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
      Depth-First-Search algorithm with directed graph, which can solve directed
    graph reachable problem.
    >>> graph = Digragh()
    >>> test_data = [(4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
    ...              (11, 12), (12, 9), (9, 10), (9, 11), (8, 9), (10, 12),
    ...              (11, 4), (4, 3), (3, 5), (7, 8), (8, 7), (5, 4), (0, 5),
    ...              (6, 4), (6, 9), (7, 6)]
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> dfs = DirectedDFS(graph, 1)
    >>> [i for i in graph.vertices() if dfs.marked(i)]
    [1]
    >>> dfs1 = DirectedDFS(graph, 2)
    >>> [i for i in graph.vertices() if dfs1.marked(i)]
    [0, 1, 2, 3, 4, 5]
    >>> dfs2 = DirectedDFS(graph, 1, 2, 6)
    >>> [i for i in graph.vertices() if dfs2.marked(i)]
    [0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12]
    """

    def __init__(self, graph, *sources):
        self._marked = defaultdict(bool)
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


class DirectedCycle(object):

    """
      Using Depth-First-Search algorithm to check
    whether a cycle exists in a directed graph.
    There is an assist attribute call _on_stack,
    if an adjacent vertext is in _on_stack(True),
    that means a cycle exists.
    >>> graph = Digragh()
    >>> test_data = [(4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
    ...              (11, 12), (12, 9), (9, 10), (9, 11), (8, 9), (10, 12),
    ...              (11, 4), (4, 3), (3, 5), (7, 8), (8, 7), (5, 4), (0, 5),
    ...              (6, 4), (6, 9), (7, 6)]
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> dc = DirectedCycle(graph)
    >>> dc.has_cycle()
    True
    >>> [i for i in dc.cycle()]
    [3, 5, 4, 3]
    """

    def __init__(self, graph):
        self._marked = defaultdict(bool)
        self._edge_to = {}
        self._on_stack = defaultdict(bool)
        self._cycle = Stack()
        for v in graph.vertices():
            if not self._marked[v]:
                self.dfs(graph, v)

    def dfs(self, graph, vertex):
        self._on_stack[vertex] = True
        self._marked[vertex] = True

        for v in graph.get_adjacent_vertices(vertex):
            if self.has_cycle():
                return
            elif not self._marked[v]:
                self._edge_to[v] = vertex
                self.dfs(graph, v)
            elif self._on_stack[v]:
                tmp = vertex
                while tmp != v:
                    self._cycle.push(tmp)
                    tmp = self._edge_to[tmp]
                self._cycle.push(v)
                self._cycle.push(vertex)
        self._on_stack[vertex] = False

    def has_cycle(self):
        return not self._cycle.is_empty()

    def cycle(self):
        return self._cycle


class DepthFirstOrder(object):

    def __init__(self, graph):
        self._pre = Queue()
        self._post = Queue()
        self._reverse_post = Stack()
        self._marked = defaultdict(bool)

        for v in graph.vertices():
            if not self._marked[v]:
                self.dfs(graph, v)

    def dfs(self, graph, vertex):
        self._pre.enqueue(vertex)
        self._marked[vertex] = True
        for v in graph.get_adjacent_vertices(vertex):
            if not self._marked[v]:
                self.dfs(graph, v)

        self._post.enqueue(vertex)
        self._reverse_post.push(vertex)

    def prefix(self):
        return self._pre

    def postfix(self):
        return self._post

    def reverse_postfix(self):
        return self._reverse_post


class Topological(object):

    """
    >>> test_data = [(2, 3), (0, 6), (0, 1), (2, 0), (11, 12),
    ...              (9, 12), (9, 10), (9, 11), (3, 5), (8, 7),
    ...              (5, 4), (0, 5), (6, 4), (6, 9), (7, 6)]
    >>> graph = Digragh()
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> topo = Topological(graph)
    >>> topo.is_DAG()
    True
    >>> [i for i in topo.order()]
    [8, 7, 2, 3, 0, 6, 9, 10, 11, 12, 1, 5, 4]
    """

    def __init__(self, graph):
        cycle_finder = DirectedCycle(graph)
        self._order = None
        if not cycle_finder.has_cycle():
            df_order = DepthFirstOrder(graph)
            self._order = df_order.reverse_postfix()

    def order(self):
        return self._order

    def is_DAG(self):
        return self._order is not None


class KosarajuSCC(object):

    """
    >>> test_data = ((4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
    ...              (11, 12), (12, 9), (9, 10), (9, 11), (7, 9), (10, 12),
    ...              (11, 4), (4, 3), (3, 5), (6, 8), (8, 6), (5, 4), (0, 5),
    ...              (6, 4), (6, 9), (7, 6))
    >>> graph = Digragh()
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> scc = KosarajuSCC(graph)
    >>> count = scc.count()
    >>> output = defaultdict(Queue)
    >>> for v in graph.vertices():
    ...     output[scc.vertex_id(v)].enqueue(v)
    ...
    >>> ['{}: {}'.format(k, ', '.join(map(str, v))) for k, v in output.items()]
    ['0: 1', '1: 0, 2, 3, 4, 5', '2: 9, 10, 11, 12', '3: 6, 8', '4: 7']
    """

    def __init__(self, graph):
        self._marked = defaultdict(bool)
        self._id = {}
        self._count = 0
        order = DepthFirstOrder(graph.reverse())
        for v in order.reverse_postfix():
            if not self._marked[v]:
                self.dfs(graph, v)
                self._count += 1

    def dfs(self, graph, vertex):
        self._marked[vertex] = True
        self._id[vertex] = self._count
        for v in graph.get_adjacent_vertices(vertex):
            if not self._marked[v]:
                self.dfs(graph, v)

    def strongly_connected(self, vertex_1, vertex_2):
        return self._id[vertex_1] == self._id[vertex_2]

    def vertex_id(self, vertex):
        return self._id[vertex]

    def count(self):
        return self._count


# 4.2.7 practice, implement Degrees class
# which compute degrees of vertices in a directed graph.
class Degrees(object):

    def __init__(self, graph):
        self._indegree = defaultdict(int)
        self._outdegree = defaultdict(int)
        for v in graph.vertices():
            for adj in graph.get_adjacent_vertices(v):
                self._indegree[adj] += 1
                self._outdegree[v] += 1

        self._sources = (k for k, v in self._indegree.iteritems() if v == 0)
        self._sinks = (k for k, v in self._outdegree.iteritems() if v == 0)
        self._is_map = any(k for k, v in self._outdegree.iteritems() if v == 1)

    def indegree(self, vertex):
        return self._indegree[vertex]

    def outdegree(self, vertex):
        return self._outdegree[vertex]

    def sources(self):
        return self._sources

    def sinks(self):
        return self._sinks

    def is_map(self):
        return self._is_map

if __name__ == '__main__':
    doctest.testmod()
