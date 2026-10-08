// Encrypts the private Snapp case studies into index.html.
//
//   node scripts/lock-case-studies.mjs "<password>" [private/snapp-case-studies.html]
//
// The readable HTML lives in private/ (git-ignored) and is never committed.
// Output: AES-256-GCM ciphertext, key derived with PBKDF2-SHA-256, written into
// <script id="locked-data"> in index.html. The page decrypts it in the browser.
import { readFileSync, writeFileSync } from 'node:fs';
import { webcrypto as crypto } from 'node:crypto';

const [password, src = 'private/snapp-case-studies.html'] = process.argv.slice(2);
if (!password || password.length < 10) {
  console.error('Usage: node scripts/lock-case-studies.mjs "<password, 10+ characters>" [source.html]');
  process.exit(1);
}

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

const page = readFileSync('index.html', 'utf8');
const re = /(<script type="application\/json" id="locked-data">)[\s\S]*?(<\/script>)/;
if (!re.test(page)) { console.error('locked-data block not found in index.html'); process.exit(1); }
writeFileSync('index.html', page.replace(re, `$1${payload}$2`));
console.log(`Encrypted ${src} into index.html (${payload.length} bytes).`);
