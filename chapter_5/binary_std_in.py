#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import struct
import sys


class BinaryStdIn(object):

    '''
    >>> bool_type = True
    >>> int_type = 1111
    >>> char_type = 'K'
    >>> BinaryStdIn.read_bool()
    '''

    stream = sys.stdin
    buff = 0
    size = 0
    EOF = -1

    @staticmethod
    def fill_buffer():
        try:
            raw = BinaryStdIn.stream.read(1)
            BinaryStdIn.buff = struct.unpack('H', raw)
            BinaryStdIn.size = 8
        except IOError:
            print('EOF')
            BinaryStdIn.buff = 0
            BinaryStdIn.size = BinaryStdIn.EOF

    @staticmethod
    def close():
        try:
            BinaryStdIn.stream.close()
        except Exception as e:
            print(e)

    @staticmethod
    def is_empty():
        return BinaryStdIn.size == BinaryStdIn.EOF

    @staticmethod
    def read_bool():
        if BinaryStdIn.is_empty():
            raise Exception('Reading from empty input stream')
        BinaryStdIn.size -= 1
        bit = ((BinaryStdIn.buff >> BinaryStdIn.size) & 1) == 1
        if BinaryStdIn.size == 0:
            BinaryStdIn.fill_buffer()
        return bit

    @staticmethod
    def read_char():
        if BinaryStdIn.is_empty():
            raise Exception('Reading from empty input stream')

        if BinaryStdIn.size == 8:
            data = BinaryStdIn.buff
            BinaryStdIn.fill_buffer()
            return chr(data & 0xff)

        data = BinaryStdIn.buff
        data <<= (8 - BinaryStdIn.size)
        old_size = BinaryStdIn.size
        BinaryStdIn.fill_buffer()
        if BinaryStdIn.is_empty():
            raise Exception('Reading from empty input stream')
        BinaryStdIn.size = old_size
        data |= BinaryStdIn.buff >> BinaryStdIn.size
        return data & 0xff

    @staticmethod
    def read_int():
        data = 0
        for i in range(4):
            c = BinaryStdIn.read_char()
            data <<= 8
            data |= ord(c)
        return data


if __name__ == '__main__':
    doctest.testmod()
