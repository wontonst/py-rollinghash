import cProfile
import itertools
import pstats
import string
import StringIO

import rollinghash



pr = cProfile.Profile()
pr.enable()

sz = 5000
a = rollinghash.RollingHash()
for c in itertools.repeat(string.printable, sz):
    a.push(c)
for _ in itertools.repeat(string.printable, sz):
    a.popleft()

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
