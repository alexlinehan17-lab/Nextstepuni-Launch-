/**
 * Boxed scheme page headings never sit inside an Irish answer key (coordinator decision, 2026-10-14).
 *
 * The SEC scheme PDFs store each page's boxed heading ("Ceist 3 FILÍOCHT 30 marc", "A – (50 marc)" …)
 * after the page body, so a key lifted across a page boundary could carry it. irish_furniture.py removes
 * them by EXACT string only. This gate pins that list, proves near-misses survive, and checks that no
 * reviewed Higher/Ordinary card still carries a heading.
 */
import { describe, expect, it } from 'vitest';
import { readdirSync, readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

type Raw = { id: string; level: string; reviewedAt?: string; criteria: { guidance: string[] }[] };
const DIR = 'components/MarkBank/cards/irish';
const raw: Raw[] = readdirSync(DIR).filter(name => name.endsWith('.json'))
  .flatMap(name => (JSON.parse(readFileSync(`${DIR}/${name}`, 'utf8')) as { cards: Raw[] }).cards);
const python = (code: string) => execFileSync('python3', ['-c', `import sys,json\nsys.path.insert(0,'scripts/markbank/authoring')\n${code}`], { encoding: 'utf8' });

const PINNED = [
  'FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH 30 marc',
  'PRÓS AINMNITHE nó PRÓS ROGHNACH 30 marc',
  'Ceist 2 PRÓS 30 marc',
  'Ceist 3 FILÍOCHT 30 marc',
  'Ceist 2 PRÓS (30 marc)',
  'Ceist 3 FILÍOCHT (30 marc)',
  'Cuid II An Cheapadóireacht 100 marc',
  'A – (50 marc)',
  'B – (50 marc)',
  'A – 50 marc',
  'B – 50 marc',
];

describe('Irish scheme page headings', () => {
  it('removes only the pinned exact headings, each a boxed heading ending in its mark total', () => {
    expect(JSON.parse(python('from irish_furniture import HEADINGS\nprint(json.dumps(list(HEADINGS), ensure_ascii=False))'))).toEqual(PINNED);
    for (const heading of PINNED) expect(heading, heading).toMatch(/\d+ marc\)?$/);
    const result = JSON.parse(python(String.raw`from irish_furniture import strip_text
cases=['0-9 0-6 Ceist 2 PRÓS 30 marc Freagair','Ceist 2 PRÓS 30 marcanna','FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH','= 50 marc',
 'Tá 50 marc ar an gceist','A – 50 marc • Bhuaigh','Cuid II An Cheapadóireacht','Ceist 2 PRÓS (30 marc) nó']
print(json.dumps([strip_text(c) for c in cases], ensure_ascii=False))`));
    expect(result).toEqual([
      ['0-9 0-6 Freagair', 1], ['Ceist 2 PRÓS 30 marcanna', 0], ['FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH', 0], ['= 50 marc', 0],
      ['Tá 50 marc ar an gceist', 0], ['• Bhuaigh', 1], ['Cuid II An Cheapadóireacht', 0], ['nó', 1],
    ]);
  });

  it('pins how many headings each reviewed paper lost and leaves none in any reviewed key', () => {
    expect(JSON.parse(python("from irish_cards import HEADING_SCOPE\nprint(json.dumps({f'{y} {l} P{p}': n for (y,l,p),n in HEADING_SCOPE.items()}))"))).toEqual({
      '2022 higher P2': 4, '2023 higher P2': 2, '2024 higher P2': 10, '2025 higher P2': 2,
      '2024 ordinary P1': 9, '2025 ordinary P1': 9, '2024 ordinary P2': 2, '2025 ordinary P2': 2,
    });
    const reviewed = raw.filter(c => c.level !== 'foundation' && c.reviewedAt);
    expect(reviewed.length).toBeGreaterThan(700);
    const left = reviewed.filter(c => c.criteria.some(r => r.guidance.some(g => PINNED.some(h => g.includes(h)))));
    expect(left.map(c => c.id)).toEqual([]);
  });
});
