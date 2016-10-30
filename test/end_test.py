# Copyright 2016 Shuhei Takahashi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import inspect
import unittest

import end

try:
    import builtins
except ImportError:
    import __builtin__ as builtins
end


class SyntaxCheckTest(unittest.TestCase):
    def test_if(self):
        import cases.if_ok
        with self.assertRaises(SyntaxError):
            import cases.if_ng
        end
        with self.assertRaises(SyntaxError):
            import cases.if_else
        end
        # TODO: Fix this nested case.
        # with self.assertRaises(SyntaxError):
        #     import cases.if_nested
        # end
    end

    def test_while(self):
        import cases.while_ok
        with self.assertRaises(SyntaxError):
            import cases.while_ng
        end
        with self.assertRaises(SyntaxError):
            import cases.while_else
        end
    end

    def test_for(self):
        import cases.for_ok
        with self.assertRaises(SyntaxError):
            import cases.for_ng
        end
        with self.assertRaises(SyntaxError):
            import cases.for_else
        end
    end

    def test_try(self):
        import cases.try_ok
        with self.assertRaises(SyntaxError):
            import cases.try_ng
        end
        with self.assertRaises(SyntaxError):
            import cases.try_except
        end
        with self.assertRaises(SyntaxError):
            import cases.try_finally
        end
        with self.assertRaises(SyntaxError):
            import cases.try_else
        end
        # TODO: Fix this tricky case.
        # with self.assertRaises(SyntaxError):
        #     import cases.try_tricky
        # end
    end

    def test_with(self):
        import cases.with_ok
        with self.assertRaises(SyntaxError):
            import cases.with_ng
        end
    end

    def test_func(self):
        import cases.func_ok
        with self.assertRaises(SyntaxError):
            import cases.func_ng
        end
    end

    def test_class(self):
        import cases.class_ok
        with self.assertRaises(SyntaxError):
            import cases.class_ng
        end
    end

    def test_hooked_import(self):
        # It should work even if __import__ is hooked by someone else.
        saved_import = builtins.__import__
        @functools.wraps(saved_import)
        def my_import(*args, **kwargs):
            return saved_import(*args, **kwargs)
        end
        builtins.__import__ = my_import
        try:
            with self.assertRaises(SyntaxError) as cm:
                import cases.hooked_import
            end
            self.assertTrue('hooked_import.py' in str(cm.exception))
        finally:
            builtins.__import__ = saved_import
        end
    end

    def test_inspect_import(self):
        import cases.import_call
    end

    def test_stray_end(self):
        with self.assertRaises(SyntaxError):
            import cases.stray_end
        end
    end
end


if __name__ == '__main__':
    unittest.main()
end
