/** Keep both pages painted until the bloom and its content have settled. */
export function animateStudyChange({ from, to, origin, reduced, returning = false, mascot, onFinish }: {
  from: HTMLElement;
  to: HTMLElement;
  origin: { x: number; y: number };
  reduced: boolean;
  returning?: boolean;
  mascot?: { from: SVGSVGElement; to: SVGSVGElement };
  onFinish: () => void;
}) {
  const animations: Animation[] = [];
  const pending: Promise<unknown>[] = [];
  let cancelled = false;
  let restoreMascot = () => {};
  const mascotBounds = mascot ? { from: mascot.from.getBoundingClientRect(), to: mascot.to.getBoundingClientRect() } : undefined;
  const animate = (element: Element, frames: Keyframe[], duration: number, delay = 0) => {
    if (!element.animate) return;
    const animation = element.animate(frames, { duration, delay, easing: 'cubic-bezier(.22,1,.36,1)', fill: 'both' });
    animations.push(animation);
    pending.push(animation.finished.catch(() => {}));
  };

  if (reduced) {
    animate(returning ? from : to, [{ opacity: returning ? 1 : 0 }, { opacity: returning ? 0 : 1 }], 120);
  } else {
    if (returning) animate(from, [{ opacity: 1 }, { opacity: 0 }], 620);
    else {
      const bounds = to.getBoundingClientRect();
      const x = origin.x - bounds.left, y = origin.y - bounds.top;
      const radius = Math.ceil(Math.hypot(Math.max(x, bounds.width - x), Math.max(y, bounds.height - y))) + 2;
      animate(to, [{ clipPath: `circle(0px at ${x}px ${y}px)` }, { clipPath: `circle(${radius}px at ${x}px ${y}px)` }], 850);
      animate(from, [{ opacity: 1 }, { opacity: .65 }], 650);
      to.querySelectorAll<HTMLElement>('[data-study-arrive]').forEach((element, index) => {
        // Artwork stays sharp throughout: only position and opacity animate.
        animate(element, [{ opacity: 0, transform: 'translateY(12px)' }, { opacity: 1, transform: 'translateY(0)' }], 500, 265 + index * 35);
      });
    }
    if (mascot && mascotBounds && mascot.from.animate) {
      const a = mascotBounds.from, b = mascotBounds.to;
      if (a.width && b.width) {
        const sprite = mascot.from.cloneNode(true) as SVGSVGElement;
        sprite.setAttribute('aria-hidden', 'true');
        sprite.dataset.studyMascotSprite = '';
        sprite.style.cssText = `position:fixed;left:0;top:0;width:${a.width}px;height:${a.height}px;transform-origin:0 0;z-index:120;pointer-events:none;background:transparent;`;
        document.body.appendChild(sprite);
        const visibility = [mascot.from.style.visibility, mascot.to.style.visibility];
        mascot.from.style.visibility = mascot.to.style.visibility = 'hidden';
        restoreMascot = () => {
          sprite.remove();
          mascot.from.style.visibility = visibility[0];
          mascot.to.style.visibility = visibility[1];
        };
        animate(sprite, [{ transform: `translate(${a.left}px,${a.top}px) scale(1)` }, { transform: `translate(${b.left}px,${b.top}px) scale(${b.width / a.width})` }], returning ? 620 : 850);
      }
    }
  }
  const clean = () => { animations.forEach(animation => animation.cancel()); restoreMascot(); };
  if (!pending.length) { onFinish(); return () => {}; }
  void Promise.all(pending).then(() => { if (!cancelled) { clean(); onFinish(); } });
  return () => { cancelled = true; clean(); };
}

export function studyControlOrigin(element: HTMLElement) {
  const bounds = element.getBoundingClientRect();
  return { x: bounds.left + bounds.width / 2, y: bounds.top + bounds.height / 2 };
}
