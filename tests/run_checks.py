#!/usr/bin/env python3
"""NexusKit mechanical checks. Run from repo root: python tests/run_checks.py

Five checks, each maps to a class of failure that actually happened:
1. link-integrity   - relative markdown links must resolve
2. references       - nk-* mentions resolve to real skills; no dangling K/R code refs
3. byte-budget      - SKILL.md <= 8000 bytes (Codex injection limit), ratchet list
4. prompt-copies    - duplicated subagent prompts match tests/prompt-copies.txt and
                      carry the nk-copy declaration header
5. frontmatter      - SKILL.md frontmatter parses under strict YAML, has name and
                      description, and name matches its directory (installers such
                      as the skills CLI derive the install dir from frontmatter name)
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SKILL_REF_DENYLIST = {"nk-section"}  # semantic marker, not a skill
BYTE_LIMIT = 8000
OVER_BUDGET: set = set()  # ratchet: may only shrink; a listed file under budget fails the check

failures = []


def check(name, problems):
    if problems:
        failures.append((name, problems))
        print(f"FAIL {name}: {len(problems)} problem(s)")
        for p in problems[:20]:
            print(f"  - {p}")
    else:
        print(f"OK   {name}")


def md_files():
    return [
        f.replace(os.sep, "/")
        for f in glob.glob("**/*.md", recursive=True)
        if not f.startswith(".git")
    ]


def strip_fences(text):
    # fenced blocks, then HTML comments (meta), then inline code (examples/templates)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


# --- 1. link integrity ---
def check_links():
    problems = []
    for f in md_files():
        base = os.path.dirname(f)
        in_skill = f.startswith("skills/nk-")
        text = strip_fences(open(f, encoding="utf-8").read())
        for m in re.finditer(r"\]\(([^)\s#]+)(#[^)]*)?\)", text):
            link = m.group(1)
            if link.startswith(("http", "file:", "mailto:", "#")):
                continue
            if "<" in link or "*" in link:  # template placeholder or glob
                continue
            if in_skill and link.startswith(("docs/", "CONCEPTS", "AGENTS")):
                continue  # target-repo paths, not repo-internal
            if not os.path.exists(os.path.normpath(os.path.join(base, link))):
                problems.append(f"{f} -> {link}")
    check("link-integrity", problems)


# --- 2. reference resolution ---
def check_references():
    problems = []
    skill_dirs = {os.path.basename(d) for d in glob.glob("skills/nk-*") if os.path.isdir(d)}
    for f in md_files():
        if not (f.startswith("skills/nk-") or f.startswith("skills/conventions")):
            continue
        text = strip_fences(open(f, encoding="utf-8").read())
        for m in re.finditer(r"[（(]K[0-9]+[）)]", text):
            problems.append(f"{f}: dangling K-code label {m.group(0)} (contracts live in conventions/)")
        for m in re.finditer(r"\bR[0-9]+\.[0-9]+\b", text):
            problems.append(f"{f}: decimal cadence ref {m.group(0)} does not exist (use e.g. 'R4 第 4 条')")
        if f.startswith("skills/nk-"):
            for m in re.finditer(r"\b(nk-[a-z][a-z0-9-]*)\b", text):
                name = m.group(1)
                if name in SKILL_REF_DENYLIST:
                    continue
                if name not in skill_dirs:
                    problems.append(f"{f}: references skill `{name}` but no {name}/ directory exists")
    check("references", problems)


# --- 3. byte budget ---
def check_byte_budget():
    problems = []
    over_now = set()
    for f in glob.glob("skills/nk-*/SKILL.md"):
        size = os.path.getsize(f)
        if size > BYTE_LIMIT:
            over_now.add(f)
            if f not in OVER_BUDGET:
                problems.append(f"{f}: {size} bytes exceeds {BYTE_LIMIT} (Codex injection limit)")
    for f in OVER_BUDGET - over_now:
        problems.append(f"{f}: now under budget - remove it from OVER_BUDGET (ratchet only shrinks)")
    check("byte-budget", problems)


# --- 4. duplicated prompt copies ---
def check_prompt_copies():
    problems = []
    manifest_path = "tests/prompt-copies.txt"
    manifest = {}
    for line in open(manifest_path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, paths = line.split(":", 1)
        manifest[name.strip()] = [p.strip() for p in paths.split(",")]

    on_disk = {}
    for f in glob.glob("skills/nk-*/references/agents/*.md") + glob.glob("skills/nk-*/references/personas/*.md"):
        on_disk.setdefault(os.path.basename(f), []).append(f.replace(os.sep, "/"))
    on_disk = {k: sorted(v) for k, v in on_disk.items() if len(v) > 1}

    for name, paths in manifest.items():
        for p in paths:
            if not os.path.exists(p):
                problems.append(f"manifest lists missing file {p}")
                continue
            head = open(p, encoding="utf-8").read(200)
            if not head.startswith("<!-- nk-copy:"):
                problems.append(f"{p}: missing nk-copy declaration header")
    for name, paths in on_disk.items():
        if name not in manifest:
            problems.append(f"unregistered duplicated prompt: {name} ({', '.join(paths)})")
        elif sorted(manifest[name]) != paths:
            problems.append(f"{name}: manifest {sorted(manifest[name])} != on-disk {paths}")
    check("prompt-copies", problems)


# --- 5. frontmatter ---
def check_frontmatter():
    problems = []
    for f in sorted(glob.glob("skills/*/SKILL.md")):
        f = f.replace(os.sep, "/")
        text = open(f, encoding="utf-8").read()
        if not text.startswith("---\n"):
            problems.append(f"{f}: missing frontmatter")
            continue
        end = text.find("\n---", 4)
        if end == -1:
            problems.append(f"{f}: unterminated frontmatter")
            continue
        name = desc = None
        for line in text[4:end].splitlines():
            m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
            if not m:
                continue
            key, val = m.group(1), m.group(2)
            if val and not val.startswith(('"', "'")) and ": " in val:
                problems.append(f"{f}: plain scalar containing ': ' breaks strict YAML parsers; quote the value")
            if key == "name":
                name = val.strip("\"'")
            elif key == "description":
                desc = val
        dirname = f.split("/")[1]
        if not name:
            problems.append(f"{f}: frontmatter missing name")
        elif name != dirname:
            problems.append(f"{f}: name '{name}' != directory '{dirname}' (installers derive install dir from frontmatter name)")
        if not desc:
            problems.append(f"{f}: frontmatter missing description")
    check("frontmatter", problems)


if __name__ == "__main__":
    check_links()
    check_references()
    check_byte_budget()
    check_prompt_copies()
    check_frontmatter()
    if failures:
        print(f"\n{sum(len(p) for _, p in failures)} problem(s) in {len(failures)} check(s)")
        sys.exit(1)
    print("\nall checks passed")
