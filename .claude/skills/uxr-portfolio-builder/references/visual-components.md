# Visual components for the case-study timeline

Every timeline step gets exactly one visual inside `<div class="vis">…</div>`, usually followed by `<p class="cap">source · base</p>`. All styles are already in `case-studies/case.css`; copy the snippets and change the content. Values are always printed as text, so the charts work in greyscale, in screen readers and in print.

## Contents
1. Which visual for which moment
2. Width maths
3. Snippets: rings · people · bars · paired bars · before/after · diverging · split · vs · chips · hypotheses · flow · journey · quotes · phone mock-up · tiers · screenshots · status list
4. Accessibility checklist

## 1. Which visual for which moment

| Story moment | Use | Avoid |
|---|---|---|
| One share of a whole ("82% had tried it") | rings (1-3 rings) | a bar chart of one bar |
| A share people should *feel* ("4 in 5 passengers") | people row | a percentage alone |
| Ranked reasons, barriers, a funnel | bars | more than 7 rows |
| Two groups on the same questions | paired bars + legend | two separate charts |
| Before vs after, round 1 vs round 2 | before/after bars (one hue, light → dark) | two unrelated colours |
| Results after launch, A/B effects, trade-offs | diverging bars | a table of deltas |
| Sample sizes, a pair of headline facts | split | long sentences of numbers |
| Who was compared or interviewed (segments, rounds, personas) | vs | bullet lists |
| "No difference on any of these", topics, hints | chips | paragraphs |
| What the team suspected; which held up | hypotheses (plain, `.yes`, `.no`) | numbered lists |
| A process, a vicious cycle, a redesigned flow | flow | images of diagrams |
| What people go through, where it hurts | journey | a full journey-map image |
| Voices from interviews | quotes (1-3) | quotes longer than ~30 words |
| What was built (confidential UI) | phone mock-up | real screenshots under NDA |
| Levels, tiers, segments with a short rule each | tiers | a table |
| Real, cleaned screens you may share | screenshots | unblurred internal data |

Use each component at most twice per page so the story has rhythm.

## 2. Width maths

- **Bars**: `width = value / largest value in that chart × 90`, rounded. The longest bar is 90% wide, leaving room for its label. Example: values 68, 52, 21 → 90%, 69%, 28%.
- **Funnels** where the first step is 100%: use the value itself as the width (100%, 85%, 42%).
- **Ranges** ("27–36%"): width from the midpoint.
- **Diverging bars**: `width = |value| / largest |value| in that chart × 45`. The largest bar fills 45% of the track (the half is 50%). `neg` grows left of zero, `pos` grows right.
- **Rings**: `--p` is the percentage itself (0-100).
- **People row**: 5 icons; `on` = round(share × 5). For finer shares use 10 icons.
- Bars inside one chart share a scale. Never mix scales across rows.

## 3. Snippets

### Rings
```html
<div class="rings">
  <div class="ring"><i style="--p:82" aria-hidden="true"></i><div><b>82%</b><span>of drivers had tried bidding</span></div></div>
  <div class="ring"><i style="--p:51;--c:var(--s2)" aria-hidden="true"></i><div><b>51%</b><span>were satisfied with it</span></div></div>
</div>
```
`--c` sets the colour (default blue `--s1`; use `--s2` for the worrying number). The text can be a ratio: `<b>≈ 1 in 2</b>`.

### People row
```html
<div class="people-row">
  <div class="people" role="img" aria-label="4 out of 5">
    <svg viewBox="0 0 34 44" class="on" aria-hidden="true"><circle cx="17" cy="9" r="8"/><path d="M3 44v-9a14 14 0 0 1 28 0v9z"/></svg>
    <svg viewBox="0 0 34 44" class="on" aria-hidden="true"><circle cx="17" cy="9" r="8"/><path d="M3 44v-9a14 14 0 0 1 28 0v9z"/></svg>
    <svg viewBox="0 0 34 44" class="on" aria-hidden="true"><circle cx="17" cy="9" r="8"/><path d="M3 44v-9a14 14 0 0 1 28 0v9z"/></svg>
    <svg viewBox="0 0 34 44" class="on" aria-hidden="true"><circle cx="17" cy="9" r="8"/><path d="M3 44v-9a14 14 0 0 1 28 0v9z"/></svg>
    <svg viewBox="0 0 34 44" class="off" aria-hidden="true"><circle cx="17" cy="9" r="8"/><path d="M3 44v-9a14 14 0 0 1 28 0v9z"/></svg>
  </div>
  <p><b>4 in 5</b> unhappy passengers said drivers bid <b>two to three times</b> the standard fare.</p>
</div>
```

### Bars (one series, ranked; or a funnel)
```html
<ul class="rows">
  <li class="row" title="Fare too low: 68%"><span class="lbl">Fare too low</span><span class="bars"><div><span class="b" style="width:90%;background:var(--s1)"></span><span class="v">68%</span></div></span></li>
  <li class="row" title="Risk of returning empty: 52%"><span class="lbl">Risk of returning empty</span><span class="bars"><div><span class="b" style="width:69%;background:var(--s1)"></span><span class="v">52%</span></div></span></li>
  <li class="row" title="Little demand on my routes: 21%"><span class="lbl">Little demand on my routes</span><span class="bars"><div><span class="b" style="width:28%;background:var(--s1)"></span><span class="v">21%</span></div></span></li>
</ul>
<p class="cap">Drivers with no long-distance ride last month · multiple answers</p>
```
To point at the one row that matters (a funnel's drop, the surprising reason), colour only that bar `var(--s2)`. Qualitative counts work too: `<span class="v">9 of 14</span>`.

### Paired bars (two groups)
```html
<div class="legend"><span><i style="background:var(--s1)"></i>Quick cancellers</span><span><i style="background:var(--s2)"></i>Finishers</span></div>
<ul class="rows">
  <li class="row" title="A passenger cancelled on me: quick cancellers 58%, finishers 44%"><span class="lbl">A passenger cancelled on me</span><span class="bars">
    <div><span class="b" style="width:90%;background:var(--s1)"></span><span class="v">58%</span></div>
    <div><span class="b" style="width:68%;background:var(--s2)"></span><span class="v">44%</span></div>
  </span></li>
</ul>
```
Group 1 is always `--s1` (blue), group 2 always `--s2` (orange), in the same order in every row and in the legend.

### Before / after (or round 1 / round 2)
Same as paired bars with `var(--before)` (light blue) then `var(--after)` (dark blue) and a legend reading Before / After. One hue, light to dark, reads as time passing.

### Diverging bars (change after launch, A/B effects)
```html
<ul class="div-rows">
  <li class="div-row" title="Average bid price: −5.5% (better)"><span class="lbl">Average bid price</span><span class="div-track"><i class="neg" style="width:45%;background:var(--gain)"></i></span><span class="v">−5.5%</span></li>
  <li class="div-row" title="Bids per request: +3.6% (better)"><span class="lbl">Bids per request</span><span class="div-track"><i class="pos" style="width:29%;background:var(--gain)"></i></span><span class="v">+3.6%</span></li>
</ul>
<p class="cap">Change vs. the old flow · A/B test, 4 weeks</p>
```
Colour by *meaning*, not direction: a fall in cancellations is a gain. With only gains, use `--gain` for all. For a trade-off, add a legend and use `--cost` for the losses:
```html
<div class="legend"><span><i style="background:var(--gain)"></i>Gain</span><span><i style="background:var(--cost)"></i>Cost</span></div>
```

### Split (big numbers)
```html
<div class="split">
  <div><div class="big">37</div><p>seller interviews</p></div>
  <div><div class="big">390</div><p>survey responses</p></div>
</div>
```
Two or three items. Values can be short phrases: `3% vs 12%`, `&lt; 8%`.

### Vs (groups compared)
```html
<div class="vs">
  <div class="grp"><i style="background:var(--s1)"></i><b>Quick cancellers</b><span>cancelled within 2 minutes of accepting</span></div>
  <span class="x">vs</span>
  <div class="grp"><i style="background:var(--s2)"></i><b>Finishers</b><span>finished their scheduled rides</span></div>
</div>
<p class="cap" style="text-align:center">Same week, random sample of each group · about 2,300 survey responses</p>
```
The colour swatches (`<i>`) tie the groups to later paired bars; drop them if no chart follows. Three groups: omit the `x`. For rounds over time, put "9 months →" in the `x`.

### Chips
```html
<div class="chips"><span>Demographics ≈</span><span>Reasons for cancelling ≈</span><span>Fare complaints ≈</span></div>
<p class="cap">No meaningful difference in who they were, or in their stated reasons</p>
```
Also good for the topics a survey covered, or the hints a design added.

### Hypotheses
```html
<div class="hypotheses">
  <div><span>No passenger details after accepting</span></div>
  <div class="yes"><span>Passengers cancelling at the last minute</span></div>
  <div class="no"><span>A fare range that made income hard to plan</span></div>
</div>
<p class="cap">All plausible. The team couldn't build all six, so which ones actually drive cancellations?</p>
```
Plain = open question (`?`), `.yes` = confirmed (`✓`), `.no` = ruled out (`✕`). Show them open early in the story; optionally show the resolved set near the end.

### Flow (process, vicious cycle, redesigned flow)
```html
<div class="flow" role="img" aria-label="Guess a price, get rejected with no feedback, then give up or overbid, and repeat">
  <div class="box"><b>Guess</b>Driver picks a price with no signal</div>
  <span class="arrow" aria-hidden="true">→</span>
  <div class="box hot"><b>Rejected</b>No feedback on why</div>
  <span class="arrow" aria-hidden="true">→</span>
  <div class="box"><b>React</b>Give up, or overbid next time</div>
</div>
<p class="flow-back">↺ and the loop repeats</p>
```
`.hot` marks the broken step. For before/after, stack two flows with `<p class="cap" style="margin:0 0 .6em">Before</p>` above each; a single box with `style="flex-basis:100%"` shows a cramped "before".

### Journey
```html
<ol class="journey">
  <li><b>Hears about it</b>From a friend or an in-app banner</li>
  <li><b>Signs up</b>Six screens, ID upload<span class="pain">Drop-off: 41%</span></li>
  <li><b>First order</b>Can't tell delivery fees up front<span class="pain">Top complaint</span></li>
  <li><b>Comes back</b>If the first order arrived on time<span class="gain">Loyalty driver</span></li>
</ol>
```

### Quotes
```html
<div class="quotes">
  <blockquote class="quote">"If one passenger cancels on me, I stop trusting the next booking."<cite>Driver, 6 years on the app</cite></blockquote>
  <blockquote class="quote">"I just want to know if it's worth the drive back."<cite>Driver, intercity routes</cite></blockquote>
</div>
```
Real words only, lightly trimmed, never invented. Attribute by role and context, never by name.

### Phone mock-up (what was built, without a real screenshot)
```html
<div class="mock">
  <div class="phone" aria-hidden="true">
    <div class="ph-row"><span>Your bid</span><span>Long-distance trip</span></div>
    <div class="ph-big">1,250,000</div>
    <div class="ph-meter" style="--p:72%"><i></i></div>
    <div class="ph-row"><span>Chance of winning</span><b>High</b></div>
    <span class="ph-chip">Verified passenger</span>
    <div class="ph-btn">Send bid</div>
  </div>
  <div class="side">
    <p>A live <b>chance of winning</b> updates as the driver changes the price.</p>
    <p class="cap">Simplified sketch of the shipped screen</p>
  </div>
</div>
```
The phone is decorative (`aria-hidden`), so the `.side` text must say what it shows. Keep it to 3-6 elements: it's a sketch of the idea, not the UI.

### Tiers
```html
<div class="tiers">
  <div class="tier"><span class="k1">Premium</span>newer, comfortable cars</div>
  <div class="tier"><span class="k2">Standard</span>most cars</div>
  <div class="tier"><span class="k3">Economy</span>older cars</div>
</div>
```
Often sits beside a phone mock-up as the `.side`.

### Screenshots (only when allowed and cleaned)
```html
<div class="shots">
  <figure><img src="../assets/case-onboarding-before.png" alt="Old sign-up: six fields on one screen" width="600" height="1200" loading="lazy"><figcaption>Before</figcaption></figure>
  <figure><img src="../assets/case-onboarding-after.png" alt="New sign-up: one question per screen with progress dots" width="600" height="1200" loading="lazy"><figcaption>After</figcaption></figure>
</div>
```
Save images in `assets/`, under ~300 KB each (PNG for UI, JPG for photos), with width and height set to avoid layout jumps.

### Status list (recommendations, after the timeline)
```html
<section>
  <h2><span class="n">Recommendations</span>In one glance</h2>
  <ul class="next-list">
    <li><span class="status shipped">Shipped</span>Share the passenger's phone number after acceptance</li>
    <li><span class="status tested">Tested</span>Narrower suggested price range</li>
    <li><span class="status dev">In development</span>Cancellation-penalty notice for passengers</li>
    <li><span class="status later">Next</span>Passenger deposits or pre-departure confirmation</li>
    <li><span class="status dropped">Dropped</span>Fixed prices on every route</li>
  </ul>
</section>
```

## 4. Accessibility checklist

- Every chart row prints its value (`.v`) and has a `title` restating label and values (a hover tooltip).
- Anything that is only a picture (`.people`, `.flow`) gets `role="img"` and an `aria-label` that says what it shows; decorative parts get `aria-hidden="true"`.
- Colour never carries meaning alone: legends name the groups, values are printed, statuses are words.
- Every `<img>` has alt text that says what matters in the image, or `alt=""` if decorative.
- On right-to-left pages, the `.flow` arrows and bar directions flip by themselves, but arrow characters typed in text do not: write ← instead of → in "Read the story", in a `vs` separator like "9 months ←", and anywhere else. Don't hard-code left/right in inline styles.
