# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Playbook rule 15: the suite guards the docs.

Fails when a command-line flag of any script is missing from AGENTS.md or
docs/USER_MANUAL.md, when the README's stated check/figure counts drift from
the executed notebooks, or when VERSION / CHANGELOG / CITATION disagree.
"""

import os
import re
import sys

import pytest

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "build"))
sys.path.insert(0, os.path.join(ROOT, "course", "tools"))


def _read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def _flags(parser):
    out = set()
    for a in parser._actions:
        for s in a.option_strings:
            if s.startswith("--") and s not in ("--help",):
                out.add(s)
    return out


@pytest.mark.parametrize("module,builder", [
    ("pythtb_tools", "build_parser"),
    ("verify_pythtb", "build_parser"),
    ("watch_upstream", "build_parser"),
    ("extract_figures", "build_parser"),
    ("build_deck", "build_parser"),
    ("verify_deck", "build_parser"),
    ("build_pptx", "build_parser"),
    ("make_handout", "build_parser"),
    ("make_slides_pdf", "build_parser"),
])
def test_script_flags_are_documented(module, builder):
    mod = __import__(module)
    flags = _flags(getattr(mod, builder)())
    agents, manual = _read("AGENTS.md"), _read("docs", "USER_MANUAL.md")
    for f in flags:
        assert f in agents, f"{module}: {f} missing from AGENTS.md"
        assert f in manual, f"{module}: {f} missing from docs/USER_MANUAL.md"


def test_build_script_flags_are_documented():
    import assemble, execute  # noqa: E401
    flags = set()
    for mod in (assemble, execute):
        # both scripts build their parser inside main(); document the public flags by hand
        src = open(mod.__file__, encoding="utf-8").read()
        flags |= set(re.findall(r'add_argument\("(--[a-z\-]+)"', src))
    agents, manual = _read("AGENTS.md"), _read("docs", "USER_MANUAL.md")
    for f in sorted(flags):
        assert f in agents, f"{f} missing from AGENTS.md"
        assert f in manual, f"{f} missing from docs/USER_MANUAL.md"


def test_readme_counts_match_notebooks():
    from execute import tally
    main = tally(os.path.join(ROOT, "PythTB_Theory_and_Practice.ipynb"))
    ex = tally(os.path.join(ROOT, "PythTB_Exercises_Solutions.ipynb"))
    total_checks, total_figs = main["pass"] + ex["pass"], main["figures"] + ex["figures"]
    readme = _read("README.md")
    assert f"{total_checks} inline" in readme, f"README must state {total_checks} inline checks"
    assert f"{total_figs} figures" in readme, f"README must state {total_figs} figures"
    assert f"{main['pass']} inline physics checks" in readme
    assert f"{main['figures']} captioned figures" in readme
    manual = _read("docs", "USER_MANUAL.md")
    assert f"{main['pass']} inline physics checks" in manual and f"{ex['pass']} checks" in manual


def test_version_consistency():
    version = _read("VERSION").strip()
    assert re.fullmatch(r"\d+\.\d+\.\d+", version)
    assert f"## [{version}]" in _read("CHANGELOG.md")
    assert f'version: "{version}"' in _read("CITATION.cff")
