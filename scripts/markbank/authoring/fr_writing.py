#!/usr/bin/env python3
"""Reviewed French writing additions. Run from any cwd; no legacy card is edited.

The source manifest records year-specific prompts and pages compared with
the original papers and marking schemes.
The inventory remains explicitly partial until every archive paper is reviewed.
"""
from pathlib import Path
from itertools import combinations
import json
import re
import hashlib
import fitz
from fr_paper import FrPaper
from fr_selection import verify_paper
from fr_reviewed_tasks import write_tasks

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'components/MarkBank/cards/french/writing.json'
DATA = ROOT / 'examiner-reports/french'


def norm(text):
    return re.sub(r'[^\w]', '', text.lower().replace('‐', '-'))


def assert_on_page(text, doc, page):
    assert norm(text) in norm(doc[page - 1].get_text()), (page, text)


HYPHENS = str.maketrans({'\u2010': '-', '\u2011': '-'})


def compact(text):
    """Whitespace removed and hyphen glyphs unified; every other character kept."""
    return re.sub(r'\s+', '', text).translate(HYPHENS)


def assert_exact(text, doc, pages, left=None):
    """Lift, never write: the entry must be the page's own characters."""
    for page in pages:
        pg = doc[page - 1]
        clip = fitz.Rect(left, 0, pg.rect.width, pg.rect.height) if left else None
        if compact(text) in compact(pg.get_text(clip=clip)):
            return
    raise AssertionError(('not printed verbatim', pages, text))


def lift(descriptors, doc, page):
    """Each grid descriptor as that scheme page prints it.

    The shared lists only name the descriptors. The words are matched in order
    where a printed line begins (after any bullet glyph, dash or band range, but
    never after another word, so "Mistakes in register" cannot match inside
    "Few mistakes in register"), and the card keeps the page's own
    capitalisation and internal punctuation: 2017 Higher prints "idiomatic
    French", 2013 Ordinary prints "Most words misspelt".
    """
    text, starts = '', set()
    for line in doc[page - 1].get_text().splitlines():
        line = ' '.join(line.split())
        if not line:
            continue
        if text:
            text += ' '
        starts.add(len(text))
        text += line
    lifted = []
    for descriptor in descriptors:
        words = re.findall(r'\w+', descriptor)
        pattern = re.compile(r'(?<!\w)' + r'\W+'.join(map(re.escape, words)) + r'(?!\w)', re.I)
        found = set()
        for m in pattern.finditer(text):
            line_start = max(start for start in starts if start <= m.start())
            if not re.search(r'[^\W\d_]', text[line_start:m.start()]):
                found.add(m.group(0))
        assert len(found) == 1, (page, descriptor, found)
        lifted.append(found.pop())
    return lifted


def criterion(id, label, maximum, guidance, bands=None, allowed=None):
    return dict(id=id, label=label, maxMarks=maximum,
                permittedMarks=allowed or list(range(maximum + 1)), guidance=guidance,
                **({'bands': bands} if bands else {}))


def bands(ranges, guidance):
    return [dict(label=label, marks=list(range(lo, hi + 1)), guidance=notes)
            for label, (lo, hi), notes in zip(['Top', 'Middle', 'Bottom'], ranges, guidance)]


COMMUNICATION = [
    ['Stimulus material well exploited', 'High level of textual coherence', 'Clarity in argumentation',
     'Communicative intention fulfilled', 'Little or no irrelevant material', 'Few mistakes in register'],
    ['More or less competent treatment of stimulus material', 'Reasonable level of textual coherence',
     'Comprehensible for French monoglot', 'Communicative intention more or less respected',
     'Some irrelevant material', 'Not too many mistakes in register'],
    ['Mere transcription or very poor treatment of stimulus material', 'Lack of textual coherence',
     'French monoglot would have difficulty understanding', 'Communicative intention stultified',
     'A lot of irrelevant material', 'Mistakes in register'],
]
HL_LANGUAGE = [
    ['Idiomatic French', 'Rich vocabulary', 'Complex sentences well handled', 'Few mistakes in verbs, agreement or spelling'],
    ['Vocabulary adequate', 'Verbs generally correct', 'Rule of agreement generally respected', 'Not too many mistakes in spelling'],
    ['Problems with vocabulary', 'Most verbs incorrect', 'Basic rule of agreement not respected', 'Many mistakes in spelling'],
]
OL_LANGUAGE = [
    ['very good range of vocabulary', 'verb endings, agreements, tenses nearly always correct',
     'nearly all words spelt correctly', 'good sense of register'],
    ['reasonable to good range of vocabulary', 'verb endings, tenses, agreements correct more often than incorrect',
     'at least half the words spelt correctly', 'some sense of register'],
    ['very poor to poor use of vocabulary', 'most verb endings, tenses, agreements incorrect',
     'most words misspelt', 'no sense of register'],
]

# Each Ordinary Level message/postcard/diary/letter prints its own communication
# tariff as an underlined heading on its scheme page. Lift it verbatim, never a
# shared paraphrase: 2012–2021 print "Two points" on all four tasks; 2022–2026
# print "Two parts" for B2A/B2B and "Two points" for B3A/B3B. Entries are
# (scheme PDF page, exact printed line); every line was checked against the
# rendered scheme page (2015–2026 on 11 October 2026; 2014 and 2013 on 11 October
# 2026 from their own scheme pages 12–15, 2012 from pages 11–14). A year without
# an entry fails.
POINTS_5 = 'Two points required for 5 marks (3 + 2)'
PARTS_5 = 'Two parts required for 5 marks (3 + 2)'
POINTS_4 = 'Two points required for 4 marks (2 + 2)'
OL_POINT_TARIFFS = {
    2012: {'B2A': (11, POINTS_5), 'B2B': (12, POINTS_5), 'B3A': (13, POINTS_5), 'B3B': (14, POINTS_4)},
    2013: {'B2A': (12, POINTS_5), 'B2B': (13, POINTS_5), 'B3A': (14, POINTS_5), 'B3B': (15, POINTS_4)},
    2014: {'B2A': (12, POINTS_5), 'B2B': (13, POINTS_5), 'B3A': (14, POINTS_5), 'B3B': (15, POINTS_4)},
    2015: {'B2A': (12, POINTS_5), 'B2B': (13, POINTS_5), 'B3A': (14, POINTS_5), 'B3B': (15, POINTS_4)},
    2016: {'B2A': (12, POINTS_5), 'B2B': (13, POINTS_5), 'B3A': (14, POINTS_5), 'B3B': (15, POINTS_4)},
    2017: {'B2A': (14, POINTS_5), 'B2B': (15, POINTS_5), 'B3A': (16, POINTS_5), 'B3B': (17, POINTS_4)},
    2018: {'B2A': (14, POINTS_5), 'B2B': (15, POINTS_5), 'B3A': (16, POINTS_5), 'B3B': (17, POINTS_4)},
    2019: {'B2A': (12, POINTS_5), 'B2B': (13, POINTS_5), 'B3A': (14, POINTS_5), 'B3B': (15, POINTS_4)},
    2020: {'B2A': (14, POINTS_5), 'B2B': (15, POINTS_5), 'B3A': (16, POINTS_5), 'B3B': (17, POINTS_4)},
    2021: {'B2A': (14, POINTS_5), 'B2B': (15, POINTS_5), 'B3A': (16, POINTS_5), 'B3B': (17, POINTS_4)},
    2022: {'B2A': (13, PARTS_5), 'B2B': (14, PARTS_5), 'B3A': (15, POINTS_5), 'B3B': (16, POINTS_4)},
    2023: {'B2A': (13, PARTS_5), 'B2B': (14, PARTS_5), 'B3A': (15, POINTS_5), 'B3B': (16, POINTS_4)},
    2024: {'B2A': (15, PARTS_5), 'B2B': (16, PARTS_5), 'B3A': (17, POINTS_5), 'B3B': (18, POINTS_4)},
    2025: {'B2A': (14, PARTS_5), 'B2B': (15, PARTS_5), 'B3A': (16, POINTS_5), 'B3B': (17, POINTS_4)},
    2026: {'B2A': (16, PARTS_5), 'B2B': (17, PARTS_5), 'B3A': (18, POINTS_5), 'B3B': (19, POINTS_4)},
}


def printed_tariff(year, parent, scheme_ol, scheme_page, maximum):
    """Return the verified tariff line, asserting it is the page's only one."""
    assert year in OL_POINT_TARIFFS, f'No verified OL communication tariff wording for {year}'
    assert parent in OL_POINT_TARIFFS[year], f'No verified OL communication tariff wording for {year} {parent}'
    page, line = OL_POINT_TARIFFS[year][parent]
    assert page == scheme_page, (year, parent, page, scheme_page)
    assert line.endswith(f'for {maximum} marks ({maximum - 2} + 2)'), (year, parent, line, maximum)
    printed = [re.sub(r'\s+', ' ', text).strip() for text in scheme_ol[page - 1].get_text().splitlines()]
    assert [text for text in printed if re.search(r'required for \d+ marks', text)] == [line], (year, parent, page)
    return line


def communication_notes(config, scheme_ol, page):
    """A year's printed communication N.B. (2010–2014 print one on each OL
    writing page), asserted verbatim on that page. A page that prints the
    note while the year's source entry omits it fails rather than drops it."""
    printed = ' '.join(scheme_ol[page - 1].get_text().split())
    note = config.get('olCommunicationNote')
    if note is None:
        assert 'Correct tense required' not in printed, (config['year'], page)
        return []
    assert note in printed, (config['year'], page, note)
    return [note]


def language(maximum, descriptors):
    ranges = {8: [(6, 8), (3, 5), (0, 2)], 12: [(9, 12), (5, 8), (0, 4)],
              15: [(11, 15), (6, 10), (0, 5)]}[maximum]
    return criterion('language', 'Language', maximum, [], bands(ranges, descriptors))


def build_year(config):
    YEAR = config['year']
    for level in ['hl', 'ol']:
        verify_paper(DATA / f'papers/{YEAR}-{level}-000-paper.pdf')
    ol_language = [list(notes) for notes in OL_LANGUAGE]
    if config['languageBottom'] is None:
        # The 2021 scheme has only three bottom-band descriptors. Do not
        # import the additional vocabulary criterion from a later year.
        ol_language[2] = ol_language[2][1:]
    else:
        ol_language[2][0] = config['languageBottom']
    index_text = (ROOT / 'paperTrailData.ts').read_text()
    block = index_text.split('  "french": [', 1)[1].split('\n  ],', 1)[0]
    entries = [json.loads(line.strip().rstrip(',')) for line in block.splitlines() if line.strip()]
    tags = json.loads((ROOT / 'scripts/paper-trail/topic-tags/tags/french.json').read_text())
    runtime = json.loads((ROOT / 'data/examTopics/french-runtime.json').read_text())
    cards, mappings, audit = [], [], []

    def add(level, n, parent, prompt, page, scheme_page, criteria, requirements=None, passage=None):
        entry = next(e for e in entries if e['year'] == YEAR and e['level'] == level and e['lang'] == 'ev')
        item = next(p for p in entry['papers'] if p['label'] == 'Exam Paper')
        paper = next(p for p in tags if p['year'] == YEAR and p['level'] == level and p['fileid'] == item['doc']['f'])
        tag = next(q for q in paper['q'] if q['n'] == parent)
        topic_indexes = next(m[5] for m in runtime['questionMappings']
                             if m[:5] == [level[0], 'e', YEAR - 2000, 's', parent])
        cid = f'fr-{YEAR}-{"hl" if level == "higher" else "ol"}-writing-{n.lower()}'
        printed = re.fullmatch(r'B(\d+)([A-C]?)', parent)
        reference = 'Q' + printed[1] + (f'({printed[2].lower()})' if printed[2] else '')
        if '-route-' in n:
            reference += ' · points ' + ', '.join(n.split('-')[-1])
        if '-field-' in n:
            reference += ' · field ' + n.split('-')[-1]
        source = dict(kind='source-text', label=f'Section B · {parent}', title='Printed writing task',
                      pages=[page], attribution=f'SEC French {YEAR} {level.title()} Level — © State Examinations Commission.',
                      presentationNote='Open the original task, including its illustrations and layout, then return to your answer.')
        card = dict(id=cid, subjectId='french', level=level, source='sec', kind='rubric', year=YEAR,
                    paperFileid=item['doc']['f'].removesuffix('.pdf'), section='B',
                    questionRef=f'{YEAR} {"HL" if level == "higher" else "OL"} Section B {reference}',
                    questionText=prompt, totalMarks=sum(c['maxMarks'] for c in criteria),
                    topicId=tag['primary'], conceptId=f'french-writing-{tag["primary"]}',
                    sourceMaterial=source, specVersion='lc-french-syllabus',
                    schemeCitation=f'SEC French {YEAR} {level.title()} Level marking scheme, p.{scheme_page} — © State Examinations Commission.',
                    schemeRegion=dict(schemeFileid=item['scheme']['f'], p=scheme_page, r=[0, 0, 1, 1]),
                    qa=dict(gates=['paper-prompt', 'published-french-grid', 'finite-route-expansion', 'visual-paper-scheme-review'],
                            humanReviewedBy='agent-verified', humanReviewedAt='2026-10-07'),
                    rubric=dict(system='french', taskRequirements=requirements or [], criteria=criteria,
                                markingGuideNote='Use the published descriptors to assess the response you wrote. The marks apply to this selected task; alternative routes are not added together.'))
        if level == 'higher' and config.get('hlSchemePageOffset'):
            printed_page = scheme_page + config['hlSchemePageOffset']
            card['schemeCitation'] = card['schemeCitation'].replace(f'p.{scheme_page}', f'p.{printed_page} (PDF page {scheme_page})')
        if passage:
            card['additionalSourceMaterials'] = [{**source, 'label': 'Section A passage', 'title': 'Reading passage referenced by this task', 'pages': passage}]
        task_notes = config.get('taskSourceNotes', {}).get(level, {})
        source_note = task_notes.get(n, task_notes.get(parent))
        if source_note:
            card['rubric']['taskRequirements'].append(source_note)
        cards.append(card)
        mappings.append(dict(cardId=cid, subjectId='french', level=level, year=YEAR, sitting='main',
                             paperKey='single', lang='ev', fileid=item['doc']['f'], n=n, parent=parent,
                             topicIds=[runtime['topics'][i][0] for i in topic_indexes],
                             topicId=tag['primary'], pages=sorted(set([page] + (passage or []))),
                             label=f'Section B · {reference}'))

    paper = FrPaper(YEAR, 'hl')
    hl_doc = fitz.open(paper.path)
    scheme_hl = fitz.open(DATA / f'schemes/{YEAR}-hl.pdf')
    for notes in COMMUNICATION + HL_LANGUAGE:
        for note in notes:
            assert_on_page(note, scheme_hl, config['hlGridPage'])
    hl_communication = [lift(notes, scheme_hl, config['hlGridPage']) for notes in COMMUNICATION]
    hl_language = [lift(notes, scheme_hl, config['hlGridPage']) for notes in HL_LANGUAGE]
    for q, letter, prompt, page in paper.section_b_asks():
        parent = f'B{q}{(letter or "").upper()}'
        task_grid = config.get('hlTaskGrids', {}).get(parent, {})
        maximum = task_grid.get('criteriaMax', config['hlCriteriaMax'][0 if q == 1 else 1])
        ranges = {30: [(20, 30), (12, 19), (0, 11)],
                  20: [(13, 20), (8, 12), (0, 7)],
                  15: [(11, 15), (6, 10), (0, 5)],
                  12: [(9, 12), (5, 8), (0, 4)]}[maximum]
        override = config.get('hlPromptParagraphs', {}).get(parent)
        if override:
            for paragraph in override:
                assert_on_page(paragraph, hl_doc, page)
            prompt = '\n\n'.join(override)
        else:
            assert_on_page(prompt, hl_doc, page)
        prompt = prompt.replace('\uf0b7', '\n•')
        if YEAR <= 2021:
            prompt = prompt.replace(' •', '\n•')
        prompt = re.sub(r' (?=- Est)', '\n', prompt) if q == 3 else prompt
        if q == 3 and YEAR == 2026:
            prompt = prompt.replace(' - Comment', '\n- Comment').replace(' - Avez', '\n- Avez')
        word_count = 90 if q == 1 else 75
        # The paper's own word-count line: a task printed in English (2013,
        # 2016, 2018, 2020 Q2(b)) ends "(about 75 words)", not the French line.
        count_line = config.get('hlWordCountLines', {}).get(parent, f'({word_count} mots environ)')
        assert_exact(count_line, hl_doc, [page])
        prompt += '\n' + count_line
        criteria = [criterion('communication', 'Communication', maximum, [], bands(ranges, hl_communication)),
                    criterion('language', 'Language', maximum, [], bands(ranges, hl_language))]
        if task_grid.get('formatMarks'):
            assert_on_page('Formule', scheme_hl, config['hlGridPage'] - 1)
            criteria.insert(0, criterion('format', 'Formule · letter format', task_grid['formatMarks'],
                task_grid['formatGuidance']))
        if parent in config.get('hlNoLayoutTasks', []) or (
                'hlNoLayoutTasks' not in config and q == config['hlNoLayoutQuestion']):
            note = config.get('hlNoLayoutNote', f'Q. {q} – no particular layout required')
            assert_on_page(note, scheme_hl, config['hlGridPage'] - 1)
            criteria[0]['guidance'] = [note.rstrip('.') + '.']
        if q == 1:
            ref = re.search(r'Section\s*(?:A|I),\s*Q[.,]\s*([12])', prompt, re.I)
            assert ref and int(ref[1]) == config['hlPassageRefs'][parent], (YEAR, parent, prompt)
        add('higher', parent, parent, prompt, page, config['hlGridPage'], criteria,
            [f'Answer in French, approximately {word_count} words.'],
            passage=paper.rc_pages[config['hlPassageRefs'][parent]] if q == 1 else None)
        if task_grid.get('formatMarks'):
            offset = config.get('hlSchemePageOffset', 0)
            pages = [config['hlGridPage'] - 1, config['hlGridPage']]
            cards[-1]['schemeCitation'] = (f'SEC French {YEAR} Higher Level marking scheme, '
                f'pp.{pages[0] + offset}–{pages[1] + offset} (PDF pages {pages[0]}–{pages[1]}) '
                '— © State Examinations Commission.')
        if parent in config['illustrationTasks']:
            cards[-1]['sourceMaterial'].update(
                kind='source-illustration', label='Writing illustration',
                title='Original writing prompt and illustration',
                presentationNote='Open the illustration before answering the prompt.')

    doc = fitz.open(DATA / f'papers/{YEAR}-ol-000-paper.pdf')
    scheme_ol = fitz.open(DATA / f'schemes/{YEAR}-ol.pdf')
    format_page = config['formatSchemePage']
    format_pages = config.get('formatSchemePages', [format_page])
    format_notes = config['formatNotes']
    for note in format_notes['top'] + format_notes['close'] + format_notes['deductions']:
        assert any(norm(note) in norm(scheme_ol[p - 1].get_text()) for p in format_pages), note
        assert_exact(note, scheme_ol, format_pages)
    for notes in ol_language:
        for note in notes:
            assert_on_page(note, scheme_ol, config['olLanguagePage'])
    ol_language_names = ol_language
    ol_language = [lift(notes, scheme_ol, config['olLanguagePage']) for notes in ol_language_names]
    form_stem = config['form_stem']
    assert_on_page(form_stem, doc, config['formPage'])
    assert_exact(form_stem, doc, [config['formPage']])
    fields = config['fields']
    answers = config['answers']
    for number, (field, answer) in enumerate(zip(fields, answers), 1):
        assert_on_page(field, doc, config['formPage'])
        assert_on_page(answer, scheme_ol, config['formSchemePage'])
        assert_exact(field, doc, [config['formPage']])
        assert_exact(answer, scheme_ol, [config['formSchemePage']])
        add('ordinary', f'B1B-field-{number}', 'B1B', f'{form_stem}\n\n{number}. {field} :', config['formPage'], config['formSchemePage'],
            [criterion('answer', field, 2, [answer], allowed=config.get('fieldAllowed', {}).get(str(number), [0, 2]))])
    form_questions = config['form_questions']
    assert len(fields) == len(answers) == 5 and len(form_questions) == 4
    for prompt in form_questions:
        assert_on_page(prompt, doc, config['formPage'])
        assert_exact(prompt, doc, [config['formPage']])
    # 2012 prints the form's tense N.B. at the top of the following scheme page.
    form_notes = communication_notes(config, scheme_ol, config.get('formNotePage', config['formSchemePage']))
    # A scheme may price one form sentence with its own condition (2012 Q7:
    # "Two or more sports required here for full marks"); lift it verbatim.
    form_question_notes = config.get('formQuestionNotes', {})
    form_scheme_text = ' '.join(scheme_ol[config['formSchemePage'] - 1].get_text().split())
    for number, note in form_question_notes.items():
        assert number in {'6', '7', '8', '9'} and note in form_scheme_text, (YEAR, number, note)
    form_choose = config.get('formChoose', 3)
    assert form_choose in [3, 4]
    assert_on_page(config.get('formInstruction', 'Pour 6, 7, 8 et 9 : choisissez trois questions et répondez par des phrases complètes.'), doc, config['formPage'])
    for chosen in combinations(range(4), form_choose):
        selected = [f'{i+6}. {form_questions[i]}' for i in chosen]
        maximum = 12 // form_choose
        clear = '3' if maximum == 3 else '3–4'
        criteria = [criterion(f'communication-{i+6}', f'Communication · question {i+6}', maximum,
                              [form_questions[i], f'0–2: message not clear. {clear}: message clear.',
                               *([form_question_notes[str(i + 6)]] if str(i + 6) in form_question_notes else []),
                               *form_notes]) for i in chosen]
        lang = language(8, ol_language)
        lang['requiresAttempt'] = True
        criteria.append(lang)
        suffix = ''.join(str(i+6) for i in chosen)
        add('ordinary', f'B1B-route-{suffix}', 'B1B', form_stem + '\n\n' + '\n'.join(selected), config['formPage'], config['formSchemePage'], criteria,
            ['Answer all four questions in complete French sentences.' if form_choose == 4 else 'Answer the three selected questions in complete French sentences.'])

    pools = config['pools']
    assert {pool[0] for pool in pools} == {'B2A', 'B2B', 'B3A', 'B3B'}
    for parent, page, scheme_page, stem, points, answers in pools:
        task_language = ol_language
        language_override = config.get('olTaskLanguageOmit', {}).get(parent)
        if language_override:
            omitted = language_override['descriptors']
            source_text = norm(scheme_ol[language_override['page'] - 1].get_text())
            for descriptor in omitted:
                assert norm(descriptor) not in source_text, (YEAR, parent, descriptor)
            task_names = [[note for note in notes if note not in omitted] for notes in ol_language_names]
            for notes in task_names:
                for note in notes:
                    assert_on_page(note, scheme_ol, language_override['page'])
            task_language = [lift(notes, scheme_ol, language_override['page']) for notes in task_names]
        # Check the English column separately: text extraction of the whole
        # bilingual page interleaves Irish and English in some SEC editions.
        clip_text = doc[page-1].get_text(clip=fitz.Rect(290, 0, doc[page-1].rect.width, doc[page-1].rect.height))
        assert norm(stem) in norm(clip_text), (parent, stem)
        assert len(points) in [3, 5]
        if len(points) == 5:
            assert 'three' in clip_text.lower()
        assert_exact(stem, doc, [page], 290)
        for point, answer in zip(points, answers):
            assert point.strip() and answer.strip(), (YEAR, parent)
            assert norm(point) in norm(clip_text), (parent, point)
            assert_on_page(answer, scheme_ol, scheme_page)
            assert_exact(point, doc, [page], 290)
            assert_exact(answer, scheme_ol, [scheme_page])
        if parent == 'B3A':
            # Each year's own diary instruction, e.g. "Note the following in your
            # diary:" (2012–2016) or "Note three of the following five points in
            # French in your diary:" (2021–2026).
            diary_instruction = config['diaryInstruction']
            assert_exact(diary_instruction, doc, [page], 290)
        for chosen in combinations(range(len(points)), 3):
            suffix = ''.join(str(i+1) for i in chosen)
            maximum = 4 if parent == 'B3B' else 5
            tariff = printed_tariff(YEAR, parent, scheme_ol, scheme_page, maximum)
            notes = communication_notes(config, scheme_ol, scheme_page)
            criteria = [criterion(f'communication-{i+1}', f'Communication · point {i+1}', maximum,
                                  [answers[i], tariff + '.', *notes,
                                   'Assess how clearly each part is communicated.']) for i in chosen]
            if parent == 'B3B':
                criteria = [criterion('format-top', 'Format · top of page', 3,
                                      ['France not necessary in address.'] + format_notes['top'] + format_notes['deductions']),
                            criterion('format-close', 'Format · closing formula', 3,
                                      format_notes['close'] + format_notes['deductions'])] + criteria
            lang = language(12 if parent == 'B3B' else 15, task_language)
            if parent == 'B3B':
                lang['requiresAttempt'] = True
            criteria.append(lang)
            context = stem + (' ' + diary_instruction if parent == 'B3A' else '')
            context += '\n\n' + '\n'.join(f'• {points[i]}' for i in chosen)
            if parent == 'B3B':
                context += '\n\n' + config['letterIdentity']
                assert norm(config['letterIdentity']) in norm(clip_text)
                assert_exact(config['letterIdentity'], doc, [page], 290)
            add('ordinary', f'{parent}-route-{suffix}', parent, context, page, scheme_page, criteria,
                ['Write in French and include all three required points.' if len(points) == 3 else 'Write in French and include all three points selected for this practice route.',
                 'No marks for layout.' if parent != 'B3B' else 'Use the formal letter layout and the supplied addresses.'])
            if parent == 'B3B':
                cards[-1]['schemeCitation'] = cards[-1]['schemeCitation'].replace(
                    f'p.{scheme_page}', 'pp.' + ', '.join(map(str, [scheme_page, *format_pages])))
        audit.append(dict(year=YEAR, level='ordinary', question=parent, choose=3, poolSize=len(points),
                          routes=len(list(combinations(points, 3))), paperPage=page, schemePage=scheme_page))

    audit.append(dict(year=YEAR, level='ordinary', question='B1B', choose=form_choose, poolSize=4, routes=len(list(combinations(form_questions, form_choose))),
                      separatelyMarkedFields=5, paperPage=config['formPage'], schemePage=config['formSchemePage']))
    audit.append(dict(year=YEAR, level='higher', question='B', routes=len(paper.section_b_asks()), paperPages=sorted({ask[3] for ask in paper.section_b_asks()}), schemePages=[config['hlGridPage'] - 1, config['hlGridPage']],
                      notes=config.get('hlSelectionNote', f'Q1a/b/c are alternatives. Q{config["hlNoLayoutQuestion"]} email bullets are all required. Q1c real/imaginary is open creative scope, not a finite response pool.')))
    for level in ['hl', 'ol']:
        for kind, suffix in [('papers', '-000-paper'), ('schemes', '')]:
            file = DATA / kind / f'{YEAR}-{level}{suffix}.pdf'
            audit.append(dict(source=str(file.relative_to(ROOT)), sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
    return cards, mappings, audit


def build():
    configs = json.loads((ROOT / 'scripts/markbank/authoring/french-writing-sources.json').read_text())
    cards, mappings, audit = [], [], []
    for config in configs:
        new_cards, new_mappings, new_audit = build_year(config)
        cards.extend(new_cards)
        mappings.extend(new_mappings)
        audit.extend(new_audit)
    OUT.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
    write_tasks('writing', mappings)
    (ROOT / 'scripts/markbank/authoring/french-writing-review.json').write_text(json.dumps(dict(
        status='partial-corpus-review', reviewedAt='2026-10-07', cards=len(cards), review=audit,
        examSelectionPolicy='Choosing two separately marked examination questions does not create one combined practice card. Each task is independently practicable at its own tariff.'
    ), ensure_ascii=False, indent=2) + '\n')
    print(f'Wrote {len(cards)} reviewed French writing cards and exact Atlas identities.')


if __name__ == '__main__':
    build()
