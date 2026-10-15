# personal-website

Vahideh Hanifzadeh's UX research portfolio. Plain HTML and CSS in a single file (`index.html`), no build step. The look is based on the [Phantom](https://github.com/jamigibbs/phantom) Jekyll theme.

## Edit content

Open `index.html` and edit:

- **In-depth case studies** are separate pages in `case-studies/` (one HTML file each, shared styles in `case-studies/case.css`). Snapp numbers are illustrative because the real ones are under NDA; Digikala numbers are real. Every project in Work is a card in `index.html` under `id="case-studies"` that links to its page.
- **Password-protected Snapp studies** are currently switched off: the section and its script are wrapped in comments in `index.html` (search for `PASSWORD`). Remove the comment wrappers to bring them back.
- **Experience**: one `<li>` per role in the `.timeline` list.
- **Skills & Education**: the four lists in `.facts`.
- **Contact**: the email and LinkedIn buttons.

## Publish

Settings → Pages → Build and deployment → Source: *Deploy from a branch*, Branch: `main`, folder `/ (root)`.
The site is then served at https://vahidehnf.github.io/personal-website/.

## Password-protected case studies

The Snapp case studies contain internal results, so the page only contains an encrypted copy (AES-256-GCM, key from the password via PBKDF2). Visitors type the password and the browser decrypts it. The readable source is **not** in this repo.

To edit them or change the password:

1. Put the readable file at `private/snapp-case-studies.html` (git-ignored, keep your own copy safe).
2. Edit it, then run `node scripts/lock-case-studies.mjs "<password>"`.
3. Commit the updated `index.html`.
