# personal-website

Vahideh Hanifzadeh's UX research portfolio. Plain HTML and CSS in a single file (`index.html`), no build step. The look is based on the [Phantom](https://github.com/jamigibbs/phantom) Jekyll theme.

## Edit content

Open `index.html` and edit:

- **Snapp case studies** are password-protected (see below).
- **Latest Work**: each `<div class="post-row">` is one project. The left side has the text and tags, and the `.figure` card on the right shows the key numbers. Rows alternate sides automatically.
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
