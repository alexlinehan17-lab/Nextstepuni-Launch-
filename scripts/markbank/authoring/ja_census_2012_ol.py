#!/usr/bin/env python3
"""Independent 2012 Ordinary census after the complete 32-page original sweep."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
 ('paper', 'examiner-reports/japanese/papers/2012-ol-000-paper.pdf', '321fb05912052148a0b71c99deb4a825dc00f0dc39b8005379e3229dbc4bc5e3'),
 ('aural', 'examiner-reports/japanese/papers/2012-ol-A00-paper.pdf', 'ae87cf36ebb7962067bfc06fca86abbb185ca34b683a443341d6d8e82db3e875'),
 ('scheme', 'examiner-reports/japanese/schemes/2012-ol.pdf', '28a98e6d51c20e2bb207594d9d2c1c03058b2637d09c0bfd9ac43f8cd4465eaf'),
]
TASKS = []

def task(section, q, marks, pp, sp, atlas, roman=None):
 component = 'aural' if section.startswith('L') else 'paper'
 TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component, 'paperPages': [pp], 'schemePages': sp,
  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})

def build():
 task('1', 1, 16, 3, [5], 1)
 for roman in ['i', 'ii']: task('1', 2, 2, 3, [5], 2, roman)
 for q, marks in [(3, 4), (4, 4), (5, 3)]: task('1', q, marks, 3, [5], q)
 for roman in ['i', 'ii']: task('1', 6, 2, 3, [5], 6, roman)
 task('2A', None, 9, 5, [6], 7)
 task('2B', None, 16, 5, [6], 8)
 for roman in ['i', 'ii']: task('3A', 1, 2, 7, [7], 9, roman)
 task('3A', 2, 4, 7, [7], 10)
 for roman, marks in [('i', 2), ('ii', 4), ('iii', 2)]: task('3A', 3, marks, 7, [7], 11, roman)
 task('3A', 4, 2, 7, [7], 12)
 for roman in ['i', 'ii']: task('3A', 5, 2, 7, [7], 13, roman)
 task('3A', 6, 2, 7, [7], 14)
 task('3B', None, 10, 8, [7], 17)
 for q in [1, 2]: task('3C', q, 10, 8, [8], 18)
 task('3D', None, 6, 9, [8], 19)
 task('4', None, 30, 10, [9], 15)
 task('5', None, 50, 11, [9, 10], 16)
 for q in range(1, 6):
  task('LA', q, 3, 2, [3], 1, 'i'); task('LA', q, 2, 2, [3], 1, 'ii')
 for q, count in [(1, 2), (2, 2), (3, 3)]:
  for roman in ['i', 'ii', 'iii'][:count]: task('LB', q, 3, 3, [3], 2, roman)
 for q, values in [(1, [3, 3, 3, 2]), (2, [3, 4, 6]), (3, [3, 3])]:
  for roman, marks in zip(['i', 'ii', 'iii', 'iv'], values): task('LC', q, marks, 4, [4], 3, roman)
 for q, values, sp in [(1, [3, 4, 4, 3], 4), (2, [3, 4, 3], 5)]:
  for roman, marks in zip(['i', 'ii', 'iii', 'iv'], values): task('LD', q, marks, 5, [sp], 4, roman)
 assert len(TASKS) == 59, len(TASKS)
 totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
  ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
  ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
 assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
 sources = []
 for component, path, digest in SOURCES:
  assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
  sources.append({'component': component, 'path': path, 'sha256': digest})
 return {'subjectId': 'japanese', 'year': 2012, 'level': 'ol', 'reviewedAt': '2026-11-10',
  'method': 'Independent visual review of all twelve written, eight aural and twelve scheme physical pages before authoring; each task boundary and quota compared against the original pricing. Printed numbered answer slots inside required finite pools remain one complete task.',
  'sources': sources, 'tasks': TASKS, 'checksums': totals,
  'candidateMaximum': {'written': 200, 'listening': 100, 'total': 300, 'writingChoice': 'All five written questions; Q4 complete ten blanks using the original bank, and Q5 any five of the seven printed questions.'},
  'pageRoles': {
   'paper': dict(zip(map(str, range(1, 13)), ['official cover: written200, all five questions',
    'Q1 complete illustrated menu, twenty-two numbered items, prices, flavours, cake-set definition, hours and closed day',
    'Q1 eight required prices; item18 and flavour; two sandwich types; two Katakana words plus Latte example; cake set; hours and closed day',
    'Q2 complete four pet-sitter profiles, names, portraits, contact number and ruby',
    'Q2A nine missing table cells with Tanaka/Ginza/Labrador already given; B eight truth/evidence pairs plus example',
    'Q3 complete Aoife interview with six questions, map, ruby and underlined grammar targets',
    'Q3A ten separate asks, including country pair, required two weekdays, four complete MCQ prompts/options',
    'Q3B ten kanji MCQs with example; C1 five negative transformations with original underlines/example; C2 five particle MCQs with example',
    'Q3D open English comparison of Japanese and Irish school systems, answer lines',
    'Q4 full self-introduction, ten blanks, complete bank including the crossed-out greeting example',
    'Q5 complete seven school prompts, any five, answer grids and all vocabulary; favourite-teacher prompt v present',
    'explicit blank back page'])),
   'aural': dict(zip(map(str, range(1, 9)), ['official cover: listening100',
    'A five requests, each independent four-option request3 and yes/no2, all distractors',
    'B seven independent questions with complete MCQ choices, directions pool, tickets, price and duration',
    'C nine tasks: film survey four prompts, pub/job/phone three, weather two; phone gives03,4 and final9 with six missing digits',
    'D two interviews with four and three tasks, complete distractors and three open responses',
    'explicit blank', 'explicit blank', 'explicit blank back page'])),
   'scheme': dict(zip(map(str, range(1, 13)), ['official cover', 'blank inside cover',
    'general listening Japanese/romaji/script half rule; A25: five3+2; B21: seven3, directions any detail',
    'C30: film11, jobs13, weather6; phone six missing digits1 each; D first interview14, people-only2 and Internet-only1 partials',
    'D second interview10, Tokyo-only1 partial; general reading inappropriate-language half rule; Q1 all35 including cake-set total3 with literal cake1/drink3, opening1+1',
    'Q2A all nine missing cells1 each, three given cells unpriced; Q2B eight truth1/evidence1 pairs, total16',
    'Q3A24: country pair2 each, weekdays2 each, full MCQ key; B allten kanji1 each',
    'Q3C1 allfive negative forms2 each, C2 allfive particles2 each; D two unprinted points2 each plusdiscretionary2',
    'Q4 ten blanks3 each; Q5 common anyfive C5/E5 with six listed prompts, favourite-teacher omission shifts finaltwo labels',
    'Q5 complete content bands1/2-3/4/5 and expression bands1/2-3/4-5, no lower-expression cap printed',
    'blank inside back cover', 'back cover'])),
  },
  'choiceBoundaries': [
   'Q1 eight required prices stay one16-mark task; sandwich pair and Katakana pair each one4-mark task. Item18, flavour, cake set, opening hours and closed day retain independent asks. Cake set stays one whole3-mark response with exact cake1/drink3 partial guidance and permitted0/1/3; no additive4 or inferred2.',
   'Q2A allnine missing cells stay one9-mark table; given Tanaka/Ginza/Labrador never score. Q2B all eight truth/evidence pairs stay one16-mark pool, decision1 and exact quotation1 each; example remains unpriced.',
   'Q3A has ten independent tasks; countries anytwo2 each, weekdays two required2 components. Paper roman i/ii and i/ii/iii identity wins over scheme a/b/c. Q3B allten kanji, C1 allfive negative forms and C2 allfive particles remain whole required pools. Q3D retains two manual distinct culture points2 each plus discretionary2 without inventing answers.',
   'Q4 allten blanks3 each; preserve original bank町 and schemeまち visibly. No explicit no-reuse direction appears, so no imported reuse penalty. All original underlines, examples, complete bank and source context retained.',
   'Q5 one50-mark task: allseven paper prompts, anyfive with common manual C0-5/E0-5 bands. Scheme omits the favourite-teacher prompt(v) and shifts after-school/school-liking labels; disclose that exact mismatch, do not drop a printed ask. Full scheme sweep finds no Ecap3 or other later-year conditional cap.',
   'Listening33 tasks: A10/B7/C9/D7, totals25/21/30/24. Phone03-8353-4969 has six missing8/3/5/3/9/6 digits1 each; given03,4 and final9 are unpriced. All original MCQ distractors preserved. Exact people-only2, Internet-only1 and Tokyo-only1 partials stay within their single response caps.',
   'General reading half applies all24 reading tasks. General named Japanese/romaji/script listening half applies all33 listening tasks. Both writing tasks have no added language rule; no extraneous condition is published.',
   'Preserve all nineteen written and four aural Atlas anchors and existing crops. Append only missing physical scheme p5 continuation to existing PartD for its second interview; correct scheme band13to12. No aliases or exclusions added.',
  ],
  'sourceDiscrepancies': [
   'Q1.5 total3 and Cake & Drink coexist with literal cake1/drink3 guidance. One response capped3 preserves the published awards without inventing2 for drink or adding components to4.',
   'Paper Q3A1 andA3 use roman subparts; scheme usesa/b/c. Preserve paper references.',
   'Q4(iii) bank prints町 and scheme printsまち; both spellings remain visible, no blanket normalization or unsourced no-reuse rule.',
   'Q5 scheme lists six prompts and omits paper(v) favourite teacher. Its after-school and school-liking prompts are labelled5/6 instead of paper(vi)/(vii). Retain all seven under the common published rubric.',
   'The original Q3 text is explicitly Aoife’s interview. Correct its six existing Atlas topic values9–14 from letters/blogs5-1 to canonical articles/interviews5-2; preserve their identities and source regions. Q2 remains the promotional flyer under everyday5-0.',
   'Original PartD Atlas region stops on scheme physical4 although Interview2 continues on5. Append original continuation without renumbering or altering existing regions.',
  ],
  'atlasSourceSpans': {**{f'written{i}': [3] for i in range(1, 7)}, 'written7': [5], 'written8': [5],
   **{f'written{i}': [7] for i in range(9, 15)}, 'written15': [10], 'written16': [11], 'written17': [8], 'written18': [8], 'written19': [9]},
 }

if __name__ == '__main__':
 data = build()
 (Path(__file__).parent / 'reviews/japanese-2012-ol-census.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
 print(f'{len(TASKS)} independently counted tasks; {data["checksums"]}')
