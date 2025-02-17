import os
import tempfile
import pytest
from find_interface_used import find_interface_used

@pytest.fixture
def temp_dir():
    # Create a temporary directory for test files
    test_dir = tempfile.TemporaryDirectory()
    yield test_dir.name
    # Clean up the temporary directory
    test_dir.cleanup()

def create_test_file(temp_dir, filename, content):
    """Helper function to create a test file."""
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath

def test_function_usage_direct_import(temp_dir):
    code = """
from mylib import myfunc
myfunc()
"""
    create_test_file(temp_dir, 'test1.py', code)
    assert find_interface_used('myfunc', 'mylib', temp_dir)

def test_function_usage_aliased_import(temp_dir):
    code = """
from mylib import myfunc as mf
mf()
"""
    create_test_file(temp_dir, 'test2.py', code)
    assert find_interface_used('myfunc', 'mylib', temp_dir)

def test_function_usage_module_import(temp_dir):
    code = """
import mylib
mylib.myfunc()
"""
    create_test_file(temp_dir, 'test3.py', code)
    assert find_interface_used('myfunc', 'mylib', temp_dir)

def test_class_usage_direct_import(temp_dir):
    code = """
from mylib import MyClass
obj = MyClass()
"""
    create_test_file(temp_dir, 'test4.py', code)
    assert find_interface_used('MyClass', 'mylib', temp_dir)

def test_class_usage_aliased_import(temp_dir):
    code = """
from mylib import MyClass as MC
obj = MC()
"""
    create_test_file(temp_dir, 'test5.py', code)
    assert find_interface_used('MyClass', 'mylib', temp_dir)

def test_class_usage_module_import(temp_dir):
    code = """
import mylib
obj = mylib.MyClass()
"""
    create_test_file(temp_dir, 'test6.py', code)
    assert find_interface_used('MyClass', 'mylib', temp_dir)

def test_no_usage(temp_dir):
    code = """
from mylib import other_func
other_func()
"""
    create_test_file(temp_dir, 'test7.py', code)
    assert not find_interface_used('myfunc', 'mylib', temp_dir)

def test_multiple_files(temp_dir):
    code1 = """
from mylib import myfunc
"""
    code2 = """
myfunc()
"""
    create_test_file(temp_dir, 'test8a.py', code1)
    create_test_file(temp_dir, 'test8b.py', code2)
    assert find_interface_used('myfunc', 'mylib', temp_dir)

def test_invalid_python_file(temp_dir):
    code = "This is not valid Python code"
    create_test_file(temp_dir, 'test9.py', code)
    assert not find_interface_used('myfunc', 'mylib', temp_dir)