#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest

RED = 1
BLACK = 2


class Node(object):

    def __init__(self, key, value, size, color):
        self._key = key
        self._value = value
        self._size = size
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        assert new_color in (RED, BLACK)
        self._color = new_color

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        self._key = new_key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        assert isinstance(node, (Node, type(None)))
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        assert isinstance(node, (Node, type(None)))
        self._right = node

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        assert isinstance(val, int) and val >= 0
        self._size = val


class RBTree(object):

    def __init__(self):
        self._root = None

    def __is_red(self, node):
        if not node:
            return BLACK
        return node.color == RED

    def __node_size(self, node):
        return 0 if not node else node.size

    def __rotate_left(self, node):
        rotate_node = node.right
        node.right = rotate_node.left
        rotate_node.left = node
        rotate_node.color = node.color
        node.color = RED
        rotate_node.size = node.size
        node.size = self.__node_size(node.left) + self.__node_size(node.right)
        return rotate_node

    def __rotate_right(self, node):
        rotate_node = node.left
        node.left = rotate_node.right
        rotate_node.right = node
        rotate_node.color = node.color
        node.color = RED
        rotate_node.size = node.size
        node.size = self.__node_size(node.left) + self.__node_size(node.right)
        return rotate_node

if __name__ == '__main__':
    doctest.testmod()
