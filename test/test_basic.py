import string

from pytest import raises

from rollinghash.rollinghash import RollingHashError,  RollingHash


SINGLE_A_HASH = 97
ABCD_HASH = 96807194002


def test_nothing_hashable():
    hash = RollingHash()
    with raises(RollingHashError, message="Nothing to hash"):
        hash.hash


def test_basic():
    a = RollingHash('abcd')
    first = a.hash
    assert a.hash == ABCD_HASH
    a.popleft()
    assert a.hash != ABCD_HASH
    before_app = a.hash
    a.push('e')
    assert a.hash != ABCD_HASH
    a.push('abcd')
    for _ in xrange(4):
        a.popleft()
    assert a.hash == ABCD_HASH

def test_pop_to_empty():
    a = RollingHash('a')
    assert a.hash == SINGLE_A_HASH
    a.popleft()
    with raises(RollingHashError, message='Nothing to hash'):
        a.hash
    with raises(IndexError, message='pop from an empty deque'):
        a.popleft()


def assert_no_collisions(instr):
    """
    Verify no hash collisions occur with input.
    :param instr: input string
    :return: None
    """
    a = RollingHash()
    visited = set()
    for c in instr:
        a.push(c)
        assert a.hash not in visited, "Collision in push at _string={}".format(a.string)
        visited.add(a.hash)

    for i in xrange(len(instr) - 2):
        a.popleft()
        assert a.hash not in visited, "Collision in pop at _string={}".format(a.string)
        visited.add(a.hash)


def test_no_collisions():
    for i in range(120):
        assert_no_collisions('abc' * i + ('abc' * i)[::-1])

def assert_push_behavior(s):
    """
    Test to ensure that hashing from constructor, pushing entire string, and one char at a time are equal.
    :param s: input string
    :return: None
    """
    a = RollingHash(s)
    b = RollingHash()
    c = RollingHash()
    b.push(s)
    for ch in s:
        c.push(ch)

    assert a.hash == b.hash
    assert b.hash == c.hash


def test_default_equality():
    instrs = [
        string.printable,
        string.ascii_letters,
        string.digits,
        'a',
        'a' * 1000,
        'Kate is a bitter is a Kate'
    ]
    for s in instrs:
        assert_push_behavior(s)

def test_pop_multiple():
    a = RollingHash('abcda')
    assert a.popleft(4) == SINGLE_A_HASH
    a = RollingHash('abcda')
    assert a.popleft(40) is None
