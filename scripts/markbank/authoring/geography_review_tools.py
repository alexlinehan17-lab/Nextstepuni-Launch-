"""Audit aids for writing and checking a Geography review ledger.

These read the same official documents the generator reads and print what a
reviewer compares against the rendered pages; they write nothing into the
repository. The committed cards are reproduced by geography_cards.py alone
(run it with --check).

  python3 geography_review_tools.py dump YEAR LEVEL OUT_DIR
      Page text of both papers, the scheme's printed lines page by page, and
      the selection-directive scan the ledger must classify.
  python3 geography_review_tools.py draft LEDGER_MODULE OUT.json
      Build every card a ledger declares (placeholder companions), reporting
      any lift or scheme slice that fails, without touching the corpus.
  python3 geography_review_tools.py show OUT.json [QUESTION_REF_FILTER]
      Print each drafted card: prompt, criteria with their scheme lines and
      permitted marks, examiner directions and sources.
"""

import importlib
import json
import os
import sys

import geography_review as GR


def dump(year: int, level: str, out_dir: str) -> None:
    sitting = GR.Sitting.open(year, level)
    os.makedirs(out_dir, exist_ok=True)
    stem = f'{year}{GR.LEVEL_SHORT[level]}'
    with open(os.path.join(out_dir, f'{stem}-pagetext.txt'), 'w', encoding='utf-8') as handle:
        seen = set()
        for part, document in sitting.papers.items():
            if document.path in seen:
                continue
            seen.add(document.path)
            for page in range(1, len(document) + 1):
                handle.write(f'#### P{part} p{page} {document.page_text(page)}\n')
    with open(os.path.join(out_dir, f'{stem}-ms-lines.txt'), 'w', encoding='utf-8') as handle:
        for page in range(1, len(sitting.scheme) + 1):
            handle.write(f'== MS {page}\n')
            for line in sitting.scheme.lines(page):
                handle.write(f'    {line}\n')
    print({part: (os.path.basename(document.path), len(document))
           for part, document in sitting.papers.items()},
          (os.path.basename(sitting.scheme.path), len(sitting.scheme)))
    print(json.dumps(GR.selection_scan(sitting)))


def draft(module_name: str, out_path: str) -> None:
    module = importlib.import_module(module_name)
    sitting = GR.Sitting.open(module.YEAR, module.LEVEL)
    companions = {kind: {'kind': 'source-illustration', 'label': kind, 'title': kind, 'pages': [1],
                         'sourceFileid': kind, 'attribution': 'draft', 'presentationNote': 'draft'}
                  for kind in ('map', 'legend', 'aerial')}
    topics = {f'geography-{strand}-{topic}' for strand in range(9) for topic in range(12)}
    cards, errors = [], 0
    for task in module.TASKS:
        try:
            cards += GR.build_task_cards(sitting, task, 'FILE', companions, topics)
        except Exception as error:  # report every failing task, not just the first
            errors += 1
            print('ERR', task.key, str(error)[:600])
    print(len(cards), 'cards,', errors, 'errors')
    with open(out_path, 'w', encoding='utf-8') as handle:
        json.dump(cards, handle, ensure_ascii=False, indent=1)


def show(path: str, selector: str = '') -> None:
    with open(path, encoding='utf-8') as handle:
        cards = json.load(handle)
    for card in cards:
        if selector and selector not in card['questionRef']:
            continue
        print('=====', card['id'], '|', card['questionRef'], '|', card['totalMarks'], '| p',
              card['paperPage'], 'ms', card['schemePage'], '|', card['topicId'], card['atlasTopicIds'])
        print('STEM:', card['stem'])
        print('Q:', card['questionText'])
        for criterion in card['criteria']:
            marks = criterion['permittedMarks']
            shown = marks if len(marks) < 8 else f"[0..{criterion['maxMarks']}]x{len(marks)}"
            print('  C:', criterion['label'], '/', criterion['maxMarks'], shown,
                  criterion['guidanceKind'], '<-', criterion['guidance'])
        for direction in card['directions']:
            print('  D:', direction)
        sources = [card.get('sourceMaterial'), *card.get('additionalSourceMaterials', [])]
        print('  SRC:', [source.get('sourceFileid') or ('page', source['pages'])
                         for source in sources if source], 'REQ', card['taskRequirements'])


if __name__ == '__main__':
    command, *args = sys.argv[1:]
    if command == 'dump':
        dump(int(args[0]), args[1], args[2])
    elif command == 'draft':
        draft(args[0], args[1])
    elif command == 'show':
        show(*args)
    else:
        raise SystemExit(__doc__)
