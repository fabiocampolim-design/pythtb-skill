# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Execute one or both notebooks top-to-bottom and tally their inline checks.

This is the project's real regression suite: every physics claim in the
notebooks prints ``[PASS]``/``[FAIL]``; this script runs the notebook with
nbconvert on the pinned kernel, stores the outputs (in place by default) and
counts PASS / FAIL / error outputs. Exit code is non-zero if any FAIL, any
error output, or an nbconvert failure occurred.

Usage:
    python build/execute.py                        # both notebooks, in place
    python build/execute.py --which main
    python build/execute.py --outdir out/          # keep the repo copies untouched
    python build/execute.py --tally-only           # just count what is already stored
    python build/execute.py --kernel pythtb-mc --timeout 900 -v

Audit log: ``<log-dir>/execute.log`` (default ``<outdir>/logs``); nbconvert's own
output goes to ``<log-dir>/nbconvert-<notebook>.log``.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from buildlog import AuditLog  # noqa: E402

NOTEBOOKS = {
    "main": "PythTB_Theory_and_Practice.ipynb",
    "exercises": "PythTB_Exercises_Solutions.ipynb",
}


def tally(path):
    """Count PASS/FAIL markers, error outputs, figures and captions in a notebook."""
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)
    t = {"cells": len(nb["cells"]), "code": 0, "pass": 0, "fail": 0,
         "errors": 0, "figures": 0, "captions": 0, "unexecuted": 0, "fail_labels": []}
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        t["code"] += 1
        outs = c.get("outputs", [])
        if not outs and "".join(c["source"]).strip():
            t["unexecuted"] += 1
        for o in outs:
            if o.get("output_type") == "error":
                t["errors"] += 1
            text = "".join(o.get("text", [])) if isinstance(o.get("text"), list) else o.get("text", "")
            t["pass"] += text.count("[PASS]")
            t["fail"] += text.count("[FAIL]")
            t["fail_labels"] += [ln for ln in text.splitlines() if "[FAIL]" in ln]
            data = o.get("data", {})
            if "image/png" in data:
                t["figures"] += 1
            html = "".join(data.get("text/html", [])) if "text/html" in data else ""
            if "<b>Figure" in html:
                t["captions"] += 1
    return t


def run_nbconvert(src, dst, kernel, timeout, log_dir):
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copyfile(src, dst)
    cmd = [sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute",
           "--inplace", dst, f"--ExecutePreprocessor.kernel_name={kernel}",
           f"--ExecutePreprocessor.timeout={timeout}"]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    logfile = os.path.join(log_dir, f"nbconvert-{os.path.basename(dst)}.log")
    with open(logfile, "w", encoding="utf-8") as lf:
        proc = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(dst)) or ".",
                              stdout=lf, stderr=subprocess.STDOUT, env=env)
    return proc.returncode, logfile


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--which", choices=["main", "exercises", "all"], default="all")
    ap.add_argument("--indir", default=ROOT, help="where the source notebooks are (default: repo root)")
    ap.add_argument("--outdir", default=None,
                    help="write executed copies here instead of in place")
    ap.add_argument("--log-dir", default=None, help="default: <outdir or indir>/logs")
    ap.add_argument("--kernel", default="pythtb-mc")
    ap.add_argument("--timeout", type=int, default=900, help="per-cell timeout in seconds")
    ap.add_argument("--tally-only", action="store_true",
                    help="do not execute; only count what the notebook files already contain")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("-v", "--verbose", action="store_true")
    g.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args(argv)

    outdir = args.outdir or args.indir
    os.makedirs(outdir, exist_ok=True)
    log_dir = args.log_dir or os.path.join(outdir, "logs")
    log = AuditLog("execute", outdir, log_dir, verbose=args.verbose, quiet=args.quiet)
    which = list(NOTEBOOKS) if args.which == "all" else [args.which]
    rc = 0
    for key in which:
        src = os.path.join(args.indir, NOTEBOOKS[key])
        dst = os.path.join(outdir, NOTEBOOKS[key])
        if not os.path.exists(src):
            log.error(f"missing {src}")
            rc = 1
            continue
        if not args.tally_only:
            t0 = time.time()
            code, logfile = run_nbconvert(src, dst, args.kernel, args.timeout, log_dir)
            log.info(f"{NOTEBOOKS[key]}: nbconvert rc={code} in {time.time() - t0:.0f}s "
                     f"(log: {logfile})")
            if code != 0:
                rc = 1
        t = tally(dst)
        line = (f"{NOTEBOOKS[key]}: {t['cells']} cells ({t['code']} code) | "
                f"PASS {t['pass']} FAIL {t['fail']} errors {t['errors']} | "
                f"figures {t['figures']} captions {t['captions']} | "
                f"unexecuted code cells {t['unexecuted']}")
        log.info(line)
        for lbl in t["fail_labels"]:
            log.warn(lbl)
        if t["fail"] or t["errors"] or t["unexecuted"]:
            rc = 1
    log.info("RESULT: " + ("OK" if rc == 0 else "PROBLEMS — see above"))
    log.close(rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
