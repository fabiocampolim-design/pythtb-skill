# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Assemble the chapter notebooks from the part modules in this directory.

The book *PythTB — Tight-Binding Physics from Theory to Code* is shipped as
one notebook per chapter under ``chapters/`` (a single 5 MB notebook crashed
viewers), plus two exercise notebooks. Every chapter is self-contained: it
starts with a generated header (title, table of contents with anchors,
previous/index/next links), the shared setup cell (``part00_intro.SETUP_TEMPLATE``,
with the figure counter offset so figure numbers run through the book), the
part module's cells, and a generated tally cell. Section numbers (§1–31) are
global. ``chapters/README.md`` (the book index) is generated here too.

Each part module defines ``CELLS = [("md", ...), ("code", ...), ...]``. Cell
*outputs* are not produced here — run ``build/execute.py`` afterwards.

Usage:
    python build/assemble.py                     # every chapter + the index, into chapters/
    python build/assemble.py --which main        # the eight book chapters + chapter 0
    python build/assemble.py --which exercises   # the two exercise notebooks
    python build/assemble.py --which 04          # one chapter (key from --list)
    python build/assemble.py --outdir out/ -v    # elsewhere (a chapters/ folder is created), chatty
    python build/assemble.py --list              # show chapters, parts and cell counts, write nothing

Every invocation appends an audit record to ``<log-dir>/assemble.log``
(default ``<outdir>/logs``) with the command line, versions and outcome.
"""

import argparse
import functools
import importlib
import os
import re
import sys
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from nbbuild import write_notebook, md, code  # noqa: E402
from buildlog import AuditLog  # noqa: E402

CHAPTERS_DIR = "chapters"          # relative to the repository root
BOOK_TITLE = "PythTB — Tight-Binding Physics from Theory to Code"

Chapter = namedtuple("Chapter", "key file title part series parts")
# series: "main" (the book, chapter 0 = introduction) or "exercises";
# part: the Part of the book the chapter belongs to (shown in the header)
CHAPTERS = [
    Chapter("00", "PythTB_00_Introduction.ipynb", "Introduction", "",
            "main", ["part00_intro"]),
    Chapter("01", "PythTB_01_Foundations.ipynb",
            "Foundations: chains, SSH, graphene and flat bands",
            "Part I — Fundamentals", "main", ["part01a_foundations"]),
    Chapter("02", "PythTB_02_Finite_Systems_and_Berry_Phases.ipynb",
            "Finite systems, spin and the Berry-phase machinery",
            "Part I — Fundamentals", "main", ["part01b_finite_berry"]),
    Chapter("03", "PythTB_03_Three_Dimensions_and_Wannier.ipynb",
            "Three dimensions, Wannier90 import and Wannierization",
            "Part I — Fundamentals", "main", ["part01c_3d_w90"]),
    Chapter("04", "PythTB_04_Chern_and_Z2.ipynb",
            "Chern and Z₂ insulators: Haldane, Kane–Mele, BHZ",
            "Part II — Topological matter", "main", ["part02a_chern_z2"]),
    Chapter("05", "PythTB_05_Higher_Order_and_Kitaev.ipynb",
            "Higher-order topology and the Kitaev chain",
            "Part II — Topological matter", "main", ["part02b_hoti_kitaev"]),
    Chapter("06", "PythTB_06_Weyl_and_Axion.ipynb",
            "Weyl semimetals and the axion angle",
            "Part II — Topological matter", "main", ["part02c_weyl_axion"]),
    Chapter("07", "PythTB_07_Stretching_PythTB.ipynb",
            "Stretching PythTB: butterfly, disorder, quasicrystal, the wall",
            "Part III — Stretching PythTB", "main", ["part03_stretching"]),
    Chapter("08", "PythTB_08_What_PythTB_Cannot_Do.ipynb",
            "What PythTB cannot do",
            "Part IV — What PythTB cannot do", "main", ["part04_limitations"]),
    Chapter("ex1", "PythTB_Exercises_I-II.ipynb",
            "Exercises and worked solutions — Parts I–II",
            "", "exercises", ["ex_part1_2"]),
    Chapter("ex2", "PythTB_Exercises_III-IV.ipynb",
            "Exercises and worked solutions — Parts III–IV",
            "", "exercises", ["ex_part3_4"]),
]
BY_KEY = {c.key: c for c in CHAPTERS}
MAIN_KEYS = [c.key for c in CHAPTERS if c.series == "main"]
EXERCISE_KEYS = [c.key for c in CHAPTERS if c.series == "exercises"]
# backwards-compatible view: series -> [(file, parts), ...]
NOTEBOOKS = {
    "main": [(c.file, c.parts) for c in CHAPTERS if c.series == "main"],
    "exercises": [(c.file, c.parts) for c in CHAPTERS if c.series == "exercises"],
}

SECTION = re.compile(r"^##\s+(\d+)\.\s+(.*)$")               # ## 14. Title
PART_EXERCISES = re.compile(r"^##\s+Exercises for Part\s+([IVX]+)\s*$")
EXERCISE = re.compile(r"^##\s+([IVX]+\.\d+)\s+—\s+(.*)$")     # ## II.3 — Title
CAPTION_CALL = re.compile(r"(?<!def )(?<![\w.])caption\(")


@functools.lru_cache(maxsize=None)
def _part_cells(name):
    """The CELLS of one part module, imported once (the assembler asks many times)."""
    return tuple(importlib.import_module(name).CELLS)


def collect(parts):
    """Return (cells, [(part_name, n_cells), ...]) for the given part modules."""
    cells = []
    per_part = []
    for name in parts:
        part = _part_cells(name)
        per_part.append((name, len(part)))
        cells.extend(part)
    return cells, per_part


def headings(cells):
    """[(anchor, label)] for every section / exercise heading among the cells."""
    out = []
    for kind, src in cells:
        if kind != "md":
            continue
        for line in src.splitlines():
            line = line.strip()
            m = SECTION.match(line)
            if m:
                out.append((f"sec-{int(m.group(1))}", f"§{m.group(1)} {m.group(2).strip()}"))
                continue
            m = PART_EXERCISES.match(line)
            if m:
                out.append((f"exercises-{m.group(1)}", f"Exercises for Part {m.group(1)}"))
                continue
            m = EXERCISE.match(line)
            if m:
                out.append((f"ex-{m.group(1).replace('.', '-')}", f"{m.group(1)} — {m.group(2).strip()}"))
    return out


def anchored(cells):
    """The same cells with an HTML anchor in front of every heading cell."""
    out = []
    for kind, src in cells:
        if kind == "md":
            for line in src.splitlines():
                line = line.strip()
                m = SECTION.match(line) or PART_EXERCISES.match(line) or EXERCISE.match(line)
                if m:
                    if SECTION.match(line):
                        anchor = f"sec-{int(m.group(1))}"
                    elif PART_EXERCISES.match(line):
                        anchor = f"exercises-{m.group(1)}"
                    else:
                        anchor = f"ex-{m.group(1).replace('.', '-')}"
                    src = f'<a id="{anchor}"></a>\n\n' + src.strip("\n")
                    break
        out.append((kind, src))
    return out


def figures_in(cells):
    """Number of figures the cells produce: one ``caption(...)`` call each
    (the helper's own ``def caption(`` does not match)."""
    return sum(len(CAPTION_CALL.findall(src)) for kind, src in cells if kind == "code")


@functools.lru_cache(maxsize=None)
def figure_offset(key):
    """Figures produced by the earlier chapters of the same series."""
    ch = BY_KEY[key]
    n = 0
    for other in CHAPTERS:
        if other.series != ch.series:
            continue
        if other.key == key:
            break
        n += figures_in(collect(other.parts)[0])
    return n


def _number(ch):
    if ch.series == "main":
        return f"chapter {int(ch.key)}"
    return f"exercises {ch.title.split('— ')[-1]}"


def _label(ch):
    return f"{int(ch.key)} {ch.title}" if ch.series == "main" else ch.title


def header_cell(key):
    """Generated first cell: title, position in the book, TOC, navigation."""
    ch = BY_KEY[key]
    series = [c for c in CHAPTERS if c.series == ch.series]
    i = series.index(ch)
    prev_ch = series[i - 1] if i > 0 else None
    next_ch = series[i + 1] if i + 1 < len(series) else None
    cells = collect(ch.parts)[0]
    lines = ['<a id="top"></a>']
    if ch.series == "main":
        lines.append(f"# Chapter {int(ch.key)} — {ch.title}")
        where = f"**{BOOK_TITLE}**"
        if ch.part:
            where += f" · {ch.part}"
        where += f" · chapter {int(ch.key)} of {len(series) - 1}" if int(ch.key) else " · the book's introduction"
    else:
        lines.append(f"# {ch.title}")
        where = f"**{BOOK_TITLE}** · exercise notebook {i + 1} of {len(series)}"
    lines += ["", where, ""]
    nav = []
    if prev_ch:
        nav.append(f"[◀ {_label(prev_ch)}]({prev_ch.file})")
    nav.append("[Contents of the book](README.md)")
    if next_ch:
        nav.append(f"[{_label(next_ch)} ▶]({next_ch.file})")
    lines += [" · ".join(nav), ""]
    toc = headings(cells)
    if toc:
        lines.append("**In this notebook**" if ch.series == "exercises" else "**In this chapter**")
        lines.append("")
        lines += [f"- [{label}](#{anchor})" for anchor, label in toc]
        lines.append("")
    if ch.series == "main":
        others = " · ".join(f"[{int(c.key)}]({c.file})" for c in series)
        lines.append(f"All chapters: {others} · exercises: " +
                     " · ".join(f"[{c.title.split('— ')[-1]}]({c.file})"
                                for c in CHAPTERS if c.series == "exercises"))
    else:
        lines.append("Chapters: " + " · ".join(f"[{int(c.key)}]({c.file})"
                                                for c in CHAPTERS if c.series == "main"))
    lines += ["",
              "*Every notebook runs on its own: the setup cell below is identical in all of them, "
              "and a chapter that reuses a model from an earlier one rebuilds it in a short recap cell. "
              "Section numbers (§1–31), figure numbers and cross-references are global to the book.*"]
    return md("\n".join(lines))


def tally_cell(key):
    ch = BY_KEY[key]
    label = _number(ch)
    return code(f'''
# ---- tally for this notebook ---------------------------------------------------
print("=" * 66)
print(f"{label} — checks passed : {{_CHECKS['pass']}}")
print(f"{label} — checks failed : {{_CHECKS['fail']}}")
print(f"wall time{' ' * (len(label) + 8)}: {{time.time() - t_chapter_start:.0f}} s")
print("=" * 66)
print("Every quantitative claim in this notebook was verified in this run."
      if _CHECKS["fail"] == 0 else "Some checks FAILED — search this notebook for '[FAIL]'.")
''')


def chapter_list_markdown():
    """The book index as a markdown list (used in chapter 0 and README.md)."""
    lines = []
    for c in CHAPTERS:
        if c.series != "main":
            continue
        secs = [lbl for a, lbl in headings(collect(c.parts)[0]) if a.startswith("sec-")]
        if secs:
            first, last = secs[0].split()[0], secs[-1].split()[0]
            span = f" ({first}–{last})" if first != last else f" ({first})"
        else:
            span = ""
        part = f" — *{c.part}*" if c.part and (c.key == "01" or BY_KEY[f'{int(c.key) - 1:02d}'].part != c.part) else ""
        lines.append(f"- **[{int(c.key)}. {c.title}]({c.file})**{span}{part}")
    lines.append("- Exercises with worked solutions: " + " · ".join(
        f"[{c.title.split('— ')[-1]}]({c.file})" for c in CHAPTERS if c.series == "exercises"))
    return "\n".join(lines)


def chapter_cells(key):
    """The complete cell list of one chapter notebook — the single source of truth."""
    ch = BY_KEY[key]
    cells = collect(ch.parts)[0]
    if ch.series == "main":
        import part00_intro as intro
        setup = intro.setup_cell(_number(ch), figure_offset(key))
        if key == "00":
            body = [(k, s.replace("__CHAPTER_LIST__", chapter_list_markdown())) for k, s in cells]
            return body + [setup]
        return [header_cell(key), setup] + anchored(cells) + [tally_cell(key)]
    import ex_common
    setup = ex_common.setup_cell(_number(ch), figure_offset(key))
    return [header_cell(key), md(ex_common.INTRO), setup] + anchored(cells) + [tally_cell(key)]


def index_markdown():
    """chapters/README.md — the book's table of contents."""
    rows = []
    for c in CHAPTERS:
        cells = collect(c.parts)[0]
        secs = [lbl for a, lbl in headings(cells) if not a.startswith("exercises-")]
        n_code = sum(1 for k, _ in chapter_cells(c.key) if k == "code")
        what = "; ".join(s.split(" ", 1)[1] if s.startswith("§") else s for s in secs)
        if c.series == "main" and c.key != "00":
            span = f"§{secs[0].split()[0][1:]}–{secs[-1].split()[0][1:]}" if secs else ""
            name = f"{int(c.key)} — {c.title}"
        elif c.key == "00":
            span, name, what = "", "0 — Introduction", "what the book is, how to run it, conventions, the shared setup cell"
        else:
            span = f"{secs[0].split(' — ')[0]}–{secs[-1].split(' — ')[0]}" if secs else ""
            name = c.title
        rows.append(f"| [{name}]({c.file}) | {span} | {n_code} | {what} |")
    return f"""# {BOOK_TITLE}

One notebook per chapter. Each runs on its own (the setup cell is the same in all of them);
section numbers §1–31, figure numbers and cross-references are global to the book, so "§14"
means section 14 wherever it lives. Start with chapter 0, or jump to any chapter — the header
of each links to the previous and next one and lists its sections.

| Notebook | Sections | Code cells | Contents |
|---|---|---|---|
{chr(10).join(rows)}

The exercise statements are at the end of the last chapter of each part (chapters 3, 6, 7, 8);
the two exercise notebooks hold the worked solutions.

Generated by `build/assemble.py` from `build/*.py` — do not edit the notebooks or this file by
hand (a test compares them with the sources). Re-execute with `build/execute.py`.
"""


def outputs(root=ROOT):
    """{key: absolute path of the chapter notebook} for a repository root."""
    return {c.key: os.path.join(root, CHAPTERS_DIR, c.file) for c in CHAPTERS}


def select(which):
    if which == "all":
        return [c.key for c in CHAPTERS]
    if which in NOTEBOOKS:
        return [c.key for c in CHAPTERS if c.series == which]
    if which in BY_KEY:
        return [which]
    raise SystemExit(f"unknown --which {which!r}; use all, main, exercises or one of "
                     + ", ".join(BY_KEY))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--which", default="all",
                    help="all (default), main, exercises, or one chapter key (see --list)")
    ap.add_argument("--outdir", default=ROOT,
                    help="repository root receiving chapters/*.ipynb (default: this repository)")
    ap.add_argument("--log-dir", default=None,
                    help="where the audit log goes (default: <outdir>/logs)")
    ap.add_argument("--list", action="store_true",
                    help="print chapters, parts and cell counts, do not write anything")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("-v", "--verbose", action="store_true")
    g.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args(argv)

    log = AuditLog("assemble", args.outdir, args.log_dir, verbose=args.verbose,
                   quiet=args.quiet, dry=args.list)
    rc = 0
    try:
        keys = select(args.which)      # an unknown --which is an audited failure too
        chapters_dir = os.path.join(args.outdir, CHAPTERS_DIR)
        for key in keys:
            ch = BY_KEY[key]
            cells = chapter_cells(key)
            for name, n in collect(ch.parts)[1]:
                log.debug(f"  {name:<28s} {n:4d} cells")
            if args.list:
                log.info(f"{key:>3s}  {ch.file}: {len(cells)} cells, "
                         f"{figures_in(cells)} figures (numbered from {figure_offset(key) + 1})")
                continue
            os.makedirs(chapters_dir, exist_ok=True)
            out = os.path.join(chapters_dir, ch.file)
            write_notebook(cells, out, echo=False)
            log.info(f"wrote {out} ({len(cells)} cells)")
        if not args.list:
            index = os.path.join(chapters_dir, "README.md")
            with open(index, "w", encoding="utf-8", newline="\n") as f:
                f.write(index_markdown())
            log.info(f"wrote {index}")
    except SystemExit as exc:
        log.error(str(exc))
        rc = 2
    except Exception as exc:  # noqa: BLE001 - the audit log must record any failure
        log.error(f"FAILED: {exc!r}")
        rc = 1
    log.close(rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
