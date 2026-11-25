/* Mark Bank audit review page: comments are kept in this browser and copied out by hand. */
(function () {
  var KEY = 'mb-audit-comments-v1';
  var notes = {};            // id -> {cid,label,text,ts}
  var db = null, col = null, dbLive = false;
  var targets = Array.prototype.slice.call(document.querySelectorAll('[data-cid]'));
  var order = {}; targets.forEach(function (el, i) { order[el.getAttribute('data-cid')] = i; });
  function loadLocal() { try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { return {}; } }
  function saveLocal() { try { localStorage.setItem(KEY, JSON.stringify(notes)); } catch (e) {} }
  notes = loadLocal();
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function holderFor(t) {
    if (t.tagName === 'TR') return t.lastElementChild;
    return t;
  }
  targets.forEach(function (t) {
    var cid = t.getAttribute('data-cid');
    var btn = el('button', 'cbtn', 'Comment'); btn.type = 'button'; btn.setAttribute('data-for', cid);
    var thread = el('div', 'cthread'); thread.setAttribute('data-thread', cid);
    var head = t.tagName === 'TR' ? null : (t.matches('h1,h2') ? t : t.querySelector('h3,h4,.cap b') );
    if (t.tagName === 'TR') { var td = holderFor(t); td.appendChild(document.createElement('br')); td.appendChild(btn); td.appendChild(thread); }
    else if (t.matches('h1,h2')) { t.appendChild(btn); t.appendChild(thread); }
    else if (head) { head.insertAdjacentElement('afterend', btn); btn.insertAdjacentElement('afterend', thread); }
    else { t.appendChild(btn); t.appendChild(thread); }
    btn.addEventListener('click', function () { openForm(cid, t.getAttribute('data-label'), thread); });
  });
  function openForm(cid, label, thread) {
    if (thread.querySelector('.cform')) { thread.querySelector('textarea').focus(); return; }
    var f = el('div', 'cform'); var ta = el('textarea'); ta.rows = 3; ta.id = 'c-' + cid; ta.placeholder = 'Your comment on: ' + label; ta.setAttribute('aria-label', 'Comment on ' + label);
    var row = el('div', 'row'); var cancel = el('button', 'btn', 'Cancel'); cancel.type = 'button'; var save = el('button', 'btn primary', 'Save comment'); save.type = 'button';
    row.appendChild(cancel); row.appendChild(save); f.appendChild(ta); f.appendChild(row); thread.appendChild(f); ta.focus();
    cancel.addEventListener('click', function () { f.remove(); });
    save.addEventListener('click', function () {
      var text = ta.value.trim(); if (!text) { ta.focus(); return; }
      var id = 'c' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
      var note = { cid: cid, label: label, text: text.slice(0, 4000), ts: Date.now() };
      notes[id] = note; saveLocal(); f.remove(); render();
      if (col) col.doc(id).set(note).catch(function () { status('Saved on this device only. Copy your comments before you leave.'); });
    });
  }
  function removeNote(id) { delete notes[id]; saveLocal(); render(); if (col) col.doc(id).delete().catch(function () {}); }
  function sorted() {
    return Object.keys(notes).map(function (id) { return { id: id, n: notes[id] }; })
      .sort(function (a, b) { return (order[a.n.cid] ?? 1e9) - (order[b.n.cid] ?? 1e9) || a.n.ts - b.n.ts; });
  }
  function render() {
    document.querySelectorAll('.cnote').forEach(function (n) { n.remove(); });
    document.querySelectorAll('.cbtn').forEach(function (b) { b.classList.remove('has'); b.textContent = 'Comment'; });
    var per = {};
    sorted().forEach(function (x) {
      var thread = document.querySelector('[data-thread="' + CSS.escape(String(x.n.cid)) + '"]'); if (!thread) return;
      per[x.n.cid] = (per[x.n.cid] || 0) + 1;
      var c = el('div', 'cnote'); c.appendChild(el('p', null, String(x.n.text)));
      var del = el('button', null, 'Delete'); del.type = 'button'; del.addEventListener('click', function () { removeNote(x.id); }); c.appendChild(del);
      thread.insertBefore(c, thread.querySelector('.cform'));
    });
    Object.keys(per).forEach(function (cid) { var b = document.querySelector('.cbtn[data-for="' + CSS.escape(cid) + '"]'); if (b) { b.classList.add('has'); b.textContent = per[cid] + (per[cid] === 1 ? ' comment · add' : ' comments · add'); } });
    var n = Object.keys(notes).length; document.getElementById('count').textContent = n + (n === 1 ? ' comment' : ' comments');
  }
  function status(msg) { var c = document.getElementById('count'); c.title = msg; }
  function exportText() {
    var list = sorted(); if (!list.length) return 'No comments yet.';
    var out = ['MARK BANK AUDIT: MY COMMENTS (' + list.length + ')', ''];
    list.forEach(function (x, i) { out.push((i + 1) + '. [' + x.n.label + ']'); out.push('   ' + String(x.n.text).replace(/\n/g, '\n   ')); out.push(''); });
    return out.join('\n');
  }
  var sheet = document.getElementById('sheet'), sheetText = document.getElementById('sheetText'), sheetMsg = document.getElementById('sheetMsg');
  function copy(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return false; });
    return Promise.resolve(false);
  }
  function showSheet() {
    var text = exportText(); sheetText.value = text; sheet.hidden = false;
    copy(text).then(function (ok) { sheetMsg.textContent = ok ? 'Copied. Paste this into the Claude Code session.' : 'Select the text below and copy it, then paste it into the Claude Code session.'; if (!ok) { sheetText.focus(); sheetText.select(); } });
  }
  document.getElementById('copyAll').addEventListener('click', showSheet);
  document.getElementById('sheetCopy').addEventListener('click', function () { copy(sheetText.value).then(function (ok) { sheetMsg.textContent = ok ? 'Copied.' : 'Copy was blocked here. Select the text and copy it by hand.'; sheetText.focus(); sheetText.select(); }); });
  document.getElementById('sheetClose').addEventListener('click', function () { sheet.hidden = true; });
  sheet.addEventListener('click', function (e) { if (e.target === sheet) sheet.hidden = true; });
  render();
  // shared store: comments survive across devices and Claude can read them
  if (window.claude && typeof window.claude.use === 'function') {
    window.claude.use('db').then(function (d) {
      if (!d) return; db = d; col = db.collection('comments');
      col.onSnapshot(function (snap) {
        var remote = {}; snap.docs.forEach(function (doc) { var v = doc.data(); if (v && v.cid && v.text) remote[doc.id] = { cid: String(v.cid), label: String(v.label || v.cid), text: String(v.text), ts: Number(v.ts) || 0 }; });
        if (!dbLive) { dbLive = true; Object.keys(notes).forEach(function (id) { if (!remote[id]) { remote[id] = notes[id]; col.doc(id).set(notes[id]).catch(function () {}); } }); }
        if (snap.metadata && snap.metadata.fromCache && !snap.docs.length) return;
        notes = remote; saveLocal(); render();
      }, function () { status('Comments are saved on this device only.'); });
    }).catch(function () {});
  }
})();

