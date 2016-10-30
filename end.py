# Copyright 2016 Shuhei Takahashi All rights reserved
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

"""Introduces "end" keyword to mark the end of a block.

This is a joke module, never use it!
"""

import ast
import functools
import inspect
import sys
import warnings

try:  # Python 2
    import __builtin__ as builtins
except ImportError:  # Python 3
    import builtins


class EndSyntaxWarning(UserWarning):
    pass


def get_caller_frame():
    """Returns the frame object of the caller."""
    return inspect.currentframe().f_back.f_back


def process_import(frame):
    """Processes an import event of "end" module.

    Args:
        frame: The frame object where import is performed.
    """
    try:
        module_name = frame.f_globals['__name__']
    except KeyError:
        warnings.warn(
            'Can not get the source of an uknown module. '
            'End-of-block syntax check is skipped.',
            EndSyntaxWarning)
        return
    filename = frame.f_globals.get('__file__', '<unknown>')
    try:
        source = inspect.getsource(sys.modules[module_name])
    except Exception:
        warnings.warn(
            'Can not get the source of module "%s". '
            'End-of-block syntax check is skipped.' % (module_name,),
            EndSyntaxWarning)
        return

    root = ast.parse(source)
    for node in ast.walk(root):
        if not hasattr(node, 'body'):
            continue
        # FIXME: This is an inaccurate hack to handle try-except-finally
        # statement which is parsed as ast.TryExcept in ast.TryFinally in
        # Python 2.
        if (isinstance(node, ast.TryFinally) and
                len(node.body) == 1 and
                isinstance(node.body[0], ast.TryExcept)):
            continue
        for i, child in enumerate(node.body):
            if not hasattr(child, 'body'):
                continue
            try:
                next_child = node.body[i + 1]
            except IndexError:
                ok = False
            else:
                ok = (isinstance(next_child, ast.Expr) and
                      isinstance(next_child.value, ast.Name) and
                      next_child.value.id == 'end')
            if not ok:
                raise SyntaxError(
                    '%s:%d: This block is not closed with "end"' %
                    (filename, child.lineno))


def install_import_hook():
    """Installs __import__ hook."""
    saved_import = builtins.__import__
    @functools.wraps(saved_import)
    def import_hook(name, *args, **kwargs):
        if name == 'end':
            process_import(get_caller_frame())
        return saved_import(name, *args, **kwargs)
    builtins.__import__ = import_hook


install_import_hook()

# First import of this module is not processed by the import hook, so
# call process_import() now.
process_import(get_caller_frame())
