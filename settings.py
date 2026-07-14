"""
Runtime settings module.

Provides a single access point for environment-aware application settings.
Values may be overridden via environment variables in future iterations.
"""

import os

from config import get_config

_CONFIG = get_config()

# Application identity
APP_NAME = _CONFIG.app_name

# Runtime flags
DEBUG = os.getenv("INSIGHTFLOW_DEBUG", str(_CONFIG.debug)).lower() in {
    "1",
    "true",
    "yes",
}

# Paths
BASE_DIR = str(_CONFIG.base_dir)
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
