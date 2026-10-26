# Writing guide

Examples marked *(original)* come from the portfolio this skill was built from; the rest are invented. They show patterns. Never reuse their wording or facts: write from the person's own material, in their voice.

## Contents
1. Readers and voice
2. Home page copy
3. Case-study pages
4. Story arcs (pick one per study)
5. Numbers
6. Resume
7. Final read-through

## 1. Readers and voice

| Reader | Time | Looks for |
|---|---|---|
| Recruiter | 30 seconds | Role, seniority, domains, a link to the resume |
| Hiring manager | 2-3 minutes per study | Problem framing, judgement, impact, how they work with teams |
| Research peer (panel interview) | 10 minutes | Rigour: sample, method fit, caveats |

Write so the first two get what they need from headings, numbers and visuals alone, and the third finds the detail in captions.

**Voice**
- Plain English, around CEFR B1-B2: short sentences (under ~20 words), common words, active voice. Many readers are not native speakers.
- "I" for what the person did, "we" for the team. Hiring managers want to know which was which.
- Concrete over abstract: "drivers cancelled within two minutes" beats "suboptimal post-acceptance behaviour".
- Explain any method a product manager might not know, in five words or fewer ("latent class analysis, a way to find hidden groups").
- One idea per sentence. Bold (`<b>`) one key phrase per paragraph at most.
- Avoid: leverage, utilize, synergy, robust, seamless, delve, spearheaded, passionate about, holistic, cutting-edge. The checker flags them.

## 2. Home page copy

**Eyebrow**: the role title, e.g. "UX Researcher", "Senior Mixed-Methods Researcher".

**Tagline (h1)**: "Hi, I'm {first name}." plus one sentence about what they do *for teams*, with the key word in `<mark>`.
- *(original)* "Hi, I'm Vahideh. I find the <mark>why</mark> behind what people do."
- "Hi, I'm Sam. I turn messy questions into <mark>decisions</mark> teams can ship."
- "Hi, I'm Lea. I make sure we build on <mark>evidence</mark>, not guesses."
Draw it from how the person describes their work; ask "what do teammates come to you for?" if nothing fits.

**Intro**: two short paragraphs.
1. Who they are: years, industries in bold, what they help teams decide. A human touch is welcome ("a curious explorer of the world and of the minds of users" *(original)*).
2. How they work: the methods they mix and why ("interviews to understand *why*, surveys to measure *how many*"), one differentiator (SQL, statistics, a design background, a second language), one generous detail (mentoring, teaching).

**Work subtitle**: one line framing the cards. *(original)* "Four research stories, each starting with <mark>a question worth answering</mark> and ending with what changed."

**Cards**
- **Label**: `Company · Product area` (or the neutral description if employers are hidden).
- **Title**: the case study's question. Make it a question a curious stranger would want answered, with the tension inside it:
  - *(original)* "Why were drivers bidding two to three times the fare?"
  - *(original)* "Why weren't sellers buying the most-viewed ad slot?"
  - "Why did half of new users never finish setting up their account?"
  - Weak: "Driver Bidding Research" (a topic, not a question), "How might we improve onboarding?" (no tension).
- **Body**: one or two sentences: the answer in plain words, the insight in bold. *(original)* "They were bidding blind. Research on both sides of the market turned guessing into a **live win-chance signal**, and prices came down."
- **Headline number**: the single most impressive *true* result, with a 2-4 word caption saying what it measures ("+15%" / "finished scheduled rides"). No metric? Use a scale or outcome ("37 interviews", "3 segments").

**"Also" cards** (optional): talks, articles, mentoring, side projects. State only what you know: title, venue, year, a link. If the person gave only a title, the card is just the title and venue; don't summarise a talk you haven't seen.

**Contact**: a heading that echoes the tagline ("Let's find the <mark>why</mark> together" *(original)*) and one inviting sentence naming what people can reach out about.

## 3. Case-study pages

**Kicker**: `Company · Product area · Year`.

**Title (h1)**: the same question as the card.

**Sub**: 2-3 sentences: the context a stranger needs, the tension, a hint of the answer with one bold phrase. *(original)* "Scheduled rides let passengers book a long trip days ahead. Too many drivers dropped them within two minutes. The answer wasn't *who* the drivers were, but **what had happened to them before**."

**Meta row**: My role (with "lead" if true), Team (roles, not names), Timeline (duration and season or dates), Methods (2-4, plain words).

**In short**: three rows, one sentence each.
- Problem: the situation, with a number if there is one.
- Insight: the reframe, with the key phrase in `<mark>`. Good insights say why, not what: "Quick cancellers weren't a different kind of driver. They had been <mark>let down by passengers</mark> before." *(original)*
- Impact: what shipped and what it did, numbers in bold.

**Timeline steps** (5-9). Each step:
- `when`: a 2-5 word time or story marker ("It started with a survey", "The surprise", "Measured on real rides", "Round 2, nine months later").
- `h2`: the finding of this step as a full sentence, not a topic. "Passengers saw prices they couldn't trust", not "Passenger survey results".
- At most two short sentences of text, often none.
- One visual, with a caption naming the source and base: "Driver survey · 2,300 responses · multiple answers".

**Recommendations, "In one glance"**: every recommendation with an honest status: Shipped, Tested, In development, Next, or Dropped. A dropped idea, with a reason in the step before, shows judgement.

**Leave out**: separate Approach, Methodology, Process or Reflection sections, long stakeholder lists, and research-process diagrams that would fit any project. The original site removed all of these after testing them; methods show up in the meta row and in the steps that use them. If a reflection matters, make it the last step ("What I'd do differently") with a visual.

## 4. Story arcs

Choose the arc that fits the study, then pick visuals (see `visual-components.md`).

**A. Problem → insight → fix → impact** (the default; most evaluative and mixed-methods studies)
1. The problem in numbers (ring, split)
2. What the team suspected (hypotheses)
3. How you found out (vs for the groups compared, split for sample sizes)
4. The surprise (chips "≈", or hypotheses marked yes/no)
5. The real driver (paired bars, people row, flow for a vicious cycle)
6. What was designed (phone mock-up, tiers, flow before/after)
7. Measured impact (diverging bars, before/after bars)
8. Optional: a trade-off or what's next (diverging bars with gain and cost)

**B. Repeated or tracking study** (a survey run twice, a quarterly pulse)
Setup with both rounds (vs) → round-1 barriers (bars) → the big round-1 finding → fixes shipped and measured (diverging bars) → round 2: what moved (before/after bars) → the new bottleneck (`mark` the word that changed) → the next fix.

**C. Discovery or generative study** (no launch yet)
The question and why it mattered → who you talked to (split, vs) → what people do today (journey) → patterns (bars with "9 of 14", quotes) → the reframe (flow or chips) → opportunities and what the team decided (status list). Impact = decisions and direction.

**D. Usability or design iteration**
The flow and where it broke (bars as a funnel) → what users said (quotes) → the design change (flow before/after, phone mock-up, shots) → round 2 results (before/after bars) → launch metrics if any.

**E. Segmentation or personas**
Why one-size-fits-all failed → data and method in plain words (split) → the segments (vs with shares) → how they differ on what matters (paired bars) → what each segment got (tiers) → impact.

## 5. Numbers

- Minus sign `−` (not hyphen) for negatives: −3.1%. Plus sign on positive changes: +15%.
- Multiplication sign: 11×.
- Percentage points for differences between percentages: "+4 pp" (explain once if needed).
- Ranges with an en dash and no spaces: 27–36%. Year ranges the same: 2024–2026.
- Thousands separators: 2,300. Round survey percentages to whole numbers unless the decimal matters.
- Ratios that people feel: "4 in 5", "≈ 1 in 2".
- Always say what a number measures and among whom: "52% of drivers with no long-distance ride last month".
- Captions state the source and base: survey, interviews, A/B test, analytics; n; date.
- Illustrative numbers: follow the policy in `intake.md` and keep each value identical everywhere it appears (card, In short, step, recommendations).

## 6. Resume

**Structure**, in this order: header (name, role, city and country, email, LinkedIn, portfolio URL) → Summary → Experience → optional Teaching and Mentoring → Education → Skills → optional Publications and Talks, Certifications, Volunteering, Honors. Standard headings so ATS parsers find them.

**Summary**: 3-4 sentences. *(original)* "UX Researcher with 5+ years in research and design across ride-hailing, e-commerce and enterprise software. I plan and run mixed-methods research (interviews, usability tests, surveys and segmentation) and follow it through to shipped, A/B-tested changes. Computer Engineering graduate, comfortable with SQL and statistics. Mentored 50+ students in UX research and design."

**Experience bullets**: 3-6 for the current role, 2-3 for older ones. Start with a scope bullet, then project bullets that follow *research → what it led to → result*, with a bold project name:
- *(original)* "**Scheduled rides:** Compared quick cancellers with drivers who finished (2,400+ responses). The resulting fixes cut passenger cancellations 2.75% and raised finished rides 17.8%."
- Weak: "Responsible for conducting user interviews and surveys."
Start bullets with a strong past-tense verb (Led, Surveyed, Ran, Built, Compared, Raised, Cut, Redesigned). Each bullet one line or two, never three.

**Dates**: "Apr 2024 – Present". **Length**: 1 page under ~5 years of experience, 2 pages maximum otherwise; `preview.cjs` reports the page count. **Keywords**: use the methods and tools from target job ads *only where true*.

**Real vs illustrative**: the resume carries real measured results when the person allows it, which is why case-study NDA notes point to the resume.

## 7. Final read-through

Before running the checker, read each page as a stranger would:
- Does every card make you want to click?
- Can you get each case study from its headings and visuals alone?
- Is every number traceable to the person's material (or clearly illustrative)?
- Did anything confidential slip through (code names, colleague names, raw screenshots)?
- Is there anything you would be embarrassed to be asked about in an interview? Then it shouldn't be there.
