import os
import subprocess
import sys
from pathlib import Path

def find_changelog_files(package_dir):
    """Find changelog files in the installed package directory."""
    changelog_files = []
    for root, _, files in os.walk(package_dir):
        for file in files:
            if 'changelog' in file.lower() and file.endswith('.py'):
                changelog_files.append(Path(root) / file)
    return changelog_files

def get_changelog(package_name):
    """Get changelog text for a single library."""
    try:
        # Create a temporary virtual environment
        venv_dir = f'/tmp/{package_name}_venv'
        subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
        
        # Install the package
        pip_path = os.path.join(venv_dir, 'bin', 'pip')
        subprocess.run([pip_path, 'install', package_name], check=True)
        
        # Find the installed package directory
        site_packages = os.path.join(venv_dir, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')
        package_dir = os.path.join(site_packages, package_name.replace('-', '_'))
        
        # Find changelog files
        changelog_files = find_changelog_files(package_dir)
        
        if not changelog_files:
            return f"No changelog.py files found for {package_name}"
            
        # Read and return the first changelog file content
        with open(changelog_files[0], 'r') as f:
            return f.read()
            
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # Clean up the virtual environment
        if os.path.exists(venv_dir):
            subprocess.run(['rm', '-rf', venv_dir])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python get_changelog.py &lt;package_name&gt;")
        sys.exit(1)
        
    package_name = sys.argv[1]
    changelog = get_changelog(package_name)
    print(changelog)