import pytest
from changelogllm.main import get_changelog


def test_get_changelog_latest():
    # Test getting latest changelog for popular packages
    packages = ["requests", "numpy", "pandas", "flask", "django"]

    for package in packages:
        result = get_changelog(package)
        assert isinstance(result, str)
        assert len(result) > 0


def test_get_changelog_specific_version():
    # Test getting specific versions
    test_cases = [("requests", "2.31.0"), ("numpy", "1.25.0"), ("pandas", "2.0.3")]

    for package, version in test_cases:
        result = get_changelog(package, version)
        assert isinstance(result, str)
        assert len(result) > 0
        assert version in result


def test_invalid_package():
    with pytest.raises(Exception):
        get_changelog("nonexistent-package-123456")


def test_invalid_version():
    with pytest.raises(ValueError):
        get_changelog("requests", "999.999.999")
