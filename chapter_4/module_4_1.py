#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from collections import defaultdict
from chapter_1.module_1_3 import Bag, Queue, Stack


class Graph(object):

    """
      Undirected graph implementation. The space is about O(V + E)
    (V is the number of vertices and E is the number of edges). Adding
    an edge only takes constant time. The running time of
    Checking if node v is adjacent to w and traveling all adjacent point of v
     is related to the degree of v.
    """

    def __init__(self, input_file=None):
        self._vertex_size = 0
        self._edge_size = 0
        self._adj = {}

        if input_file:
            with open(input_file) as f:
                lines = [l.rstrip('\n') for l in f]
                self._vertex_size = int(lines[0])
                self._edge_size = int(lines[1])
                for i in range(1, self._edge_size):
                    a, b = lines[i].split()
                    self.add_edge(a, b)

    def vertex_size(self):
        return self._vertex_size

    def edge_size(self):
        return self._edge_size

    def add_edge(self, vertext_a, vertext_b):
        if vertext_a not in self._adj:
            self._adj[vertext_a] = Bag()
        if vertext_b not in self._adj:
            self._adj[vertext_b] = Bag()
        self._adj[vertext_a].add(vertext_b)
        self._adj[vertext_b].add(vertext_a)

        self._edge_size += 1

    def get_adjacent_vertices(self, vertex):
        return self._adj.get(vertex, None)

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
        return count / 2

    def __str__(self):
        s = str(self._vertex_size) + ' vertices, ' + str(self._edge_size) + 'edges\n'
        for k in self._adj:
            try:
                lst = ' '.join([vertex for vertex in self._adj[k]])
            except ValueError:
                lst = ' '.join([str(vertex) for vertex in self._adj[k]])
            s += '{}: {}'.format(k, lst)
        return s


class DepthFirstPaths(object):

    """
    Undirected graph depth-first searching algorithms implementation.
    """

    def __init__(self, graph, start_vertex):
        self._marked = defaultdict(bool)
        self._edge_to = {}
        self._start = start_vertex

    def dfs(self, graph, vertex):
        self._marked[vertex] = True

        for v in graph.get_adjacent_vertices(vertex):
            if not self._marked[v]:
                self._edge_to[v] = vertex
                self.dfs(graph, v)

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


class BreadthFirstPaths(object):

    """
    """

    def __init__(self, graph, start_vertex):
        self._marked = defaultdict(bool)
        self._edge_to = {}
        self._start = start_vertex
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

if __name__ == '__main__':
    doctest.testmod()
