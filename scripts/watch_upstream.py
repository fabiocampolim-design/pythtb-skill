# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Weekly upstream watch for PythTB (playbook S8 / rule 23).

Watches github.com/pythtb/pythtb (releases, issues, pull requests, the head of
the default branch) and pypi.org/project/pythtb (published versions), anonymously.

--snapshot   dump the current upstream state (JSON) to --state-dir
--weekly     compare with the previous snapshot, write <outdir>/YYYY-WW.md, then snapshot
--pull       git pull --ff-only every clone under --upstream-dir and log what moved
             (a directory without .git is reported as a snapshot and left alone)

Usage:
    python scripts/watch_upstream.py --weekly --pull
    python scripts/watch_upstream.py --snapshot --state-dir forum/github

Requests are anonymous (60/h GitHub quota; a run needs about five), one page per
second, with a descriptive User-Agent. Every run writes one audit log under
<state-dir>/logs/. Exit 0 ok, 1 upstream unreachable, 2 usage error.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pythtb_tools  # noqa: E402

REPO = "pythtb/pythtb"
API = "https://api.github.com/repos/" + REPO
PYPI = "https://pypi.org/pypi/pythtb/json"
USER_AGENT = "pythtb-skill watch (study project; github.com/pythtb/pythtb reader)"
# paginated list endpoints; the delta key is "number" for issues/pulls, "tag_name" otherwise
ENDPOINTS = {"releases": "/releases",
             "issues": "/issues?state=all&sort=updated&direction=desc",
             "pulls": "/pulls?state=all&sort=updated&direction=desc"}
STUDY_ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
_LINK_NEXT = re.compile(r'<([^>]+)>;\s*rel="next"')


def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8")), dict(r.headers)


def next_link(headers):
    """URL of the next page from a GitHub ``Link`` header, or None."""
    link = headers.get("Link") or headers.get("link") or ""
    m = _LINK_NEXT.search(link)
    return m.group(1) if m else None


def fetch_all(url, max_pages=50, pause=1.0):
    """Follow rel="next" through a paginated GitHub list endpoint."""
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}per_page=100"
    items, page = [], 0
    while url and page < max_pages:
        batch, headers = _get(url)
        items.extend(batch)
        url = next_link(headers)
        page += 1
        if url:
            time.sleep(pause)
    return items


def drop_pull_requests(issues):
    """GitHub's /issues lists pull requests too; keep only real issues."""
    return [x for x in issues if "pull_request" not in x]


def pypi_releases(data):
    """PyPI JSON -> [{tag_name, released_at}] sorted by upload time."""
    out = []
    for ver, files in data.get("releases", {}).items():
        when = min((f.get("upload_time_iso_8601", "") for f in files), default="")
        out.append({"tag_name": ver, "released_at": when})
    return sorted(out, key=lambda x: x["released_at"])


def _key(x, key):
    return x.get(key, x.get("tag_name"))


def delta(old, new, key="number"):
    """Split `new` into new / updated / closed relative to `old` (by number or tag_name)."""
    o = {_key(x, key): x for x in old}
    out = {"new": [], "updated": [], "closed": []}
    for x in new:
        k = _key(x, key)
        if k not in o:
            out["new"].append(x)
        elif x.get("state") == "closed" and o[k].get("state") != "closed":
            out["closed"].append(x)
        elif x.get("updated_at") != o[k].get("updated_at"):
            out["updated"].append(x)
    return out


def render_weekly(deltas, week, head_before=None, head_after=None):
    lines = [f"# Upstream watch {week}", "",
             f"Source: https://github.com/{REPO} and https://pypi.org/project/pythtb/", ""]
    if head_after:
        sha_b = (head_before or {}).get("sha", "")[:7] or "?"
        sha_a = head_after.get("sha", "")[:7]
        moved = "moved" if sha_b != sha_a else "unchanged"
        lines += [f"## default branch: {moved} ({sha_b} → {sha_a}, {head_after.get('date', '')[:10]})", ""]
    for name, d in deltas.items():
        lines.append(f"## {name}: {len(d['new'])} new, {len(d['updated'])} updated, {len(d['closed'])} closed")
        for bucket in ("new", "updated", "closed"):
            for x in d[bucket]:
                if "tag_name" in x:
                    lines.append(f"- [{bucket}] {x['tag_name']} ({x.get('released_at', x.get('published_at', ''))[:10]})")
                else:
                    lines.append(f"- [{bucket}] #{x['number']} {x.get('title', '')} — {x.get('html_url', '')}")
        lines.append("")
    return "\n".join(lines)


def fetch_head():
    """{sha, date} of the default branch."""
    repo, _ = _get(API)
    branch, _ = _get(f"{API}/branches/{repo.get('default_branch', 'main')}")
    commit = branch.get("commit", {})
    date = commit.get("commit", {}).get("committer", {}).get("date", "")
    return {"sha": commit.get("sha", ""), "date": date, "branch": repo.get("default_branch", "main")}


def snapshot(state_dir):
    """Fetch everything and write one JSON file per feed; return the data."""
    os.makedirs(state_dir, exist_ok=True)
    data = {}
    for name, ep in ENDPOINTS.items():
        items = fetch_all(API + ep)
        data[name] = drop_pull_requests(items) if name == "issues" else items
    data["pypi"] = pypi_releases(_get(PYPI)[0])
    data["head"] = fetch_head()
    for name, payload in data.items():
        with open(os.path.join(state_dir, f"{name}.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f)
    return data


def load_previous(state_dir):
    prev = {}
    for name in list(ENDPOINTS) + ["pypi", "head"]:
        p = os.path.join(state_dir, f"{name}.json")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                prev[name] = json.load(f)
        else:
            prev[name] = {} if name == "head" else []
    return prev


def pull_all(upstream_dir):
    """git pull --ff-only in every clone; return [(name, before, after)].

    A directory without .git (a source snapshot such as mirror/pythtb-repo) is
    listed as ("<name>", "snapshot", "snapshot") and not touched."""
    moved = []
    if not os.path.isdir(upstream_dir):
        return moved
    for d in sorted(os.listdir(upstream_dir)):
        p = os.path.join(upstream_dir, d)
        if not os.path.isdir(p):
            continue
        if not os.path.isdir(os.path.join(p, ".git")):
            moved.append((d, "snapshot", "snapshot"))
            continue
        before = subprocess.run(["git", "rev-parse", "HEAD"], cwd=p, capture_output=True, text=True).stdout.strip()
        subprocess.run(["git", "pull", "--ff-only", "-q"], cwd=p, capture_output=True, text=True)
        after = subprocess.run(["git", "rev-parse", "HEAD"], cwd=p, capture_output=True, text=True).stdout.strip()
        moved.append((d, before[:7], after[:7]))
    return moved


def build_parser():
    ap = argparse.ArgumentParser(prog="watch_upstream", description=__doc__.splitlines()[0])
    ap.add_argument("--snapshot", action="store_true", help="dump the current upstream state")
    ap.add_argument("--weekly", action="store_true", help="delta vs previous snapshot, then snapshot")
    ap.add_argument("--pull", action="store_true", help="git pull every clone under --upstream-dir")
    ap.add_argument("--state-dir", default=os.path.join(STUDY_ROOT, "forum", "github"),
                    help="where snapshots and logs live (default <study>/forum/github)")
    ap.add_argument("--upstream-dir", default=os.path.join(STUDY_ROOT, "mirror"),
                    help="directory of upstream clones/snapshots (default <study>/mirror)")
    ap.add_argument("--outdir", default=os.path.join(STUDY_ROOT, "docs", "watch"),
                    help="where weekly reports go (default <study>/docs/watch)")
    ap.add_argument("--log-dir", default=None,
                    help="audit-log directory (default <state-dir>/logs)")
    ap.add_argument("-q", "--quiet", action="store_true", help="no console output")
    ap.add_argument("--version", action="version", version=f"pythtb-skill {pythtb_tools.__version__}")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    week = datetime.date.today().strftime("%G-W%V")
    extra = {}
    log_root = os.path.dirname(args.log_dir) if args.log_dir else args.state_dir
    try:
        if args.weekly:
            prev = load_previous(args.state_dir)
            new = snapshot(args.state_dir)
            deltas = {n: delta(prev[n], new[n]) for n in ENDPOINTS}
            deltas["pypi"] = delta(prev["pypi"], new["pypi"], key="tag_name")
            md = render_weekly(deltas, week, prev.get("head"), new["head"])
            if args.pull:
                md += "\n## clones\n" + "\n".join(f"- {d}: {b} → {a}" for d, b, a in pull_all(args.upstream_dir)) + "\n"
            os.makedirs(args.outdir, exist_ok=True)
            with open(os.path.join(args.outdir, f"{week}.md"), "w", encoding="utf-8") as f:
                f.write(md)
            extra["written"] = f"{week}.md"
            extra["counts"] = {n: len(new[n]) for n in list(ENDPOINTS) + ["pypi"]}
            extra["head"] = new["head"].get("sha", "")[:7]
        elif args.snapshot:
            data = snapshot(args.state_dir)
            extra["snapshot"] = args.state_dir
            extra["counts"] = {n: len(data[n]) for n in list(ENDPOINTS) + ["pypi"]}
        elif args.pull:
            extra["moved"] = pull_all(args.upstream_dir)
        else:
            build_parser().print_help()
            return 2
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        extra["error"] = str(exc)
        pythtb_tools.audit_log(log_root, argv if argv is not None else sys.argv[1:], extra, script="watch_upstream")
        print(f"watch_upstream: upstream unreachable: {exc}", file=sys.stderr)
        return 1
    # audit logs live with the snapshots (gitignored), not among the weekly reports
    pythtb_tools.audit_log(log_root, argv if argv is not None else sys.argv[1:], extra, script="watch_upstream")
    if not args.quiet:
        print("watch_upstream:", json.dumps(extra, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
