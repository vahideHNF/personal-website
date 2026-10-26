// Render a portfolio site the way visitors and recruiters will see it.
//
//   node preview.cjs SITE_DIR [OUT_DIR]
//
// Writes to OUT_DIR (default SITE_DIR/../preview):
//   home-desktop.png, home-mobile.png, resume.png, <case>-desktop.png,
//   <case>-mobile.png, and resume.pdf (printed exactly as "Download PDF" does).
// Prints the resume's page count, pages that scroll sideways on a phone,
// missing local files and console errors. Needs Playwright
// (npm i -g playwright && npx playwright install chromium); if it is missing,
// open the pages in a browser and check them by eye instead.
const fs = require('fs');
const path = require('path');

let chromium;
try { ({ chromium } = require('playwright')); } catch (e) {
  console.error('Playwright is not installed. Install it (npm i -g playwright && npx playwright install chromium) or preview by opening index.html in a browser.');
  process.exit(2);
}

const site = path.resolve(process.argv[2] || '.');
const out = path.resolve(process.argv[3] || path.join(site, '..', 'preview'));
fs.mkdirSync(out, { recursive: true });
const url = (p) => 'file://' + path.join(site, p);

(async () => {
  const browser = await chromium.launch();
  const problems = [];
  // Reduced motion shows every section at once, so full-page shots are complete.
  const desktop = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const mobile = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });

  async function shot(ctx, file, name) {
    const page = await ctx.newPage();
    page.on('console', (m) => { if (m.type() === 'error') problems.push(`${file}: console error: ${m.text()}`); });
    page.on('requestfailed', (r) => { if (r.url().startsWith('file:')) problems.push(`${file}: missing file ${r.url().replace('file://' + site + '/', '')}`); });
    await page.goto(url(file), { waitUntil: 'networkidle' }).catch(() => page.goto(url(file)));
    await page.evaluate(() => document.fonts && document.fonts.ready);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    if (overflow > 1) problems.push(`${file}: scrolls sideways by ${overflow}px at ${page.viewportSize().width}px wide`);
    await page.screenshot({ path: path.join(out, name), fullPage: true });
    return page;
  }

  await shot(desktop, 'index.html', 'home-desktop.png');
  await shot(mobile, 'index.html', 'home-mobile.png');

  const caseDir = path.join(site, 'case-studies');
  const cases = fs.existsSync(caseDir) ? fs.readdirSync(caseDir).filter((f) => f.endsWith('.html')).sort() : [];
  for (const f of cases) {
    const slug = f.replace(/\.html$/, '');
    await shot(desktop, `case-studies/${f}`, `${slug}-desktop.png`);
    await shot(mobile, `case-studies/${f}`, `${slug}-mobile.png`);
  }

  let pages = 0;
  if (fs.existsSync(path.join(site, 'resume.html'))) {
    const page = await shot(desktop, 'resume.html', 'resume.png');
    await page.emulateMedia({ media: 'print' });
    const pdf = await page.pdf({ path: path.join(out, 'resume.pdf'), preferCSSPageSize: true, printBackground: false });
    pages = (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
  }
  await browser.close();

  console.log(`Screenshots and resume.pdf written to ${out}`);
  console.log(`Case studies rendered: ${cases.length}`);
  if (pages) console.log(`Resume PDF: ${pages} page${pages === 1 ? '' : 's'}${pages > 2 ? '  <- too long: aim for 1-2 pages (tighten bullets or drop old roles)' : ''}`);
  if (problems.length) { console.log(`Problems (${problems.length}):`); problems.forEach((p) => console.log('  ' + p)); }
  else console.log('No missing files, console errors or sideways scrolling.');
})();
