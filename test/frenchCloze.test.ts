import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import { FRENCH_CLOZE_CARDS as cards } from '../components/MarkBank/cards/french/cloze';
import tasks from '../data/examTopics/french-reviewed-tasks.json';
import { tariffReconciles } from '../types/markBank';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import { frenchMarks } from '../components/MarkBank/frenchRubric';

const answers: Record<number, string[]> = {
  2010: ['pas', 'occupée', 'en', 'de', 'tous', 'me', 'viens', 'nouveau', 'visite', 'peux'],
  2011: ['tout', 'malade', 'trois', 'pas', 'suis', 'mon', 'banque', 'aller', 'très', 'bonjour'],
  2012: ['musique', 'pas', 'dit', 'boulot', 'magasin', 'argent', 'est', 'samedi', 'à', 'tes'],
  2013: ['avec', 'grande', 'demandé', 'jouer', 'membre', 'deux', 'romans', 'librairie', 'poche', 'aimes'],
  2014: ['répondu', 'suis', 'bac', 'pas', 'professeurs', 'difficile', 'beaucoup', 'examens', 'robes', 'venir'],
  2015: ['écrit', 'voyage', 'dernier', 'ballon', 'passer', 'dit', 'parents', 'pas', 'avec', 'de'],
  2016: ['long', 'avec', 'pas', 'beau', 'sortais', 'copains', 'humeur', 'elle', 'espère', 'suis'],
  2017: ['lettre', 'pour', 'achetons', 'cinéma', 'vu', 'passer', 'gare', 'libre', 'te', 'peux'],
  2018: ['cadeau', 'mon', 'organisé', 'en', 'tous', 'courses', 'argent', 'suis', 'ranger', 'pas'],
  2019: ['lettre', 'tu', 'content', 'ta', 'trouvé', 'travaille', 'clients', 'heure', 'acheter', 'l’'],
  2020: ['ta', 'passe', 'avec', 'jolie', 'natation', 'plages', 'soir', 'rencontré', 'elle', 'serai'],
  2021: ['vas', 'mois', 'la', 'ai', 'visité', 'classe', 'appartement', 'petit', 'faire', 'tes'],
  2022: ['je', 'semaines', 'avons', 'près', 'assez', 'beau', 'l’', 'pas', 'vacances', 'du'],
  2023: ['la', 'trouvé', 'travaille', 'pas', 'sympas', 'mes', 'nous', 'j’', 'chez', 'famille'],
  2024: ['en', 'passe', 'me', 'soleil', 'une', 'desserts', 'acheté', 'ma', 'prochaine', 'allons'],
  2025: ['à', 'visite', 'nationale', 'musique', 'amuse', 'magnifiques', 'moi', 'fait', 'irons', 'restaurant'],
  2026: ['bien', 'examens', 'commencé', 'je', 'sont', 'pas', 'pour', 'logement', 'tes', 'iras'],
};

describe('French gap-level practice', () => {
  it('retains all 170 separately priced gaps and the source word banks', () => {
    expect(cards).toHaveLength(170);
    for (const [year, expected] of Object.entries(answers)) {
      const group = cards.filter(card => card.year === Number(year));
      expect(group).toHaveLength(10);
      expect(new Set(group.map(card => card.questionText)).size).toBe(10);
      group.forEach((card, index) => {
        expect(card.id).toBe(`fr-${year}-ol-cloze-b1a-gap-${index + 1}`);
        // The scheme's numbered answer entry, exactly as printed (with the
        // reviewed exceptions pinned in the cloze ledger).
        const printedEntry: Record<string, string> = {
          '2019-6': '6 travaille', '2019-7': '7 clients', '2019-8': '8 heure', '2019-9': '9 acheter', '2019-10': '10 l’',
          '2020-2': '2. passe/serai', '2022-10': '10.', '2025-6': '6. maqnifiques',
        };
        expect(card.rubric.answerGuide![0]).toBe(printedEntry[`${year}-${index + 1}`] ?? `${index + 1}. ${expected[index]}`);
        expect(card.rubric.answerGuide).toContain('10 gaps for 3 marks each');
        // Printed instruction, printed bank, then the excerpt. No generator-written French.
        const [instruction, bankLine, excerpt] = card.questionText.split('\n\n');
        expect(instruction).toMatch(/^Complétez la lettre ci.dessous en écrivant les mots suivants dans les espaces appropriés\. \(N\.B\. Cette liste n’est pas dans le bon ordre\.\)$/);
        expect(excerpt).toContain(`[${index + 1}]`);
        const bank = bankLine.replace(/\.$/, '').split(', ');
        expect(bank.sort()).toEqual([...expected].sort());
        expect(card.questionText).not.toMatch(/Mots proposés|Complétez l’espace/);
        expect(card.rubric.taskRequirements).toEqual([]);
        expect(card.rubric.criteria[0].guidance).toEqual([]);
        expect(card.rubric.markingGuideNote).toBe('');
        expect(card.rubric.practiceNotes![0]).toBe(`This card practises gap [${index + 1}] only; any other numbered gap in the excerpt is a separate card.`);
        expect(card.totalMarks).toBe(3);
        expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 2, 3]);
        expect(tariffReconciles(card)).toBe(true);
        // The gap is one stepped row: 3, or 2 after the printed deduction; nothing else is a value.
        expect(card.rubric.allocation?.rows.map(row => row.steps)).toEqual([[3, 2]]);
        expect(frenchMarks(card, { 'french:row:r1': 2 })).toBe(2);
        expect(frenchMarks(card, { 'french:row:r1': 1 })).toBe(0);
      });
      expect(group.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(30);
    }
  });

  it('keeps the first gap when the original salutation has no comma', () => {
    const first = cards.find(card => card.id === 'fr-2018-ol-cloze-b1a-gap-1')!;
    expect(first.questionText).toContain('J’écris pour te remercier très sincèrement de ton beau [1]');
    expect(first.questionText).not.toContain('Cher Nicolas');
    expect(first.questionText.split('\n\n')[1]).toBe('courses, mon, suis, tous, argent, organisé, pas, cadeau, en, ranger');
  });

  it('restores printed words the column reader dropped from the 2012, 2013, 2016 and 2017 letters', () => {
    const excerpt = (id: string) => cards.find(card => card.id === id)!.questionText.split('\n\n')[2];
    expect(excerpt('fr-2012-ol-cloze-b1a-gap-10')).toBe('Dis bonjour de ma part à [10] parents.');
    expect(excerpt('fr-2013-ol-cloze-b1a-gap-8')).toBe('J’achète mes livres dans la [8] .');
    expect(excerpt('fr-2013-ol-cloze-b1a-gap-9')).toBe('Ça coûte cher, donc je n’ai jamais assez d’argent de [9] .');
    expect(excerpt('fr-2017-ol-cloze-b1a-gap-5')).toBe('Hier soir, j’ai [5] un film d’espionnage.');
    expect(excerpt('fr-2017-ol-cloze-b1a-gap-10')).toBe('Téléphone-moi ou envoie-moi un texto pour me dire si tu [10] venir.');
    // Only the card's own gap is numbered; the others keep their printed blanks.
    expect(excerpt('fr-2016-ol-cloze-b1a-gap-5')).toBe('Quand je [5] avec mes ____________ , Orla était toujours de mauvaise ____________ .');
    expect(excerpt('fr-2016-ol-cloze-b1a-gap-6')).toBe('Quand je ____________ avec mes [6] , Orla était toujours de mauvaise ____________ .');
    expect(excerpt('fr-2016-ol-cloze-b1a-gap-7')).toBe('Quand je ____________ avec mes ____________ , Orla était toujours de mauvaise [7] .');
  });

  it('lifts the 2012 capital-letter exception for samedi into every 2012 gap', () => {
    for (const card of cards.filter(card => card.year === 2012)) {
      expect(card.rubric.answerGuide!.at(-1)).toBe('Careless transcription, including accents, deduct 1 mark. Accept capital letters (apart from samedi).');
      expect(card.schemeRegion?.p).toBe(9);
    }
    for (const card of cards.filter(card => card.year !== 2012)) {
      expect(card.rubric.answerGuide!.at(-1)).toBe('Careless transcription, including accents, deduct 1 mark. Accept capital letters.');
    }
  });

  it('carries the 2011 gap-9 condition printed under the answer list on that gap only', () => {
    const note = 'N.B. Gap 9: accept « tout » for 3 marks if not already accepted in Gap 1.';
    const group = cards.filter(card => card.year === 2011);
    expect(group.filter(card => card.rubric.answerGuide!.includes(note)).map(card => card.id)).toEqual(['fr-2011-ol-cloze-b1a-gap-9']);
    expect(group.find(card => card.id === 'fr-2011-ol-cloze-b1a-gap-9')!.rubric.answerGuide![0]).toBe('9. très');
  });

  it('uses the verified completed-letter answer when the 2022 answer list is blank', () => {
    const card = cards.find(card => card.id === 'fr-2022-ol-cloze-b1a-gap-10')!;
    // The numbered list prints "10." with nothing after it; the completed letter prints the answer.
    expect(card.rubric.answerGuide!.slice(0, 2)).toEqual(['10.', 'On pourrait faire __du____ vélo']);
    expect(card.rubric.practiceNotes!.join(' ')).toContain('leaves item 10 blank');
    const misprint = cards.find(card => card.id === 'fr-2025-ol-cloze-b1a-gap-6')!;
    expect(misprint.rubric.answerGuide!.slice(0, 2)).toEqual(['6. maqnifiques', 'Les feux d’artifice sont magnifiques.']);
    expect(card.questionText).toContain('On pourrait faire [10] vélo');
    expect(card.schemeRegion?.p).toBe(11);
  });

  it('opens the original letter from each matching Atlas task', () => {
    for (const card of cards) {
      const task = tasks.find(task => task.cardId === card.id)!;
      const paper = topicsForPaper('french', card.year, 'ordinary', 'ev', task.fileid)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === task.n)!)).toEqual(task.topicIds);
      expect(task.topicIds.flatMap(curriculumNodeIdsForExamTopic)).toContain(card.topicId);
      const map = JSON.parse(fs.readFileSync(`public/paper-anchors/${card.year}/${task.fileid}.json`, 'utf8'));
      expect(paperRegionFor(map.q, task.n, map.maxCropPages)?.map(region => region.p)).toEqual([card.year <= 2019 ? 10 : 12]);
      expect(card.sourceMaterial?.pages).toEqual([card.year <= 2019 ? 10 : 12]);
    }
  });
});
