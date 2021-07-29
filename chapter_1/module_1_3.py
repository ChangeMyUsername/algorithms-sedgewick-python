#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
from __future__ import annotations, print_function

import doctest
import random
import string
from abc import ABCMeta, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional, Union

from common import DoubleNode, Node


class BaseDataType(metaclass=ABCMeta):
    """
        Abstract class for stack, queue or other collection type.
    """
    @abstractmethod
    def __iter__(self):
        while True:
            yield None

    @abstractmethod
    def size(self):
        return NotImplemented

    @abstractmethod
    def is_empty(self):
        return NotImplemented


class Stack(object):
    """Stack, a LIFO data structure with linked list implementation."""

    # 1.3.42 practice
    def __init__(self, old_stack: Stack) -> None:
        """Initial method, use `_first` to mark head of linked list,
           use `_size` to keep track of linked-list size.
           >>> s = Stack()
           >>> s._first
           >>> s._size
           0
        """
        self._first = None
        self._size = 0
        if isinstance(old_stack, Stack) and not old_stack.is_empty():
            for item in old_stack:
                self.push(item)

    def __iter__(self) -> Iterator[Any]:
        """Iterate all elements of current stack.

        Yields:
            Any: elements of stack, can be any data type of elements
        >>> s = Stack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.push(3)
        >>> s.push(4)
        >>> for item in s:
        ...     print(item)
        ...
        4
        3
        2
        1
        """
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self) -> bool:
        """Check if stack is empty or not.

        Returns:
            bool: True if stack is empty else False
        """
        return self._first is None

    def size(self) -> int:
        """Return the size of stack.

        Returns:
            int: size of stack
        """
        return self._size

    def push(self, val: Any) -> None:
        """Push `val` into stack, and `val` becomes the top element.

        Args:
            val (Any): element to be pushed into stack

        >>> s = Stack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.push(3)
        >>> s.size()
        3
        """
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def pop(self) -> Any:
        """Pop out the top element in the stack.

        Returns:
            Any: popped out element

        >>> s = Stack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.push(3)
        >>> s.pop()
        3
        >>> s.size()
        2
        """
        if self._first:
            old = self._first
            self._first = self._first.next_node
            self._size -= 1
            return old.val
        return None

    # 1.3.7 practice
    def peek(self) -> Any:
        """Return the top element in stack.

        Returns:
            Any: top element in stack
        >>> s = Stack()
        >>> s.peek()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.push(3)
        >>> s.peek()
        3
        >>> s.pop()
        3
        >>> s.peek()
        2
        """
        if self._first:
            return self._first.val
        return None

    # 1.3.12 practice
    @staticmethod
    def copy(stack: Stack) -> Stack:
        """Copy existing stack and return new stack.

        Args:
            stack (Stack): existing stack

        Returns:
            Stack: new stack

        >>> old_stack = Stack()
        >>> old_stack.push(1)
        >>> old_stack.push(2)
        >>> old_stack.push(3)
        >>> old_stack.push(4)
        >>> new_stack = Stack.copy(old_stack)
        >>> [item for item in new_stack]
        [1, 2, 3, 4]
        """
        new_stack = Stack()
        for item in stack:
            new_stack.push(item)
        return new_stack


class BaseConverter(object):

    """
      Convert decimal number to x base number with stack.
    """
    digits = '0123456789ABCDEF'

    @staticmethod
    def convert_decimal_integer(dec_num: int, base: int) -> str:
        """Convert decimal number to x base number with stack.

        Args:
            dec_num (int): decimal number to be converted
            base (int): base number, maximum base number is 16

        Returns:
            str: n-base number as string format

        >>> BaseConverter.convert_decimal_integer(50, 2)
        '110010'
        >>> BaseConverter.convert_decimal_integer(8, 2)
        '1000'
        >>> BaseConverter.convert_decimal_integer(15, 16)
        'F'
        >>> BaseConverter.convert_decimal_integer(9, 8)
        '11'
        >>> BaseConverter.convert_decimal_integer(99, 7)
        '201'
        >>> BaseConverter.convert_decimal_integer(99, 9)
        '120'
        """
        stack = Stack()
        while dec_num:
            stack.push(dec_num % base)
            dec_num //= base
        res = []
        while not stack.is_empty():
            res.append(BaseConverter.digits[stack.pop()])
        return ''.join(res)


class Evaluate(object):

    """
      Dijkstra Shunting-yard algorithm variant
    """

    def __init__(self) -> None:
        """
            Initialize method.
        """
        self._ops_stack = Stack()
        self._vals_stack = Stack()
        self._ops_char = ('+', '-', '*', '/', '√')

    def calculate(self, infix_string: str) -> int:
        """Dijkstra Shunting-yard algorithm, but the output is
           the result of given mathematical expression,
           `infix_string` can support space character.

        Args:
            infix_string (str): infix string

        Returns:
            int: calculated result

        >>> evaluate = Evaluate()
        >>> evaluate.calculate('(1+((2+3)*(4*5)))')
        101.0
        >>> evaluate.calculate('((1-2)*(8/4))')
        -2.0
        >>> evaluate.calculate('((1 - 2) * (8 / 4))')
        -2.0
        """
        for i in infix_string:
            if i in self._ops_char:
                self._ops_stack.push(i)
            elif i == '(' or i == ' ':
                continue
            elif i == ')':
                ops = self._ops_stack.pop()
                val = self._vals_stack.pop()
                if ops == '+':
                    val += self._vals_stack.pop()
                elif ops == '-':
                    val = self._vals_stack.pop() - val
                elif ops == '*':
                    val *= self._vals_stack.pop()
                elif ops == '/':
                    val = float(self._vals_stack.pop()) / val
                self._vals_stack.push(val)
            else:
                self._vals_stack.push(float(i))
        return self._vals_stack.pop()


class Queue(object):

    """
      Queue FIFO data structure linked-list implementation.
    """

    # 1.3.41 practice
    def __init__(self, exist_queue: Optional['Queue'] = None) -> None:
        """Initial method for queue, if `exist_queue` is not None,
           then copy all elements to current queue.

        Args:
            exist_queue ([Queue], optional): Existing Queue object.
                                             Defaults to None.

        >>> old = Queue()
        >>> for i in range(5):
        ...     old.enqueue(i)
        ...
        >>> new_queue = Queue(old)
        >>> [i for i in new_queue]
        [0, 1, 2, 3, 4]
        >>> new_queue.enqueue(6)
        >>> [i for i in old]
        [0, 1, 2, 3, 4]
        >>> [i for i in new_queue]
        [0, 1, 2, 3, 4, 6]
        """
        self._first = None
        self._last = None
        self._size = 0
        if exist_queue:
            for item in exist_queue:
                self.enqueue(item)

    def __iter__(self) -> Iterator[Any]:
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self) -> bool:
        """Check if queue is empty.

        Returns:
            bool: True if queue is empty else False

        >>> queue = Queue()
        >>> queue.is_empty()
        True
        >>> queue.enqueue('a')
        >>> queue.is_empty()
        False
        """
        return self._first is None

    def size(self) -> int:
        """Return the size of queue.

        Returns:
            int: the size of queue

        >>> queue = Queue()
        >>> queue.size()
        0
        >>> queue.enqueue('b')
        >>> queue.size()
        1
        """
        return self._size

    def enqueue(self, val: Any) -> None:
        """Append element to queue.

        Args:
            val (Any): element to be appended

        >>> queue = Queue()
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> queue.enqueue(3)
        >>> queue.enqueue(4)
        >>> queue.size()
        4
        """
        old_last = self._last
        self._last = Node(val)
        self._last.next_node = None
        if self.is_empty():
            self._first = self._last
        else:
            old_last.next_node = self._last
        self._size += 1

    def dequeue(self) -> Union[Any, None]:
        """Remove element from the head of queue,
           if queue is empty, return None.

        Returns:
            Union[Any, None]: dequeued element, if queue is empty,
                              then return None

        >>> queue = Queue()
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> queue.enqueue(3)
        >>> queue.enqueue(4)
        >>> queue.dequeue()
        1
        >>> queue.dequeue()
        2
        >>> queue.dequeue()
        3
        >>> queue.dequeue()
        4
        >>> queue.dequeue()
        >>> queue.dequeue()
        >>> queue.size()
        0
        """
        if not self.is_empty():
            val = self._first.val
            self._first = self._first.next_node
            if self.is_empty():
                self._last = None
            self._size -= 1
            return val
        return None


class Bag(object):
    """
        Bag data structure with linked-list implementation.
    """

    def __init__(self) -> None:
        """Intial method
        """
        self._first = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterator method, yields each elements in bag

        Yields:
            Iterator[Any]: element in bag
        """
        node = self._first
        while node is not None:
            yield node.val
            node = node.next_node

    def add(self, val: Any) -> None:
        """Prepend element to bag

        Args:
            val (Any): element to be inserted

        >>> bag = Bag()
        >>> for i in range(1, 6):
        ...     bag.add(i)
        ...
        >>> bag.size()
        5
        >>> [i for i in bag]
        [5, 4, 3, 2, 1]
        """
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def is_empty(self) -> bool:
        """Check if bag is empty

        Returns:
            bool: True if bag is empty else False
        >>> bag = Bag()
        >>> bag.is_empty()
        True
        """
        return self._first is None

    def size(self) -> int:
        """Return the size of bag

        Returns:
            int: the size of bag
        >>> bag = Bag()
        >>> bag.size()
        0
        """
        return self._size


# stack example
# 1.3.4 practice
class Parentheses(object):
    """
        Using stack data structure for judging if parenthese is symmetric.
    """

    def __init__(self) -> None:
        self._left_parenthese_stack = Stack()
        self._left_parentheses = ('[', '{', '(')
        self._right_parentheses = (']', '}', ')')

    def __is_match(self, left_parenthese: str, right_parenthese: str) -> bool:
        return (self._left_parentheses.index(left_parenthese) ==
                self._right_parentheses.index(right_parenthese))

    def is_parenthese_symmetric(self, parenthese_string: str) -> bool:
        """Using stack data structure for judging if parenthese is symmetric.

        Args:
            parenthese_string (str): input string with all parentheses

        Returns:
            bool: True if parenthese string are symmetric else False

        >>> p = Parentheses()
        >>> p.is_parenthese_symmetric('[()]{}{[()()]()}')
        True
        >>> p.is_parenthese_symmetric('[(])}}{}{]])')
        False
        >>> p.is_parenthese_symmetric('{{{{}}}')
        False
        >>> p.is_parenthese_symmetric('{}}}}}}}{{{')
        False
        """
        for s in parenthese_string:
            if s in self._left_parentheses:
                self._left_parenthese_stack.push(s)
            elif s in self._right_parentheses:
                if self._left_parenthese_stack.is_empty():
                    return False
                result = self.__is_match(self._left_parenthese_stack.peek(), s)
                if result:
                    self._left_parenthese_stack.pop()
        return self._left_parenthese_stack.is_empty()


# stack example
# 1.3.5 practice
def get_binary(integer):
    '''
      Using stack for getting integer binary representation.
    >>> get_binary(50)
    '110010'
    >>> get_binary(8)
    '1000'
    '''
    s = Stack()
    while integer:
        s.push(integer % 2)
        integer //= 2
    return ''.join([str(i) for i in s])


# 1.3.9 practice
class CompleteInfixString(object):

    """
        Using stack for complete infix string,
        the basic principle is similar to dijkstra infix arithmetic algorithm.
    """

    def __init__(self) -> None:
        """Initialize method"""
        self._ops_stack = Stack()
        self._vals_stack = Stack()
        self._ops_char = ('+', '-', '*', '/')

    def complete_string(self, incmplt_string: str) -> str:
        """Complete infix string, `incmplt_string` can not include `(` character.

        Args:
            incmplt_string (str): in-completed infix string

        Returns:
            str: infix string with `(`

        >>> cis = CompleteInfixString()
        >>> cis.complete_string('1+2)*3-4)*5-6)))')
        '((1+2)*((3-4)*(5-6)))'
        """
        for i in incmplt_string:
            if i in self._ops_char:
                self._ops_stack.push(i)
            elif i == ')':
                ops = self._ops_stack.pop()
                val = self._vals_stack.pop()
                new_str = '({}{}{})'.format(self._vals_stack.pop(), ops, val)
                self._vals_stack.push(new_str)
            else:
                self._vals_stack.push(i)
        return self._vals_stack.pop()


# 1.3.10 practice
class InfixToPostfix(object):

    """
      Convert infix string to postfix string using stack.
    """

    operand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    ops = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}

    def __init__(self) -> None:
        """Initialize method"""
        self._ops_stack = Stack()

    def infix_to_postfix(self, infix_string: str) -> str:
        """Convert infix string to postfix string using stack.

        Args:
            infix_string (str): infix string

        Returns:
            str: postfix string

        >>> itp = InfixToPostfix()
        >>> itp.infix_to_postfix("(A+B)*(C+D)")
        'A B + C D + *'
        >>> itp.infix_to_postfix("(A+B)*C")
        'A B + C *'
        >>> itp.infix_to_postfix("A+B*C")
        'A B C * +'
        >>> itp.infix_to_postfix("A*B+C")
        'A B * C +'
        """
        postfix_list = []
        for i in infix_string:
            if i in InfixToPostfix.operand:
                postfix_list.append(i)
            elif i == '(':
                self._ops_stack.push(i)
            elif i == ')':
                token = self._ops_stack.pop()
                while token != '(':
                    postfix_list.append(token)
                    token = self._ops_stack.pop()
            else:
                while (not self._ops_stack.is_empty() and
                       InfixToPostfix.ops[
                           self._ops_stack.peek()] >= InfixToPostfix.ops[i]):
                    postfix_list.append(self._ops_stack.pop())
                self._ops_stack.push(i)

        while not self._ops_stack.is_empty():
            postfix_list.append(self._ops_stack.pop())
        return ' '.join(postfix_list)


# 1.3.11 practice
class PostfixEvaluate(object):

    """
        Using stack for postfix evaluation.
    """

    def __init__(self) -> None:
        """Initialize method"""
        self._operand_stack = Stack()

    def evaluate(self, postfix_string: string) -> float:
        """Using stack for postfix evaluation.

        Args:
            postfix_string (string): postfix string

        Returns:
            float: postfix evaluation

        Using stack for postfix evaluation.
        >>> pfe = PostfixEvaluate()
        >>> pfe.evaluate('78+32+/')
        3.0
        """
        for i in postfix_string:
            if i in string.digits:
                self._operand_stack.push(int(i))
            else:
                v2 = self._operand_stack.pop()
                v1 = self._operand_stack.pop()
                if i == '+':
                    self._operand_stack.push(v1 + v2)
                elif i == '-':
                    self._operand_stack.push(v1 - v2)
                elif i == '*':
                    self._operand_stack.push(v1 * v2)
                elif i == '/':
                    self._operand_stack.push(v1 / v2)
        return self._operand_stack.pop()


# 1.3.32 practice
class Steque(object):

    """
      Steque, combining stack and queue operation.
    """

    def __init__(self):
        """Initialize method"""
        self._top = None
        self._bottom = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        tmp = self._top
        while tmp:
            yield tmp.val
            tmp = tmp.next_node

    def push(self, val: Any) -> None:
        """Add element at the top of steque.

        Args:
            val (Any): element to add

        >>> steque = Steque()
        >>> for i in range(1, 10):
        ...     steque.push(i)
        ...
        >>> [i for i in steque]
        [9, 8, 7, 6, 5, 4, 3, 2, 1]
        """
        old = self._top
        self._top = Node(val)
        self._top.next_node = old
        if old is None:
            self._bottom = self._top
        self._size += 1

    def pop(self) -> Union[None, Any]:
        """Remove top element from steque.

        Returns:
            Union[None, Any]: removed element, None if steque is empty.

        >>> steque = Steque()
        >>> for i in range(1, 10):
        ...     steque.push(i)
        ...
        >>> [steque.pop() for _ in range(1, 10)]
        [9, 8, 7, 6, 5, 4, 3, 2, 1]
        >>> steque.is_empty()
        True
        >>> steque.size()
        0
        >>> steque.pop()
        """
        if self._top:
            out = self._top
            self._top = self._top.next_node
            if self._top is None:
                self._bottom = None
            self._size -= 1
            return out.val
        return None

    def enqueue(self, val: Any) -> None:
        """Append item to steque.

        Args:
            val (Any): element to append

        >>> steque = Steque()
        >>> for i in range(1, 10):
        ...     steque.enqueue(i)
        ...
        >>> [i for i in steque]
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        if not self._bottom:
            self._bottom = self._top = Node(val)
            self._size += 1
            return
        node = Node(val)
        self._bottom.next_node = node
        self._bottom = self._bottom.next_node
        self._size += 1

    def is_empty(self) -> bool:
        """Check if steque is empty

        Returns:
            bool: True if steque is empty else False
        """
        return self._top is None

    def size(self) -> int:
        """Return the size of steque

        Returns:
            int: size of steque
        """
        return self._size


# 1.3.33 practice deque implementation.
class Deque(object):

    '''
      Double queue AKA Deque linked list version, deque iterates
      elements from left to right.
    >>> d = Deque()
    >>> d.push_left(1)
    >>> d.push_right(2)
    >>> d.push_right(3)
    >>> d.push_left(0)
    >>> [i for i in d]
    [0, 1, 2, 3]
    >>> d.pop_left()
    0
    >>> d.pop_right()
    3
    >>> d.pop_left()
    1
    >>> d.pop_left()
    2
    >>> d.is_empty()
    True
    >>> d.size()
    0
    '''

    def __init__(self) -> None:
        """Initial method"""
        self._left = self._right = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        tmp = self._left
        while tmp:
            yield tmp.val
            tmp = tmp.next_node

    def is_empty(self) -> bool:
        """Check if deque is empty

        Returns:
            bool: True if deque is empty else False
        """
        return self._left is None and self._right is None

    def size(self) -> int:
        """Return the size of deque

        Returns:
            int: size of deque
        """
        return self._size

    def push_left(self, item: Any) -> None:
        """Add element from the left of deque.

        Args:
            item (Any): element to add

        >>> deque = Deque()
        >>> for i in range(10):
        ...     deque.push_left(i)
        ...
        >>> deque.size()
        10
        >>> deque.is_empty()
        False
        >>> [i for i in deque]
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        """
        old = self._left
        self._left = Node(item)
        self._left.next_node = old
        if self._right is None:
            self._right = self._left
        self._size += 1

    def push_right(self, item: Any) -> None:
        """Add element from the right of deque.

        Args:
            item (Any): element to add

        >>> deque = Deque()
        >>> for i in range(10):
        ...     deque.push_right(i)
        ...
        >>> deque.size()
        10
        >>> deque.is_empty()
        False
        >>> [i for i in deque]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        old = self._right
        self._right = Node(item)
        if not self._left:
            self._left = self._right
        else:
            old.next_node = self._right
        self._size += 1

    def pop_left(self) -> Any:
        if self._left:
            old = self._left
            self._left = self._left.next_node
            self._size -= 1
            if not self._left:
                self._right = None
            return old.val
        return None

    def pop_right(self) -> Any:
        if self._right:
            tmp = self._left
            while tmp.next_node != self._right:
                tmp = tmp.next_node
            old = tmp.next_node
            self._right = tmp
            tmp.next_node = None
            self._size -= 1
            if not self._right:
                self._left = None
            return old.val
        return None


# 1.3.34 random bag implementation.
class RandomBag(object):

    def __init__(self):
        self._bag = []

    def __iter__(self):
        random.shuffle(self._bag)
        for i in self._bag:
            yield i

    def is_empty(self):
        return len(self._bag) == 0

    def size(self):
        return len(self._bag)

    def add(self, item):
        self._bag.append(item)


# 1.3.35 random queue implementation.
class RandomQueue(object):

    def __init__(self):
        self._queue = []

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)

    def enqueue(self, item):
        self._queue.append(item)

    def dequeue(self):
        if len(self._queue):
            index = random.randint(0, len(self._queue) - 1)
            return self._queue.pop(index)
        return None

    def sample(self):
        if len(self._queue):
            index = random.randint(0, len(self._queue) - 1)
            return self._queue[index]
        return None

    # 1.3.36 practice
    def __iter__(self):
        random.shuffle(self._queue)
        for i in self._queue:
            yield i


# 1.3.38
class GeneralizeQueue(object):

    """
    >>> queue = GeneralizeQueue()
    >>> for i in range(10):
    ...     queue.insert(i)
    ...
    >>> queue.delete(10)
    9
    >>> queue.delete(1)
    0
    >>> queue.delete(4)
    4
    >>> ' '.join([str(i) for i in queue])
    '1 2 3 5 6 7 8'
    """

    def __init__(self):
        self._first = None
        self._last = None
        self._size = 0

    def __iter__(self):
        tmp = self._first
        while tmp:
            yield tmp.val
            tmp = tmp.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def insert(self, item):
        old = self._last
        self._last = Node(item)
        if not self._first:
            self._first = self._last
        else:
            old.next_node = self._last
        self._size += 1

    def delete(self, k):
        if k > self._size:
            return

        if k == 1:
            old = self._first
            self._first = self._first.next_node
            old.next_node = None
            self._size -= 1
            return old.val

        tmp = self._first
        count = 0

        while tmp and count != k - 2:
            tmp = tmp.next_node
            count += 1

        old = tmp.next_node
        tmp.next_node = tmp.next_node.next_node
        self._size -= 1
        old.next_node = None
        return old.val


# 1.3.40 practice
class MoveToFront(object):

    """
      Move to front implementation, if insert new value into the list,
    then insert into the head of the list, else move the node to the head
    >>> mtf = MoveToFront()
    >>> mtf.push(5)
    >>> mtf.push(4)
    >>> mtf.push(3)
    >>> mtf.push(2)
    >>> mtf.push(1)
    >>> mtf.push(1)
    >>> mtf.push(3)
    >>> mtf.push('abcde')
    >>> for i in mtf:
    ...     print(i)
    ...
    abcde
    3
    1
    2
    4
    5
    """

    def __init__(self):
        self._first = None
        self._set = set()

    def push(self, item):
        if not self._first:
            self._first = DoubleNode(item)
            self._set.add(item)
            return
        elif item not in self._set:
            old = self._first
            self._first = DoubleNode(item)
            self._first.next = old
            old.prev = self._first
            self._set.add(item)
        elif item in self._set:
            if item == self._first.val:
                return
            tmp = self._first
            while tmp and tmp.val != item:
                tmp = tmp.next
            # extract node from list
            prev_node, next_node = tmp.prev, tmp.next
            prev_node.next = next_node
            next_node.prev = prev_node
            tmp.prev = tmp.next = None
            tmp = None
            # insert into head
            old = self._first
            self._first = DoubleNode(item)
            self._first.next = old
            old.prev = self._first

    def __iter__(self):
        tmp = self._first
        while tmp:
            yield tmp.val
            tmp = tmp.next


# 1.3.43
def print_files(directory: str) -> None:
    def _print_files(indent: int, queue: Queue):
        directory = queue.dequeue()
        for item in Path(directory).glob('*'):
            if item.is_dir():
                print(f'{" " * indent} - {str(item)}/')
                queue.enqueue(item)
                _print_files(indent + 2, queue)
            elif item.is_file():
                print(f'{" " * indent} - {str(item)}')

    queue = Queue()
    print(f'- {directory}/')
    queue.enqueue(directory)
    _print_files(2, queue)


BaseDataType.register(RandomBag)
BaseDataType.register(RandomQueue)
BaseDataType.register(Deque)
BaseDataType.register(Steque)
BaseDataType.register(Bag)
BaseDataType.register(Stack)
BaseDataType.register(Queue)

if __name__ == '__main__':
    doctest.testmod()
