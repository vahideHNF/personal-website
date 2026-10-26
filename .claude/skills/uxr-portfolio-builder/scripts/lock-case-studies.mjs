// Encrypt private case studies into a portfolio's index.html.
//
//   node lock-case-studies.mjs "<password>" SITE_DIR [SOURCE_HTML]
//
// SOURCE_HTML defaults to SITE_DIR/private/locked-case-studies.html. Keep that
// folder out of git (add "private/" to .gitignore): only the ciphertext is
// published. AES-256-GCM, key from the password with PBKDF2-SHA-256 (600,000
// rounds), written into <script id="locked-data"> in index.html; the page
// decrypts it in the visitor's browser. See references/password-protection.md.
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { webcrypto as crypto } from 'node:crypto';

const [password, site, srcArg] = process.argv.slice(2);
if (!password || password.length < 10 || !site) {
  console.error('Usage: node lock-case-studies.mjs "<password, 10+ characters>" SITE_DIR [source.html]');
  process.exit(1);
}
const src = srcArg || join(site, 'private', 'locked-case-studies.html');
const indexPath = join(site, 'index.html');

const ITER = 600000;
const enc = new TextEncoder();
const salt = crypto.getRandomValues(new Uint8Array(16));
const iv = crypto.getRandomValues(new Uint8Array(12));
const base = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']);
const key = await crypto.subtle.deriveKey({ name: 'PBKDF2', salt, iterations: ITER, hash: 'SHA-256' },
  base, { name: 'AES-GCM', length: 256 }, false, ['encrypt']);
const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(readFileSync(src, 'utf8')));

const b64 = (u8) => Buffer.from(u8).toString('base64');
const payload = JSON.stringify({ v: 1, iter: ITER, salt: b64(salt), iv: b64(iv), ct: b64(new Uint8Array(ct)) });

const page = readFileSync(indexPath, 'utf8');
const re = /(<script type="application\/json" id="locked-data">)[\s\S]*?(<\/script>)/;
if (!re.test(page)) {
  console.error('No <script type="application/json" id="locked-data"> in index.html. Add the locked section first.');
  process.exit(1);
}
writeFileSync(indexPath, page.replace(re, `$1${payload}$2`));
console.log(`Encrypted ${src} into ${indexPath} (${payload.length} bytes).`);
