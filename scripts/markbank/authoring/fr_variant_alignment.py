#!/usr/bin/env python3
"""Account for every French paper variant Paper Trail lists.

    python3 scripts/markbank/authoring/fr_variant_alignment.py          # write the ledger
    python3 scripts/markbank/authoring/fr_variant_alignment.py --check  # fail on drift

Each of the 98 variants (17 sittings x Higher/Ordinary x written/aural booklet,
English edition, plus the Irish-language editions of 2010-2018) is either
CARDED or DEFERRED with a written reason:

* carded (English edition): the local source the cards were reviewed from is
  byte-identical to the Paper Trail document, its scheme likewise; the cards and
  Atlas tasks cite that exact file; the sitting's paper census has no open ask.
* deferred (Irish-language edition): not carded, by decision (Irish-language
  editions are deferred). The same sitting's English edition is carded and
  listed as its counterpart.

The ledger is written to french-variant-alignment.json; --check (and
tests/test_fr_variant_alignment.py) recompute it and fail on any difference.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import sys

AUTH = Path(__file__).resolve().parent
ROOT = AUTH.parents[2]
LEDGER = AUTH / 'french-variant-alignment.json'
LEVEL = {'higher': 'hl', 'ordinary': 'ol'}
DEFERRAL = ('Irish-language (IV) edition. Irish-language editions of subjects are deferred by decision; this '
            'variant is not carded. The English edition of the same sitting is carded (see englishCounterpart).')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def variants():
    """The French entries of paperTrailData.ts, one per printed booklet."""
    text = (ROOT / 'paperTrailData.ts').read_text()
    block = text.split('  "french": [', 1)[1].split('\n  ],', 1)[0]
    out = []
    for entry in (json.loads(line.strip().rstrip(',')) for line in block.splitlines() if line.strip()):
        if entry.get('sitting') or entry['year'] < 2010:
            continue  # reviewed window only: June sittings from 2010
        for item in entry['papers']:
            out.append(dict(year=entry['year'], level=entry['level'], lang=entry['lang'], label=item['label'],
                            paper=f'exampapers/{entry["year"]}/{item["doc"]["f"]}',
                            scheme=f'markingschemes/{entry["year"]}/{item["scheme"]["f"]}' if item.get('scheme') else None,
                            fileid=item['doc']['f']))
    return out


def build():
    sys.path.insert(0, str(AUTH))
    import reconcile  # noqa: E402

    inventory = json.loads((AUTH / 'french-corpus-inventory.json').read_text())
    sources = inventory['sources']
    listed = variants()
    assert [(v['year'], v['level'], v['lang'], v['label'], v['paper'], v['scheme']) for v in listed] == \
        [(p['year'], p['level'], p['lang'], p['label'], p['paper'], p['scheme']) for p in inventory['papers']], \
        'Paper Trail variants differ from the verified inventory'

    decks = {name: json.loads((ROOT / f'components/MarkBank/cards/french/{name}.json').read_text())
             for name in ('writing', 'reading', 'cloze', 'listening')}
    shipped = {card['id'] for cards in decks.values() for card in cards}
    legacy = [card for card in json.loads((ROOT / 'scripts/markbank/authored/french.json').read_text())
              if card['id'] not in shipped]
    tasks = json.loads((ROOT / 'data/examTopics/french-reviewed-tasks.json').read_text())
    census = {(p['year'], p['level']): p for p in reconcile.reconcile_subject('french')['papers']}

    rows = []
    for v in listed:
        row = dict(year=v['year'], level=v['level'], lang=v['lang'], label=v['label'],
                   paper=v['paper'], paperSha256=sources[v['paper']]['sha256'],
                   scheme=v['scheme'], schemeSha256=sources[v['scheme']]['sha256'] if v['scheme'] else None)
        if v['lang'] == 'iv':
            twin = next(t for t in listed if t['lang'] == 'ev' and (t['year'], t['level'], t['label']) ==
                        (v['year'], v['level'], v['label']))
            row.update(status='deferred', reason=DEFERRAL, englishCounterpart=twin['paper'])
            rows.append(row)
            continue
        assert v['lang'] == 'ev', v
        component = 'A00' if v['label'] == 'Aural Paper' else '000'
        local_paper = f'examiner-reports/french/papers/{v["year"]}-{LEVEL[v["level"]]}-{component}-paper.pdf'
        local_scheme = f'examiner-reports/french/schemes/{v["year"]}-{LEVEL[v["level"]]}.pdf'
        assert sha(ROOT / local_paper) == row['paperSha256'], local_paper
        assert sha(ROOT / local_scheme) == row['schemeSha256'], local_scheme
        fileid = v['fileid'].removesuffix('.pdf')
        cards = {name: sum(1 for card in deck if card['year'] == v['year'] and card['level'] == v['level']
                           and card.get('paperFileid') == fileid) for name, deck in decks.items()}
        if component == '000':
            # The four preserved whole-letter cloze cards predate file ids; they
            # belong to the written booklet of their own sitting.
            cards['legacyCloze'] = sum(1 for card in legacy if card['year'] == v['year'] and card['level'] == v['level'])
        cards = {name: count for name, count in cards.items() if count}
        sitting = census[(v['year'], LEVEL[v['level']])]
        row.update(status='carded', localPaper=local_paper, localScheme=local_scheme, cards=cards,
                   atlasTasks=sum(1 for t in tasks if (t['year'], t['level'], t['lang'], t['fileid']) ==
                                  (v['year'], v['level'], 'ev', v['fileid'])),
                   sittingCensus=dict(leaves=sitting['leaves'], covered=sitting['covered'],
                                      excluded=sitting['excluded'], open=len(sitting['open'])))
        assert row['cards'] and row['atlasTasks'] and row['sittingCensus']['open'] == 0, row
        rows.append(row)

    # Every shipped card and every reviewed Atlas task belongs to exactly one variant.
    carded = [row for row in rows if row['status'] == 'carded']
    assert sum(sum(row['cards'].values()) for row in carded) == sum(map(len, decks.values())) + len(legacy)
    assert sum(row['atlasTasks'] for row in carded) == len(tasks)
    status = Counter(row['status'] for row in rows)
    return dict(subject='french', paperVariants=len(rows), carded=status['carded'], deferred=status['deferred'],
                byEdition=dict(sorted(Counter(f'{r["lang"]} {r["label"]}' for r in rows).items())),
                rule='Every Paper Trail variant is carded (English edition: byte-identical source, cards and Atlas '
                     'tasks citing the file, zero open asks for its sitting) or deferred with a written reason.',
                variants=rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if LEDGER.read_text() != text:
            raise SystemExit('French variant alignment drifted; review and rewrite the ledger')
        print('French variant alignment unchanged')
        return
    LEDGER.write_text(text)
    print(json.dumps({k: result[k] for k in ('paperVariants', 'carded', 'deferred', 'byEdition')}))


if __name__ == '__main__':
    main()
