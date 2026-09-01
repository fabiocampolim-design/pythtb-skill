# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""The real regression suite: the notebooks themselves.

Fast part (always runs): every committed chapter notebook must be fully
executed with 0 FAIL / 0 error outputs, must match what build/assemble.py
generates from build/*.py (the builder sources are the source of truth), must
carry the generated header (title, table of contents, navigation) and must be
small enough to open (the split into chapters exists because a 5 MB notebook
crashed viewers). The book-wide minimum counts guard against silent loss.

Slow part (``--run-notebooks``): re-execute every chapter on the pinned
kernel into a temporary directory and tally again. Skips when the kernel is
not registered.
"""

import json
import os
import re
import subprocess
import sys

import pytest

from conftest import ROOT, kernel_available

sys.path.insert(0, os.path.join(ROOT, "build"))
from assemble import (BY_KEY, CHAPTERS, EXERCISE_KEYS, MAIN_KEYS,  # noqa: E402
                      chapter_cells, headings, collect, index_markdown, outputs)
from execute import tally, tally_series  # noqa: E402
from nbbuild import make_cell  # noqa: E402

KEYS = [c.key for c in CHAPTERS]
PATHS = outputs(ROOT)
EXPECTED = {  # book-wide minimum counts — raising them is fine, lowering them is a regression
    "main": {"cells": 140, "pass": 72, "figures": 69},
    "exercises": {"cells": 45, "pass": 35, "figures": 18},
}
MAX_NOTEBOOK_BYTES = 1_500_000      # the whole point of the split


def _nb(key):
    with open(PATHS[key], encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("key", KEYS)
def test_committed_notebook_is_green(key):
    t = tally(PATHS[key])
    assert t["fail"] == 0, t["fail_labels"]
    assert t["errors"] == 0
    assert t["unexecuted"] == 0
    assert t["captions"] == t["figures"], "every figure must carry a caption"
    if key != "00":
        assert t["pass"] >= 1, "a chapter without any check is not verified"


@pytest.mark.parametrize("series,keys", [("main", MAIN_KEYS), ("exercises", EXERCISE_KEYS)])
def test_series_totals_do_not_regress(series, keys):
    t = tally_series([PATHS[k] for k in keys])
    for k, v in EXPECTED[series].items():
        assert t[k] >= v, (series, k, t[k], v)


@pytest.mark.parametrize("key", KEYS)
def test_committed_notebook_matches_builder_sources(key):
    built = ["".join(make_cell(k, s)["source"]) for k, s in chapter_cells(key)]
    nb = _nb(key)
    stored = ["".join(c["source"]) for c in nb["cells"]]
    assert len(built) == len(stored), f"{key}: {len(built)} cells built, {len(stored)} stored"
    for i, (a, b) in enumerate(zip(built, stored)):
        assert a.strip() == b.strip(), f"{key}: cell {i} differs from build/ sources"
    assert nb["metadata"]["kernelspec"]["name"] == "pythtb-mc"


def test_index_matches_builder_sources():
    with open(os.path.join(ROOT, "chapters", "README.md"), encoding="utf-8") as f:
        assert f.read() == index_markdown(), "run build/assemble.py (chapters/README.md is generated)"


@pytest.mark.parametrize("key", KEYS)
def test_notebook_is_small_enough_to_open(key):
    size = os.path.getsize(PATHS[key])
    assert size <= MAX_NOTEBOOK_BYTES, f"{BY_KEY[key].file} is {size / 1e6:.1f} MB — split it"


@pytest.mark.parametrize("key", [k for k in KEYS if k != "00"])
def test_chapter_header_has_toc_and_navigation(key):
    """First cell: title, one TOC entry per section heading, links that resolve."""
    ch = BY_KEY[key]
    cells = _nb(key)["cells"]
    head = "".join(cells[0]["source"])
    assert cells[0]["cell_type"] == "markdown"
    assert head.startswith('<a id="top"></a>\n# ')
    assert "[Contents of the book](README.md)" in head
    anchors = {a for a, _ in headings(collect(ch.parts)[0])}
    assert anchors, "a chapter must have at least one section heading"
    for anchor in anchors:
        assert f"](#{anchor})" in head, f"{key}: TOC entry for #{anchor} missing"
    body = "".join("".join(c["source"]) for c in cells[1:])
    for anchor in anchors:
        assert f'<a id="{anchor}"></a>' in body, f"{key}: anchor #{anchor} missing"
    for target in re.findall(r"\]\(([^)#]+\.(?:ipynb|md))\)", head):
        assert os.path.exists(os.path.join(ROOT, "chapters", target)), f"{key}: broken link {target}"
    series = [c for c in CHAPTERS if c.series == ch.series]
    i = series.index(ch)
    if i > 0:
        assert f"]({series[i - 1].file})" in head, "previous-chapter link missing"
    if i + 1 < len(series):
        assert f"]({series[i + 1].file})" in head, "next-chapter link missing"


@pytest.mark.parametrize("key", [k for k in KEYS if k != "00"])
def test_every_chapter_runs_on_its_own(key):
    """The shared setup cell is present and the last cell is the tally."""
    cells = _nb(key)["cells"]
    codes = [c for c in cells if c["cell_type"] == "code"]
    assert "shared setup" in "".join(codes[0]["source"])
    assert "tally for this notebook" in "".join(cells[-1]["source"])
    text = "".join(o.get("text", "") if isinstance(o.get("text"), str) else "".join(o.get("text", []))
                   for o in cells[-1].get("outputs", []))
    assert "checks failed : 0" in text


def test_figure_numbers_run_through_the_book():
    """Figure numbers continue across chapters (offset in the setup cell)."""
    for keys in (MAIN_KEYS, EXERCISE_KEYS):
        expected = 1
        for key in keys:
            nb = _nb(key)
            for c in nb["cells"]:
                for o in c.get("outputs", []) if c["cell_type"] == "code" else []:
                    html = "".join(o.get("data", {}).get("text/html", []))
                    m = re.search(r"<b>Figure (\d+)\.</b>", html)
                    if m:
                        assert int(m.group(1)) == expected, (key, m.group(1), expected)
                        expected += 1


@pytest.mark.parametrize("key", KEYS)
def test_no_personal_paths_or_codenames_in_notebook(key):
    with open(PATHS[key], encoding="utf-8") as f:
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
    import shutil
    # data/ is found relatively from the notebook's directory (../data)
    shutil.copytree(os.path.join(ROOT, "data"), tmp_path / "data")
    cmd = [sys.executable, os.path.join(ROOT, "build", "execute.py"), "--outdir", str(tmp_path),
           "--kernel", kernel, "-q"]
    rc = subprocess.run(cmd, cwd=ROOT).returncode
    assert rc == 0
    for series, keys in (("main", MAIN_KEYS), ("exercises", EXERCISE_KEYS)):
        t = tally_series([str(tmp_path / "chapters" / BY_KEY[k].file) for k in keys])
        assert t["fail"] == 0 and t["errors"] == 0
        assert t["pass"] >= EXPECTED[series]["pass"]
