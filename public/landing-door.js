/*
 * Home from the app: when this document is the destination of a
 * cross-document view transition from the app (public/door.js), the browser
 * lands starguy on #landing-mark, and the traveller (Traveller.tsx) picks him
 * up from there and walks him to the hero. A classic script served from our
 * own origin, because the production CSP allows no inline script.
 */
/* global document, addEventListener */
addEventListener('pagereveal', function (e) {
  var m = document.getElementById('landing-mark');
  if (!e.viewTransition || !m) return;
  m.setAttribute('data-here', '');
  m.style.viewTransitionName = 'starguy';
  e.viewTransition.finished.finally(function () { m.style.viewTransitionName = ''; });
});
