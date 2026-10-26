# Theming

The layout stays the same for everyone (it's tested and it works); the accent colour, fonts and icon make the site the person's own. Two sites built with this skill should not look like copies, so ask for a colour.

## Choosing

Ask one light question: "Is there a colour you like, or one from your personal brand? Otherwise I'll use warm yellow." If they name a colour in words, pick the closest preset or a hex. Don't use an employer's brand colour unless they ask: the portfolio is about them, not the company.

**Accent presets** (`python3 scripts/theme.py --list` prints the derived shades):

| Preset | Hex | Feel |
|---|---|---|
| sunflower | `#FFC629` | warm, optimistic (the original site) |
| coral | `#FF7A59` | friendly, energetic |
| teal | `#14B8A6` | calm, trustworthy |
| sky | `#38BDF8` | light, open |
| violet | `#8061FF` | creative, confident |
| rose | `#F472B6` | playful, bold |
| leaf | `#4CC38A` | fresh, grounded |
| cobalt | `#2A62F0` | serious, corporate-friendly |

**Font presets** (all checked to load from Google Fonts):

| Preset | Headings / body | Feel |
|---|---|---|
| editorial | Merriweather / Open Sans | classic, readable (the original) |
| modern | Fraunces / Inter | contemporary, a little warm |
| classic | Lora / Source Sans 3 | literary, gentle |
| humanist | Source Serif 4 / Source Sans 3 | neutral, very legible |
| geometric | Space Grotesk / Inter | technical, product-y |
| persian | Vazirmatn / Vazirmatn | Persian or Arabic script sites |

## What the theme script does

`theme.py SITE --accent <preset or #hex> --fonts <preset>`:
- derives `--accent-soft` (highlighter), `--accent-tint` (pale fills), `--accent-deep` (small text, at least 4.5:1 on white) and `--on-accent` (ink or white, whichever reads on the accent), and prints the contrast of each against its target;
- nudges the accent slightly if no text colour can sit on it readably, and says so;
- rewrites the block between the theme markers in `assets/theme.css`, swaps the Google Fonts link on every page, and bumps the `?v=` cache version.

Chart colours (`--s1` blue, `--s2` orange, before/after blues) deliberately stay the same across themes: they were checked for colour-blind-safe contrast, and keeping data colours separate from the accent stops a highlight being mistaken for data. If the accent is itself blue or orange, that's still fine; the accent never appears inside charts.

After changing the accent, re-run `favicons.py` so the dot on the icon matches.

## Logo or photo

- **Own logo**: save it as `assets/favicon.svg` (or PNGs `assets/favicon-32.png`, `assets/favicon-512.png`, `assets/apple-touch-icon.png` 180×180, and `favicon.ico`) instead of running `favicons.py`. It also appears in the navbar.
- **Photo**: optional. If wanted, add above the eyebrow in the hero: `<img class="anim d1" src="assets/photo.jpg" alt="{Name}" width="120" height="120" style="border-radius:50%;margin-bottom:1.2em">`, a square image about 240×240 px and under 60 KB. Many researchers prefer no photo; don't push it.

## Right-to-left sites (Persian, Arabic, Hebrew, Urdu)

The CSS uses logical properties, so the layout mirrors itself. To switch a page:
1. `<html lang="fa" dir="rtl">` (or `ar`, `he`, `ur`) on every page.
2. `theme.py SITE --fonts persian` (Vazirmatn covers Persian and Arabic; for Hebrew use the geometric or humanist preset, which fall back to system Hebrew fonts, or ask).
3. Write ← instead of → in "Read the story" links and anywhere an arrow means "forward", and → instead of ← in the case-study navbar's back link. Numbers in cards and charts (`+8%`, `21% → 13%`) are kept left-to-right by the CSS, so leave those as they are.
4. Uppercase and letter-spacing on labels have no effect in these scripts; that's expected.
5. Numbers: use the script's own digits only if the person wants them; Western digits are common in tech portfolios.

For a bilingual site, build the English site first, then copy it into a `fa/` (or other) folder, translate, set `dir="rtl"`, fix the relative links (`../assets/...`), and add a language link to both navbars.
