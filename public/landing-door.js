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
  // The traveller may already be running on a restored page, or may never
  // mount on mobile / reduced motion. Always clear this temporary copy once
  // the transition ends so it cannot linger beside the footer's Starguy.
  var clear = function () {
    m.removeAttribute('data-here');
    m.style.viewTransitionName = '';
  };
  e.viewTransition.finished.then(clear, clear);
});
