import fs from 'node:fs';
import { builtDecks, loadCards, SUBJECTS } from '../components/MarkBank/deck';
const out = process.argv[2];
const decks = builtDecks();
fs.writeFileSync(`${out}/_subjects.json`, JSON.stringify(SUBJECTS));
for (const d of decks) {
  const cards = await loadCards(d.subjectId, d.level);
  fs.writeFileSync(`${out}/${d.subjectId}__${d.level}.json`, JSON.stringify(cards));
  console.log(d.label, cards.length);
}
