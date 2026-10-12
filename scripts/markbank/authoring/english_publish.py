#!/usr/bin/env python3
"""Publish independently reviewed English papers to the runtime, paper by paper.

Only a paper whose OWN strict gate passes is published
(`english_review_gate.check_paper`). The corpus-wide gate may still refuse
because of other years; that never blocks a reviewed paper and never lets an
unreviewed one through.

Papers served by the 650 legacy runtime cards (2021-2025) are refused unless
`english-legacy-bridge.json` maps every legacy card of that paper to the
reviewed task that replaces it: "same-id" (the published card keeps the legacy
id and saved progress) or "alias" (an explicit progress alias in
components/MarkBank/cardAliases.ts). The legacy manifest (`authored.json`) is
never rewritten; the runtime only stops serving the bridged legacy cards.

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

import english_choices
from english_cards import comparable
from english_complete import ROOT, inventory
import english_full_cards as parser
from english_review_gate import check_paper

AUTHORED = ROOT / 'scripts/markbank/authored'
CARDS_DIR = ROOT / 'components/MarkBank/cards/english'
EXAM_TOPICS = ROOT / 'data/examTopics'
GRIDS = AUTHORED / 'english-marking-grids.json'
LEGACY_BRIDGE = AUTHORED / 'english-legacy-bridge.json'
CARD_ALIASES = ROOT / 'components/MarkBank/cardAliases.ts'
PRINTED_DUPLICATES = AUTHORED / 'english-printed-duplicates.json'
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
        'taskRequirements': list(route['taskRequirements']),
    }
    if route.get('printedChoice'):
        # One card for a printed choice the scheme marks identically: the task
        # check states the choice the student makes (english_choices).
        card['taskRequirements'].insert(1, route['printedChoice']['requirement'])
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


def legacy_additional_sources(bridged=frozenset()):
    """Aggregate reviewed companion readers of leaf tasks onto legacy bundled parents.

    A legacy runtime card (2021-2025) bundles separately marked leaf tasks. A
    reviewed `additionalSources` entry on one of those leaves must reach the
    bundled card, or the legacy parent would silently lose a required reader.
    A bridged paper's legacy cards are no longer served, so it is skipped.
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
        if not extra or paper_id not in papers or paper_id in bridged:
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


def squashed(text):
    """Whitespace-free, dash-unified text: a lifted item must match its print exactly otherwise."""
    return re.sub(r'\s', '', re.sub(r'[‐‑‒–—−]', '-', text.replace('\xa0', ' ')))


def choice_signature(card):
    """A route card with its choice label removed: what the student is marked on."""
    label = card.get('choiceLabel', '')
    stripped = {key: value for key, value in card.items() if key not in ('id', 'choiceParentId', 'choiceLabel')}
    stripped['questionRef'] = stripped['questionRef'].replace(' · ' + label, '')
    stripped['questionText'] = re.sub(r'\n\nFor this practice response — .*$', '', stripped['questionText'], flags=re.S)
    return json.dumps(stripped, sort_keys=True, ensure_ascii=False)


def refuse_label_only_routes(cards):
    """Refuse route cards that differ only in their choice label (coordinator rule, 2026-10-12).

    Route cards are allowed only when the scheme prints different marking
    content per route; otherwise the task is one printed-choice card.
    """
    groups = {}
    for card in cards:
        if card.get('choiceParentId'):
            groups.setdefault(card['choiceParentId'], []).append(card)
    for parent, members in sorted(groups.items()):
        if len({choice_signature(card) for card in members}) == 1:
            raise ValueError(f'{parent}: {len(members)} route cards differ only in a choice label; '
                             'publish one printed-choice card')


def task_signature(card):
    """What makes two printed tasks the same practice task."""
    return json.dumps({key: card.get(key) for key in (
        'questionText', 'totalMarks', 'assessment', 'sourceMaterial', 'additionalSourceMaterials',
        'topicId', 'conceptId', 'stem', 'taskRequirements')}, sort_keys=True, ensure_ascii=False)


def merge_printed_duplicates(key, cards, duplicates):
    """Publish a task printed more than once on one paper as ONE card.

    A declared duplicate must match its canonical card exactly (wording,
    tariff, grid, reader, requirements); it is dropped and its printed place
    is kept as an Atlas placement. An undeclared identical task is refused.
    """
    by_id = {card['id']: card for card in cards}
    dropped = set()
    for dup, entry in sorted(duplicates.items()):
        if not dup.startswith(key + '-'):
            continue
        canonical = by_id.get(entry['canonical'])
        if dup not in by_id or not canonical or not entry.get('reason', '').strip():
            raise ValueError(f'{dup}: declared printed duplicate is not published beside its canonical card')
        if task_signature(by_id[dup]) != task_signature(canonical):
            raise ValueError(f'{dup}: declared printed duplicate differs from {entry["canonical"]}')
        placements = canonical.setdefault('atlasPlacements', [])
        place = by_id[dup]['atlas']
        if place != canonical['atlas'] and place not in placements:
            placements.append(place)
        if not placements:
            canonical.pop('atlasPlacements')
        dropped.add(dup)
    kept = [card for card in cards if card['id'] not in dropped]
    seen = {}
    for card in kept:
        other = seen.setdefault(task_signature(card), card['id'])
        if other != card['id']:
            raise ValueError(f'{card["id"]}: printed identically to {other}; declare it in english-printed-duplicates.json')
    return kept, len(dropped)


def card_aliases():
    return dict(re.findall(r'^\s*"([^"]+)": "([^"]+)",?$', CARD_ALIASES.read_text(), re.M))


def apply_bridge(key, bridge, record, emitted, legacy_manifest):
    """Prove a bridged paper keeps every legacy card id, and carry lifted extras.

    Every legacy card of the paper is mapped exactly once; a same-id card is
    published under its legacy id; an alias names a published card, is not
    itself published and is registered in cardAliases.ts; the legacy prompt and
    its target are the same printed task (one contains the other); and every
    lifted indicative item is printed on the bound scheme page.
    """
    if bridge['paperSha256'] != record['questionPaper']['sha256']:
        raise ValueError(f'{key}: legacy bridge bound to a different paper')
    if any(old.startswith(key + '-') for old in legacy_manifest.get('withdrawnAliases', {})):
        raise ValueError(f'{key}: legacy withdrawn aliases need their own bridge entries')
    legacy = {card['id']: card for card in legacy_manifest['cards'] if card['id'].startswith(key + '-')}
    entries = bridge['legacyCards']
    if set(entries) != set(legacy):
        raise ValueError(f'{key}: legacy bridge must map exactly its legacy cards; '
                         f'missing={sorted(set(legacy) - set(entries))}, extra={sorted(set(entries) - set(legacy))}')
    by_id = {card['id']: card for card in emitted}
    registered = card_aliases()
    with fitz.open(ROOT / record['markingScheme']['path']) as doc:
        for old, entry in sorted(entries.items()):
            if entry['kind'] == 'same-id':
                target = by_id.get(old)
                if not target:
                    raise ValueError(f'{old}: same-id bridge but the reviewed paper publishes no such card')
            elif entry['kind'] == 'alias':
                target = by_id.get(entry['to'])
                if old in by_id or not target:
                    raise ValueError(f'{old}: alias bridge must leave the legacy id unpublished and name a published card')
                if registered.get(old) != entry['to']:
                    raise ValueError(f'{old}: register the progress alias -> {entry["to"]} in cardAliases.ts')
            else:
                raise ValueError(f'{old}: unknown bridge kind {entry["kind"]}')
            legacy_text, target_text = comparable(legacy[old]['questionText']), comparable(target['questionText'])
            if legacy_text not in target_text and target_text not in legacy_text:
                raise ValueError(f'{old}: legacy prompt and bridged card are not the same printed task')
            if target['totalMarks'] > legacy[old]['totalMarks']:
                raise ValueError(f'{old}: bridged card exceeds the legacy tariff')
            lifted = entry.get('indicativeMaterial')
            if lifted:
                if entry['kind'] != 'same-id' or lifted['schemePage'] not in target['schemePages']:
                    raise ValueError(f'{old}: lifted indicative material must come from the card\'s own scheme page')
                page = squashed(doc[lifted['schemePage'] - 1].get_text())
                missing = [item for item in lifted['items'] if squashed(item) not in page]
                if missing or not lifted['items']:
                    raise ValueError(f'{old}: indicative items not printed on scheme PDF{lifted["schemePage"]}: {missing}')
                target['indicativeMaterial'] = lifted['items']


def publish():
    records = inventory()['papers']
    grids = read(GRIDS)
    verify_grids(grids, records)
    legacy = legacy_papers()
    bridges = read(LEGACY_BRIDGE)['papers'] if LEGACY_BRIDGE.exists() else {}
    reviews = read(AUTHORED / 'english-task-review.json')['tasks']
    printed_duplicates = read(PRINTED_DUPLICATES)['duplicates'] if PRINTED_DUPLICATES.exists() else {}
    finite = sorted(tid for tid, decision in read(AUTHORED / 'english-selection-review.json')['decisions'].items()
                    if decision['kind'] == 'finite')
    if finite:
        # Any paper, published or not: a choice-only route group never enters the ledger.
        raise ValueError(english_choices.FINITE_REFUSAL.format(task=', '.join(finite)))
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
        refuse_label_only_routes(emitted)
        emitted, duplicates = merge_printed_duplicates(key, emitted, printed_duplicates)
        if key in bridges:
            apply_bridge(key, bridges[key], record, emitted, read(CARDS_DIR / 'authored.json'))
        cards[record['level']].extend(emitted)
        published.append({'paperId': key, 'year': record['year'], 'level': record['level'],
                          'paper': record['paper'], 'tasks': report['baseTasks'], 'cards': len(emitted),
                          'printedDuplicates': duplicates,
                          'paperSha256': record['questionPaper']['sha256'],
                          'schemeSha256': record['markingScheme']['sha256']})

    ids = [card['id'] for level in cards.values() for card in level]
    if len(set(ids)) != len(ids):
        raise ValueError('Repeated published English card id')
    if any('.' in cid or '/' in cid or '__' in cid for cid in ids):
        raise ValueError('Published English card id is not a valid Mark Bank id')
    legacy_manifest = read(CARDS_DIR / 'authored.json')
    legacy_ids = {card['id'] for card in legacy_manifest['cards']} | set(legacy_manifest.get('withdrawnAliases', {}))
    bridged_papers = {paper['paperId'] for paper in published if paper['paperId'] in bridges}
    same_ids = {old for key in bridged_papers for old, entry in bridges[key]['legacyCards'].items()
                if entry['kind'] == 'same-id'}
    if (legacy_ids & set(ids)) - same_ids:
        raise ValueError('Published card would reuse a legacy runtime id outside a same-id bridge')

    outputs = {}
    level_papers = {level: {paper['paperId'] for paper in published if paper['level'] == level}
                    for level in ('higher', 'ordinary')}
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
            'legacyAdditionalSources': {cid: sources for cid, sources in legacy_additional_sources(bridged_papers).items()
                                        if any(c['id'] == cid and c['level'] == level for c in legacy_manifest['cards'])},
            'bridgedPapers': sorted(key for key in bridged_papers if key in level_papers[level]),
            'bridgedLegacyIds': sorted(old for key in bridged_papers if key in level_papers[level]
                                       for old in bridges[key]['legacyCards']),
            'bridgeAliases': {old: entry['to'] for key in sorted(bridged_papers) if key in level_papers[level]
                              for old, entry in sorted(bridges[key]['legacyCards'].items()) if entry['kind'] == 'alias'},
            'cardCount': len(cards[level]),
            'cards': cards[level],
        }
    archive, question_runtime = atlas_outputs(cards)
    outputs[EXAM_TOPICS / 'english-reviewed-archive-topics.json'] = archive
    outputs[EXAM_TOPICS / 'english-reviewed-question-runtime.json'] = question_runtime
    return outputs, published, refused


# ----------------------------------------------------------------- coverage

def bridged_published_papers():
    """Legacy (2021-2025) papers now served by their published reviewed cards."""
    return {paper for level in ('higher', 'ordinary')
            for paper in read(CARDS_DIR / f'published-{level}.json').get('bridgedPapers', [])}


def bridged_legacy_ids():
    """Legacy authored.json ids the runtime no longer serves (published same-id or aliased)."""
    return {cid for level in ('higher', 'ordinary')
            for cid in read(CARDS_DIR / f'published-{level}.json').get('bridgedLegacyIds', [])}


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
            continue  # a bridged legacy paper is published, so its row comes from the manifest
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
    rows = {}
    for level, node in needed:
        slug = re.sub(r'[^a-z0-9]+', '-', archive_label(node, names).lower()).strip('-')
        topic_id = f'english-{level}-{slug}-reviewed-archive'
        rows[topic_id] = {'id': topic_id, 'level': level, 'slug': slug, 'label': archive_label(node, names),
                          'curriculumNodeIds': archive_nodes(level, node)}
        topics_by_node.setdefault((level_code[level], node), []).append(topic_id)
    # Append-only: archive topics already generated keep their order (and so
    # their runtime row index); a newly needed one is added after them.
    archive = [rows.pop(row['id']) for row in existing_archive if row['id'] in rows] + list(rows.values())
    if len({row['id'] for row in archive}) != len(archive):
        raise ValueError('Repeated reviewed archive topic id')

    topic_ids, mappings = [], {}
    for level in ('higher', 'ordinary'):
        for card in cards[level]:
            topics = topics_by_node[(level_code[level], card['topicId'])]
            for place in [card['atlas'], *card.get('atlasPlacements', [])]:
                key = (level_code[level], 'e', card['year'], f'p{card["paper"]}', place['fileid'], place['n'])
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
