# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Shared fixtures for the regression suite.

Run from the repository root:  python -m pytest tests
Slow notebook executions are opt-in:  python -m pytest tests --run-notebooks
"""

import os
import subprocess
import sys

import pytest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def pytest_addoption(parser):
    parser.addoption("--run-notebooks", action="store_true", default=False,
                     help="execute both notebooks end-to-end (about 3 minutes)")
    parser.addoption("--kernel", default="pythtb-mc",
                     help="Jupyter kernel to execute the notebooks with")


def kernel_available(name):
    """True if `jupyter kernelspec list` (of this interpreter) knows `name`."""
    try:
        out = subprocess.run([sys.executable, "-m", "jupyter", "kernelspec", "list"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:  # noqa: BLE001
        return False
    return any(line.strip().startswith(name + " ") or line.strip() == name
               for line in out.splitlines())


@pytest.fixture(scope="session")
def repo_root():
    return ROOT


@pytest.fixture(scope="session")
def pythtb():
    return pytest.importorskip("pythtb")
