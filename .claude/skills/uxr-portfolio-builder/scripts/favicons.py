#!/usr/bin/env python3
"""Make a monogram site icon: initials on a soft square, with an accent dot.

    python favicons.py SITE_DIR --initials "SR" [--accent "#FFC629"]

Writes into SITE_DIR/assets/:
  favicon.svg            always (the browser renders it with a serif font)
  favicon-32.png, favicon-512.png, apple-touch-icon.png, ../favicon.ico
                         when Pillow is installed (pip install pillow)

The accent defaults to the --accent value in assets/theme.css. Skip this script
if the person has their own logo: save it as the same file names instead.
"""
import argparse
import re
from pathlib import Path

BG = "#FBFAF6"
INK = "#1F2A33"
FONT_CANDIDATES = [
    # Linux
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    # macOS
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/Library/Fonts/Georgia Bold.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    # Windows
    "C:/Windows/Fonts/georgiab.ttf",
    "C:/Windows/Fonts/timesbd.ttf",
]


def read_accent(site):
    css = site / "assets" / "theme.css"
    if css.exists():
        m = re.search(r"--accent:\s*(#[0-9A-Fa-f]{6})", css.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return "#FFC629"


def svg(initials, accent):
    # Sized so even wide serif fonts (Georgia Bold) stay clear of the dot.
    size = {1: 58, 2: 40, 3: 29}[len(initials)]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<rect width="100" height="100" rx="22" fill="{BG}"/>
<text x="45" y="52" text-anchor="middle" dominant-baseline="central" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="{size}" fill="{INK}">{initials}</text>
<circle cx="86" cy="74" r="6.5" fill="{accent}"/>
</svg>
"""


def png_set(initials, accent, out):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False
    font_path = next((p for p in FONT_CANDIDATES if Path(p).exists()), None)

    def render(px):
        scale = 4  # draw large, then shrink for smooth edges
        n = px * scale
        img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * 0.22), fill=BG)
        fsize = int(n * {1: 0.58, 2: 0.52, 3: 0.40}[len(initials)])
        font = ImageFont.truetype(font_path, fsize) if font_path else ImageFont.load_default(size=fsize)
        # Keep the letters clear of the dot, however wide the font is.
        while fsize > 8 and d.textlength(initials, font=font) > n * 0.64:
            fsize -= max(1, fsize // 20)
            font = ImageFont.truetype(font_path, fsize) if font_path else ImageFont.load_default(size=fsize)
        d.text((n * 0.45, n * 0.52), initials, font=font, fill=INK, anchor="mm")
        r = n * 0.065
        cx, cy = n * 0.86, n * 0.74
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
        return img.resize((px, px), Image.LANCZOS)

    render(32).save(out / "favicon-32.png")
    render(512).save(out / "favicon-512.png")
    # iOS adds its own rounded corners, so give it a full square.
    touch = Image.new("RGBA", (180, 180), BG)
    touch.alpha_composite(render(180))
    touch.convert("RGB").save(out / "apple-touch-icon.png")
    render(48).save(out.parent / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site")
    ap.add_argument("--initials", required=True, help="1 to 3 letters, e.g. SR")
    ap.add_argument("--accent", help="#RRGGBB; defaults to the theme accent")
    args = ap.parse_args()

    site = Path(args.site)
    out = site / "assets"
    out.mkdir(parents=True, exist_ok=True)
    initials = re.sub(r"[^\w]", "", args.initials)[:3].upper() or "?"
    accent = args.accent or read_accent(site)
    (out / "favicon.svg").write_text(svg(initials, accent), encoding="utf-8")
    if png_set(initials, accent, out):
        print(f"Icons written for '{initials}': favicon.svg, PNGs and favicon.ico")
    else:
        print(f"favicon.svg written for '{initials}'. Pillow is not installed, so no PNG/ICO icons;"
              " browsers use the SVG. For iPhone home-screen icons: pip install pillow, then re-run.")


if __name__ == "__main__":
    main()
