#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import sys
from basic_data_struct import MinPQ


class Node(object):

    def __init__(self, char, freq, left, right):
        self._char = char
        self._freq = freq
        self._left = left
        self._right = right

    def is_leaf(self):
        return self._left is None and self._right is None

    def __cmp__(self, other):
        return self._freq - other._freq

    @property
    def char(self):
        return self._char

    @property
    def freq(self):
        return self._freq

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right


class Huffman(object):

    @staticmethod
    def compress():
        input_string = ''.join(sys.stdin.readlines())
        frequency = [0] * 256
        for i in input_string:
            frequency[ord(i)] += 1

        root = Huffman.build_trie(frequency)

        Huffman.write_trie(root)

        st = [None] * 256
        Huffman.build_code(st, root, '')
        sys.stdout.buffer.write(bytes(len(input_string)))

        for i in input_string:
            code = st[i]
            for c in code:
                if c == '0':
                    sys.stdout.buffer.write(b'0')
                elif c == '1':
                    sys.stdout.buffer.write(b'1')
                else:
                    raise Exception('Illegal state.')

        sys.stdout.close()

    @staticmethod
    def build_trie(freq):
        min_pq = MinPQ()
        for i in range(256):
            if freq[i]:
                min_pq.insert(chr(i), freq, None, None)

        while min_pq.size() > 1:
            left = min_pq.del_min()
            right = min_pq.del_min()
            parent = Node('\0', left.freq + right.freq, left, right)
            min_pq.insert(parent)
        return min_pq.del_min()

    @staticmethod
    def write_trie(node):
        if node.is_leaf():
            sys.stdout.buffer.write(b'1')
            sys.stdout.buffer.write(bytes(node.char.encode('ascii')))
            return
        sys.stdout.write_bit(b'0')
        Huffman.write_trie(node.left)
        Huffman.write_trie(node.right)

    @staticmethod
    def build_code(st, node, code):
        if not node.is_leaf():
            Huffman.build_code(st, node.left, code + '0')
            Huffman.build_code(st, node.right, code + '1')
        else:
            st[ord(node.char)] = code

    @staticmethod
    def expand():
        root = Huffman.read_trie()
        length = sys.stdin.read(4)
        for i in range(length):
            node = root
            while not node.is_leaf():
                bit = sys.stdin.read(1)
                node = node.right if bit else node.left
            sys.stdout.write(node.char)

    @staticmethod
    def read_trie():
        is_leaf = sys.stdin.read(1)
        if(is_leaf):
            return Node(sys.stdin.read(1).decode('ascii'), -1, None, None)
        return Node('\0', -1, Huffman.read_trie(), Huffman.read_trie())

if __name__ == '__main__':
    doctest.testmod()
