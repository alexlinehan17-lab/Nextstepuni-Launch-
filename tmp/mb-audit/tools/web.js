/* Mark Bank audit review page: comments are kept in this browser and copied out with one button.
 * Every keyed collection is a Map, so stored ids and anchors can never name an object property. */
(function () {
  var KEY = 'mb-audit-comments-v1';
  var notes = new Map();     // id -> {cid,label,text,ts}
  var col = null, dbLive = false;
  var targets = Array.prototype.slice.call(document.querySelectorAll('[data-cid]'));
  var order = new Map(); targets.forEach(function (el, i) { order.set(el.getAttribute('data-cid'), i); });
  var threads = new Map(), buttons = new Map();

  function clean(v) {
    if (!v || typeof v !== 'object' || !v.cid || !v.text) return null;
    return { cid: String(v.cid), label: String(v.label || v.cid), text: String(v.text).slice(0, 4000), ts: Number(v.ts) || 0 };
  }
  function loadLocal() {
    var out = new Map();
    try {
      var raw = JSON.parse(localStorage.getItem(KEY) || '[]');
      var rows = Array.isArray(raw) ? raw : Object.entries(raw || {});
      rows.forEach(function (row) { var n = clean(row[1]); if (n && typeof row[0] === 'string') out.set(row[0], n); });
    } catch (e) { /* storage unavailable: comments last for this visit only */ }
    return out;
  }
  function saveLocal() { try { localStorage.setItem(KEY, JSON.stringify(Array.from(notes.entries()))); } catch (e) { /* see loadLocal */ } }
  notes = loadLocal();

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }

  targets.forEach(function (t) {
    var cid = t.getAttribute('data-cid');
    var btn = el('button', 'cbtn', 'Comment'); btn.type = 'button';
    var thread = el('div', 'cthread');
    threads.set(cid, thread); buttons.set(cid, btn);
    var head = t.tagName === 'TR' ? null : (t.matches('h1,h2') ? t : t.querySelector('h3,h4,.cap b'));
    if (t.tagName === 'TR') { var td = t.lastElementChild; td.appendChild(document.createElement('br')); td.appendChild(btn); td.appendChild(thread); }
    else if (t.matches('h1,h2')) { t.appendChild(btn); t.appendChild(thread); }
    else if (head) { head.insertAdjacentElement('afterend', btn); btn.insertAdjacentElement('afterend', thread); }
    else { t.appendChild(btn); t.appendChild(thread); }
    btn.addEventListener('click', function () { openForm(cid, t.getAttribute('data-label'), thread); });
  });

  function newId() {
    var a = new Uint32Array(2);
    if (window.crypto && window.crypto.getRandomValues) window.crypto.getRandomValues(a);
    return 'c' + Date.now().toString(36) + a[0].toString(36) + a[1].toString(36);
  }
  function openForm(cid, label, thread) {
    if (thread.querySelector('.cform')) { thread.querySelector('textarea').focus(); return; }
    var f = el('div', 'cform'); var ta = el('textarea'); ta.rows = 3; ta.id = 'c-' + cid;
    ta.placeholder = 'Your comment on: ' + label; ta.setAttribute('aria-label', 'Comment on ' + label);
    var row = el('div', 'row'); var cancel = el('button', 'btn', 'Cancel'); cancel.type = 'button';
    var save = el('button', 'btn primary', 'Save comment'); save.type = 'button';
    row.appendChild(cancel); row.appendChild(save); f.appendChild(ta); f.appendChild(row); thread.appendChild(f); ta.focus();
    cancel.addEventListener('click', function () { f.remove(); });
    save.addEventListener('click', function () {
      var text = ta.value.trim(); if (!text) { ta.focus(); return; }
      var id = newId();
      var note = { cid: cid, label: label, text: text.slice(0, 4000), ts: Date.now() };
      notes.set(id, note); saveLocal(); f.remove(); render();
      if (col) col.doc(id).set(note).catch(function () { status('Saved on this device only. Copy your comments before you leave.'); });
    });
  }
  function removeNote(id) { notes.delete(id); saveLocal(); render(); if (col) col.doc(id).delete().catch(function () {}); }
  function rank(cid) { return order.has(cid) ? order.get(cid) : 1e9; }
  function sorted() {
    return Array.from(notes.entries()).map(function (e) { return { id: e[0], n: e[1] }; })
      .sort(function (a, b) { return rank(a.n.cid) - rank(b.n.cid) || a.n.ts - b.n.ts; });
  }
  function render() {
    document.querySelectorAll('.cnote').forEach(function (n) { n.remove(); });
    buttons.forEach(function (b) { b.classList.remove('has'); b.textContent = 'Comment'; });
    var per = new Map();
    sorted().forEach(function (x) {
      var thread = threads.get(x.n.cid); if (!thread) return;
      per.set(x.n.cid, (per.get(x.n.cid) || 0) + 1);
      var c = el('div', 'cnote'); c.appendChild(el('p', null, x.n.text));
      var del = el('button', null, 'Delete'); del.type = 'button'; del.addEventListener('click', function () { removeNote(x.id); }); c.appendChild(del);
      thread.insertBefore(c, thread.querySelector('.cform'));
    });
    per.forEach(function (count, cid) {
      var b = buttons.get(cid); if (!b) return;
      b.classList.add('has'); b.textContent = count + (count === 1 ? ' comment · add' : ' comments · add');
    });
    var n = notes.size; document.getElementById('count').textContent = n + (n === 1 ? ' comment' : ' comments');
  }
  function status(msg) { document.getElementById('count').title = msg; }
  function exportText() {
    var list = sorted(); if (!list.length) return 'No comments yet.';
    var out = ['MARK BANK AUDIT: MY COMMENTS (' + list.length + ')', ''];
    list.forEach(function (x, i) { out.push((i + 1) + '. [' + x.n.label + ']'); out.push('   ' + x.n.text.replace(/\n/g, '\n   ')); out.push(''); });
    return out.join('\n');
  }
  var sheet = document.getElementById('sheet'), sheetText = document.getElementById('sheetText'), sheetMsg = document.getElementById('sheetMsg');
  function copy(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return false; });
    return Promise.resolve(false);
  }
  document.getElementById('copyAll').addEventListener('click', function () {
    var text = exportText(); sheetText.value = text; sheet.hidden = false;
    copy(text).then(function (ok) {
      sheetMsg.textContent = ok ? 'Copied. Paste this into the Claude Code session.' : 'Select the text below and copy it, then paste it into the Claude Code session.';
      if (!ok) { sheetText.focus(); sheetText.select(); }
    });
  });
  document.getElementById('sheetCopy').addEventListener('click', function () {
    copy(sheetText.value).then(function (ok) { sheetMsg.textContent = ok ? 'Copied.' : 'Copy was blocked here. Select the text and copy it by hand.'; sheetText.focus(); sheetText.select(); });
  });
  document.getElementById('sheetClose').addEventListener('click', function () { sheet.hidden = true; });
  sheet.addEventListener('click', function (e) { if (e.target === sheet) sheet.hidden = true; });
  render();

  // Where the page is opened as a Claude artifact, comments also go to its shared store.
  if (window.claude && typeof window.claude.use === 'function') {
    window.claude.use('db').then(function (db) {
      if (!db) return; col = db.collection('comments');
      col.onSnapshot(function (snap) {
        var remote = new Map();
        snap.docs.forEach(function (doc) { var n = clean(doc.data()); if (n) remote.set(String(doc.id), n); });
        if (!dbLive) {
          dbLive = true;
          notes.forEach(function (n, id) { if (!remote.has(id)) { remote.set(id, n); col.doc(id).set(n).catch(function () {}); } });
        }
        if (snap.metadata && snap.metadata.fromCache && !snap.docs.length) return;
        notes = remote; saveLocal(); render();
      }, function () { status('Comments are saved on this device only.'); });
    }).catch(function () {});
  }
})();
