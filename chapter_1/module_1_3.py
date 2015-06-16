#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
from __future__ import print_function
import string
import doctest
import random
from abc import ABCMeta, abstractmethod
from common import Node, DoubleNode


class BaseDataType:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __iter__(self):
        while False:
            yield None

    @abstractmethod
    def size(self):
        return NotImplemented

    @abstractmethod
    def is_empty(self):
        return NotImplemented


class Stack(object):

    '''
    stack LIFO data structure linked-list implementation
    >>> s = Stack()
    >>> s.peek()
    >>> s.push(1)
    >>> s.push(2)
    >>> s.push(3)
    >>> s.size()
    3
    >>> s.peek()
    3
    >>> for item in s:
    ...     print(item)
    ...
    3
    2
    1
    >>>
    >>> s.is_empty()
    False
    >>> s.pop()
    3
    >>> s.pop()
    2
    >>> s.pop()
    1
    >>> s.pop()
    >>> s.size()
    0
    >>> s.is_empty()
    True
    '''

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def push(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def pop(self):
        if self._first:
            old = self._first
            self._first = self._first.next_node
            self._size -= 1
            return old.val
        return None

    # 1.3.7 practice
    def peek(self):
        if self._first:
            return self._first.val
        return None


class BaseConverter(object):

    '''
    convert decimal number to x base number using stack.
    >>> BaseConverter.convert_decimal_integer(50, 2)
    '110010'
    >>> BaseConverter.convert_decimal_integer(8, 2)
    '1000'
    >>> BaseConverter.convert_decimal_integer(15, 16)
    'F'
    >>> BaseConverter.convert_decimal_integer(9, 8)
    '11'
    '''
    digits = '0123456789ABCDEF'

    @staticmethod
    def convert_decimal_integer(dec_num, base):
        stack = Stack()
        while dec_num:
            stack.push(dec_num % base)
            dec_num //= base
        res = []
        while not stack.is_empty():
            res.append(BaseConverter.digits[stack.pop()])
        return ''.join(res)


class Evaluate(object):

    '''
    dijkstra infix evaluate algorithm, using stack for data structure.
    >>> evaluate = Evaluate()
    >>> evaluate.calculate('(1+((2+3)*(4*5)))')
    101.0
    >>> evaluate.calculate('((1-2)*(8/4))')
    -2.0
    '''

    def __init__(self):
        self._ops_stack = Stack()
        self._vals_stack = Stack()
        self._ops_char = ('+', '-', '*', '/')

    def calculate(self, infix_string):
        for i in infix_string:
            if i in self._ops_char:
                self._ops_stack.push(i)
            elif i == '(':
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

    '''
    queue FIFO data structure linked-list implementation
    >>> q = Queue()
    >>> q.is_empty()
    True
    >>> q.size()
    0
    >>> q.enqueue(1)
    >>> q.enqueue(2)
    >>> q.enqueue(3)
    >>> q.enqueue(4)
    >>> q.size()
    4
    >>> q.is_empty()
    False
    >>> for item in q:
    ...     print(item)
    ...
    1
    2
    3
    4
    >>>
    >>> q.dequeue()
    1
    >>> q.dequeue()
    2
    >>> q.dequeue()
    3
    >>> q.dequeue()
    4
    >>> q.dequeue()
    >>> q.dequeue()
    >>> q.size()
    0
    >>> old = Queue()
    >>> for i in range(5):
    ...     old.enqueue(i)
    ...
    >>> new_queue = Queue(old)
    >>> for i in new_queue:
    ...     print(i, end=' ')
    ...
    0 1 2 3 4
    >>> new_queue.enqueue(6)
    >>> for i in old:
    ...     print(i, end=' ')
    ...
    0 1 2 3 4
    >>> for i in new_queue:
    ...     print(i, end=' ')
    ...
    0 1 2 3 4 6
    '''

    # 1.3.41 practice

    def __init__(self, q=None):
        self._first = None
        self._last = None
        self._size = 0
        if q:
            for item in q:
                self.enqueue(item)

    def __iter__(self):
        node = self._first
        while node:
            yield node.val
            node = node.next_node

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size

    def enqueue(self, val):
        old_last = self._last
        self._last = Node(val)
        self._last.next_node = None
        if self.is_empty():
            self._first = self._last
        else:
            old_last.next_node = self._last
        self._size += 1

    def dequeue(self):
        if not self.is_empty():
            val = self._first.val
            self._first = self._first.next_node
            if self.is_empty():
                self._last = None
            self._size -= 1
            return val
        return None


class Bag(object):

    '''
    bag data structure linked-list implementation.
    >>> bag = Bag()
    >>> bag.size()
    0
    >>> bag.is_empty()
    True
    >>> bag.add(1)
    >>> bag.add(2)
    >>> bag.add(3)
    >>> bag.add(4)
    >>> bag.add(5)
    >>> bag.size()
    5
    >>> for i in bag:
    ...     print(i)
    ...
    5
    4
    3
    2
    1
    >>> bag.is_empty()
    False
    '''

    def __init__(self):
        self._first = None
        self._size = 0

    def __iter__(self):
        node = self._first
        while node is not None:
            yield node.val
            node = node.next_node

    def add(self, val):
        node = Node(val)
        old = self._first
        self._first = node
        self._first.next_node = old
        self._size += 1

    def is_empty(self):
        return self._first is None

    def size(self):
        return self._size


# stack example
# 1.3.4 practice
class Parentheses(object):

    '''
    using stack data structure for judging if parenthese is symmetric.
    >>> p = Parentheses()
    >>> p.is_parenthese_symmetric('[()]{}{[()()]()}')
    True
    >>> p.is_parenthese_symmetric('[(])}}{}{]])')
    False
    >>> p.is_parenthese_symmetric('{{{{}}}')
    False
    >>> p.is_parenthese_symmetric('{}}}}}}}{{{')
    False
    '''

    def __init__(self):
        self._left_parenthese_stack = Stack()
        self._left_parentheses = ('[', '{', '(')
        self._right_parentheses = (']', '}', ')')

    def __is_match(self, left_parenthese, right_parenthese):
        return (self._left_parentheses.index(left_parenthese) ==
                self._right_parentheses.index(right_parenthese))

    def is_parenthese_symmetric(self, parenthese_string):
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
    using stack for getting integer binary representation.
    >>> get_binary(50)
    '110010'
    >>> get_binary(8)
    '1000'
    '''
    s = Stack()
    while integer:
        s.push(integer % 2)
        integer /= 2
    return ''.join([str(i) for i in s])


# 1.3.9 practice
class CompleteInfixString(object):

    '''
    using stack for complete infix string,
    the basic principle is similar to dijkstra infix arithmetic algorithm.
    >>> cis = CompleteInfixString()
    >>> cis.complete_string('1+2)*3-4)*5-6)))')
    '((1+2)*((3-4)*(5-6)))'
    '''

    def __init__(self):
        self._ops_stack = Stack()
        self._vals_stack = Stack()
        self._ops_char = ('+', '-', '*', '/')

    def complete_string(self, incmplt_string):
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

    '''
    turn infix string to postfix string using stack.
    >>> itp = InfixToPostfix()
    >>> itp.infix_to_postfix("(A+B)*(C+D)")
    'A B + C D + *'
    >>> itp.infix_to_postfix("(A+B)*C")
    'A B + C *'
    >>> itp.infix_to_postfix("A+B*C")
    'A B C * +'
    '''
    operand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    ops = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}

    def __init__(self):
        self._ops_stack = Stack()

    def infix_to_postfix(self, infix_string):
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
                       InfixToPostfix.ops[self._ops_stack.peek()] >= InfixToPostfix.ops[i]):
                    postfix_list.append(self._ops_stack.pop())
                self._ops_stack.push(i)

        while not self._ops_stack.is_empty():
            postfix_list.append(self._ops_stack.pop())
        return ' '.join(postfix_list)


# 1.3.11 practice
class PostfixEvaluate(object):

    '''
    using stack for postfix evaluation.
    >>> pfe = PostfixEvaluate()
    >>> pfe.evaluate('78+32+/')
    3
    '''

    def __init__(self):
        self._operand_stack = Stack()

    def evaluate(self, postfix_string):
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

    '''
    steque data structure, combining stack operation and queue operation.
    >>> s = Steque()
    >>> for i in range(1, 10):
    ...     s.push(i)
    ...
    >>> s.pop()
    9
    >>> s.pop()
    8
    >>> s.enqueue(10)
    >>> for i in s:
    ...     print(i, end=' ')
    ...
    7 6 5 4 3 2 1 10
    >>> s2 = Steque()
    >>> for i in range(10):
    ...     s2.enqueue(i)
    ...
    >>> for j in s2:
    ...     print(j, end=' ')
    ...
    0 1 2 3 4 5 6 7 8 9
    >>> while not s2.is_empty():
    ...     print(s2.pop(), end=' ')
    ...
    0 1 2 3 4 5 6 7 8 9
    '''

    def __init__(self):
        self._top = None
        self._bottom = None
        self._size = 0

    def __iter__(self):
        tmp = self._top
        while tmp:
            yield tmp.val
            tmp = tmp.next_node

    def push(self, val):
        old = self._top
        self._top = Node(val)
        self._top.next_node = old
        if old is None:
            self._bottom = self._top
        self._size += 1

    def pop(self):
        if self._top:
            out = self._top
            self._top = self._top.next_node
            if self._top is None:
                self._bottom = None
            self._size -= 1
            return out.val
        return None

    def enqueue(self, val):
        if not self._bottom:
            self._bottom = self._top = Node(val)
            self._size += 1
            return
        node = Node(val)
        self._bottom.next_node = node
        self._bottom = self._bottom.next_node
        self._size += 1

    def is_empty(self):
        return self._top is None

    def size(self):
        return self._size


# 1.3.33 practice deque implementation.
class Deque(object):

    '''
    double queue datastructure implementaion.
    >>> d = Deque()
    >>> d.push_left(1)
    >>> d.push_right(2)
    >>> d.push_right(3)
    >>> d.push_left(0)
    >>> for i in d:
    ...     print(i)
    ...
    0
    1
    2
    3
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

    def __init__(self):
        self._left = self._right = None
        self._size = 0

    def __iter__(self):
        tmp = self._left
        while tmp:
            yield tmp.val
            tmp = tmp.next_node

    def is_empty(self):
        return self._left is None and self._right is None

    def size(self):
        return self._size

    def push_left(self, item):
        old = self._left
        self._left = Node(item)
        self._left.next_node = old
        if self._right is None:
            self._right = self._left
        self._size += 1

    def push_right(self, item):
        old = self._right
        self._right = Node(item)
        if self.is_empty():
            self._left = self._right
        else:
            old.next_node = self._right
        self._size += 1

    def pop_left(self):
        if self._left:
            old = self._left
            self._left = self._left.next_node
            self._size -= 1
            if not self._left:
                self._right = None
            return old.val
        return None

    def pop_right(self):
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

    '''
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
    >>> for i in queue:
    ...     print(i, end=' ')
    ...
    1 2 3 5 6 7 8
    '''

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

    '''
    move to front implementation, if insert new value into the list,
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
    '''

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


BaseDataType.register(RandomBag)
BaseDataType.register(RandomQueue)
BaseDataType.register(Deque)
BaseDataType.register(Steque)
BaseDataType.register(Bag)
BaseDataType.register(Stack)
BaseDataType.register(Queue)

if __name__ == '__main__':
    doctest.testmod()

    # random bag test case.
    # random_bag = RandomBag()
    # for i in range(10):
    #     random_bag.add(i)

    # for i in random_bag:
    #     print(i)
