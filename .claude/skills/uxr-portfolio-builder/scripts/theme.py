#!/usr/bin/env python3
"""Apply a colour and font theme to a portfolio site.

    python theme.py SITE_DIR [--accent sunflower|#RRGGBB] [--fonts editorial]
    python theme.py SITE_DIR --refresh          # after adding pages or editing CSS: re-apply the
                                                # current fonts to every page and bump ?v= versions
    python theme.py --list                      # show the presets

From ONE accent colour it derives the whole accent family and checks contrast:
  --accent       the colour itself: bars, dots, underlines (decoration only)
  --accent-soft  highlighter behind <mark> and big numbers (dark text stays >= 7:1)
  --accent-tint  pale fills for pills and hovers (body text stays >= 7:1)
  --accent-deep  small text in the accent hue, >= 4.5:1 on white and on the tint
  --on-accent    ink or white, whichever reads better on top of --accent

It rewrites the block between the theme markers in assets/theme.css, swaps the
Google Fonts <link> in every page, and bumps ?v= on local stylesheets so
browsers fetch the new files. Standard library only.
"""
import argparse
import re
import sys
import time
from pathlib import Path

ACCENTS = {
    "sunflower": "#FFC629",  # warm yellow (the original site)
    "coral": "#FF7A59",
    "teal": "#14B8A6",
    "sky": "#38BDF8",
    "violet": "#8061FF",
    "rose": "#F472B6",
    "leaf": "#4CC38A",
    "cobalt": "#2A62F0",
}

# head = headings, body = everything else. Every URL below was checked to load.
FONTS = {
    "editorial": ("'Merriweather', Georgia, serif", "'Open Sans', 'Helvetica Neue', Arial, sans-serif",
                  "family=Merriweather:ital,wght@0,400;0,700;1,400&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400"),
    "modern": ("'Fraunces', Georgia, serif", "'Inter', 'Helvetica Neue', Arial, sans-serif",
               "family=Fraunces:ital,wght@0,600;0,700;1,600&family=Inter:ital,wght@0,400;0,600;0,700;1,400"),
    "classic": ("'Lora', Georgia, serif", "'Source Sans 3', 'Helvetica Neue', Arial, sans-serif",
                "family=Lora:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400"),
    "humanist": ("'Source Serif 4', Georgia, serif", "'Source Sans 3', 'Helvetica Neue', Arial, sans-serif",
                 "family=Source+Serif+4:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400"),
    "geometric": ("'Space Grotesk', 'Helvetica Neue', Arial, sans-serif", "'Inter', 'Helvetica Neue', Arial, sans-serif",
                  "family=Space+Grotesk:wght@500;700&family=Inter:ital,wght@0,400;0,600;0,700;1,400"),
    "persian": ("'Vazirmatn', Tahoma, sans-serif", "'Vazirmatn', Tahoma, sans-serif",
                "family=Vazirmatn:wght@400;600;700"),
}

INK = "#0A0A0A"
TEXT = "#333333"
WHITE = "#FFFFFF"
PAPER = "#FCFCFA"  # background of visual panels in case studies

FONT_LINK_RE = re.compile(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">')
LOCAL_CSS_RE = re.compile(r'(href="(?!https?:)[^"?]+\.css)(\?v=[^"]*)?"')
THEME_BLOCK_RE = re.compile(r"/\* theme:start.*?theme:end \*/", re.S)


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(f"not a hex colour: #{h}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in rgb)


def theme_hex(h):
    return rgb_to_hex(hex_to_rgb(h))


def luminance(h):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(a, b, t):
    """t=0 gives a, t=1 gives b."""
    ra, rb = hex_to_rgb(a), hex_to_rgb(b)
    return rgb_to_hex(tuple(x + (y - x) * t for x, y in zip(ra, rb)))


def derive(accent):
    accent = rgb_to_hex(hex_to_rgb(accent))
    # Text sits on the accent in a few places (step numbers, button hover). If
    # neither ink nor white reads well on it, nudge the accent until one does.
    for _ in range(25):
        if max(contrast(INK, accent), contrast(WHITE, accent)) >= 4.6:
            break
        toward = "#000000" if contrast(WHITE, accent) > contrast(INK, accent) else WHITE
        accent = mix(accent, toward, 0.03)
    t = 0.45
    soft = mix(accent, WHITE, t)
    while contrast(INK, soft) < 7 and t < 0.95:
        t += 0.05
        soft = mix(accent, WHITE, t)
    t = 0.87
    tint = mix(accent, WHITE, t)
    while contrast(TEXT, tint) < 7 and t < 0.98:
        t += 0.01
        tint = mix(accent, WHITE, t)
    # Darken toward black only as far as needed, so the hue stays recognisable.
    t, deep = 0.0, accent
    while min(contrast(deep, WHITE), contrast(deep, tint), contrast(deep, PAPER)) < 4.6 and t < 0.95:
        t += 0.02
        deep = mix(accent, "#000000", t)
    on = INK if contrast(INK, accent) >= contrast(WHITE, accent) else WHITE
    # label -> (ratio, target)
    report = {
        "accent on white (bars and dots)": (contrast(accent, WHITE), 1.4),
        "ink on accent-soft (highlighted text)": (contrast(INK, soft), 7),
        "text on accent-tint (pills)": (contrast(TEXT, tint), 7),
        "accent-deep on white (small labels)": (contrast(deep, WHITE), 4.5),
        "on-accent on accent (button hover, dots)": (contrast(on, accent), 4.5),
    }
    return {"accent": accent, "soft": soft, "tint": tint, "deep": deep, "on": on}, report


def theme_block(p, fonts_key):
    head, body, _ = FONTS[fonts_key]
    return (
        f"/* theme:start fonts={fonts_key} (written by scripts/theme.py; re-run it rather than editing by hand) */\n"
        ":root{\n"
        f"  --accent:{p['accent']}; --accent-soft:{p['soft']}; --accent-tint:{p['tint']};\n"
        f"  --accent-deep:{p['deep']}; --on-accent:{p['on']};\n"
        f"  --head:{head};\n"
        f"  --body:{body};\n"
        "}\n"
        "/* theme:end */"
    )


def font_link(fonts_key):
    return ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
            f'{FONTS[fonts_key][2]}&display=swap">')


def bump_css_versions(site):
    version = time.strftime("%Y%m%d%H%M%S")
    for page in site.rglob("*.html"):
        if any(part.startswith(".") for part in page.relative_to(site).parts[:-1]):
            continue
        src = page.read_text(encoding="utf-8")
        out = LOCAL_CSS_RE.sub(lambda m: f'{m.group(1)}?v={version}"', src)
        if out != src:
            page.write_text(out, encoding="utf-8")
    return version


def sync_fonts(site, fonts_key):
    link = font_link(fonts_key)
    for page in Path(site).rglob("*.html"):
        if any(part.startswith(".") for part in page.relative_to(site).parts[:-1]):
            continue
        text = page.read_text(encoding="utf-8")
        new = FONT_LINK_RE.sub(lambda _: link, text)
        if new != text:
            page.write_text(new, encoding="utf-8")


def current_fonts(site):
    css = Path(site) / "assets" / "theme.css"
    m = re.search(r"theme:start fonts=(\w+)", css.read_text(encoding="utf-8")) if css.exists() else None
    return m.group(1) if m and m.group(1) in FONTS else None


def current_accent(site):
    css = Path(site) / "assets" / "theme.css"
    m = re.search(r"--accent:\s*(#[0-9A-Fa-f]{6})", css.read_text(encoding="utf-8")) if css.exists() else None
    return m.group(1) if m else None


def refresh(site):
    """Make every page match the current theme: same font link, fresh CSS versions."""
    fonts_key = current_fonts(site)
    if fonts_key:
        sync_fonts(site, fonts_key)
    return fonts_key, bump_css_versions(Path(site))


def apply(site, accent, fonts_key):
    site = Path(site)
    css = site / "assets" / "theme.css"
    if not css.exists():
        sys.exit(f"{css} not found. Is {site} a site made from the template?")
    palette, report = derive(accent)
    src = css.read_text(encoding="utf-8")
    if not THEME_BLOCK_RE.search(src):
        sys.exit(f"theme markers missing in {css}")
    css.write_text(THEME_BLOCK_RE.sub(lambda _: theme_block(palette, fonts_key), src), encoding="utf-8")
    sync_fonts(site, fonts_key)
    version = bump_css_versions(site)
    return palette, report, version


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", nargs="?")
    ap.add_argument("--accent", help="preset name or #RRGGBB (default: keep the current one, else sunflower)")
    ap.add_argument("--fonts", choices=sorted(FONTS), help="font preset (default: keep the current one, else editorial)")
    ap.add_argument("--refresh", "--bump-only", dest="refresh", action="store_true",
                    help="re-apply the current fonts to every page and bump ?v= on local CSS links")
    ap.add_argument("--list", action="store_true", help="print the accent and font presets")
    args = ap.parse_args()

    if args.list:
        print("Accents:")
        for name, hx in ACCENTS.items():
            p, _ = derive(hx)
            print(f"  {name:10} {hx}  soft {p['soft']}  tint {p['tint']}  deep {p['deep']}  text-on-accent {p['on']}")
        print("Fonts (headings / body):")
        for name, (head, body, _) in FONTS.items():
            print(f"  {name:10} {head.split(',')[0]} / {body.split(',')[0]}")
        return
    if not args.site:
        ap.error("SITE_DIR is required")
    if args.refresh:
        fonts_key, version = refresh(args.site)
        print(f"Pages refreshed: fonts '{fonts_key or 'unchanged'}', CSS version {version}")
        return
    args.fonts = args.fonts or current_fonts(args.site) or "editorial"
    args.accent = args.accent or current_accent(args.site) or "sunflower"

    accent = ACCENTS.get(args.accent.lower(), args.accent)
    try:
        palette, report, version = apply(args.site, accent, args.fonts)
    except ValueError as e:
        sys.exit(str(e))
    print(f"Theme applied: accent {palette['accent']}, fonts '{args.fonts}', CSS version {version}")
    if palette["accent"].upper() != theme_hex(accent):
        print(f"  (nudged from {theme_hex(accent)} so text on the accent stays readable)")
    for k, v in palette.items():
        print(f"  {k:7} {v}")
    print("Contrast (ratio / target):")
    for label, (ratio, target) in report.items():
        print(f"  {ratio:5.2f} / {target:<4} {'ok ' if ratio >= target else 'LOW'} {label}")
    if contrast(palette["accent"], WHITE) < 1.4:
        print("Warning: this accent is very pale on white; bars and dots will be hard to see. Pick a stronger colour.")


if __name__ == "__main__":
    main()
