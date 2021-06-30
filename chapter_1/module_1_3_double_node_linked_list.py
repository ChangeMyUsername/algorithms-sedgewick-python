#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
from __future__ import print_function

import doctest
from typing import Any, Iterator

from common import DoubleNode


# 1.3.31 practice
class DoubleLinkedList(object):

    """
      The double-node linked list implementation
      which the node has prev and next attribute.
    """

    def __init__(self) -> None:
        """Initialize method"""
        self._first = self._last = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        tmp = self._first
        while tmp:
            yield tmp.val
            tmp = tmp.next

    def is_empty(self) -> bool:
        """Check if double linked list is empty.

        Returns:
            bool: True if double linked list is empty else False
        """
        return self._first is None

    def size(self) -> int:
        """Return the size of double linked list.

        Returns:
            int: size of double linked list
        """
        return self._size

    def print_list(self) -> None:
        """Print all elements in linked list."""
        tmp = self._first
        while tmp:
            if not tmp.next:
                print(tmp.val)
            else:
                print(tmp.val, end=' ')
            tmp = tmp.next

    def push_front(self, item: Any) -> None:
        """Add element in front of double linked list.

        Args:
            item (Any): item to prepend

        >>> lst = DoubleLinkedList()
        >>> for i in range(10):
        ...     lst.push_front(i)
        ...
        >>> lst.print_list()
        9 8 7 6 5 4 3 2 1 0
        >>> lst.size()
        10
        >>> lst.is_empty()
        False
        """
        old = self._first
        self._first = DoubleNode(item)
        self._first.next = old
        if old:
            old.prev = self._first
        else:
            self._last = self._first
        self._size += 1

    def push_back(self, item: Any) -> None:
        """Append item to double linked list

        Args:
            item (Any): item to append

        >>> lst = DoubleLinkedList()
        >>> for i in range(10):
        ...     lst.push_back(i)
        ...
        >>> lst.print_list()
        0 1 2 3 4 5 6 7 8 9
        >>> lst.size()
        10
        >>> lst.is_empty()
        False
        """
        old = self._last
        self._last = DoubleNode(item)
        self._last.prev = old
        if old:
            old.next = self._last
        else:
            self._first = self._last
        self._size += 1

    def pop_front(self) -> Any:
        """Remove first element from double linked list.

        Returns:
            Any: element value to remove

        >>> lst = DoubleLinkedList()
        >>> for i in range(10):
        ...     lst.push_back(i)
        ...
        >>> lst.pop_front()
        0
        >>> lst.pop_front()
        1
        >>> lst.print_list()
        2 3 4 5 6 7 8 9
        """
        if self._first:
            old = self._first
            self._first = self._first.next
            old.next = None
            if self._first:
                self._first.prev = None
            else:
                self._last = None
            self._size -= 1
            return old.val
        return None

    def pop_back(self) -> Any:
        """Remove last element from double linked list

        Returns:
            Any: element value to remove

        >>> lst = DoubleLinkedList()
        >>> for i in range(10):
        ...     lst.push_back(i)
        ...
        >>> lst.pop_back()
        9
        >>> lst.pop_back()
        8
        >>> lst.print_list()
        0 1 2 3 4 5 6 7
        """
        if self._last:
            old = self._last
            self._last = self._last.prev
            old.prev = None
            if self._last:
                self._last.next = None
            else:
                self._first = None
            self._size -= 1
            return old.val
        return None

    def insert_before(self, target_value: Any, new_node: DoubleNode) -> None:
        """Insert `new_node` into double linked list before `target_value`,
           if `target_value` not exists, then do noting.

        Args:
            target_value (Any): existing element in double linked list
            new_node (DoubleNode): new element to insert

        >>> lst = DoubleLinkedList()
        >>> for i in range(10):
        ...     lst.push_back(i)
        ...
        >>> lst.insert_before(11, DoubleNode(9.9))
        >>> lst.print_list()
        0 1 2 3 4 5 6 7 8 9
        >>> lst.insert_before(2, DoubleNode(1.5))
        >>> lst.print_list()
        0 1 1.5 2 3 4 5 6 7 8 9
        >>> lst.insert_before(0, DoubleNode(-1))
        >>> lst.print_list()
        -1 0 1 1.5 2 3 4 5 6 7 8 9
        """
        tmp = self._first
        while tmp and tmp.val != target_value:
            tmp = tmp.next

        if not tmp:
            return

        if not tmp.prev:
            tmp.prev = new_node
            new_node.next = tmp
            self._first = new_node
            self._size += 1
            return

        prev_node = tmp.prev
        prev_node.next = new_node
        new_node.prev = prev_node

        tmp.prev = new_node
        new_node.next = tmp

        self._size += 1

    def insert_after(self, target_value: Any, new_node: DoubleNode) -> None:
        """Insert `new_node` into double linked list after `target_value`,
           if `target_value` not exists, then do noting.

        Args:
            target_value (Any): existing element value in double linked list
            new_node (DoubleNode): new node to insert

        >>> lst = DoubleLinkedList()
        >>> for i in range(10):
        ...     lst.push_back(i)
        ...
        >>> lst.insert_after(11, DoubleNode(9.9))
        >>> lst.print_list()
        0 1 2 3 4 5 6 7 8 9
        >>> lst.insert_after(2, DoubleNode(2.5))
        >>> lst.print_list()
        0 1 2 2.5 3 4 5 6 7 8 9
        >>> lst.insert_after(9, DoubleNode(9.9))
        >>> lst.print_list()
        0 1 2 2.5 3 4 5 6 7 8 9 9.9
        """
        tmp = self._first
        while tmp and tmp.val != target_value:
            tmp = tmp.next

        if not tmp:
            return

        if not tmp.next:
            tmp.next = new_node
            new_node.prev = tmp
            self._last = new_node
            self._size += 1
            return

        next_node = tmp.next
        next_node.prev = new_node
        new_node.next = next_node

        tmp.next = new_node
        new_node.prev = tmp

        self._size += 1

    def remove(self, item: Any) -> None:
        """Remove element from double linked list.

        Args:
            item (Any): element value to remove

        >>> lst = DoubleLinkedList()
        >>> for i in range(10):
        ...     lst.push_back(i)
        ...
        >>> lst.remove(8)
        >>> lst.print_list()
        0 1 2 3 4 5 6 7 9
        >>> lst.push_back(0)
        >>> lst.remove(0)
        >>> lst.print_list()
        1 2 3 4 5 6 7 9
        >>> lst2 = DoubleLinkedList()
        >>> for i in (0, 0, 0, 1, 1):
        ...     lst2.push_back(i)
        ...
        >>> lst2.remove(0)
        >>> lst2.remove(1)
        >>> lst2.print_list()
        >>> lst2.size()
        0
        """
        if not self._first.next and self._first.val == item:
            self._first = None
            self._size = 0
            return

        tmp = self._first
        while tmp:
            if tmp.val == item:
                prev_node = tmp.prev
                next_node = tmp.next
                # cut all tmp node connection
                tmp.next = tmp.prev = None
                if prev_node:
                    prev_node.next = next_node
                else:
                    # this is first element, need to set
                    # self._first to `next_node`
                    self._first = next_node
                if next_node:
                    next_node.prev = prev_node
                else:
                    # this is last element, need to set
                    # self._last as `prev_node`
                    self._last = prev_node
                tmp = next_node
                self._size -= 1
            else:
                tmp = tmp.next


if __name__ == '__main__':
    doctest.testmod()
