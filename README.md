end
===

This Python module magically introduces `end` keyword which marks
the end of a block statement.

[![PyPI version](https://badge.fury.io/py/end.svg)](http://badge.fury.io/py/end)
[![Build Status](https://travis-ci.org/nya3jp/end.svg?branch=master)](https://travis-ci.org/nya3jp/end)


Usage
-----

Import "end" module and mark ends of blocks with `end`.
When you forget to mark any, `SyntaxError` is raised in import time (not in execution time).

```python
import end

def func():
    for i in range(3):
        print(i)
    end
end

with open('a.txt') as f:
    print(f.read())
end

try:
    time.sleep(3)
except KeyboardInterrupt:
    print('Interrupted')
finally:
    print('Slept')
end

if 28 > 3:
    print('nya-n')
# end is missing here. SyntaxError is raised!
```


Warning
-------

This is a joke module --- never use it.


Author
------

Shuhei Takahashi

- Website: https://nya3.jp/
- Twitter: https://twitter.com/nya3jp/


License
-------

Apache 2.0
