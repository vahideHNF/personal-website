# personal-website

Vahideh Hanifzadeh's UX research portfolio. Plain HTML and CSS in a single file (`index.html`), no build step. The look is based on the [Phantom](https://github.com/jamigibbs/phantom) Jekyll theme.

## Edit content

Open `index.html` and edit:

- **Latest Work**: each `<div class="post-row">` is one project. The left side has the text and tags, and the `.figure` card on the right shows the key numbers. Rows alternate sides automatically.
- **Experience**: one `<li>` per role in the `.timeline` list.
- **Skills & Education**: the four lists in `.facts`.
- **Contact**: the email and LinkedIn buttons.

## Publish

Settings → Pages → Build and deployment → Source: *Deploy from a branch*, Branch: `main`, folder `/ (root)`.
The site is then served at https://vahidehnf.github.io/personal-website/.
