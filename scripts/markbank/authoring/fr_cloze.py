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
        with fitz.open(paper.path) as source_pdf:
            printed_page = source_pdf[page - 1].get_text(sort=True)
        compact = lambda value: re.sub(r'\s+', '', value)
        # The bilingual column reader can drop words printed past its column
        # bound. Each repair restores text visually verified on the page: the
        # extracted run must occur once and the restored run must be printed.
        for repair in record.get('letterRepairs', []):
            assert text.count(repair['extracted']) == 1 and repair['reason'], (year, repair)
            assert compact(repair['printed']) in compact(printed_page), (year, repair)
            text = text.replace(repair['extracted'], repair['printed'])
        assert len(re.findall(r'_{3,}', text)) == 10
        bank_start = text.index('(N.B.')
        bank_start = text.index(')', bank_start) + 1
        # The paper's own instruction, exactly as printed above the word bank.
        instruction = ' '.join(text[:bank_start].split())
        assert instruction.startswith('Complétez la lettre') and compact(instruction) in compact(printed_page), year
        # Ten comma-separated words precede the location/date, which are not
        # part of the bank. The final word is one token in every reviewed paper.
        if record.get('wordBank'):
            # Some full-width banks cross the bilingual column boundary.
            # Pin all ten words to the original page, preserving their order.
            words = record['wordBank']
            assert len(words) == 10 and record['wordBankReason']
            assert compact(','.join(words)) in compact(printed_page), year
        else:
            words = text[bank_start:].strip().split(',', 9)
            words = [word.strip() for word in words[:9]] + [words[9].split()[0]]
        assert set(words) == set(record['answers']), (year, words)
        # The bank as printed: its words, commas and (where printed) final stop.
        bank = ', '.join(words)
        if compact(bank + '.') in compact(printed_page):
            bank += '.'
        assert compact(bank) in compact(printed_page), year
        with fitz.open(ROOT / f'examiner-reports/french/schemes/{year}-ol.pdf') as scheme:
            scheme_text = ' '.join(scheme[record['schemePage'] - 1].get_text().split())
            for answer in record['answers']:
                assert answer in scheme_text, (year, answer)
            # A gap-specific N.B. printed under the answer list (2011 gap 9:
            # "accept « tout » for 3 marks if not already accepted in Gap 1").
            for gap, note in record.get('gapNotes', {}).items():
                assert 1 <= int(gap) <= 10 and note in scheme_text, (year, gap, note)
            for gap, alternatives in record.get('acceptedAlternatives', {}).items():
                assert 1 <= int(gap) <= 10
                assert all(answer in words and answer in scheme_text for answer in alternatives)
            # 2012 excepts one word from the capital-letter allowance; lift the year's own line.
            capitals = record.get('capitalLetters', 'Accept capital letters.')
            # Each gap's entry in the scheme's numbered answer list, as printed
            # (2019 prints "6 travaille" without a stop; 2020 "2. passe/serai").
            list_entries = {}
            for gap, answer in enumerate(record['answers'], 1):
                entry = record.get('answerListEntries', {}).get(str(gap), f'{gap}. {answer}')
                assert re.search(r'(?<!\S)' + re.escape(entry) + r'(?=\s|$)', scheme_text), (year, gap, entry)
                list_entries[gap] = entry
            # Where the numbered list misprints or omits an answer, the scheme's
            # completed letter prints it; lift that line too.
            evidence = record.get('answerEvidence', {})
            for gap, item in evidence.items():
                assert item['printed'] in scheme_text and item['note'], (year, gap)
            for phrase in ['10 gaps for 3 marks each', 'Careless transcription, including accents, deduct 1 mark.', capitals]:
                assert phrase in scheme_text, (year, phrase)
        if record.get('salutation'):
            salutation = record['salutation']
            assert text.count(salutation) == 1, year
            letter_start = text.index(salutation) + len(salutation)
        else:
            letter_start = re.search(r'Ch(?:er|ère) [^,]+,', text).end()
        body = text[letter_start:].strip()
        # Fail closed on any dropped word or mark: apart from whitespace, the
        # whole letter body every gap excerpt is cut from is the printed page.
        assert compact(body) in compact(printed_page), (year, 'letter body differs from the printed page')
        blanks = re.findall(r'_{3,}', body)
        counter = iter(range(1, 11))
        numbered = re.sub(r'_{3,}', lambda _: f'[{next(counter)}]', body)
        entry = next(e for e in entries if e['year'] == year and e['level'] == 'ordinary' and e['lang'] == 'ev')
        doc = next(p for p in entry['papers'] if p['label'] == 'Exam Paper')
        paper_tag = next(p for p in tags if p['year'] == year and p['level'] == 'ordinary' and p['fileid'] == doc['doc']['f'])
        tag = next(q for q in paper_tag['q'] if q['n'] == 'B1A')
        topic_indexes = next(m[5] for m in runtime['questionMappings'] if m[:5] == ['o', 'e', year - 2000, 's', 'B1A'])
        for gap, answer in enumerate(record['answers'], 1):
            sentences = re.split(r'(?<=[.!?])\s+', numbered)
            excerpt = next(sentence for sentence in sentences if f'[{gap}]' in sentence)
            # Only this card's gap carries its number; any other gap in the same
            # sentence keeps the printed blank, so the target is unambiguous.
            excerpt = re.sub(r'\[(\d+)\]', lambda m: m.group(0) if int(m.group(1)) == gap else blanks[int(m.group(1)) - 1], excerpt)
            n, cid = f'B1A-gap-{gap}', f'fr-{year}-ol-cloze-b1a-gap-{gap}'
            prompt = f'{instruction}\n\n{bank}\n\n{excerpt}'
            gap_evidence = evidence.get(str(gap))
            source = dict(kind='source-text', label='Original letter', title=f'Section B · Q1(a) — gap {gap}', pages=[page],
                          attribution=f'SEC French {year} Ordinary Level examination paper — © State Examinations Commission.',
                          presentationNote='Read the complete letter and its word bank. Gaps are counted in the order they appear in the original letter.')
            card = dict(id=cid, subjectId='french', level='ordinary', source='sec', kind='rubric', year=year,
                        paperFileid=doc['doc']['f'].removesuffix('.pdf'), section='B', questionRef=f'{year} OL Section B Q1(a) · gap {gap}',
                        questionText=prompt, topicId=tag['primary'], conceptId='cloze-letter-gap-fill', totalMarks=3,
                        sourceMaterial=source, specVersion='lc-french-syllabus',
                        schemeCitation=f'SEC French {year} Ordinary Level marking scheme, p.{record["schemePage"]} — © State Examinations Commission.',
                        schemeRegion=dict(schemeFileid=doc['scheme']['f'], p=record['schemePage'], r=[0, 0, 1, 1]),
                        rubric=dict(system='french', taskRequirements=[],
                                    answerGuide=[list_entries[gap], *([gap_evidence['printed']] if gap_evidence else []),
                                                 *([record['gapNotes'][str(gap)]] if str(gap) in record.get('gapNotes', {}) else []),
                                                 '10 gaps for 3 marks each', f'Careless transcription, including accents, deduct 1 mark. {capitals}'],
                                    criteria=[dict(id='response', label='Response', maxMarks=3, permittedMarks=[0, 2, 3], guidance=[])],
                                    markingGuideNote='',
                                    # Our guidance, shown under the app's own label, never as scheme text.
                                    practiceNotes=[f'This card practises gap [{gap}] only; any other numbered gap in the excerpt is a separate card.',
                                                   'Score 3 for the correct word, 2 when careless transcription is the only fault (the scheme deducts 1 mark), otherwise 0.',
                                                   *([gap_evidence['note']] if gap_evidence else [])]),
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
