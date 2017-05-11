"""
Kinda didn't feel like reading about linear congruency generators so just going to brute force it.
The results of this show that runtime becomes an issue before collisions do, so we're good.
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
    jump = 100000
    while True:
        s = 'abc' * i * jump + ('abc' * i * jump)[::-1]
        if not assert_no_collisions(s, modulo, multiplier):
            return i * 6 * jump
        i += 1
        print('i={}'.format(i))

def pair_generator():
    for modul in range(1, sys.maxint, sys.maxint/100):
        for mult in range(1, 100, 10):
            yield (modul, mult)

best_len = 0
best_pair = ()
pool = multiprocessing.Pool(16)
lock = multiprocessing.Lock()


def process_pair(tup):
    modulo, multiplier = tup
    global best_len, best_pair, lock
    print("Running mod={},mult={}".format(modulo, multiplier))
    l = find_max_strlen(modulo, multiplier)
    if l > best_len:
        lock.acquire()
        best_len = l
        best_pair = (modulo, multiplier)
        lock.release()

# pool.map(process_pair, pair_generator())

for pair in pair_generator():
    process_pair(pair)

print("Best length is {} with mod={} and multiplier={}".format(best_len, best_pair[0], best_pair[1]))