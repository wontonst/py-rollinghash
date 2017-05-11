"""
Kinda didn't feel like reading about linear congruency generators so just going to brute force it.
"""
from __future__ import print_function

import multiprocessing
import sys

from rollinghash import RollingHash


def assert_no_collisions(instr, mod, mult):
    a = RollingHash(modulo=mod, multiplier=mult)
    visited = set()
    for c in instr:
        a.push(c)
        if a.hash in visited:
            return False
        visited.add(a.hash)
    for i in xrange(len(instr) - 2):
        a.popleft()
        if a.hash in visited:
            return False
        visited.add(a.hash)
    return True


def find_max_strlen(modulo, multiplier):
    i = 0
    while True:
        s = 'abc' * i*1000 + ('abc' * i)[::-1]
        if not assert_no_collisions(s, modulo, multiplier):
            return i * 6
        i += 1
        print('i={}'.format(i))

def pair_generator():
    for modul in range(1, sys.maxint, sys.maxint/100):
        for mult in range(1, 10000, 100):
            yield (modul, mult)

best_len = 0
best_pair = ()
pool = multiprocessing.Pool(16)
lock = multiprocessing.Lock()


def process_pair(tup):
    modulo, multiplier = tup
    global best_len, best_pair, lock
    l = find_max_strlen(modulo, multiplier)
    print("{},{}={}".format(modulo, multiplier, l))
    if l > best_len:
        lock.acquire()
        best_len = l
        best_pair = (modulo, multiplier)
        lock.release()

# pool.map(process_pair, pair_generator())

for pair in pair_generator():
    process_pair(pair)

print("Best length is {} with mod={} and multiplier={}".format(best_len, best_pair[0], best_pair[1]))