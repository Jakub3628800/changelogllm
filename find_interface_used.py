"""
find_interface_used.py

This script analyzes Python code to determine if a specific interface (function or class)
from a library is being used using static analysis with AST.

Usage:
    python find_interface_used.py [OPTIONS] INTERFACE LIBRARY PATH

Arguments:
    INTERFACE    Name of the interface (function/class) to search for
    LIBRARY      Library/module where the interface is defined
    PATH         Path to the codebase to analyze

Options:
    --show-lines  Show line numbers where interface is used (default: False)
    --verbose     Show detailed output (default: False)

Examples:
    1. Basic usage:
       python find_interface_used.py my_function my_lib ./src

    2. With line numbers:
       python find_interface_used.py --show-lines MyClass my_lib ./project

    3. Verbose output:
       python find_interface_used.py --verbose process_data data_lib ./src

Returns:
    List of dictionaries containing:
    - file_path: Path to file where interface is used
    - lines: List of line numbers (optional)
    - context: Code context (optional, verbose mode only)
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
    def __init__(self, target_name, is_function, aliases, show_lines=False, verbose=False):
        self.target_name = target_name
        self.is_function = is_function
        self.aliases = set(aliases)
        self.used = False
        self.show_lines = show_lines
        self.verbose = verbose
        self.usage_locations = []

    def visit_Call(self, node):
        usage_info = {
            'line': node.lineno,
            'context': ast.unparse(node) if self.verbose else None
        }
        
        if isinstance(node.func, ast.Name) and node.func.id in self.aliases:
            self.used = True
            self.usage_locations.append(usage_info)
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
                    self.usage_locations.append(usage_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if not self.is_function:
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id in self.aliases:
                    self.used = True
                    self.usage_locations.append({
                        'line': node.lineno,
                        'context': ast.unparse(node) if self.verbose else None
                    })
        self.generic_visit(node)

def is_interface_used(code, target_name, is_function, show_lines=False, verbose=False):
    try:
        tree = ast.parse(code)
        tracker = ImportTracker()
        tracker.visit(tree)
        target_aliases = [alias for alias, full in tracker.imports.items() if full == target_name]
        target_aliases.append(target_name.split('.')[-1])
        checker = UsageChecker(target_name, is_function, target_aliases, show_lines, verbose)
        checker.visit(tree)
        return {
            'used': checker.used,
            'locations': checker.usage_locations
        }
    except SyntaxError:
        return {
            'used': False,
            'locations': []
        }

def find_interface_used(interface_name: str, target_lib: str, codebase_path: str, show_lines=False, verbose=False) -> list:
    """
    Main function to find where an interface is being used.
    
    Args:
        interface_name: Name of the interface (function/class) to search for
        target_lib: Library/module where the interface is defined
        codebase_path: Path to the codebase to analyze
        show_lines: Whether to include line numbers in results
        verbose: Whether to include code context in results
        
    Returns:
        list: List of dictionaries containing usage locations with file paths and optional line numbers
    """
    target_name = f"{target_lib}.{interface_name}"
    is_function = True  # Default to function, can be enhanced to detect class
    results = []
    
    for root, _, files in os.walk(codebase_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                    usage = is_interface_used(code, target_name, is_function, show_lines, verbose)
                    if usage['used']:
                        for location in usage['locations']:
                            result = {
                                'file_path': file_path,
                                'line': location['line'] if show_lines else None,
                                'context': location['context'] if verbose else None
                            }
                            results.append(result)
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find where an interface is used in a codebase")
    parser.add_argument("interface", help="Interface name (function/class)")
    parser.add_argument("library", help="Library/module name")
    parser.add_argument("path", help="Path to codebase")
    parser.add_argument("--show-lines", action="store_true", help="Show line numbers where interface is used")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output with code context")
    args = parser.parse_args()
    
    results = find_interface_used(args.interface, args.library, args.path, args.show_lines, args.verbose)
    
    if results:
        print(f"Interface {args.library}.{args.interface} is used in:")
        for result in results:
            output = f"- {result['file_path']}"
            if args.show_lines:
                output += f" (line {result['line']})"
            if args.verbose and result['context']:
                output += f"\n  Context: {result['context']}"
            print(output)
    else:
        print(f"Interface {args.library}.{args.interface} is not used in {args.path}")