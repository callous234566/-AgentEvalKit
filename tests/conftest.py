"""Shared fixtures for the test suite."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure project root is on sys.path so imports resolve.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture()
def temp_dir():
    """Provide a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture()
def env_sandbox():
    """Snapshot and restore os.environ so tests can mutate env vars safely."""
    original = os.environ.copy()
    yield os.environ
    os.environ.clear()
    os.environ.update(original)
