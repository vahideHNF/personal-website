---
name: uxr-portfolio-builder
description: Builds a complete UX research portfolio website from a researcher's CV, research reports and notes - a home page with question-titled case-study cards, an ATS-friendly resume page that saves as a clean PDF, and case studies told as visual timelines - then checks it, previews it and explains how to publish it free on GitHub Pages. Use whenever a UX researcher (or a designer, PM or data person who does research) wants a portfolio, personal website, online CV or resume page, or case-study pages; wants to turn a CV, LinkedIn profile or study reports into a portfolio; or asks to add or update a case study, refresh the resume or re-theme a site built this way. Trigger even when they never say "website", for example "help me show my research work to recruiters" or "I need something to send hiring managers before interviews".
---

# UX research portfolio builder

You are building a portfolio that gets a researcher hired. Three parts, one look:

1. **Home page** (`index.html`): a short, warm intro, then 3-4 case-study cards. Each card shows a headline number, a title written as a question, and the answer in one or two sentences.
2. **Resume** (`resume.html`): one column, plain text, standard headings, so applicant-tracking systems can read it. Its "Download PDF" button prints it to a clean 1-2 page PDF.
3. **Case studies** (`case-studies/*.html`): each one a story told as a numbered visual timeline (problem, what we suspected, how we found out, the surprise, the insight, what shipped, measured impact), with an "In short" box at the top.

Why this format: hiring managers skim. A question title makes them want the answer; a headline number proves the work mattered; a visual timeline shows research thinking in two minutes, where walls of methodology text get skipped. Everything here came from an iterated real portfolio; the reasons behind each rule are in the reference files.

The template site, the scripts and the component library do the heavy lifting. Your job is the part only you can do: finding the story in the person's material and telling it in plain words.

## Files in this skill

| Path | Use it for |
|---|---|
| `assets/portfolio-brief.md` | The fill-in form you give the person when material is missing |
| `assets/site/` | The template site; `scripts/scaffold.py` copies it |
| `assets/case-study-template.html` | The skeleton for each case-study page |
| `references/intake.md` | What to collect, how to mine CVs and reports, the questions to ask, confidentiality |
| `references/writing-guide.md` | Voice, the story arcs, card and resume formulas, number formatting |
| `references/visual-components.md` | Every timeline visual: when to use it, a ready snippet, the width maths |
| `references/theming.md` | Accent and font presets, custom colours, right-to-left languages |
| `references/publishing.md` | GitHub Pages and alternatives, link previews, updating the site |
| `references/password-protection.md` | Optional: encrypted, password-protected case studies |
| `scripts/scaffold.py` | Start a site: copy template, apply theme, make icons |
| `scripts/theme.py` | Re-theme a site; `--refresh` re-syncs fonts and CSS cache versions on every page |
| `scripts/favicons.py` | Monogram site icon from initials |
| `scripts/check_site.py` | Validate the finished site (errors and craft warnings) |
| `scripts/preview.cjs` | Screenshots, mobile overflow check, resume PDF page count (needs Playwright) |

Scripts need Python 3 (Pillow optional, for PNG icons) and, for previews, Node with Playwright. Run them with the skill's absolute path, e.g. `python3 <skill-dir>/scripts/scaffold.py ...`.

## Workflow

### 1. Gather the material

Read `references/intake.md` first. In short:

- **Look at what you already have** before asking anything: attached CV or LinkedIn PDF, research reports or decks, a filled-in brief, an existing site, notes in the conversation.
- **If there is almost nothing**, give the person `assets/portfolio-brief.md` (send or attach the file, or paste its short version) and explain they can fill it with rough notes. Offer the alternative: answering your questions here in two short rounds.
- **The minimum to start**: name, role, email; the resume facts (roles, dates, education); and for each of 2-4 projects the problem, what they did, what they found, and what changed. You can draft around other gaps.
- **Ask about confidentiality before you write a single number** (real, changed, or none; can employers be named). Getting this wrong can cost someone their job.

### 2. Plan the stories, then confirm

Pick 3-4 projects (best evidence of impact, a spread of methods, recent first; see intake.md). For each, sketch on one screen:

- the question title and the headline number for the card;
- "In short": problem / insight / impact, one sentence each;
- the 5-9 timeline steps, each with its one-sentence finding and the visual you will use (see the arcs in `writing-guide.md` and the chooser table in `visual-components.md`).

Add the site-level choices: tagline, accent colour and fonts, how employers are named, the number policy. Show this plan and get a go-ahead, because rewriting a planned story is cheap and rewriting built pages is not. If the person said "just build it", build it and list your choices at the end instead.

### 3. Scaffold and theme

```bash
python3 <skill-dir>/scripts/scaffold.py <out-dir> --initials "AB" --accent sunflower --fonts editorial
```

`<out-dir>`: a new folder such as `<firstname>-portfolio` in the working directory (or the output folder your environment uses), unless the person names a place or is updating an existing site. Accent and font presets are in `theme.py --list` and `references/theming.md`; any `#RRGGBB` works and the script keeps it readable. If the person has a logo, save it over the generated icons with the same file names.

### 4. Write the pages

Read `references/writing-guide.md` before writing, and `references/visual-components.md` before building any timeline.

- **Home**: fill every `{{…}}` in `index.html`. One card per case study, in the order of the plan. Keep the optional blocks (hero stats, "Also" cards) only when there is real material for them; delete them otherwise.
- **Resume**: fill `resume.html` from the CV, rewriting bullets as research → what it led to → result. Keep only optional sections the person has content for. Set `@page` to `letter` for the US and Canada.
- **Case studies**: copy `assets/case-study-template.html` to `case-studies/<slug>.html` for each study (short, lowercase, hyphenated slug, no employer-internal names). Build the timeline from the component snippets. Keep the NDA note only on pages whose numbers were changed. Link Previous/Next in the same order as the cards.
- Keep the card's headline number, the "In short" impact and the last timeline step consistent: the same values everywhere.
- If the number policy differs by employer, reword the note under the cards to say which studies are illustrative (e.g. "Numbers in the two Acme case studies are illustrative…").
- Fill in the site's `README.md` (delete the illustrative-numbers line if no numbers were changed).

### 5. Check and look

```bash
python3 <skill-dir>/scripts/theme.py <out-dir> --refresh   # new pages carry default fonts and ?v=1; this syncs them
python3 <skill-dir>/scripts/check_site.py <out-dir>
node <skill-dir>/scripts/preview.cjs <out-dir>             # if Playwright is available
```

Fix every error. Read every warning and fix it unless you have a reason not to. Then **look at the screenshots yourself** (home desktop and mobile, each case study, the resume): cramped text, empty visuals, bars that don't match their numbers, a resume over two pages. The checker can't judge whether the story makes sense; you can. Without Playwright, re-read each page's HTML top to bottom as a visitor would.

### 6. Hand over

- Zip the site folder (`<firstname>-portfolio.zip`) when the person will download it, or commit and push when you're working in their repository and they asked for that.
- Tell them, briefly: what's in the site; **every assumption you made and every gap you wrote around** (a missing number, a guessed date, a merged project), so they can correct it; how to preview (open `index.html`).
- Walk them through publishing with `references/publishing.md` (GitHub Pages, about 10 minutes, free), and suggest the follow-ups: share the link on LinkedIn, add it to the resume header, check the link preview.

## Updating an existing site

Sites built with this skill keep the same structure, so changes are local:

- **Add a case study**: plan it as in step 2, copy the template, add its card, fix Previous/Next on its neighbours, run the checker.
- **Update the resume**: edit `resume.html`; re-run `preview.cjs` to confirm it still prints at 2 pages or fewer.
- **Change colours or fonts**: `python3 <skill-dir>/scripts/theme.py <site> --accent teal --fonts modern`, then rebuild icons with `favicons.py` if the accent changed.
- **After adding pages or editing any CSS**: `python3 <skill-dir>/scripts/theme.py <site> --refresh`. New pages from the template carry default fonts and `?v=1`; this re-applies the site's fonts and bumps cache versions, so visitors don't get a stale stylesheet (a real bug the original site hit: new pages rendered unstyled).
- **A site not built with this skill**: read it first. Offer to rebuild it in this format rather than mixing two styles.

## What not to compromise on

- **Never invent a number, method, sample size, result or quote.** A portfolio is a professional claim; interviewers ask about every figure. If a fact is missing, ask, write around it with honest qualitative language ("most drivers", "cut by about half" only if the person said so), or leave it out, and list it in the hand-over. Invention rarely sneaks in through headline numbers; it comes through the small connective text: card blurbs, "Also" cards, captions ("fixes in between rounds"), segment descriptions, quote attributions ("usability test" when the source wasn't given), a stray "monthly" or "most". Before the checker, re-read every sentence against the material and cut what you can't source. A short true line beats a vivid guess.
- **Confidential work stays safe.** Follow the person's number policy exactly; strip internal code names, dashboards, colleague names, participant names and unblurred screenshots. When unsure, ask.
- **Show, don't tell.** Every timeline step has a visual; text only connects them. No long "Approach", "Methodology" or "Reflection" sections: methods live in the meta row and the visuals.
- **Plain words.** Short sentences, no buzzwords, jargon explained the first time. Many readers are not native English speakers, and hiring managers skim.
- **Accessible by default.** Values printed as text on every chart, `aria-label` on visual-only diagrams, real alt text, motion off for people who ask for reduced motion. The template does most of this; don't undo it.
