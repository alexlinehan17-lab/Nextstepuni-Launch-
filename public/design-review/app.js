/* ==== audit.js ==== */
/* Audit view: loads assets/audit-screens.json, draws the full list once, then filters by hiding rows. */
(function () {
  var view = document.getElementById('view-audit');
  var body = document.getElementById('audit-rows');
  if (!view || !body) return;

  var count = document.getElementById('audit-count');
  var seg = document.getElementById('audit-class');
  var area = document.getElementById('audit-area');
  var find = document.getElementById('audit-q');
  var none = document.getElementById('audit-none');
  var fail = document.getElementById('audit-fail');
  var stick = document.getElementById('audit-stick');

  var NAMES = { 1: 'Good already', 2: 'Minor refinement', 3: 'Redesign', 4: 'Rebuild' };
  var AREAS = ['Core student loop', 'Exam tools', 'Launchpad', 'Sign-in and onboarding', 'Account and settings',
    'Counsellor dashboard', 'Admin dashboard', 'Learning modules', 'Other'];
  var state = { k: 0, area: '', q: '' };
  var rows = [];

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }

  /* searching ignores case and the difference between straight and curly quotes */
  function plain(s) { return String(s).toLowerCase().replace(/[\u2018\u2019]/g, "'").replace(/[\u201c\u201d]/g, '"'); }

  /* worst first; within a class: the screens Alex named, then by area, then screens few people can reach */
  function rank(a, b) {
    return (b.class - a.class) ||
      ((a.reach ? 1 : 0) - (b.reach ? 1 : 0)) ||
      ((a.issue ? 0 : 1) - (b.issue ? 0 : 1)) ||
      (AREAS.indexOf(a.area) - AREAS.indexOf(b.area)) ||
      (a.i - b.i);
  }

  function draw(list) {
    list.forEach(function (r, i) { r.i = i; });
    list.sort(rank);
    body.innerHTML = list.map(function (r) {
      var extra = '';
      if (r.device) extra += '<span class="s-x">' + esc(r.device) + '</span>';
      if (r.reach) extra += '<span class="s-x">' + esc(r.reach) + '</span>';
      return '<tr><td class="s-n"><span class="s-name">' + esc(r.screen) + '</span>' +
        (r.issue ? '<span class="s-iss">Your issue ' + r.issue + '</span>' : '') + '</td>' +
        '<td class="s-a">' + esc(r.area) + '</td>' +
        '<td class="s-k"><span class="mark k' + r.class + '">' + NAMES[r.class] + '</span></td>' +
        '<td class="s-w">' + esc(r.why) + extra + '</td></tr>';
    }).join('');
    rows = Array.prototype.map.call(body.children, function (tr, i) {
      var r = list[i];
      return { el: tr, k: r.class, area: r.area, text: plain(r.screen + ' ' + r.area + ' ' + r.why) };
    });
    /* keep the headline numbers in step with the data */
    var totals = { 1: 0, 2: 0, 3: 0, 4: 0 };
    list.forEach(function (r) { totals[r.class]++; });
    view.querySelectorAll('[data-au-count]').forEach(function (el) { el.textContent = totals[el.getAttribute('data-au-count')]; });
    view.querySelectorAll('[data-au-total]').forEach(function (el) { el.textContent = list.length; });
    apply();
  }

  /* a long list is shown thirty at a time, worst first, so the page itself stays short */
  var CAP = 30;
  var more = document.createElement('button');
  more.type = 'button'; more.className = 'pbtn'; more.id = 'audit-more'; more.hidden = true;
  more.style.marginTop = '20px';
  var host = body.closest('.tbl-wrap') || body.closest('table') || body;
  host.parentNode.insertBefore(more, host.nextSibling);
  more.addEventListener('click', function () { state.all = true; apply(); });

  function apply() {
    var shown = 0, matched = 0;
    rows.forEach(function (r) {
      var on = (!state.k || r.k === state.k) && (!state.area || r.area === state.area) && (!state.q || r.text.indexOf(state.q) >= 0);
      if (on) matched++;
      var vis = on && (state.all || matched <= CAP);
      if (r.el.hidden === vis) r.el.hidden = !vis;
      if (vis) shown++;
    });
    count.textContent = 'Showing ' + shown + ' of ' + matched + (matched < rows.length ? ' (' + rows.length + ' screens in all)' : '');
    more.hidden = state.all || matched <= CAP;
    more.textContent = 'Show all ' + matched;
    none.hidden = matched > 0 || !rows.length;
  }

  seg.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-k]');
    if (!b) return;
    state.k = +b.getAttribute('data-k'); state.all = false;
    seg.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    apply();
  });
  area.addEventListener('change', function () { state.area = area.value; state.all = false; apply(); });
  find.addEventListener('input', function () { state.q = plain(find.value.trim()); state.all = false; apply(); });

  /* the filter bar sticks just under the page's own section bar, whatever height that is */
  function setTop() {
    var bar = document.querySelector('.views');
    if (bar && stick) stick.style.setProperty('--au-top', bar.offsetHeight + 'px');
  }
  setTop();
  window.addEventListener('resize', setTop);

  /* a "fix shown at" link whose concept section is not on the page yet opens the concepts view instead */
  view.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#c-"]');
    if (a && !document.getElementById(a.getAttribute('href').slice(1))) { e.preventDefault(); location.hash = '#concepts'; }
  });

  function failed() {
    count.textContent = 'List not loaded';
    fail.hidden = false;
  }
  if (!window.fetch) { failed(); return; }
  fetch('assets/audit-screens.json')
    .then(function (res) { if (!res.ok) throw new Error(res.status); return res.json(); })
    .then(draw)
    .catch(failed);
})();

/* ==== c-launch.js ==== */
/* c-launch: choosing a Future Finder answer. Three motions and a speed switch.
   No timers: every change starts from a tap and is carried by CSS transitions. Listeners sit on the
   artboard's own elements, so they keep working when the phone is moved into the full-screen preview. */
(function () {
  var root = document.getElementById('c-launch-select');
  if (!root) return;

  /* Future Finder's own wording (futureFinderRiasecItems.ts, items I2 to I9; questions 12 to 19 of 60) */
  var QUESTIONS = [
    'Solve a tricky maths or logic problem.',
    'Figure out why something works the way it does.',
    'Analyse data to spot patterns others miss.',
    'Write code to solve a problem.',
    'Research a question deeply and write up what you find.',
    'Work out what is wrong with a patient or a system.',
    'Study how the body or the brain works.',
    'Read about a new scientific discovery.'
  ];
  var FIRST = 12, TOTAL = 60;
  var NAMES = { '1': 'A · Draw', '2': 'B · Press and set', '3': 'C · Carry' };
  var mode = '1';
  var boards = [];

  function each(list, fn) { Array.prototype.forEach.call(list, fn); }

  function makeBoard(scr) {
    var opts = scr.querySelector('[data-cl-opts]');
    var tiles = opts.querySelectorAll('.c-launch-opt');
    var carry = opts.querySelector('.c-launch-carry');
    var need = scr.querySelector('[data-cl-need]');
    var go = scr.querySelector('[data-cl-go]');
    var back = scr.querySelector('[data-cl-back]');
    var clear = scr.querySelector('[data-cl-clear]');
    var text = scr.querySelector('[data-cl-text]');
    var count = scr.querySelector('[data-cl-count]');
    var fill = scr.querySelector('[data-cl-fill]');
    var ask = scr.querySelector('[data-cl-ask]');
    var picked = -1, q = 0, answers = {};

    /* where the travelling mark sits for a tile (layout pixels, so the artboard's scale does not matter) */
    function yOf(tile) { return tile.offsetTop + (tile.offsetHeight - 22) / 2; }
    function moveTo(tile) { carry.style.transform = 'translateY(' + yOf(tile) + 'px)'; }

    function paint() {
      each(tiles, function (t, n) { t.setAttribute('aria-checked', n === picked ? 'true' : 'false'); });
      if (need) need.textContent = picked < 0 ? 'Choose one to continue.' : 'Your answer: ' + tiles[picked].getAttribute('data-label') + '.';
      if (go) go.setAttribute('aria-disabled', picked < 0 ? 'true' : 'false');
    }

    /* show a state with no motion: a new question, going back, switching the motion */
    function settle(i) {
      opts.classList.add('c-launch-still');
      picked = i;
      paint();
      carry.classList.toggle('on', mode === '3' && i >= 0);
      if (i >= 0) moveTo(tiles[i]);
      void opts.offsetWidth;
      opts.classList.remove('c-launch-still');
    }

    function select(i, side) {
      if (i === picked) return;
      var had = picked >= 0;
      var tile = tiles[i];
      if (mode === '2') {
        /* start the wipe from the side that was touched, whatever this tile did last time */
        tile.classList.add('c-launch-snap');
        tile.setAttribute('data-from', side || 'l');
        void tile.offsetWidth;
        tile.classList.remove('c-launch-snap');
      }
      picked = i;
      paint();
      if (mode === '3') {
        if (had && carry.classList.contains('on')) {
          moveTo(tile);                                  /* the same mark travels; a new tap simply retargets it */
        } else {
          carry.classList.add('c-launch-still');         /* first answer: the mark is drawn where it is needed */
          moveTo(tile);
          void carry.offsetWidth;
          carry.classList.remove('c-launch-still');
          carry.classList.add('on');
        }
      }
    }

    function show(dir) {
      if (text) text.textContent = QUESTIONS[q];
      if (count) count.textContent = (FIRST + q) + ' of ' + TOTAL;
      if (fill) fill.style.setProperty('--p', ((FIRST + q) / TOTAL).toFixed(3));
      settle(answers[q] === undefined ? -1 : answers[q]);
      [ask, opts].forEach(function (el) {
        if (!el) return;
        el.classList.remove('c-launch-fwd', 'c-launch-bwd');
        void el.offsetWidth;
        el.classList.add(dir > 0 ? 'c-launch-fwd' : 'c-launch-bwd');
      });
    }

    each(tiles, function (t, n) {
      var side = 'l';
      t.addEventListener('pointerdown', function (e) {
        var r = t.getBoundingClientRect();
        side = (e.clientX - r.left) < r.width / 2 ? 'l' : 'r';
        t.classList.add('c-launch-down');
      });
      ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (ev) {
        t.addEventListener(ev, function () { t.classList.remove('c-launch-down'); });
      });
      t.addEventListener('click', function () { select(n, side); });
    });

    [ask, opts].forEach(function (el) {
      if (!el) return;
      el.addEventListener('animationend', function (e) {
        if (e.target === el) el.classList.remove('c-launch-fwd', 'c-launch-bwd');
        if (e.animationName === 'c-launch-nudge') opts.classList.remove('c-launch-nudge');
      });
    });

    if (go) go.addEventListener('click', function () {
      if (picked < 0) {                                  /* say what is missing by pointing at it */
        opts.classList.remove('c-launch-nudge');
        void opts.offsetWidth;
        opts.classList.add('c-launch-nudge');
        return;
      }
      answers[q] = picked;
      if (q === QUESTIONS.length - 1) { q = 0; answers = {}; } else { q += 1; }
      show(1);
    });
    if (back) back.addEventListener('click', function () {
      if (q === 0) return;
      if (picked >= 0) answers[q] = picked;
      q -= 1;
      show(-1);
    });
    if (clear) clear.addEventListener('click', function () {
      picked = -1;
      paint();
      carry.classList.remove('on');
    });

    return {
      setMode: function (m) {
        opts.classList.add('c-launch-still');
        opts.setAttribute('data-mode', m);
        void opts.offsetWidth;
        opts.classList.remove('c-launch-still');
        settle(-1);
      },
      setSlow: function (on) {
        var s = scr.style;
        if (on) {
          s.setProperty('--c-launch-k', '5');
          s.setProperty('--t-press', '600ms');
          s.setProperty('--t-ui', '1000ms');
          s.setProperty('--t-move', '1300ms');
        } else {
          ['--c-launch-k', '--t-press', '--t-ui', '--t-move'].forEach(function (p) { s.removeProperty(p); });
        }
      }
    };
  }

  each(root.querySelectorAll('[data-cl-board]'), function (scr) { boards.push(makeBoard(scr)); });

  function press(group, btn) {
    each(group.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', x === btn ? 'true' : 'false'); });
  }

  each(root.querySelectorAll('[data-cl-mode] button'), function (b) {
    b.addEventListener('click', function () {
      mode = b.getAttribute('data-mode');
      press(b.parentNode, b);
      boards.forEach(function (bd) { bd.setMode(mode); });
      var cap = root.querySelector('[data-cl-cap]');
      if (cap) cap.textContent = NAMES[mode];
      each(root.querySelectorAll('[data-cl-row]'), function (r) { r.classList.toggle('on', r.getAttribute('data-cl-row') === mode); });
    });
  });

  each(root.querySelectorAll('[data-cl-speed] button'), function (b) {
    b.addEventListener('click', function () {
      press(b.parentNode, b);
      var slow = b.getAttribute('data-speed') === '5';
      boards.forEach(function (bd) { bd.setSlow(slow); });
    });
  });
})();

/* ==== c-markbank.js ==== */
/* c-markbank: Structure A's first artboard is a live stack of four screens: subject home, a strand,
   a topic, the practice card. Listeners sit on the artboard itself, so they keep working when the
   artboard is moved into the full-screen try-out. Nothing runs until a tap. */
(function () {
  var flow = document.getElementById('c-markbank-flow');
  var stackEl = flow && flow.querySelector('[data-stack]');
  if (stackEl) {
    var stack = ['home'];
    var toastTimer = null;
    var view = function (name) { return stackEl.querySelector('[data-view="' + name + '"]'); };
    var set = function (root, key, value) {
      root.querySelectorAll('[data-f="' + key + '"]').forEach(function (el) { el.textContent = value; });
    };
    var render = function () {
      var top = stack[stack.length - 1];
      var topIsTask = top === 'practice';
      stackEl.querySelectorAll('[data-view]').forEach(function (v) {
        var at = stack.indexOf(v.getAttribute('data-view'));
        v.classList.toggle('is-on', at === stack.length - 1);
        /* the page directly beneath a task stays where it is; pages beneath a pushed page move left */
        v.classList.toggle('is-held', topIsTask && at === stack.length - 2);
        v.classList.toggle('is-under', at > -1 && at < stack.length - 1 && !(topIsTask && at === stack.length - 2));
      });
    };
    var push = function (name) {
      var v = view(name);
      if (!v) return;
      var page = v.querySelector('.page');
      if (page) page.scrollTop = 0;
      stack.push(name);
      render();
    };
    var fillTopic = function (d) {
      var v = view('topic');
      var count = +d.count, tried = +d.tried;
      set(v, 'strand', d.strand); set(v, 'code', d.code); set(v, 'title', d.title);
      set(v, 'count', count); set(v, 'years', d.years); set(v, 'years2', d.years);
      set(v, 'triedline', tried ? 'You have tried ' + tried + ' of them.' : 'You have not tried any yet.');
      set(v, 'a', d.a); set(v, 'b', d.b); set(v, 'c', d.c);
      set(v, 'browse', 'Browse all ' + count + ' questions');
      var bar = v.querySelector('[data-f="bar"]');
      if (bar) bar.style.width = (tried ? Math.max(2, Math.round(100 * tried / count)) : 0) + '%';
      var years = v.querySelectorAll('[data-f="mask"] i');
      years.forEach(function (el, i) { el.classList.toggle('on', d.mask.charAt(i) === '1'); });
      /* the same three sizes the tool offers today, capped at what the topic holds */
      var sizes = [3, 6, 12].map(function (n) { return Math.min(n, count); });
      v.querySelectorAll('[data-size] button').forEach(function (b, i) {
        b.textContent = sizes[i]; b.classList.toggle('on', i === 1);
      });
      var go = v.querySelector('[data-go="practice"]');
      go.setAttribute('data-n', sizes[1]); go.setAttribute('data-title', d.title);
      go.setAttribute('data-ref', d.ref); go.setAttribute('data-marks', d.marks);
      set(v, 'practise', 'Practise ' + sizes[1] + ' questions');
    };
    var fillPractice = function (d) {
      var v = view('practice');
      var n = +d.n || 6;
      set(v, 'ptitle', d.title || 'Photosynthesis'); set(v, 'pn', 1); set(v, 'ptotal', n);
      set(v, 'pref', d.ref || ''); set(v, 'pmarks', d.marks || '');
      var steps = v.querySelector('[data-f="steps"]');
      if (steps) {
        var html = '';
        for (var i = 0; i < n; i++) html += i === 0 ? '<i class="now"></i>' : '<i></i>';
        steps.innerHTML = html;
      }
    };
    var toast = function (text) {
      var t = stackEl.querySelector('.c-markbank-toast');
      if (!t) return;
      t.textContent = text; t.hidden = false;
      clearTimeout(toastTimer);
      toastTimer = setTimeout(function () { t.hidden = true; }, 2600);
    };
    stackEl.addEventListener('click', function (e) {
      var size = e.target.closest('[data-size] button');
      if (size) {
        var v = view('topic');
        size.parentNode.querySelectorAll('button').forEach(function (b) { b.classList.toggle('on', b === size); });
        v.querySelector('[data-go="practice"]').setAttribute('data-n', size.textContent);
        set(v, 'practise', 'Practise ' + size.textContent + ' questions');
        return;
      }
      if (e.target.closest('[data-leave]')) {
        if (stack.length > 1) { stack.pop(); render(); }
        else toast('Back returns to the Launchpad.');
        return;
      }
      var go = e.target.closest('[data-go]');
      if (go) {
        var to = go.getAttribute('data-go');
        if (to === 'strand') view('strand').setAttribute('data-show', go.getAttribute('data-strand'));
        if (to === 'topic') fillTopic(go.dataset);
        if (to === 'practice') fillPractice(go.dataset);
        push(to);
        return;
      }
      var note = e.target.closest('[data-toast]');
      if (note) toast(note.getAttribute('data-toast'));
    });
  }
})();

/* ==== c-papers.js ==== */
/* c-papers: the Paper Trail mock-ups (viewer bar, paper picker, control vocabulary).
   Listeners sit on each artboard, so they keep working when one is moved to the full-screen try-out.
   Nothing runs on a timer; every change is a response to a tap or a scroll inside the artboard. */
(function () {
  var ZOOM = [75, 100, 125, 150, 200, 250];

  ['c-papers-bar', 'c-papers-pick', 'c-papers-controls'].forEach(function (id) {
    var sec = document.getElementById(id);
    if (!sec) return;
    Array.prototype.forEach.call(sec.querySelectorAll('.scr.dc'), wire);
  });

  function wire(scr) {
    var page = scr.querySelector('.page');
    var kind = scr.getAttribute('data-c-papers');
    var give = kind === 'giveway' && page ? giveWay(scr, page) : null;
    if (kind === 'quiet' && page) quiet(scr, page);

    scr.addEventListener('click', function (e) {
      var t = e.target;

      /* selection bars */
      var segBtn = t.closest('.seg button');
      if (segBtn) {
        var seg = segBtn.parentNode;
        Array.prototype.forEach.call(seg.children, function (b) { b.setAttribute('aria-selected', b === segBtn ? 'true' : 'false'); });
        var what = seg.getAttribute('data-seg');
        if (what === 'year') {
          var y = segBtn.getAttribute('data-y');
          Array.prototype.forEach.call(scr.querySelectorAll('[data-list] [data-y]'), function (r) { r.hidden = y !== 'all' && r.getAttribute('data-y') !== y; });
          var note = scr.querySelector('[data-note]');
          if (note) note.hidden = y !== '2026';
        }
        if (what === 'level') {
          Array.prototype.forEach.call(scr.querySelectorAll('[data-lv]'), function (s) { s.textContent = segBtn.textContent; });
        }
        if (give && what) give(true);
        return;
      }

      /* switches: the bar's Answers switch and the rows of the Tools sheet */
      var sw = t.closest('[data-switch]');
      if (sw) {
        var knob = sw.querySelector('.switch');
        var on = !knob.classList.contains('on');
        knob.classList.toggle('on', on);
        sw.setAttribute('aria-checked', on ? 'true' : 'false');
        var count = scr.querySelector('[data-on-count]');
        if (count) count.textContent = scr.querySelectorAll('.sheet .switch.on').length + ' on';
        return;
      }

      /* zoom steps */
      var z = t.closest('[data-zoom]');
      if (z) {
        var wrap = z.closest('[data-zoom-wrap]');
        var i = Math.max(0, Math.min(ZOOM.length - 1, Number(wrap.getAttribute('data-step')) + Number(z.getAttribute('data-zoom'))));
        wrap.setAttribute('data-step', i);
        wrap.querySelector('[data-zoom-val]').textContent = ZOOM[i] + '%';
        scr.style.setProperty('--z', ZOOM[i] / 100);
        return;
      }

      /* choice tiles in the vocabulary: one of the pair */
      var tile = t.closest('.choice[data-pair]');
      if (tile) {
        Array.prototype.forEach.call(tile.parentNode.children, function (c) { c.setAttribute('aria-pressed', c === tile ? 'true' : 'false'); });
        return;
      }

      /* the Tools sheet */
      if (page && t.closest('[data-sheet-close]')) { page.setAttribute('data-sheet', 'closed'); return; }
      if (page && t.closest('[data-sheet-open]')) { page.setAttribute('data-sheet', 'open'); return; }

      /* option B: the name in the bar goes back to the top */
      if (give && t.closest('.mid')) give(false);
    });
  }

  /* Option C of the viewer: the bar leaves while the paper is scrolled and returns on a tap. */
  function quiet(scr, page) {
    var anchor = 0, hidden = false;
    var pos = scr.querySelector('[data-pos]');
    function set(h) {
      hidden = h;
      if (h) page.setAttribute('data-state', 'quiet'); else page.removeAttribute('data-state');
      anchor = page.scrollTop;
    }
    page.addEventListener('scroll', function () {
      var y = page.scrollTop;
      if (pos) {
        var sheet = page.querySelector('.c-papers-sheet');
        var h = (sheet ? sheet.getBoundingClientRect().height / (scr.getBoundingClientRect().width / scr.offsetWidth) : 529) + 12;
        var n = Math.min(20, 7 + Math.floor((y + h * 0.45) / h));
        pos.textContent = (n < 10 ? '0' : '') + n + ' / 20';
      }
      if (y < 4) { if (hidden) set(false); return; }
      if (!hidden && Math.abs(y - anchor) > 14) set(true);
    }, { passive: true });
    scr.addEventListener('click', function (e) {
      if (hidden && !e.target.closest('button')) set(false);
    });
  }

  /* Option B of the picker: the character shrinks into the bar when the student starts working. */
  function giveWay(scr, page) {
    var fly = scr.querySelector('.c-papers-fly');
    var spot = scr.querySelector('.c-papers-spot');
    var mid = scr.querySelector('.mid');
    var nav = scr.querySelector('.nav');
    var working = false;
    function place() {
      if (!fly || !spot || !mid || !nav) return;
      /* layout offsets, so the artboard's own scale does not matter */
      var x = mid.offsetLeft + spot.offsetLeft;
      var y = parseFloat(getComputedStyle(nav).paddingTop) + spot.offsetTop;
      fly.style.setProperty('--dx', (x - fly.offsetLeft) + 'px');
      fly.style.setProperty('--dy', (y - fly.offsetTop) + 'px');
    }
    function set(on) {
      if (on === working) return;
      working = on;
      place();
      if (on) page.setAttribute('data-state', 'working');
      else { page.scrollTop = 0; page.removeAttribute('data-state'); }
      if (fly) fly.classList.toggle('disc', on);
    }
    page.addEventListener('scroll', function () { if (!working && page.scrollTop > 6) set(true); }, { passive: true });
    return set;
  }
})();

/* ==== c-progress.js ==== */
/* c-progress: the My Progress mock-ups (sections #c-progress-page and #c-progress-dark).
   Stamps the screen pieces into each artboard, then makes the section switcher, the subject menu and the
   Week / Month / Year bar work. Listeners sit on each artboard, so they keep working in the full-screen
   try-out. Nothing here closes a menu on blur: that is the fault in the current picker. No timers. */
(function () {
  'use strict';
  var hosts = document.querySelectorAll('#c-progress-page [data-c-progress], #c-progress-dark [data-c-progress]');
  if (!hosts.length) return;

  var SECS = ['overview', 'study', 'confidence', 'practice', 'milestones'];
  var NAMES = { overview: 'Overview', study: 'Study', confidence: 'Confidence', practice: 'Practice', milestones: 'Milestones' };
  var SUBJECTS = ['Accounting', 'Applied Maths', 'English', 'Geography', 'Irish', 'Mathematics', 'Politics & Society'];
  /* minutes of focus. The week is the demo account's real record; month and year are filled out to match its totals. */
  var WEEK_BY = { 'Applied Maths': [57, 0], 'Mathematics': [0, 60], 'Geography': [0, 42], 'Politics & Society': [0, 19] };
  var SHARE = { 'Geography': 0.30, 'Mathematics': 0.24, 'Applied Maths': 0.18, 'Politics & Society': 0.12, 'Accounting': 0.07, 'English': 0.05, 'Irish': 0.04 };
  var WOBBLE = [0.8, 1.2, 1, 1.5, 0.5];
  var DATA = {
    week: { label: '23 – 29 Nov', unit: 'week', word: 'this week', n: 7, ticks: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      all: [57, 121], sessions: 4, slot: 'day', best: 'Best day', active: 'Active days' },
    month: { label: 'November', unit: 'month', word: 'this month', n: 30, ticks: { 0: '1', 7: '8', 14: '15', 21: '22', 28: '29' },
      all: [15, 30, 30, 25, 0, 0, 25, 40, 135, 40, 45, 30, 40, 30, 55, 40, 30, 40, 35, 40, 30, 45, 57, 121], sessions: 24, slot: 'day', best: 'Best day', active: 'Active days' },
    year: { label: '2026', unit: 'year', word: 'this year', n: 12, ticks: ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
      all: [60, 95, 140, 170, 236, 150, 0, 60, 282, 420, 978], sessions: 63, slot: 'month', best: 'Best month', active: 'Active months' }
  };
  var NS = 'http://www.w3.org/2000/svg';
  var state = new WeakMap();

  function all(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function one(root, sel) { return root.querySelector(sel); }
  function sum(a) { return a.reduce(function (x, y) { return x + y; }, 0); }

  /* fill a placeholder from a <template>, then any placeholders that template brought with it */
  function stamp(el) {
    var t = document.getElementById(el.getAttribute('data-cp-use'));
    el.removeAttribute('data-cp-use');
    if (!t || !t.content) return;
    el.appendChild(t.content.cloneNode(true));
    all(el, '[data-cp-use]').forEach(stamp);
  }

  /* each slot's minutes are shared out between the subjects, so the subjects always add up to the total.
     A day goes to one or two subjects in turn; a month is split between all of them. */
  var TURN = ['Geography', 'Mathematics', 'Applied Maths', 'Geography', 'Politics & Society', 'Mathematics', 'Geography',
    'Applied Maths', 'Accounting', 'Mathematics', 'Geography', 'Applied Maths', 'Mathematics', 'English', 'Geography',
    'Politics & Society', 'Mathematics', 'Applied Maths', 'Geography', 'Irish'];
  var split = {};
  function shareOut(period) {
    var p = DATA[period], by = {}, last = p.all.length - 1;
    SUBJECTS.forEach(function (name) { by[name] = p.all.map(function () { return 0; }); });
    p.all.forEach(function (v, i) {
      if (p.slot === 'day') {
        var a = TURN[i % TURN.length], b = TURN[(i + 7) % TURN.length];
        var first = a === b || v < 40 ? v : Math.round(v * 0.6);
        by[a][i] += first; by[b][i] += v - first;
        return;
      }
      var w = SUBJECTS.map(function (name, k) { return SHARE[name] * WOBBLE[(i + k) % WOBBLE.length]; });
      var W = sum(w), left = v, big = 0;
      SUBJECTS.forEach(function (name, k) {
        var part = Math.round(v * w[k] / W);
        by[name][i] = part; left -= part;
        if (w[k] > w[big]) big = k;
      });
      by[SUBJECTS[big]][i] += left;
    });
    if (period === 'month') SUBJECTS.forEach(function (name) {        /* the last two days are the real week */
      var w = WEEK_BY[name] || [0, 0];
      by[name][last - 1] = w[0]; by[name][last] = w[1];
    });
    return by;
  }
  function series(period, subject) {
    if (subject === 'All subjects') return DATA[period].all;
    if (period === 'week') return WEEK_BY[subject] || [0, 0];
    if (!split[period]) split[period] = shareOut(period);
    return split[period][subject];
  }
  function hm(min, tight) {
    var h = Math.floor(min / 60), m = min % 60, gap = tight ? '' : ' ';
    if (!h) return m + '<small>m</small>';
    return h + '<small>h</small>' + (m ? gap + m + '<small>m</small>' : '');
  }
  function plain(min) {
    if (min < 100) return min + ' min';
    return Math.floor(min / 60) + 'h' + (min % 60 ? ' ' + (min % 60) + 'm' : '');
  }
  function sessionsFor(period, subject, s) {
    var p = DATA[period];
    if (subject === 'All subjects') return p.sessions;
    var active = s.filter(function (v) { return v > 0; }).length;
    if (period === 'week') return active;
    return Math.max(active, Math.round(p.sessions * (SHARE[subject] || 0)));
  }

  /* ---------- the time chart: a smooth line, a flat fill, today marked ---------- */
  function node(name, attrs, text) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (text != null) n.textContent = text;
    return n;
  }
  /* a curve that never dips below its points (monotone), so an empty day reads as zero and not less */
  function smooth(pts) {
    var n = pts.length, i, d, m = [], t = [];
    if (n < 2) return '';
    for (i = 0; i < n - 1; i++) m[i] = (pts[i + 1][1] - pts[i][1]) / (pts[i + 1][0] - pts[i][0]);
    t[0] = m[0]; t[n - 1] = m[n - 2];
    for (i = 1; i < n - 1; i++) t[i] = m[i - 1] * m[i] <= 0 ? 0 : 2 / (1 / m[i - 1] + 1 / m[i]);
    d = 'M' + pts[0][0].toFixed(1) + ' ' + pts[0][1].toFixed(1);
    for (i = 0; i < n - 1; i++) {
      var h = (pts[i + 1][0] - pts[i][0]) / 3;
      d += ' C' + (pts[i][0] + h).toFixed(1) + ' ' + (pts[i][1] + t[i] * h).toFixed(1) + ' ' +
        (pts[i + 1][0] - h).toFixed(1) + ' ' + (pts[i + 1][1] - t[i + 1] * h).toFixed(1) + ' ' +
        pts[i + 1][0].toFixed(1) + ' ' + pts[i + 1][1].toFixed(1);
    }
    return d;
  }
  function draw(svg, period, s) {
    var p = DATA[period], L = 36, R = 336, T = 14, B = 134;
    var max = Math.max.apply(null, p.all);
    var step = max <= 180 ? 60 : 360;
    var ymax = Math.max(step * 2, Math.ceil(max / step) * step);
    var x = function (i) { return L + (R - L) * i / (p.n - 1); };
    var y = function (v) { return B - (B - T) * v / ymax; };
    var v, i, last = s.length - 1;
    while (svg.firstChild) svg.removeChild(svg.firstChild);

    for (v = 0; v <= ymax; v += step) {
      svg.appendChild(node('line', { 'class': 'gl', x1: L, x2: R, y1: y(v), y2: y(v) }));
      svg.appendChild(node('text', { x: L - 8, y: y(v) + 4, 'text-anchor': 'end' }, v ? (v / 60) + 'h' : '0'));
    }
    var steady = false, on = s.filter(function (q) { return q > 0; });
    if (on.length >= 3) {
      var mean = sum(on) / on.length, top = Math.min(ymax, mean * 1.35), low = mean * 0.65;
      svg.appendChild(node('rect', { 'class': 'band', x: L, width: R - L, y: y(top), height: y(low) - y(top) }));
      svg.appendChild(node('text', { 'class': 'steady', x: L + 2, y: y(top) - 5 }, 'STEADY'));
      steady = true;
    }
    var pts = s.map(function (q, k) { return [x(k), y(q)]; });
    var path = smooth(pts);
    if (path) {
      svg.appendChild(node('path', { 'class': 'ar', d: path + ' L' + pts[last][0].toFixed(1) + ' ' + B + ' L' + pts[0][0].toFixed(1) + ' ' + B + ' Z' }));
      svg.appendChild(node('path', { 'class': 'ln', d: path }));
    }
    for (i = 0; i < p.n; i++) {
      var lab = p.ticks[i];
      if (lab == null) continue;
      svg.appendChild(node('text', { 'class': i === last ? 'on' : '', x: x(i), y: B + 22, 'text-anchor': 'middle' }, lab));
    }
    /* today: the one orange mark, with its value */
    var tx = pts[last][0], ty = pts[last][1];
    svg.appendChild(node('circle', { 'class': 'now', cx: tx, cy: ty, r: 5 }));
    var anchor = tx > R - 46 ? 'end' : tx < L + 30 ? 'start' : 'middle';
    var lx = anchor === 'end' ? tx + 4 : anchor === 'start' ? tx - 4 : tx;
    svg.appendChild(node('text', { 'class': 'val', x: lx, y: Math.max(T - 2, ty - 12), 'text-anchor': anchor }, plain(s[last])));
    svg.setAttribute('aria-label', 'Focus time, ' + p.label + '. ' + plain(sum(s)) + ' in total.');
    return steady;
  }

  /* ---------- everything on the pane that depends on the subject and the period ---------- */
  function render(root) {
    var st = state.get(root), pane = one(root, '[data-c="pane"]'), p = DATA[st.period];
    if (!pane) return;
    var s = series(st.period, st.subject), total = sum(s);
    var sessions = sessionsFor(st.period, st.subject, s);
    var active = s.filter(function (v) { return v > 0; }).length;
    var set = function (key, html) { all(pane, '[data-c="' + key + '"]').forEach(function (n) { n.innerHTML = html; }); };
    set('ctx', p.label + ' · ' + st.subject.replace('&', '&amp;'));
    set('unit', p.unit);
    set('time', hm(total));
    set('timenote', total
      ? sessions + (sessions === 1 ? ' session' : ' sessions') + ' across ' + active + ' active ' + p.slot + (active === 1 ? '' : 's')
      : 'No study time recorded ' + p.word);
    set('s1', String(sessions));
    set('s2', String(active));
    set('s2l', p.active);
    set('s3', hm(Math.max.apply(null, s), true));
    set('s3l', p.best);
    var svg = one(pane, '[data-c="chart"]');
    if (svg) {
      var steady = draw(svg, st.period, s);
      var note = one(pane, '[data-c="steadynote"]');
      if (note) {
        note.classList.toggle('c-progress-off', !steady);
        note.textContent = 'The green band is your steady range. Most ' + p.slot + 's land inside it.';
      }
    }
    var bars = one(pane, '[data-c="bars"]');
    if (bars) {
      var rows = SUBJECTS.map(function (name) { return { name: name, v: sum(series(st.period, name)) }; })
        .sort(function (a, b) { return b.v - a.v; });
      var top = rows[0].v || 1, allTotal = sum(p.all);
      bars.innerHTML = rows.filter(function (r) { return r.v > 0; }).map(function (r) {
        var dim = st.subject !== 'All subjects' && st.subject !== r.name;
        return '<div class="c-progress-brow' + (dim ? ' dim' : '') + '"><span class="t-h3">' + r.name.replace('&', '&amp;') +
          '</span><span class="t-read">' + plain(r.v) + '</span><div class="c-progress-track"><i style="width:' +
          Math.max(3, Math.round(100 * r.v / top)) + '%"></i></div></div>';
      }).join('');
      set('subnote', (allTotal <= 180 ? allTotal + ' focused minutes' : plain(allTotal) + ' of focus') + ', shared across your subjects.');
      var none = rows.filter(function (r) { return !r.v; }).map(function (r) { return r.name; }).sort();
      var nn = one(pane, '[data-c="none"]');
      if (nn) { nn.classList.toggle('c-progress-off', !none.length); nn.textContent = 'No time yet ' + p.word + ': ' + none.join(', ') + '.'; }
    }
  }

  function syncFilters(root) {
    var st = state.get(root);
    all(root, '[data-c="subject"]').forEach(function (n) { n.textContent = st.subject; });
    all(root, '[data-subject]').forEach(function (b) { b.setAttribute('aria-checked', String(b.getAttribute('data-subject') === st.subject)); });
    all(root, '[data-period]').forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-period') === st.period)); });
  }

  function show(root, sec, how) {
    var st = state.get(root), i = SECS.indexOf(sec);
    st.sec = sec;
    all(root, '[data-c="sec"]').forEach(function (n) { n.textContent = NAMES[sec]; });
    all(root, '[data-c="pos"]').forEach(function (n) { n.textContent = String(i + 1); });
    all(root, '[data-sec]').forEach(function (b) {
      var on = String(b.getAttribute('data-sec') === sec);
      b.setAttribute(b.getAttribute('role') === 'tab' ? 'aria-selected' : 'aria-checked', on);
    });
    var filters = one(root, '[data-c="filters"]');
    if (filters) filters.classList.toggle('c-progress-off', sec === 'milestones');   /* milestones are not filtered */
    var pane = one(root, '[data-c="pane"]');
    var t = document.getElementById('c-progress-p-' + sec);
    pane.textContent = '';
    if (t && t.content) pane.appendChild(t.content.cloneNode(true));
    all(pane, '[data-cp-use]').forEach(stamp);
    render(root);
    if (!how) return;
    pane.classList.remove('c-progress-in');
    void pane.offsetWidth;
    pane.classList.add('c-progress-in');
    /* bring the chosen name into view, and start the new part from its top */
    var tab = one(root, '.c-progress-tabs [aria-selected="true"]');
    if (tab) {
      var tray = tab.parentNode;
      tray.scrollLeft += tab.getBoundingClientRect().left - tray.getBoundingClientRect().left -
        (tray.getBoundingClientRect().width - tab.getBoundingClientRect().width) / 2;
    }
    var page = one(root, '[data-c="page"]');
    if (page) { var limit = pinAt(page); if (page.scrollTop > limit) page.scrollTop = limit; }
  }
  /* how far the page scrolls before the bar of five reaches the top bar (0 when there is no such bar) */
  function pinAt(page) {
    var nav = one(page, '.nav'), large = one(page, '.large');
    if (!one(page, '[data-c="stick"]') || !nav || !large) return 0;
    return Math.max(0, large.offsetTop + large.offsetHeight - nav.offsetHeight);
  }

  function closeMenus(root, except) {
    all(root, '.c-progress-mw[data-open="true"]').forEach(function (mw) {
      if (mw === except) return;
      mw.removeAttribute('data-open');
      one(mw, '.menu-btn').setAttribute('aria-expanded', 'false');
    });
  }
  function openMenu(root, mw) {
    closeMenus(root, mw);
    mw.setAttribute('data-open', 'true');
    one(mw, '.menu-btn').setAttribute('aria-expanded', 'true');
  }

  /* C: the index pushes a page; Back pops it */
  function push(root, sec) {
    var index = one(root, '[data-c="index"]'), detail = one(root, '[data-c="detail"]');
    show(root, sec, false);
    index.classList.add('c-progress-off');
    detail.classList.remove('c-progress-off', 'c-progress-push');
    detail.scrollTop = 0;
    void detail.offsetWidth;
    detail.classList.add('c-progress-push');
  }
  function pop(root) {
    var index = one(root, '[data-c="index"]'), detail = one(root, '[data-c="detail"]');
    closeMenus(root);
    detail.classList.add('c-progress-off');
    index.classList.remove('c-progress-off', 'c-progress-pop');
    void index.offsetWidth;
    index.classList.add('c-progress-pop');
  }

  function onClick(e) {
    var root = e.currentTarget, st = state.get(root), t = e.target, hit;
    if ((hit = t.closest('.c-progress-mw > .menu-btn'))) {
      var mw = hit.parentNode;
      if (mw.getAttribute('data-open') === 'true') closeMenus(root); else openMenu(root, mw);
      return;
    }
    if ((hit = t.closest('.c-progress-mw .menu button'))) {
      if (hit.hasAttribute('data-sec')) show(root, hit.getAttribute('data-sec'), true);
      if (hit.hasAttribute('data-subject')) { st.subject = hit.getAttribute('data-subject'); syncFilters(root); render(root); }
      closeMenus(root);
      return;
    }
    closeMenus(root);                                   /* a tap anywhere else puts the menu away */
    if ((hit = t.closest('[role="tab"][data-sec]'))) { show(root, hit.getAttribute('data-sec'), true); return; }
    if ((hit = t.closest('[data-period]'))) { st.period = hit.getAttribute('data-period'); syncFilters(root); render(root); return; }
    if ((hit = t.closest('[data-goto]'))) { push(root, hit.getAttribute('data-goto')); return; }
    if (t.closest('[data-back]')) pop(root);
  }

  Array.prototype.forEach.call(hosts, function (root) {
    var kind = root.getAttribute('data-c-progress');
    root.setAttribute('data-cp-use', 'c-progress-f-' + kind);
    stamp(root);
    state.set(root, { sec: 'overview', subject: 'All subjects', period: 'week' });
    root.addEventListener('click', onClick);
    root.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenus(root); });
    var page = one(root, '[data-c="page"]'), stick = one(root, '[data-c="stick"]');
    if (page && stick) page.addEventListener('scroll', function () {
      stick.classList.toggle('stuck', page.scrollTop > pinAt(page));
    }, { passive: true });
    if (kind === 'c') { state.get(root).sec = 'study'; show(root, 'study', false); }
    else show(root, 'overview', false);
    var open = root.getAttribute('data-open');
    if (open) { var mw = one(root, '.c-progress-mw[data-menu="' + open + '"]'); if (mw) openMenu(root, mw); }
  });

  /* the ladder prints the kit's own values, so the chart cannot drift from the system */
  function hex(v) {
    v = (v || '').trim();
    var m = v.match(/^rgba?\((\d+)[,\s]+(\d+)[,\s]+(\d+)/);
    if (!m) return v;
    return '#' + [m[1], m[2], m[3]].map(function (q) { return ('0' + parseInt(q, 10).toString(16)).slice(-2); }).join('');
  }
  all(document, '#c-progress-dark .c-progress-ladder').forEach(function (panel) {
    var cs = getComputedStyle(panel);
    all(panel, '[data-var]').forEach(function (n) {
      var v = hex(cs.getPropertyValue(n.getAttribute('data-var')));
      if (v) n.textContent = v;
    });
  });
})();

/* ==== c-study.js ==== */
/* c-study: study set-up (issue 6), timer marks (issue 7), pause screen (issue 2).
   Listeners are attached to the artboards themselves, so they keep working when a phone is moved into
   the full-screen try-out. Timers start on a tap and stop when their room leaves the screen. */
(function () {
  var SPEED = 20;                       /* demo speed for the running rooms */
  var FACE = { Mathematics: 'mathematics.png', Irish: 'irish-v3.png', Accounting: 'accounting.png', Biology: 'biology.png', English: 'english.png' };
  var METHOD = { 'new-learning': 'New Learning', practice: 'Practice', revision: 'Revision' };
  var uid = 0;
  var rooms = [];

  function one(root, sel) { return root.querySelector(sel); }
  function all(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function stamp(host, id, before) {
    var t = document.getElementById(id);
    if (t && t.content) host.insertBefore(t.content.cloneNode(true), before || null);
  }
  function mmss(s) {
    s = Math.max(0, Math.round(s));
    var m = Math.floor(s / 60), r = s % 60;
    return (m < 10 ? '0' : '') + m + ':' + (r < 10 ? '0' : '') + r;
  }
  function text(el, v) { if (el && el.textContent !== v) el.textContent = v; }

  /* ---------------- the marks ---------------- */

  /* rule: n intervals at a fixed pitch; ticks from..to are inked, the orange tick sits at `from` */
  function rule(host, o) {
    host.classList.add('c-study-rule', 'is-' + o.size);
    host.style.width = (o.n * o.pitch) + 'px';
    var ticks = [], lastFrom = -1, lastTo = -1;
    for (var i = 0; i <= o.n; i++) {
      var t = document.createElement('i');
      t.style.left = (i * o.pitch).toFixed(2) + 'px';
      if (i % o.major === 0) t.className = 'm5';
      else if (o.mid && i % o.mid !== 0) t.className = 'half';
      host.appendChild(t); ticks.push(t);
    }
    var now = document.createElement('b');
    host.appendChild(now);
    return {
      set: function (from, to) {
        var f = Math.ceil(from - 1e-6);
        if (f !== lastFrom || to !== lastTo) {
          for (var i = 0; i < ticks.length; i++) ticks[i].classList.toggle('ink', i >= f && i <= to);
          lastFrom = f; lastTo = to;
        }
        now.style.transform = 'translateX(' + (Math.min(from, o.n) * o.pitch).toFixed(2) + 'px)';
      }
    };
  }

  /* dial: ring, wedge for a share of an hour, orange hand at the wedge's moving edge when live */
  function dial(host, size) {
    var k = 32 / size, sw = 1.5 * k, rr = 16 - sw / 2 - 0.25 * k, rw = rr - sw / 2 - (size > 22 ? 2.5 : 2) * k;
    host.innerHTML = '<svg class="c-study-dial" width="' + size + '" height="' + size + '" viewBox="0 0 32 32" aria-hidden="true">' +
      '<circle class="ring" cx="16" cy="16" r="' + rr.toFixed(2) + '" stroke-width="' + sw.toFixed(2) + '"/><path class="wedge" d=""/>' +
      '<line class="hand" x1="16" y1="16" x2="16" y2="16" stroke-width="' + (1.75 * k).toFixed(2) + '"/></svg>';
    var wedge = one(host, '.wedge'), hand = one(host, '.hand');
    return {
      set: function (share, live) {
        share = Math.max(0, Math.min(1, share));
        var a = share * Math.PI * 2, x = 16 + rw * Math.sin(a), y = 16 - rw * Math.cos(a);
        var d = '';
        if (share >= 0.999) d = 'M16 ' + (16 - rw) + 'a' + rw + ' ' + rw + ' 0 1 1 0 ' + (2 * rw) + 'a' + rw + ' ' + rw + ' 0 1 1 0 ' + (-2 * rw) + 'z';
        else if (share > 0.002) d = 'M16 16L16 ' + (16 - rw).toFixed(2) + 'A' + rw.toFixed(2) + ' ' + rw.toFixed(2) + ' 0 ' + (a > Math.PI ? 1 : 0) + ' 1 ' + x.toFixed(2) + ' ' + y.toFixed(2) + 'Z';
        wedge.setAttribute('d', d);
        if (live) {
          var rh = rr - sw / 2;
          hand.setAttribute('x2', (16 + rh * Math.sin(a)).toFixed(2));
          hand.setAttribute('y2', (16 - rh * Math.cos(a)).toFixed(2));
          hand.style.display = '';
        } else hand.style.display = 'none';
      }
    };
  }

  /* star: the crew's five-point star; the orange fill is clipped from the top as time passes */
  function starPoints(cx, cy, R, r) {
    var p = [];
    for (var i = 0; i < 10; i++) {
      var a = -Math.PI / 2 + i * Math.PI / 5, q = i % 2 ? r : R;
      p.push((cx + q * Math.cos(a)).toFixed(2) + ',' + (cy + q * Math.sin(a)).toFixed(2));
    }
    return p.join(' ');
  }
  function star(host, size) {
    var id = 'c-study-clip-' + (++uid), k = 24 / size, pts = starPoints(12, 12.7, 10, 5.2);
    host.innerHTML = '<svg class="c-study-star" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" aria-hidden="true"><defs><clipPath id="' + id + '"><rect x="0" y="0" width="24" height="24"/></clipPath></defs>' +
      '<polygon class="fill" points="' + pts + '" clip-path="url(#' + id + ')"/><polygon class="line" points="' + pts + '" stroke-width="' + (1.6 * k).toFixed(2) + '"/></svg>';
    var rect = one(host, 'rect');
    return {
      set: function (frac) {
        var top = 2.7, bot = 20.8, y = top + (1 - Math.max(0, Math.min(1, frac))) * (bot - top);
        rect.setAttribute('y', y.toFixed(2));
        rect.setAttribute('height', Math.max(0, 24 - y).toFixed(2));
      }
    };
  }

  /* blocks: one per five minutes; passed blocks empty, the current one is orange and drains */
  function blocks(host, n, size) {
    host.classList.add('c-study-blocks', 'is-' + size);
    var arr = [];
    for (var i = 0; i < n; i++) {
      var b = document.createElement('i');
      b.appendChild(document.createElement('b'));
      host.appendChild(b); arr.push(b);
    }
    return {
      set: function (e, live) {
        for (var i = 0; i < n; i++) {
          var gone = live && i < Math.floor(e), now = live && i === Math.floor(e);
          arr[i].classList.toggle('gone', gone);
          arr[i].classList.toggle('now', now);
          if (now) arr[i].firstChild.style.transform = 'scaleX(' + (1 - (e - i)).toFixed(4) + ')';
        }
      }
    };
  }

  /* the static marks on the set-up card and the Home row */
  function drawStatic(host) {
    var kind = host.getAttribute('data-c-study-mark'), size = host.getAttribute('data-size'), len = +host.getAttribute('data-len') || 0;
    if (kind === 'rule' && size === 'card') rule(host, { n: 60, pitch: 5, major: 5, size: 'card' }).set(0, len);
    else if (kind === 'rule') rule(host, { n: 12, pitch: 6, major: 3, size: 'mini' }).set(0, len / 5);
    else if (kind === 'dial') dial(host, +size).set(len / 60, false);
    else if (kind === 'blocks') blocks(host, Math.ceil(len / 5), size).set(0, false);
    else if (kind === 'star') star(host, +size).set(1);
  }

  /* ---------------- the study room ---------------- */

  function Room(host, before, mark) {
    stamp(host, 'c-study-tpl-room', before);
    var page = one(host, '.c-study-room');
    var st = { total: 1500, elapsed: 468, start: 468, up: false, playing: false, done: false };
    var cells = all(page, '.c-study-count span');
    var label = one(page, '[data-s="label"]'), elapsedEl = one(page, '[data-s="elapsed"]'), plannedEl = one(page, '[data-s="planned"]');
    var btn = one(page, '[data-play]'), btnUse = one(btn, 'use'), btnLab = one(btn, 'span');
    var side = one(page, '[data-slot="side"]'), prog = one(page, '[data-slot="prog"]');
    var m = {}, raf = 0, last = 0, api;

    function build() {
      side.innerHTML = ''; prog.innerHTML = ''; prog.className = 'c-study-prog'; prog.removeAttribute('style'); m = {};
      var mins = st.total / 60;
      if (mark === 'rule') {
        var unit = mins <= 30 ? 30 : mins <= 75 ? 60 : 300;                 /* seconds per tick */
        var n = Math.round(st.total / unit);
        m.unit = unit; m.n = n;
        m.rule = rule(prog, { n: n, pitch: 350 / n, major: unit === 30 ? 10 : unit === 60 ? 5 : 3, mid: unit === 30 ? 2 : 0, size: 'room' });
      } else if (mark === 'blocks') {
        m.n = Math.ceil(st.total / 300);
        m.blocks = blocks(prog, m.n, 'room');
      } else {
        prog.innerHTML = '<div class="bar c-study-line"><i></i></div>';
        m.bar = one(prog, 'i');
        if (mark === 'dial') m.dial = dial(side, 28);
        if (mark === 'star') m.star = star(side, 28);
      }
    }

    function render() {
      var remain = Math.max(0, st.total - st.elapsed);
      var shown = st.up ? mmss(Math.floor(st.elapsed)) : mmss(Math.ceil(remain - 1e-6));
      for (var i = 0; i < 5; i++) text(cells[i], shown.charAt(i));
      text(elapsedEl, mmss(Math.floor(st.elapsed)) + ' elapsed');
      text(plannedEl, st.up ? 'Open-ended' : mmss(st.total) + ' planned');
      text(label, st.up ? 'Time studied' : st.done ? 'Time’s up' : 'Time remaining');
      var frac = Math.min(1, st.elapsed / st.total);
      if (m.bar) m.bar.style.width = (frac * 100).toFixed(3) + '%';
      if (m.rule) m.rule.set(Math.min(m.n, st.elapsed / m.unit), m.n);
      if (m.blocks) m.blocks.set(Math.min(m.n, st.elapsed / 300), true);
      if (m.dial) m.dial.set(st.up ? Math.min(1, st.elapsed / 3600) : remain / 3600, true);
      if (m.star) m.star.set(st.up ? 1 : remain / st.total);
    }

    function ui() {
      btnUse.setAttribute('href', st.playing ? '#i-pause' : '#i-play');
      text(btnLab, st.playing ? 'Pause' : st.done ? 'Again' : 'Play');
    }

    function frame(now) {
      if (!st.playing) return;
      var dt = Math.min(0.1, (now - last) / 1000); last = now;
      st.elapsed += dt * SPEED;
      if (!st.up && st.elapsed >= st.total) { st.elapsed = st.total; st.done = true; st.playing = false; }
      if (st.up && st.elapsed >= 5940) { st.elapsed = 5940; st.playing = false; }
      render();
      if (st.playing) raf = requestAnimationFrame(frame); else ui();
    }

    api = {
      play: function () {
        if (st.done) { st.elapsed = st.start; st.done = false; }
        rooms.forEach(function (r) { if (r !== api) r.pause(); });
        st.playing = true; last = performance.now();
        cancelAnimationFrame(raf); raf = requestAnimationFrame(frame);
        render(); ui();
      },
      pause: function () {
        if (!st.playing) return;
        st.playing = false; cancelAnimationFrame(raf); ui();
      },
      /* used by the set-up mock-ups: a fresh session with the student's own choices */
      configure: function (o) {
        api.pause();
        st.up = o.minutes === 'open';
        st.total = st.up ? 3600 : o.minutes * 60;
        st.elapsed = 0; st.start = 0; st.done = false;
        text(one(page, '[data-s="subject"]'), o.subject);
        text(one(page, '[data-s="meta"]'), o.method + ' · ' + (st.up ? 'Open-ended' : o.minutes + ' min'));
        build(); render(); ui();
      },
      extra: one(page, '[data-slot="extra"]'),
      page: page
    };

    btn.addEventListener('click', function () { if (st.playing) api.pause(); else api.play(); });
    if (window.IntersectionObserver) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { if (!e.isIntersecting) api.pause(); }); }).observe(page);
    }
    build(); render(); ui();
    rooms.push(api);
    return api;
  }

  /* ---------------- theme lock: the study room is dark in both themes ---------------- */

  var mo = window.MutationObserver ? new MutationObserver(function (list) {
    list.forEach(function (r) {
      var s = r.target, lock = s.getAttribute('data-c-study-lock'), cur = s.getAttribute('data-theme');
      if (lock && cur !== lock) { s._csWant = cur; s.setAttribute('data-theme', lock); }
    });
  }) : null;
  function lock(scr, theme) {
    scr._csWant = scr.getAttribute('data-theme');
    scr.setAttribute('data-c-study-lock', theme);
    scr.setAttribute('data-theme', theme);
  }
  function unlock(scr) {
    scr.removeAttribute('data-c-study-lock');
    scr.setAttribute('data-theme', scr._csWant || 'light');
  }

  /* ---------------- set-up mock-ups (issue 6) ---------------- */

  function Setup(scr) {
    var kind = scr.getAttribute('data-c-study-setup');
    var ORDER = ['subject', 'method', 'time'];
    var WORD = { subject: 'your subject', method: 'how you’ll work', time: 'your time' };
    var ASK = { subject: 'Choose your subject', method: 'Choose how you’ll work', time: 'Set your time' };
    var STEPNEED = { subject: 'Choose your subject to continue.', method: 'Choose how you’ll work to continue.', time: 'Set your time to start.' };
    var HELP = 'Choose a preset or enter 5–180 minutes.';
    var st, step = 0, sheet = null, timers = [];

    all(scr, '[data-fill]').forEach(function (h) { stamp(h, 'c-study-tpl-' + h.getAttribute('data-fill')); });
    var page = one(scr, '.c-study-page'), need = one(scr, '[data-need]'), main = one(scr, '[data-main]'), mainLab = one(scr, '[data-main-label]');
    var scrim = one(scr, '.c-study-scrim'), face = one(scr, '.c-study-face'), started = one(scr, '[data-started]');
    var back = one(scr, '[data-back]'), count = one(scr, '[data-count]'), stepbar = one(scr, '[data-stepbar]');
    var room = Room(started, null, 'rule');
    room.extra.innerHTML = '<button class="link quiet" data-reset>Set up again</button>';

    function later(fn, ms) { timers.push(setTimeout(fn, ms)); }
    function missing() { return ORDER.filter(function (k) { return !st[k]; }); }
    function value(k) { return k === 'subject' ? st.subject : k === 'method' ? METHOD[st.method] : st.time === 'open' ? 'Open-ended' : st.time + ' min'; }

    function sync() {
      all(scr, '[data-group]').forEach(function (g) {
        var k = g.getAttribute('data-group');
        all(g, '[data-pick]').forEach(function (c) { c.setAttribute('aria-pressed', String(st[k]) === c.getAttribute('data-pick') ? 'true' : 'false'); });
        if (k === 'time') {
          var custom = typeof st.time === 'number' && st.time > 0 && [15, 25, 45].indexOf(st.time) < 0;
          var field = one(g, '.c-study-field'), input = one(g, 'input'), help = one(g, '[data-timehelp]');
          field.classList.toggle('is-set', custom);
          if (!custom && document.activeElement !== input) input.value = '';
          if (custom) input.value = st.time;
          if (!help.hasAttribute('data-err')) text(help, st.time === 'open' ? 'The clock counts up. Finish whenever you’re done, after 5 minutes or more.' : HELP);
        }
      });
      all(scr, '[data-val]').forEach(function (v) {
        var k = v.getAttribute('data-val');
        text(v, st[k] ? value(k) : 'Choose'); v.classList.toggle('is-set', !!st[k]);
      });
      if (face) {
        if (st.subject) { face.src = 'assets/crew/' + FACE[st.subject]; face.classList.add('is-on'); }
        else face.classList.remove('is-on');
      }
      var miss = missing(), list = miss.map(function (k) { return WORD[k]; }).join(', ');
      if (kind === 'a') {
        text(need, miss.length ? miss.length + (miss.length === 1 ? ' thing' : ' things') + ' left: ' + list : 'Ready');
        need.classList.toggle('is-clear', !miss.length);
        main.className = 'btn ' + (miss.length ? 'primary' : 'go') + ' lg block split';
        text(mainLab, miss.length ? ASK[miss[0]] : 'Start session');
      } else if (kind === 'b') {
        text(need, 'Still to choose: ' + list + '.');
        need.classList.toggle('c-study-hide', !miss.length);
        if (miss.length) main.setAttribute('aria-disabled', 'true'); else main.removeAttribute('aria-disabled');
      } else {
        var k = ORDER[step], ok = !!st[k];
        text(need, STEPNEED[k]);
        need.classList.toggle('c-study-hide', ok);
        main.className = 'btn ' + (step === 2 ? 'go' : 'primary') + ' lg block split';
        text(mainLab, step === 2 ? 'Start session' : 'Continue');
        if (ok) main.removeAttribute('aria-disabled'); else main.setAttribute('aria-disabled', 'true');
        back.parentNode.classList.toggle('is-first', step === 0);
        text(count, '0' + (step + 1) + ' / 03');
        all(stepbar, 'i').forEach(function (i, n) { i.className = n < step ? 'on' : n === step ? 'now' : ''; });
      }
    }

    function go(n, dir) {
      step = n;
      all(scr, '.c-study-step').forEach(function (s, i) {
        s.classList.remove('is-fwd', 'is-back');
        s.classList.toggle('is-on', i === n);
        if (i === n) { void s.offsetWidth; s.classList.add(dir === 'back' ? 'is-back' : 'is-fwd'); }
      });
      page.scrollTop = 0;
      sync();
    }

    function openSheet(k) {
      closeSheet();
      sheet = one(scr, '[data-sheet="' + k + '"]');
      if (!sheet) return;
      sheet.classList.add('is-on'); scrim.classList.add('is-on');
    }
    function closeSheet() {
      if (sheet) sheet.classList.remove('is-on');
      if (scrim) scrim.classList.remove('is-on');
      sheet = null;
    }

    /* scroll to the missing control and draw one ink outline round it */
    function nudge(k) {
      var g = one(page, (kind === 'c' ? '.c-study-step.is-on ' : '') + '[data-group="' + k + '"]');
      if (!g) return;
      var sec = g.closest('.sec') || g, nav = one(page, '.nav');
      var top = Math.max(0, Math.min(sec.offsetTop - nav.offsetHeight - 12, page.scrollHeight - page.clientHeight));
      var far = Math.abs(page.scrollTop - top) > 6;
      if (far) { if (page.scrollTo) page.scrollTo({ top: top, behavior: 'smooth' }); else page.scrollTop = top; }
      later(function () {
        g.classList.remove('is-nudged'); void g.offsetWidth; g.classList.add('is-nudged');
        later(function () { g.classList.remove('is-nudged'); }, 1600);
      }, far ? 380 : 0);
    }

    function setCustom(g) {
      var input = one(g, 'input'), help = one(g, '[data-timehelp]'), n = parseInt(input.value, 10);
      help.removeAttribute('data-err');
      if (!n || n < 5) { help.setAttribute('data-err', ''); text(help, 'Minimum 5 minutes'); input.focus(); return false; }
      if (n > 180) { help.setAttribute('data-err', ''); text(help, '180 minutes is the longest session'); input.focus(); return false; }
      st.time = n; input.blur();
      return true;
    }

    function start() {
      closeSheet();
      room.configure({ subject: st.subject, method: METHOD[st.method], minutes: st.time });
      lock(scr, 'dark');
      started.classList.add('is-on');
      room.play();
    }

    function reset() {
      timers.forEach(clearTimeout); timers = [];
      room.pause();
      if (started.classList.contains('is-on')) { started.classList.remove('is-on'); unlock(scr); }
      closeSheet();
      st = { subject: '', method: '', time: 0 };
      all(scr, '[data-timehelp]').forEach(function (h) { h.removeAttribute('data-err'); });
      all(scr, '.c-study-group input').forEach(function (i) { i.value = ''; });
      if (kind === 'c') go(0, 'back'); else sync();
      page.scrollTop = 0;
    }

    scr.addEventListener('click', function (e) {
      var t = e.target, el;
      if ((el = t.closest('[data-pick]'))) {
        var g = el.closest('[data-group]'), k = g.getAttribute('data-group'), v = el.getAttribute('data-pick');
        st[k] = k === 'time' && v !== 'open' ? +v : v;
        if (k === 'time') one(g, '[data-timehelp]').removeAttribute('data-err');
        sync();
        if (kind === 'a') later(closeSheet, 340);      /* let the tile fill and its tick draw, then leave */
        return;
      }
      if ((el = t.closest('[data-custom]'))) {
        if (setCustom(el.closest('[data-group]'))) { sync(); if (kind === 'a') later(closeSheet, 260); }
        return;
      }
      if ((el = t.closest('[data-open]'))) { openSheet(el.getAttribute('data-open')); return; }
      if (t.closest('[data-close]')) { closeSheet(); return; }
      if ((el = t.closest('[data-switch]'))) {
        var on = el.getAttribute('aria-checked') !== 'true';
        el.setAttribute('aria-checked', on ? 'true' : 'false');
        one(el, '.switch').classList.toggle('on', on);
        return;
      }
      if (t.closest('[data-reset]')) { reset(); return; }
      if (t.closest('[data-back]')) { if (step > 0) go(step - 1, 'back'); return; }
      if (t.closest('[data-main]')) {
        var miss = missing();
        if (kind === 'a') { if (miss.length) openSheet(miss[0]); else start(); }
        else if (kind === 'b') { if (miss.length) nudge(miss[0]); else start(); }
        else {
          var cur = ORDER[step];
          if (!st[cur]) nudge(cur); else if (step < 2) go(step + 1, 'fwd'); else start();
        }
      }
    });
    scr.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.matches && e.target.matches('.c-study-field input')) {
        var g = e.target.closest('[data-group]');
        if (setCustom(g)) { sync(); if (kind === 'a') later(closeSheet, 260); }
      }
    });

    st = { subject: '', method: '', time: 0 };
    sync();
  }

  /* ---------------- pause screen (issue 2) ---------------- */

  function Pause(scr) {
    var scrim = one(scr, '.c-study-scrim'), sheet = one(scr, '.c-study-sheet'), toast = one(scr, '[data-toast]'), tid = 0;
    function open(on) { sheet.classList.toggle('is-on', on); scrim.classList.toggle('is-on', on); }
    function say(msg) {
      toast.textContent = msg; toast.classList.add('is-on');
      clearTimeout(tid); tid = setTimeout(function () { toast.classList.remove('is-on'); }, 2400);
    }
    scr.addEventListener('click', function (e) {
      var t = e.target;
      if (t.closest('[data-finish]')) open(true);
      else if (t.closest('[data-keep]')) open(false);
      else if (t.closest('[data-end]')) { open(false); say('17 min kept. On to your debrief.'); }
      else if (t.closest('[data-discard]')) { open(false); say('Session discarded. Nothing was saved.'); }
      else if (t.closest('[data-resume]')) say('Back in the study room. Timer running.');
      else if (t.closest('[data-breathe]')) say('The breathing guide opens here.');
    });
  }

  /* ---------------- start-up ---------------- */

  function init() {
    var secs = ['c-study-start', 'c-study-timer', 'c-study-pause'].map(function (id) { return document.getElementById(id); }).filter(Boolean);
    if (!secs.length) return;
    secs.forEach(function (sec) {
      all(sec, '[data-c-study-mark]').forEach(drawStatic);
      all(sec, '[data-c-study-room]').forEach(function (scr) { Room(scr, one(scr, '.hb'), scr.getAttribute('data-c-study-room')); });
      all(sec, '[data-c-study-setup]').forEach(Setup);
      all(sec, '[data-c-study-pause]').forEach(Pause);
      all(sec, '.scr.dc').forEach(function (scr) {
        var l = scr.getAttribute('data-c-study-lock');
        if (l) scr.setAttribute('data-theme', l);
        if (mo) mo.observe(scr, { attributes: true, attributeFilter: ['data-theme'] });
        /* the sound button works because the bar holds it below the status band */
        scr.addEventListener('click', function (e) {
          var b = e.target.closest('[data-sound]');
          if (!b) return;
          var off = b.getAttribute('aria-label') === 'Sound on';
          b.setAttribute('aria-label', off ? 'Sound off' : 'Sound on');
          one(b, 'use').setAttribute('href', off ? '#i-mute' : '#i-sound');
        });
      });
      /* status-band annotation switch (pause section) */
      var seg = one(sec, '[data-c-study-bandseg]');
      if (seg) seg.addEventListener('click', function (e) {
        var b = e.target.closest('[data-c-study-band]');
        if (!b) return;
        var on = b.getAttribute('data-c-study-band') === 'on';
        all(seg, 'button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        one(sec, '.rail').classList.toggle('is-band', on);
      });
    });
    document.addEventListener('visibilitychange', function () { if (document.hidden) rooms.forEach(function (r) { r.pause(); }); });
    if (window.NSU && window.NSU.fitAll) window.NSU.fitAll();
  }

  /* app.js is bundled after this file; wait for it so the page's own set-up has run */
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

/* ==== c-world.js ==== */
/* c-world: the Journey map sheet (rest / pulled up), the island welcome sheet, the three steps, the note.
   Listeners sit on elements inside each artboard, so they keep working when the artboard is moved
   into the full-screen try-out. Nothing runs until a control is touched. */
(function () {
  function ready(fn) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn); else fn(); }
  function each(root, sel, fn) { Array.prototype.forEach.call(root.querySelectorAll(sel), fn); }

  /* Drag a sheet by its handle. It follows the finger one for one, clamped to [min, max] px of travel,
     then hands the result to done(). Artboards are scaled on the page, so travel is measured in the
     artboard's own pixels. A press that barely moves is left to the handle's click. */
  function drag(handle, sheet, range, from, done) {
    var id = null, y0 = 0, base = 0, scale = 1, far = 0, lastY = 0, lastT = 0, vel = 0;
    handle.addEventListener('pointerdown', function (e) {
      if (e.button) return;
      var b = e.target.closest('button');
      if (b && b !== handle) return;                       /* a button inside the handle keeps its own tap */
      id = e.pointerId; y0 = lastY = e.clientY; lastT = e.timeStamp; far = 0; vel = 0;
      scale = (sheet.getBoundingClientRect().width / sheet.offsetWidth) || 1;
      base = from();
      try { handle.setPointerCapture(id); } catch (err) { /* older browsers: the drag still tracks on the handle */ }
    });
    handle.addEventListener('pointermove', function (e) {
      if (e.pointerId !== id) return;
      var dy = (e.clientY - y0) / scale;
      far = Math.max(far, Math.abs(dy));
      if (far < 5) return;
      var r = range();
      sheet.classList.add('dragging');
      sheet.style.transform = 'translateY(' + Math.max(r[0], Math.min(r[1], base + dy)) + 'px)';
      var dt = e.timeStamp - lastT;
      if (dt > 0) { vel = (e.clientY - lastY) / scale / dt; lastY = e.clientY; lastT = e.timeStamp; }
    });
    function end(e) {
      if (e.pointerId !== id) return;
      id = null;
      var dragged = far >= 5, r = range();
      if (e.timeStamp - lastT > 90) vel = 0;               /* held still before letting go: not a flick */
      var pos = Math.max(r[0], Math.min(r[1], base + (e.clientY - y0) / scale));
      if (dragged) {
        sheet.getBoundingClientRect();                     /* settle from where the finger left it */
        sheet.classList.remove('dragging');
        sheet.style.transform = '';
      }
      done({ dragged: dragged, pos: pos, vel: vel, max: r[1] });
    }
    handle.addEventListener('pointerup', end);
    handle.addEventListener('pointercancel', end);
  }

  /* C of the Journey bar: a sheet resting above the tab bar */
  function mapSheet(scr) {
    var sheet = scr.querySelector('.c-world-msheet');
    if (!sheet) return;
    var handle = sheet.querySelector('.c-world-drag'), more = sheet.querySelector('.c-world-more'), map = scr.querySelector('.c-world-map');
    var PEEK = 149, quietUntil = 0;
    function travel() { return sheet.offsetHeight - PEEK; }
    function set(state) {
      var open = state === 'open';
      sheet.setAttribute('data-state', open ? 'open' : 'peek');
      handle.setAttribute('aria-expanded', open ? 'true' : 'false');
      handle.setAttribute('aria-label', open ? 'Show less' : 'Show stories, visitors and rewards');
      if (open) more.removeAttribute('inert'); else { more.setAttribute('inert', ''); more.scrollTop = 0; }
    }
    function isOpen() { return sheet.getAttribute('data-state') === 'open'; }
    /* starting position, without the opening movement */
    sheet.classList.add('dragging');
    set(scr.getAttribute('data-cw-msheet') === 'open' ? 'open' : 'peek');
    sheet.getBoundingClientRect();
    sheet.classList.remove('dragging');

    drag(handle, sheet, function () { return [0, travel()]; }, function () { return isOpen() ? 0 : travel(); }, function (o) {
      if (!o.dragged) return;
      quietUntil = Date.now() + 400;                       /* the click that follows a drag is not a tap */
      if (Math.abs(o.vel) > 0.45) set(o.vel < 0 ? 'open' : 'peek');
      else set(o.pos < o.max * (isOpen() ? 0.4 : 0.6) ? 'open' : 'peek');
    });
    handle.addEventListener('click', function () { if (Date.now() < quietUntil) return; set(isOpen() ? 'peek' : 'open'); });
    map.addEventListener('click', function (e) { if (isOpen() && !e.target.closest('button')) set('peek'); });
  }

  /* A of the welcome: a bottom sheet that closes by Close, the main button, a tap outside, or a swipe down */
  function welcome(scr) {
    var layer = scr.querySelector('.c-world-layer');
    if (!layer) return;
    var sheet = layer.querySelector('.sheet'), pull = layer.querySelector('.c-world-pull');
    function set(open) { layer.setAttribute('data-open', open ? 'true' : 'false'); if (open) sheet.removeAttribute('inert'); else sheet.setAttribute('inert', ''); }
    each(layer, '[data-cw-close]', function (b) { b.addEventListener('click', function () { set(false); }); });
    layer.querySelector('.scrim').addEventListener('click', function () { set(false); });
    each(scr, '[data-cw-reopen]', function (b) { b.addEventListener('click', function () { set(true); }); });
    drag(pull, sheet, function () { return [0, sheet.offsetHeight]; }, function () { return 0; }, function (o) {
      if (o.dragged && (o.vel > 0.45 || o.pos > o.max * 0.4)) set(false);
    });
  }

  /* B of the welcome: three steps on a full page */
  function steps(scr) {
    var first = scr.querySelector('.c-world-first');
    if (!first) return;
    var panes = first.querySelectorAll('.c-world-step'), bars = first.querySelectorAll('.steps i');
    var count = first.querySelector('.c-world-count'), next = first.querySelector('[data-cw-next]'), back = first.querySelector('[data-cw-back]'), under = first.querySelector('.c-world-under');
    var at = 0, last = panes.length - 1;
    function show(n, dir) {
      at = n;
      if (dir) first.setAttribute('data-dir', dir); else first.removeAttribute('data-dir');
      Array.prototype.forEach.call(panes, function (p, k) { p.classList.toggle('on', k === n); });
      Array.prototype.forEach.call(bars, function (b, k) { b.className = k < n ? 'on' : k === n ? 'now' : ''; });
      count.textContent = '0' + (n + 1) + ' / 0' + panes.length;
      next.querySelector('span').textContent = n === last ? 'Explore my island' : 'Continue';
      back.hidden = n === 0;
      under.classList.toggle('solo', n === 0);
    }
    function set(open) { first.setAttribute('data-open', open ? 'true' : 'false'); if (open) first.removeAttribute('inert'); else first.setAttribute('inert', ''); }
    next.addEventListener('click', function () { if (at === last) set(false); else show(at + 1, 'fwd'); });
    back.addEventListener('click', function () { if (at > 0) show(at - 1, 'back'); });
    first.querySelector('[data-cw-close]').addEventListener('click', function () { set(false); });
    each(scr, '[data-cw-reopen]', function (b) { b.addEventListener('click', function () { show(0, null); set(true); }); });
  }

  /* C of the welcome: a note that folds away */
  function note(scr) {
    var n = scr.querySelector('.c-world-note');
    if (!n) return;
    function set(open) { n.setAttribute('data-open', open ? 'true' : 'false'); if (open) n.removeAttribute('inert'); else n.setAttribute('inert', ''); }
    n.querySelector('[data-cw-close]').addEventListener('click', function () { set(false); });
    each(scr, '[data-cw-reopen]', function (b) { b.addEventListener('click', function () { set(n.getAttribute('data-open') === 'false'); }); });
  }

  ready(function () {
    ['c-world-journeybar', 'c-world-island'].forEach(function (id) {
      var root = document.getElementById(id);
      if (!root) return;
      each(root, '[data-cw-msheet]', mapSheet);
      each(root, '[data-cw-welcome]', welcome);
      each(root, '[data-cw-steps]', steps);
      each(root, '[data-cw-note]', note);
    });
  });
})();

/* ==== system.js ==== */
/* system: "The system" view. Every example on it is live.
   One delegated click listener on #view-system does the work. Movement is carried by CSS transitions;
   the only timers are the three in the loading example, and they start from a tap. */
(function () {
  var root = document.getElementById('view-system');
  if (!root) return;

  function each(list, fn) { Array.prototype.forEach.call(list, fn); }
  function q(sel, el) { return (el || root).querySelector(sel); }
  function qa(sel, el) { return (el || root).querySelectorAll(sel); }
  function pressed(el, on) { el.setAttribute('aria-pressed', on ? 'true' : 'false'); }

  /* iOS only shows a pressed state when something is listening for touches */
  root.addEventListener('touchstart', function () {}, { passive: true });

  /* the Light / Dark switch rests just under the page's own sticky bar */
  var bar = q('.sys-bar'), views = document.querySelector('.views');
  if (bar && views && views.offsetHeight) bar.style.setProperty('--sys-top', views.offsetHeight + 'px');

  /* the colour section's two sheets stay light and dark whatever the switch says */
  if (window.MutationObserver) {
    each(qa('[data-sys-fixed]'), function (el) {
      var want = el.getAttribute('data-sys-fixed');
      new MutationObserver(function () {
        if (el.getAttribute('data-theme') !== want) el.setAttribute('data-theme', want);
      }).observe(el, { attributes: true, attributeFilter: ['data-theme'] });
    });
  }

  /* the icon set, read from the page's sprite so it is always the set in use */
  var grid = q('[data-sys-icons]');
  if (grid) {
    each(document.querySelectorAll('svg symbol[id^="i-"]'), function (sym) {
      var cell = document.createElement('span');
      cell.innerHTML = '<svg class="ic"><use href="#' + sym.id + '"/></svg>';
      grid.appendChild(cell);
    });
  }

  /* ---------- choices ---------- */
  function pickOne(tile) {
    var group = tile.closest('[data-sys-one]');
    each(group.querySelectorAll('.choice'), function (t) { pressed(t, t === tile); });
    var say = group.getAttribute('data-sys-say');
    var out = say && q('[data-sys-said]', tile.closest('.scr'));
    if (out) out.textContent = say.replace('{v}', tile.getAttribute('data-v'));
  }
  function pickMany(tile) {
    var group = tile.closest('[data-sys-many]');
    var on = tile.getAttribute('aria-pressed') !== 'true';
    pressed(tile, on);
    var word = q('[data-sys-word]', tile);
    if (word) word.textContent = on ? 'Added' : 'Add';
    var count = q('[data-sys-count]', group.closest('.scr'));
    if (count) count.textContent = group.querySelectorAll('.choice[aria-pressed="true"]').length + ' of ' + group.querySelectorAll('.choice').length + ' chosen';
  }

  /* ---------- the selection bar: move the pill, swap what is under it at once ---------- */
  function slide(btn) {
    var seg = btn.closest('.sys-seg');
    each(seg.querySelectorAll('button'), function (b, n) {
      var on = b === btn;
      b.setAttribute('aria-selected', on ? 'true' : 'false');
      if (on) seg.style.setProperty('--i', n);
    });
    var out = q('[data-sys-seg-out]', seg.parentNode);
    if (out && btn.getAttribute('data-out')) out.textContent = btn.getAttribute('data-out');
  }

  /* ---------- menus: choosing applies at once and closes ---------- */
  function setMenu(host, open) {
    host.classList.toggle('open', open);
    var b = q('.menu-btn', host);
    if (b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function choose(item) {
    var host = item.closest('[data-sys-menu]');
    each(host.querySelectorAll('.menu button'), function (b) { b.setAttribute('aria-checked', b === item ? 'true' : 'false'); });
    var val = q('[data-sys-val]', host);
    if (val) val.textContent = item.textContent.trim();
    setMenu(host, false);
  }

  /* ---------- the main button that says what is missing ---------- */
  var need = q('[data-sys-need]');
  function needState() {
    var s = q('[data-g="subject"] .choice[aria-pressed="true"]', need), t = q('[data-g="time"] .seg button.on', need);
    return { subject: s && s.getAttribute('data-v'), time: t && t.getAttribute('data-v') };
  }
  function paintNeed() {
    var st = needState(), ready = st.subject && st.time;
    var go = q('[data-sys-need-go]', need);
    q('[data-sys-need-say]', need).textContent = ready ? st.subject + ' for ' + st.time + ' minutes.'
      : !st.subject && !st.time ? 'Choose a subject and how long to study.'
      : !st.subject ? 'Choose a subject to start.' : 'Choose how long to study.';
    q('span', go).textContent = ready ? 'Start session' : !st.subject ? 'Choose your subject' : 'Choose your time';
    go.setAttribute('aria-disabled', ready ? 'false' : 'true');
    go.classList.toggle('go', !!ready);
  }
  function nudge(name) {
    var g = q('[data-g="' + name + '"]', need);
    g.classList.remove('is-on');
    void g.offsetWidth;
    g.classList.add('is-on');
  }
  function needClick(t) {
    var tile = t.closest('[data-g="subject"] .choice');
    var time = t.closest('[data-g="time"] .seg button');
    if (tile) each(need.querySelectorAll('[data-g="subject"] .choice'), function (c) { pressed(c, c === tile); });
    else if (time) each(need.querySelectorAll('[data-g="time"] .seg button'), function (b) { b.classList.toggle('on', b === time); });
    else if (t.closest('[data-sys-need-reset]')) {
      each(need.querySelectorAll('.choice'), function (c) { pressed(c, false); });
      each(need.querySelectorAll('.seg button'), function (b) { b.classList.remove('on'); });
    } else if (t.closest('[data-sys-need-go]')) {
      var st = needState();
      if (!st.subject) nudge('subject'); else if (!st.time) nudge('time');
      return;
    } else return;
    paintNeed();
  }

  /* ---------- loading: nothing for 300ms, then the skeleton, then the content ---------- */
  var timers = [];
  function playLoad(btn) {
    var box = q('[data-sys-load]', btn.closest('.scr'));
    timers.forEach(clearTimeout);
    box.setAttribute('data-step', 'blank');
    btn.textContent = 'Loading';
    timers = [
      setTimeout(function () { box.setAttribute('data-step', 'skel'); }, 300),
      setTimeout(function () { box.setAttribute('data-step', 'done'); btn.textContent = 'Play it again'; }, 1700)
    ];
  }

  /* ---------- the sheet that rises ---------- */
  function setSheet(scr, open) {
    scr.classList.toggle('open', open);
    var fig = scr.closest('.shot'), b = fig && q('[data-sys-sheet-toggle]', fig);
    if (b) b.textContent = open ? 'Close the sheet' : 'Open the sheet';
  }

  root.addEventListener('click', function (e) {
    var t = e.target, el;

    if (need && need.contains(t)) { needClick(t); return; }

    /* a menu closes when you tap anywhere else on its own sheet */
    var host = t.closest('[data-sys-menu]'), spec = t.closest('.scr');
    if (spec) each(spec.querySelectorAll('[data-sys-menu].open'), function (h) { if (h !== host) setMenu(h, false); });
    if (host) {
      if ((el = t.closest('.menu button'))) choose(el);
      else if (t.closest('.menu-btn')) setMenu(host, !host.classList.contains('open'));
      return;
    }

    if ((el = t.closest('[data-sys-sheet-toggle]'))) { var live = q('[data-sys-sheet]', el.closest('.shot')); setSheet(live, !live.classList.contains('open')); return; }
    if ((el = t.closest('[data-sys-sheet-close]'))) { setSheet(el.closest('[data-sys-sheet]'), false); return; }

    if ((el = t.closest('[data-sys-one] .choice'))) { pickOne(el); return; }
    if ((el = t.closest('[data-sys-many] .choice'))) { pickMany(el); return; }
    if ((el = t.closest('[data-sys-toggle]'))) { pressed(el, el.getAttribute('aria-pressed') !== 'true'); return; }

    if ((el = t.closest('[data-sys-switch]'))) {
      var sw = q('.switch', el), on = !sw.classList.contains('on');
      sw.classList.toggle('on', on);
      pressed(el, on);
      if (el.hasAttribute('data-sys-slow')) q('#sys-motion').classList.toggle('sys-slow', on);
      return;
    }

    if ((el = t.closest('.sys-seg button'))) { slide(el); return; }
    if ((el = t.closest('[data-sys-load-go]'))) { playLoad(el); return; }
    if ((el = t.closest('[data-sys-err-go]'))) { el.closest('[data-sys-err]').classList.toggle('fixed'); return; }

    if ((el = t.closest('[data-sys-safe-set]'))) {
      each(el.parentNode.querySelectorAll('button'), function (b) { pressed(b, b === el); });
      q('#sys-safe-board').setAttribute('data-sys-safe', el.getAttribute('data-sys-safe-set'));
      return;
    }

    /* in the motion phone, the Subject row opens the sheet */
    if ((el = t.closest('[data-sys-sheet]')) && t.closest('.row') && !t.closest('.sheet')) setSheet(el, true);
  });

  /* text links here are not real links: let the keyboard press them too */
  root.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('a[role="button"]')) { e.preventDefault(); e.target.click(); }
  });
})();

/* ==== app.js ==== */
/* Review page behaviour: hash views, artboard scaling, rails, theme switches, full-screen try-out. */
(function () {
  var VIEWS = ['directions', 'concepts', 'audit', 'system', 'plan'];

  /* stamp screen templates into their artboards: <div class="scr dc" data-use="scr-home"></div> */
  document.querySelectorAll('[data-use]').forEach(function (el) {
    var t = document.getElementById(el.getAttribute('data-use'));
    if (t && t.content) el.appendChild(t.content.cloneNode(true));
  });

  function showView() {
    var h = (location.hash || '').replace('#', '');
    var target = null;
    var name = VIEWS.indexOf(h) >= 0 ? h : null;
    if (!name && h) {
      target = document.getElementById(h);
      var host = target && target.closest('.view');
      if (host) name = host.id.replace('view-', '');
    }
    if (!name) name = VIEWS[0];
    document.querySelectorAll('.view').forEach(function (v) { v.classList.toggle('on', v.id === 'view-' + name); });
    document.querySelectorAll('.tray a').forEach(function (a) {
      a.setAttribute('aria-current', a.getAttribute('href') === '#' + name ? 'true' : 'false');
    });
    fitAll();
    if (target && target.id !== 'view-' + name) { target.scrollIntoView({ block: 'start' }); }
    else if (VIEWS.indexOf(h) >= 0) { window.scrollTo(0, 0); }
  }

  /* scale each 390px (or 1280px) artboard to the width of its slot */
  function fit(slot) {
    var board = slot.querySelector('.phone, .desk');
    if (!board) return;
    var base = board.classList.contains('desk') ? 1280 : 390;
    var pad = slot.classList.contains('bare') || slot.classList.contains('desk-slot') ? 0 : 18;
    var w = slot.clientWidth;
    if (!w) return;
    /* the bezel padding scales with the board, so slot width = (base + pad) * s */
    var s = Math.min(1, w / (base + pad));
    slot.style.setProperty('--s', s.toFixed(4));
    var sizer = slot.querySelector('.phone-sizer, .desk-sizer');
    if (sizer) sizer.style.height = (board.offsetHeight * s) + 'px';
  }
  function fitAll() { document.querySelectorAll('.phone-slot, .desk-slot').forEach(fit); }
  window.addEventListener('resize', fitAll);
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(function (es) { es.forEach(function (e) { var s = e.target.closest('.phone-slot, .desk-slot'); if (s) fit(s); }); });
    document.querySelectorAll('.phone, .desk').forEach(function (b) { ro.observe(b); });
  }

  /* light / dark switch for a group of artboards: <div class="seg" data-theme-for="groupId"> */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-set-theme]');
    if (b) {
      var seg = b.closest('[data-theme-for]');
      var group = document.getElementById(seg.getAttribute('data-theme-for'));
      seg.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      if (group) group.querySelectorAll('.scr:not(.img)').forEach(function (s) { s.setAttribute('data-theme', b.getAttribute('data-set-theme')); });
      return;
    }
    var nav = e.target.closest('[data-rail]');
    if (nav) {
      var rail = document.getElementById(nav.getAttribute('data-rail'));
      if (rail) rail.scrollBy({ left: (nav.getAttribute('data-dir') === 'prev' ? -1 : 1) * Math.max(260, rail.clientWidth * 0.8), behavior: 'smooth' });
      return;
    }
    var tryBtn = e.target.closest('[data-try]');
    if (tryBtn) { openFs(tryBtn.closest('.shot').querySelector('.phone')); return; }
    if (e.target.closest('.fs-close')) closeFs();
  });

  /* full-screen: move the live artboard into an overlay so its own scripts keep working */
  var fs, stage, home = null, moved = null;
  function openFs(phone) {
    if (!phone) return;
    fs = fs || document.querySelector('.fs'); stage = stage || fs.querySelector('.fs-stage');
    home = phone.parentNode; moved = phone;
    var s = Math.min(window.innerWidth / 390, 1.25);
    phone.style.transform = 'scale(' + s + ')';
    phone.style.borderRadius = '0';
    stage.style.height = (phone.offsetHeight * s) + 'px';
    stage.style.width = (390 * s) + 'px';
    stage.style.margin = '0 auto';
    stage.appendChild(phone);
    fs.classList.add('on');
    document.documentElement.style.overflow = 'hidden';
  }
  function closeFs() {
    if (!moved) return;
    moved.style.transform = ''; moved.style.borderRadius = '';
    home.appendChild(moved); moved = null;
    fs.classList.remove('on');
    document.documentElement.style.overflow = '';
    fitAll();
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeFs(); });

  /* local testing only: ?theme=dark flips every artboard */
  if (/theme=dark/.test(location.search)) document.querySelectorAll('.scr:not(.img)').forEach(function (x) { x.setAttribute('data-theme', 'dark'); });
  window.addEventListener('hashchange', showView);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
  showView();
  window.NSU = { fitAll: fitAll };
})();
