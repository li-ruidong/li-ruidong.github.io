"""Synchronize the shared header/profile into seven static pages.

Edit includes/header.html or includes/profile.html, then run:
    python tools/sync_shared.py
Use --check for a non-mutating consistency check. No third-party dependencies.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = {"index.html": "/", **{
    f"{name}/index.html": f"/{name}/" for name in
    ("news", "cv", "research", "activities", "publications", "teaching")
}}

def fragment(name: str, route: str) -> str:
    text = (ROOT / "includes" / f"{name}.html").read_text(encoding="utf-8")
    if name == "header":
        def mark_nav(match: re.Match[str]) -> str:
            nav = match.group(0)
            def mark_anchor(anchor: re.Match[str]) -> str:
                tag = anchor.group(0)
                if anchor.group(1) == route:
                    tag = tag[:-1] + ' class="active" aria-current="page">'
                return tag
            return re.sub(r'<a\b[^>]*href="([^"]+)"[^>]*>', mark_anchor, nav)
        text = re.sub(r'<nav\b[^>]*>.*?</nav>', mark_nav, text, flags=re.S)
    text = text.replace("viewbox=", "viewBox=").strip()
    return text.encode("ascii", "xmlcharrefreplace").decode("ascii")

def expected_html(path: Path, route: str) -> str:
    text = path.read_text(encoding="utf-8")
    for name, tag, element_id in (
        ("header", "header", "site-header"), ("profile", "aside", "profile-panel")
    ):
        pattern = rf'(<{tag}\b[^>]*id="{element_id}"[^>]*>).*?(</{tag}>)'
        block = fragment(name, route)
        text, count = re.subn(pattern, lambda m: m[1]+"\n"+block+"\n"+m[2], text, flags=re.S)
        if count != 1:
            raise ValueError(f"{path}: expected one #{element_id}, found {count}")
    return text

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = []
    for name, route in PAGES.items():
        path = ROOT / name
        expected = expected_html(path, route)
        if path.read_text(encoding="utf-8") != expected:
            changed.append(name)
            if not args.check:
                path.write_text(expected, encoding="utf-8")
    if args.check and changed:
        raise SystemExit("Shared fragments differ in: " + ", ".join(changed))
    print(f"Seven-page shared shell: {'OK' if args.check else f'{len(changed)} pages synchronized' }.")

if __name__ == "__main__":
    main()
