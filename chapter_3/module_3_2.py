#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest


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

    '''
    binary search tree implementation.
    >>> bst = BST()
    >>> test_str = 'EASYQUESTION'
    >>> for (index, element) in enumerate(test_str):
    ...     bst.put(element, index)
    ...
    >>> bst.get('Q')
    4
    >>> bst.get('E')
    6
    >>> bst.get('N')
    11
    >>> bst.size()
    10
    >>> bst.max_val().key
    'Y'
    >>> bst.min_val().key
    'A'
    >>> bst.select(0).key
    'A'
    >>> bst.select(3).key
    'N'
    >>> bst.select(4).key
    'O'
    >>> bst.select(9).key
    'Y'
    >>> bst.rank('A')
    0
    >>> bst.rank('E')
    1
    >>> bst.rank('Y')
    9
    >>> bst.rank('T')
    7
    >>> bst.rank('U')
    8
    '''

    def __init__(self):
        self._root = None
        self._exist_keys = set()

    def size(self):
        '''
        return the node's amount of the binary search tree.
        '''
        if not self._root:
            return 0
        return self._root.size

    def is_empty(self):
        return self._root is None

    def node_size(self, node):
        return 0 if not node else node.size

    def get(self, key):
        '''
        return the corresponding value with the given key, iterate the whole tree,
        if the current node's key is equal to the given key, then return the node's value.
        if the current node's key is smaller than the given key,
        then jump to the right node of the current node,
        else jump to the left node of the current node.
        '''
        temp = self._root

        while temp:
            if temp.key == key:
                return temp.val

            if temp.key > key:
                temp = temp.left

            if temp.key < key:
                temp = temp.right
        return temp if not temp else temp.key

    def put(self, key, val):
        '''
        insert a new node into the binary search tree, iterate the whole tree,
        find the appropriate location for the new node and add the new node as the tree leaf.
        '''
        key_exists = key in self._exist_keys
        if not key_exists:
            self._exist_keys.add(key)
        temp = self._root
        inserted_node = None
        new_node = Node(key, val, 1)

        while temp:
            inserted_node = temp
            if not key_exists:
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

        inserted_node.size = self.node_size(
                inserted_node.left) + self.node_size(inserted_node.right) + 1

    def max_val(self):
        '''
        find the maximum value in the binary search tree.
        '''
        if not self._root:
            return None
        tmp = self._root
        while tmp.right:
            tmp = tmp.right
        return tmp

    def min_sub_tree_val(self, node):
        '''
        find the minimum value in the binary search tree which start with specific node.
        '''
        if not node:
            return None
        assert isinstance(node, Node)

        tmp = node
        while tmp.left:
            tmp = tmp.left
        return tmp

    def min_val(self):
        '''
        find the minimum value in the binary search tree.
        '''
        if not self._root:
            return None
        tmp = self._root
        while tmp.left:
            tmp = tmp.left
        return tmp

    def select(self, k):
        '''
        find the kth node of the binary search tree,
        the solution is similar with get() or put() function.
        '''
        assert isinstance(k, int) and k <= self.size()

        if not self._root:
            return None

        tmp = self._root
        while tmp:
            tmp_size = self.node_size(tmp.left)
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
                result += self.node_size(tmp.left) + 1
                tmp = tmp.right
            elif tmp.key == key:
                result += self.node_size(tmp.left)
                break
        return result

    def delete_min(self):
        self._root = self.__delete_min(self._root)

    def __delete_min(self, node):
        # find the minimum-value node.
        if not node.left:
            return node.right
        node.left = self.__delete_min(node.left)
        node.size = self.node_size(node.left) + self.node_size(node.right) + 1
        return node

    def delete(self, key):
        self._root = self.__delete(self._root, key)

    def __delete(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self.__delete(node.left, key)
        elif key > node.key:
            node.right = self.__delete(node.right, key)
        else:
            # node's left or right side is None.
            if not node.left or not node.right:
                return (node.left or node.right)
            # node's both side is not None.
            tmp = node
            node = self.min_sub_tree_val(tmp.right)
            node.right = self.__delete_min(tmp.right)
            node.left = tmp.left
        node.size = self.node_size(node.left) + self.node_size(node.right) + 1
        return node

    def keys(self):
        return self.keys_range(self.min_val().key, self.max_val().key)

    def keys_range(self, low, high):
        queue = []
        self.__keys(self._root, queue, low, high)
        return queue

    def __keys(self, node, queue, low, high):
        if not node:
            return
        if low < node.key:
            self.__keys(node.left, queue, low, high)
        if low <= node.key and high >= node.key:
            queue.append(node.key)
        if high > node.key:
            self.__keys(node.right, queue, low, high)

    def height(self):
        return self.__height(self._root)

    def __height(self, node):
        if not node:
            return -1
        return 1 + self.__height(node.left) + self.__height(node.right)


if __name__ == '__main__':
    doctest.testmod()
