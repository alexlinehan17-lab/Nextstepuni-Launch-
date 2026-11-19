#!/usr/bin/env python3
"""Independent 2013 Ordinary census after the full 36-page original sweep."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
 ('paper', 'examiner-reports/japanese/papers/2013-ol-000-paper.pdf', '60e7746677773e02248892c88d25ef79416fff3627afcab2fbf61e94756dd3e4'),
 ('aural', 'examiner-reports/japanese/papers/2013-ol-A00-paper.pdf', '3e7d66bbb89fdf43d90374851501c743140d1b01a4538902b41c10a3e4ca892e'),
 ('scheme', 'examiner-reports/japanese/schemes/2013-ol.pdf', '52d26642f93c8f6e01c84e3eda961db01a643ba645848692770fc9c764887e08'),
]
TASKS = []

def task(section, q, marks, pp, sp, atlas, roman=None):
 component = 'aural' if section.startswith('L') else 'paper'
 TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component, 'paperPages': [pp], 'schemePages': sp,
  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})

def build():
 task('1A', None, 15, 2, [5], 1)
 task('1B', None, 20, 3, [5], 1)
 task('2A', 1, 8, 5, [6], 2)
 task('2A', 2, 4, 5, [6], 2)
 task('2B', None, 15, 5, [6], 2)
 task('2C', None, 5, 6, [7], 6)
 task('3A', 1, 8, 9, [7], 3)
 for q, marks in [(2, 3), (3, 2)]:
  for roman in ['i', 'ii', 'iii']: task('3A', q, marks, 9, [7], 3, roman)
 task('3B', None, 10, 10, [7, 8], 7)
 task('3C', 1, 10, 10, [8], 8)
 task('3C', 2, 10, 11, [8], 9)
 task('4', None, 30, 12, [9], 4)
 task('5', None, 50, 13, [9, 10], 5)
 for q in range(1, 5):
  for roman in ['i', 'ii']: task('LA', q, 3, 2, [3], q, roman)
 for roman in ['i', 'ii', 'iii']: task('LB', 1, 3, 3, [3], 10, roman)
 for roman, marks in [('i', 1), ('ii', 4), ('iii', 4), ('iv', 4), ('v', 4)]: task('LB', 2, marks, 3, [3], 11, roman)
 for q, values in [(1, [3, 3, 4]), (2, [3, 3, 3]), (3, [3, 4])]:
  for roman, marks in zip(['i', 'ii', 'iii'], values): task('LC', q, marks, 4, [4], 11 + q, roman)
 for q, marks in enumerate([1, 3, 3, 3, 3, 3, 3, 3, 2], 1): task('LD', q, marks, 5, [4 if q <= 5 else 5], q + 14 if q <= 4 else q)
 assert len(TASKS) == 51
 totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
  ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
  ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
 assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
 sources = []
 for component, path, digest in SOURCES:
  assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
  sources.append({'component': component, 'path': path, 'sha256': digest})
 return {'subjectId': 'japanese', 'year': 2013, 'level': 'ol', 'reviewedAt': '2026-11-10',
  'method': 'Independent visual sweep of every original page: sixteen written, eight aural and twelve scheme pages, before authoring. The separately priced listening/comprehension tasks and whole finite pools were compared against the original scheme, not inferred from parser counts.',
  'sources': sources, 'tasks': TASKS, 'checksums': totals,
  'candidateMaximum': {'written': 200, 'listening': 100, 'total': 300, 'writingChoice': 'All five written questions. Q4 all ten blanks without reusing a word; Q5 any five of seven responses.'},
  'pageRoles': {
   'paper': dict(zip(map(str, range(1, 17)), [
    'cover: written200, all five questions', 'Q1A complete sports floorplan, given batting6, five required areas',
    'Q1B complete main/annex department-store floorplans; given Sakura Hall main10; five required building/floor pairs',
    'Q2 complete four favourite-character profiles with pictures, names and vocabulary',
    'Q2A required four character matches; four details under scheme anytwo quota; B five truth/evidence pairs and given example',
    'Q2C open culture discussion, English instruction', 'explicit blank',
    'Q3 full Rikako email, blood-type passage, underlined kanji, ruby and vocabulary',
    'Q3A required four blood-type cells, three Japanese responses and three four-option MCQs',
    'Q3B ten required reading MCQs with example; Q3C1 five required present-tense transformations with example',
    'Q3C2 five required particle MCQs with example',
    'Q4 full email, ten blanks, full eleven-token bank including crossed-out greeting example',
    'Q5 all seven personal prompts, choosefive, full vocabulary and answer grids', 'explicit blank', 'explicit blank', 'blank back cover'])),
   'aural': dict(zip(map(str, range(1, 9)), ['cover: listening100, English answers',
    'A four conversations, eight separately priced prompts with full distractors',
    'B advice three MCQs and pool five prompts; phone prefilled06-81_-4___ has four missing digits',
    'C eight prompts: teacher, school secretary, directions, complete distractors',
    'D nine separately numbered interview prompts with complete distractors', 'explicit blank', 'explicit blank', 'blank back cover'])),
   'scheme': dict(zip(map(str, range(1, 13)), ['official cover', 'published-scheme general marking notice',
    'general listening romaji/Japanese-script half marks; A24/B26; phone1percorrectmissingnumber',
    'C26 including anyONE direction4; D firstfive13marks',
    'D lastfour11marks with restaurants1 partial; general reading inappropriate-language half marks; Q1A15/B20',
    'Q2A12: fourmatches2each plus ANYTWO of four details2each, guitar1; B15: truth2 plusquote1 each',
    'Q2C5 two unprinted points2each plusdisc1; Q3A23 with私のあね2 partial; firstfourkanji1each',
    'remaining sixkanji1each; presenttensefive2each; particlesfive2each labelledD whereas paperC2',
    'Q4 tenblanks3each, no word reuse, literal local spelling alternatives; Q5 anyfiveC5/E5, viC2+3, fullcontentbands',
    'Q5 ownEcap3 ifownC<4, full expressionbands and markingguidance', 'explicit blank', 'blank back cover'])),
  },
  'choiceBoundaries': [
   'Q1A five areas remain one15-mark pool; Q1B five building/floor pairs remain one20-mark task, each component2 and restaurants9/B1 one floor alternative. Given examples unpriced.',
   'Q2A1 four character matches is one8-mark pool. Q2A2 has four printed named blanks (Sarah/Tom merchandise and Susan/Harry places); the scheme explicitly awards anytwo2each, total4. One complete choice card, no duplicate bilingual questions. Guitar-only1 is local to Sarah, not an extra answer.',
   'Q2B five required decisions each2 plus evidence1 remain one15-mark pool with the example unpriced. Q2C has two unprinted culture points2each and discretionary1; no model answer invented.',
   'Q3 required four blood types stay one8-mark table. ThreeJapanese3each and threeMCQs2each remain independent. Alltenkanji, allfivepresent-tense and allfiveparticles remain whole required pools.',
   'Q4 alltenblanks3each, originalbank/example, no word reuse. Canonical source-local bank spellings先生 and二年生 bind literal schemeせんせい/２年生 for blankix; all original spellings visible, no global normalization.',
   'Q5 one50-mark card retains allseven prompts, choosefive, eachmanualC0-5/E0-5 with fullbands; vi prints C2+3 but no component partial mapping, so common whole-answer content scale retained. Each expression cap3 depends only on its own content<4.',
   'Listening33tasks A8/B8/C8/D9; totals24/26/26/24. Phone06-810-4545 fourmissingdigits0/5/4/5 each1; given06-81 and4 unpriced. C3ii ANYONE direction4, not Higher mixedtariff. D8 restaurantsonly1 versusfull3.',
   'General reading languagehalf applies all16reading tasks; namedJapanese/romaji listeninghalf applies all33listening tasks. No writing language penalty or extraneous-material rule.',
   'All9written and18aural originalAtlas anchors retained. Only physicalschemeband13to12 corrected; no alias or exclusion added.',
  ],
  'sourceDiscrepancies': [
   'Q2B(v) scheme prints あかとくる while original passage prints 赤と黒 with rubyくろ; literal scheme quotation retained with visible precise discrepancy, no silent correction.',
   'Paper Q3C2 particles are labelledD in scheme; retain original C2 identity and allfive answers.',
   'Q4ix scheme usesせんせい and２年生 while bank uses先生 and二年生; source-local bindings enforce the printed no-reuse instruction without normalizing other Japanese text.',
  ],
  'atlasSourceSpans': {'written1': [2, 3], 'written2': [4, 5], 'written3': [8, 9, 10, 11], 'written4': [12], 'written5': [13], 'written6': [6], 'written7': [10], 'written8': [10], 'written9': [11]},
 }

if __name__ == '__main__':
 data = build()
 (Path(__file__).parent / 'reviews/japanese-2013-ol-census.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
 print(f'{len(TASKS)} independently counted tasks; {data["checksums"]}')
