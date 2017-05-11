from __future__ import print_function

import collections
import sys


DEFAULT_MODULO = sys.maxint/2
DEFAULT_MULTIPLIER_CONSTANT = 999


class RollingHashError(Exception):
    pass


class RollingHash(object):

    @classmethod
    def _calculate_hash(cls, s, multiplier, modulo):
        res = 0
        for i, c in enumerate(s):
            res += ord(c) * multiplier**(len(s) - 1 - i)
            res = res % modulo
        return res

    def __init__(self, initial_string=None,
                 multiplier=DEFAULT_MULTIPLIER_CONSTANT,
                 modulo=DEFAULT_MODULO):
        if not multiplier:
            raise RollingHashError('multiplier cannot be set to 0')
        if not modulo:
            raise RollingHashError('modulo cannot be set to 0')
        self._multiplier = multiplier
        self._modulo = modulo
        self._hash = 0
        self._string = collections.deque()
        if initial_string is not None:
            self._string += initial_string
            self._hash = RollingHash._calculate_hash(self._string, multiplier, modulo)

    @property
    def string(self):
        return ''.join(self._string)

    def _incr_hash(self, value):
        self._hash += value
        self._hash %= self._modulo

    def _grow_hash_right(self, places=1):
        """
        Prepare to add elements to the right of the hash window.
        This is basically multipling all other element values by the multiplier.
        :param places: how many elements being removed
        :return:
        """
        self._hash *= self._multiplier ** places
        self._hash %= self._modulo

    def _shrink_hash_right(self, places=1):
        """
        Prepare to popo elements from the right of the hash window.
        This is basically dividing all other element values by the multiplier.
        :param places:
        :return:
        """
        self._hash /= self._multiplier**places

    def _calculate_single(self, index):
        # note: this is the critical section of the code, takes 99.9% of time in push/pop operation
        return (ord(self._string[index]) * self._multiplier**(len(self._string) - 1 - index)) % self._modulo

    def popleft(self, num=1):
        if num <= 0:
            raise RollingHashError('Cannot pop less than 1 value')

        for _ in xrange(min(len(self._string), num) - 1):
            self._popleft()
        return self._popleft()

    def _popleft(self):
        self._hash -= self._calculate_single(0) % self._modulo
        self._string.popleft()
        if not self._string:
            return None
        return self.hash

    def push(self, in_str):
        self._grow_hash_right(len(in_str))
        self._incr_hash(self._calculate_hash(in_str, self._multiplier, self._modulo))
        self._string += in_str
        return self.hash


    @property
    def hash(self):
        if not self._string:
            raise RollingHashError('Nothing to hash')
        return self._hash
        

