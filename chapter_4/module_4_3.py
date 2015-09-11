#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import copy
from collections import defaultdict
from basic_data_struct import Bag, Queue, MinPQ, GenericUnionFind
import heapq


class Edge(object):

    """
      Minimum spanning tree edge representation.
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

    def __eq__(self, other):
        return self._weight == other._weight

    def __lt__(self, other):
        return self._weight < other._weight

    def __le__(self, other):
        return self._weight <= other._weight

    def __hash__(self):
        return hash('{} {} {}'.format(self._vertex_a, self._vertex_b, self._weight))

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w):
        self._weight = w

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

    # 4.3.17 practice, implement a method printing out the whole graph.
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


# 4.3.10 practice, implement weighted graph matrix
class WeightedGraphMatrix(object):

    """
    >>> test_data = ((4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 5, 0.32),
    ...              (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19), (0, 2, 0.26), (1, 2, 0.36),
    ...              (1, 3, 0.29), (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58),
    ...              (6, 4, 0.93))
    >>> wgm = WeightedGraphMatrix()
    >>> for a, b, weight in test_data:
    ...    wgm.add_edge(a, b, weight)
    ...
    >>> wgm.edges_size()
    16
    >>> wgm.vertices_size()
    8
    >>> [(5, v, w) for v, w in wgm.adjacent_edges(5).items()]
    [(5, 1, 0.32), (5, 4, 0.35), (5, 7, 0.28)]
    >>> wgm
    8 vertices, 16 edges.
    0: 0-2 0.26, 0-4 0.38, 0-6 0.58, 0-7 0.16
    1: 1-2 0.36, 1-3 0.29, 1-5 0.32, 1-7 0.19
    2: 2-0 0.26, 2-1 0.36, 2-3 0.17, 2-6 0.4, 2-7 0.34
    3: 3-1 0.29, 3-2 0.17, 3-6 0.52
    4: 4-0 0.38, 4-5 0.35, 4-6 0.93, 4-7 0.37
    5: 5-1 0.32, 5-4 0.35, 5-7 0.28
    6: 6-0 0.58, 6-2 0.4, 6-3 0.52, 6-4 0.93
    7: 7-0 0.16, 7-1 0.19, 7-2 0.34, 7-4 0.37, 7-5 0.28
    <BLANKLINE>
    """

    def __init__(self, graph=None):
        self._matrix = defaultdict(dict)
        self._edges_size = 0

    def edges_size(self):
        return self._edges_size

    def vertices_size(self):
        return len(self._matrix.keys())

    def add_edge(self, a, b, weight):
        self._matrix[a][b] = weight
        self._matrix[b][a] = weight
        self._edges_size += 1

    def adjacent_edges(self, vertex):
        return self._matrix[vertex]

    def vertices(self):
        return self._matrix.keys()

    def edges(self):
        result = Bag()
        for v in self.vertices():
            for adj_verx, weight in self.adjacent_edges(v).items():
                if adj_verx != v:
                    result.add((v, adj_verx, weight))
        return result

    def __repr__(self):
        print_string = '{} vertices, {} edges.\n'.format(
            self.vertices_size(), self.edges_size())
        output_edge = '{}-{} {}'
        for v in self.vertices():
            lst = ', '.join([output_edge.format(v, vrtx, w)
                             for vrtx, w in self._matrix[v].items()])
            print_string += '{}: {}\n'.format(v, lst)
        return print_string


class LazyPrimMST(object):

    """
      Lazy version Prim-Minimum-Spanning-Tree. This algorithm is a greedy strategy.
    First input a start vertex, then visit all the adjacent edges, if the other side
    of the vertex is not marked, put the edge into a priority queue. The result queue
    only enqueue those edges with small weight and either vertex is not marked.
    The cost of space is proportional to number of edges, and the worst case of running time
    is proportional to O(ElogE) (E is the number of edges).
    >>> test_data = ((4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 5, 0.32),
    ...              (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19), (0, 2, 0.26), (1, 2, 0.36),
    ...              (1, 3, 0.29), (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58),
    ...              (6, 4, 0.93))
    >>> ewg = EdgeWeightedGraph()
    >>> for a, b, weight in test_data:
    ...    edge = Edge(a, b, weight)
    ...    ewg.add_edge(edge)
    ...
    >>> lazy_prim_mst = LazyPrimMST(ewg, 0)
    >>> lazy_prim_mst.weight()
    1.81
    >>> [edge for edge in lazy_prim_mst.edges()]
    [0-7 0.16, 1-7 0.19, 0-2 0.26, 2-3 0.17, 5-7 0.28, 4-5 0.35, 6-2 0.4]
    """

    def __init__(self, graph, start_vertex):
        self._pq = MinPQ()
        self._marked = defaultdict(bool)
        self._mst = Queue()
        self.visit(graph, start_vertex)
        while not self._pq.is_empty():
            edge = self._pq.del_min()
            a = edge.either()
            b = edge.other(a)
            if self._marked[a] and self._marked[b]:
                continue
            self._mst.enqueue(edge)
            if not self._marked[a]:
                self.visit(graph, a)
            if not self._marked[b]:
                self.visit(graph, b)

    def visit(self, graph, vertex):
        self._marked[vertex] = True
        for edge in graph.adjacent_edges(vertex):
            if not self._marked[edge.other(vertex)]:
                self._pq.insert(edge)

    def edges(self):
        return self._mst

    # 4.3.31 practice, lazy weight implementation
    def weight(self):
        return sum(i.weight for i in self._mst)


class PrimMST(object):

    """
      Prim-Minimum-Spanning-Tree instant version, this python implementation is not efficient
    enough yet.
    >>> test_data = ((4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 5, 0.32),
    ...              (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19), (0, 2, 0.26), (1, 2, 0.36),
    ...              (1, 3, 0.29), (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58),
    ...              (6, 4, 0.93))
    >>> ewg = EdgeWeightedGraph()
    >>> for a, b, weight in test_data:
    ...    edge = Edge(a, b, weight)
    ...    ewg.add_edge(edge)
    ...
    >>> prim_mst = PrimMST(ewg, 0)
    >>> prim_mst.weight()
    1.81
    >>> [edge for edge in prim_mst.edges()]
    [1-7 0.19, 0-2 0.26, 2-3 0.17, 4-5 0.35, 5-7 0.28, 6-2 0.4, 0-7 0.16]
    """

    def __init__(self, graph, start_vertex):
        self._edge_to = {}
        self._dist_to = dict((vertex, 999999999) for vertex in graph.vertices())
        self._marked = defaultdict(bool)
        self._pq = []
        self._dist_to[start_vertex] = 0
        heapq.heappush(self._pq, (0, start_vertex))
        while len(self._pq) != 0:
            self.visit(graph, heapq.heappop(self._pq)[1])

    def visit(self, graph, vertex):
        self._marked[vertex] = True
        for edge in graph.adjacent_edges(vertex):
            other_vertex = edge.other(vertex)
            if self._marked[other_vertex]:
                continue
            if edge.weight < self._dist_to[other_vertex]:
                self._edge_to[other_vertex] = edge
                old_dist = self._dist_to[other_vertex]
                self._dist_to[other_vertex] = edge.weight
                if (old_dist, other_vertex) in self._pq:
                    self._pq.remove((old_dist, other_vertex))
                heapq.heappush(self._pq, (self._dist_to[other_vertex], other_vertex))

    # 4.3.21 practice, the code is given in the book.
    def edges(self):
        return self._edge_to.values()

    # 4.3.31 practice
    def weight(self):
        return round(sum(val for val in self._dist_to.values()), 2)


class KruskalMST(object):

    """
      Kruskal-Minimum-Spanning-Tree algorithm. This is a greedy stategy algorithm. First
    put all edges into the priority queue, then delete the minimum-weight edge in the
    priority queue. Check if those vertices on the both side of the edge is connected.
    If connected, ignore the edge, if not, then use a disjoint set to connect two vertices
    and put the edge into the result. This algorithm is a little bit slower than Prim's algorithm,
    because the cost of connect operation is expensive. The running time of this algorithm
    is proportional to O(ElogE) (E is the number of the edges). And the cost of the space
    is proportional to E.
    >>> test_data = ((4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 5, 0.32),
    ...              (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19), (0, 2, 0.26), (1, 2, 0.36),
    ...              (1, 3, 0.29), (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58),
    ...              (6, 4, 0.93))
    >>> ewg = EdgeWeightedGraph()
    >>> for a, b, weight in test_data:
    ...    edge = Edge(a, b, weight)
    ...    ewg.add_edge(edge)
    ...
    >>> kruskal_mst = KruskalMST(ewg)
    >>> [edge for edge in kruskal_mst.edges()]
    [0-7 0.16, 2-3 0.17, 1-7 0.19, 0-2 0.26, 5-7 0.28, 4-5 0.35, 6-2 0.4]
    >>> kruskal_mst.weight()
    1.81
    """

    def __init__(self, graph):
        self._mst = Queue()
        pq = self._init_priority_queue(graph)
        uf = GenericUnionFind()

        while not pq.is_empty() and self._mst.size() < graph.vertices_size() - 1:
            edge = pq.del_min()
            a = edge.either()
            b = edge.other(a)
            if uf.connected(a, b):
                continue
            uf.union(a, b)
            self._mst.enqueue(edge)

    def _init_priority_queue(self, graph):
        pq = MinPQ()
        for edge in graph.edges():
            pq.insert(edge)
        return pq

    def edges(self):
        return self._mst

    def weight(self):
        return sum(i.weight for i in self._mst)


class DynamicMST(object):

    """
    >>> test_data = ((4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 5, 0.32),
    ...              (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19), (0, 2, 0.26), (1, 2, 0.36),
    ...              (1, 3, 0.29), (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58),
    ...              (6, 4, 0.93))
    >>> ewg = EdgeWeightedGraph()
    >>> for a, b, weight in test_data:
    ...    edge = Edge(a, b, weight)
    ...    ewg.add_edge(edge)
    ...
    >>> dmst = DynamicMST(ewg)
    >>> new_edge = Edge(1, 6, 0.65) # add a new edge that doesn't change the mst result
    >>> ewg.add_edge(new_edge)
    >>> [e for e in dmst.incr_edge(ewg, new_edge)]
    [0-7 0.16, 2-3 0.17, 1-7 0.19, 0-2 0.26, 5-7 0.28, 4-5 0.35, 6-2 0.4]
    >>> new_edge2 = Edge(3, 4, 0.3)
    >>> ewg.add_edge(new_edge2)
    >>> # add a new edge that change the mst result
    >>> # and if the new edge is in the mst, then it must be in the end of the queue.
    >>> [e for e in dmst.incr_edge(ewg, new_edge2)]
    [0-7 0.16, 2-3 0.17, 1-7 0.19, 0-2 0.26, 5-7 0.28, 6-2 0.4, 3-4 0.3]
    >>> # delete edge operation, the edge is not actually deleted
    >>> # delete a edge that is out of the mst
    >>> [e for e in dmst.del_edge(ewg, new_edge)]
    [0-7 0.16, 2-3 0.17, 1-7 0.19, 0-2 0.26, 5-7 0.28, 6-2 0.4, 3-4 0.3]
    >>> # really sad that the order of the edges is not weight-increased
    >>> [e for e in dmst.del_edge(ewg, new_edge2)]
    [0-7 0.16, 2-3 0.17, 1-7 0.19, 0-2 0.26, 5-7 0.28, 6-2 0.4, 4-5 0.35]
    >>> test_data = ((4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 5, 0.32),
    ...              (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19), (0, 2, 0.26), (1, 2, 0.36),
    ...              (1, 3, 0.29), (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58),
    ...              (6, 4, 0.93))
    >>> ewg2 = EdgeWeightedGraph()
    >>> for a, b, weight in test_data:
    ...    edge = Edge(a, b, weight)
    ...    ewg2.add_edge(edge)
    ...
    >>> dmst2 = DynamicMST(ewg2)
    >>> dmst2.edge_add_to_mst(ewg, Edge(1, 6, 0.41))
    False
    >>> dmst2.edge_add_to_mst(ewg, Edge(1, 6, 0.29))
    True
    >>> dmst2.edge_add_to_mst(ewg, Edge(4, 2, 0.3))
    True
    """

    def __init__(self, graph):
        self._mst = Queue()
        pq = self._init_priority_queue(graph)
        uf = GenericUnionFind()

        while not pq.is_empty() and self._mst.size() < graph.vertices_size() - 1:
            edge = pq.del_min()
            a = edge.either()
            b = edge.other(a)
            if uf.connected(a, b):
                continue
            uf.union(a, b)
            self._mst.enqueue(edge)

    def _init_priority_queue(self, graph):
        pq = MinPQ()
        for edge in graph.edges():
            pq.insert(edge)
        return pq

    def _get_max_cycle_edge(self, graph, new_edge):
        # put the new edge into the mst creates a unique cycle
        tmp = Queue(self._mst)
        tmp.enqueue(new_edge)
        mst_query_set = set(tmp)
        cycle = Queue()
        cycle.enqueue([new_edge])

        start_vertex = new_edge.either()
        end_vertex = new_edge.other(start_vertex)

        while start_vertex != end_vertex:
            path = cycle.dequeue()
            last_edge = path[-1]
            a, b = last_edge.either(), last_edge.other(last_edge.either())
            start_vertex = b if a == start_vertex else a
            for edge in graph.adjacent_edges(start_vertex):
                if edge is not new_edge and edge in mst_query_set:
                    path.append(edge)
                    cycle.enqueue(path)
        max_edge = max(cycle.dequeue())
        return max_edge

    # 4.3.16 practice, the solution is similar with 4.3.15
    def edge_add_to_mst(self, graph, new_edge):
        max_cycle_edge = self._get_max_cycle_edge(graph, new_edge)
        return new_edge < max_cycle_edge

    # 4.3.15 practice, the solution is given on the website,
    # see http://algs4.cs.princeton.edu/43mst/
    def incr_edge(self, graph, edge):
        max_cycle_edge = self._get_max_cycle_edge(graph, edge)
        self._mst.enqueue(edge)
        result = Queue([e for e in self._mst if e is not max_cycle_edge])
        self._mst = result
        return result

    # 4.3.14 practice, the solution is given on the website,
    # see http://algs4.cs.princeton.edu/43mst/
    def del_edge(self, graph, edge):

        if edge not in set(self._mst):
            return self._mst

        # init disjoint set with iterable object
        uf = GenericUnionFind([(e.either(), e.other(e.either()))
                               for e in self._mst if e is not edge])

        pq = MinPQ()
        for e in graph.edges():
            if e is not edge:
                pq.insert(e)

        tmp = Queue([e for e in self._mst if e is not edge])

        # find the minimum edge with both vertices is not connected
        while not pq.is_empty():
            min_edge = pq.del_min()
            vertx_a = min_edge.either()
            vertx_b = min_edge.other(vertx_a)

            if uf.connected(vertx_a, vertx_b):
                continue
            # only need one edge
            tmp.enqueue(min_edge)
            break

        self._mst = tmp
        return self._mst

if __name__ == '__main__':
    doctest.testmod()
