# RollingHash #

This is a python implementation of a rolling hash function. The implementation
is based off the [wikipedia article](https://en.wikipedia.org/w/index.php?title=Rolling_hash&oldid=751411496#Rabin-Karp_rolling_hash).

# Installation #

Simply ```pip install /path/to/rollinghash```

# Usage & API #

This package is very simple to use

```
import rollinghash

a = rollinghash.RollingHash()
# or alternatively
a = rollinghash.RollingHash('some stuff to hash first')

# to add to the window

a.push('some more stuff')  # returns new hash of window

# get current hash
curr_hash = a.hash

# pop off first 

a.pop() # returns new hash of window

# alternatively pop more off

a.pop(10)
```

If you pop more than there are values, it will pop everything off and return None

