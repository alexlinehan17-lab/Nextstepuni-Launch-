/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "How your points work": the CAO grid for Higher, Ordinary and Foundation,
 * opened from the grades step. Built from the Kobra Dialog, Tabs, Progress and
 * Button. Only the levels a student's subjects offer get a tab, and the grades
 * they have picked are marked on it.
 */

import React, { useMemo, useState } from 'react';
import { ArrowUpRight, Info } from 'lucide-react';
import KobraScope, {
  Button, Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle,
  Progress, Tabs, TabsContent, TabsList, TabsTrigger,
} from '../approved-ui-runtime';
import {
  FOUNDATION_POINTS, HIGHER_POINTS, LCVP_POINTS, ORDINARY_POINTS, lcSubjectLevels, type Level,
} from '../subjectData';
import type { SetupDraft } from './model';
import './points-guide.css';

type Column = 'higher' | 'ordinary' | 'foundation';
const COLUMNS: { level: Column; label: string; prefix: string; points: Record<string, number>; blurb: string }[] = [
  { level: 'higher', label: 'Higher', prefix: 'H', points: HIGHER_POINTS, blurb: 'The most points for every grade.' },
  { level: 'ordinary', label: 'Ordinary', prefix: 'O', points: ORDINARY_POINTS, blurb: 'O1 matches H5, then the points step down.' },
  { level: 'foundation', label: 'Foundation', prefix: 'F', points: FOUNDATION_POINTS, blurb: 'Maths and Irish only. Not every college counts it.' },
];
const GRADES = [1, 2, 3, 4, 5, 6, 7, 8];

/** Levels worth showing for these subjects; every level before any are chosen. */
export function guideColumns(subjects: string[]): Column[] {
  if (!subjects.length) return ['higher', 'ordinary', 'foundation'];
  const offered = new Set<Level>(subjects.flatMap(lcSubjectLevels));
  const columns = COLUMNS.map(c => c.level).filter(level => offered.has(level));
  return columns.length ? columns : ['higher', 'ordinary'];
}

interface Props {
  draft: Pick<SetupDraft, 'subjects' | 'configs'>;
  label?: string;
  className?: string;
}

export default function PointsGuide({ draft, label = 'How do points work?', className = '' }: Props) {
  const [open, setOpen] = useState(false);
  const columns = useMemo(() => COLUMNS.filter(c => guideColumns(draft.subjects).includes(c.level)), [draft.subjects]);
  // Open on the level the student is actually sitting, else the first one.
  const startLevel = useMemo(() => {
    const own = draft.subjects.map(name => draft.configs[name]?.level).find((level): level is Column => columns.some(c => c.level === level));
    return own ?? columns[0].level;
  }, [columns, draft.subjects, draft.configs]);
  const [tab, setTab] = useState<string | null>(null);
  const active = tab && columns.some(c => c.level === tab) ? tab : startLevel;

  const current = new Set<string>();
  const target = new Set<string>();
  for (const name of draft.subjects) {
    const config = draft.configs[name];
    if (config?.current && config.current !== 'later') current.add(config.current);
    if (config?.target && config.target !== 'later') target.add(config.target);
  }
  const hasMaths = draft.subjects.includes('Mathematics');
  const hasLcvp = draft.subjects.includes('LCVP Link Modules');

  return (
    <KobraScope className={`nsu-points-guide ${className}`}>
      <Button variant="outline" className="nsu-ink-outline pg-trigger" onClick={() => setOpen(true)}>
        <Info aria-hidden="true" />{label}<ArrowUpRight aria-hidden="true" />
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="pg-dialog" size="lg">
          <DialogHeader>
            <p className="pg-eyebrow">Leaving Cert · CAO points</p>
            <DialogTitle>Every grade is worth points.</DialogTitle>
            <DialogDescription>
              Colleges add up your best six subjects for a total out of 625. The same grade is worth more at a higher level.
            </DialogDescription>
          </DialogHeader>

          <Tabs value={active} onValueChange={value => setTab(String(value))} className="pg-tabs">
            <TabsList aria-label="Level">
              {columns.map(c => {
                const marked = [...current, ...target].some(code => code.startsWith(c.prefix) && code in c.points);
                return (
                  <TabsTrigger key={c.level} value={c.level}>
                    {c.label}
                    {marked && <i className="pg-dot" role="img" aria-label="has your grades" />}
                  </TabsTrigger>
                );
              })}
            </TabsList>
            {columns.map(c => (
              <TabsContent key={c.level} value={c.level} className="pg-panel">
                <p className="pg-blurb">{c.blurb}</p>
                <ol className="pg-lines">
                  {GRADES.map(grade => {
                    const code = `${c.prefix}${grade}`;
                    const points = c.points[code] ?? 0;
                    const isCurrent = current.has(code);
                    const isTarget = target.has(code);
                    return (
                      <li key={code} className="pg-line" data-current={isCurrent || undefined} data-target={isTarget || undefined}>
                        <span className="pg-code">{code}</span>
                        <Progress className="pg-bar" value={points} max={100} aria-label={`${code}, ${points} points`} />
                        <span className="pg-points">{points}</span>
                        <span className="pg-mark">
                          {isCurrent && <em data-kind="current">You now</em>}
                          {isTarget && <em data-kind="target">Target</em>}
                        </span>
                      </li>
                    );
                  })}
                </ol>
              </TabsContent>
            ))}
          </Tabs>

          <section className="pg-notes" aria-label="Good to know">
            <p className="pg-notes-title">Good to know</p>
            <ul>
              <li><b>Same points, different level.</b> O1 and H5 are both 56. An Ordinary student aiming at Higher is aiming at more points.</li>
              <li><b>The bottom grades score nothing.</b> H8, O7 and O8, and Foundation below F2, are worth zero. The subject still earns study time in your plan.</li>
              {hasMaths && <li><b>Higher Maths bonus.</b> H6 or better earns 25 extra points, so H1 is worth 125.</li>}
              {hasLcvp && <li><b>LCVP Link Modules</b> is Distinction, Merit or Pass: {LCVP_POINTS.Distinction}, {LCVP_POINTS.Merit} or {LCVP_POINTS.Pass} points, and can stand in for one of your six.</li>}
            </ul>
          </section>
        </DialogContent>
      </Dialog>
    </KobraScope>
  );
}
