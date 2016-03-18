#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
from basic_data_struct import Queue


class Node(object):

    def __init__(self):
        self._val = None
        self._size = 1
        self.next_nodes = {}

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

    # 5.2.10 practice
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size


class Trie(object):

    '''
        Trie is a special data structure for string querying. Trie is similar with other tree-like
    structures, But every node has R links, which R is alphabet's size, that means every link is
    corresponding to a character. A node with a value that means the node is the end of a string.
        For searching a string, we can keep getting the next node by the next character, until we
    reach a node with an actual value, otherwise the target string miss.
        Trie is as fast as symbol table and more flexible than binary tree, but it cost lots of
    extra space. The running time of searching and inserting be proportional to O(N) which N is
    the length of the searching key.
        Trie is suitable for those shorter keys and the alphabet is rather small. Because long key
    and large alphabet could take much more space.
    >>> trie = Trie()
    >>> trie.get('xxxx')
    >>> test_data = ['she', 'sells', 'sea', 'shells', 'by', 'the', 'sea', 'shore']
    >>> for index, d in enumerate(test_data):
    ...     trie.put(d, index)
    >>> trie.size()
    8
    >>> [trie.get(i).val for i in test_data]
    [0, 1, 6, 3, 4, 5, 6, 7]
    >>> [i for i in trie.keys()]
    ['by', 'sea', 'sells', 'she', 'shells', 'shore', 'the']
    >>> [trie.rank(i) for i in trie.keys()]
    [1, 2, 3, 4, 5, 6, 7]
    >>> [trie.select(i) for i in range(1, 8)]
    ['by', 'sea', 'sells', 'she', 'she', 'shore', 'the']
    >>> [i for i in trie.keys_with_prefix('sh')]
    ['she', 'shells', 'shore']
    >>> [i for i in trie.keys_that_match('.he')]
    ['she', 'the']
    >>> [i for i in trie.keys_that_match('s..')]
    ['sea', 'she']
    >>> trie.longest_prefix_of('shellsort')
    6
    >>> trie.delete('she')
    >>> trie.size()
    7
    >>> trie.get('she').val
    >>> [i for i in trie.keys()]
    ['by', 'sea', 'sells', 'shells', 'shore', 'the']
    >>> [trie.rank(i) for i in trie.keys()]
    [1, 2, 3, 4, 5, 6]
    '''

    def __init__(self):
        self._root = Node()
        self._size = 0

    def size(self):
        return self._size

    def get(self, key):
        tmp = self._root
        d = 0

        while tmp:
            if d == len(key):
                return tmp
            char = key[d]
            try:
                tmp = tmp.next_nodes[char]
            except KeyError:
                return None
            d += 1
        return tmp

    def put(self, key, value):
        exist_node = self.get(key)
        if exist_node:
            exist_node.val = value
            self._size += 1
            return

        tmp = self._root
        for i in key:
            if i not in tmp.next_nodes:
                tmp.next_nodes[i] = Node()
            else:
                tmp.next_nodes[i].size += 1
            tmp = tmp.next_nodes[i]
        tmp.val = value
        self._size += 1

    def keys(self):
        '''
        Return all the keys in trie tree.
        '''
        return self.keys_with_prefix('')

    def keys_with_prefix(self, prefix):
        '''
        Return all the keys starts with the given prefix in the trie tree.
        '''
        q = Queue()
        if prefix == '':
            self._collect(self._root, prefix, q)
        else:
            start_node = self.get(prefix)
            self._collect(start_node, prefix, q)
        return q

    def _collect(self, node, prefix, q):
        if not node:
            return

        if node.val is not None:
            q.enqueue(prefix)

        for i in range(256):
            if chr(i) in node.next_nodes:
                self._collect(node.next_nodes[chr(i)], prefix + chr(i), q)

    def keys_that_match(self, pattern):
        '''
        Return all the keys match the given pattern in the trie tree.
        '''
        q = Queue()
        self._keys_collect(self._root, '', pattern, q)
        return q

    def _keys_collect(self, node, prefix, pattern, q):
        length = len(prefix)
        if not node:
            return

        if length == len(pattern):
            if node.val is not None:
                q.enqueue(prefix)
            return

        char = pattern[length]
        for i in range(256):
            if (char == '.' or char == chr(i)) and chr(i) in node.next_nodes:
                self._keys_collect(node.next_nodes[chr(i)], prefix + chr(i), pattern, q)

    def longest_prefix_of(self, s):
        '''
        Return the longest prefix's length of the given string which the prefix is in the trie tree.
        '''
        tmp = self._root
        length = d = 0

        while tmp:
            if tmp.val:
                length = d
            if d == len(s):
                return length
            char = s[d]
            if char not in tmp.next_nodes:
                break
            tmp = tmp.next_nodes[char]
            d += 1

        return length

    def delete(self, key):
        self._root = self._delete(self._root, key, 0)
        self._size -= 1

    def _delete(self, node, key, d):
        if not node:
            return None

        if d == len(key):
            node.val = None
            node.size -= 1
        else:
            index = key[d]
            node.size -= 1
            node.next_nodes[index] = self._delete(node.next_nodes[index], key, d + 1)

        if node.val:
            return node

        for i in range(256):
            if chr(i) in node.next_nodes:
                return node
        return None

    # 5.2.8 practice
    def select(self, k):
        tmp = self._root
        result = ''
        while tmp and tmp.val is None:
            count = 0
            count_list = []
            sorted_keys = sorted(tmp.next_nodes.keys())
            for c in sorted_keys:
                count_list.append((c, tmp.next_nodes[c].size + count))
                count = tmp.next_nodes[c].size + count

            for index, elem in enumerate(count_list):
                key, count = elem
                if k <= count:
                    tmp = tmp.next_nodes[key]
                    result += key
                    if index != 0:
                        k -= count_list[index - 1][1]
                    break
        return result

    # 5.2.8 practice
    def rank(self, key):
        tmp = self._root
        d = 0
        result = 0

        while d != len(key):
            char = key[d]
            if char not in tmp.next_nodes:
                return -1
            char_list = sorted(tmp.next_nodes.keys())
            for c in char_list:
                if c == char:
                    break
                result += tmp.next_nodes[c].size
            if len(tmp.next_nodes) == 1 and tmp.size != 1:
                result += 1
            tmp = tmp.next_nodes[char]

            d += 1
        return result + 1


class TNode(object):

    def __init__(self):
        self._char = None
        self._left = None
        self._right = None
        self._mid = None
        self._val = None

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, new_char):
        self._char = new_char

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node

    @property
    def mid(self):
        return self._mid

    @mid.setter
    def mid(self, node):
        self._mid = node

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value


class TernarySearchTries(object):

    '''
        Ternary-Search-Trie is another tree-like data structure for string querying.
    Every node in Ternary-Search-Trie contains a value and three links, and from left
    to right each link means the key of the node is smaller, equal, and large than the
    current node. Ternary-Search-Trie is more compatible than Trie, but also every
    operation is a little bit more complicated than Trie.
    >>> tst = TernarySearchTries()
    >>> tst.get('test')
    >>> test_data = ['she', 'sells', 'sea', 'shells', 'by', 'the', 'sea', 'shore']
    >>> for index, d in enumerate(test_data):
    ...     tst.put(d, index)
    >>> tst.size()
    8
    >>> [tst.get(i).val for i in test_data]
    [0, 1, 6, 3, 4, 5, 6, 7]
    >>> [i for i in tst.keys_with_prefix('sh')]
    ['she', 'shells', 'shore']
    >>> tst.longest_prefix_of('shellsort')
    6
    >>> [i for i in tst.keys_that_match('.he')]
    ['she', 'the']
    '''

    def __init__(self):
        self._root = None
        self._size = 0

    def size(self):
        return self._size

    def get(self, key):
        tmp = self._root
        if not tmp:
            return None
        d = 0
        while d < len(key) and tmp:
            char = key[d]
            if char < tmp.char:
                tmp = tmp.left
            elif char > tmp.char:
                tmp = tmp.right
            elif d < len(key) - 1:
                tmp = tmp.mid
                d += 1
            else:
                break
        return tmp if tmp else None

    def put(self, key, value):
        if not key:
            return
        self._root = self._put(self._root, key, value, 0)
        self._size += 1

    def _put(self, node, key, value, d):
        char = key[d]
        if not node:
            node = TNode()
            node.char = char

        if char < node.char:
            node.left = self._put(node.left, key, value, d)
        elif char > node.char:
            node.right = self._put(node.right, key, value, d)
        elif d < len(key) - 1:
            node.mid = self._put(node.mid, key, value, d + 1)
        else:
            node.val = value
        return node

    def keys(self):
        '''
        Return all the keys in trie tree.
        '''
        return self.keys_with_prefix('')

    # 5.2.9 practice, implementation is available on the official website
    def keys_with_prefix(self, prefix):
        '''
        Return all the keys starts with the given prefix in the trie tree.
        '''
        q = Queue()
        node = self.get(prefix)
        if not node:
            return q
        if node.val:
            q.enqueue(prefix)
        self._collect(node.mid, prefix, q)
        return q

    def _collect(self, node, prefix, q):
        if not node:
            return
        self._collect(node.left, prefix, q)
        if node.val is not None:
            q.enqueue(prefix + node.char)
        self._collect(node.mid, prefix + node.char, q)
        self._collect(node.right, prefix, q)

    # 5.2.9 practice, implementation is available on the official website
    def longest_prefix_of(self, key):
        if not key or key.strip() == '':
            return 0

        length = d = 0
        tmp = self._root

        while tmp:
            if d == len(key):
                return length
            char = key[d]
            if char < tmp.char:
                tmp = tmp.left
            elif char > tmp.char:
                tmp = tmp.right
            else:
                d += 1
                if tmp.val:
                    length = d
                tmp = tmp.mid
        return length

    # 5.2.9 practice, implementation is available on the official website
    def keys_that_match(self, pattern):
        q = Queue()
        self._keys_collect(self._root, '', 0, pattern, q)
        return q

    def _keys_collect(self, node, prefix, index, pattern, q):
        if not node:
            return

        char = pattern[index]
        if char == '.' or char < node.char:
            self._keys_collect(node.left, prefix, index, pattern, q)

        if char == '.' or char == node.char:
            if node.val is not None and index == len(pattern) - 1:
                q.enqueue(prefix + node.char)
            if index < len(pattern) - 1:
                self._keys_collect(node.mid, prefix + node.char, index + 1, pattern, q)

        if char == '.' or char > node.char:
            self._keys_collect(node.right, prefix, index, pattern, q)

if __name__ == '__main__':
    doctest.testmod()
