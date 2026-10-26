# Optional: password-protected case studies

Some researchers have studies they can show to a hiring panel but not to the public internet. This adds a locked panel to the home page; the content is published only as encrypted data (AES-256-GCM), and the visitor's browser decrypts it with the password the researcher shares privately.

**Offer it only when asked, or when the person has strong confidential work and illustrative numbers aren't enough.** It adds friction: recruiters must ask for a password, and many won't. The original site built this, then switched it off in favour of illustrative numbers plus real results on the resume. Mention that trade-off.

Security notes to pass on:
- Strong password (10+ characters, not reused). Anyone with it can read the content, and can copy it.
- The readable source must never be committed: keep it in `private/` and add `private/` to `.gitignore` (create `.gitignore` if missing). Check `git status` before every commit.
- Changing the password means re-running the script and publishing again; old copies of the page stay decryptable with the old password.
- Ask the person whether their employer allows sharing this material at all, even behind a password.

## Steps

1. Write the locked studies as plain HTML fragments (cards, or full case-study sections using the case-study classes) in `SITE/private/locked-case-studies.html`. It is inserted into the home page as is.
2. Add the CSS, the panel and the script below to `index.html`.
3. Encrypt: `node <skill-dir>/scripts/lock-case-studies.mjs "<password>" SITE`
4. Open `index.html`, unlock with the password, check, then publish. Re-run step 3 after every edit to the private file.

## CSS (add inside the `<style>` of index.html)

```css
/* Password-protected case studies */
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}
.locked{margin-top:4em}
.locked-panel{max-width:40rem;margin:0 auto;text-align:center;border:1px solid var(--line);border-radius:10px;background:var(--tint);padding:2.6em clamp(20px,5vw,48px)}
.lock-icon{width:34px;height:34px;color:var(--chev);margin-bottom:.8em}
.locked-panel h3{font-size:1.3rem;margin-bottom:.7em}
.locked-panel > p{font-size:1rem;margin:0 auto;max-width:32rem}
.locked-list{list-style:none;margin:1.6em auto 0;padding:0;display:grid;gap:.45em;font-size:15px;color:var(--muted)}
.unlock{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:1.8em}
.unlock input{font:400 16px var(--body);padding:12px 16px;border:1px solid var(--line);border-radius:99px;min-width:0;flex:0 1 16rem;background:#fff;color:var(--ink)}
.unlock input:focus{outline:2px solid var(--ink2);outline-offset:1px}
.unlock .btn{cursor:pointer}
.unlock-msg{min-height:1.6em;margin-top:.8em !important;font-size:14px !important;color:#B3261E}
#locked-content:empty{display:none}
```

## HTML (inside `<section id="work">`, after the cards)

```html
<div class="locked" id="locked">
  <div class="locked-panel reveal">
    <svg class="lock-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a5 5 0 0 0-5 5v3H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2h-1V7a5 5 0 0 0-5-5zm-3 5a3 3 0 1 1 6 0v3H9V7zm3 7a2 2 0 0 1 1 3.73V19h-2v-1.27A2 2 0 0 1 12 14z"/></svg>
    <h3>More studies, with real results</h3>
    <p>These include confidential product results, so they are password-protected. If you are reviewing my work for a role, <a href="#contact">ask me for the password</a>.</p>
    <ul class="locked-list">
      <li>{{Locked study title 1}}</li>
      <li>{{Locked study title 2}}</li>
    </ul>
    <form class="unlock" id="unlock-form" autocomplete="off">
      <label class="sr-only" for="unlock-pw">Password</label>
      <input id="unlock-pw" type="password" placeholder="Password" required>
      <button class="btn" type="submit">Unlock</button>
    </form>
    <p class="unlock-msg" id="unlock-msg" role="status" aria-live="polite"></p>
  </div>
</div>
<div id="locked-content"></div>
<script type="application/json" id="locked-data">{}</script>
```
The titles in `.locked-list` are public; keep them vague enough to be safe.

## JavaScript (after the reveal script, before `</body>`)

```html
<script>
// Locked case studies are AES-GCM encrypted (scripts/lock-case-studies.mjs);
// the password decrypts them in the browser. Nothing readable is in the page.
(function(){
  var form = document.getElementById('unlock-form');
  if (!form || !window.crypto || !crypto.subtle) return;
  var data; try { data = JSON.parse(document.getElementById('locked-data').textContent); } catch (e) { return; }
  if (!data.ct) return;
  var msg = document.getElementById('unlock-msg');
  function b64(s){ return Uint8Array.from(atob(s), function(c){ return c.charCodeAt(0); }); }
  function unlock(pw){
    return crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveKey'])
      .then(function(base){ return crypto.subtle.deriveKey({name:'PBKDF2', salt:b64(data.salt), iterations:data.iter, hash:'SHA-256'}, base, {name:'AES-GCM', length:256}, false, ['decrypt']); })
      .then(function(key){ return crypto.subtle.decrypt({name:'AES-GCM', iv:b64(data.iv)}, key, b64(data.ct)); })
      .then(function(buf){
        var box = document.getElementById('locked-content');
        box.innerHTML = new TextDecoder().decode(buf);
        box.querySelectorAll('.reveal').forEach(function(e){ e.classList.add('in'); });
        document.getElementById('locked').hidden = true;
        try { sessionStorage.setItem('cs-pw', pw); } catch (e) {}
      });
  }
  form.addEventListener('submit', function(ev){
    ev.preventDefault();
    var pw = document.getElementById('unlock-pw').value;
    msg.textContent = 'Unlocking…'; msg.style.color = 'var(--muted)';
    unlock(pw).then(function(){ msg.textContent = ''; }, function(){ msg.style.color = ''; msg.textContent = 'That password didn\'t work. Please try again.'; });
  });
  var saved = null; try { saved = sessionStorage.getItem('cs-pw'); } catch (e) {}
  if (saved) unlock(saved).catch(function(){ try { sessionStorage.removeItem('cs-pw'); } catch (e) {} });
})();
</script>
```
