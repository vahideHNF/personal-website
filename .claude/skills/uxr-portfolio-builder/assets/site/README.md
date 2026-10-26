# {{FULL_NAME}} — UX research portfolio

Plain HTML and CSS, no build step. Open `index.html` in a browser to preview.

## What's where

| File | What it is |
|---|---|
| `index.html` | Home page: intro, case-study cards, contact |
| `resume.html` | Resume. Its **Download PDF** button opens the print dialog: choose *Save as PDF* and turn off headers and footers |
| `case-studies/*.html` | One page per case study |
| `case-studies/case.css` | Shared styles for the case studies |
| `assets/theme.css` | Colours and fonts for every page |
| `assets/favicon*`, `favicon.ico` | The site icon |

## Edit content

- **Text**: edit the HTML files directly. Each case study has a card in `index.html` (inside `id="case-studies"`) that links to its page.
- **Add a case study**: copy an existing page in `case-studies/`, rewrite it, add a card for it in `index.html`, and update the Previous/Next links at the bottom of the neighbouring pages.
- **Colours and fonts**: change them in `assets/theme.css` (or ask Claude with the portfolio skill to re-theme the site, which also checks the contrast).
- **After changing any `.css` file**, change the `?v=` number at the end of its `<link>` in every page (for example `case.css?v=2` → `case.css?v=3`), so browsers load the new file instead of an old cached copy.
{{IF_ILLUSTRATIVE: - **Case-study numbers are illustrative** because the original data is under NDA. Real measured results are only on the resume.}}

## Publish (free, with GitHub Pages)

1. Put these files in a GitHub repository (for the shortest address, name it `<your-username>.github.io`).
2. In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch `main`, folder `/ (root)`, **Save**.
3. After a minute or two the site is live at {{SITE_URL}}.

Every change you push to `main` updates the site.
