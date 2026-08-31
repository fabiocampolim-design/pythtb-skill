# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""scripts/watch_upstream.py — pure functions, the parser and the scheduler script; no network."""

import os
import shutil
import subprocess
import sys

import pytest

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "scripts"))
import watch_upstream as wu  # noqa: E402


def test_delta_new_updated_closed():
    old = [{"number": 1, "updated_at": "a", "state": "open"}, {"number": 2, "updated_at": "a", "state": "open"}]
    new = [{"number": 1, "updated_at": "b", "state": "open"}, {"number": 2, "updated_at": "a", "state": "closed"},
           {"number": 3, "updated_at": "a", "state": "open"}]
    d = wu.delta(old, new)
    assert [x["number"] for x in d["new"]] == [3]
    assert [x["number"] for x in d["updated"]] == [1]
    assert [x["number"] for x in d["closed"]] == [2]


def test_delta_on_releases_uses_tag_name():
    d = wu.delta([{"tag_name": "v2.0.2"}], [{"tag_name": "v2.0.2"}, {"tag_name": "v2.1.0"}], key="tag_name")
    assert [x["tag_name"] for x in d["new"]] == ["v2.1.0"] and d["updated"] == [] and d["closed"] == []


def test_drop_pull_requests_keeps_only_issues():
    items = [{"number": 1}, {"number": 2, "pull_request": {"url": "u"}}, {"number": 3}]
    assert [x["number"] for x in wu.drop_pull_requests(items)] == [1, 3]


def test_pypi_releases_sorted_by_upload_time():
    data = {"releases": {"2.0.2": [{"upload_time_iso_8601": "2026-03-01T00:00:00Z"}],
                         "1.8.0": [{"upload_time_iso_8601": "2022-01-01T00:00:00Z"},
                                   {"upload_time_iso_8601": "2021-12-31T00:00:00Z"}],
                         "empty": []}}
    rel = wu.pypi_releases(data)
    assert [r["tag_name"] for r in rel] == ["empty", "1.8.0", "2.0.2"]
    assert rel[1]["released_at"].startswith("2021-12-31")


def test_next_link_parses_github_link_header():
    h = {"Link": '<https://api.github.com/x?page=2>; rel="next", <https://api.github.com/x?page=5>; rel="last"'}
    assert wu.next_link(h) == "https://api.github.com/x?page=2"
    assert wu.next_link({"Link": '<https://api.github.com/x?page=1>; rel="prev"'}) is None
    assert wu.next_link({}) is None


def test_render_weekly_mentions_every_bucket_and_head():
    md = wu.render_weekly(
        {"releases": {"new": [{"tag_name": "v2.1.0", "published_at": "2026-09-01T00:00:00Z"}], "updated": [], "closed": []},
         "issues": {"new": [], "updated": [], "closed": []},
         "pulls": {"new": [{"number": 9, "title": "fix", "html_url": "u"}], "updated": [], "closed": []},
         "pypi": {"new": [], "updated": [], "closed": []}},
        "2026-W36", {"sha": "aaaaaaa1"}, {"sha": "bbbbbbb2", "date": "2026-08-30T10:00:00Z"})
    assert md.startswith("# Upstream watch 2026-W36") and "v2.1.0" in md and "#9 fix" in md
    assert "issues: 0 new" in md and "pypi: 0 new" in md
    assert "default branch: moved (aaaaaaa → bbbbbbb, 2026-08-30)" in md


def test_render_weekly_without_head_info():
    md = wu.render_weekly({"issues": {"new": [], "updated": [], "closed": []}}, "2026-W36")
    assert "default branch" not in md and "issues: 0 new, 0 updated, 0 closed" in md


def test_cli_parser_and_no_mode_exit_2():
    ns = wu.build_parser().parse_args(["--weekly", "--state-dir", "s", "--outdir", "o"])
    assert ns.weekly and ns.state_dir == "s" and ns.outdir == "o"
    assert wu.main([]) == 2


def test_pull_all_reports_snapshots_and_skips_missing(tmp_path):
    assert wu.pull_all(str(tmp_path)) == []
    assert wu.pull_all(str(tmp_path / "missing")) == []
    (tmp_path / "pythtb-repo").mkdir()
    (tmp_path / "a-file.txt").write_text("x")
    assert wu.pull_all(str(tmp_path)) == [("pythtb-repo", "snapshot", "snapshot")]


def test_load_previous_on_empty_state_dir(tmp_path):
    prev = wu.load_previous(str(tmp_path))
    assert prev["issues"] == [] and prev["pypi"] == [] and prev["head"] == {}


def test_weekly_unreachable_upstream_exits_1_and_logs(tmp_path, monkeypatch, capsys):
    import urllib.error

    def boom(url, timeout=60):
        raise urllib.error.URLError("offline")
    monkeypatch.setattr(wu, "_get", boom)
    rc = wu.main(["--weekly", "--state-dir", str(tmp_path / "s"), "--outdir", str(tmp_path / "o")])
    assert rc == 1 and "unreachable" in capsys.readouterr().err
    logs = os.listdir(tmp_path / "s" / "logs")
    assert len(logs) == 1 and logs[0].startswith("watch_upstream-")


def test_weekly_offline_end_to_end(tmp_path, monkeypatch):
    """Fake the network once: the report, the snapshot and the audit log all appear."""
    pages = {
        wu.API: ({"default_branch": "main"}, {}),
        wu.API + "/branches/main": ({"commit": {"sha": "c0ffee1234", "commit": {"committer": {"date": "2026-08-30T00:00:00Z"}}}}, {}),
        wu.PYPI: ({"releases": {"2.0.2": [{"upload_time_iso_8601": "2026-03-01T00:00:00Z"}]}}, {}),
    }

    def fake_get(url, timeout=60):
        if url in pages:
            return pages[url]
        if url.startswith(wu.API + "/releases"):
            return [{"tag_name": "v2.0.2", "published_at": "2026-03-01T00:00:00Z"}], {}
        if url.startswith(wu.API + "/issues"):
            return [{"number": 1, "title": "real", "state": "open", "updated_at": "a", "html_url": "u"},
                    {"number": 2, "title": "pr", "state": "open", "updated_at": "a", "pull_request": {}}], {}
        if url.startswith(wu.API + "/pulls"):
            return [{"number": 2, "title": "pr", "state": "open", "updated_at": "a", "html_url": "u"}], {}
        raise AssertionError(url)
    monkeypatch.setattr(wu, "_get", fake_get)
    state, out = tmp_path / "state", tmp_path / "out"
    assert wu.main(["--weekly", "--state-dir", str(state), "--outdir", str(out), "-q"]) == 0
    reports = os.listdir(out)
    assert len(reports) == 1 and reports[0].endswith(".md")
    md = (out / reports[0]).read_text(encoding="utf-8")
    assert "releases: 1 new" in md and "issues: 1 new" in md and "pulls: 1 new" in md and "pypi: 1 new" in md
    assert "default branch: moved (? → c0ffee1" in md
    assert sorted(os.listdir(state)) == ["head.json", "issues.json", "logs", "pulls.json", "pypi.json", "releases.json"]
    # second run: nothing new
    assert wu.main(["--weekly", "--state-dir", str(state), "--outdir", str(out), "-q"]) == 0
    md = (out / reports[0]).read_text(encoding="utf-8")
    assert "issues: 0 new, 0 updated, 0 closed" in md and "default branch: unchanged" in md


def _powershell():
    return shutil.which("powershell") or shutil.which("pwsh")


@pytest.mark.skipif(_powershell() is None, reason="no PowerShell on this host")
def test_register_watch_task_dry_run_and_version():
    path = os.path.join(ROOT, "scripts", "register_watch_task.ps1")
    with open(path, encoding="utf-8") as f:
        assert "SPDX-License-Identifier: Apache-2.0" in f.read(400)
    ps = _powershell()
    r = subprocess.run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path, "-DryRun"],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    assert "DRY-RUN" in r.stdout and "Register-ScheduledTask" in r.stdout and "watch_upstream.py" in r.stdout
    r = subprocess.run([ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path, "-Version"],
                       capture_output=True, text=True, timeout=120)
    with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as f:
        assert r.returncode == 0 and r.stdout.strip() == "pythtb-skill " + f.read().strip()
