/*
 * The landing page's starguy walks into the app. When this document is the
 * destination of a cross-document view transition from the landing page
 * (components/landing/leave.ts), the small figure #app-mark is where the
 * browser lands him: it takes the shared name at pagereveal, waits by the
 * door four seconds, then fades. On the way back it takes the name again.
 *
 * A classic script served from our own origin (the production CSP allows no
 * inline script), loaded in <head> before the render-blocking expect link,
 * so the handler exists before pagereveal can fire.
 */
(function () {
  var fromLanding = /(^|[?&])from=landing(&|$)/.test(location.search) || /\/landing-dev\.html/.test(document.referrer);
  if (!fromLanding) return;
  var mark = function () { return document.getElementById('app-mark'); };
  var hide = function (m) {
    m.style.opacity = '0';
    setTimeout(function () { m.removeAttribute('data-here'); m.style.opacity = ''; }, 700);
  };
  addEventListener('pagereveal', function (e) {
    var m = mark();
    if (!e.viewTransition || !m) return;
    m.setAttribute('data-here', '');
    m.style.viewTransitionName = 'starguy';
    e.viewTransition.finished.finally(function () {
      m.style.viewTransitionName = '';
      setTimeout(function () { hide(m); }, 4000);
    });
  });
  addEventListener('pageswap', function (e) {
    var m = mark();
    if (!e.viewTransition || !m || !m.hasAttribute('data-here')) return;
    m.style.viewTransitionName = 'starguy';
  });
})();
