#!/usr/bin/env python3
"""Start a new portfolio site from the template.

    python scaffold.py OUT_DIR --initials "SR" [--accent sunflower|#RRGGBB] [--fonts editorial]

Copies assets/site/ from this skill into OUT_DIR (which must not exist or be
empty), applies the theme, makes the monogram icons, and prints the next steps.
Case-study pages are made afterwards from assets/case-study-template.html.
"""
import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import favicons  # noqa: E402
import theme  # noqa: E402

TEMPLATE = HERE.parent / "assets" / "site"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("--initials", required=True)
    ap.add_argument("--accent", default="sunflower")
    ap.add_argument("--fonts", default="editorial", choices=sorted(theme.FONTS))
    args = ap.parse_args()

    out = Path(args.out)
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} already has files in it. Pick an empty folder, or edit the existing site instead.")
    shutil.copytree(TEMPLATE, out, dirs_exist_ok=True)

    accent = theme.ACCENTS.get(args.accent.lower(), args.accent)
    palette, report, _ = theme.apply(out, accent, args.fonts)
    sys.argv = ["favicons.py", str(out), "--initials", args.initials]
    favicons.main()

    print(f"\nSite started in {out}")
    print(f"  accent {palette['accent']} · fonts {args.fonts}")
    low = [label for label, (ratio, target) in report.items() if ratio < target]
    print("  contrast: all checks pass" if not low else "  contrast too low for: " + ", ".join(low) + " (pick another accent)")
    print("Next: fill index.html and resume.html, make one page per case study from"
          " assets/case-study-template.html, then run scripts/check_site.py on the folder.")


if __name__ == "__main__":
    main()
