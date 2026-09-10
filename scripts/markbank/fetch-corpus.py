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
    'lcvp': 'link-modules',
    'classical-studies': 'classical-studies',
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
FILEID = re.compile(r'^LC(\d{3})([ACG])LP([0-9A-Z]{3})([EIB])V\.pdf$', re.I)
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
                by_level.setdefault(LEVEL[m.group(2).upper()], []).append(
                    (m.group(3), name))
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
