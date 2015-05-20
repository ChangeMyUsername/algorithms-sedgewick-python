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
        '''
        return the node's amount of the binary search tree.
        '''
        if not self._root:
            return 0
        return self._root.size

    def get(self, key):
        '''
        return the corresponding value with the given key, iterate the whole tree,
        if the current node's key is equal to the given key, then return the node's value.
        if the current node's key is smaller than the given key, then jump to the right node of the current node,
        else jump to the left node of the current node.
        '''
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
        '''
        insert a new node into the binary search tree, iterate the whole tree,
        find the appropriate location for the new node and add the new node as the tree leaf.
        '''
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

    def max_val(self):
        '''
        find the maximum value in the binary search tree.
        '''
        if not self._root:
            return None
        tmp = self._root
        while tmp.right:
            tmp = tmp.right
        return tmp.val

    def min_val(self):
        '''
        find the minimum value in the binary search tree.
        '''
        if not self._root:
            return None
        tmp = self._root
        while tmp.left:
            tmp = tmp.left
        return tmp.val

    def select(self, k):
        '''
        find the kth node of the binary search tree, the solution is similar with get() or put() function.
        '''
        assert isinstance(k, int) and k <= self.size()

        if not self._root:
            return None

        tmp = self._root
        while tmp:
            tmp_size = tmp.left.size
            if tmp_size > k:
                tmp = tmp.left
            elif tmp_size < k:
                tmp = tmp.right
                k = k - tmp_size - 1
            else:
                return tmp

    def rank(self, key):
        '''
        find the rank of the node in the binary search tree by the given key.
        '''
        result = 0
        if not self._root:
            return -1
        tmp = self._root

        while tmp:
            if tmp.key > key:
                tmp = tmp.left
            elif tmp.key < key:
                result += tmp.left.size + 1
                tmp = tmp.right
            elif tmp.key == key:
                result = tmp.left.size
        return result
