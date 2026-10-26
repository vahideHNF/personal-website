# UX research portfolio builder (a Claude skill)

Turns your CV and research work into a portfolio website: a home page with case-study cards, a resume page that saves as a clean PDF, and case studies told as visual stories. It then checks the site and walks you through publishing it for free.

**See an example built in this style:** https://vahidehnf.github.io/personal-website/

What you get:
- **Home page**: a short intro, then 3-4 cards. Each card has a headline number and a title written as a question ("Why were drivers bidding two to three times the fare?").
- **Resume page**: one column and plain text, so applicant-tracking systems can read it. A *Download PDF* button saves it as a 1-2 page PDF.
- **Case-study pages**: each story is a numbered timeline of small charts and diagrams (problem → what we suspected → what we found → what shipped → the result), with an "In short" summary at the top.
- **A colour and font theme** of your choice, an icon made from your initials, and a checklist for putting it online.

---

## 1. Install the skill

**Claude app or claude.ai**: open the `uxr-portfolio-builder.skill` file you were sent and click **Save skill**. Or go to *Settings → Capabilities → Skills*, choose *Upload skill*, and select the file. Menu names can change a little over time. Skills need to be turned on for your account (and, on a Team or Enterprise plan, allowed by your admin).

**Claude Code**: copy the `uxr-portfolio-builder` folder into `~/.claude/skills/` (for all your projects) or into `.claude/skills/` inside a project.

You don't need to name the skill when you ask. Asking for a portfolio website is enough to start it.

## 2. Gather your material (15-30 minutes)

The better the input, the better the site. In order of usefulness:

1. **Your CV**, or your LinkedIn profile saved as a PDF (on your profile: *More → Save to PDF*).
2. **2-4 projects you're proud of**: the report, deck or one-pager for each, **with confidential details removed**. If you have no documents, a few rough notes per project are fine.
3. **The brief**: [`assets/portfolio-brief.md`](assets/portfolio-brief.md). Fill in what you can; it asks for what CVs and reports usually leave out (what the team believed before, the surprise, what shipped, the measured result).
4. **Your confidentiality rules**: can employers be named? May the site show real numbers, changed ("illustrative") numbers, or none? Check with your manager if you're unsure.
5. Optional: a job ad you like, a colour you like, a logo, cleaned screenshots.

> You can also start with nothing. Claude will ask you questions in two short rounds instead.

## 3. Copy a prompt

Attach your files, paste one of these, and change the parts in [brackets].

**Build everything (recommended)**
```
Use the UX research portfolio skill to build my portfolio website and resume.
Attached: my CV, my filled-in portfolio brief, and reports for [3] projects.
Confidentiality: [name my employers / describe them only]; on case-study pages [real numbers are fine / change the numbers and mark them illustrative / no numbers]; my resume [may / may not] show real results.
I'm applying for [Senior UX Researcher roles in fintech].
Show me the plan for the case studies before you build.
```

**Start from just a CV**
```
I'm a UX researcher and I want a portfolio website like the one the UX research portfolio skill makes.
Here's my CV. Interview me about my best 3 projects, ask about confidentiality first, then build the site.
```

**Start from nothing**
```
I want a UX research portfolio website and an ATS-friendly resume. I don't have anything written yet.
Please ask me what you need, a few questions at a time.
```

**Add a case study to an existing site**
```
Add a new case study to my portfolio (folder [my-portfolio], or the attached zip).
Attached: the report for [the onboarding study]. Numbers must be [illustrative].
Put its card [first / after the checkout study].
```

**Tailor the resume to a job**
```
Update resume.html in my portfolio for this job ad (pasted below).
Use only true facts from my experience; reorder and reword bullets to match what they're looking for.
Keep it to 2 pages.
[paste the job ad]
```

**Change the look**
```
Re-theme my portfolio: accent colour [teal / #0F766E], fonts [modern]. Update the icon too.
```

**Help me publish**
```
My portfolio is ready. Walk me through putting it on GitHub Pages step by step. I've never used GitHub.
```

## 4. Tips for a great result

- **Numbers make the cards.** Even one number per project helps: a sample size ("1,200 responses"), a problem size ("38% abandoned"), or a result ("+9% completion").
- **Tell Claude the surprise.** "We thought X, but it was Y" is the heart of a good case study, and it's rarely written in reports.
- **Say what changed** because of your research: shipped, tested, decided, or stopped. A decision is impact too.
- **Claude won't invent facts.** If something is missing, it asks or leaves it out, and at the end it lists everything it assumed so you can correct it. Read that list.
- **Check confidentiality yourself** before publishing. You know what's sensitive in your company; Claude only knows what you tell it.
- **Junior or switching careers?** Bootcamp, academic, volunteer and personal projects work well. Say what they were.
- **Not in English?** The site supports right-to-left languages (Persian, Arabic, Hebrew). Ask for it.

## 5. After the build

You'll get a folder (or a zip) with your site. Open `index.html` to preview it in your browser. To put it online, follow `references/publishing.md`, or just ask Claude to walk you through it. GitHub Pages is free and takes about 10 minutes. Then add the link to your LinkedIn profile and your resume.

---

### What's inside this folder

| Path | What it is |
|---|---|
| `SKILL.md` | Instructions Claude follows |
| `assets/portfolio-brief.md` | The form you fill in |
| `assets/site/`, `assets/case-study-template.html` | The website template |
| `references/` | Guides Claude reads: intake, writing, visual components, theming, publishing, password protection |
| `scripts/` | Helpers: start a site, apply a theme, make the icon, check the site, take screenshots |
