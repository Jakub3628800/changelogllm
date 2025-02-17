import os
import pytest
from find_interface_used import find_interface_used


@pytest.fixture
def test_codebase(tmp_path):
    # Create test files with known line numbers
    code1 = """from mylib import myfunc

def func1():
    myfunc()  # Line 4
"""

    code2 = """from mylib import MyClass

class TestClass(MyClass):  # Line 3
    pass
"""

    code3 = """import mylib

def func2():
    mylib.myfunc()  # Line 4
"""

    code4 = """def func3():
    pass
"""

    # Create files in the temporary directory
    create_test_file(tmp_path / "module1.py", code1)
    create_test_file(tmp_path / "module2.py", code2)
    create_test_file(tmp_path / "module3.py", code3)
    create_test_file(tmp_path / "module4.py", code4)

    return tmp_path


def create_test_file(path, content):
    """Helper function to create a test file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return path


def test_find_function_usage(test_codebase):
    results = find_interface_used("myfunc", "mylib", str(test_codebase))
    assert len(results) == 2
    assert any("module1.py" in r["file_path"] for r in results)
    assert any("module3.py" in r["file_path"] for r in results)


def test_find_class_usage(test_codebase):
    results = find_interface_used("MyClass", "mylib", str(test_codebase))
    assert len(results) == 1
    assert "module2.py" in results[0]["file_path"]


def test_no_usage_found(test_codebase):
    results = find_interface_used("non_existent", "mylib", str(test_codebase))
    assert len(results) == 0


def test_show_lines_option(test_codebase):
    results = find_interface_used(
        "myfunc", "mylib", str(test_codebase), show_lines=True
    )
    assert len(results) == 2
    assert results[0]["line"] == 4  # Line number in module1.py
    assert results[1]["line"] == 4  # Line number in module3.py


def test_verbose_option(test_codebase):
    results = find_interface_used("myfunc", "mylib", str(test_codebase), verbose=True)
    assert len(results) == 2
    assert all(r["context"] is not None for r in results)
    assert any("myfunc()" in r["context"] for r in results)


def test_combined_options(test_codebase):
    results = find_interface_used(
        "myfunc", "mylib", str(test_codebase), show_lines=True, verbose=True
    )
    assert len(results) == 2
    assert all(r["line"] is not None for r in results)
    assert all(r["context"] is not None for r in results)
    assert any("myfunc()" in r["context"] for r in results)
