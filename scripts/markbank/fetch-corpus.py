#!/usr/bin/env python3
"""Pull exam papers and marking schemes from the Paper Trail corpus in Firebase.

    python3 scripts/markbank/fetch-corpus.py biology
    python3 scripts/markbank/fetch-corpus.py --all
    python3 scripts/markbank/fetch-corpus.py chemistry --schemes

The corpus already holds every Leaving Cert subject, world-readable, at
papers/{cycle}/{subject}/{year}/{kind}/{fileid} — see components/PaperTrail/
storage.ts, which is where the app reads it from. Going out to examinations.ie
for a paper that is already sitting in our own bucket is wasted effort and a
second source of truth; fetch from here.

Files land in examiner-reports/<subject>/papers/ named the way the authoring
scripts expect: <year>-<level>-paper.pdf, or <year>-<level>-<component>-paper.pdf
where a subject splits its exam across booklets (Biology prints Sections A and B
in one and Section C in another). Schemes land in .../schemes/<year>-<level>.pdf
alongside the markdown conversions already in the repo.

SEC file ids read LC<subject><level>LP<component><language>V.pdf, where the
level letter is A for Higher, G for Ordinary and C for a COMMON-level subject
(LCVP's Link Modules is sat at one level by everyone: LC462CLP000EV.pdf), and
the language letter E for the English version. Only the English versions are
fetched.

A common-level subject files under the level token 'cl' — its own token, not
'hl' with a note. The pipeline carries that token end to end: paper_census.py's
sittings() reads <year>-cl-paper.pdf, extract-scheme.py writes schemes/<year>-cl.md,
reconcile.py's citation grammar reads "2025 CL Q1", and the card model's level
field is 'common'. Mapping C onto 'hl' would have made every LCVP card claim a
Higher Level paper that does not exist.
"""
import argparse
import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request

BUCKET = 'nextstepuni-app.firebasestorage.app'
CTX = ssl.create_default_context()
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# The bank's default window. Overridable with --from/--to: Construction Studies
# has been examined on the same 1983 syllabus throughout the corpus and its
# replacement is not examined until 2028, so its older papers are exactly as
# valid as its recent ones. Subjects mid-redevelopment are a different matter.
YEARS = range(2021, 2026)

# Mark Bank subject -> the corpus's own slug, where they differ.
SUBJECTS = {
    'agricultural-science': 'agricultural-science',
    'biology': 'biology',
    'business': 'business',
    'chemistry': 'chemistry',
    'economics': 'economics',
    # English uses a bespoke card model: the paper supplies the prompt while
    # the scheme supplies a PCLM rubric and non-exhaustive indicative material.
    # See authoring/ENGLISH.md and authoring/english_census.py.
    'english': 'english',
    'home-economics': 'home-economics-s-and-s',
    'physics': 'physics',
    # Added 23 August 2026. Stage 0 passed on the drawing+ pattern: the scheme
    # answers "draw a section through this wall" with a list of the details the
    # drawing must contain — "Breather membrane", "Cavity closer", "Triple
    # glazing" — which is a stated answer and cards well. See stage0.py.
    'construction-studies': 'construction-studies',
    # Added 23 August 2026. Rejected at Stage 0 for notation that turned to
    # mush; see mathtext.py, which shows the mangling is a reversible font
    # fault and that the Marking Notes column is clean English.
    'maths': 'mathematics',
    # Added 30 August 2026. Stage 0 passed it on the Economics "Responses may
    # make reference to" menu pattern, which econ_lib already reads. The corpus
    # holds a complete run: papers AND schemes for every year 2018-2025.
    'politics-society': 'politics-and-society',
    # Added 30 August 2026, to MEASURE it before choosing it. See stage 0.
    'computer-science': 'computer-science',
    # Added 10 September 2026, to MEASURE before choosing. Technology has
    # never been assessed at stage 0 and is the closest uncarded sibling to
    # Engineering and Construction Studies, both of which ship. The rest are
    # re-measures of subjects whose earlier verdicts were recorded without a
    # count (see markbank-stage0-subject-verdicts).
    'technology': 'technology',
    'religious-education': 'religious-education',
    'history': 'history',
    'applied-maths': 'applied-mathematics',
    # Added 10 September 2026, to MEASURE the modern-language family at stage 0
    # (French first, then its two closest siblings) before choosing any of them.
    'french': 'french',
    'german': 'german',
    'spanish': 'spanish',
    # Added 10 September 2026. French shipped; Italian is the next modern
    # language to be MEASURED at stage 0 — a full paper with the same
    # architecture, sat by a much smaller cohort.
    'italian': 'italian',
    # Added 10 September 2026. Four modern languages ship on one reader
    # (fr_paper/fr_scheme); Russian is the next of the family to be MEASURED at
    # stage 0. SEC subject 099, the same two booklets (written '000' and
    # Listening Comprehension 'A00') printed bilingually, language letter 'B'.
    'russian': 'russian',
    # Added 10 September 2026. Japanese is the modern language furthest from
    # the four already carded: it is set in a NON-LATIN script across three
    # writing systems, so before anything else the corpus has to answer whether
    # kana and kanji survive the PDF text layer at all. Measured at stage 0
    # before it is chosen.
    'japanese': 'japanese',
    # Added 10 September 2026. Polish is a NON-CURRICULAR EU language (SEC
    # subject 548) — a different animal to the six curricular languages already
    # carded, and measured at stage 0 before it is chosen. Two structural
    # differences the listing shows before a single PDF is opened: it is sat at
    # ONE level (file letter 'A') up to and including 2021 and at TWO from 2022,
    # and it publishes SEPARATE English ('E') and Irish ('I') editions rather
    # than the bilingual 'B' booklet the curricular languages print — so the
    # existing WANTED_LANGS already takes the right one. It does carry the
    # Listening Comprehension booklet 'A00', from 2022 onward only.
    'polish': 'polish',
    # Added 10 September 2026. Arabic is the modern language with the hardest
    # TEXT problem in the corpus: it is written right-to-left, and a PDF text
    # layer routinely hands back RTL runs reversed, visually rather than
    # logically ordered, or with the letters in isolated instead of joined
    # forms. Measured at stage 0 — and the direction and joining verified
    # against rendered pages — before it is chosen. SEC subject 059, one
    # booklet '000' at each level (there is NO separate Listening
    # Comprehension 'A00': Arabic is sat as a single written paper), language
    # letter 'E'.
    'arabic': 'arabic',
    # Added 10 September 2026. Portuguese, Romanian and Dutch are the next
    # NON-CURRICULAR EU languages after Polish, and the listing answers their
    # shape before a PDF is opened. Portuguese (SEC 018) is Polish's twin: ONE
    # level (file letter 'A') up to and including 2021, TWO from 2022, a
    # separate Listening Comprehension booklet 'A00' from 2022 onward, and
    # separate English ('E') and Irish ('I') editions rather than the bilingual
    # 'B' booklet. Romanian (SEC 553) and Dutch (SEC 017) are NOT: each is sat
    # at ONE level ('A') in every year 2010-2026 and prints ONE booklet '000'
    # with NO Listening Comprehension Test at all — so a missing '-A00-paper'
    # for those two is the corpus being complete, not a fetch failure.
    'portuguese': 'portuguese',
    'romanian': 'romanian',
    'dutch': 'dutch',
    'lcvp': 'link-modules',
    'classical-studies': 'classical-studies',
    # Added 10 September 2026. Latin is a language but NOT a modern one: SEC
    # subject 006, ONE booklet ('000'), no Listening Comprehension Test, and —
    # unlike French/German/Spanish/Italian/Russian/Japanese — it is NOT printed
    # bilingually. The SEC publishes an English edition (letter 'E') and a
    # separate Irish edition (letter 'I'), so WANTED_LANGS already selects the
    # right one and the 'B' path never fires here. Ordinary Level stops after
    # 2023: the corpus holds a Higher paper for every year 2021-2025 but an
    # Ordinary paper only for 2021, 2022 and 2023 — eight sittings, not ten,
    # and that is the corpus being complete, not a fetch failure.
    'latin': 'latin',
    # Added 10 September 2026. Lithuanian, Latvian and Czech are the next three
    # NON-CURRICULAR EU languages after Polish (SEC subjects 550, 549 and 547),
    # and the corpus holds them further back than any other language: papers
    # AND schemes for every year 2010-2026, not the 2021-2025 window the
    # curricular subjects run to. That is why --from/--to is passed here rather
    # than left at the default; the older sittings are the SAME examination the
    # 2021 one is, and dropping them would shrink the denominator by two
    # thirds.
    #
    # Lithuanian follows Polish exactly: sat at ONE level (file letter 'A',
    # cover "Higher Level") up to and including 2021 and at TWO from 2022, when
    # a Listening Comprehension Test in its own booklet ('A00') appears; and it
    # publishes SEPARATE English ('E') and Irish ('I') editions rather than the
    # bilingual 'B' booklet, so WANTED_LANGS already takes the right one.
    'lithuanian': 'lithuanian',
    # Latvian and Czech did NOT follow Polish and Lithuanian through the 2022
    # rebuild: every sitting in the corpus, 2010 to 2026, is the old
    # examination — one Higher-only booklet ('000'), no Listening
    # Comprehension Test at all, and no Ordinary paper in any year. A fetch
    # that reports one file a year for each of them is the corpus being
    # complete, not a fetch failure.
    'latvian': 'latvian',
    'czech': 'czech',
    # Added 10 September 2026. Ancient Greek is Latin's sibling — SEC subject
    # 007, ONE booklet ('000'), no Listening Comprehension Test, and printed as
    # separate English ('E') and Irish ('I') editions rather than the bilingual
    # 'B' booklet the curricular modern languages use, so WANTED_LANGS already
    # takes the right one. The corpus runs 2010-2024 with 2020 absent (no
    # written exam that year) and no Ordinary paper for 2024: 14 Higher papers
    # and 13 Ordinary. Schemes are sparser still — Higher for every year on
    # disk except 2021, Ordinary for 2015, 2019 and 2023 only. That is the
    # corpus being what the SEC published, not a fetch failure; the subject is
    # examined to 2026 but the bucket stops at 2024.
    'ancient-greek': 'ancient-greek',
    # Added 10 September 2026. Modern Greek is a NON-CURRICULAR EU language
    # like Polish (SEC subject 019), but simpler in two ways the listing shows
    # before a PDF is opened: it is sat at ONE level throughout (file letter
    # 'A' — there is no Ordinary paper in any year), and there is NO separate
    # Listening Comprehension booklet, only component '000'. Language letter
    # 'E'. The corpus runs 2010-2026 with 2020 absent: 16 papers, 16 schemes.
    'modern-greek': 'modern-greek',
    # Added 10 September 2026. The nine remaining NON-CURRICULAR EU languages.
    # The corpus listing answers their shape before a PDF is opened and it is
    # the SAME shape for all nine: every file id carries the level letter 'A'
    # and ONLY 'A' (there is no Ordinary paper in any year of any of them),
    # component '000' and ONLY '000' (no Listening Comprehension Test booklet
    # 'A00' in any year — unlike Polish, Portuguese and Lithuanian, none of
    # these nine went through the 2022 rebuild), and the language letter 'E'
    # (separate English and Irish editions, not the bilingual 'B' booklet the
    # curricular modern languages print). So one file a year, at one level, is
    # the corpus being COMPLETE for these subjects, not a fetch failure.
    #
    # The corpus runs 2010-2026 rather than the default 2021-2025 window, so
    # --from/--to is passed; the older sittings are the same examination.
    # Papers on disk: Hungarian 17 (2010-2026), Bulgarian 17 (2010-2026),
    # Slovakian 16 (2020 absent), Swedish 16 (2020 absent), Estonian 15
    # (2010-2025, 2020 absent), Finnish 13 (2017, 2020, 2021 absent),
    # Croatian 13 (2014-2026 — the subject is not examined before 2014),
    # Danish 13 (2013, 2017*, 2020, 2021 absent from the regular run;
    # *2017 IS published, under a malformed file id — see FILEID), Slovenian 5
    # (2018, 2019, 2022, 2023, 2024 only).
    'hungarian': 'hungarian',
    'bulgarian': 'bulgarian',
    'slovakian': 'slovakian',
    'swedish': 'swedish',
    'estonian': 'estonian',
    'finnish': 'finnish',
    'croatian': 'croatian',
    'danish': 'danish',
    'slovenian': 'slovenian',
    # Added 10 September 2026. Mandarin Chinese is a CURRICULAR modern language
    # (SEC subject 566) first examined in 2022, so its corpus is the window
    # 2022-2026 and nothing earlier exists to fetch. Two structural facts the
    # listing gives before a PDF is opened: it is sat at TWO levels in every
    # year, with a separate Listening Comprehension booklet ('A00') beside the
    # written paper ('000') at each; and — unlike French/German/Spanish/
    # Italian/Russian/Japanese — it is NOT printed bilingually. The SEC
    # publishes separate English ('E') and Irish ('I') editions, so
    # WANTED_LANGS already takes the right one and the 'B' path never fires.
    # Its risk is not the corpus but the WRITING SYSTEM: see MANDARIN.md.
    'mandarin-chinese': 'mandarin-chinese',
    # Added 10 September 2026. Maltese is a NON-CURRICULAR EU language (SEC
    # subject 557) on the Latvian/Czech pattern: ONE Higher-only booklet
    # ('000') in every sitting, no Ordinary paper and no Listening
    # Comprehension Test at all, English edition only. The corpus holds 2018,
    # 2019 and 2022-2025 — six sittings, with 2020 and 2021 absent because no
    # written examination was held in those years. A fetch that reports one
    # paper and one scheme a year is the corpus being complete.
    'maltese': 'maltese',
    # Added 10 September 2026. Ukrainian (SEC subject 570) is the newest
    # non-curricular EU language in the corpus: first examined in 2025, so two
    # sittings exist in total. Latvian's shape — one Higher-only booklet
    # ('000'), no Ordinary paper, no Listening Comprehension Test.
    'ukrainian': 'ukrainian',
    # Added 10 September 2026. Hebrew Studies (SEC subject 009) is a
    # DISCONTINUED subject, last examined in 2019, so its window is 2010-2019
    # rather than the bank's default. It is sat at TWO levels, one booklet
    # ('000') each, no Listening Comprehension Test. Papers exist for 2010,
    # 2011, 2014, 2015, 2018 and 2019 at both levels (12); schemes for only
    # five of those twelve sittings — 2010, 2014, 2018 and 2019 Higher and
    # 2015 Ordinary. A sitting with no scheme has no answers to lift, which is
    # a fact about what the SEC published, not a fetch failure. Its risk is
    # DIRECTION: Hebrew is written right-to-left, like Arabic.
    'hebrew-studies': 'hebrew-studies',
    # Added 10 September 2026, all four to MEASURE at stage 0 before choosing.
    #
    # Physical Education (SEC 225) has NEVER been assessed by this bank. ONE
    # written booklet '000', Higher and Ordinary, language letter 'E'; 2020 is
    # Higher-only (there was no Ordinary sitting that year), 2021-2026 carry
    # both — thirteen sittings. The written paper is one of three components
    # (the others are a physical performance and a project), neither of which
    # the corpus holds or this bank could ever card.
    'physical-education': 'physical-education',
    # Accounting (SEC 032) is a RE-MEASURE: rejected in memory as "worked
    # ledgers" without a count. Papers and schemes for every year 2010-2026 at
    # both levels — 2020 publishes an Ordinary paper but the corpus holds no
    # Ordinary scheme for it.
    'accounting': 'accounting',
    # Music (SEC 067) is a RE-MEASURE, rejected as "quality bands and the
    # listening half needs audio" without a count. It is sat as THREE written
    # booklets on separate components, not one: '006' (Listening, both
    # levels), '007' (Composing, Higher only) and '008' (Composing/Melody,
    # both levels), plus a 'U00' supplement in 2013-2016. The scheme is
    # published ONCE per year and level on component '000' and answers all of
    # them, so the paper suffix and the scheme name do not correspond — the
    # census reads the components, the scheme reader splits one file.
    'music': 'music',
    # Design and Communication Graphics (SEC 562) is a RE-MEASURE, rejected as
    # "a drawing subject". Its papers changed component token twice — '000'
    # and '014' in 2010-2011, '014' and '015' in 2012-2018, '014' and '039'
    # from 2019 — because the second booklet is the drawing/answer sheet set
    # that goes with the question paper. One scheme per year and level on
    # '000'. 2020 is Higher-only.
    'dcg': 'design-and-communication-graphics',
}

# A subject the SEC sets as TWO papers on the same afternoon, one of which a
# candidate answers, and which the corpus therefore indexes as two subjects.
#
# History is the case: Later Modern 1815-1993 is subject 004 and Early Modern
# 1492-1815 is subject 096, and ONE marking scheme answers both. Fetching only
# the subject's own slug pulled Later Modern alone, so half of what the scheme
# answers had no paper to be censused, keyed or reconciled against — Law 1
# broken for that half, silently, because nothing reports a paper that was
# never asked for. The companion's papers land beside the subject's own with a
# field token in the name (`2021-hl-em-paper.pdf`), which is what paper_census
# reads as a component and what a citation names.
#
# Schemes are fetched from the PRIMARY slug only: the SEC publishes one scheme
# per year and level covering both fields, and hist_scheme.py splits it.
FIELDS = {
    'history': [('history', 'lm'), ('history-early-modern', 'em')],
}

# The component token is not always three DIGITS, and the language letter is
# not always 'E'. A modern language is sat as two booklets on the same
# afternoon: the SEC names the written paper '000' and the Listening
# Comprehension Test 'A00', and it publishes both as a single BILINGUAL
# booklet whose language letter is 'B' — every rubric printed twice, Irish in
# one column and English in the other, with no English-only edition to fetch.
# Requiring \d{3} and 'E' matched neither: Spanish censused its written paper
# alone while the listening test prints eighty marks' worth of asks its scheme
# answers, and Italian fetched five papers where the corpus holds ten. Both
# failures were silent "0 file(s) fetched" — the History FIELDS failure in a
# different disguise, and the silence Law 1 exists to prevent.
# The component token is three characters — except where the SEC's own file
# name carries a typo. Classical Studies 2024 Ordinary publishes its Paper X as
# LC008GLP0004BV.pdf, with FOUR digits, and a strict {3} silently fetched one
# file for that sitting where the corpus holds two: the illustration booklet
# every image question on that paper depends on was simply absent, with no
# error. A four-digit component is read and its leading zero dropped, which is
# what the SEC means by it; nothing else in the corpus matches the wider form.
# The 'LP' is not always 'LP' either. Danish 2017 publishes its only paper as
# LC038AP000EV.pdf, with the L dropped, and a strict 'LP' skipped it in
# silence — the corpus holds thirteen Danish sittings and the fetch reported
# twelve, with no error. The L is optional here; nothing else in the corpus
# depends on it being present, and every well-formed id still matches.
FILEID = re.compile(r'^LC(\d{3})([ACG])L?P([0-9A-Z]{3,4})([EIB])V\.pdf$', re.I)
WANTED_LANGS = {'E', 'B'}
# 'C' is not a third grade of difficulty: it is the SEC's marker for a subject
# examined at ONE level. Without it here every LCVP file failed the match and
# the fetch reported "0 file(s) fetched" with no error — silence, which is the
# failure mode this repo has paid for most often.
LEVEL = {'A': 'hl', 'G': 'ol', 'C': 'cl'}


def _api(path, query=None):
    url = f'https://firebasestorage.googleapis.com/v0/b/{BUCKET}/o'
    if path is not None:
        url += '/' + urllib.parse.quote(path, safe='')
    if query:
        url += '?' + urllib.parse.urlencode(query)
    with urllib.request.urlopen(urllib.request.Request(url), timeout=120, context=CTX) as r:
        return r.read()


def listing(prefix):
    names, token = [], None
    while True:
        q = {'prefix': prefix, 'maxResults': '1000'}
        if token:
            q['pageToken'] = token
        data = json.loads(_api(None, q))
        names += [i['name'] for i in data.get('items', [])]
        token = data.get('nextPageToken')
        if not token:
            return names


def download(path, dest):
    data = _api(path, {'alt': 'media'})
    if not data.startswith(b'%PDF'):
        return None
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as fh:
        fh.write(data)
    return len(data)


def fetch(subject, kinds):
    fields = FIELDS.get(subject) or [(SUBJECTS.get(subject, subject), None)]
    return sum(_fetch_one(subject, slug, field, kinds, primary=(i == 0))
               for i, (slug, field) in enumerate(fields))


def _fetch_one(subject, slug, field, kinds, primary):
    got = 0
    for year in YEARS:
        for kind in kinds:
            if kind == 'scheme' and not primary:
                continue        # one scheme covers both fields of study
            out_dir = 'papers' if kind == 'paper' else 'schemes'
            names = listing(f'papers/lc/{slug}/{year}/{kind}/')
            # Group by level so a subject printed across several booklets keeps
            # each one, and a single-booklet subject keeps its plain name.
            by_level = {}
            for name in names:
                m = FILEID.match(name.rsplit('/', 1)[-1])
                if not m or m.group(4).upper() not in WANTED_LANGS:
                    continue                       # skip the Irish-language versions
                component = m.group(3)
                if len(component) == 4 and component.startswith('0') \
                        and component.isdigit():
                    component = component[1:]
                by_level.setdefault(LEVEL[m.group(2).upper()], []).append(
                    (component, name))
            for level, entries in sorted(by_level.items()):
                entries.sort()
                for component, name in entries:
                    suffix = f'-{component}' if len(entries) > 1 else ''
                    # A field of study names the paper instead of a booklet
                    # code: the two are one paper each, not two halves of one.
                    if field and kind == 'paper':
                        suffix = f'-{field}'
                    stem = (f'{year}-{level}{suffix}-paper.pdf' if kind == 'paper'
                            else f'{year}-{level}{suffix}.pdf')
                    dest = os.path.join(ROOT, 'examiner-reports', subject, out_dir, stem)
                    if os.path.exists(dest):
                        print(f'  skip {subject}/{out_dir}/{stem}')
                        continue
                    size = download(name, dest)
                    if size:
                        got += 1
                        print(f'  {subject}/{out_dir}/{stem:<34} {size/1024:>7.0f} KB')
                    else:
                        print(f'  FAILED {name}', file=sys.stderr)
    return got


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('subjects', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--schemes', action='store_true',
                    help='also fetch the marking-scheme PDFs')
    ap.add_argument('--from', dest='y0', type=int, help='first year (default 2021)')
    ap.add_argument('--to', dest='y1', type=int, help='last year (default 2025)')
    args = ap.parse_args()
    targets = sorted(SUBJECTS) if args.all else args.subjects
    if not targets:
        raise SystemExit('name a subject, or pass --all')
    if args.y0 or args.y1:
        globals()['YEARS'] = range(args.y0 or 2021, (args.y1 or 2025) + 1)
    kinds = ['paper'] + (['scheme'] if args.schemes else [])
    total = sum(fetch(s, kinds) for s in targets)
    print(f'\n{total} file(s) fetched')
