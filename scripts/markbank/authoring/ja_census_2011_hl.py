#!/usr/bin/env python3
"""Independent 2011 Higher task census, from original-page review."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
 ('paper', 'examiner-reports/japanese/papers/2011-hl-000-paper.pdf', 'fea3c8874340bd32e29af2fa5a3ea6900c82d4245be0df89fed00441957877cb'),
 ('aural', 'examiner-reports/japanese/papers/2011-hl-A00-paper.pdf', '791f4689903af58657a32cdef4020201a3c012bc3725f3a20bd3a4996350373d'),
 ('scheme', 'examiner-reports/japanese/schemes/2011-hl.pdf', 'b074b5846c2f41ce7a4476795922fd4570334c44536924c8484a4aed02238f81'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
 component = 'aural' if section.startswith('L') else 'paper'
 TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
  'paperPages': pp if isinstance(pp, list) else [pp], 'schemePages': sp,
  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
 task('1A', None, 8, 3, [7], 1)
 for q in range(1, 7): task('1B', q, 2, 3, [7], 2)
 for q in range(1, 4): task('1C', q, 2, 4, [8], 3)
 for q in [1, 2]: task('1D', q, 4, 4, [8], 4)
 task('2A', 1, 5, 7, [9], 5)
 for roman, marks in [('i', 2), ('ii', 2), ('iii', 4)]: task('2A', 2, marks, 7, [9], 5, roman)
 task('2A', 3, 8, 7, [9], 5)
 for q in range(1, 4): task('2B', q, 2, 7, [10], 6)
 task('2C', None, 10, 8, [10], 7)
 task('3A', 1, 2, 10, [11], 8)
 task('3A', 2, 12, 10, [11], 8)
 for q in range(1, 5): task('3B', q, 2, 10, [11] if q == 1 else [11, 12], 9)
 task('3C', None, 12, 11, [12], 10)
 task('3D', None, 10, 11, [12], 11)
 task('3E', None, 5, 11, [12], 12)
 task('4', None, 40, 12, [13, 14], 13)
 task('5', None, 60, [15, 16], [15, 16], 14)
 task('LA', None, 21, 2, [3], 1)
 for q, values in [(1, [2, 4, 2]), (2, [2, 2, 2, 2])]:
  for roman, marks in zip(['i', 'ii', 'iii', 'iv'], values): task('LB', q, marks, 3, [4], 2, roman)
 task('LB', 3, 3, 3, [4], 2)
 for q, values in [(1, [1, 2, 2, 2, 3]), (2, [2, 4, 2])]:
  for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v'], values): task('LC', q, marks, 4, [5], 3, roman)
 task('LC', 3, 4, 4, [5], 3)
 for q, values in [(1, [2, 4, 2]), (2, [2, 4, 4])]:
  for roman, marks in zip(['i', 'ii', 'iii'], values): task('LD', q, marks, 5, [6], 4, roman)
 assert len(TASKS) == 56, len(TASKS)
 totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
  ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
  ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
 assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
 sources = []
 for component, path, digest in SOURCES:
  assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
  sources.append({'component': component, 'path': path, 'sha256': digest})
 return {'subjectId': 'japanese', 'year': 2011, 'level': 'hl', 'reviewedAt': '2026-11-11',
  'method': 'Independent complete visual review of the original written, aural and scheme pages before authoring. Every task boundary is compared with its published allocation; required tables and finite pools remain complete.',
  'sources': sources, 'tasks': TASKS, 'checksums': totals,
  'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300,
   'writingChoice': 'Q4 choose great-day or terrible-day diary; Q5 choose scholarship essay or speech-contest entry, with all three headings of the chosen option.'},
  'pageRoles': {
   'paper': dict(zip(map(str, range(1, 21)), ['official cover: written220, all five questions',
    'Q1 complete Music Life contents page, both columns, page numbers, full vocabulary',
    'Q1A eight required page matches; B six English asks with exact two-detail quotas',
    'Q1C three Japanese asks; D four kanji readings and four meanings with given examples', 'explicit blank',
    'Q2 complete Niamh/Mike fortune slips, all four fortune sections, numbers/colours and vocabulary',
    'Q2A complete lucky-number/colour and advice tables, three intervening prompts; B three Japanese questions',
    'Q2C ten required nonpast plain-form transformations, full sentences and example',
    'Q3 complete Nakamura email about iPhone study apps, illustrations and full vocabulary',
    'Q3A two-reason pool and full six-app advice table; B four Japanese questions',
    'Q3C six required reading/meaning pairs; D ten required particles; E technology/company culture question',
    'Q4 both complete alternative diary prompts, approximately200 characters',
    'Q4 answer grid', 'Q4 continued answer grid',
    'Q5 instruction and complete scholarship-essay option/flyer, approximately320 characters',
    'Q5 complete speech-contest option/flyer, same task', 'Q5 answer grid', 'continued answer grid', 'continued answer grid', 'explicit blank back page'])),
   'aural': dict(zip(map(str, range(1, 9)), ['official cover: listening80',
    'A four-caller voicemail table:12 missing cells, four given cells unpriced',
    'B eight prompts: MrDonuts location/directions/transport, food/orders/cost, three appearance details',
    'C five garden asks, three recruitment asks including whole phone, one weather pool',
    'D conversation about part-time jobs: three Tomomi and three Kenichi asks', 'explicit blank', 'explicit blank', 'explicit blank back page'])),
   'scheme': dict(zip(map(str, range(1, 21)), ['official scheme cover', 'blank inside cover',
    'A21 full12-cell allocation, given cells, four1-mark partials, this-evening0, local Japanese/romaji/script half condition',
    'B19 complete pools, Mori1+department-store1, left-only1 partial, all printed quotas',
    'C22 gardens/full-partial pool, recruitment anytwo and pool-level manga1, whole phone2, weather anytwo with fine/rain1 partials',
    'D18 complete job/like/dislike pools, gym1/university1/friends1 partials, last task misnumbered(iv)',
    'Q1A8 required page matches; B12 six2-mark answers and local Japanese half rule',
    'Q1C6 three2-mark Japanese answers, English and combined quotation/extraneous half; D8 all readings/meanings',
    'Q2A21 complete tables and scenarios, precise partial components, local Japanese half rule',
    'Q2B6 exact answers, generic language half and combined quotation/extraneous half; C10 full verb pool',
    'Q3A14 full reason pool and six-app table, all per-detail tariffs/interesting1; B1 with local combined/language half rules',
    'Q3B remaining answers; C12 six paired tasks; D10 particles; E5 two points2each plusdiscretionary1, no model answer',
    'Q4 alternatives share three headings5each plusdiscretionary5 andexpression20',
    'Q4 full normal/lower expression bands; lower15 ifcontent<=10 orfewer150characters',
    'Q5 alternatives share required headings5/10/10 plusdiscretionary5 andexpression30',
    'Q5 full normal/lower expression bands; lower20 ifcontent<=15 orfewer200characters',
    'blank with printed15 footer', 'blank with printed16 footer', 'blank inside back cover', 'pink blank back cover'])),
  },
  'choiceBoundaries': [
   'Q1 eight page matches and both four-item kanji pools remain whole. Six English and three Japanese comprehension asks retain their independent2-mark allocations; named finite choices use the complete printed pool and quota.',
   'Q2 both required two-person tables stay whole. A2(iii) retains both required conditional scenarios in one4-mark task, with the four printed1-mark components. B three questions remain separate; C allten verb transformations form one required pool.',
   'Q3A2 allsix apps stay one12-mark table with full accepted alternatives and individual component tariffs. C six reading/meaning pairs and D ten particles remain whole. Culture has two manual2-mark response slots and one discretionary mark, with no invented model answer.',
   'Q4 one40-mark task choosing great-day OR terrible-day diary; allthree headings5each plusdiscretionary5 andE20. Q5 one60-mark task choosing one complete flyer; allthree headings5/10/10 plusdiscretionary5 andE30. Exact lowerE thresholds are inclusive content10/15 orfewer150/200characters.',
   'Listening A one21-mark table with12missingcells; B eighttasks19; C ninetasks22; D sixtasks18. Whole phone2444-1701 earns2 with no invented per-digit tariff. Finite pools retain all printed options and quotas.',
   'C2(ii) keeps the whole literal company-answer pool and pool-level manga1 partial in two manually assessed response slots: first0/1/2, second0/2. Place the sole manga-only partial in the first slot regardless of answer order. No unsupported unique association or independent extra partial concept; distinct responses count once, and manga-only cannot also score alongside an overlapping full detail. Weather and Kenichi-dislike partials stay within their matching full concepts.',
   'Language half is local: listening A only; reading Q1B Japanese, Q1C English, Q2A Japanese, Q2B/Q3B language-not-specified. Combined quotation-without-required-manipulation/extraneous half applies only to Q1C/Q2B/Q3B. Overlapping conditions apply once. No global reading/listening penalty is inferred.',
   'Preserve all11 original written and4 aural Atlas IDs/regions. Append missing Q3E/Q4/Q5 groups12–14; bind previously untagged A/B/D to Conversation and C to Radio/News. Correct physical schemeband21to20. No original shipped identities or aliases for this sitting are added or removed.',
  ],
  'sourceDiscrepancies': [
   'Scheme physical10 Q2B2 literally prints はじめまた; retain it with a visible source-typo note, without silently correcting the answer.',
   'Scheme physical11 names the weather app ウェザー・ニュース・リポート while paper physical10 names ウェザー・ニュース・タッチ; retain both with a visible note.',
   'Scheme physical5 repeats(iii) for the garden duration answer; paper identifies it as C1(ii), which is retained.',
   'Scheme physical6 labels the last listening answer(iv); paper physical5 correctly identifies Q2(iii), which is retained.',
   'Writing guidance retains stale numbering(1–6) for Q4 and(i)a–f/(ii)a–d for Q5; neither overrides the three actual required headings of each printed option.',
  ],
  'atlasSourceSpans': {'written1': [3], 'written2': [3], 'written3': [4], 'written4': [4],
   'written5': [7], 'written6': [7], 'written7': [8], 'written8': [10], 'written9': [10],
   'written10': [11], 'written11': [11], 'written12': [11], 'written13': [12, 13, 14], 'written14': [15, 16, 17, 18, 19]},
 }


if __name__ == '__main__':
 data = build()
 assert set(data['pageRoles']['scheme']) == set(map(str, range(1, 21))), 'Finish the independent scheme-page sweep before census publication'
 (Path(__file__).parent / 'reviews/japanese-2011-hl-census.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
 print(f'{len(TASKS)} independently counted tasks; {data["checksums"]}')
