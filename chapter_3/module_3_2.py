#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random
from typing import Any, Deque, Iterable, List, Optional

from common import CT


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

    """
      Binary search tree implementation.
    """

    def __init__(self) -> None:
        """Initialization method
        """
        self._root = None
        self._exist_keys = set()
        self._last_visited_node = None

    def size(self) -> int:
        """Return total size of binary tree.

        Returns:
            int: size of binary tree
        """
        if not self._root:
            return 0
        return self._root.size

    def is_empty(self) -> bool:
        """Check if binary tree is empty or not.

        Returns:
            bool: True if tree is empty else False

        >>> bst = BST()
        >>> bst.is_empty()
        True
        >>> bst.put('H', 1)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def node_size(self, node: Node) -> int:
        """Return size of given `node`.

        Args:
            node (Node): any Node object in binary tree

        Returns:
            int: size of `node`
        """
        return 0 if not node else node.size

    # 3.2.13 practice, implement get method with iteration.
    def get(self, key: CT) -> Optional[Node]:
        """Return the corresponding value with the given key.

        Args:
            key (CT): key of Node object

        Returns:
            Node: matched Node object, if `key` is not found, return `None`

        >>> bst = BST()
        >>> bst.is_empty()
        True
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> test_str == ''.join(bst.get(i).key for i in test_str)
        True
        >>> bst.get('vvv') # no such key
        """
        # 3.2.28 practice add cache for bst.
        if self._last_visited_node and self._last_visited_node.key == key:
            return self._last_visited_node

        temp = self._root

        while temp:
            if temp.key == key:
                self._last_visited_node = temp
                return temp

            if temp.key > key:
                temp = temp.left

            if temp.key < key:
                temp = temp.right
        return temp

    # 3.2.13 practice.
    def put(self, key: CT, val: Any) -> None:
        """Insert a new node into the binary search tree,
        iterate tree from root,
        find appropricate node and insert new node as leaf,
        then update all node's size.

        Args:
            key (CT): key of new node
            val (Any): value of new node

        >>> bst = BST()
        >>> bst.is_empty()
        True
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.size()
        10
        """
        key_exists = key in self._exist_keys
        if not key_exists:
            self._exist_keys.add(key)
        temp = self._root
        inserted_node = None
        new_node = Node(key, val, 1)
        # find leaf node to append
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
    def max_val(self) -> Optional[Node]:
        """Return maximum value in binary tree, no recursion.

        Returns:
            CT: maximum value

        >>> bst = BST()
        >>> bst.max_val()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.max_val().key
        'Y'
        """
        if not self._root:
            return None
        tmp = self._root
        while tmp.right:
            tmp = tmp.right
        return tmp

    # 3.2.14 practice
    def min_val(self) -> Optional[Node]:
        """Return minimum value in binary tree.

        Returns:
            CT: minimum value

        >>> bst = BST()
        >>> bst.min_val()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.min_val().key
        'A'
        """
        if not self._root:
            return None
        tmp = self._root
        while tmp.left:
            tmp = tmp.left
        return tmp

    # 3.2.14 practice
    def select(self, key_rank: int) -> Optional[Node]:
        """Find the kth node of binary tree,
        the solution is similar with get() or put() function.

        Args:
            key_rank (int): rank of selected key

        Returns:
            Optional[Node]: kth Node object

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> ''.join(bst.select(i).key for i in range(10))
        'AEINOQSTUY'
        """
        assert isinstance(key_rank, int) and key_rank <= self.size()

        if not self._root:
            return None

        tmp = self._root
        while tmp:
            tmp_size = self.node_size(tmp.left)
            if tmp_size > key_rank:
                tmp = tmp.left
            elif tmp_size < key_rank:
                tmp = tmp.right
                key_rank = key_rank - tmp_size - 1
            else:
                return tmp

    # 3.2.14 practice
    def rank(self, key: CT) -> int:
        """Return the rank of given key in binary tree, if key is not in
        binary tree, return -1.

        Args:
            key (CT): key in binary tree

        Returns:
            int: rank of key in binary tree

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> ''.join(str(bst.rank(key)) for key in 'AEINOQSTUY')
        '0123456789'
        """
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

    def delete_min(self) -> None:
        """Delete minimal node in binary tree.

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.delete_min()
        >>> bst.min_val().key
        'E'
        """
        self._root = self.__delete_min(self._root)

    def __delete_min(self, node: Node) -> Optional[Node]:
        if not node.left:
            return node.right
        node.left = self.__delete_min(node.left)
        node.size = self.node_size(node.left) + self.node_size(node.right) + 1
        return node

    def delete_max(self) -> None:
        """Delete maximal node in binary tree.

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.delete_max()
        >>> bst.max_val().key
        'U'
        """
        self._root = self.__delete_max(self._root)

    def __delete_max(self, node: Node) -> Optional[Node]:
        # find the maximum-value node.
        if not node.right:
            return node.left
        node.right = self.__delete_max(node.right)
        node.size = self.node_size(node.left) + self.node_size(node.right) + 1
        return node

    def delete(self, key: CT) -> None:
        """Delete given key in binary tree.

        Args:
            key (CT): key in binary tree

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> for char in 'AEINOQSTUY':
        ...     bst.delete(char)
        >>> bst.size()
        0
        >>> bst.is_empty()
        True
        """
        self._root = self.__delete(self._root, key)

    def __delete(self, node: Node, key: CT) -> Node:
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
            node = self.__min_val(tmp.right)
            node.right = self.__delete_min(tmp.right)
            node.left = tmp.left
        node.size = self.node_size(node.left) + self.node_size(node.right) + 1
        return node

    def keys(self) -> List[CT]:
        """Return all keys in binary tree

        Returns:
            List[CT]: list of all keys

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> ''.join(bst.keys())
        'AEINOQSTUY'
        """
        return self.keys_range(self.min_val().key, self.max_val().key)

    def keys_range(self, low: CT, high: CT) -> List[CT]:
        """Return keys between `low` and `high` in binary tree.

        Args:
            low (CT): low key
            high (CT): high key

        Returns:
            List[CT]: list of keys

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> ''.join(bst.keys_range('A', 'O'))
        'AEINO'
        """
        queue = []
        self.__keys(self._root, queue, low, high)
        return queue

    def __keys(self, node: Node, queue: List[CT], low: CT, high: CT):
        if not node:
            return
        if low < node.key:
            self.__keys(node.left, queue, low, high)
        if low <= node.key and high >= node.key:
            queue.append(node.key)
        if high > node.key:
            self.__keys(node.right, queue, low, high)

    def floor(self, key: CT) -> Optional[Node]:
        """Return the nearest key element that less than given `key`,
        if `key` in binary tree, return `key`.

        Args:
            key (CT): input key

        Returns:
            Optional[Node]: node object

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> fn = bst.floor('B')
        >>> fn.key
        'A'
        >>> fn2 = bst.floor('Z')
        >>> fn2.key
        'Y'
        >>> fn3 = bst.floor('E')
        >>> fn3.key
        'E'
        """
        tmp = None
        node = self._root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                tmp = node
                node = node.right
            else:
                return node
        return tmp

    def ceiling(self, key: CT) -> Optional[Node]:
        """Return the nearest key element that larger than given `key`,
        if `key` in binary tree, return `key`.

        Args:
            key (CT): input key

        Returns:
            Optional[Node]: node object

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> cn = bst.ceiling('B')
        >>> cn.key
        'E'
        >>> cn2 = bst.ceiling('R')
        >>> cn2.key
        'S'
        >>> cn3 = bst.ceiling('S')
        >>> cn3.key
        'S'
        """
        tmp = None
        node = self._root
        while node:
            if key < node.key:
                tmp = node
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return tmp

    # 3.2.6 practice, add height function for binary tree.
    def height(self) -> int:
        """Return height of binary tree.

        Returns:
            int: height of binary tree

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.height()
        5
        """
        return self.__height(self._root)

    def __height(self, node: Node) -> int:
        if not node:
            return -1
        return 1 + max(self.__height(node.left), self.__height(node.right))

    # 3.2.21 randomly choose a node from bianry search tree.
    def random_key(self) -> CT:
        """Return random key in binary tree.

        Returns:
            CT: key in binary tree

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> for _ in range(100):
        ...     assert bst.random_key() in test_str
        ...
        """
        if not self._root:
            return None
        total_size = self._root.size
        rank = random.randint(0, total_size - 1)
        random_node = self.select(rank)
        return random_node.key

    # 3.2.29 practice, check if each node's size is
    # equals to the summation of left node's size and right node's size.
    def is_binary_tree(self) -> bool:
        """Check if current binary tree is valid.

        Returns:
            bool: True if binary tree is valid else False

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.is_binary_tree()
        True
        """
        queue = Deque([self._root])
        while len(queue) != 0:
            tmp = queue.popleft()
            added_size = (
                self.node_size(tmp.left) + self.node_size(tmp.right) + 1)
            if tmp.size != added_size:
                return False
            if tmp.left:
                queue.append(tmp.left)
            if tmp.right:
                queue.append(tmp.right)
        return True

    # 3.2.30 practice, check if each node in binary search tree is ordered
    # (less than right node and greater than left node)
    def is_ordered(self) -> bool:
        """Check if all elements in binary tree are ordered.

        Returns:
            bool: True if all elements are ordered else False
        """
        queue = Deque([self._root])
        while len(queue) != 0:
            tmp = queue.popleft()
            if tmp.left and tmp.key < tmp.left.key:
                return False
            if tmp.right and tmp.key > tmp.right.key:
                return False
            if tmp.left:
                queue.append(tmp.left)
            if tmp.right:
                queue.append(tmp.right)
        return True

    # 3.2.31 practice
    def is_no_duplicated(self) -> bool:
        """Check if binary tree contains duplicated key nodes.

        Returns:
            bool: True if binary doesn't contain duplicated nodes else False.

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.is_no_duplicated()
        True
        """
        keys = set()
        queue = Deque([self._root])
        while len(queue) != 0:
            tmp = queue.popleft()
            if tmp.key in keys:
                return False
            keys.add(tmp.key)
            if tmp.left:
                queue.append(tmp.left)
            if tmp.right:
                queue.append(tmp.right)
        return True

    # 3.2.32 practice, check if a data structure is binary search tree.
    def check(self) -> bool:
        """Check if binary tree is valid.

        Returns:
            bool: True if binary tree is valid else False
        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.check()
        True
        """
        if not self.is_binary_tree():
            return False
        if not self.is_ordered():
            return False
        if not self.is_no_duplicated():
            return False
        return True

    # 3.2.33 practice, check if each node's rank is correct.
    def is_rank_consistent(self) -> bool:
        """Check if node's rank is equals to node's size.

        Returns:
            bool: True if all nodes' are consistent else False

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> bst.is_rank_consistent()
        True
        """
        for i in range(self.size()):
            if i != self.rank(self.select(i).key):
                return False

        for key in self.keys():
            if key != self.select(self.rank(key)).key:
                return False
        return True

    # 3.2.36 practice
    def keys_iteration(self) -> Iterable[Node]:
        """Return all keys in binary tree

        Returns:
            List[CT]: list of all keys

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> ''.join(char.key for char in bst.keys_iteration())
        'EASQYIUOTN'
        """
        return self.keys_range_iteration(
            self.min_val().key, self.max_val().key)

    def keys_range_iteration(self, low: CT, high: CT) -> Iterable[Node]:
        """Return keys between `low` and `high` in binary tree.

        Args:
            low (CT): low key
            high (CT): high key

        Returns:
            List[CT]: list of keys

        >>> bst = BST()
        >>> test_str = 'EASYQUESTION'
        >>> for (index, element) in enumerate(test_str):
        ...     bst.put(element, index)
        ...
        >>> ''.join(char.key for char in bst.keys_range_iteration('A', 'O'))
        'EAION'
        """
        queue = Deque([self._root])
        while len(queue) != 0:
            tmp = queue.popleft()
            if low <= tmp.key and high >= tmp.key:
                yield tmp
            if tmp.left:
                queue.append(tmp.left)
            if tmp.right:
                queue.append(tmp.right)


if __name__ == '__main__':
    doctest.testmod()
