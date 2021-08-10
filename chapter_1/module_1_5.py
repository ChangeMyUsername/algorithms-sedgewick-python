# !/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random
from typing import Optional


class UnionFind(object):

    """Union find implementation.
    """

    def __init__(self, size: int) -> None:
        """Union–Find data type initialization,
        inital number of sets is the nodes size.

        Args:
            size (int): number of nodes
        """
        self._id = [i for i in range(size)]
        self._count = size

    def count(self) -> int:
        """Returns the number of sets

        Returns:
            int: number of sets
        """
        return self._count

    def validate(self, node: int) -> bool:
        """Validate if node in Union-Find data type.

        Args:
            node (int): node to validate

        Returns:
            bool: [description]

        >>> uf = UnionFind(10)
        >>> uf.validate(10)
        False
        >>> uf.validate(-1)
        False
        >>> uf.validate(9)
        True
        """
        if 0 <= node and node < len(self._id):
            return True
        return False

    def find(self, node: int) -> Optional[int]:
        """Find canonical element of the set where `node` belongs,
        if `node` not in Union-Find, will return None.

        Args:
            node (int): node to find

        Returns:
            int: canonical element of the set where `node` belongs.

        >>> uf = UnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     uf.union(i, j)
        ...
        >>> uf.find(4)
        8
        >>> uf.find(8)
        8
        >>> uf.find(7)
        1
        >>> uf.find(6)
        1
        """
        is_validated = self.validate(node)
        if not is_validated:
            return None

        root = node
        while root != self._id[root]:
            root = self._id[root]
        # 1.5.12 practice
        while node != root:
            new_node = self._id[node]
            self._id[node] = root
            node = new_node
        return root

    def connected(self, p: int, q: int) -> bool:
        """To check if element `p` and `q` is connected.

        Args:
            p (int): one element
            q (int): the other element

        Returns:
            bool: True if connected else False

        >>> uf = UnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     uf.union(i, j)
        ...
        >>> uf.connected(1, 4)
        False
        >>> uf.connected(8, 4)
        True
        >>> uf.connected(1, 5)
        True
        >>> uf.connected(1, 7)
        True
        """
        is_p_valid = self.validate(p)
        is_q_valid = self.validate(q)
        if not (is_p_valid and is_q_valid):
            return False

        return self.find(p) == self.find(q)

    def union(self, p: int, q: int) -> None:
        """Connect the set containing `p` to the set
        containing `q`.

        Args:
            p (int): one element
            q (int): the other element

        >>> uf = UnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     uf.union(i, j)
        ...
        >>> uf.count()
        2
        """
        p_root = self.find(p)
        q_root = self.find(q)
        # validation failed
        if p_root is None or q_root is None:
            return

        if p_root == q_root:
            return
        self._id[p_root] = q_root
        self._count -= 1


class WeightedUnionFind(object):

    """
      Weighted union find algorithm, merge small set
      into large set to lower the set height to greatly improve
      algorithm's performance.
    """

    def __init__(self, size: int) -> None:
        """Weighted union-find initialization

        Args:
            size (int): number of nodes
        """
        self._count = size
        self._id = [i for i in range(size)]
        self._size = [1] * size

    def validate(self, node: int) -> bool:
        """Validate if node in Union-Find data type.

        Args:
            node (int): node to validate

        Returns:
            bool: True if node is valid else False

        >>> wuf = WeightedUnionFind(10)
        >>> wuf.validate(10)
        False
        >>> wuf.validate(-1)
        False
        >>> wuf.validate(9)
        True
        """
        if 0 <= node and node < len(self._id):
            return True
        return False

    def count(self) -> int:
        """Return the number of sets in Union-Find data type.

        Returns:
            int: number of sets
        """
        return self._count

    def connected(self, p: int, q: int) -> bool:
        """To check if element `p` and `q` is connected.

        Args:
            p (int): one element
            q (int): the other element

        Returns:
            bool: True if connected else False

        >>> wuf = WeightedUnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     wuf.union(i, j)
        ...
        >>> wuf.connected(1, 4)
        False
        >>> wuf.connected(8, 4)
        True
        >>> wuf.connected(1, 5)
        True
        >>> wuf.connected(1, 7)
        True
        """
        is_p_valid = self.validate(p)
        is_q_valid = self.validate(q)
        if not (is_p_valid and is_q_valid):
            return False

        return self.find(p) == self.find(q)

    def find(self, node: int) -> Optional[int]:
        """Find canonical element of the set where `node` belongs,
        if `node` not in Union-Find, will return None.

        Args:
            node (int): node to find

        Returns:
            int: canonical element of the set where `node` belongs.

        >>> wuf = WeightedUnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     wuf.union(i, j)
        ...
        >>> wuf.find(4)
        4
        >>> wuf.find(8)
        4
        >>> wuf.find(7)
        6
        >>> wuf.find(6)
        6
        """
        is_validated = self.validate(node)
        if not is_validated:
            return None

        root = node
        while root != self._id[root]:
            root = self._id[root]
        return root

    def union(self, p: int, q: int) -> None:
        """Connect the set containing `p` to the set
        containing `q`.

        Args:
            p (int): one element
            q (int): the other element

        >>> wuf = WeightedUnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     wuf.union(i, j)
        ...
        >>> wuf.count()
        2
        """
        p_root = self.find(p)
        q_root = self.find(q)
        # validation failed
        if p_root is None or q_root is None:
            return
        if p_root == q_root:
            return

        if self._size[p_root] < self._size[q_root]:
            self._id[p_root] = q_root
            self._size[q_root] += self._size[p_root]
        else:
            self._id[q_root] = p_root
            self._size[p_root] += self._size[q_root]
        self._count -= 1


# 1.5.14 practice
class HeightedUnionFind(object):

    """
      Heighted union find algorithm,
    put the shorter tree into taller tree,
    the tree's height won't be taller than log(n).
    """

    def __init__(self, size: int) -> None:
        """Heighted Union-Find initialization

        Args:
            size (int): number of nodes
        """
        self._id = [i for i in range(size)]
        self._height = [1] * size
        self._count = size

    def validate(self, node: int) -> bool:
        """Validate if node in Union-Find data type.

        Args:
            node (int): node to validate

        Returns:
            bool: True if node is valid else False

        >>> huf = HeightedUnionFind(10)
        >>> huf.validate(10)
        False
        >>> huf.validate(-1)
        False
        >>> huf.validate(9)
        True
        """
        if 0 <= node and node < len(self._id):
            return True
        return False

    def count(self) -> int:
        """Return the number of sets in Union-Find data type.

        Returns:
            int: number of sets
        """
        return self._count

    def find(self, node: int) -> Optional[int]:
        """Find canonical element of the set where `node` belongs,
        if `node` not in Union-Find, will return None.

        Args:
            node (int): node to find

        Returns:
            int: canonical element of the set where `node` belongs.

        >>> huf = HeightedUnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     huf.union(i, j)
        ...
        >>> huf.find(4)
        4
        >>> huf.find(8)
        4
        >>> huf.find(7)
        6
        >>> huf.find(6)
        6
        >>> huf.find(11)
        """
        is_validated = self.validate(node)
        if not is_validated:
            return None

        while node != self._id[node]:
            node = self._id[node]
        return node

    def connected(self, p: int, q: int) -> bool:
        """To check if element `p` and `q` is connected.

        Args:
            p (int): one element
            q (int): the other element

        Returns:
            bool: True if connected else False

        >>> huf = HeightedUnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     huf.union(i, j)
        ...
        >>> huf.connected(1, 4)
        False
        >>> huf.connected(8, 4)
        True
        >>> huf.connected(1, 5)
        True
        >>> huf.connected(1, 7)
        True
        """
        is_p_valid = self.validate(p)
        is_q_valid = self.validate(q)
        if not (is_p_valid and is_q_valid):
            return False

        return self.find(p) == self.find(q)

    def union(self, p: int, q: int) -> None:
        """Connect the set containing `p` to the set
        containing `q`.

        Args:
            p (int): one element
            q (int): the other element

        >>> huf = HeightedUnionFind(10)
        >>> connections = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1),
        ... (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
        >>> for i, j in connections:
        ...     huf.union(i, j)
        ...
        >>> huf.count()
        2
        """
        p_root = self.find(p)
        q_root = self.find(q)
        if p_root == q_root:
            return
        if self._height[p_root] < self._height[q_root]:
            self._id[p_root] = q_root
        elif self._height[p_root] > self._height[q_root]:
            self._id[q_root] = p_root
        else:
            self._id[q_root] = p_root
            self._height[p_root] += 1
        self._count -= 1


# 1.5.17 practice
def erdos_renyi(size):
    """
    >>> erdos_renyi(1000)
    """
    uf = UnionFind(size)
    while uf.count() > 1:
        a = random.randint(0, size - 1)
        b = random.randint(0, size - 1)
        if a == b:
            continue
        if not uf.connected(a, b):
            uf.union(a, b)


if __name__ == '__main__':
    doctest.testmod()
