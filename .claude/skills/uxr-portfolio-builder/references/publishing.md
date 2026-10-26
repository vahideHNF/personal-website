# Publishing and keeping the site fresh

The site is plain HTML and CSS, so any static host works. GitHub Pages is free, needs no build step, and gives a stable address recruiters can trust. Walk the person through it at their pace; many researchers have never used GitHub, and that's fine.

## Option A: GitHub Pages in the browser (no command line, ~10 minutes)

1. Sign up or sign in at github.com.
2. Create a new repository (the **+** menu → *New repository*):
   - For the address `https://<username>.github.io/`, name it exactly `<username>.github.io`.
   - Any other name (e.g. `portfolio`) gives `https://<username>.github.io/portfolio/`.
   - Public. Tick nothing else. *Create repository*.
3. On the new repository page, click *uploading an existing file*. Unzip the site on your computer and drag **the contents** of the folder (`index.html`, `resume.html`, `assets`, `case-studies`, …) into the page, not the folder itself. *Commit changes*.
   - The `.nojekyll` file is hidden on most computers; it's fine if it doesn't upload. Add it later with *Add file → Create new file*, name `.nojekyll`, empty, commit.
4. *Settings → Pages → Build and deployment → Source: Deploy from a branch*, branch `main`, folder `/ (root)`, *Save*.
5. Wait 1-2 minutes, refresh the Pages settings, and open the address shown there.

Then put the real address everywhere it's needed: `og:url`, `og:image` and the JSON-LD `url` in `index.html`, `og:image` on case pages, the portfolio link in the resume header, and the README. Run the checker again.

## Option B: GitHub Pages with git (for people comfortable with a terminal)

```bash
cd <site-folder>
git init -b main && git add . && git commit -m "First version of my portfolio"
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```
Then step 4 above. If you (Claude) are working inside the person's repository with push access and they asked you to publish, commit on the branch they want and push; otherwise give them these commands.

## Other hosts

- **Netlify Drop** (app.netlify.com/drop): drag the folder, get an address in seconds. Good for a quick preview link; claim the site with an account to keep it.
- **Cloudflare Pages**: free, fast; connect the GitHub repository.
- **A custom domain** (e.g. `firstnamelastname.com`, ~$10-15 a year from any registrar): on GitHub Pages, *Settings → Pages → Custom domain*, then add the DNS records GitHub shows. Tick *Enforce HTTPS* once it's available.

## After it's live

- **Link preview**: paste the address into a LinkedIn post draft (or LinkedIn's Post Inspector) to check the title, description and image. Previews cache for days; the Post Inspector refreshes them.
- **Share it**: LinkedIn *Featured* section and *Contact info → Website*, email signature, the resume header, job applications.
- **Search**: the page title and meta description are what Google shows. Name, role and main methods in both is enough. Optionally add the site in Google Search Console.

## Updating

- Edit the files (or ask Claude with this skill), then upload or push again; GitHub Pages updates in a minute or two.
- **After changing any `.css` file**, bump the `?v=` in every page's `<link>` (`theme.py SITE --refresh` does it), or returning visitors may see the new HTML with the old styles.
- Re-run `check_site.py` before every publish.
- Review once a quarter: newest study in, weakest out, resume dates current.
