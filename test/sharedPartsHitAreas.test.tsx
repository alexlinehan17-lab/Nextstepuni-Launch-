/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every shared control has a 44 x 44 hit area (mobile.md, "Touch"). A control
 * drawn at 44 or more is sized so in components/ui/parts.css; one drawn
 * smaller (the 36px button, a short text button, the switch, the selection
 * bar's choices, the "what is missing" sentence) carries the frame's
 * invisible 44 x 44 layer, `frame-hit` (components/ui/frame.css).
 *
 * jsdom has no layout, so this checks the declared sizes and the mechanism on
 * every control the parts render; the drawn and pressable sizes were also
 * measured in Chrome on the parts sheet (stage 2A evidence, measurements.json).
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { cleanup, render } from '@testing-library/react';
import { afterEach, expect, test } from 'vitest';
import { ChevronLeft } from 'lucide-react';
import { Button, Glyph, IconButton, TextButton } from '@/components/ui/Button';
import { ChoiceGroup, SelectionBar, Switch } from '@/components/ui/Choice';
import { Menu } from '@/components/ui/Menu';
import { PinnedFooter, TabBar, TopBar } from '@/components/ui/Bars';
import { Field, SearchField } from '@/components/ui/Field';
import { List, PressBox, Row } from '@/components/ui/List';
import { Sheet } from '@/components/ui/Sheet';

afterEach(cleanup);

const css = readFileSync(join(process.cwd(), 'components/ui/parts.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
const frame = readFileSync(join(process.cwd(), 'components/ui/frame.css'), 'utf8');

/** The smallest height and width a class is declared at (its own rule, outside media queries). */
function declared(cls: string): { h: number; w: number } {
  const top = css.replace(/@media[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}/g, '');
  let h = 0; let w = 0;
  for (const m of top.matchAll(new RegExp(`(?:^|\\})\\s*([^{}]*\\.${cls}(?![\\w-])[^{}]*)\\{([^}]*)\\}`, 'g'))) {
    if (!m[1].split(',').some(sel => new RegExp(`^\\s*\\.${cls}\\s*$`).test(sel))) continue;
    const body = m[2];
    const px = (prop: string) => Number(body.match(new RegExp(`(?:^|;|\\s)${prop}:\\s*(\\d+)px`))?.[1] ?? 0);
    h = Math.max(h, px('height'), px('min-height'));
    w = Math.max(w, px('width'), px('min-width'));
    if (/(?:^|;|\s)width:\s*100%/.test(body)) w = Math.max(w, 1000);
  }
  return { h, w };
}

test('the frame hit layer is 44 x 44', () => {
  expect(frame).toMatch(/--frame-hit:\s*44px;/);
  expect(frame).toMatch(/\.frame-hit::after\s*\{[^}]*width:\s*max\(100%, var\(--frame-hit\)\);[^}]*height:\s*max\(100%, var\(--frame-hit\)\);/);
});

test('every control the parts render is 44 x 44 to the finger', () => {
  const noop = () => {};
  const { container } = render(<>
    <Button kind="main" size="lg" block arrow="forward">Start session</Button>
    <Button>Add</Button>
    <Button size="sm">Filter</Button>
    <Button kind="main" missing={{ sentence: 'Choose a subject.', goTo: noop }}>Choose your subject</Button>
    <Button unavailable="Opens later.">Start What matters</Button>
    <TextButton>Skip</TextButton>
    <IconButton label="Back" icon={<Glyph icon={ChevronLeft} />} />
    <ChoiceGroup<string> legend="One" value="a" onChange={noop} options={[{ value: 'a', label: 'A' }, { value: 'b', label: 'B' }]} />
    <ChoiceGroup<string> kind="several" tiles legend="Several" value={['a']} onChange={noop} options={[{ value: 'a', label: 'A' }, { value: 'b', label: 'B' }]} />
    <Switch checked onChange={noop} label="On" />
    <SelectionBar<string> label="Show" value="a" onChange={noop} options={[{ value: 'a', label: 'A' }, { value: 'b', label: 'B' }]} />
    <Menu label="Subject" value="a" onChange={noop} options={[{ value: 'a', label: 'All' }]} />
    <TopBar leave={{ kind: 'back', onPress: noop }} title="Biology" />
    <TabBar items={[{ id: 'home', label: 'Home', icon: ChevronLeft }]} current="home" onSelect={noop} />
    <PinnedFooter><Button kind="main" size="lg" block>Continue</Button></PinnedFooter>
    <Field label="Name" />
    <SearchField label="Search" />
    <List><Row title="Unit 2" onPress={noop} /></List>
    <PressBox onPress={noop}>Exam paper</PressBox>
  </>);
  const controls = [...container.querySelectorAll<HTMLElement>('button, a[href], input')];
  expect(controls.length).toBeGreaterThan(20);
  const short: string[] = [];
  for (const el of controls) {
    const ui = [...el.classList].filter(c => c.startsWith('ui-') && c !== 'ui-part');
    const size = ui.map(declared).reduce((a, b) => ({ h: Math.max(a.h, b.h), w: Math.max(a.w, b.w) }), { h: 0, w: 0 });
    const hit = el.classList.contains('frame-hit') || Boolean(el.closest('.frame-bar, .frame-dialog-head'));
    const name = `${el.tagName.toLowerCase()}.${ui.join('.')} "${(el.textContent || el.getAttribute('aria-label') || '').trim()}"`;
    // A sized dimension of 44+ passes; a full-width control passes its width; anything else needs the hit layer.
    const tallEnough = size.h >= 44 || hit;
    const wideEnough = size.w >= 44 || hit || el.classList.contains('ui-btn') || el.classList.contains('ui-menu-btn') || el.classList.contains('ui-tab') || el.classList.contains('ui-field-input');
    if (!tallEnough || !wideEnough) short.push(`${name}: h ${size.h}, w ${size.w}, frame-hit ${hit}`);
  }
  expect(short, 'controls under 44 x 44 with no hit layer').toEqual([]);
});

test('the sheet header controls are 44 and sit in a frame-dialog-head (44 x 44 layer)', () => {
  render(<Sheet open title="Goal" onClose={() => {}} save={{ label: 'Save', onPress: () => {} }}><p>Body</p></Sheet>);
  const head = document.querySelector('.ui-sheet-head');
  expect(head).toHaveClass('frame-dialog-head');
  expect(declared('ui-sheet-text').h).toBeGreaterThanOrEqual(44);
});
