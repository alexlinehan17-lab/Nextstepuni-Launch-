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
level letter is A for Higher and G for Ordinary, and the language letter E for
the English version. Only the English versions are fetched.
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
}

FILEID = re.compile(r'^LC(\d{3})([AG])LP(\d{3})([EI])V\.pdf$', re.I)
LEVEL = {'A': 'hl', 'G': 'ol'}


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
    slug = SUBJECTS.get(subject, subject)
    got = 0
    for year in YEARS:
        for kind in kinds:
            out_dir = 'papers' if kind == 'paper' else 'schemes'
            names = listing(f'papers/lc/{slug}/{year}/{kind}/')
            # Group by level so a subject printed across several booklets keeps
            # each one, and a single-booklet subject keeps its plain name.
            by_level = {}
            for name in names:
                m = FILEID.match(name.rsplit('/', 1)[-1])
                if not m or m.group(4).upper() != 'E':
                    continue                       # skip the Irish-language versions
                by_level.setdefault(LEVEL[m.group(2).upper()], []).append(
                    (m.group(3), name))
            for level, entries in sorted(by_level.items()):
                entries.sort()
                for component, name in entries:
                    suffix = f'-{component}' if len(entries) > 1 else ''
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
