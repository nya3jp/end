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

"""Introduces "end" keyword to mark the end of a block.

This is a joke module, never use it!
"""

import end  # Dogfooding

import ast
import dis
import functools
import inspect
import sys
import warnings

if not ((sys.version_info[0] == 2 and sys.version_info[1] >= 7) or
        (sys.version_info[0] == 3 and sys.version_info[1] >= 3)):
    raise ImportError('Supported Python verions are 2.7+ and 3.3+.')
end

PY2 = (sys.version_info.major == 2)
PY3 = not PY2

if PY2:
    import __builtin__ as builtins
else:
    import builtins
end


class EndSyntaxWarning(UserWarning):
    pass
end


def find_importer_frame():
    """Returns the outer frame importing this "end" module.

    If this module is being imported by other means than import statement,
    None is returned.

    Returns:
        A frame object or None.
    """
    byte = lambda ch: ord(ch) if PY2 else ch
    frame = inspect.currentframe()
    try:
        while frame:
            code = frame.f_code
            lasti = frame.f_lasti
            if byte(code.co_code[lasti]) == dis.opmap['IMPORT_NAME']:
                # FIXME: Support EXTENDED_ARG.
                arg = (
                    byte(code.co_code[lasti + 1])
                    + byte(code.co_code[lasti + 2]) * 256)
                name = code.co_names[arg]
                if name == 'end':
                    break
                end
            end
            frame = frame.f_back
        end
        return frame
    finally:
        del frame
    end
end


def is_end_node(node):
    """Checks if a node is the "end" keyword.

    Args:
        node: AST node.

    Returns:
        True if the node is the "end" keyword, otherwise False.
    """
    return (isinstance(node, ast.Expr) and
            isinstance(node.value, ast.Name) and
            node.value.id == 'end')
end


def get_compound_bodies(node):
    """Returns a list of bodies of a compound statement node.

    Args:
        node: AST node.

    Returns:
        A list of bodies of the node. If the given node does not represent
        a compound statement, an empty list is returned.
    """
    if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.With)):
        return [node.body]
    elif isinstance(node, (ast.If, ast.While, ast.For)):
        return [node.body, node.orelse]
    elif PY2 and isinstance(node, ast.TryFinally):
        return [node.body, node.finalbody]
    elif PY2 and isinstance(node, ast.TryExcept):
        return [node.body, node.orelse] + [h.body for h in node.handlers]
    elif PY3 and isinstance(node, ast.Try):
        return ([node.body, node.orelse, node.finalbody]
                + [h.body for h in node.handlers])
    end
    return []
end


def check_end_blocks(frame):
    """Performs end-block check.

    Args:
        frame: A frame object of the module to be checked.

    Raises:
        SyntaxError: If check failed.
    """
    try:
        try:
            module_name = frame.f_globals['__name__']
        except KeyError:
            warnings.warn(
                'Can not get the source of an uknown module. '
                'End-of-block syntax check is skipped.',
                EndSyntaxWarning)
            return
        end

        filename = frame.f_globals.get('__file__', '<unknown>')
        try:
            source = inspect.getsource(sys.modules[module_name])
        except Exception:
            warnings.warn(
                'Can not get the source of module "%s". '
                'End-of-block syntax check is skipped.' % (module_name,),
                EndSyntaxWarning)
            return
        end
    finally:
        del frame
    end

    root = ast.parse(source)
    for node in ast.walk(root):
        bodies = get_compound_bodies(node)
        if not bodies:
            continue
        end

        # FIXME: This is an inaccurate hack to handle if-elif-else.
        if (isinstance(node, ast.If) and
                len(node.orelse) == 1 and
                isinstance(node.orelse[0], ast.If)):
            continue
        end

        # FIXME: This is an inaccurate hack to handle try-except-finally
        # statement which is parsed as ast.TryExcept in ast.TryFinally in
        # Python 2.
        if (PY2 and
                isinstance(node, ast.TryFinally) and
                len(node.body) == 1 and
                isinstance(node.body[0], ast.TryExcept)):
            continue
        end

        for body in bodies:
            skip_next = False
            for i, child in enumerate(body):
                if skip_next:
                    skip_next = False
                elif is_end_node(child):
                    raise SyntaxError(
                        '"end" does not close a block.',
                        [filename, child.lineno, child.col_offset,
                         source.splitlines()[child.lineno - 1] + '\n'])
                elif get_compound_bodies(child):
                    try:
                        ok = is_end_node(body[i + 1])
                    except IndexError:
                        ok = False
                    end
                    if not ok:
                        raise SyntaxError(
                            'This block is not closed with "end".',
                            [filename, child.lineno, child.col_offset,
                             source.splitlines()[child.lineno - 1] + '\n'])
                    end
                    skip_next = True
                end
            end
        end
    end
end


def process_import():
    """Processes an import event of "end" module.

    Raises:
        SyntaxError: If check failed.
    """
    frame = find_importer_frame()
    if frame:
        try:
            check_end_blocks(frame)
        finally:
            del frame
        end
    end
end


def install_import_hook():
    """Installs __import__ hook."""
    saved_import = builtins.__import__
    @functools.wraps(saved_import)
    def import_hook(name, *args, **kwargs):
        if name == 'end':
            process_import()
        end
        return saved_import(name, *args, **kwargs)
    end
    builtins.__import__ = import_hook
end


install_import_hook()

# Check this module itself!
check_end_blocks(inspect.currentframe())

# First import of this module is not processed by the import hook, so
# call process_import() now.
process_import()
