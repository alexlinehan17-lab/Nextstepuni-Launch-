#!/usr/bin/env python3
"""Publish independently reviewed English papers to the runtime, paper by paper.

Only a paper whose OWN strict gate passes is published
(`english_review_gate.check_paper`). The corpus-wide gate may still refuse
because of other years; that never blocks a reviewed paper and never lets an
unreviewed one through.

Papers served by the 650 legacy runtime cards (2021-2025) are refused unless a
legacy bridge maps every legacy card of that paper. None exist yet, so the
legacy manifest (`authored.json`), its ids, aliases and `n` are untouched.

Outputs (all generated; `--check` fails when any is stale):
- components/MarkBank/cards/english/published-{higher,ordinary}.json
- data/examTopics/english-reviewed-archive-topics.json
- data/examTopics/english-reviewed-question-runtime.json

    python3 scripts/markbank/authoring/english_publish.py
    python3 scripts/markbank/authoring/english_publish.py --check
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import re
import sys

import fitz

from english_complete import ROOT, inventory
import english_full_cards as parser
from english_review_gate import check_paper

AUTHORED = ROOT / 'scripts/markbank/authored'
CARDS_DIR = ROOT / 'components/MarkBank/cards/english'
EXAM_TOPICS = ROOT / 'data/examTopics'
GRIDS = AUTHORED / 'english-marking-grids.json'
LEGACY_BRIDGE = AUTHORED / 'english-legacy-bridge.json'
CENSUS = AUTHORED / 'english-census.json'


def read(path):
    return json.loads(path.read_text())


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=1) + '\n'


# ----------------------------------------------------------------- grids

def cell_marks(cell):
    """Marks a printed grid cell permits: '30-26', '85-100', '7', '2/1'."""
    if '/' in cell:
        return sorted({int(part) for part in cell.split('/')})
    if '-' in cell:
        low, high = sorted(int(part) for part in cell.split('-'))
        return list(range(low, high + 1))
    return [int(cell)]


def family_cells(family):
    for tariff in family['discrete'].values():
        for row, cells in tariff.items():
            yield from cells
    for tariff in family['combined'].values():
        for row, cells in tariff.items():
            if isinstance(cells, list):
                yield from cells


def page_tokens(path, pages):
    with fitz.open(ROOT / path) as doc:
        text = ' '.join(doc[page - 1].get_text() for page in pages)
    text = text.replace('\xa0', ' ')
    text = re.sub(r'[‐‑‒–—−]', '-', text)
    return Counter(re.sub(r'\s', '', token) for token in re.findall(r'\d+\s*-\s*\d+|\d+/\d+|\d+', text))


def normalised_cell(cell):
    return cell.replace(' ', '')


def verify_grids(grids, records):
    """Bind every transcribed grid to the exact scheme PDF and its printed cells."""
    schemes = {}
    for record in records:
        schemes.setdefault((record['year'], record['level']), set()).add(
            (record['markingScheme']['path'], record['markingScheme']['sha256']))
    for key, sitting in grids['sittings'].items():
        year, level = key.split('-')
        bound = schemes.get((int(year), level), set())
        if (sitting['scheme'], sitting['schemeSha256']) not in bound:
            raise ValueError('Marking grid bound to a different scheme: ' + key)
        if hashlib.sha256((ROOT / sitting['scheme']).read_bytes()).hexdigest() != sitting['schemeSha256']:
            raise ValueError('Scheme changed under a transcribed grid: ' + key)
        family = grids['families'][sitting['family']]
        if family['level'] != level:
            raise ValueError('Grid family level differs from its sitting: ' + key)
        printed = page_tokens(sitting['scheme'], sitting['gridPages'])
        wanted = Counter(normalised_cell(cell) for cell in family_cells(family))
        missing = wanted - printed
        if missing:
            raise ValueError(f'{key}: transcribed cells not printed on PDF{sitting["gridPages"]}: {dict(missing)}')
        if sitting['capRule']['kind'] not in ('none', 'purpose-primacy', 'language-at-d-band'):
            raise ValueError('Unknown cap rule: ' + key)


# ----------------------------------------------------------------- cards

ALLOCATION_KEYS = {'PC': 'P+C', 'LM': 'L+M', 'P+C': 'P+C', 'L+M': 'L+M', 'P': 'P', 'C': 'C', 'L': 'L', 'M': 'M'}


def assessment_for(task, review, sitting_key, grids):
    criteria = review['criteria']
    family = grids['families'][grids['sittings'][sitting_key]['family']]
    tariff = str(task['totalMarks'])
    if criteria['mode'] in ('holistic', 'combined'):
        if tariff not in family['combined']:
            raise ValueError(f'{task["id"]}: no printed combined grid for {tariff} marks in {sitting_key}')
        result = {'mode': 'combined', 'grid': sitting_key}
    elif criteria['mode'] == 'discrete':
        if tariff not in family['discrete']:
            raise ValueError(f'{task["id"]}: no printed discrete grid for {tariff} marks in {sitting_key}')
        result = {'mode': 'discrete', 'grid': sitting_key}
    else:
        raise ValueError(f'{task["id"]}: unknown reviewed criteria mode {criteria["mode"]}')
    if criteria.get('allocation'):
        allocation = {ALLOCATION_KEYS[key]: value for key, value in criteria['allocation'].items()}
        if sum(allocation.values()) != task['totalMarks']:
            raise ValueError(f'{task["id"]}: reviewed allocation does not sum to the tariff')
        if result['mode'] == 'discrete' and set(allocation) != {'P', 'C', 'L', 'M'}:
            raise ValueError(f'{task["id"]}: discrete allocation must be P/C/L/M')
        result['allocation'] = allocation
    elif result['mode'] == 'discrete':
        raise ValueError(f'{task["id"]}: discrete task without a reviewed allocation')
    return result


def stem_for(task):
    stem = task.get('stem') or ''
    notes = task.get('contextNotes') or []
    if notes:
        stem = (stem + ' — ' if stem else '') + ' '.join(notes)
    return stem or None


def card_record(route, record, review, grids):
    sitting_key = f'{record["year"]}-{record["level"]}'
    if sitting_key not in grids['sittings']:
        raise ValueError('No transcribed marking grid for ' + sitting_key)
    card = {
        'id': route['id'], 'year': record['year'], 'level': record['level'], 'paper': record['paper'],
        'questionRef': route['questionRef'], 'questionText': route['questionText'],
        'totalMarks': route['totalMarks'], 'topicId': route['topicId'], 'conceptId': route['conceptId'],
        'taskRequirements': route['taskRequirements'],
    }
    stem = stem_for(route)
    if stem:
        card['stem'] = stem
    for field in ('sourceMaterial', 'additionalSourceMaterials'):
        if route.get(field):
            card[field] = route[field]
    if route.get('choiceParentId'):
        card['choiceParentId'] = route['choiceParentId']
        card['choiceLabel'] = route['choiceRoute']['label']
    card['schemePages'] = review['schemePages']
    card['assessment'] = assessment_for(route, review, sitting_key, grids)
    card['paperFileid'] = record['paperFileid'].removesuffix('.pdf')
    card['atlas'] = {'fileid': record['paperFileid'], 'n': str(route['atlasParent'])}
    return card


def legacy_papers():
    census = read(CENSUS)
    return {f"english-{ask['year']}-{ask['level']}-p{ask['paper']}" for ask in census['asks']}


def legacy_additional_sources():
    """Aggregate reviewed companion readers of leaf tasks onto legacy bundled parents.

    A legacy runtime card (2021-2025) bundles separately marked leaf tasks. A
    reviewed `additionalSources` entry on one of those leaves must reach the
    bundled card, or the legacy parent would silently lose a required reader.
    """
    census = read(CENSUS)
    manifest = read(CARDS_DIR / 'authored.json')
    aliases = manifest.get('withdrawnAliases', {})
    legacy_ids = sorted({aliases.get(ask['id'], ask['id']) for ask in census['asks']}, key=len, reverse=True)
    papers = legacy_papers()
    attachments = read(AUTHORED / 'english-source-review.json')['attachments']
    aggregated = {}
    for task_id, attachment in sorted(attachments.items()):
        extra = attachment.get('additionalSources') or []
        paper_id = re.match(r'^(english-\d{4}-(?:hl|ol)-p[12])-', task_id).group(1)
        if not extra or paper_id not in papers:
            continue
        parent = next((cid for cid in legacy_ids if task_id == cid or task_id.startswith(cid + '-')), None)
        if not parent:
            raise ValueError('Reviewed companion reader has no legacy parent card: ' + task_id)
        sources = aggregated.setdefault(parent, [])
        for item in extra:
            source = parser.source_from_attachment(item, task_id)
            if source not in sources:
                sources.append(source)
    return aggregated


def publish():
    records = inventory()['papers']
    grids = read(GRIDS)
    verify_grids(grids, records)
    legacy = legacy_papers()
    bridges = read(LEGACY_BRIDGE)['papers'] if LEGACY_BRIDGE.exists() else {}
    reviews = read(AUTHORED / 'english-task-review.json')['tasks']
    visual = {entry['paperId']: entry for entry in read(AUTHORED / 'english-visual-review.json')['papers']}

    published, refused, cards = [], [], {'higher': [], 'ordinary': []}
    for record in sorted(records, key=lambda r: (-r['year'], r['level'], r['paper'])):
        key = record['id']
        entry = visual[key]
        if key in legacy and key not in bridges:
            refused.append({'paperId': key, 'reason': 'served by legacy runtime cards; no legacy bridge'})
            continue
        if not (entry['visualSweepComplete'] and entry.get('independentPaperTally')):
            refused.append({'paperId': key, 'reason': 'independent review not recorded'})
            continue
        _, tasks = parser.extract_record(record)
        report, routes = check_paper(record, tasks, strict=False)
        if any(report['pending'].values()):
            refused.append({'paperId': key, 'reason': 'paper gate pending',
                            'pending': {k: len(v) for k, v in report['pending'].items() if v}})
            continue
        by_task = {task['id']: task for task in tasks}
        emitted = []
        for route in routes:
            task_id = route.get('choiceParentId', route['id'])
            if task_id not in by_task:
                raise ValueError('Route without a reviewed task: ' + route['id'])
            emitted.append(card_record(route, record, reviews[task_id], grids))
        cards[record['level']].extend(emitted)
        published.append({'paperId': key, 'year': record['year'], 'level': record['level'],
                          'paper': record['paper'], 'tasks': report['baseTasks'], 'cards': len(emitted),
                          'paperSha256': record['questionPaper']['sha256'],
                          'schemeSha256': record['markingScheme']['sha256']})

    ids = [card['id'] for level in cards.values() for card in level]
    if len(set(ids)) != len(ids):
        raise ValueError('Repeated published English card id')
    if any('.' in cid or '/' in cid or '__' in cid for cid in ids):
        raise ValueError('Published English card id is not a valid Mark Bank id')
    legacy_manifest = read(CARDS_DIR / 'authored.json')
    legacy_ids = {card['id'] for card in legacy_manifest['cards']} | set(legacy_manifest.get('withdrawnAliases', {}))
    if legacy_ids & set(ids):
        raise ValueError('Published card would reuse a legacy runtime id')

    outputs = {}
    for level in ('higher', 'ordinary'):
        sittings = sorted({card['assessment']['grid'] for card in cards[level]})
        families = sorted({grids['sittings'][s]['family'] for s in sittings})
        outputs[CARDS_DIR / f'published-{level}.json'] = {
            'subject': 'english', 'level': level,
            'rule': ('Generated by english_publish.py from papers whose own strict review gate passes. '
                     'Never hand-edit; legacy 2021-2025 cards live in authored.json.'),
            'papers': [paper for paper in published if paper['level'] == level],
            'grids': {
                'families': {name: grids['families'][name] for name in families},
                'sittings': {name: {k: grids['sittings'][name][k] for k in
                                    ('family', 'gridPages', 'capRule', 'capRulePage')} for name in sittings},
            },
            'legacyAdditionalSources': {cid: sources for cid, sources in legacy_additional_sources().items()
                                        if any(c['id'] == cid and c['level'] == level for c in legacy_manifest['cards'])},
            'cardCount': len(cards[level]),
            'cards': cards[level],
        }
    archive, question_runtime = atlas_outputs(cards)
    outputs[EXAM_TOPICS / 'english-reviewed-archive-topics.json'] = archive
    outputs[EXAM_TOPICS / 'english-reviewed-question-runtime.json'] = question_runtime
    return outputs, published, refused


# ----------------------------------------------------------------- coverage

def coverage_census_papers():
    """Coverage rows beyond the legacy 2021-2025 census.

    Published papers contribute one leaf per published card (task or finite
    route); the publisher already proved that count equals the paper's
    independent visual tally. Every other non-legacy paper is DECLARED OPEN:
    its extracted candidate tasks are listed, labelled as unreviewed, so the
    ratchet shows the work outstanding instead of hiding it. Candidate counts
    are parser output, not an independent denominator.
    """
    legacy = legacy_papers()
    rows, published_ids = [], set()
    for level in ('higher', 'ordinary'):
        manifest = read(CARDS_DIR / f'published-{level}.json')
        for paper in manifest['papers']:
            cards = [card for card in manifest['cards'] if card['id'].startswith(paper['paperId'] + '-')]
            published_ids.add(paper['paperId'])
            rows.append({'year': paper['year'], 'level': 'hl' if level == 'higher' else 'ol',
                         'paper': paper['paper'], 'status': 'published',
                         'leaves': [(card['id'], card['questionRef']) for card in cards]})
    for record in inventory()['papers']:
        if record['id'] in legacy or record['id'] in published_ids:
            continue
        _, tasks = parser.extract_record(record)
        rows.append({'year': record['year'], 'level': 'hl' if record['level'] == 'higher' else 'ol',
                     'paper': record['paper'], 'status': 'unreviewed',
                     'leaves': [(task['id'], task['questionRef'] + ' (unreviewed candidate task)') for task in tasks]})
    return rows


# ----------------------------------------------------------------- atlas

def curriculum_names():
    source = (ROOT / 'curriculum.ts').read_text()
    return dict(re.findall(r'"id": "(english-[\d-]+)",\s*"name": "([^"]+)"', source))


def archive_label(node, names):
    name = names[node]
    if node.startswith('english-12-'):
        return 'Text - ' + re.sub(r'\s*\([^)]*\)\s*$', '', name)
    if node.startswith('english-11-'):
        return 'Poetry - ' + name.split()[-1]
    if node.startswith('english-7-'):
        return 'Comparative - ' + name
    raise ValueError('No archive label rule for ' + node)


def archive_nodes(level, node):
    if node.startswith('english-12-'):
        return ['english-6-0', node]
    if node.startswith('english-11-'):
        return ['english-8-0' if level == 'higher' else 'english-8-1', node]
    if node.startswith('english-7-'):
        return [node]
    raise ValueError('No archive node rule for ' + node)


def atlas_outputs(cards):
    """Additive Atlas links: archive topics for absent nodes plus exact block mappings."""
    runtime = read(EXAM_TOPICS / 'english-runtime.json')
    existing_archive = read(EXAM_TOPICS / 'english-reviewed-archive-topics.json')['topics'] \
        if (EXAM_TOPICS / 'english-reviewed-archive-topics.json').exists() else []
    reviewed_archive_ids = {row['id'] for row in existing_archive}
    base_topics = [row for row in runtime['topics'] if row[0] not in reviewed_archive_ids]
    names = curriculum_names()
    level_code = {'higher': 'h', 'ordinary': 'o'}
    topics_by_node = {}
    for row in base_topics:
        for node in row[5]:
            topics_by_node.setdefault((row[6], node), []).append(row[0])

    archive = []
    needed = sorted({(card['level'], card['topicId']) for level in cards.values() for card in level
                     if (level_code[card['level']], card['topicId']) not in topics_by_node})
    for level, node in needed:
        slug = re.sub(r'[^a-z0-9]+', '-', archive_label(node, names).lower()).strip('-')
        topic_id = f'english-{level}-{slug}-reviewed-archive'
        archive.append({'id': topic_id, 'level': level, 'slug': slug, 'label': archive_label(node, names),
                        'curriculumNodeIds': archive_nodes(level, node)})
        topics_by_node.setdefault((level_code[level], node), []).append(topic_id)
    if len({row['id'] for row in archive}) != len(archive):
        raise ValueError('Repeated reviewed archive topic id')

    topic_ids, mappings = [], {}
    for level in ('higher', 'ordinary'):
        for card in cards[level]:
            topics = topics_by_node[(level_code[level], card['topicId'])]
            key = (level_code[level], 'e', card['year'], f'p{card["paper"]}', card['atlas']['fileid'], card['atlas']['n'])
            mappings.setdefault(key, [])
            for topic in topics:
                if topic not in topic_ids:
                    topic_ids.append(topic)
                if topic_ids.index(topic) not in mappings[key]:
                    mappings[key].append(topic_ids.index(topic))
    question_runtime = {
        'schemaVersion': 1, 'subjectId': 'english',
        'rule': ('Additive exact-booklet links for independently reviewed, published English papers. '
                 'Unioned with existing Atlas topics; never replaces a mapping.'),
        'topicIds': topic_ids,
        'questionMappings': [[*key, sorted(indexes)] for key, indexes in sorted(mappings.items(), key=lambda item: (
            -item[0][2], item[0][0], item[0][3], int(item[0][5])))],
    }
    return {'schemaVersion': 1, 'subjectId': 'english',
            'rule': 'Archive topics for canonical nodes that published reviewed cards need and the reference menu lacks.',
            'topics': archive}, question_runtime


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--check', action='store_true')
    options = args.parse_args()
    outputs, published, refused = publish()
    stale = []
    for path, value in outputs.items():
        text = dump(value)
        if options.check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(text)
    summary = {'published': len(published), 'cards': sum(p['cards'] for p in published),
               'refused': len(refused)}
    print(json.dumps(summary))
    for paper in published:
        print(f"  publish {paper['paperId']}: {paper['tasks']} tasks -> {paper['cards']} cards")
    if stale:
        print('Stale generated English files: ' + ', '.join(stale), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
