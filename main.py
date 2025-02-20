import sys
import requests
from typing import Optional


def get_changelog(package_name: str, version: Optional[str] = None) -> str:
    """Fetch changelog for a given package from GitHub releases."""
    try:
        url = f"https://api.github.com/repos/{package_name}/releases"
        response = requests.get(url)
        response.raise_for_status()
        releases = response.json()
        
        if version:
            for release in releases:
                if release['tag_name'] == version:
                    return release['body']
            raise ValueError(f"Version {version} not found")
            
        return releases[0]['body']
    except Exception as e:
        raise ValueError(f"Failed to fetch changelog: {str(e)}")


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
