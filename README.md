end
===

This module magically introduces `end` keyword to your Python code which marks
the end of a block statement.

[![PyPI version](https://badge.fury.io/py/end.svg)](http://badge.fury.io/py/end)


Usage
-----

Import "end" module and mark end of blocks with `end`. If you forget to mark them,
`SyntaxError` is raised on import time (not on execution time).

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
    time.sleep(10000)
except KeyboardInterrupt:
    print('Interrupted')
finally:
    print('Bye!')
end

if 28 > 3:
    print('nya-n')
# end is missing here, SyntaxError is raised!
```


Disclaimer
----------

This is a joke module -- never use it.


Author
------

Shuhei Takahashi

- Website: https://nya3.jp/
- Twitter: https://twitter.com/nya3jp/


License
-------

Apache 2.0
