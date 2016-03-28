#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from basic_data_struct import Digragh, Stack, Bag
from collections import defaultdict


class DirectedDFS(object):

    def __init__(self, graph, sources):
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


class NFA(object):

    '''
        NFA(nondeterministic finite state automaton) algorithm for regular expression.
    Regular expression is a effective string searching method, it will identify specific
    string with a given regular expression. First this algorithm construct a NFA with a
    given regular expression, that will be a directed graph of epsilon transitions. Then
    input a text and go through every character. For each character, first reach all the
    possible states  and then execute a epsilon transition which output a set with all possible
    states. When all character is checked, if we reach the end state, that means the input
    text match the regular expression. The worst case of running time is proportional to
    O(MN), M is the length of regular expression, N is the length of the input text.
    >>> nfa = NFA('(A*B|AC)D')
    >>> nfa.recognizes('AAAABD')
    True
    >>> nfa2 = NFA('(A*B|AC)D')
    >>> nfa2.recognizes('AAAAC')
    False
    >>> nfa3 = NFA('(a|(bc)*d)*')
    >>> nfa3.recognizes('abcbcd')
    True
    >>> nfa4 = NFA('(a|(bc)*d)*')
    >>> nfa4.recognizes('abcbcbcdaaaabcbcdaaaddd')
    True
    >>> nfa5 = NFA('(.*AB((C|D|E)F)*G)')
    >>> nfa5.recognizes('dfawefdABCQQQG')
    True
    '''

    def __init__(self, regexp):
        self._regexp = regexp
        self._ops = Stack()
        self._reg_len = len(self._regexp)
        self._graph = Digragh(self._reg_len + 1)

        for i in range(self._reg_len):
            lp = i
            if self._regexp[i] == '(' or self._regexp[i] == '|':
                self._ops.push(i)
            elif self._regexp[i] == ')':
                or_op = self._ops.pop()
                if self._regexp[or_op] == '|':
                    lp = self._ops.pop()
                    self._graph.add_edge(lp, or_op + 1)
                    self._graph.add_edge(or_op, i)
                else:
                    lp = or_op
            if i < self._reg_len - 1 and self._regexp[i + 1] == '*':
                self._graph.add_edge(lp, i + 1)
                self._graph.add_edge(i + 1, lp)
            if self._regexp[i] in ('(', '*', ')') or self._regexp[i].isalpha():
                self._graph.add_edge(i, i + 1)

    def recognizes(self, txt):
        pc = Bag()
        dfs = DirectedDFS(self._graph, (0,))
        for v in self._graph.vertices():
            if dfs.marked(v):
                pc.add(v)

        length = len(txt)
        for i in range(length):
            match = Bag()
            for v in pc:
                if v < self._reg_len:
                    if self._regexp[v] == txt[i] or self._regexp[v] == '.':
                        match.add(v + 1)

            pc = Bag()
            dfs = DirectedDFS(self._graph, match)
            for v in self._graph.vertices():
                if dfs.marked(v):
                    pc.add(v)

        for v in pc:
            if v == self._reg_len:
                return True
        return False


if __name__ == '__main__':
    doctest.testmod()
