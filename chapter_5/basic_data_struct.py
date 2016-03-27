#!/usr/bin/env python
# -*- encoding:UTF-8 -*-


class Node(object):

    def __init__(self, val):
        self._val = val
        self.next_node = None

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, node):
        self._next_node = node


class Queue(object):

    def __init__(self, q=None):
        self._first = None
        self._last = None
        self._size = 0
        if q:
            for item in q:
                self.enqueue(item)

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def enqueue(self, val):
        old_last = self._last
        self._last = Node(val)
        self._last.next_node = None
        if self.is_empty():
            self._first = self._last
        else:
            old_last.next_node = self._last
        self._size += 1

    def dequeue(self):
        if not self.is_empty():
            val = self._first.val
            self._first = self._first.next_node
            if self.is_empty():
                self._last = None
            self._size -= 1
            return val
        return None


class Stack(object):

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def push(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def pop(self):
        if self._first:
            old = self._first
            self._first = self._first.next_node
            self._size -= 1
            return old.val
        return None

    def peek(self):
        if self._first:
            return self._first.val
        return None


class Bag(object):

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node is not None:
            yield node.val
            node = node.next_node

    def add(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size


class Digragh(object):

    def __init__(self, steps):
        self._edges_size = 0
        self._adj = {i: None for i in range(steps)}
        self._vertices = set()

    def vertices_size(self):
        return len(self._vertices)

    def edges_size(self):
        return self._edges_size

    def add_edge(self, start, end):
        self._vertices.add(start)
        self._vertices.add(end)
        if not self._adj[start]:
            self._adj[start] = Bag()
        self._adj[start].add(end)
        self._edges_size += 1

    def get_adjacent_vertices(self, vertex):
        return self._adj[vertex] if self._adj[vertex] is not None else []

    def vertices(self):
        return self._vertices

    def reverse(self):
        reverse_graph = Digragh()
        for vertex in self.vertices():
            for adjacent_vertex in self.get_adjacent_vertices(vertex):
                reverse_graph.add_edge(adjacent_vertex, vertex)
        return reverse_graph

    def has_edge(self, start, end):
        if not self._adj[start]:
            return False
        edge = next((i for i in self._adj[start] if i == end), None)
        return edge is not None

    def __repr__(self):
        s = str(len(self._vertices)) + ' vertices, ' + str(self._edges_size) + ' edges\n'
        for k in self._adj:
            try:
                lst = ' '.join([vertex for vertex in self._adj[k]])
            except TypeError:
                if self._adj[k]:
                    lst = ' '.join([str(vertex) for vertex in self._adj[k]])
                else:
                    lst = ''
            s += '{}: {}\n'.format(k, lst)
        return s
