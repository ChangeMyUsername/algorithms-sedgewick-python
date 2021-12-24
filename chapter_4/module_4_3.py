#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import copy
from collections import defaultdict
from basic_data_struct import Bag, Queue, MinPQ, GenericUnionFind, MaxPQ, IndexMinPQ


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
        result = set()
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
        result = set()
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


# 4.3.28 practice, using primitive data structure with EdgeWeightedGraph
class WeightedGraph(object):

    """
    >>> test_data = ((0.35, 4, 5), (0.37, 4, 7), (0.28, 5, 7), (0.16, 0, 7), (0.32, 1, 5),
    ...              (0.38, 0, 4), (0.17, 2, 3), (0.19, 1, 7), (0.26, 0, 2), (0.36, 1, 2),
    ...              (0.29, 1, 3), (0.34, 2, 7), (0.4, 6, 2), (0.52, 3, 6), (0.58, 6, 0),
    ...              (0.93, 6, 4))
    >>> wg = WeightedGraph()
    >>> for edge in test_data:
    ...     wg.add_edge(edge)
    ...
    >>> wg.edges_size()
    16
    >>> wg.vertices_size()
    8
    >>> [(a, b, w) for w, a, b in wg.adjacent_edges(5)]
    [(4, 5, 0.35), (5, 7, 0.28), (1, 5, 0.32)]
    >>> [(a, b, w) for w, a, b in wg.adjacent_edges(7)]
    [(4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 7, 0.19), (2, 7, 0.34)]
    """

    def __init__(self):
        self._adj = defaultdict(list)
        self._edges_size = 0

    def add_edge(self, edge):
        self._adj[edge[1]].append(edge)
        self._adj[edge[2]].append(edge)
        self._edges_size += 1

    def vertices_size(self):
        return len(self._adj.keys())

    def edges_size(self):
        return self._edges_size

    def adjacent_edges(self, vertex):
        return self._adj[vertex]

    def vertices(self):
        return self._adj.keys()

    def edges(self):
        result = set()
        for v in self.vertices():
            for a, b, weight in self.adjacent_edges(v):
                if a != b:
                    result.add((a, b, weight))
        return result


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
      Prim-Minimum-Spanning-Tree instant version. Put the start_vertex and 0 weight into the
    index minimum priority queue. Then check all adjacent vertices, if the adjacent vertex is
    checked before, ignore it; otherwise update the distance between the current vertex and the
    start vertex. The cost of space is proportional to O(V), and the cost of running time is
    proportional to O(ElogV)
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
        self._pq = IndexMinPQ(graph.vertices_size())
        self._dist_to[start_vertex] = 0
        self._pq.insert(start_vertex, 0.0)
        while len(self._pq) != 0:
            self.visit(graph, self._pq.delete_min())

    def visit(self, graph, vertex):
        self._marked[vertex] = True
        for edge in graph.adjacent_edges(vertex):
            other_vertex = edge.other(vertex)
            if self._marked[other_vertex]:
                continue
            if edge.weight < self._dist_to[other_vertex]:
                self._edge_to[other_vertex] = edge
                self._dist_to[other_vertex] = edge.weight

                if self._pq.contains(other_vertex):
                    self._pq.change_key(other_vertex, self._dist_to[other_vertex])
                else:
                    self._pq.insert(other_vertex, self._dist_to[other_vertex])

    # 4.3.21 practice, the code is given in the book.
    def edges(self):
        return self._edge_to.values()

    # 4.3.31 practice
    def weight(self):
        return round(sum(val for val in self._dist_to.values()), 2)


class KruskalMST(object):

    """
      Kruskal-Minimum-Spanning-Tree algorithm. This is a greedy strategy algorithm. First
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


class EdgeConnectedComponent(object):

    """
    >>> g = EdgeWeightedGraph()
    >>> test_data = [(0, 5, 0.28), (4, 3, 0.88), (0, 1, 0.2), (9, 12, 0.95),
    ...              (6, 4, 0.47), (5, 4, 0.74), (0, 2, 0.43),
    ...              (11, 12, 0.57), (9, 10, 0.03), (0, 6, 0.86),
    ...              (7, 8, 0.23), (9, 11, 0.32), (5, 3, 0.46)]
    >>> for a, b, w in test_data:
    ...     e = Edge(a, b, w)
    ...     g.add_edge(e)
    ...
    >>> ecc = EdgeConnectedComponent(g)
    >>> ecc.connected(0, 8)
    False
    >>> ecc.connected(0, 4)
    True
    >>> ecc.connected(0, 9)
    False
    >>> ecc.count()
    3
    >>> sorted([comp for comp in ecc.get_components()])
    [[0, 1, 2, 3, 4, 5, 6], [7, 8], [9, 10, 11, 12]]
    """

    def __init__(self, graph):
        self._marked = defaultdict(bool)
        self._id = defaultdict(int)
        self._count = 0

        for edge in graph.edges():
            if not self._marked[edge.either()]:
                self.dfs(graph, edge.either())
                self._count += 1

    def dfs(self, graph, vertex):
        self._marked[vertex] = True
        self._id[vertex] = self._count
        for edge in graph.adjacent_edges(vertex):
            if not self._marked[edge.other(vertex)]:
                self.dfs(graph, edge.other(vertex))

    def connected(self, vertex_1, vertex_2):
        return self._id[vertex_1] == self._id[vertex_2]

    def count(self):
        return self._count

    def get_components(self):
        components = defaultdict(list)
        for k, v in self._id.items():
            components[v].append(k)
        return components.values()


# 4.3.22 practice, implement minimum spanning forest
class KruskalMSF(object):

    """
    >>> test_data = ((4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16), (1, 5, 0.32),
    ...              (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19), (0, 2, 0.26), (1, 2, 0.36),
    ...              (1, 3, 0.29), (2, 7, 0.34), (6, 2, 0.4), (3, 6, 0.52), (6, 0, 0.58),
    ...              (6, 4, 0.93), (8, 12, 0.61), (8, 11, 0.77), (11, 12, 0.12), (8, 9, 0.99),
    ...              (9, 11, 0.36), (9, 10, 0.39), (8, 10, 0.04), (10, 12, 0.14))
    >>> ewg = EdgeWeightedGraph()
    >>> for a, b, weight in test_data:
    ...    edge = Edge(a, b, weight)
    ...    ewg.add_edge(edge)
    ...
    >>> kmsf = KruskalMSF(ewg)
    >>> sorted([[e for e in mst] for mst in kmsf.edges()])
    [[8-10 0.04, 11-12 0.12, 10-12 0.14, 9-11 0.36], [0-7 0.16, 2-3 0.17, 1-7 0.19, 0-2 0.26, 5-7 0.28, 4-5 0.35, 6-2 0.4]]
    """

    def __init__(self, forest):
        ecc = EdgeConnectedComponent(forest)
        self._msf = Queue()

        for vertices in ecc.get_components():
            pq = self._init_priority_queue(vertices, forest)
            uf = GenericUnionFind()
            mst = Queue()
            while not pq.is_empty() and mst.size() < len(vertices) - 1:
                edge = pq.del_min()
                a = edge.either()
                b = edge.other(a)
                if uf.connected(a, b):
                    continue
                uf.union(a, b)
                mst.enqueue(edge)
            self._msf.enqueue(mst)

    def _init_priority_queue(self, vertices, forest):
        dup_set = set()
        pq = MinPQ()
        for v in vertices:
            for edge in forest.adjacent_edges(v):
                if edge not in dup_set:
                    pq.insert(edge)
                    dup_set.add(edge)
        return pq

    def edges(self):
        return self._msf

    def weight(self):
        return sum(i.weight for i in self._mst)


# 4.3.24 practice, implement an algorithm delete a maximum-weight
# edge that the graph is still connected every time
class ReverseDeleteMST(object):

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
    >>> rd_mst = ReverseDeleteMST(ewg)
    >>> sorted([edge for edge in rd_mst.edges()])
    [0-7 0.16, 2-3 0.17, 1-7 0.19, 0-2 0.26, 5-7 0.28, 4-5 0.35, 6-2 0.4]
    """

    def __init__(self, graph):
        deleted_edges = set()
        max_pq = MaxPQ(graph.edges())
        self._mst = Queue()
        while not max_pq.is_empty():
            edge = max_pq.del_max()
            if self._graph_connected(graph, edge, deleted_edges):
                deleted_edges.add(edge)
            else:
                self._mst.enqueue(edge)

    def _graph_connected(self, graph, canidate_edge, deleted_edges):
        self._marked = defaultdict(bool)
        start_vertex = canidate_edge.either()
        self._marked[start_vertex] = True
        for edge in graph.adjacent_edges(start_vertex):
            a = edge.other(start_vertex)
            if edge is not canidate_edge and edge not in deleted_edges and not self._marked[a]:
                self._dfs(graph, a, canidate_edge, deleted_edges)
        connected_vertices = len([v for v in self._marked if self._marked[v]])
        return graph.vertices_size() == connected_vertices

    def _dfs(self, graph, vertex, canidate_edge, deleted_edges):
        self._marked[vertex] = True
        for edge in graph.adjacent_edges(vertex):
            v = edge.other(vertex)
            if edge is not canidate_edge and edge not in deleted_edges and not self._marked[v]:
                self._dfs(graph, v, canidate_edge, deleted_edges)

    def edges(self):
        return self._mst


# 4.3.28 practice
class PrimitiveLazyPrimMST(object):

    """
    >>> test_data = ((0.35, 4, 5), (0.37, 4, 7), (0.28, 5, 7), (0.16, 0, 7), (0.32, 1, 5),
    ...              (0.38, 0, 4), (0.17, 2, 3), (0.19, 1, 7), (0.26, 0, 2), (0.36, 1, 2),
    ...              (0.29, 1, 3), (0.34, 2, 7), (0.4, 6, 2), (0.52, 3, 6), (0.58, 6, 0),
    ...              (0.93, 6, 4))
    >>> wg = WeightedGraph()
    >>> for edge in test_data:
    ...     wg.add_edge(edge)
    ...
    >>> primitive_mst = PrimitiveLazyPrimMST(wg, 0)
    >>> [edge for edge in primitive_mst.edges()]
    [(0.16, 0, 7), (0.19, 1, 7), (0.26, 0, 2), (0.17, 2, 3), (0.28, 5, 7), (0.35, 4, 5), (0.4, 6, 2)]
    """

    def __init__(self, graph, start_vertex):
        self._marked = defaultdict(bool)
        self._mst = Queue()
        self.pq = MinPQ()
        self.visit(graph, start_vertex)
        while not self.pq.is_empty():
            edge = self.pq.del_min()
            if self._marked[edge[1]] and self._marked[edge[2]]:
                continue
            self._mst.enqueue(edge)
            if not self._marked[edge[1]]:
                self.visit(graph, edge[1])
            if not self._marked[edge[2]]:
                self.visit(graph, edge[2])

    def visit(self, graph, vertex):
        self._marked[vertex] = True
        for edge in graph.adjacent_edges(vertex):
            if edge[1] == vertex and not self._marked[edge[2]]:
                self.pq.insert(edge)
            elif edge[2] == vertex and not self._marked[edge[1]]:
                self.pq.insert(edge)

    def edges(self):
        return self._mst

    def weight(self):
        return sum(edge[0] for edge in self._mst)


# 4.3.32 practice, generate a mst with given edges(no cycle included)
class EdgeSetMST(object):

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
    >>> contain_edges = set(edge for edge in ewg.adjacent_edges(6))
    >>> mst = EdgeSetMST(ewg, contain_edges)
    >>> [edge for edge in mst.edges()]
    [6-4 0.93, 3-6 0.52, 6-2 0.4, 6-0 0.58, 0-7 0.16, 1-7 0.19, 5-7 0.28]
    """

    def __init__(self, graph, contain_edges):
        self._mst = Queue([edge for edge in contain_edges])
        pq = self._init_priority_queue(graph, contain_edges)
        uf = GenericUnionFind()
        for edge in contain_edges:
            uf.union(edge.either(), edge.other(edge.either()))

        while not pq.is_empty() and self._mst.size() < graph.vertices_size() - 1:
            edge = pq.del_min()
            a = edge.either()
            b = edge.other(a)
            if uf.connected(a, b):
                continue
            uf.union(a, b)
            self._mst.enqueue(edge)

    def _init_priority_queue(self, graph, contain_edges):
        pq = MinPQ()
        for edge in graph.edges():
            if edge not in contain_edges:
                pq.insert(edge)
        return pq

    def edges(self):
        return self._mst

    def weight(self):
        return sum(i.weight for i in self._mst)


if __name__ == '__main__':
    doctest.testmod()
