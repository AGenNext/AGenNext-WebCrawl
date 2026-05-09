"""
Version information for Web Crawler Service.

Semantic Versioning: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- BUGFIX: Bug fixes only

Release Types:
- alpha: Development testing
- beta: Feature complete, testing
- rc: Release candidate
- release: Stable release
"""

__version__ = "0.1.0"
__semver__ = "0.1.0"

# Version stages
VERSION_ALPHA = "alpha"
VERSION_BETA = "beta"
VERSION_RC = "rc"
VERSION_RELEASE = "release"

# Build info
__build__ = "001"

# API Version
__api_version__ = "v1"

# App info
APP_NAME = "web-crawler"
APP_TITLE = "Web Crawler Service"
APP_DESCRIPTION = "AI-powered web crawling with multiple providers"

# Supported versions
MIN_PYTHON = "3.10"

# Changelog URL
CHANGELOG_URL = "https://github.com/AGenNext/AGenNext-WebCrawl/releases"


def get_version():
    """Return current version string."""
    return __version__


def get_semver():
    """Return semantic version."""
    return __semver__


def is_stable():
    """Check if this is a stable release."""
    return "alpha" not in __version__ and "beta" not in __version__


def is_release():
    """Check if this is a release build."""
    return VERSION_RELEASE in __version__ or is_stable()


# Default to stable for now
__version_status__ = VERSION_RELEASE

# 2026-05-09


if __name__ == "__main__":
    print(f"{APP_NAME} v{__version__}")
    print(f"API: {__api_version__}")
    print(f"Status: {__version_status__}")