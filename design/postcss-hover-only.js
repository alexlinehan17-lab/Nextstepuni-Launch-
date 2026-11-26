/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Hover looks only on devices that can hover.
 *
 * On a phone a tap fires :hover and the look stays until the next tap
 * somewhere else, so a button looks pressed or highlighted after it has done
 * its job (the design audit counted 907 places). Tailwind's hover: variants
 * are guarded by `future.hoverOnlyWhenSupported` in tailwind.config.ts; this
 * plugin gives every hand-written `:hover` rule the same guard, the same
 * media query Tailwind uses, so the two never disagree:
 *
 *   .a:hover, .a:focus-visible { color: red }
 * becomes
 *   .a:focus-visible { color: red }
 *   @media (hover: hover) and (pointer: fine) { .a:hover { color: red } }
 *
 * A rule already inside a hover media query is left alone.
 */
export const HOVER_QUERY = '(hover: hover) and (pointer: fine)';

const isHoverGuarded = node => {
  for (let parent = node.parent; parent; parent = parent.parent) {
    if (parent.type === 'atrule' && parent.name === 'media' && /\bhover\s*:\s*hover\b/.test(parent.params)) return true;
  }
  return false;
};
const isInKeyframes = node => {
  for (let parent = node.parent; parent; parent = parent.parent) {
    if (parent.type === 'atrule' && /keyframes$/i.test(parent.name)) return true;
  }
  return false;
};

export default function hoverOnlyWhenSupported() {
  return {
    postcssPlugin: 'nsu-hover-only-when-supported',
    Once(root, { AtRule }) {
      const rules = [];
      root.walkRules(rule => {
        if (rule.selector.includes(':hover') && !isHoverGuarded(rule) && !isInKeyframes(rule)) rules.push(rule);
      });
      for (const rule of rules) {
        const hover = rule.selectors.filter(selector => selector.includes(':hover'));
        const rest = rule.selectors.filter(selector => !selector.includes(':hover'));
        const media = new AtRule({ name: 'media', params: HOVER_QUERY });
        media.append(rule.clone({ selectors: hover }));
        if (rest.length) {
          rule.selectors = rest;
          rule.after(media);
        } else {
          rule.replaceWith(media);
        }
      }
    },
  };
}
hoverOnlyWhenSupported.postcss = true;
