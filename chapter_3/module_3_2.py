#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random


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
    >>> bst.is_empty()
    True
    >>> test_str = 'EASYQUESTION'
    >>> for (index, element) in enumerate(test_str):
    ...     bst.put(element, index)
    ...
    >>> bst.is_binary_tree()
    True
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
    >>> bst.is_empty()
    False
    >>> node = bst.select(0)
    >>> node.key
    'A'
    >>> node2 = bst.select(2)
    >>> node2.key
    'I'
    >>> node3 = bst.select(9)
    >>> node3.key
    'Y'
    >>> bst.keys()
    ['A', 'E', 'I', 'N', 'O', 'Q', 'S', 'T', 'U', 'Y']
    >>> bst.height()
    5
    >>> random_key = bst.random_key()
    >>> random_key in test_str
    True
    >>> bst.delete_min()
    >>> bst.min_val().key
    'E'
    >>> bst.delete_max()
    >>> bst.max_val().key
    'U'
    >>> bst.delete('O')
    >>> bst.delete('S')
    >>> bst.keys()
    ['E', 'I', 'N', 'Q', 'T', 'U']
    >>> bst.is_binary_tree()
    True
    >>> bst.is_ordered()
    True
    >>> bst.is_rank_consistent()
    True
    >>> bst.check()
    True
    '''

    def __init__(self):
        self._root = None
        self._exist_keys = set()
        self._last_visited_node = None

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

    # 3.2.13 practice, implement get method with iteration.
    def get(self, key):
        '''
        return the corresponding value with the given key, iterate the whole tree,
        if the current node's key is equal to the given key, then return the node's value.
        if the current node's key is smaller than the given key,
        then jump to the right node of the current node,
        else jump to the left node of the current node.
        '''

        # 3.2.28 practice add cache for bst.
        if self._last_visited_node and self._last_visited_node.key == key:
            return self._last_visited_node.val

        temp = self._root

        while temp:
            if temp.key == key:
                self._last_visited_node = temp
                return temp.val

            if temp.key > key:
                temp = temp.left

            if temp.key < key:
                temp = temp.right
        return temp

    # 3.2.13 practice, implement get method with iteration,
    # use set data structure for recording exist keys, if new key exists, stop
    # increment the node's size counter.
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
            self._root = new_node
            return
        else:
            if inserted_node.key < key:
                inserted_node.right = new_node
            else:
                inserted_node.left = new_node

        inserted_node.size = self.node_size(
                inserted_node.left) + self.node_size(inserted_node.right) + 1

        self._last_visited_node = new_node

    # 3.2.14 practice
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

    # 3.2.14 practice
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

    # 3.2.14 practice
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

    # 3.2.14 practice
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

    def delete_max(self):
        self._root = self.__delete_max(self._root)

    def __delete_max(self, node):
        # find the maximum-value node.
        if not node.right:
            return node.left
        node.right = self.__delete_max(node.right)
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

    # 3.2.6 practice, add height function for binary tree.
    def height(self):
        return self.__height(self._root)

    def __height(self, node):
        if not node:
            return -1
        return 1 + max(self.__height(node.left), self.__height(node.right))

    # 3.2.21 randomly choose a node from bianry search tree.
    def random_key(self):
        if not self._root:
            return None
        total_size = self._root.size
        rank = random.randint(0, total_size - 1)
        random_node = self.select(rank)
        return random_node.key

    # 3.2.29 practice, check if each node's size is
    # equals to the summation of left node's size and right node's size.
    def is_binary_tree(self):
        return self.__is_binary_tree(self._root)

    def __is_binary_tree(self, node):
        if not node:
            return True
        if node.size != self.node_size(node.left) + self.node_size(node.right) + 1:
            return False
        return self.__is_binary_tree(node.left) and self.__is_binary_tree(node.right)

    # 3.2.30 practice, check if each node in binary search tree is ordered
    # (less than right node and greater than left node)
    def is_ordered(self):
        return self.__is_ordered(self._root, None, None)

    def __is_ordered(self, node, min_key, max_key):
        if not node:
            return True
        if min_key and node.key <= min_key:
            return False
        if max_key and node.key >= max_key:
            return False
        return (self.__is_ordered(node.left, min_key, node.key)
                and self.__is_ordered(node.right, node.key, max_key))

    # 3.2.24 practice, check if each node's rank is correct.
    def is_rank_consistent(self):
        for i in range(self.size()):
            if i != self.rank(self.select(i).key):
                return False

        for key in self.keys():
            if key != self.select(self.rank(key)).key:
                return False

        return True

    # 3.2.32 practice, check if a data structure is binary search tree.
    def check(self):
        if not self.is_binary_tree():
            return False
        if not self.is_ordered():
            return False
        if not self.is_rank_consistent():
            return False
        return True

if __name__ == '__main__':
    doctest.testmod()
