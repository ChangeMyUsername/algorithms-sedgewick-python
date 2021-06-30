#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
from __future__ import print_function

import doctest
from typing import Any, Union

from common import Node


class LinkedList(object):

    """
        Linked list practice
    """

    def __init__(self) -> None:
        """
            Initialize method
        """
        self._first = None
        self._size = 0

    def print_list(self) -> None:
        """Print all elements in linked list.
        >>> lst = LinkedList()
        >>> for i in range(1, 5):
        ...     lst.append(i)
        ...
        >>> lst.print_list()
        1 2 3 4
        """
        tmp = self._first
        while tmp:
            if not tmp.next_node:
                print(tmp.val)
            else:
                print(tmp.val, end=' ')
            tmp = tmp.next_node

    def append(self, val: Any) -> None:
        """Append element to linked list.

        Args:
            val (Any): element to be appended

        >>> lst = LinkedList()
        >>> for i in range(1, 5):
        ...     lst.append(i)
        ...
        >>> lst.size()
        4
        """
        if not self._first:
            self._first = Node(val)
            self._size += 1
            return
        tmp = self._first
        while tmp.next_node:
            tmp = tmp.next_node
        tmp.next_node = Node(val)
        self._size += 1

    # 1.3.19 practice
    def delete_last(self) -> Union[None, Any]:
        """Delete last item in linked list.

        Returns:
            Union[None, Any]: None if linked list is empty,
                              else last element in linked list

        >>> lst = LinkedList()
        >>> for i in range(1, 5):
        ...     lst.append(i)
        ...
        >>> while lst.size():
        ...     lst.delete_last()
        4
        3
        2
        1
        """
        tmp = self._first
        if not tmp:
            return
        if not self._first.next_node:
            deleted_val = self._first.val
            self._first = None
            self._size -= 1
            return deleted_val
        while tmp.next_node.next_node:
            tmp = tmp.next_node
        deleted_val = tmp.next_node.val
        tmp.next_node = None
        self._size -= 1
        return deleted_val

    # 1.3.21 practice
    def find(self, val: Any) -> bool:
        """Find if `val` in linked list.

        Args:
            val (Any): element to search in linked list

        Returns:
            bool: True if `val` in linked list else False

        >>> lst = LinkedList()
        >>> for i in range(1, 5):
        ...     lst.append(i)
        ...
        >>> lst.find(5)
        False
        >>> lst.find(4)
        True
        >>> lst.find(1)
        True
        """
        tmp = self._first
        while tmp:
            if tmp.val == val:
                return True
            tmp = tmp.next_node
        return False

    def size(self) -> int:
        """Return the size of linked list

        Returns:
            int: size of linked list
        """
        return self._size

    # 1.3.20 practice
    def delete(self, pos: int) -> None:
        """Delete element from linked list
           which element in n position (1-based).

        Args:
            pos (int): linked list position, if `pos` > self.size(),
                       then do nothing.
        >>> lst = LinkedList()
        >>> for i in range(1, 5):
        ...     lst.append(i)
        ...
        >>> lst.delete(1)
        >>> lst.print_list()
        2 3 4
        >>> lst.delete(4)
        >>> lst.print_list()
        2 3 4
        >>> lst.delete(2)
        >>> lst.print_list()
        2 4
        """
        if pos > self._size:
            return
        if pos == 1:
            self._first = self._first.next_node
            self._size -= 1
            return
        tmp, count = self._first, 1
        while count != pos - 1:
            count += 1
            tmp = tmp.next_node
        target = tmp.next_node
        tmp.next_node = tmp.next_node.next_node
        target.next_node = None
        self._size -= 1

    # 1.3.24 practice, accept val as parameter instead of node as parameter
    def remove_after(self, item: Any) -> None:
        """Remove element after `item`.

        Args:
            item (Any): element value in linked list

        >>> lst = LinkedList()
        >>> for i in range(10):
        ...     lst.append(i)
        ...
        >>> lst.remove_after(8)
        >>> lst.remove_after(0)
        >>> lst.print_list()
        0 2 3 4 5 6 7 8
        >>> lst.size()
        8
        """
        tmp = self._first
        while tmp.next_node:
            if tmp.val == item:
                tmp.next_node = tmp.next_node.next_node
                self._size -= 1
                break
            tmp = tmp.next_node

    # 1.3.25 practice, accept val as parameter instead of node as parameter
    def insert_after(self, current_node_item: Any, new_node_item: Any) -> None:
        """Insert `new_node_item` into linked list after `current_node_item`.

        Args:
            current_node_item (Any): existing element value
            new_node_item (Any): new element value
        >>> lst = LinkedList()
        >>> for i in range(10):
        ...     lst.append(i)
        ...
        >>> lst.insert_after(0, 1.5)
        >>> lst.print_list()
        0 1.5 1 2 3 4 5 6 7 8 9
        >>> lst.insert_after(9, 10)
        >>> lst.print_list()
        0 1.5 1 2 3 4 5 6 7 8 9 10
        """
        tmp = self._first
        while tmp:
            if tmp.val == current_node_item:
                old_next_node = tmp.next_node
                new_node = Node(new_node_item)
                tmp.next_node = new_node
                new_node.next_node = old_next_node
                self._size += 1
                break
            tmp = tmp.next_node

    # 1.3.26 practice
    def remove(self, key: Any) -> int:
        """Remove all `key` from linked list.

        Args:
            key (Any): element to be removed

        Returns:
            int: removed elements count

        >>> lst = LinkedList()
        >>> for i in range(10):
        ...     lst.append(i)
        >>> lst.append(8)
        >>> lst.append(1)
        >>> lst.remove(1)
        2
        >>> lst.remove(8)
        2
        >>> lst.print_list()
        0 2 3 4 5 6 7 9
        >>> lst2 = LinkedList()
        >>> for i in range(5):
        ...    lst2.append(i)
        >>> lst2.remove(3)
        1
        >>> lst2.remove(3)
        0
        >>> lst3 = LinkedList()
        >>> lst3.append(1)
        >>> lst3.remove(1)
        1
        """
        removed_num = 0

        tmp = self._first
        prev = None
        while tmp:
            if tmp.val == key:
                if not prev:
                    target = tmp
                    tmp = tmp.next_node
                    target.next_node = None
                else:
                    prev.next_node = tmp.next_node
                self._size -= 1
                removed_num += 1
            prev = tmp
            if tmp:
                tmp = tmp.next_node
        return removed_num

    # 1.3.27 practice
    def max_value(self) -> Any:
        """Return maximum value in linked list, each value must be comparable.

        Returns:
            Any: maximum value in linked list, None if linked list is empty

        >>> lst = LinkedList()
        >>> for i in range(10):
        ...     lst.append(i)
        >>> lst.max_value()
        9
        """
        tmp = self._first
        max_val = None
        while tmp:
            if max_val is None:
                max_val = tmp.val
            if tmp.val > max_val:
                max_val = tmp.val
            tmp = tmp.next_node
        return max_val

    # 1.3.30 practice
    def reverse(self) -> Node:
        """Reverse linked list and return first node.

        Returns:
            Node: reversed first node

        >>> lst = LinkedList()
        >>> for i in range(10):
        ...     lst.append(i)
        >>> lst.print_list()
        0 1 2 3 4 5 6 7 8 9
        >>> lst.reverse().val
        9
        >>> lst.print_list()
        9 8 7 6 5 4 3 2 1 0
        """
        first = self._first
        reverse_node = None
        while first:
            second = first.next_node
            first.next_node = reverse_node
            reverse_node = first
            first = second
        self._first = reverse_node
        return reverse_node

    def is_cyclic(self) -> bool:
        if not self._first:
            return False
        fast = second = self._first
        while fast and fast.next_node:
            fast = fast.next_node.next_node
            second = second.next_node
            if fast == second:
                return True
        return False


if __name__ == '__main__':
    doctest.testmod()
