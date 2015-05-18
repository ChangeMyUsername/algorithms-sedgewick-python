#!/usr/bin/env python
# -*- encoding:UTF-8 -*-


class Node(object):

    def __init__(self, key, val, size):
        self._left = self._right = None
        self._key = key
        self._val = val
        self._size = size

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        assert isinstance(node, Node)
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        assert isinstance(node, Node)
        self._right = node

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        assert isinstance(val, int) and val >= 0
        self._size = val

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, val):
        self._key = val

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value


class BST(object):

    def __init__(self):
        self._root = None

    def size(self):
        if not self._root:
            return 0
        return self._root.size

    def get(self, key):
        temp = self._root
        if not temp:
            return None

        while temp:
            if temp.key == key:
                return temp.val

            if temp.key > key:
                temp = temp.left

            if temp.key < key:
                temp = temp.right
        return None

    def put(self, key, val):
        temp = self._root
        inserted_node = None
        new_node = Node(key, val, 1)
        while temp:
            inserted_node = temp
            temp.size += 1

            if temp.key > key:
                temp = temp.left
            elif temp.key < key:
                temp = temp.right
            elif temp.key == key:
                temp.val = val
                return

        if not inserted_node:
            self._root = Node(key, val, 1)
            return
        else:
            if inserted_node.key < key:
                inserted_node.right = new_node
            else:
                inserted_node.left = new_node

            inserted_node.size = self.size(inserted_node.left) + self.size(inserted_node.right) + 1
