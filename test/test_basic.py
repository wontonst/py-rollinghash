import string

from pytest import raises

from rollinghash.rollinghash import RollingHashError,  RollingHash


SINGLE_A_HASH = 97
ABCD_HASH = 1466


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
    a.appendleft('a')
    assert first == a.hash
    before_app = a.hash
    a.append('e')
    assert a.hash != ABCD_HASH
    a.pop()
    assert before_app == a.hash


def assert_push_append_equality(instr):
    """
    Verify that hash generated while pushing is equal when popping back off.
    :param instr: input string
    :return: None
    """
    mapping = []
    a = RollingHash()
    for c in instr:
        a.append(c)
        mapping.append(a.hash)
    for i in xrange(len(instr)):
        assert a.hash == mapping[len(instr) - 1 - i], "At i={} with str={}".format(i, a._string)
        a.pop()

    mapping = []
    a = RollingHash()
    for c in instr:
        a.appendleft(c)
        mapping.append(a.hash)
    for i in xrange(len(instr)):
        assert a.hash == mapping[len(instr) - 1 - i], "At i={} with str={}".format(i, a._string)
        a.popleft()


def test_push_append_equality():
    for i in xrange(100):
        assert_push_append_equality('a'*i)
    instrs = [
        'abcdefg',
        string.printable,
        string.ascii_letters,
        string.digits,
        'a',
        'a' * 1000,
    ]
    for s in instrs:
        assert_push_append_equality(s)


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
        a.append(c)
        assert a.hash not in visited
        visited.add(a.hash)

    for i in xrange(len(instr)):
        a.popleft()
        assert a.hash not in visited
        visited.add(a.hash)


def test_no_collisions():
    assert_no_collisions(string.printable * 100)
    assert_no_collisions('a' * 10000000)


def assert_push_behavior(s):
    """
    Test to ensure that hashing from constructor, appending entire string, and one char at a time are equal.
    :param s: input string
    :return: None
    """
    a = RollingHash(s)
    b = RollingHash()
    c = RollingHash()
    b.append(s)
    for ch in s:
        c.append(ch)

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