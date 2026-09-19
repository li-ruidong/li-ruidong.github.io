"""Dependency-free checks for the seven-page static site.
Run: python tools/check_site.py
Layout/interaction measurements from the delivered browser run are in
    docs/browser-validation.json
"""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT/'index.html']+[ROOT/name/'index.html' for name in
    ('news','cv','research','activities','publications','teaching')]

class Page(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[str] = []
        self.anchors: list[tuple[str,str]] = []
        self.current_anchor: tuple[str,list[str]] | None = None
        self.charset = ''
        self.css: list[str] = []
        self.js: list[str] = []
        self.inline_style = False
        self.feed(source)
    def handle_starttag(self, tag: str, attrs: list[tuple[str,str|None]]) -> None:
        a = dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        for key in ('href','src'):
            if a.get(key): self.references.append(a[key])
        if tag=='meta' and a.get('charset'): self.charset=a['charset']
        if tag=='link' and a.get('rel')=='stylesheet': self.css.append(a.get('href',''))
        if tag=='script' and a.get('src'): self.js.append(a['src'])
        if tag=='font' or 'style' in a: self.inline_style=True
        if tag=='a': self.current_anchor=(a.get('href',''),[])
    def handle_startendtag(self, tag: str, attrs: list[tuple[str,str|None]]) -> None:
        self.handle_starttag(tag,attrs)
    def handle_data(self, data: str) -> None:
        if self.current_anchor: self.current_anchor[1].append(data)
    def handle_endtag(self, tag: str) -> None:
        if tag=='a' and self.current_anchor:
            href, parts = self.current_anchor
            self.anchors.append((href,''.join(parts).strip()))
            self.current_anchor=None

def check() -> list[str]:
    errors=[]
    pages={p:Page(p.read_text(encoding='utf-8')) for p in PAGES}
    css_versions=set();js_versions=set()
    for p, data in pages.items():
        label=str(p.relative_to(ROOT));source=p.read_text(encoding='utf-8')
        if data.charset.lower()!='utf-8': errors.append(f'{label}: missing UTF-8 declaration')
        if '\ufffd' in source: errors.append(f'{label}: replacement character found')
        if data.inline_style: errors.append(f'{label}: local font/inline style override')
        if len(data.css)!=1 or len(data.js)!=1:errors.append(f'{label}: expected one shared CSS and JS')
        css_versions.update(data.css);js_versions.update(data.js)
        if 'site-header' not in data.ids or 'profile-panel' not in data.ids:errors.append(f'{label}: missing shared shell')
        for href,text in data.anchors:
            if re.search(r'\b(university|college|polytechnic|institute of technology)\b',text,re.I):
                errors.append(f'{label}: school-name hyperlink: {text}')
        for ref in data.references:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            if not u.path: target=p
            elif u.path.startswith('/'): target=ROOT/unquote(u.path).lstrip('/')
            else: target=p.parent/unquote(u.path)
            target=target.resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f'{label}: local reference outside site: {ref}');continue
            if target.is_dir():target=target/'index.html'
            if not target.exists():errors.append(f'{label}: missing {ref}');continue
            if u.fragment and target.suffix=='.html':
                parsed=pages.get(target) or Page(target.read_text(encoding='utf-8'))
                if u.fragment not in parsed.ids:errors.append(f'{label}: missing anchor {ref}')
    if len(css_versions)!=1 or len(js_versions)!=1:errors.append('Seven pages do not share the same CSS/JS version')
    css=(ROOT/'assets/css/academic-site.css').read_text(encoding='utf-8')
    if '@import' in css or '@font-face' in css:errors.append('Unexpected remote or embedded font dependency')
    return errors

if __name__=='__main__':
    issues=check()
    if issues:
        print('\n'.join(issues),file=sys.stderr);raise SystemExit(1)
    print('PASS: seven pages; encoding; shared assets; school-name links; local files and anchors.')
