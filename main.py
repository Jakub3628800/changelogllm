import sys
import requests
from typing import Optional
from datetime import datetime
from packaging.version import parse

def get_changelog(package_name: str, version: Optional[str] = None) -> str:
    """Fetch changelog for a given package and optional version."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    response.raise_for_status()
    
    package_info = response.json()
    releases = package_info.get('releases', {})
    
    if version:
        if version not in releases:
            raise ValueError(f"Version {version} not found for package {package_name}")
        return releases[version][0].get('upload_time', '') + "\n" + releases[version][0].get('description', '')
    
    # Get latest version if no version specified
    latest_version = max(releases.keys(), key=parse)
    return releases[latest_version][0].get('upload_time', '') + "\n" + releases[latest_version][0].get('description', '')

def main():
    if len(sys.argv) < 2:
        print("Usage: changelogllm <package_name> [version]")
        sys.exit(1)
    
    package_name = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        changelog = get_changelog(package_name, version)
        print(changelog)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()