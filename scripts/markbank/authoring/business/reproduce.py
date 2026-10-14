#!/usr/bin/env python3
"""Re-run every Business card generator and prove it reproduces the committed output byte for byte.

    python3 scripts/markbank/authoring/business/reproduce.py            # check (default)
    python3 scripts/markbank/authoring/business/reproduce.py --write    # regenerate in place
    python3 scripts/markbank/authoring/business/reproduce.py --schemes  # also re-extract the scheme .md files

Run from the repo root (it needs paper-trail-corpus/ and node). The chain below
is every generator in the order the cards were authored: the Higher ABQs, the
2013-2020 Higher papers, the 2026-2021 Higher papers, the 2026-2021 Ordinary
papers, the two choice-is-not-a-route passes, the 2020-2010 Ordinary
papers, the 2012-2010 Higher papers outside their ABQs and the post-generation edits; the corpus inventory is rebuilt last. Each generator
replaces only what it wrote, so re-running the chain on the committed files
must leave every one of them byte-identical. A hand edit to a generated card,
or a generator that no longer produces the committed text, shows up here.

--check (the default) backs up the generated files, runs the chain, compares,
and always restores the backup. --write leaves the regenerated files in place.

Some committed records have no generator, because they were written before
scripts were kept; the chain preserves them and never rewrites them:
  * the 2025 Higher ABQ pilot cards (four) and their review;
  * the 2013 Higher Section 3 Q1(B) route pool (its scheme marks the three
    approaches differently, so it stays routed);
  * the 2010-2024 Higher ABQ and 2013 S3Q1 entries in
    business-source-reviewed-topics.json;
  * the 2013-2020 Higher full-paper reviews in business-paper-reviews.json;
  * selection-review decisions already recorded (every generator skips a
    directive that has a review, so re-runs never overwrite one).

--schemes re-extracts the scheme .md files this work produced (extract-scheme.py
--marks-column --digit-mark-cells --glyph-ids --unnamed-glyphs) and compares them byte for byte. The 2021-2025
files come from the main Mark Bank pipeline (extract plus the append-scheme-*
passes) and the glyph-id repair, so they are not re-extracted here.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

CHAIN = [
    *[f'add-{y}-abq.py' for y in range(2010, 2025)], 'add-2026-abq.py',
    'add-2013-section1.py', 'add-2013-section3.py', 'add-2013-section3-q3-q7.py',
    'add-2014.py', 'add-2014-routes.py', 'add-2015.py', 'add-2015-routes.py',
    'add-2016.py', 'add-2017.py', 'add-2018.py', 'add-2019.py', 'add-2020.py',
    *[s for y in range(2026, 2020, -1) for s in (f'add-{y}.py', f'add-{y}-paper-reviews.py')],
    *[s for y in range(2026, 2020, -1) for s in (f'add-{y}-ol.py', f'add-{y}-ol-paper-reviews.py')],
    'collapse-choices.py', 'collapse-choose-one.py',
    'add-2020-ol.py', 'add-2020-ol-paper-reviews.py',
    'add-2019-ol.py', 'add-2019-ol-paper-reviews.py',
    'add-2018-ol.py', 'add-2018-ol-paper-reviews.py',
    'add-2017-ol.py', 'add-2017-ol-paper-reviews.py',
    'add-2016-ol.py', 'add-2016-ol-paper-reviews.py',
    'add-2015-ol.py', 'add-2015-ol-paper-reviews.py',
    'add-2014-ol.py', 'add-2014-ol-paper-reviews.py',
    'add-2013-ol.py', 'add-2013-ol-paper-reviews.py',
    'add-2012-ol.py', 'add-2012-ol-paper-reviews.py',
    'add-2011-ol.py', 'add-2011-ol-paper-reviews.py',
    'add-2010-ol.py', 'add-2010-ol-paper-reviews.py',
    'add-2012-hl.py', 'add-2012-hl-paper-reviews.py',
    'add-2011-hl.py', 'add-2011-hl-paper-reviews.py',
    'add-2010-hl.py', 'add-2010-hl-paper-reviews.py',
    'post-generation-edits.py',
]

OUTPUTS = [
    'components/MarkBank/cards/business/rubric-authored.json',
    'components/MarkBank/cards/business/route-pools.json',
    'scripts/markbank/authored/business-selection-reviews.json',
    'scripts/markbank/authored/business-paper-reviews.json',
    'scripts/markbank/authored/business-2013-hl-pending-review.json',
    'scripts/markbank/authored/business-corpus-inventory.json',
    'data/examTopics/business-source-reviewed-topics.json',
]

# Scheme files extracted in this work, with the extractor flags that made them.
SCHEMES = [f'{y}-hl' for y in range(2010, 2021)] + ['2010-ol', '2011-ol', '2012-ol', '2013-ol', '2014-ol', '2015-ol', '2016-ol', '2017-ol', '2018-ol', '2019-ol', '2020-ol', '2026-hl', '2026-ol']


def run(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode:
        sys.stderr.write(out.stdout[-2000:] + out.stderr[-4000:])
        raise SystemExit(f'failed: {" ".join(map(str, cmd))}')
    return out.stdout


def regenerate():
    for script in CHAIN:
        run([sys.executable, str(HERE / script)])
    run([sys.executable, 'scripts/markbank/authoring/business_corpus_inventory.py'])


def check_schemes():
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        for name in SCHEMES:
            year, level = name.split('-')
            pdf = f'paper-trail-corpus/markingschemes/{year}/LC033{"ALP" if level == "hl" else "GLP"}000EV.pdf'
            out = Path(tmp) / f'{name}.md'
            run([sys.executable, 'scripts/markbank/extract-scheme.py', pdf, '--marks-column', '--digit-mark-cells',
                 '--glyph-ids', '--unnamed-glyphs', '-o', str(out)])
            if out.read_bytes() != Path(f'examiner-reports/business/schemes/{name}.md').read_bytes():
                bad.append(name)
    return bad


def main():
    if not Path('paper-trail-corpus').exists():
        raise SystemExit('run from the repo root, with paper-trail-corpus/ present')
    write = '--write' in sys.argv
    backup = {p: Path(p).read_bytes() for p in OUTPUTS}
    try:
        regenerate()
        changed = [p for p in OUTPUTS if Path(p).read_bytes() != backup[p]]
    finally:
        if not write:
            for p, data in backup.items():
                Path(p).write_bytes(data)
    for p in changed:
        print(f'DIFFERS {p}')
    print(f'{len(CHAIN)} generators re-run; {len(OUTPUTS) - len(changed)}/{len(OUTPUTS)} generated files byte-identical')
    bad = check_schemes() if '--schemes' in sys.argv else []
    for name in bad:
        print(f'DIFFERS examiner-reports/business/schemes/{name}.md')
    if '--schemes' in sys.argv:
        print(f'{len(SCHEMES) - len(bad)}/{len(SCHEMES)} scheme files re-extract byte-identically')
    if (changed and not write) or bad:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
