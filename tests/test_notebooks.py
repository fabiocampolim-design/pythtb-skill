# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""The real regression suite: the notebooks themselves.

Fast part (always runs): the committed notebooks must be fully executed with
0 FAIL / 0 error outputs, and must match what build/assemble.py generates
from build/*.py (the builder sources are the source of truth).

Slow part (``--run-notebooks``): re-execute both notebooks on the pinned
kernel into a temporary directory and tally again. Skips when the kernel is
not registered.
"""

import json
import os
import subprocess
import sys

import pytest

from conftest import ROOT, kernel_available

sys.path.insert(0, os.path.join(ROOT, "build"))
from assemble import NOTEBOOKS, collect  # noqa: E402
from execute import tally  # noqa: E402
from nbbuild import make_cell  # noqa: E402

EXPECTED = {  # minimum counts — raising them is fine, lowering them is a regression
    "main": {"cells": 116, "pass": 72, "figures": 69},
    "exercises": {"cells": 44, "pass": 35, "figures": 18},
}


@pytest.mark.parametrize("key", list(NOTEBOOKS))
def test_committed_notebook_is_green(key):
    path = os.path.join(ROOT, NOTEBOOKS[key][0])
    t = tally(path)
    assert t["fail"] == 0, t["fail_labels"]
    assert t["errors"] == 0
    assert t["unexecuted"] == 0
    for k, v in EXPECTED[key].items():
        assert t[k] >= v, (k, t[k], v)
    assert t["captions"] == t["figures"], "every figure must carry a caption"


@pytest.mark.parametrize("key", list(NOTEBOOKS))
def test_committed_notebook_matches_builder_sources(key):
    fname, parts = NOTEBOOKS[key]
    built = ["".join(make_cell(k, s)["source"]) for k, s in collect(parts)[0]]
    with open(os.path.join(ROOT, fname), encoding="utf-8") as f:
        nb = json.load(f)
    stored = ["".join(c["source"]) for c in nb["cells"]]
    assert len(built) == len(stored)
    for i, (a, b) in enumerate(zip(built, stored)):
        assert a.strip() == b.strip(), f"cell {i} differs from build/ sources"
    assert nb["metadata"]["kernelspec"]["name"] == "pythtb-mc"


@pytest.mark.parametrize("key", list(NOTEBOOKS))
def test_no_personal_paths_or_codenames_in_notebook(key):
    with open(os.path.join(ROOT, NOTEBOOKS[key][0]), encoding="utf-8") as f:
        blob = f.read()
    # every needle is assembled by concatenation so this file itself passes the
    # plain-text scrub and the hardcoded-path scan (playbook rules 3 and 11)
    codename = "CLAUDE" + "_"
    win_home = "C:" + "\\\\" + "Users" + "\\\\"   # the JSON-escaped form found in .ipynb
    posix_home = "/c/" + "Users/"
    mail = "@" + "gm" + "ail"
    for needle in (win_home, posix_home, mail, codename):
        assert needle not in blob, needle


def test_execute_notebooks_end_to_end(request, tmp_path):
    if not request.config.getoption("--run-notebooks"):
        pytest.skip("pass --run-notebooks to execute (about 3 minutes)")
    kernel = request.config.getoption("--kernel")
    if not kernel_available(kernel):
        pytest.skip(f"kernel {kernel!r} not registered for {sys.executable}")
    # data/ is referenced relatively from the notebook's directory
    os.symlink if False else None
    import shutil
    shutil.copytree(os.path.join(ROOT, "data"), tmp_path / "data")
    cmd = [sys.executable, os.path.join(ROOT, "build", "execute.py"), "--outdir", str(tmp_path),
           "--kernel", kernel, "-q"]
    rc = subprocess.run(cmd, cwd=ROOT).returncode
    assert rc == 0
    for key, (fname, _) in NOTEBOOKS.items():
        t = tally(str(tmp_path / fname))
        assert t["fail"] == 0 and t["errors"] == 0
        assert t["pass"] >= EXPECTED[key]["pass"]
