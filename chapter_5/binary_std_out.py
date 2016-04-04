#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import struct
from sys import stdout


class BinaryStdOut(object):

    '''
    >>> bool_type = True
    >>> char_type = 'K'
    >>> BinaryStdOut.write_bool(bool_type)
    >>> BinaryStdOut.write_char(char_type)
    >>> BinaryStdOut.flush()
    '''

    out = stdout.buffer
    buff = 0
    size = 0

    @staticmethod
    def write_bit(bit):
        BinaryStdOut.buff <<= 1
        if bit:
            BinaryStdOut.buff |= 1
        BinaryStdOut.size += 1
        if BinaryStdOut.size == 8:
            BinaryStdOut.clear_buffer()

    @staticmethod
    def write_byte(int_type):
        assert 0 <= int_type < 256

        if BinaryStdOut.size == 0:
            data = struct.pack('H', int_type)
            BinaryStdOut.out.write(data)
            return

        for i in range(8):
            bit = ((int_type >> (8 - i - 1)) & 1) == 1
            BinaryStdOut.write_bit(bit)

    @staticmethod
    def clear_buffer():
        if BinaryStdOut.size == 0:
            return
        if BinaryStdOut.size > 0:
            BinaryStdOut.buff <<= (8 - BinaryStdOut.size)
        try:
            BinaryStdOut.out.write(BinaryStdOut.buff)
        except IOError as e:
            print(e)
        BinaryStdOut.buff = BinaryStdOut.size = 0

    @staticmethod
    def flush():
        BinaryStdOut.clear_buffer()
        try:
            BinaryStdOut.out.flush()
        except IOError as e:
            print(e)

    @staticmethod
    def close():
        BinaryStdOut.flush()
        try:
            BinaryStdOut.out.close()
        except IOError as e:
            print(e)

    @staticmethod
    def write_bool(boolean):
        BinaryStdOut.write_bit(boolean)

    @staticmethod
    def write_char(char, r=None):
        if ord(char) < 0 or ord(char) > 255:
            raise Exception('Illegal 8-bit char = {}'.format(char))
        BinaryStdOut.write_byte(ord(char))

if __name__ == '__main__':
    doctest.testmod()
