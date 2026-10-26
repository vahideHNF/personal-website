#!/usr/bin/env python3
"""Check a portfolio site before it goes live.

    python check_site.py SITE_DIR

ERRORS break the site or leak template text: leftover {{placeholders}}, broken
internal links or anchors, case studies with no card, cards with no page,
images without alt text. WARNINGS are craft issues worth a look: story length,
question titles, NDA notes that don't match, stale CSS versions, filler words,
hyphens used as minus signs. Exit code 1 when there are errors. Stdlib only.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
FILLER = ["leverage", "leveraged", "utilize", "utilized", "synergy", "robust", "seamless", "seamlessly",
          "delve", "cutting-edge", "game-changer", "passionate about", "best-in-class", "world-class",
          "spearheaded", "holistic"]
RTL_LANGS = {"ar", "fa", "he", "ur", "ps", "ku", "yi"}


class Node:
    def __init__(self, tag, attrs, parent=None, line=0):
        self.tag, self.attrs, self.parent, self.line = tag, dict(attrs), parent, line
        self.children, self.text = [], []

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.walk()

    def find_all(self, tag=None, cls=None):
        return [n for n in self.walk() if (tag is None or n.tag == tag) and (cls is None or cls in n.classes)]

    def find(self, tag=None, cls=None):
        found = self.find_all(tag, cls)
        return found[0] if found else None

    def get_text(self):
        out = []
        for c in self.children:
            if isinstance(c, Node):
                if c.tag not in ("script", "style"):
                    out.append(c.get_text())
            else:
                out.append(c)
        return re.sub(r"\s+", " ", "".join(out)).strip()


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [])
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur, self.getpos()[0])
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur, self.getpos()[0]))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(path):
    b = Builder()
    b.feed(path.read_text(encoding="utf-8"))
    return b.root


class Report:
    def __init__(self, site):
        self.site, self.errors, self.warnings = site, [], []

    def rel(self, p):
        try:
            return str(p.relative_to(self.site))
        except ValueError:
            return str(p)

    def err(self, p, msg, line=None):
        self.errors.append(f"{self.rel(p)}{':' + str(line) if line else ''}  {msg}")

    def warn(self, p, msg, line=None):
        self.warnings.append(f"{self.rel(p)}{':' + str(line) if line else ''}  {msg}")


def ids_in(doc):
    return {n.attrs["id"] for n in doc.walk() if n.attrs.get("id")}


def is_local(url):
    return url and not re.match(r"^(https?:|mailto:|tel:|javascript:|data:|//)", url)


def check_links(page, doc, docs, r):
    for n in doc.walk():
        for attr in ("href", "src"):
            url = n.attrs.get(attr)
            if not url or not is_local(url) or "{{" in url:
                continue
            if n.tag == "link" and n.attrs.get("rel") in ("preconnect", "dns-prefetch"):
                continue
            parts = urlsplit(url)
            target = page if not parts.path else (page.parent / unquote(parts.path)).resolve()
            if parts.path and not target.exists():
                r.err(page, f'broken link: {attr}="{url}"', n.line)
                continue
            if parts.fragment and target.suffix == ".html":
                tdoc = docs.get(target)
                if tdoc is not None and parts.fragment not in ids_in(tdoc) and parts.fragment != "top":
                    r.err(page, f'link to a missing anchor: "{url}"', n.line)


def check_common(page, doc, raw, r):
    for m in re.finditer(r"\{\{[^}]*\}\}?", raw):
        line = raw.count("\n", 0, m.start()) + 1
        r.err(page, f"leftover placeholder: {m.group(0)[:70]}", line)
    html = doc.find("html")
    if html is None or not html.attrs.get("lang"):
        r.err(page, 'missing <html lang="…">')
    elif html.attrs["lang"].split("-")[0] in RTL_LANGS and html.attrs.get("dir") != "rtl":
        r.warn(page, 'right-to-left language without dir="rtl" on <html>')
    title = doc.find("title")
    if title is None or not title.get_text():
        r.err(page, "missing <title>")
    desc = next((n for n in doc.find_all("meta") if n.attrs.get("name") == "description"), None)
    if desc is None or not desc.attrs.get("content"):
        r.warn(page, "missing meta description (used by search engines and link previews)")
    elif not 50 <= len(desc.attrs["content"]) <= 170:
        r.warn(page, f"meta description is {len(desc.attrs['content'])} characters; aim for 120-160")
    for img in doc.find_all("img"):
        if "alt" not in img.attrs:
            r.err(page, f'<img src="{img.attrs.get("src")}"> has no alt (use alt="" if decorative)', img.line)
        src = img.attrs.get("src", "")
        if is_local(src):
            f = (page.parent / unquote(urlsplit(src).path))
            if f.exists() and f.stat().st_size > 600_000:
                r.warn(page, f"{src} is {f.stat().st_size // 1000} KB; compress it below ~300 KB", img.line)
    for n in doc.walk():
        if n.attrs.get("role") == "img" and not n.attrs.get("aria-label"):
            r.err(page, f'<{n.tag} role="img"> needs an aria-label describing what it shows', n.line)
    if "<!-- OPTIONAL" in raw:
        r.warn(page, "an OPTIONAL template block is still in the file (fill it in or delete it)")
    body = doc.find("body")
    text = body.get_text() if body else ""
    for word in FILLER:
        if re.search(rf"\b{re.escape(word)}\b", text, re.I):
            r.warn(page, f'filler word "{word}": say what actually happened instead')
    for m in re.finditer(r"(?<![\w.])-(\d+(?:[.,]\d+)?\s?(?:%|pp|×|x\b|s\b|min))", text):
        r.warn(page, f'"-{m.group(1)}" uses a hyphen; use the minus sign "−{m.group(1)}"')
        break


def check_bars(page, doc, r):
    for n in doc.walk():
        style = n.attrs.get("style") or ""
        m = re.search(r"width:\s*([\d.]+)%", style)
        if m and "b" in n.classes and float(m.group(1)) > 100:
            r.err(page, f"bar wider than 100% ({m.group(1)}%)", n.line)
        if m and n.tag == "i" and n.parent is not None and "div-track" in n.parent.classes and float(m.group(1)) > 50:
            r.err(page, f"diverging bar wider than its half (max 50%, got {m.group(1)}%)", n.line)
        p = re.search(r"--p:\s*([\d.]+)", style)
        if p and not 0 <= float(p.group(1)) <= 100:
            r.err(page, f"ring --p must be 0-100, got {p.group(1)}", n.line)
    for row in doc.find_all(cls="row") + doc.find_all(cls="div-row"):
        if row.find(cls="v") is None:
            r.warn(page, "a chart row has no printed value (.v); values must be readable without colour", row.line)


def check_case(page, doc, raw, r):
    if len(doc.find_all("h1")) != 1:
        r.err(page, "a case study needs exactly one <h1> (its question)")
    h1 = doc.find("h1")
    if h1 is not None and not h1.get_text().endswith("?"):
        r.warn(page, f'title is not a question: "{h1.get_text()}"')
    tldr = doc.find(cls="tldr")
    if tldr is None:
        r.err(page, 'missing the "In short" block (.tldr)')
    else:
        labels = [s.get_text().lower() for s in tldr.find_all("span")]
        for want in ("problem", "insight", "impact"):
            if want not in labels:
                r.warn(page, f'"In short" has no {want.title()} row')
    steps = doc.find_all("li", "step")
    if not 4 <= len(steps) <= 10:
        r.warn(page, f"the story has {len(steps)} steps; 5-9 reads best")
    for i, step in enumerate(steps, 1):
        dot = step.find(cls="dot")
        if dot is None or dot.get_text() != str(i):
            r.warn(page, f"step {i}: its dot should read {i}", step.line)
        if step.find(cls="when") is None or step.find("h2") is None:
            r.warn(page, f'step {i}: needs a .when label and an <h2> finding', step.line)
        if step.find(cls="vis") is None:
            r.warn(page, f"step {i}: no visual (.vis); every step should show, not only tell", step.line)
        words = sum(len(p.get_text().split()) for p in step.children if isinstance(p, Node) and p.tag == "p")
        if words > 45:
            r.warn(page, f"step {i}: {words} words of text; keep it under ~40 and let the visual talk", step.line)
    marks = len(doc.find_all("mark"))
    if marks > 3:
        r.warn(page, f"{marks} <mark> highlights; keep 1-2 so the key insight stands out")
    if doc.find(cls="next") is None:
        r.warn(page, "no previous/next navigation at the bottom")
    if doc.find(cls="next-list") is None:
        r.warn(page, 'no "Recommendations / In one glance" list')


def check_home(page, doc, r):
    cards = doc.find_all("a", "feat")
    if not cards:
        r.err(page, "no case-study cards (a.feat) on the home page")
    elif not 2 <= len(cards) <= 6:
        r.warn(page, f"{len(cards)} case-study cards; 3-4 strong ones beat many weak ones")
    for c in cards:
        h = c.find("h3") or c.find("h4")
        if h is not None and not h.get_text().endswith("?"):
            r.warn(page, f'card title is not a question: "{h.get_text()}"', c.line)
        if c.find(cls="feat-num") is None:
            r.warn(page, "card without a headline number (.feat-num)", c.line)
    if doc.find("h1") is None:
        r.err(page, "home page has no <h1>")
    og = {n.attrs.get("property"): n.attrs.get("content", "") for n in doc.find_all("meta") if n.attrs.get("property")}
    if not og.get("og:url", "").startswith("https://"):
        r.warn(page, "og:url should be the live https:// address (for LinkedIn and Slack previews)")


def check_resume(page, doc, r):
    sheet = doc.find(cls="sheet") or doc
    heads = [h.get_text().lower() for h in sheet.find_all("h2")]
    for want in ("experience", "education", "skills"):
        if not any(want in h for h in heads):
            r.warn(page, f'no "{want.title()}" section; ATS systems look for standard headings')
    if sheet.find("table") is not None:
        r.warn(page, "a <table> in the resume; many ATS parsers scramble tables")
    if sheet.find("img") is not None:
        r.warn(page, "an image inside the resume sheet; ATS cannot read it")
    if not any("mailto:" in (a.attrs.get("href") or "") for a in sheet.find_all("a")):
        r.warn(page, "no email link in the resume header")
    bullets = [li.get_text() for li in sheet.find_all("li") if li.parent is not None and li.parent.parent is not None
               and "entry" in li.parent.parent.classes]
    if bullets and sum(bool(re.search(r"\d", b)) for b in bullets) < len(bullets) / 2:
        r.warn(page, "fewer than half the experience bullets have a number; add scale or results where true")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    site = Path(sys.argv[1]).resolve()
    r = Report(site)
    pages = sorted(site.rglob("*.html"))
    # Skip hidden folders (.git, .claude), dependencies and git-ignored drafts.
    pages = [p for p in pages
             if not any(part.startswith(".") or part in ("node_modules", "private")
                        for part in p.relative_to(site).parts[:-1])]
    if not (site / "index.html").exists():
        sys.exit(f"{site} has no index.html")
    raws = {p: p.read_text(encoding="utf-8") for p in pages}
    docs = {p.resolve(): parse(p) for p in pages}

    for md in sorted(site.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        for m in re.finditer(r"\{\{[^}]*\}\}?", text):
            r.err(md, f"leftover placeholder: {m.group(0)[:70]}", text.count("\n", 0, m.start()) + 1)
    for p in pages:
        doc = docs[p.resolve()]
        check_common(p, doc, raws[p], r)
        check_links(p, doc, docs, r)
        check_bars(p, doc, r)
    home = site / "index.html"
    check_home(home, docs[home.resolve()], r)
    if (site / "resume.html").exists():
        check_resume(site / "resume.html", docs[(site / "resume.html").resolve()], r)
    else:
        r.err(home, "resume.html is missing")

    cases = [p for p in pages if p.parent.name == "case-studies"]
    for p in cases:
        check_case(p, docs[p.resolve()], raws[p], r)

    # Cards and pages match one to one
    card_targets = set()
    for a in docs[home.resolve()].find_all("a", "feat"):
        href = urlsplit(a.attrs.get("href", "")).path
        if href:
            card_targets.add((home.parent / href).resolve())
    for p in cases:
        if p.resolve() not in card_targets:
            r.err(p, "this case study has no card on the home page")

    # NDA notes agree
    nda_pages = [p for p in cases if docs[p.resolve()].find(cls="nda") is not None]
    home_note = docs[home.resolve()].find(cls="feat-note")
    if nda_pages and home_note is None:
        r.warn(home, "some case studies use illustrative numbers but the home page has no note saying so")
    if not nda_pages and home_note is not None and "illustrative" in home_note.get_text().lower():
        r.warn(home, "the home page says numbers are illustrative, but no case study has an NDA note")

    # Every page loads the same stylesheet versions and fonts
    versions, fonts = {}, {}
    for p in pages:
        for m in re.finditer(r'href="([^"]*?([\w-]+\.css))\?v=([^"]+)"', raws[p]):
            versions.setdefault(m.group(2), {}).setdefault(m.group(3), []).append(r.rel(p))
        for m in re.finditer(r'href="https://fonts\.googleapis\.com/css2\?([^"]+)"', raws[p]):
            fonts.setdefault(m.group(1), []).append(r.rel(p))
        for m in re.finditer(r'href="(?!https?:)[^"]+\.css"', raws[p]):
            r.warn(p, f"{m.group(0)} has no ?v= version; browsers may keep a stale copy")
    for css, by_version in versions.items():
        if len(by_version) > 1:
            detail = "; ".join(f"v={v} in {', '.join(ps)}" for v, ps in by_version.items())
            r.warn(home, f"{css} is linked with different versions ({detail}); run theme.py SITE --refresh")
    if len(fonts) > 1:
        r.warn(home, "pages load different Google Fonts; run theme.py SITE --refresh so they match")
    if not (site / ".nojekyll").exists():
        r.warn(home, "no .nojekyll file; GitHub Pages may skip some files")

    for kind, items in (("ERRORS", r.errors), ("WARNINGS", r.warnings)):
        if items:
            print(f"{kind} ({len(items)})")
            for i in items:
                print("  " + i)
    print(f"\nChecked {len(pages)} pages ({len(cases)} case studies): "
          f"{len(r.errors)} errors, {len(r.warnings)} warnings.")
    sys.exit(1 if r.errors else 0)


if __name__ == "__main__":
    main()
