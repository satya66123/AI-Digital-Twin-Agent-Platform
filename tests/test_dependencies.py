"""Dependency smoke tests for AI Digital Twin Agent Platform.

These tests verify that the Python packages listed in requirements.txt
are installed and importable. They do not test provider credentials,
network connectivity, or application-level integrations.
"""

import importlib
import pytest


DEPENDENCY_MODULES = [
    ("streamlit", "streamlit"),
    ("python-dotenv", "dotenv"),
    ("requests", "requests"),
    ("pypdf", "pypdf"),
    ("python-docx", "docx"),
    ("openai", "openai"),
    ("anthropic", "anthropic"),
    ("google-genai", "google.genai"),
    ("mistralai", "mistralai"),
    ("groq", "groq"),
    ("cohere", "cohere"),
    ("pytest-cov", "pytest_cov"),
]


@pytest.mark.parametrize(
    ("distribution_name", "module_name"),
    DEPENDENCY_MODULES,
    ids=[item[0] for item in DEPENDENCY_MODULES],
)
def test_dependency_is_importable(distribution_name, module_name):
    """Every declared runtime/test dependency should be importable."""
    try:
        importlib.import_module(module_name)
    except Exception as exc:
        pytest.fail(
            f"Dependency '{distribution_name}' could not be imported "
            f"as '{module_name}': {exc}"
        )
