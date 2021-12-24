#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import copy
import pprint
from collections import defaultdict
from abc import ABCMeta
from basic_data_struct import Bag, IndexMinPQ, Stack, Topological, Queue

INFINITE_POSITIVE_NUMBER = float('inf')
INFINITE_NEGATIVE_NUMBER = float('-inf')


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
    >>> sorted([v for v in ewd.vertices()])
    [0, 1, 2, 3, 4, 5, 6, 7]
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

    def __init__(self, graph=None):
        self._vertices = set()
        self._edges_size = 0
        self._adj = defaultdict(Bag)

        if graph:
            self._vertices = set(v for v in graph.vertices())
            self._edges_size = graph.edges_size()
            self._adj = copy.deepcopy(graph._adj)

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

    def vertices(self):
        return self._vertices

    def vertices_size(self):
        return len(self._vertices)

    def edges_size(self):
        return self._edges_size

    # 4.4.2 practice
    def __repr__(self):
        print_str = '{} vertices, {} edges\n'.format(
            len(self._vertices), self._edges_size)
        edge_str = '{}->{} {}'
        for v in self._vertices:
            edges = ', '.join(
                edge_str.format(edge.start, edge.end, edge.weight) for edge in self._adj[v])
            print_str += '{}: {}\n'.format(v, edges)
        return print_str


# 4.4.3 practice, implement an adjacent matrix
class EdgeWeightedMatrix(object):

    """
    >>> test_data = ((4, 5, 0.35), (5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28), (7, 5, 0.28),
    ...              (5, 1, 0.32), (0, 4, 0.38), (0, 2, 0.26), (7, 3, 0.39), (1, 3, 0.29),
    ...              (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93))
    >>> ewm = EdgeWeightedMatrix()
    >>> for item in test_data:
    ...     ewm.add_edge(*item)
    ...
    >>> ewm.vertices_size()
    8
    >>> ewm.edges_size()
    15
    >>> ewm.adjacent_edges(5)
    {1: 0.32, 4: 0.35, 7: 0.28}
    >>> ewm.adjacent_edges(7)
    {3: 0.39, 5: 0.28}
    >>> sorted([v for v in ewm.vertices()])
    [0, 1, 2, 3, 4, 5, 6, 7]
    """

    def __init__(self):
        self._adj = defaultdict(dict)
        self._vertices = set()
        self._edges_size = 0

    def add_edge(self, source, dist, weight):
        if not self._adj[source].get(dist, None):
            self._edges_size += 1
        self._adj[source][dist] = weight
        self._vertices.add(source)
        self._vertices.add(dist)

    def adjacent_edges(self, vertex):
        return self._adj[vertex]

    def vertices(self):
        return self._vertices

    def vertices_size(self):
        return len(self._vertices)

    def edges_size(self):
        return self._edges_size

    def edges(self):
        result = Bag()
        for k in self._adj:
            for j in self._adj[k]:
                result.add((k, j, self._adj[k][j]))
        return result


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

    def relax_vertex_lp(self, graph, vertex):
        for edge in graph.adjacent_edges(vertex):
            end = edge.end
            if self._dist_to[end] < self._dist_to[vertex] + edge.weight:
                self._dist_to[end] = self._dist_to[vertex] + edge.weight
                self._edge_to[end] = edge

    def dist_to(self, vertex):
        return self._dist_to[vertex]

    def has_path_to(self, vertex):
        return self._dist_to[vertex] < INFINITE_POSITIVE_NUMBER

    def path_to(self, vertex):
        if not self.has_path_to(vertex):
            return None
        path = Stack()
        edge = self._edge_to[vertex]
        while edge:
            path.push(edge)
            edge = self._edge_to[edge.start]
        return path


class DijkstraSP(ShortestPath):

    """
      Dijkstra Shortest Path algorithm. First reach the source vertex, 'relax' all the adjacent
    edges of the source vertex, and then put all 'relaxed' edges into the priority queue or
    change the distance from the priority queue util the priority queue is empty. The cost of
    running time is proportional to O(ElogV), and the cost of the space is proportional to O(V).
    This algorithm is not applied to the graph with NEGATIVE edges. The worst case still has good
    performance.
    >>> test_data = ((4, 5, 0.35), (5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28), (7, 5, 0.28),
    ...              (5, 1, 0.32), (0, 4, 0.38), (0, 2, 0.26), (7, 3, 0.39), (1, 3, 0.29),
    ...              (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93))
    >>> ewd = EdgeWeightedDigraph()
    >>> for a, b, weight in test_data:
    ...     edge = DirectedEdge(a, b, weight)
    ...     ewd.add_edge(edge)
    ...
    >>> sp = DijkstraSP(ewd, 0)
    >>> [sp.has_path_to(i) for i in range(1, 8)]
    [True, True, True, True, True, True, True]
    >>> [sp.dist_to(i) for i in range(1, 8)]
    [1.05, 0.26, 0.99, 0.38, 0.73, 1.51, 0.6]
    >>> pprint.pprint([[edge for edge in sp.path_to(i)] for i in range(1, 8)])
    [[0->4 0.38, 4->5 0.35, 5->1 0.32],
     [0->2 0.26],
     [0->2 0.26, 2->7 0.34, 7->3 0.39],
     [0->4 0.38],
     [0->4 0.38, 4->5 0.35],
     [0->2 0.26, 2->7 0.34, 7->3 0.39, 3->6 0.52],
     [0->2 0.26, 2->7 0.34]]
    """

    def __init__(self, graph, source):
        self._dist_to = dict((v, INFINITE_POSITIVE_NUMBER) for v in graph.vertices())
        self._edge_to = {}
        self._pq = IndexMinPQ(graph.vertices_size())
        self._pq.insert(source, 0)
        self._edge_to[source] = None
        self._dist_to[source] = 0

        while not self._pq.is_empty():
            self.relax(graph, self._pq.delete_min())

    def relax(self, graph, vertex):
        for edge in graph.adjacent_edges(vertex):
            end = edge.end
            if self._dist_to[end] > self._dist_to[vertex] + edge.weight:
                self._dist_to[end] = round(self._dist_to[vertex] + edge.weight, 2)
                self._edge_to[end] = edge

                if self._pq.contains(end):
                    self._pq.change_key(end, self._dist_to[end])
                else:
                    self._pq.insert(end, self._dist_to[end])


class DijkstraAllPairsSP(object):

    def __init__(self, graph):
        self._all = {}
        for v in graph.vertices():
            self._all[v] = DijkstraSP(graph, v)

    def path(self, source, dest):
        return self._all[source].path_to(dest)

    def dist(self, source, dest):
        return self._all[source].dist_to(dest)


class AcyclicSP(ShortestPath):

    """
      Acyclic Shortest Path algorithm. Apply topological sort and 'relax'
    all the adjacent edges of the vertices in the topological order. This
    algorithm is not applied to the graph with cycle (topological). This
    algorithm can solve task schedule problems. The cost running time is
    proportional to O(E + V), which is linear and much faster than Dijkstra's
    one.
    >>> test_data = ((5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28),
    ...              (5, 1, 0.32), (4, 0, 0.38), (0, 2, 0.26), (3, 7, 0.39), (1, 3, 0.29),
    ...              (7, 2, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93))
    >>> ewd = EdgeWeightedDigraph()
    >>> for a, b, weight in test_data:
    ...     edge = DirectedEdge(a, b, weight)
    ...     ewd.add_edge(edge)
    ...
    >>> sp = AcyclicSP(ewd, 5)
    >>> [sp.has_path_to(i) for i in range(1, 8)]
    [True, True, True, True, True, True, True]
    >>> pprint.pprint([[edge for edge in sp.path_to(i)] for i in range(8)])
    [[5->4 0.35, 4->0 0.38],
     [5->1 0.32],
     [5->7 0.28, 7->2 0.34],
     [5->1 0.32, 1->3 0.29],
     [5->4 0.35],
     [],
     [5->1 0.32, 1->3 0.29, 3->6 0.52],
     [5->7 0.28]]
    """

    def __init__(self, graph, source):
        self._dist_to = dict((v, INFINITE_POSITIVE_NUMBER) for v in graph.vertices())
        self._edge_to = {}
        self._edge_to[source] = None
        self._dist_to[source] = 0
        topo = Topological(graph)

        for v in topo.order():
            self.relax_vertex(graph, v)


# 4.4.28 practice
class AcyclicLP(ShortestPath):

    """
    >>> test_data = ((5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28),
    ...              (5, 1, 0.32), (4, 0, 0.38), (0, 2, 0.26), (3, 7, 0.39), (1, 3, 0.29),
    ...              (7, 2, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93))
    >>> ewd = EdgeWeightedDigraph()
    >>> for a, b, weight in test_data:
    ...     edge = DirectedEdge(a, b, weight)
    ...     ewd.add_edge(edge)
    ...
    >>> lp = AcyclicLP(ewd, 5)
    >>> [lp.has_path_to(i) for i in range(1, 8)]
    [True, True, True, True, True, True, True]
    >>> pprint.pprint([[edge for edge in lp.path_to(i)] for i in range(8)])
    [[5->1 0.32, 1->3 0.29, 3->6 0.52, 6->4 0.93, 4->0 0.38],
     [5->1 0.32],
     [5->1 0.32, 1->3 0.29, 3->6 0.52, 6->4 0.93, 4->7 0.37, 7->2 0.34],
     [5->1 0.32, 1->3 0.29],
     [5->1 0.32, 1->3 0.29, 3->6 0.52, 6->4 0.93],
     [],
     [5->1 0.32, 1->3 0.29, 3->6 0.52],
     [5->1 0.32, 1->3 0.29, 3->6 0.52, 6->4 0.93, 4->7 0.37]]
    """

    def __init__(self, graph, source):
        self._dist_to = dict((v, INFINITE_NEGATIVE_NUMBER) for v in graph.vertices())
        self._dist_to[source] = 0
        self._edge_to = {source: None}

        topo = Topological(graph)

        for v in topo.order():
            self.relax_vertex_lp(graph, v)


class EdgeWeightedDirectedCycle(object):

    def __init__(self, graph):
        self._mark = defaultdict(bool)
        self._on_stack = defaultdict(bool)
        self._edge_to = {}
        self._cycle = None

        for v in graph.vertices():
            if not self._mark[v]:
                self.dfs(graph, v)

    def dfs(self, graph, vertex):
        self._on_stack[vertex] = True
        self._mark[vertex] = True

        for edge in graph.adjacent_edges(vertex):
            end = edge.end
            if not self._mark[end]:
                self._edge_to[end] = edge
                self.dfs(graph, end)
            elif self._on_stack[end]:
                self._cycle = Stack()
                while edge.start != end:
                    self._cycle.push(edge)
                    edge = self._edge_to[edge.start]
                self._cycle.push(edge)

        self._on_stack[vertex] = False

    def has_cycle(self):
        return self._cycle is not None

    def cycle(self):
        return self._cycle


class BellmanFordSP(ShortestPath):

    """
      BellmanFord Shortest Path algorithm. This version is not a traditional one,
    it's a queue-based version. First enqueue the source vertex, and dequeue the vertex,
    'relax' all adjacent edges and put the adjacent vertices into the queue until the queue
    is empty or find the negative cycle. A negative cycle check is nessesary every V times
    relaxation.The cost of running time is proportional to O(V + E), the worst case is VE.
    This is a universal algorithm for Shortest Path algorithm.
    >>> test_data = ((4, 5, 0.35), (5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28), (7, 5, 0.28),
    ...              (5, 1, 0.32), (0, 4, 0.38), (0, 2, 0.26), (7, 3, 0.39), (1, 3, 0.29),
    ...              (2, 7, 0.34), (6, 2, -1.2), (3, 6, 0.52), (6, 0, -1.4), (6, 4, -1.25))
    >>> ewd = EdgeWeightedDigraph()
    >>> for a, b, weight in test_data:
    ...     edge = DirectedEdge(a, b, weight)
    ...     ewd.add_edge(edge)
    ...
    >>> sp = BellmanFordSP(ewd, 0)
    >>> [sp.has_path_to(i) for i in range(8)]
    [True, True, True, True, True, True, True, True]
    >>> sp._has_negative_cycle()
    False
    >>> [edge for edge in sp.path_to(7)]
    [0->2 0.26, 2->7 0.34]
    >>> [edge for edge in sp.path_to(4)]
    [0->2 0.26, 2->7 0.34, 7->3 0.39, 3->6 0.52, 6->4 -1.25]
    """

    def __init__(self, graph, source):
        self._dist_to = dict((v, INFINITE_POSITIVE_NUMBER) for v in graph.vertices())
        self._dist_to[source] = 0

        self._edge_to = {source: None}

        self._queue = Queue()
        self._queue.enqueue(source)
        self._on_queue = defaultdict(bool)
        self._on_queue[source] = True

        self._cost = 0
        self._cycle = None

        while not self._queue.is_empty() and not self._has_negative_cycle():
            vertex = self._queue.dequeue()
            self._on_queue[vertex] = False
            self.relax(graph, vertex)

        assert self.check(graph, source)

    def relax(self, graph, vertex):
        for edge in graph.adjacent_edges(vertex):
            end = edge.end

            if self._dist_to[end] > self._dist_to[vertex] + edge.weight:
                self._dist_to[end] = round(self._dist_to[vertex] + edge.weight, 2)
                self._edge_to[end] = edge
                if not self._on_queue[end]:
                    self._queue.enqueue(end)
                    self._on_queue[end] = True

            if self._cost % graph.vertices_size() == 0:
                self._find_negative_cycle(graph)
            self._cost += 1

    def _find_negative_cycle(self, graph):
        spt = EdgeWeightedDigraph()
        for v in graph.vertices():
            if self._edge_to.get(v, None):
                spt.add_edge(self._edge_to[v])

        cf = EdgeWeightedDirectedCycle(spt)
        self._cycle = cf.cycle()

    def _has_negative_cycle(self):
        return self._cycle is not None

    def negative_cycle(self):
        return self._cycle

    def check(self, graph, source):
        # if negative cycle exists, check the total weight of the negative cycle is negative.
        if self._has_negative_cycle():
            if sum(e.weight for e in self.negative_cycle()) >= 0:
                print('positive weight from negative cycle')
                return False
        # no negative cycle
        else:
            # check vertex self._dist_to[v] and self._edge_to[v] are consistent
            if self._dist_to[source] != 0 or self._edge_to[source] is not None:
                print('the distance and edge_to of source vertex inconsistent')
                return False

            for v in graph.vertices():
                if v == source:
                    continue
                if self._edge_to[v] is None and self._dist_to[v] != INFINITE_POSITIVE_NUMBER:
                    print('the distance and edge_to of {} inconsistent'.format(v))
                    return False

            # check each edge is relaxed
            for v in graph.vertices():
                for e in graph.adjacent_edges(v):
                    if round(self._dist_to[v] + e.weight, 2) < self._dist_to[e.end]:
                        print('edge {} is not relaxed'.format(e))
                        return False

            # check that all edges e = v->w on SPT satisfy distTo[w] == distTo[v] + e.weight()
            for v in graph.vertices():
                if self._edge_to[v] is None:
                    continue
                edge = self._edge_to[v]
                if v != edge.end:
                    print('here')
                    return False
                if round(self._dist_to[edge.start] + edge.weight, 2) != self._dist_to[v]:
                    print('edge {} on shortest path not tight'.format(edge))
                    return False

        return True


# 4.4.24 practice, implement multiple sources DijkstraSP, the solution is given on the book.
class DijkstraMultipleSourcesSP(ShortestPath):

    """
    >>> test_data = ((4, 5, 0.35), (5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28), (7, 5, 0.28),
    ...              (5, 1, 0.32), (0, 4, 0.38), (0, 2, 0.26), (7, 3, 0.39), (1, 3, 0.29),
    ...              (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93))
    >>> ewd = EdgeWeightedDigraph()
    >>> for a, b, weight in test_data:
    ...     edge = DirectedEdge(a, b, weight)
    ...     ewd.add_edge(edge)
    ...
    >>> sp = DijkstraMultipleSourcesSP(ewd, (0, 6))
    >>> [sp.has_path_to(i) for i in range(1, 8)]
    [True, True, True, True, True, True, True]
    """

    def __init__(self, graph, sources):
        tmp = EdgeWeightedDigraph(graph)
        for v in sources:
            tmp.add_edge(DirectedEdge(-1, v, 0))

        self._dist_to = dict((v, INFINITE_POSITIVE_NUMBER) for v in tmp.vertices())
        self._edge_to = {}
        self._pq = IndexMinPQ(tmp.vertices_size())
        self._pq.insert(-1, 0)
        self._edge_to[-1] = None
        self._dist_to[-1] = 0
        self._sources = (i for i in sources)

        while not self._pq.is_empty():
            self.relax(tmp, self._pq.delete_min())

    def relax(self, graph, vertex):
        for edge in graph.adjacent_edges(vertex):
            end = edge.end
            if self._dist_to[end] > self._dist_to[vertex] + edge.weight:
                self._dist_to[end] = round(self._dist_to[vertex] + edge.weight, 2)
                self._edge_to[end] = edge

                if self._pq.contains(end):
                    self._pq.change_key(end, self._dist_to[end])
                else:
                    self._pq.insert(end, self._dist_to[end])

    def dist(self, source, dist):
        if source not in self._sources:
            return None
        return self.dist_to(dist)


# 4.4.26 practice, imeplement adjacent matrix version of dijkstra shortest path
class DijkstraMatrixSP(ShortestPath):

    """
    >>> test_data = ((4, 5, 0.35), (5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28), (7, 5, 0.28),
    ...              (5, 1, 0.32), (0, 4, 0.38), (0, 2, 0.26), (7, 3, 0.39), (1, 3, 0.29),
    ...              (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93))
    >>> ewm = EdgeWeightedMatrix()
    >>> for a, b, weight in test_data:
    ...     ewm.add_edge(a, b, weight)
    ...
    >>> sp = DijkstraMatrixSP(ewm, 0)
    >>> [sp.has_path_to(i) for i in range(1, 8)]
    [True, True, True, True, True, True, True]
    >>> [sp.dist_to(i) for i in range(1, 8)]
    [1.05, 0.26, 0.99, 0.38, 0.73, 1.51, 0.6]
    >>> [e for e in sp.path_to(7)]
    [(0, 2, 0.26), (2, 7, 0.34)]
    >>> [e for e in sp.path_to(6)]
    [(0, 2, 0.26), (2, 7, 0.34), (7, 3, 0.39), (3, 6, 0.52)]
    """

    def __init__(self, graph, source):
        self._dist_to = dict((v, INFINITE_POSITIVE_NUMBER) for v in graph.vertices())
        self._dist_to[source] = 0
        self._edge_to = {source: None}
        self._pq = IndexMinPQ(graph.vertices_size())
        self._pq.insert(source, 0)

        while not self._pq.is_empty():
            self.relax(graph, self._pq.delete_min())

    def relax(self, graph, vertex):
        for v, weight in graph.adjacent_edges(vertex).items():
            if self._dist_to[v] > self._dist_to[vertex] + weight:
                self._dist_to[v] = round(self._dist_to[vertex] + weight, 2)
                self._edge_to[v] = (vertex, v, weight)

                if self._pq.contains(v):
                    self._pq.change_key(v, self._dist_to[v])
                else:
                    self._pq.insert(v, self._dist_to[v])

    def path_to(self, vertex):
        if not self.has_path_to(vertex):
            return None
        path = Stack()
        edge = self._edge_to[vertex]
        while edge:
            path.push(edge)
            edge = self._edge_to[edge[0]]
        return path

if __name__ == '__main__':
    doctest.testmod()
