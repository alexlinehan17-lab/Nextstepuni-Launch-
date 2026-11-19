#!/usr/bin/env python3
"""Review-only 2013 source preparation from already-inspected cached text.

Never writes a source deck. The original-PDF selector/replay, final filings and
application checks remain required before this draft can be released.
"""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz

HERE = Path(__file__).resolve().parent
LANE = Path('/Users/alexlinehan/Documents/Nextstepuni-LCVP-Release-20261119')
sys.path.insert(0, str(LANE / 'scripts/markbank/authoring'))
from lcvp_review_2026 import tidy, point, criterion
from lcvp_review_2024 import split_raw
from lcvp_review_2018 import choice_row, response_row, before_rate, models
from lcvp_review_2017 import component_rows, header_body

FIXED = 'The scheme prints no answer for this part.'
TEXT_HASHES = {
    'paper': '49f314980d4d810717674ed15168ce642e7a132b961e0abe1802702a6ea0ad4a',
    'scheme': 'ded9ebd35e40c5c8499b56de6949ef1ff549b4a67f84a3f5756f7d946bcd2352',
    'case': '67f27e9c05a04a24cddc14f77369a64733a9171f0581999e889b039bb2cdeb4f',
}


def pages(kind):
    path = HERE / (kind + '-text-layer.txt')
    assert hashlib.sha256(path.read_bytes()).hexdigest() == TEXT_HASHES[kind]
    text = path.read_text()
    chunks = re.split(r'===== ORIGINAL PDF PHYSICAL PAGE (\d+) =====\n', text)
    inventory = json.loads((HERE/'cached-source-inventory.json').read_text())
    record = next(r for r in inventory['sources'] if
        ('scheme' if r['kind'] == 'markingschemes' else 'case' if '016' in r['fileid'] else 'paper') == kind)
    original = Path(record['path'])
    assert hashlib.sha256(original.read_bytes()).hexdigest() == record['sha256']
    document = fitz.open(original)
    result = {}
    for i in range(1, len(chunks), 2):
        number = int(chunks[i])
        value = document[number - 1].get_text(sort=False)
        assert value.strip() == chunks[i + 1].strip(), (kind, number, 'original page differs from frozen source text')
        if kind == 'scheme':
            value = re.sub(r'^\s*' + str(number - 2) + r'\s*\n', '', value, count=1)
        else:
            value = re.sub(r'^\s*Page \d+ of 32\s*$', '', value, flags=re.M)
            # The two examiner score columns are standalone 1/2 spans. All
            # original pages were inspected; no question uses a bare 1/2 line.
            value = re.sub(r'^\s*[12]\s*$', '', value, flags=re.M)
            value = value.replace('\uf0b7', '•')
        result[number] = value
    return result


def scheme_parts(pages):
    text = '\n'.join(pages[n] for n in range(4, 19))
    # Native text order places C6(c)'s right-hand marking box after four C6(d)
    # models. The original page image confirms the box belongs to the email.
    summaries = re.findall(r'Summary of Marks\s+To\s+1m.*?Total\s+7m', text, re.S)
    assert len(summaries) == 1
    email_summary = summaries[0]
    text = text.replace(email_summary, '')
    text = re.sub(r'^\s*Part [123]\s*$', '', text, flags=re.M)
    sections = split_raw(text, r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, section_text in sections.items():
        questions = split_raw(section_text, r'^\s*Q\.?\s*(\d+)\s*',
            [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 6}[section] + 1)])
        for q, block in questions.items():
            if section == 'A' or (section == 'B' and q == '1'):
                out[section + q] = block
            elif section == 'B':
                heading, body = header_body(block)
                for roman, part in split_raw(body, r'^\s*\((i{1,3})\)\s*', ['i', 'ii', 'iii'] if q == '2' else ['i', 'ii']).items():
                    out[section + q + roman] = heading + '\n' + part
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    out[section + q + letter] = part
    assert len(out) == 38
    out['C6c'] += '\n' + email_summary
    return out


PAGES = {'A' + str(q): [p] for q, p in enumerate([3, 3, 3, 4, 4, 5, 6, 7], 1)}
PAGES['A5'] = [4, 5]
PAGES['B1'] = [9]
PAGES.update({'B2' + r: [10, 11] for r in ['i', 'ii', 'iii']})
PAGES.update({'B3' + r: [11, 12] for r in ['i', 'ii']})
PAGES.update({'C' + str(q) + l: [14 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[l]]
    for q in range(1, 7) for l in 'abcd'})


def question(paper, ref):
    match = re.fullmatch(r'([ABC])(\d)([abcd]?)(i{0,3})', ref)
    section, q, letter, roman = match.groups()
    value = paper[PAGES[ref][0]]
    if section in ['A', 'B']:
        value = re.split(r'^\s*Q\.?\s*' + q + r'\s*', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*Q\.?\s*\d+\s*', value, maxsplit=1, flags=re.M)[0]
    if letter:
        value = re.split(r'^\s*\(' + letter + r'\)\s*', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*\([abcd]\)\s*', value, maxsplit=1, flags=re.M)[0]
    if roman:
        value = re.split(r'\(' + roman + r'\)\s*', value, maxsplit=1)[1]
        value = re.split(r'\(i{1,3}\)\s*', value, maxsplit=1)[0]
    value = re.sub(r'\b\d+\s+marks?\b', '', value, flags=re.I)
    value = tidy(value)
    if ref == 'C3b':
        # The chart is source material, not a trail of labels in the prompt.
        chart = '45.8% 6.7% 8.3% 16.7% 12.5% 10.0% Recreational Facilities for Teenagers Youth Cafe Swimming Pool Cinema Sports Hall Skate Park Music & Drama'
        assert value.endswith(chart)
        value = value[:-len(chart)].strip()
    assert not re.search(r'Office Use|Only|Page \d+ of 32', value), (ref, value)
    return value


def source(page_numbers, title='Original question', kind='source-question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=page_numbers,
        attribution='SEC LCVP Link Modules 2013 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def source_scheme_prompt(raw, ref):
    prompt = header_body(raw[ref])[0]
    if ref.startswith(('B2', 'B3')):
        roman = ref[2:]
        prompt = re.split(r'\(' + roman + r'\)\s*', prompt, maxsplit=1)[1]
        prompt = re.split(r'\(i{1,3}\)\s*', prompt, maxsplit=1)[0]
    elif ref == 'B1':
        prompt = prompt.split('Smartphones', 1)[0]
    return tidy(re.sub(r'\b\d+\s+marks?\b', '', prompt, flags=re.I))


def build():
    inventory = json.loads((HERE/'cached-source-inventory.json').read_text())
    for record in inventory['sources']:
        assert hashlib.sha256(Path(record['path']).read_bytes()).hexdigest() == record['sha256']
    listing = next(r for r in inventory['cachedListings'] if 'exampapers' in r['path'])
    listing_path = Path(listing['path'])
    assert hashlib.sha256(listing_path.read_bytes()).hexdigest() == listing['sha256']
    assert 'LC462CLP031EV.mp4' in listing_path.read_text()
    assert inventory['recording'] == 'https://www.examinations.ie/archive/exampapers/2013/LC462CLP031EV.mp4'
    paper, scheme = pages('paper'), pages('scheme')
    raw = scheme_parts(scheme)
    rows, totals, topics = {}, {}, {}
    def put(ref, marks, topic, value):
        rows[ref], totals[ref], topics[ref] = value, marks, topic
    def body(ref):
        return header_body(raw[ref])[1]
    def pool(ref, expected, rate):
        text = before_rate(body(ref), rate)
        text = re.sub(r'\b\d+\s+[Mm]arks?\s*$', '', text)
        return models(text, expected)
    def ordinary(ref, topic, count, per, expected, binary=False):
        options = pool(ref, expected, str(count) + r'\s*@\s*' + str(per) + 'm')
        if binary or per == 1:
            row = choice_row('responses', question(paper, ref), options, count, per,
                f'The scheme gives {count} responses {per} or 0 marks each. Keep all original alternatives.')
        else:
            row = response_row('responses', question(paper, ref), options, count, list(range(per + 1)),
                f'The scheme gives {count} responses {per} marks each in printed one-mark components.')
        put(ref, count * per, topic, [row])
    def missing(ref, marks, topic, note, count=1, per=None):
        row = criterion('unprinted-answer', FIXED, count, list(range((per or marks) + 1)), note)
        row['unprinted'] = True
        put(ref, marks, topic, [row])
    def partial(ref, note):
        rows[ref].append(dict(id='missing-expansion', kind='criterion', verbatim=FIXED,
            marks=0, unprinted=True, contextNote=note))

    put('A1', 1, '1-1', [point('years', tidy(before_rate(body('A1'), r'1\s+mark')), 1)])
    for args in [('A2','1-1',2,1,5),('A3','1-1',3,1,3),('A4','1-0',4,1,5),
                 ('A5','1-1',2,2,2),('A6','1-1',2,2,3),('A7','1-0',3,2,4),('A8','1-0',3,2,6)]:
        ordinary(*args)

    terms = ['Smartphones', 'Plan of Action', 'Redundancy', 'Curriculum Vitae']
    term_parts = split_raw(before_rate(body('B1'), r'3\s*@\s*2m'),
        r'^\s*(Smartphones|Plan of Action|Redundancy|Curriculum Vitae)\s*', terms)
    put('B1', 6, '0-1', [response_row('terms', question(paper, 'B1'),
        [term + ': ' + tidy(term_parts[term]) for term in terms], 3, [0, 1, 2],
        'The paper asks for three of four terms. Keep this one printed choice and every complete model. The paper says Redundancy Package; the scheme heading is Redundancy. No option is compulsory.')])
    agencies = [tidy(line) for line in before_rate(body('B2i'), r'2\s*@\s*1m').splitlines() if line.strip()]
    assert len(agencies) == 5
    put('B2i', 2, '1-1', [choice_row('agencies', question(paper, 'B2i'), agencies, 2, 1)])
    titles = ['IDA Ireland', 'Enterprise Ireland', 'County Enterprise Board', 'FAS (SOLAS)', 'Department of Social Protection', 'Leader']
    agency_text = before_rate(body('B2ii'), r'2\s*@\s*4m')
    agency_text = re.sub(r'\b8\s+marks\s*$', '', agency_text)
    agency_parts = split_raw(agency_text, r'^\s*(' + '|'.join(map(re.escape, titles)) + r')\s*$', titles)
    all_agencies = [title + ': ' + ' | '.join(models(agency_parts[title], n)) for title, n in zip(titles, [7,5,4,2,2,4])]
    put('B2ii', 8, '1-1', component_rows(question(paper, 'B2ii'), all_agencies, [[2,2],[2,2]],
        'Use the same two agencies selected in part (i). The scheme gives 2 @ 4m (2 + 2). Keep every agency pool and all its models. No cross-card deduction is invented.'))
    ordinary('B2iii','1-2',2,1,5)
    ordinary('B3i','0-2',3,2,5)
    ordinary('B3ii','0-1',3,2,8)
    partial('B3ii', 'Only the valid expansions for options 1 and 8 are unprinted. Keep all eight printed options and the existing three two-mark response controls; this notice adds no marks.')

    definition = tidy(before_rate(body('C1a'), r'2\s*@\s*2m'))
    put('C1a',4,'1-0',[response_row('definition',question(paper,'C1a'),[definition],2,[0,2],
        'The scheme gives the whole definition 2 @ 2m (0, 2). Keep two binary components and the full model; no one-mark award is printed.')])
    choices = split_raw(body('C1b'), r'^\s*(Two benefits:|Two challenges)\s*', ['Two benefits:', 'Two challenges'])
    put('C1b',4,'1-0',[choice_row('benefits',question(paper,'C1b'),models(before_rate(choices['Two benefits:'],r'2\s*@\s*1m'),4),2,1),
        choice_row('challenges',question(paper,'C1b'),models(before_rate(choices['Two challenges'],r'2\s*@\s*1m'),4),2,1)])
    ordinary('C1c','1-0',4,2,6)
    traits = pool('C1d',6,r'3\s*@\s*1m')
    put('C1d',9,'1-0',[response_row('names',question(paper,'C1d'),traits,3,[0,1],
        'The scheme gives 3 @ 1m – naming. No repetition of points.'),
        response_row('importance',question(paper,'C1d'),traits,3,[0,1,2],
        'The scheme gives 3 @ 2m (1 + 1), Characteristic/ Explanation/ Importance. Explain the same three selected characteristics. No repetition of points.')])
    ordinary('C2a','0-3',3,2,9);ordinary('C2b','0-3',2,2,5)
    work_pool = pool('C2c',6,r'3\s*@\s*2m')
    put('C2c',7,'0-3',component_rows(question(paper,'C2c'),work_pool,[[1,1],[1,1],[1,1],[1]],
        'The scheme gives 3 @ 2m (1 + 1), plus 1 @ 1m. Four distinct responses; no uniform mark allocation is inferred.'))
    ordinary('C2d','0-3',4,2,7)
    ordinary('C3a','1-2',2,2,7,True);ordinary('C3b','1-0',3,2,7)
    name, account = body('C3c').split('1m',1)
    assert tidy(name) == 'Name of organisation.'
    account_pool = models(before_rate(account,r'4\s*@\s*2m'),6)
    first = criterion('name',FIXED,1,[0,1],'Name of organisation. 1m. No particular organisation is printed.')
    first['unprinted']=True
    second = criterion('account',FIXED,4,[0,1,2],
        'The scheme gives 4 @ 2m (1 + 1). No Marks for headings. Use the same organisation selected in the first ask and four relevant headings. No chosen-organisation account is printed. Complete original guidance: '+' | '.join(account_pool))
    second['unprinted']=True
    put('C3c',9,'1-2',[first,second]);ordinary('C3d','1-2',3,2,7)
    missing('C4a',1,'1-1','Name of the Business. 1m. No particular business is printed.')
    ordinary('C4b','1-1',4,2,7);partial('C4b','Only option 1 requires an unprinted valid expansion. Keep all seven printed models and four two-mark response controls. This notice adds no marks.')
    ordinary('C4c','1-0',4,2,7);ordinary('C4d','1-1',4,2,6)
    ordinary('C5a','1-3',2,1,7);ordinary('C5b','1-0',3,2,5)
    financial_model = body('C5c').split('Summary:',1)[0]
    finance_rows = []
    for i,label in enumerate(['Resources and Costs/Financial Section [Income/Expenditure]', 'Revenue [Income]', 'Costs [Expenditure]', 'Surplus[Profit]'],1):
        assert label in financial_model
        finance_rows.append(point('heading-'+str(i),label,1))
    for i,(label,value) in enumerate([('Sales','1,000'),('Sponsorship','100'),('Advertising','75.00'),('Raw Materials','300.00'),('Telephone','8.50'),('Stationery','18.00'),('Surplus[Profit]','€698.50')],1):
        assert label in financial_model and value in financial_model
        finance_rows.append(point('figure-'+str(i),label+' '+value,1))
    finance_rows[0]['contextNote']='Summary: 7 figures with labels @ 1m each; 4 Headings @ 1m each. The unmarked intermediate totals 1,100.00 and 401.50 remain in this complete printed model and receive no additional marks:\n'+financial_model.strip()
    put('C5c',11,'1-3',finance_rows)
    ordinary('C5d','1-0',3,2,8)
    partial('C5d','Only the explanations for printed options 3, 7 and 8 are absent. Retain all eight models and three two-mark response controls. The generic (1 + 1) does not label separate state/explain allocations; the whole six-mark ask is provisional pending third reading. No product-name mark is printed or invented.')
    ordinary('C6a','1-0',4,1,6);ordinary('C6b','1-0',5,1,8)

    # The complete model and exact seven criteria are selected below; this
    # source-preparation step must not invent a replacement email.
    email = body('C6c')
    labels = ['To', 'Subject Line', 'Opening', 'Purpose of email', 'Arrangements', 'Closing', 'Neatness/Presentation/Layout']
    email_rows = [point('email-'+str(i),label,1) for i,label in enumerate(labels,1)]
    for label in labels: assert label in email, label
    email_rows[0]['contextNote']='Complete original email and printed marking directions:\n'+email.strip()
    put('C6c',7,'1-0',email_rows)
    evaluation = pool('C6d',5,r'3\s*@\s*3m')
    put('C6d',9,'1-0',component_rows(question(paper,'C6d'),evaluation,[[1,1,1]]*3,
        'The scheme gives 3 @ 3m (1 + 1 + 1): Heading / Explanation / Reason. One requested description, with three complete evaluation responses. Keep all five full models.'))

    assert set(rows)==set(raw)==set(PAGES) and sum(totals.values())==210
    # The question side remains the paper's wording. A criterion label is a
    # scheme claim, so use the scheme's own prompt wherever it differs.
    for ref, values in rows.items():
        for row in values:
            if row['verbatim'] == question(paper, ref):
                row['verbatim'] = source_scheme_prompt(raw, ref)
    # All case paragraphs and the original graph remain accessible before reveal.
    case = paper[8]
    case = re.sub(r'^\s*(Section B|Case Study|30 marks|Office Use|Only|[12])\s*$', '', case, flags=re.M)
    case = tidy(case)
    stems={}
    for q in range(1,7):
        text=re.split(r'^\s*Q\.?\s*'+str(q)+r'\s*',paper[14+(q-1)*3],maxsplit=1,flags=re.M)[1]
        stems[q]=tidy(text.split('(a)',1)[0])
    cards=[]
    for ref in raw:
        section=ref[0];q=int(ref[1]);suffix=ref[2:]
        printed=f'2013 CL Section {section} Q{q}'
        if suffix:
            printed += '('+suffix+')'
        card=dict(id='lcvp-2013-cl-'+ref.lower(),subjectId='lcvp',topicId='lcvp-link-modules-'+topics[ref],
            conceptId='lcvp-2013-'+ref.lower(),level='common',year=2013,section=section,
            questionRef=printed,questionText=question(paper,ref),stem=case if section=='B' else stems[q] if section=='C' else '',
            figureKey='',labelKey=[],totalMarks=totals[ref],rows=rows[ref],
            tariffModel=dict(kind='fixed',notation='Original 2013 marking scheme allocation.'),sourceMaterial=source(PAGES[ref]))
        if section=='A':
            card['videoMaterial']=dict(kind='source-video',label='OFFICIAL VIDEO',title='2013 LCVP audiovisual examination',
                playbackUrl='https://www.examinations.ie/archive/exampapers/2013/LC462CLP031EV.mp4',
                canonicalUrl='https://www.examinations.ie/archive/exampapers/2013/LC462CLP031EV.mp4',secFileid='LC462CLP031EV.mp4',
                attribution='State Examinations Commission — original 2013 Common Level English audiovisual recording.',
                presentationNote='Watch the original recording with its sound and follow the printed viewing instructions. Hosted playback remains pending the audio-hosting lane while the SEC archive is blocked.')
            card['additionalSourceMaterials']=[source([2],title='Original audiovisual instructions')]
        if section=='B':
            card['sourceMaterial']=source([8],title='Complete original case study',kind='source-text')
            card['additionalSourceMaterials']=[source(PAGES[ref])]
        if ref=='B2ii':card['stem']+=' '+question(paper,'B2i')
        if ref=='C3b':
            card['sourceMaterial'] = source([20], title='Original recreational-facilities chart and question', kind='source-text')
            card['sourceMaterial']['presentationNote'] = 'Read the complete original pie chart, its title, legend, percentages and question before answering.'
        if section=='C' and q==4 and suffix!='a':card['stem']+=' '+question(paper,'C4a')
        cards.append(card)
    for ref,start,marks,second_ref in [('C1b','and two challenges',[2,2],'challenges'),
                                      ('C1d','Explain the importance',[3,6],'importance of characteristics'),
                                      ('C3c','Write a detailed account',[1,8],'account of the organisation')]:
        index=next(i for i,c in enumerate(cards) if c['id']=='lcvp-2013-cl-'+ref.lower())
        first=cards[index];second=deepcopy(first);full=first['questionText'];cut=full.index(start)
        first_text,second_text=full[:cut].strip(),full[cut:].strip()
        assert first_text+' '+second_text==full and len(first['rows'])==2
        first.update(questionText=first_text,totalMarks=marks[0],rows=[first['rows'][0]])
        second.update(id=first['id']+'-2',conceptId=first['conceptId']+'-2',questionRef=first['questionRef']+' — '+second_ref,
            questionText=second_text,totalMarks=marks[1],rows=[second['rows'][1]],stem=first['stem']+' '+first_text)
        if ref=='C1b':
            # The first source span relies on the end of the shared sentence.
            first['stem']=(first['stem']+' '+full).strip()
        for card in [first,second]:
            for row in card['rows']:
                if not row.get('unprinted'):row['verbatim']=card['questionText']
        cards[index:index+1]=[first,second]
    assert len(cards)==41 and sum(c['totalMarks'] for c in cards)==210
    assert all(sum(r['marks'] for r in c['rows'])==c['totalMarks'] for c in cards)
    return cards


if __name__=='__main__':
    cards=build()
    (HERE/'proposed-authored-cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n')
    print('Wrote review-only payload; fresh PDF selectors, topic adjudication and application checks remain pending.')
