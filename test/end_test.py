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

import unittest


class SyntaxCheckTest(unittest.TestCase):
    def test_if(self):
        import cases.if_ok
        with self.assertRaises(SyntaxError):
            import cases.if_ng

    def test_while(self):
        import cases.while_ok
        with self.assertRaises(SyntaxError):
            import cases.while_ng

    def test_for(self):
        import cases.for_ok
        with self.assertRaises(SyntaxError):
            import cases.for_ng

    def test_try(self):
        import cases.try_ok
        with self.assertRaises(SyntaxError):
            import cases.try_ng
        # TODO: Fix this tricky case.
        # with self.assertRaises(SyntaxError):
        #     import cases.try_tricky

    def test_with(self):
        import cases.with_ok
        with self.assertRaises(SyntaxError):
            import cases.with_ng

    def test_func(self):
        import cases.func_ok
        with self.assertRaises(SyntaxError):
            import cases.func_ng

    def test_class(self):
        import cases.class_ok
        with self.assertRaises(SyntaxError):
            import cases.class_ng


if __name__ == '__main__':
    unittest.main()
