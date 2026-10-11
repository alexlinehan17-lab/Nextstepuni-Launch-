#!/usr/bin/env python3
"""Reviewed gap-level practice, preserving every original whole-letter card."""
from pathlib import Path
import hashlib
import json
import re
import fitz
from fr_paper import FrPaper
from fr_selection import verify_paper
from fr_reviewed_tasks import write_tasks

ROOT = Path(__file__).resolve().parents[3]


def build():
    review = json.loads(Path(__file__).with_name('french-cloze-review.json').read_text())
    block = (ROOT / 'paperTrailData.ts').read_text().split('  "french": [', 1)[1].split('\n  ],', 1)[0]
    entries = [json.loads(line.strip().rstrip(',')) for line in block.splitlines() if line.strip()]
    tags = json.loads((ROOT / 'scripts/paper-trail/topic-tags/tags/french.json').read_text())
    runtime = json.loads((ROOT / 'data/examTopics/french-runtime.json').read_text())
    cards, tasks = [], []
    for record in review['papers']:
        year = record['year']
        for source in record['sources']:
            assert hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() == source['sha256']
        paper = FrPaper(year, 'ol')
        verify_paper(Path(paper.path), pages=[record['paperPage']])
        text, page = next((text, page) for q, letter, text, page in paper.section_b_asks() if q == 1 and letter == 'a')
        assert page == record['paperPage']
        assert len(re.findall(r'_{3,}', text)) == 10
        bank_start = text.index('(N.B.')
        bank_start = text.index(')', bank_start) + 1
        # Ten comma-separated words precede the location/date, which are not
        # part of the bank. The final word is one token in every reviewed paper.
        if record.get('wordBank'):
            # Some full-width banks cross the bilingual column boundary.
            # Pin all ten words to the original page, preserving their order.
            words = record['wordBank']
            assert len(words) == 10 and record['wordBankReason']
            with fitz.open(paper.path) as source_pdf:
                raw_page = source_pdf[page - 1].get_text(sort=True)
            compact = lambda value: re.sub(r'\s+', '', value)
            assert compact(','.join(words)) in compact(raw_page), year
        else:
            words = text[bank_start:].strip().split(',', 9)
            words = [word.strip() for word in words[:9]] + [words[9].split()[0]]
        assert set(words) == set(record['answers']), (year, words)
        with fitz.open(ROOT / f'examiner-reports/french/schemes/{year}-ol.pdf') as scheme:
            scheme_text = ' '.join(scheme[record['schemePage'] - 1].get_text().split())
            for answer in record['answers']:
                assert answer in scheme_text, (year, answer)
            for gap, alternatives in record.get('acceptedAlternatives', {}).items():
                assert 1 <= int(gap) <= 10
                assert all(answer in words and answer in scheme_text for answer in alternatives)
            for phrase in ['10 gaps for 3 marks each', 'Careless transcription, including accents, deduct 1 mark.', 'Accept capital letters.']:
                assert phrase in scheme_text, (year, phrase)
        if record.get('salutation'):
            salutation = record['salutation']
            assert text.count(salutation) == 1, year
            letter_start = text.index(salutation) + len(salutation)
        else:
            letter_start = re.search(r'Ch(?:er|ère) [^,]+,', text).end()
        body = text[letter_start:].strip()
        counter = iter(range(1, 11))
        numbered = re.sub(r'_{3,}', lambda _: f'[{next(counter)}]', body)
        entry = next(e for e in entries if e['year'] == year and e['level'] == 'ordinary' and e['lang'] == 'ev')
        doc = next(p for p in entry['papers'] if p['label'] == 'Exam Paper')
        paper_tag = next(p for p in tags if p['year'] == year and p['level'] == 'ordinary' and p['fileid'] == doc['doc']['f'])
        tag = next(q for q in paper_tag['q'] if q['n'] == 'B1A')
        topic_indexes = next(m[5] for m in runtime['questionMappings'] if m[:5] == ['o', 'e', year - 2000, 's', 'B1A'])
        for gap, answer in enumerate(record['answers'], 1):
            accepted = ' / '.join([answer] + record.get('acceptedAlternatives', {}).get(str(gap), []))
            sentences = re.split(r'(?<=[.!?])\s+', numbered)
            excerpt = next(sentence for sentence in sentences if f'[{gap}]' in sentence)
            n, cid = f'B1A-gap-{gap}', f'fr-{year}-ol-cloze-b1a-gap-{gap}'
            prompt = (f'Complétez l’espace [{gap}] de la lettre avec un mot de la liste. '
                      'Les espaces sont numérotés dans l’ordre du texte.\n\n'
                      f'{excerpt}\n\nMots proposés : {", ".join(words)}')
            source = dict(kind='source-text', label='Original letter', title=f'Section B · Q1(a) — gap {gap}', pages=[page],
                          attribution=f'SEC French {year} Ordinary Level examination paper — © State Examinations Commission.',
                          presentationNote='Read the complete letter and its word bank. Gaps are counted in the order they appear in the original letter.')
            card = dict(id=cid, subjectId='french', level='ordinary', source='sec', kind='rubric', year=year,
                        paperFileid=doc['doc']['f'].removesuffix('.pdf'), section='B', questionRef=f'{year} OL Section B Q1(a) · gap {gap}',
                        questionText=prompt, topicId=tag['primary'], conceptId='cloze-letter-gap-fill', totalMarks=3,
                        sourceMaterial=source, specVersion='lc-french-syllabus',
                        schemeCitation=f'SEC French {year} Ordinary Level marking scheme, p.{record["schemePage"]} — © State Examinations Commission.',
                        schemeRegion=dict(schemeFileid=doc['scheme']['f'], p=record['schemePage'], r=[0, 0, 1, 1]),
                        rubric=dict(system='french', taskRequirements=['Complete only the selected gap.'], answerGuide=[f'Gap {gap}: {accepted} — 3 marks.', 'Careless transcription, including accents, deduct 1 mark. Accept capital letters.'],
                                    criteria=[dict(id='response', label='Response', maxMarks=3, permittedMarks=[0, 2, 3], guidance=['3 marks for the correct word; 2 if a transcription error is the only fault; otherwise 0.'])],
                                    markingGuideNote='The complete exercise awards 3 marks for each of ten gaps. This card assesses one gap.'),
                        qa=dict(gates=['visual-paper-scheme-review', 'published-gap-tariff', 'selection-review'], humanReviewedBy='agent-verified', humanReviewedAt=review['reviewedAt']))
            cards.append(card)
            tasks.append(dict(cardId=cid, subjectId='french', level='ordinary', year=year, sitting='main', paperKey='single', lang='ev', fileid=doc['doc']['f'],
                              n=n, parent='B1A', topicIds=[runtime['topics'][i][0] for i in topic_indexes], topicId=tag['primary'], pages=[page], label=f'Section B · Q1(a) · gap {gap}'))
    assert len(cards) == review['expectedCards']
    (ROOT / 'components/MarkBank/cards/french/cloze.json').write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
    write_tasks('cloze', tasks)
    print(f'Wrote {len(cards)} reviewed gap tasks and exact Atlas identities.')


if __name__ == '__main__':
    build()
