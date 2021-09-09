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
        self._left = None
        self._right = None

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

    """
    >>> rbt = RBTree()
    >>> rbt.is_empty()
    True
    >>> rbt.size()
    0
    >>> for index, e in enumerate('EASYQUITION'):
    ...     rbt.put(e, index)
    ...
    >>> rbt.check()
    True
    >>> node1 = rbt.get('A').value
    >>> node1
    1
    >>> rbt.get('E').value
    0
    >>> rbt.get('Y').value
    3
    >>> rbt.get('N').value
    10
    >>> rbt.is_empty()
    False
    >>> rbt.size() ### duplicate values 'I'
    10
    >>> rbt.min_val().value
    1
    >>> rbt.max_val().value
    3
    >>> rbt.delete_min()
    >>> rbt.min_val().value
    0
    >>> rbt.delete_min()
    >>> rbt.min_val().value
    8
    >>> rbt.delete_max()
    >>> rbt.max_val().value
    5
    >>> rbt.delete_max()
    >>> rbt.max_val().value
    7
    >>> rbt.check()
    True
    """

    def __init__(self):
        self._root = None

    def __is_red(self, node):
        if not node:
            return False
        return node.color == RED

    def size(self):
        return self.__node_size(self._root)

    def is_empty(self):
        return self._root is None

    def __node_size(self, node):
        return 0 if not node else node.size

    def __rotate_left(self, node):
        assert node and self.__is_red(node.right)

        rotate_node = node.right
        node.right = rotate_node.left
        rotate_node.left = node
        rotate_node.color = node.color
        node.color = RED
        rotate_node.size = node.size
        node.size = self.__node_size(
            node.left) + self.__node_size(node.right) + 1
        return rotate_node

    def __rotate_right(self, node):
        assert node and self.__is_red(node.left)

        rotate_node = node.left
        node.left = rotate_node.right
        rotate_node.right = node
        rotate_node.color = node.color
        node.color = RED
        rotate_node.size = node.size
        node.size = self.__node_size(
            node.left) + self.__node_size(node.right) + 1
        return rotate_node

    def __flip_colors(self, node):
        assert node and node.left and node.right
        assert (not self.__is_red(node) and self.__is_red(node.left) and
                self.__is_red(node.right) or
                self.__is_red(node) and
                not self.__is_red(node.left) and
                not self.__is_red(node.right))

        node.color = RED if node.color == BLACK else BLACK
        node.left.color = RED if node.left.color == BLACK else BLACK
        node.right.color = RED if node.right.color == BLACK else BLACK

    def get(self, key):
        return self.__get(self._root, key)

    def __get(self, node, key):
        tmp = node
        while tmp:
            if tmp.key > key:
                tmp = tmp.left
            elif tmp.key < key:
                tmp = tmp.right
            else:
                break
        return tmp

    def min_val(self):
        return self.__min_val(self._root)

    def __min_val(self, node):
        tmp = node
        while tmp.left:
            tmp = tmp.left
        return tmp

    def put(self, key, value):
        self._root = self.__put(self._root, key, value)
        self._root.color = BLACK

    def __put(self, node, key, value):
        if not node:
            return Node(key, value, 1, RED)
        if key < node.key:
            node.left = self.__put(node.left, key, value)
        elif key > node.key:
            node.right = self.__put(node.right, key, value)
        else:
            node.value = value

        # according to the book's definition, red node only exists in left node,
        # if right node is red, rotate left, make sure left node is red.
        if self.__is_red(node.right) and not self.__is_red(node.left):
            node = self.__rotate_left(node)

        # a red-black tree could not exist two consecutive red left node,
        # in this case, rotate right, then the left node and right node is both red,
        # the next move would be flip both node's colors.
        if self.__is_red(node.left) and node.left.left and self.__is_red(node.left.left):
            node = self.__rotate_right(node)

        if self.__is_red(node.left) and self.__is_red(node.right):
            self.__flip_colors(node)

        node.size = self.__node_size(
            node.left) + self.__node_size(node.right) + 1
        return node

    def __balance(self, node):
        assert node is not None

        if self.__is_red(node.right):
            node = self.__rotate_left(node)

        if self.__is_red(node.left) and self.__is_red(node.left.left):
            node = self.__rotate_right(node)

        if self.__is_red(node.left) and self.__is_red(node.right):
            self.__flip_colors(node)

        node.size = self.__node_size(
            node.left) + self.__node_size(node.right) + 1
        return node

    def __move_red_left(self, node):
        assert node is not None
        assert (self.__is_red(node) and not self.__is_red(node.left) and
                not self.__is_red(node.left.left))

        self.__flip_colors(node)
        # if node.right.left node is red, that means there is one more node can be "borrow",
        # then move one node to node's right side.
        if self.__is_red(node.right.left):
            node.right = self.__rotate_right(node.right)
            node = self.__rotate_left(node)
        return node

    # 3.3.39 delete minimum key in red-black tree, the java implementation is on the book,
    # this is python implementation of the book's answer.
    def delete_min(self):

        if self.is_empty():
            return None

        # this is for keeping red-black tree's balance
        if not self.__is_red(self._root.left) and not self.__is_red(self._root.right):
            self._root.color = RED
        self._root = self.__delete_min(self._root)
        if not self.is_empty():
            self._root.color = BLACK

    def __delete_min(self, node):
        if not node.left:
            return None
        # if node's left node and node's left's left node is not red, "borrow" one node
        # from node's right side to keep the red-black tree balance.
        if not self.__is_red(node.left) and not self.__is_red(node.left.left):
            node = self.__move_red_left(node)
        node.left = self.__delete_min(node.left)
        return self.__balance(node)

    def __move_red_right(self, node):
        self.__flip_colors(node)
        # this is the same priciple to the __move_red_left function, move one node from
        # the node's right side if the two consecutive left node is not red.
        if not self.__is_red(node.left.left):
            node = self.__rotate_right(node)
        return node

    # 3.3.39 delete maximum key in red-black tree, the java implementation is on the book,
    # this is python implementation of the book's answer, there is a little bit different with
    # delete_min function.
    def delete_max(self):
        # this is for keeping red-black tree's balance
        if not self.__is_red(self._root.left) and not self.__is_red(self._root.right):
            self._root.color = RED
        self._root = self.__delete_max(self._root)
        if not self.is_empty():
            self._root.color = BLACK

    def __delete_max(self, node):
        if self.__is_red(node.left):
            node = self.__rotate_right(node)
        if not node.right:
            return None
        if not self.__is_red(node.right) and not self.__is_red(node.right.left):
            node = self.__move_red_right(node)
        node.right = self.__delete_max(node.right)
        return self.__balance(node)

    def delete(self, key):
        if not self.__is_red(self._root.left) and not self.__is_red(self._root.right):
            self._root.color = RED
        self._root = self.__delete(self._root, key)
        if not self.is_empty():
            self._root.color = BLACK

    def __delete(self, node, key):
        if key < node.key:
            # same principle with delete_min function
            if not self.__is_red(node.left) and not self.__is_red(node.left.left):
                node = self.__move_red_left(node)
            node.left = self.__delete(node.left, key)
        else:
            if self.__is_red(node.left):
                node = self.__rotate_right(node)

            if key == node.key and node.right is None:
                return None

            if not self.__is_red(node.right) and not self.__is_red(node.right.left):
                node = self.__move_red_right(node)

            if key == node.key:
                node.value = self.__get(
                    node.right, self.__min_val(node.right).key)
                node.key = self.__min_val(node.right).key
                node.right = self.__delete_min(node.right)
            else:
                node.right = self.__delete(node.right, key)
        return self.__balance(node)

    def select(self, k):
        """
          Find the kth node of the binary search tree,
        the solution is similar with get() or put() function.
        """
        assert isinstance(k, int) and k <= self.size()

        if not self._root:
            return None

        tmp = self._root
        while tmp:
            tmp_size = self.__node_size(tmp.left)
            if tmp_size > k:
                tmp = tmp.left
            elif tmp_size < k:
                tmp = tmp.right
                k = k - tmp_size - 1
            else:
                return tmp

    def rank(self, key):
        """
          Find the rank of the node in the binary search tree by the given key.
        """
        result = 0
        if not self._root:
            return -1
        tmp = self._root

        while tmp:
            if tmp.key > key:
                tmp = tmp.left
            elif tmp.key < key:
                result += self.__node_size(tmp.left) + 1
                tmp = tmp.right
            elif tmp.key == key:
                result += self.__node_size(tmp.left)
                break
        return result

    def max_val(self):
        """
          Find the maximum value in the binary search tree.
        """
        if not self._root:
            return None
        tmp = self._root
        while tmp.right:
            tmp = tmp.right
        return tmp

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

    def is_rbt(self):
        return self.__is_rbt(self._root)

    def __is_rbt(self, node):
        if not node:
            return True
        if self.__is_red(node.right):
            return False
        if node != self._root and self.__is_red(node) and self.__is_red(node.left):
            return False
        return self.__is_rbt(node.left) and self.__is_rbt(node.right)

    def is_binary_tree(self):
        return self.__is_binary_tree(self._root)

    def __is_binary_tree(self, node):
        if not node:
            return True
        if node.size != self.__node_size(node.left) + self.__node_size(node.right) + 1:
            return False
        return self.__is_binary_tree(node.left) and self.__is_binary_tree(node.right)

    def is_ordered(self):
        return self.__is_ordered(self._root, None, None)

    def __is_ordered(self, node, min_key, max_key):
        if not node:
            return True
        if min_key and node.key <= min_key:
            return False
        if max_key and node.key >= max_key:
            return False
        return (self.__is_ordered(node.left, min_key, node.key) and
                self.__is_ordered(node.right, node.key, max_key))

    def is_rank_consistent(self):
        for i in range(self.size()):
            if i != self.rank(self.select(i).key):
                return False

        for key in self.keys():
            if key != self.select(self.rank(key)).key:
                return False

        return True

    def check(self):
        if not self.is_binary_tree():
            return False
        if not self.is_ordered():
            return False
        if not self.is_rank_consistent():
            return False
        if not self.is_rbt():
            return False
        return True


if __name__ == '__main__':
    doctest.testmod()
