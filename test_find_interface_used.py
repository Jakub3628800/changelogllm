import unittest
import os
import tempfile
from find_interface_used import find_interface_used


class TestFindInterfaceUsed(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = self.test_dir.name

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def create_test_file(self, filename, content):
        """Helper function to create a test file."""
        filepath = os.path.join(self.test_path, filename)
        with open(filepath, "w") as f:
            f.write(content)
        return filepath

    def test_function_usage_direct_import(self):
        code = """
from mylib import myfunc
myfunc()
"""
        self.create_test_file("test1.py", code)
        self.assertTrue(find_interface_used("myfunc", "mylib", self.test_path))

    def test_function_usage_aliased_import(self):
        code = """
from mylib import myfunc as mf
mf()
"""
        self.create_test_file("test2.py", code)
        self.assertTrue(find_interface_used("myfunc", "mylib", self.test_path))

    def test_function_usage_module_import(self):
        code = """
import mylib
mylib.myfunc()
"""
        self.create_test_file("test3.py", code)
        self.assertTrue(find_interface_used("myfunc", "mylib", self.test_path))

    def test_class_usage_direct_import(self):
        code = """
from mylib import MyClass
obj = MyClass()
"""
        self.create_test_file("test4.py", code)
        self.assertTrue(find_interface_used("MyClass", "mylib", self.test_path))

    def test_class_usage_aliased_import(self):
        code = """
from mylib import MyClass as MC
obj = MC()
"""
        self.create_test_file("test5.py", code)
        self.assertTrue(find_interface_used("MyClass", "mylib", self.test_path))

    def test_class_usage_module_import(self):
        code = """
import mylib
obj = mylib.MyClass()
"""
        self.create_test_file("test6.py", code)
        self.assertTrue(find_interface_used("MyClass", "mylib", self.test_path))

    def test_no_usage(self):
        code = """
from mylib import other_func
other_func()
"""
        self.create_test_file("test7.py", code)
        self.assertFalse(find_interface_used("myfunc", "mylib", self.test_path))

    def test_multiple_files(self):
        code1 = """
from mylib import myfunc
"""
        code2 = """
myfunc()
"""
        self.create_test_file("test8a.py", code1)
        self.create_test_file("test8b.py", code2)
        self.assertTrue(find_interface_used("myfunc", "mylib", self.test_path))

    def test_invalid_python_file(self):
        code = "This is not valid Python code"
        self.create_test_file("test9.py", code)
        self.assertFalse(find_interface_used("myfunc", "mylib", self.test_path))


if __name__ == "__main__":
    unittest.main()
