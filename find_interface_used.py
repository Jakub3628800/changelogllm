"""
find_interface_used.py

This script analyzes Python code to determine if a specific interface (function or class)
from a library is being used using static analysis with AST.
"""

import ast
import os

class ImportTracker(ast.NodeVisitor):
    def __init__(self):
        self.imports = {}  # Format: {alias: full_qualified_name}

    def visit_Import(self, node):
        for alias in node.names:
            self.imports[alias.asname or alias.name] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = f"{'.' * node.level}{node.module or ''}"
        for alias in node.names:
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports[alias.asname or alias.name] = full_name
        self.generic_visit(node)

class UsageChecker(ast.NodeVisitor):
    def __init__(self, target_name, is_function, aliases):
        self.target_name = target_name
        self.is_function = is_function
        self.aliases = set(aliases)
        self.used = False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.aliases:
            self.used = True
        elif isinstance(node.func, ast.Attribute):
            attr_parts = []
            current = node.func
            while isinstance(current, ast.Attribute):
                attr_parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                attr_parts.append(current.id)
                full_name = '.'.join(reversed(attr_parts))
                if full_name == self.target_name:
                    self.used = True
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if not self.is_function:
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id in self.aliases:
                    self.used = True
        self.generic_visit(node)

def is_interface_used(code, target_name, is_function):
    try:
        tree = ast.parse(code)
        tracker = ImportTracker()
        tracker.visit(tree)
        target_aliases = [alias for alias, full in tracker.imports.items() if full == target_name]
        target_aliases.append(target_name.split('.')[-1])
        checker = UsageChecker(target_name, is_function, target_aliases)
        checker.visit(tree)
        return checker.used
    except SyntaxError:
        return False

def find_interface_used(interface_name: str, target_lib: str, codebase_path: str) -> bool:
    """
    Main function to determine if an interface is being used.
    
    Args:
        interface_name: Name of the interface (function/class) to search for
        target_lib: Library/module where the interface is defined
        codebase_path: Path to the codebase to analyze
        
    Returns:
        bool: True if interface is used, False otherwise
    """
    target_name = f"{target_lib}.{interface_name}"
    is_function = True  # Default to function, can be enhanced to detect class
    
    for root, _, files in os.walk(codebase_path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    code = f.read()
                    if is_interface_used(code, target_name, is_function):
                        return True
    return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find if an interface is used in a codebase")
    parser.add_argument("interface", help="Interface name (function/class)")
    parser.add_argument("library", help="Library/module name")
    parser.add_argument("path", help="Path to codebase")
    args = parser.parse_args()
    
    result = find_interface_used(args.interface, args.library, args.path)
    print(f"Interface {args.library}.{args.interface} is {'used' if result else 'not used'} in {args.path}")