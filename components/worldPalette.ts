/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The five module worlds' colours, in one place.
 *
 * This lived twice — once in ModulesView and once in ModuleShowcase — with the
 * same five hexes copied into both. Giving the worlds a dark-mode ink fixed only
 * the copy in ModulesView, and every module title on the category screen stayed
 * at roughly 1.2:1 until someone looked at it. One source, so a third copy
 * cannot drift away again.
 */
import React from 'react';
import { useSettingsContext } from '../contexts/SettingsContext';

export interface WorldTones {
  /** Pale fill behind the world's illustration. */
  blob: string;
  /** Saturated mid-tone — italic sub-headline, primary button, progress fill. */
  mid: string;
  /** `mid` lightened for use as TEXT in dark. It is not a background swap: `mid`
   *  also fills buttons and progress bars, and lightening those while the label
   *  stays white takes them from 3.6:1 to 2.4:1. Backgrounds keep `mid`. */
  midText?: string;
  /** Deeper shade for emphasis text, used at 60-80% alpha via a hex suffix. */
  deep: string;
  /** Same hue as `deep`, raised in luminance. The authored tone is chosen to sit
   *  on a light card and drops to between 1.5:1 and 2.3:1 on the dark one. */
  deepDark: string;
}

export const WORLD_TONES: Record<string, WorldTones> = {
  'architecture-mindset':    { blob: '#B8C9E5', mid: '#5B7DB0', midText: '#8FA9CF', deep: '#1e3a5f', deepDark: '#C2D6EF' },
  'science-growth':          { blob: '#F5C9A8', mid: '#C4873B', midText: '#D9A25F', deep: '#7c4a14', deepDark: '#F3CFA4' },
  'learning-cheat-codes':    { blob: '#B8DDC8', mid: '#F26B1F', midText: '#F58C4E', deep: '#115e4f', deepDark: '#AFE4D3' },
  'subject-specific-science':{ blob: '#F0BFCE', mid: '#C76489', midText: '#DC8FAB', deep: '#8a2860', deepDark: '#F9CFE3' },
  'exam-zone':               { blob: '#F5BFB0', mid: '#D4564E', midText: '#E38B84', deep: '#7f1d1d', deepDark: '#FBD2D2' },
};

/**
 * The world tones resolved for the active theme.
 *
 * Resolved in the component rather than in CSS because these are consumed as hex
 * strings with an alpha suffix (`${deep}AA`), which a var() cannot provide.
 */
export const useWorldTones = () => {
  const darkMode = useSettingsContext()?.settings.darkMode ?? false;
  return React.useMemo(() => ({
    ink: (t: Pick<WorldTones, 'deep' | 'deepDark'>) => (darkMode ? t.deepDark : t.deep),
    /** For TEXT. Backgrounds and fills must use `t.mid` directly. */
    midText: (t: Pick<WorldTones, 'mid' | 'midText'>) => (darkMode ? t.midText ?? t.mid : t.mid),
    /**
     * Fill and ink for a CTA carrying the world colour.
     *
     * Light is unchanged: the saturated `mid` with a white label. Dark inverts
     * instead of darkening. Using `deep` as the fill would give the label
     * excellent contrast but leaves the button only 1.4-2.2:1 apart from the
     * card behind it, so it reads as a tinted hole rather than a raised action.
     * The pale tone sits 11:1 clear of the card and takes dark ink at 12:1.
     */
    cta: (t: Pick<WorldTones, 'mid' | 'deepDark'>) => (darkMode
      // The token, not the literal: the compat layer rewrites an inline
      // `color: #1A1A1A` onto --ink-primary, assuming it is legacy light-mode
      // text, which would turn this label near-white on a pale fill.
      ? { background: t.deepDark, color: 'var(--ink-on-accent)' }
      : { background: t.mid, color: '#FFFFFF' }),
  }), [darkMode]);
};
