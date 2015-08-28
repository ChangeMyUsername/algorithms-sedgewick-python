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
    >>> graph.vertices_size()
    13
    >>> graph.edges_size()
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
        self._edges_size = 0
        self._adj = defaultdict(Bag)
        self._vertices = set()

        # 4.2.3 practice, generate graph from another graph.
        if graph:
            self._adj = copy.deepcopy(graph._adj)
            self._vertices_size = graph.vertices_size()
            self._edges_size = graph.edges_size()
            self._vertices = copy.copy(graph.vertices())

    def vertices_size(self):
        return len(self._vertices)

    def edges_size(self):
        return self._edges_size

    def add_edge(self, start, end):
        # 4.2.5 practice, parallel edge and self cycle are not allowed
        if self.has_edge(start, end) or start == end:
            return
        self._vertices.add(start)
        self._vertices.add(end)
        self._adj[start].add(end)
        self._edges_size += 1

    def get_adjacent_vertices(self, vertex):
        return self._adj[vertex]

    def vertices(self):
        return self._vertices

    def reverse(self):
        reverse_graph = Digragh()
        for vertex in self.vertices():
            for adjacent_vertex in self.get_adjacent_vertices(vertex):
                reverse_graph.add_edge(adjacent_vertex, vertex)
        return reverse_graph

    # 4.2.4 practice, add has_edge method for Digraph
    def has_edge(self, start, end):
        edge = next((i for i in self._adj[start] if i == end), None)
        return edge is not None

    def __repr__(self):
        s = str(len(self._vertices)) + ' vertices, ' + str(self._edges_size) + ' edges\n'
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
        for adjacent_vertex in graph.get_adjacent_vertices(vertex):
            if not self._marked[adjacent_vertex]:
                self.dfs(graph, adjacent_vertex)

    def marked(self, vertex):
        return self._marked[vertex]


class DirectedCycle(object):

    """
      Using Depth-First-Search algorithm to check
    whether a cycle exists in a directed graph.
    There is an assist attribute call _on_stack,
    if an adjacent vertex is in _on_stack(True),
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
      Topological-Sorting implementation. Topological-Sorting
    has to be applied on a directed acyclic graph. If there is
    an edge u->w, then u is before w. This implementation is using
    Depth-First-Search algorithm, for any edge v->w, dfs(w)
    will return before dfs(v), because the input graph should
    not contain any cycle.
      Another Topological-Sorting implementation is using queue to
    enqueue a vertex which indegree is 0. Then dequeue and marked
    it, enqueue all its adjacent vertex util all the vertices in the
    graph is marked. This implementation is not given.
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


class TransitiveClosure(object):

    """
      This class can check if v is reachable
    from w in a directed graph using DirectedDFS.
    The cost of running time is proportional to
    O(V(V + E)), and the cost of space is proportional
    to O(V*V), so this is not a good solution for
    large scale graphs.
    >>> test_data = ((4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
    ...              (11, 12), (12, 9), (9, 10), (9, 11), (7, 9), (10, 12),
    ...              (11, 4), (4, 3), (3, 5), (6, 8), (8, 6), (5, 4), (0, 5),
    ...              (6, 4), (6, 9), (7, 6))
    >>> graph = Digragh()
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> tc = TransitiveClosure(graph)
    >>> tc.reachable(1, 5)
    False
    >>> tc.reachable(1, 0)
    False
    >>> tc.reachable(0, 1)
    True
    >>> tc.reachable(0, 9)
    False
    >>> tc.reachable(8, 12)
    True
    """

    def __init__(self, graph):
        self._all = {}
        for vertex in graph.vertices():
            self._all[vertex] = DirectedDFS(graph, vertex)

    def reachable(self, start, end):
        return self._all[start].marked(end)


# 4.2.7 practice, implement Degrees class
# which compute degrees of vertices in a directed graph.
class Degrees(object):

    """
    >>> test_data = ((4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
    ...              (11, 12), (12, 9), (9, 10), (9, 11), (7, 9), (10, 12),
    ...              (11, 4), (4, 3), (3, 5), (6, 8), (8, 6), (5, 4), (0, 5),
    ...              (6, 4), (6, 9), (7, 6))
    >>> graph = Digragh()
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> degree = Degrees(graph)
    >>> degree.indegree(0)
    2
    >>> degree.outdegree(0)
    2
    >>> degree.indegree(1)
    1
    >>> degree.outdegree(1)
    0
    >>> degree.indegree(9)
    3
    >>> degree.outdegree(9)
    2
    >>> degree.is_map()
    False
    >>> [i for i in degree.sources()]
    []
    """

    def __init__(self, graph):
        self._indegree = defaultdict(int)
        self._outdegree = defaultdict(int)
        length = 0
        for v in graph.vertices():
            length += 1
            for adj in graph.get_adjacent_vertices(v):
                self._indegree[adj] += 1
                self._outdegree[v] += 1

        self._sources = (k for k, v in self._indegree.items() if v == 0)
        self._sinks = (k for k, v in self._outdegree.items() if v == 0)
        self._is_map = len([k for k, v in self._outdegree.items() if v == 1]) == length

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


# 4.2.20 practice, check if euler cycle exists.
class Euler(object):

    """
    >>> test_data = ((4, 2), (2, 3), (3, 2), (6, 0), (0, 1), (2, 0),
    ...              (11, 12), (12, 9), (9, 10), (9, 11), (7, 9), (10, 12),
    ...              (11, 4), (4, 3), (3, 5), (6, 8), (8, 6), (5, 4), (0, 5),
    ...              (6, 4), (6, 9), (7, 6))
    >>> graph = Digragh()
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> euler = Euler(graph)
    >>> euler.is_euler_cycle_exists()
    False
    """

    def __init__(self, graph):
        self._indegree = defaultdict(int)
        self._outdegree = defaultdict(int)
        length = 0
        for v in graph.vertices():
            length += 1
            for adj in graph.get_adjacent_vertices(v):
                self._indegree[adj] += 1
                self._outdegree[v] += 1

        self._euler_cycle_exists = len([k for k, v in self._indegree.items()
                                        if self._outdegree[k] == v]) == length

    def is_euler_cycle_exists(self):
        return self._euler_cycle_exists


# 4.2.24 practice, check if a graph contains hamilton path,
# the following step is very simple and is given in the book.
def hamilton_path_exists(graph):
    """
    >>> test_data = [(2, 3), (0, 6), (0, 1), (2, 0), (11, 12),
    ...              (9, 12), (9, 10), (9, 11), (3, 5), (8, 7),
    ...              (5, 4), (0, 5), (6, 4), (6, 9), (7, 6)]
    >>> graph = Digragh()
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> graph = Digragh()
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> hamilton_path_exists(graph)
    False
    >>> graph_2 = Digragh(graph)
    >>> graph_2.add_edge(7, 2)
    >>> graph_2.add_edge(3, 0)
    >>> graph_2.add_edge(12, 1)
    >>> graph_2.add_edge(1, 5)
    >>> graph_2.add_edge(10, 11)
    >>> hamilton_path_exists(graph_2)
    True
    """

    ts = Topological(graph)
    vertices = [v for v in ts.order()]
    has_path = True
    for i in range(len(vertices) - 1):
        if not graph.has_edge(vertices[i], vertices[i+1]):
            has_path = False
    return has_path


# 4.2.25 practice
def unique_topologial_sort_order(graph):
    return hamilton_path_exists(graph)


# 4.2.30 practice, see http://algs4.cs.princeton.edu/42digraph/TopologicalX.java.html.
class TopologicalWithDegree(object):

    """
    >>> test_data = [(2, 3), (0, 6), (0, 1), (2, 0), (11, 12),
    ...              (9, 12), (9, 10), (9, 11), (3, 5), (8, 7),
    ...              (5, 4), (0, 5), (6, 4), (6, 9), (7, 6)]
    >>> graph = Digragh()
    >>> for a, b in test_data:
    ...     graph.add_edge(a, b)
    ...
    >>> twd = TopologicalWithDegree(graph)
    >>> twd.has_order()
    True
    >>> [v for v in twd.order()]
    [2, 8, 0, 3, 7, 1, 5, 6, 9, 4, 11, 10, 12]
    >>> twd.rank(8)
    1
    >>> twd.rank(10)
    11
    """

    def __init__(self, graph):
        indegree = defaultdict(int)
        self._order = Queue()
        self._rank = defaultdict(int)
        count = 0
        for v in graph.vertices():
            for adj in graph.get_adjacent_vertices(v):
                indegree[adj] += 1
        queue = Queue()
        for v in graph.vertices():
            if indegree[v] == 0:
                queue.enqueue(v)

        while not queue.is_empty():
            vertex = queue.dequeue()
            self._order.enqueue(vertex)
            self._rank[vertex] = count
            count += 1
            for v in graph.get_adjacent_vertices(vertex):
                indegree[v] -= 1
                if indegree[v] == 0:
                    queue.enqueue(v)

        if count != graph.vertices_size():
            self._order = None

        assert self.check(graph)

    def has_order(self):
        return self._order is not None

    def order(self):
        return self._order

    def rank(self, vertex):
        if vertex not in self._rank:
            return -1
        return self._rank[vertex]

    def check(self, graph):
        # digraph is acyclic
        if self.has_order():
            # check that ranks provide a valid topological order
            for vertex in graph.vertices():
                # check that vertex has a rank number
                if vertex not in self._rank:
                    return 1
                for adj in graph.get_adjacent_vertices(vertex):
                    if self._rank[vertex] > self._rank[adj]:
                        return 2
            # check that ranks provide a valid topological order
            for index, v in enumerate(self._order):
                if index != self._rank[v]:
                    return 3
            return True
        return False

if __name__ == '__main__':
    doctest.testmod()
