#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import copy
import doctest
import random
from collections import defaultdict
from basic_data_struct import Bag, Queue, Stack


class Graph(object):

    """
      Undirected graph implementation. The cost of space is proportional to O(V + E)
    (V is the number of vertices and E is the number of edges). Adding
    an edge only takes constant time. The running time of
    Checking if node v is adjacent to w and traveling all adjacent point of v
    is related to the degree of v. This implementation supports multiple
    input data types(immutable).
    TODO: Test file input.
    >>> g = Graph()
    >>> test_data = [(0, 5), (4, 3), (0, 1), (9, 12), (6, 4), (5, 4), (0, 2),  # from book tinyG.txt
    ...              (11, 12), (9, 10), (0, 6), (7, 8), (9, 11), (5, 3)]
    >>> for a, b in test_data:
    ...     g.add_edge(a, b)
    ...
    >>> g.vertex_size()
    13
    >>> len(test_data) == g.edge_size()
    True
    >>> adjacent_vertices = ' '.join([str(v) for v in g.get_adjacent_vertices(0)])
    >>> adjacent_vertices
    '6 2 1 5'
    >>> g.degree(0)
    4
    >>> g.degree(9)
    3
    >>> g.max_degree()
    4
    >>> g.number_of_self_loops()
    0
    >>> g
    13 vertices, 13 edges
    0: 6 2 1 5
    1: 0
    2: 0
    3: 5 4
    4: 5 6 3
    5: 3 4 0
    6: 0 4
    7: 8
    8: 7
    9: 11 10 12
    10: 9
    11: 9 12
    12: 11 9
    <BLANKLINE>
    >>> g2 = Graph(graph=g)
    >>> g2.add_edge(4, 9)
    >>> g.has_edge(4, 9)
    False
    >>> g2.has_edge(4, 9)
    True
    >>> g2.has_edge(9, 4)
    True
    >>> g2.add_edge(4, 9)
    >>> [i for i in g2.get_adjacent_vertices(4)]
    [9, 5, 6, 3]
    """

    def __init__(self, input_file=None, graph=None):
        self._vertex_size = 0
        self._edge_size = 0
        self._adj = defaultdict(Bag)

        # this is not tested yet.
        if input_file:
            with open(input_file) as f:
                lines = [l.rstrip('\n') for l in f]
                self._vertex_size = int(lines[0])
                self._edge_size = int(lines[1])
                for i in range(1, self._edge_size):
                    a, b = lines[i].split()
                    self.add_edge(a, b)
        # 4.1.3 practice, add a graph parameter for constructor method.
        elif graph:
            self._adj = copy.deepcopy(graph._adj)
            self._vertex_size = graph.vertex_size()
            self._edge_size = graph.edge_size()

    def vertex_size(self):
        if not self._vertex_size:
            return len(self._adj.keys())
        return self._vertex_size

    def edge_size(self):
        return self._edge_size

    def add_edge(self, vertext_a, vertext_b):
        # 4.1.5 practice, no self cycle or parallel edges.
        if self.has_edge(vertext_a, vertext_b) or vertext_a == vertext_b:
            return
        self._adj[vertext_a].add(vertext_b)
        self._adj[vertext_b].add(vertext_a)

        self._edge_size += 1

    # 4.1.4 practice, add has_edge method
    def has_edge(self, vertext_a, vertext_b):
        if vertext_a not in self._adj or vertext_b not in self._adj:
            return False
        edge = next((i for i in self._adj[vertext_a] if i == vertext_b), None)
        return edge is not None

    def get_adjacent_vertices(self, vertex):
        return self._adj[vertex]

    def vertices(self):
        return self._adj.keys()

    def degree(self, vertex):
        assert vertex in self._adj
        return self._adj[vertex].size()

    def max_degree(self):
        result = 0
        for vertex in self._adj:
            v_degree = self.degree(vertex)
            if v_degree > result:
                result = v_degree
        return result

    def avg_degree(self):
        return float(2 * self._edge_size) / self._vertex_size

    def number_of_self_loops(self):
        count = 0
        for k in self._adj:
            for vertex in self._adj[k]:
                if vertex == k:
                    count += 1
        return int(count / 2)

    # 4.1.31 check the number of parallel edges with linear running time.
    def number_of_parallel_edges(self):
        count = 0
        for k in self._adj:
            tmp = set()
            for vertex in self._adj[k]:
                if vertex not in tmp:
                    tmp.add(vertex)
                else:
                    count += 1
        return int(count / 2)

    def __repr__(self):
        s = str(self.vertex_size()) + ' vertices, ' + str(self._edge_size) + ' edges\n'
        for k in self._adj:
            try:
                lst = ' '.join([vertex for vertex in self._adj[k]])
            except TypeError:
                lst = ' '.join([str(vertex) for vertex in self._adj[k]])
            s += '{}: {}\n'.format(k, lst)
        return s


class DepthFirstPaths(object):

    """
      Undirected graph depth-first searching algorithms implementation.
    Depth-First-Search recurvisely reaching all vertices that are adjacent to it,
    and then treat these adjacent_vertices as start_vertex and searching again util all the
    connected vertices is marked.
    >>> g = Graph()
    >>> test_data = [(0, 5), (2, 4), (2, 3), (1, 2), (0, 1), (3, 4), (3, 5), (0, 2)]
    >>> for a, b in test_data:
    ...     g.add_edge(a, b)
    ...
    >>> dfp = DepthFirstPaths(g,  0)
    >>> [dfp.has_path_to(i) for i in range(6)]
    [True, True, True, True, True, True]
    >>> [i for i in dfp.path_to(4)]
    [0, 2, 3, 4]
    >>> [i for i in dfp.path_to(1)]
    [0, 2, 1]
    """

    def __init__(self, graph, start_vertex):
        self._marked = defaultdict(bool)
        self._edge_to = {}
        self._start = start_vertex
        self.dfs(graph, self._start)

    def dfs(self, graph, vertex):
        self._marked[vertex] = True

        for v in graph.get_adjacent_vertices(vertex):
            if not self._marked[v]:
                self._edge_to[v] = vertex
                self.dfs(graph, v)

    def has_path_to(self, vertex):
        return self._marked[vertex]

    def vertices_size(self):
        return len(self._marked.keys())

    def path_to(self, vertex):
        if not self.has_path_to(vertex):
            return None

        tmp = vertex
        path = Stack()
        while tmp != self._start:
            path.push(tmp)
            tmp = self._edge_to[tmp]
        path.push(self._start)
        return path


class BreadthFirstPaths(object):

    """
      Breadth-First-Search algorithm implementation. This algorithm
    uses queue as assist data structure. First enqueue the start_vertex,
    marked it as visited and dequeue the vertex, then marked all the
    adjacent vertices of start_vertex and enqueue them. Continue this process
    util all connected vertices are marked.
      With Breadth-First-Search algorithm, we can find the shortest path from x to y.
    The worst scenario of running time is proportional to O(V + E) (V is the number
    of vertices and E is the number of edges).
    >>> g = Graph()
    >>> test_data = [(0, 5), (2, 4), (2, 3), (1, 2), (0, 1), (3, 4), (3, 5), (0, 2)]
    >>> for a, b in test_data:
    ...     g.add_edge(a, b)
    ...
    >>> bfp = BreadthFirstPaths(g, 0)
    >>> [bfp.has_path_to(i) for i in range(6)]
    [True, True, True, True, True, True]
    >>> [i for i in bfp.path_to(4)]
    [0, 2, 4]
    >>> [i for i in bfp.path_to(5)]
    [0, 5]
    >>> bfp.dist_to(4)
    2
    >>> bfp.dist_to(5)
    1
    >>> bfp.dist_to('not a vertex')
    -1
    """

    def __init__(self, graph, start_vertex):
        self._marked = defaultdict(bool)
        self._edge_to = {}

        self._start = start_vertex
        self._dist = {start_vertex: 0}
        self.bfs(graph, self._start)

    def bfs(self, graph, vertex):
        queue = Queue()
        self._marked[vertex] = True
        queue.enqueue(vertex)
        while not queue.is_empty():
            tmp = queue.dequeue()
            for v in graph.get_adjacent_vertices(tmp):
                if not self._marked[v]:
                    self._edge_to[v] = tmp
                    self._dist[v] = self._dist[tmp] + 1
                    self._marked[v] = True
                    queue.enqueue(v)

    def has_path_to(self, vertex):
        return self._marked[vertex]

    def path_to(self, vertex):
        if not self.has_path_to(vertex):
            return None

        tmp = vertex
        path = Stack()
        while tmp != self._start:
            path.push(tmp)
            tmp = self._edge_to[tmp]
        path.push(self._start)
        return path

    # 4.1.13 practice, implement dist_to method which only takes constant time.
    def dist_to(self, vertex):
        return self._dist.get(vertex, -1)

    def max_distance(self):
        return max(self._dist.values())


class ConnectedComponent(object):

    """
      Construct connected components using Depth-First-Search algorithm.
    Using this algorithm we need to construct all the connected components
    from the beginning which the cost of running time and space are both
    proportional to O(V + E). But it takes only constant time for querying
    if two vertices are connected.
    >>> g = Graph()
    >>> test_data = [(0, 5), (4, 3), (0, 1), (9, 12), (6, 4), (5, 4), (0, 2),
    ...              (11, 12), (9, 10), (0, 6), (7, 8), (9, 11), (5, 3)]
    >>> for a, b in test_data:
    ...     g.add_edge(a, b)
    ...
    >>> cc = ConnectedComponent(g)
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

        for s in graph.vertices():
            if not self._marked[s]:
                self.dfs(graph, s)
                self._count += 1

    def dfs(self, graph, vertex):
        self._marked[vertex] = True
        self._id[vertex] = self._count
        for s in graph.get_adjacent_vertices(vertex):
            if not self._marked[s]:
                self.dfs(graph, s)

    def connected(self, vertex_1, vertex_2):
        return self._id[vertex_1] == self._id[vertex_2]

    def vertex_id(self, vertex):
        return self._id[vertex]

    def count(self):
        return self._count


class Cycle(object):

    """
    Using Depth-First-Search algorithm to check whether a graph has a cycle.
    if a graph is tree-like structure(no cycle), then has_cycle is never reached.
    >>> g = Graph()
    >>> test_data = [(0, 1), (0, 2), (0, 6), (0, 5), (3, 5), (6, 4)]
    >>> for a, b in test_data:
    ...     g.add_edge(a, b)
    ...
    >>> cycle = Cycle(g)
    >>> cycle.has_cycle()
    False
    >>> g2 = Graph()
    >>> has_cycle_data = [(0, 1), (0, 2), (0, 6), (0, 5), (3, 5), (6, 4), (3, 4)]
    >>> for a, b in has_cycle_data:
    ...     g2.add_edge(a, b)
    ...
    >>> cycle2 = Cycle(g2)
    >>> cycle2.has_cycle()
    True
    """

    def __init__(self, graph):
        self._marked = defaultdict(bool)
        self._has_cycle = False
        for vertex in graph.vertices():
            if not self._marked[vertex]:
                self.dfs(graph, vertex, vertex)

    def dfs(self, graph, vertex_1, vertex_2):
        self._marked[vertex_1] = True
        for adj in graph.get_adjacent_vertices(vertex_1):
            if not self._marked[adj]:
                self.dfs(graph, adj, vertex_1)
            else:
                if adj != vertex_2:
                    self._has_cycle = True

    def has_cycle(self):
        return self._has_cycle


class TwoColor(object):

    """
    Using Depth-First-Search algorithm to solve Two-Color problems.
    >>> g = Graph()
    >>> test_data = [(0, 5), (2, 4), (2, 3), (1, 2), (0, 1), (3, 4), (3, 5), (0, 2)]
    >>> for a, b in test_data:
    ...     g.add_edge(a, b)
    ...
    >>> tc = TwoColor(g)
    >>> tc.is_bipartite()
    False
    """

    def __init__(self, graph):
        self._marked = defaultdict(bool)
        self._color = defaultdict(bool)
        self._is_twocolorable = True

        for vertex in graph.vertices():
            if not self._marked[vertex]:
                self.dfs(graph, vertex)

    def dfs(self, graph, vertex):
        self._marked[vertex] = True
        for v in graph.get_adjacent_vertices(vertex):
            if not self._marked[v]:
                self._color[v] = self._color[vertex]
                self.dfs(graph, v)
            else:
                if self._color[v] == self._color[vertex]:
                    self._is_twocolorable = False

    def is_bipartite(self):
        return self._is_twocolorable


# 4.1.16 practice, implement GraphProperties class.
class GraphProperties(object):

    """
    >>> g = Graph()
    >>> test_data = [(0, 5), (2, 4), (2, 3), (1, 2), (0, 1), (3, 4), (3, 5), (0, 2)]
    >>> for a, b in test_data:
    ...     g.add_edge(a, b)
    ...
    >>> gp = GraphProperties(g)
    >>> gp.eccentricity(0)
    2
    >>> gp.eccentricity(1)
    2
    >>> gp.diameter()
    2
    >>> gp.radius()
    2
    """

    def __init__(self, graph):
        self._eccentricities = {}
        self._diameter = 0
        self._radius = 9999999999
        dfp = DepthFirstPaths(graph, random.sample(graph.vertices(), 1)[0])
        if dfp.vertices_size() != graph.vertex_size():
            raise Exception('graph is not connected.')

        for vertex in graph.vertices():
            bfp = BreadthFirstPaths(graph, vertex)
            dist = bfp.max_distance()
            if dist < self._radius:
                self._radius = dist
            if dist > self._diameter:
                self._diameter = dist
            self._eccentricities[vertex] = dist

    def eccentricity(self, vertex):
        return self._eccentricities.get(vertex, -1)

    def diameter(self):
        return self._diameter

    def radius(self):
        return self._radius

    def center(self):
        centers = [k for k, v in self._eccentricities.items() if v == self._radius]
        random.shuffle(centers)
        return centers[0]

    # 4.1.17 practice
    def girth(self):
        pass


if __name__ == '__main__':
    doctest.testmod()
