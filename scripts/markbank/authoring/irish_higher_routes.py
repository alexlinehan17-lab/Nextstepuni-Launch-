"""Source-reviewed corrections to 2022/2024 Higher Q2 and Q3B.

This is a partial paper review, never a completeness certificate. All legacy
identities survive. New routes are generated from the actual printed pools.
"""
from __future__ import annotations
import copy
import hashlib
import itertools
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
HASHES = {
    2022: ('e29b5862e8650455db716de7c58c1c81d7f09f169f482d53d5831027b5637d58',
           '600bdfd6f0a8499687c09a98873aa32915415299e83885186dd1a7ca251ca92c'),
    2024: ('5302117a0e3dbbf46d0e635680fd78ceb00d46d89e54cc3a04d4f7d9506cd2ca',
           'c2d30b98b2a6e6b2747b8479b9df527609652b52ce5e352f356fab9bdac1c27e'),
}


def compact(text):
    return re.sub(r'\s+', ' ', text.replace('‐', '-')).strip()


def section(text, start, end=None):
    match = re.search(start, text, re.S)
    assert match, ('Stale reviewed start', start)
    tail = text[match.end():]
    if end:
        stop = re.search(end, tail, re.S)
        assert stop, ('Stale reviewed end', end)
        tail = tail[:stop.start()]
    return tail.strip()


def award(key, label, marks, guidance):
    return dict(id=key, label=label, kind='award', maxMarks=marks,
                permittedMarks=list(range(marks+1)), guidanceKind='quality' if key == 'gaeilge' else 'indicative',
                guidance=[compact(guidance)])


def classify_selections(year, pages):
    # Match actual extracted wording, not a parser-generated list of card IDs.
    # Every directive on these reviewed pages must be covered; every decision
    # must still match its source. The rest of each paper remains pending.
    rules = [
        ('prose-family', r'Freagair Ceist 2A \(Prós Ainmnithe\) nó Ceist 2B \(Prós Roghnach\)\.',
         'Choose prescribed or optional prose. Each has three explicit 30-mark routes after its film/drama choice.'),
        ('outer-option', r'Freagair do rogha ceann amháin de \(a\) nó \(b\)(?: thíos)?\.',
         'Each printed (a)/(b) response is retained; internal choices are expanded separately.'),
        ('prescribed-film-drama', r'Freagair an cheist thíos ar an scannán Cáca Milis nó ar an dráma An Lasair Choille\.',
         'Two 30-mark routes: Cáca Milis and An Lasair Choille. Each keeps 25 Eolas plus one shared 5 Gaeilge.'),
        ('optional-film-drama', r'Freagair an cheist thíos ar an scannán roghnach nó ar an dráma roghnach\.',
         'Two 30-mark genre routes. The studied work, author and character/theme remain open choices.'),
        ('prose-heading', r'PRÓS AINMNITHE nó PRÓS ROGHNACH',
         'Repeated heading for the already classified prescribed/optional choice.'),
        ('alternative-separator', r'(?m)^\s*nó\s*$',
         'Printed separator between the alternatives classified above; not an additional task.'),
    ]
    if year == 2022:
        rules += [
            ('prose-or-poetry', r'Freagair Ceist 2 \(Prós\) nó Ceist 3 \(Filíocht\)\.',
             '2022 outer exam choice. Both response families remain available for independent practice.'),
            ('poetry-technique', r'Déan plé ar an úsáid a bhaineann an file as do rogha ceann amháin díobh seo a leanas chun an príomhthéama sin a chur in iúl: íomhánna, codarsnacht nó mothúcháin\.',
             'Closed choose-one pool: three complete 30-mark routes, each retaining compulsory (ii)/(iii) and shared Gaeilge.'),
        ]
    else:
        rules += [('open-character', r'roghnaigh duine de na carachtair \(na pearsana\) sa ghearrscéal sin\.',
                   'Open choice from the student’s independently chosen short story, not a finite printed character pool.')]
    hits = {key: [] for key, _, _ in rules}
    for page, raw in pages.items():
        # Preserve standalone nó lines while normalizing wrapping elsewhere.
        separators = list(re.finditer(r'(?m)^\s*nó\s*$', raw))
        text = compact(raw)
        for key, pattern, reason in rules:
            if key == 'alternative-separator':
                for match in separators:
                    hits[key].append(dict(page=page, quote=compact(match.group()), reason=reason))
                continue
            for match in re.finditer(pattern, text):
                hits[key].append(dict(page=page, quote=match.group(), reason=reason))
        # Standalone separators can be recognized unambiguously between tariffs
        # and the next question/heading. Mask the corresponding normalized text.
        masked = re.sub(r'(?m)^\s*nó\s*$', ' ', raw)
        masked = compact(masked)
        for _, pattern, _ in rules:
            masked = re.sub(pattern, lambda m: ' ' * len(m.group()), masked)
        unknown = list(re.finditer(r'\b(?:rogha|roghnaigh|nó)\b', masked, re.I))
        assert not unknown, (year, page, 'Unclassified selection directive', [masked[max(0,m.start()-45):m.end()+60] for m in unknown])
    assert all(hits.values()), ('Stale selection decision', year, [k for k,v in hits.items() if not v])
    return [dict(key=key, occurrences=value) for key,value in hits.items()]


def apply_review(cards):
    by_id = {c['id']: c for c in cards}
    original_ids = set(by_id)
    reviews = []
    for year, (paper_hash, scheme_hash) in HASHES.items():
        docs = []
        for kind, fileid, expected in [('exampapers', 'LC001ALP200IV.pdf', paper_hash),
                                       ('markingschemes', 'LC001ALP000IV.pdf', scheme_hash)]:
            path = ROOT / f'paper-trail-corpus/{kind}/{year}/{fileid}'
            assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'Source changed: repeat visual review'
            docs.append(fitz.open(path))
        paper, scheme = docs
        paper_pages = [8,9,12] if year == 2022 else [8,11]
        raw_pages = {n: paper[n-1].get_text() for n in paper_pages}
        decisions = classify_selections(year, raw_pages)
        p = {n: compact(text) for n,text in raw_pages.items()}
        s = {n: compact(re.sub(r'(?m)^\s*\d+\s*$', '', page.get_text())) for n,page in enumerate(scheme,1)}
        reviewed_ids = []
        def put(key, atlas, text, topic, pages, scheme_pages, criteria, title, requirements=None, template=None, route=None):
            identifier = f'irish-{year}-hl-p2-{key}'
            card = copy.deepcopy(by_id[template or identifier])
            if key.startswith(('prose-2b-', 'poetry-3b-')):
                restriction = ('Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.'
                               if key.startswith('prose') else
                               'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.')
                if restriction not in text:
                    text += ' '+restriction
            card.update(id=identifier, questionRef=f'{year} HL Paper 2 {title}',
                        questionText=compact(text), topicId=topic,
                        conceptId=f'irish-{key}-{topic}', totalMarks=30,
                        paperPage=pages[0], paperTraceScore=1, schemeTraceScore=1,
                        schemePage=scheme_pages[0], schemePages=scheme_pages,
                        atlasQuestionId=atlas, reviewedPaperPages=pages,
                        reviewedAt='2026-10-07', criteria=criteria + [award('gaeilge','Gaeilge',5,
                            '5 sárchumas; 4 cumas an-mhaith; 3 cumas maith; 2 cumas measartha; 1 cumas lag/an-lag; 0 gan fiúntas. Gramadach, comhréir, struchtúr agus deilbhíocht.')],
                        taskRequirements=requirements or ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.'],
                        markingGuideNote='One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. Supporting examples are indicative; other valid points are credited on their merits. Do not add alternative route tariffs together.')
            if route: card['selectedRoute'] = route
            if identifier not in by_id: cards.append(card)
            else: cards[cards.index(by_id[identifier])] = card
            by_id[identifier] = card
            reviewed_ids.append(identifier)
            return card

        # All prose prompts come from the exact paper, including title/author
        # requirements. The first film identity remains; the drama is additive.
        pa = section(p[8], r'2A\. Prós Ainmnithe', r'2B\. Prós Roghnach' if year == 2024 else r'– PRÓS AINMNITHE')
        pb = section(p[9 if year == 2022 else 8], r'2B\. Prós Roghnach', r'PRÓS AINMNITHE nó PRÓS ROGHNACH' if year == 2024 else None)
        film = section(pa, r'\(a\).*?An Lasair Choille\. ', r'\(30 marc\)') + ' (30 marc)'
        drama = section(pa, r'\(30 marc\) nó ', r'\(30 marc\)') + ' (30 marc)'
        # The choice instruction itself contains (a)/(b). Match the actual
        # task heading, never the first occurrence of the option letter.
        other = section(pa, r'\(b\) (?=Hurlamaboc|Dís)', r'\(30 marc\)') + ' (30 marc)'
        optional_film = section(pb, r'\(a\).*?dráma roghnach\. ', r'\(30 marc\)') + ' (30 marc)'
        optional_drama = section(pb, r'\(30 marc\) nó ', r'\(30 marc\)') + ' (30 marc)'
        optional_other = section(pb, r'\(b\) (?=Maidir)', r'\(30 marc\)') + ' (30 marc)'
        base = f'irish-{year}-hl-p2-'
        general = s[27]
        prose_guide = lambda text: award('eolas','Eolas',25,general+' '+text)
        put('prose-2a-a','P-2A-a-caca-milis',film,'irish-4-6',[8],[27,28],
            [prose_guide(s[28])], 'Prós 2A(a) · Cáca Milis')
        put('prose-2a-a-an-lasair-choille','P-2A-a-an-lasair-choille',drama,'irish-4-8',[8],[27,29,30],
            [prose_guide(s[29]+' '+s[30].split('nó (b)',1)[0])],
            'Prós 2A(a) · An Lasair Choille', template=base+'prose-2a-a')
        other_title, other_topic = ('Hurlamaboc','irish-4-5') if year == 2022 else ('Dís','irish-4-4')
        other_guide = section(s[30], r'\(b\) '+other_title) + (' '+s[31].split('2B.',1)[0] if year == 2024 else '')
        put('prose-2a-b','P-2A-b',other,other_topic,[8],[27,30]+([31] if year == 2024 else []),
            [prose_guide(other_guide)], 'Prós 2A(b) · '+other_title)
        restrictions = ['Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.',
                        'Ní mór teideal an tsaothair agus ainm an scríbhneora a scríobh síos go cruinn.']
        optional_guide = section(s[31], r'Treoir:')
        optional_criteria = ([award('theme','Príomhthéama',2,'An príomhthéama = 2 mharc.'),
                              award('development','Forbairt an phríomhthéama',23,optional_guide)]
                             if year == 2024 else [prose_guide(optional_guide)])
        # The optional film and the optional play share one grid and one Atlas heading (irish-4-7),
        # so one card carries both printed alternatives (choose-one refinement, 2026-10-12).
        optional_head = re.search(r'\(a\) Freagair an cheist thíos ar an scannán roghnach nó ar an dráma roghnach\. ', pb).group(0)
        put('prose-2b-a','P-2B-a',optional_head+optional_film+' nó '+optional_drama,'irish-4-7',[9 if year == 2022 else 8],[27,31],
            copy.deepcopy(optional_criteria), 'Prós 2B(a) · Scannán nó dráma roghnach', restrictions)
        other_criteria = ([award('theme','Príomhthéama',2,'An príomhthéama = 2 mharc.'),
                           award('development','Forbairt an phríomhthéama',23,section(s[32],r'Treoir:'))]
                          if year == 2022 else [prose_guide(s[32])])
        put('prose-2b-b','P-2B-b',optional_other,'irish-4-7',[9 if year == 2022 else 8],[27,32],other_criteria,
            'Prós 2B(b) · '+('Úrscéal roghnach' if year == 2022 else 'Gearrscéal roghnach'), restrictions)

        poetry_page = 12 if year == 2022 else 11
        poetry = section(p[poetry_page], r'3B\. Filíocht Roghnach')
        poetry_a = '(a) (i) '+section(poetry, r'\(a\) \(i\) ', r' nó \(b\)')
        poetry_b = '(b) (i) '+section(poetry, r'\(b\) \(i\) ')
        for prompt in [poetry_a,poetry_b]:
            assert all(prompt.count('('+part+')') == 1 for part in ['i','ii','iii'])
        for option, prompt, scheme_pages, guide in [
            ('a',poetry_a,[37,38] if year == 2022 else [38,39],
             section(s[37],r'3B\. Filíocht Roghnach')+' '+s[38] if year == 2022 else s[38]+' '+s[39].split('nó (b)',1)[0]),
            ('b',poetry_b,[39,40],section(s[39],r'\(b\)')+' '+s[40]),
        ]:
            parts = [section(guide, r'\('+part+r'\)', r'\('+next_part+r'\)' if next_part else r'Gaeilge')
                     for part,next_part in [('i','ii'),('ii','iii'),('iii',None)]]
            criteria = [award('eolas-'+part,'Eolas ('+part+')',marks,text) for part,marks,text in zip(['i','ii','iii'],[13,5,7],parts)]
            put('poetry-3b-'+option,'F-3B-'+option,prompt,'irish-5-6',[poetry_page],scheme_pages,criteria,
                f'Filíocht 3B({option}) · Dán roghnach',
                ['Freagair (i), (ii) agus (iii).', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.'])
        if year == 2022:
            # Keep the historical unspecialised ID, and add the C(3,1) routes.
            pool_text = section(poetry_a, r'a chur in iúl: ', r'\. \(15 mharc\)')
            pool = re.split(r', | nó ', pool_text)
            assert pool == ['íomhánna','codarsnacht','mothúcháin'], ('Changed finite pool',pool)
            slugs = ['iomhanna','codarsnacht','mothuchain']
            original = by_id[base+'poetry-3b-a']
            for ((choice,slug),) in itertools.combinations(zip(pool,slugs),1):
                put('poetry-3b-a-'+slug,'F-3B-a-'+slug,
                    original['questionText']+' An rogha don chárta seo: '+choice+'.',
                    'irish-5-6',[12],[37,38],copy.deepcopy(original['criteria'][:-1]),
                    'Filíocht 3B(a) · '+choice, original['taskRequirements']+['Rogha (i): '+choice+'.'],
                    template=original['id'], route=choice)
        reviews.append(dict(year=year,level='higher',paperFileid='LC001ALP200IV.pdf',
                            paperSha256=paper_hash,schemeSha256=scheme_hash,reviewDate='2026-10-07',
                            scope=('Q2 and Q3B only; full paper review remains pending' if year==2022 else
                                   'Q2 and Q3B only; full-paper status is recorded separately in irish-paper-reviews.json.'),
                            reviewedPaperPages=paper_pages,
                            reviewedSchemePages=list(range(27,33))+list(range(37 if year==2022 else 38,41)),
                            cardIds=reviewed_ids,selectionDecisions=decisions))
    assert original_ids <= {c['id'] for c in cards}
    assert len(cards) == 405 and len({c['id'] for c in cards}) == 405
    return cards, reviews
