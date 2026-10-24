import { it } from 'vitest';
import { writeFileSync } from 'node:fs';
import authored from '../components/MarkBank/cards/irish/authored.json';
import { parseIrishAnswers } from '../components/MarkBank/cards/irish/answers';

const OUT = '/private/tmp/claude-501/-Users-alexlinehan/bca4b610-fa80-4e89-aba4-3e2d69642c1b/scratchpad/irish-report.txt';
type Card = { id: string; level: string; totalMarks: number; questionRef: string; questionText: string; criteria: { guidanceKind: string; maxMarks: number; guidance: string[] }[] };

it('scratch irish report', () => {
  const cards = (authored as { cards: Card[] }).cards;
  const lines: string[] = [];
  const family = (card: Card) => /Cluastuiscint/.test(card.questionRef) ? 'listening' : /Léamhthuiscint/.test(card.questionRef) ? 'reading' : 'other';
  const counts: Record<string, number> = {}; const reasons: Record<string, string[]> = {}; const samples: Record<string, string> = {};
  const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9áéíóú’'-]+/g, '');
  const lifting: string[] = [];
  for (const card of cards) {
    const criterion = card.criteria[0];
    if (criterion.guidanceKind !== 'exact' || family(card) === 'other') continue;
    const key = `${family(card)}/${card.level}`;
    const result = parseIrishAnswers({ id: card.id, totalMarks: criterion.maxMarks, questionRef: card.questionRef, questionText: card.questionText, guidance: criterion.guidance });
    counts[`${key} ${result.ok ? 'ok' : 'fail'}`] = (counts[`${key} ${result.ok ? 'ok' : 'fail'}`] ?? 0) + 1;
    if (!result.ok) {
      (reasons[`${key} :: ${result.reason.replace(/\d+/g, 'N').slice(0, 50)}`] ??= []).push(card.id);
      if (/tariffs add|unpriced answers/.test(result.reason) && Object.keys(samples).filter(k => k.startsWith('FAIL')).length < 14) {
        const text = criterion.guidance.join(' ').replace(//g, '•');
        samples['FAIL ' + card.id + ' :: ' + result.reason + ' :: Q=' + card.questionText.slice(0, 120)] = 'HEAD ' + text.slice(0, 160) + ' … TAIL ' + text.slice(-260);
      }
      continue;
    }
    const corpus = normalise(criterion.guidance.join(' ') + ' ' + card.questionText);
    for (const part of result.allocation.parts) {
      if (part.prompt && !corpus.includes(normalise(part.prompt))) lifting.push(`${card.id}: prompt "${part.prompt.slice(0, 50)}"`);
      for (const row of part.rows) if (!row.text || !corpus.includes(normalise(row.text))) lifting.push(`${card.id}: row "${row.text.slice(0, 50)}"`);
    }
    for (const note of result.allocation.directions) if (!corpus.includes(normalise(note))) lifting.push(`${card.id}: direction "${note.slice(0, 50)}"`);
    if (!samples[key] || ['irish-2021-hl-p2-reading-b-q1', 'irish-2021-ol-p2-reading-a-q1', 'irish-2023-ol-p1-listening-b-c2', 'irish-2021-ol-p1-listening-c-p2'].includes(card.id)) {
      samples[key + ' ' + card.id] = JSON.stringify(result.allocation.parts.map(p => [p.prompt?.slice(0, 50), p.tariff, p.ladder, p.rows.map(r => [r.text.slice(0, 45), r.marks])])) + ' DIR ' + JSON.stringify(result.allocation.directions.map(d => d.slice(0, 60)));
    }
  }
  lines.push(JSON.stringify(counts, null, 1));
  for (const [reason, ids] of Object.entries(reasons).sort((a, b) => b[1].length - a[1].length)) lines.push(`${ids.length.toString().padStart(3)}  ${reason}  e.g. ${ids.slice(0, 3).join(', ')}`);
  lines.push(`lifting failures: ${lifting.length}`); lifting.slice(0, 15).forEach(l => lines.push('   ' + l));
  for (const [k, v] of Object.entries(samples)) lines.push(`SAMPLE ${k}\n   ${v}`);
  writeFileSync(OUT, lines.join('\n') + '\n');
});
