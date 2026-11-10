#!/usr/bin/env python3
"""Independent 2012 Higher census after all 48 original pages were swept."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
 ('paper', 'examiner-reports/japanese/papers/2012-hl-000-paper.pdf', '7fd8f6abeb2e7a8ca2b953fd94a0570d3449f40ad58cbd8d478a24b3b9963130'),
 ('aural', 'examiner-reports/japanese/papers/2012-hl-A00-paper.pdf', '2e741b464b4af7f55b555a54db4000c1f784c3a727e38865f7390a6bae81958f'),
 ('scheme', 'examiner-reports/japanese/schemes/2012-hl.pdf', 'f976e52a9df6dfb58cd5887e5d003fe5fe2307907d71d0cf515f083fd184e6d5'),
]
TASKS = []

def task(section, q, marks, pp, sp, atlas, roman=None, letter=None):
 component = 'aural' if section.startswith('L') else 'paper'
 item = {'key': [section, q, letter, roman], 'marks': marks, 'component': component, 'paperPages': [pp], 'schemePages': sp,
  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}}
 if roman and letter: item['paperRef'] = f'2012 HL Section {section} Q{q}({roman})({letter})'
 TASKS.append(item)

def build():
 task('1A', None, 8, 3, [7], 1)
 task('1B', 1, 9, 3, [7], 2)
 task('1B', 2, 2, 3, [7], 3)
 for roman, marks in [('i', 1), ('ii', 2)]: task('1B', 3, marks, 3, [7], 4, roman)
 task('1B', 4, 4, 4, [7], 5, 'i')
 task('1B', 4, 2, 4, [8], 5, 'ii')
 for q in [5, 6]: task('1B', q, 2, 4, [8], q + 1)
 for q, marks in enumerate([3, 2, 2, 2, 2, 3], 1): task('2A', q, marks, 7, [9], q + 7)
 task('2B', 1, 2, 7, [9], 14)
 task('2B', 2, 2, 7, [9], 15)
 task('2B', 3, 2, 7, [9, 10], 15)
 task('2C', None, 4, 8, [10], 16)
 for q in [1, 2]: task('2D', q, 5, 8, [10], 17)
 task('2E', 1, 10, 8, [10], 18)
 task('2E', 2, 10, 9, [10], 18)
 for letter in ['a', 'b', 'c']: task('3A', 1, 2, 11, [11], 19, letter=letter)
 task('3A', 2, 4, 11, [11], 19)
 for q in range(1, 6): task('3B', q, 4 if q == 5 else 2, 11, [11], 20)
 task('3C', None, 12, 11, [11], 21)
 task('4', None, 40, 12, [12, 13], 22)
 task('5', None, 60, 15, [14, 15], 23)
 task('LA', None, 19, 2, [3], 1)
 for q, values in [(1, [2, 4]), (2, [2, 2, 2]), (3, [2, 2, 2])]:
  for roman, marks in zip(['i', 'ii', 'iii'], values): task('LB', q, marks, 3, [4], 2, roman)
 for letter in ['a', 'b']: task('LC', 1, 4, 4, [5], 3, 'i', letter)
 task('LC', 1, 1, 4, [5], 3, 'ii')
 for roman, marks in [('i', 2), ('ii', 4), ('iii', 3)]: task('LC', 2, marks, 4, [5], 3, roman)
 for roman, marks in [('i', 3), ('ii', 2)]: task('LC', 3, marks, 4, [5], 3, roman)
 for q, values in [(1, [1, 2, 4, 2, 2]), (2, [1, 2, 2, 2, 2])]:
  for roman, marks in zip(['i', 'ii', 'iii', 'iv', 'v'], values): task('LD', q, marks, 5, [6], 4, roman)
 assert len(TASKS) == 62, len(TASKS)
 totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
  ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
  ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
 assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
 sources = []
 for component, path, digest in SOURCES:
  assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
  sources.append({'component': component, 'path': path, 'sha256': digest})
 return {'subjectId': 'japanese', 'year': 2012, 'level': 'hl', 'reviewedAt': '2026-11-10',
  'method': 'Independent complete visual review of all twenty written, eight aural and twenty scheme physical pages, with each task boundary and allocation compared to the original scheme before authoring. Required pools remain whole and separately priced comprehension responses retain their printed identities.',
  'sources': sources, 'tasks': TASKS, 'checksums': totals,
  'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300, 'writingChoice': 'Q4 choose best-day or worst-day diary; Q5 choose introduction of Ireland or report on Japan, then any four of that option’s six headings.'},
  'pageRoles': {
   'paper': dict(zip(map(str, range(1, 21)), ['cover: written220, all five questions',
    'Q1 full i-doggy webpage with eight links, three dog photographs/profiles, names, colours, parentage and prices',
    'Q1A eight required links and given homepage example; B complete nine-cell dog table, abilities, poodle location/reason',
    'Q1B four-cell parentage table, two mongrel activities, one-day price and Japanese dog synonym', 'explicit blank with source footer typo',
    'Q2 full Tom interview with photo, highlighted questions, underlines, ruby and vocabulary',
    'Q2A six English tasks with explicit quotas; Q2B three Japanese prompts',
    'Q2C translation; D five meanings and five hiragana stems with examples; E1 ten particle blanks within eight sentences',
    'Q2E2 ten required plain-form transformations with original underlines and worked example',
    'Q3 complete Nadeshiko Japan article, illustrations and full vocabulary',
    'Q3A four English asks; B four Japanese asks and two-expression pool; C six required reading/meaning pairs with example',
    'Q4 two complete alternative diary prompts, one40-mark task, approximately200characters',
    'Q4 answer grid', 'Q4 continued answer grid',
    'Q5 two complete scenarios and six headings each, chooseone then anyfour, approximately320characters',
    'Q5 answer grid', 'continued answer grid', 'continued answer grid', 'explicit blank', 'blank back cover'])),
   'aural': dict(zip(map(str, range(1, 9)), ['cover: listening80',
    'A five-request table with14 missing cells, fifth request given',
    'B eight separate prompts: directions, doctor, tickets',
    'C film survey boys/girls separately priced, film name, pub/jobs/phone, two forecasts; phone03 given andeight missingdigits',
    'D two interviews with five independent prompts each', 'explicit blank', 'explicit blank', 'blank back cover'])),
   'scheme': dict(zip(map(str, range(1, 21)), ['official cover', 'blank inside cover',
    'A19, local Japanese/romaji/script half rule, complete14-cell tariff, exact partials and zero Japanese-test response',
    'B18, local Japanese/romaji/script half rule, anytwo directions2each with elevator1 partial, anytwo advice1each, station spelling1',
    'C23 complete survey pools, pub1 partial, jobsanytwo2each, wholephone3, three explicit weather components1each',
    'D20 complete interview answers, partial people1/Onsen1, alternative negative routes, work/Tokyo and study/Japanese1+1, zero Friends/Tokyo',
    'reading120, Q1A8/B24; all8links, nine dog cells, abilitiesanytwo1each, poodleplace/reasons, parentagefour1marks',
    'Q1 remaining6marks: play1/sleep1, price2, synonym2',
    'Q2A14 exact finite pools/zero answers/partials, B1/B2 and B3 prompt',
    'Q2B3 two1-mark components, C translationfour1, D tenkanji1each, E tenparticles1 andtenplainforms1',
    'Q3 all34marks: English10 with Frankfurt2/Germany1, JapaneseB12 with locally scoped Englishhalf and quotation/extraneous half, C six reading/meaning pairs1+1',
    'Q4 two prompts share aggregate content15 plusdiscretionary5 andexpression20',
    'Q4 complete normal/lower expressionbands; lowerE15 ifcontent<=10 orcharacters<150',
    'Q5 two scenarios share fourselectedheadings6each plusglobaldiscretionary6, expression30',
    'Q5 complete normal/lower expressionbands; lowerE20 ifcontent<=15 orcharacters<200',
    'blank printed14', 'blank printed15', 'blank printed16', 'blank inside backcover', 'backcover'])),
  },
  'choiceBoundaries': [
   'Q1 eight links, nine dog-profile cells and four parentage cells stay complete required pools. Examples and given breed labels do not score. Abilities anytwo1each; poodle location1 and reason two explicit1 components stay separate tasks.',
   'Q2A six separately asked tasks retain their quotas and exact printed partial/zero rules. B three Japanese questions stay separate; B3 has two published1-mark components. C translation stays one4-mark response with four priced components. Both five-item kanji pools and both ten-answer grammar pools stay whole; every underlined source fragment/example retained.',
   'Q3A1 a/b/c are three separately prompted2-mark answers; nickname is anytwo2each. B1–4 each2, B5 two required expressions2each is one4-mark pool. C allsix reading/meaning pairs1+1 stay one12-mark pool.',
   'Q4 one40-mark choice task: aggregate content15, discretionary5 andexpression20; no invented per-prompt split or discretionary descriptors. Exact lowerE threshold is content<=10 orfewer150characters, not later-year strict<10.',
   'Q5 one60-mark task, chooseone scenario andfour ofsix headings, four6-mark response slots plusglobaldiscretionary6 andexpression30. Do not import later-year per-heading discretionary1 orintro/cohesion awards. LowerE20 ifcontent<=15 orfewer200characters.',
   'Listening A one complete19-mark table with14missingcells, exact partials andgiven fifthrequest unpriced. B eighttasks18marks; C eighttasks23marks; D tentasks20marks. Whole phone03-8353-4969 earns3, with no invented per-digit allocation.',
   'Listening languagehalf is explicitly printed only on A/B headings; no general C/D rule found in full20-page scheme. Reading Englishhalf and quotation-without-required-manipulation/extraneous half are local to fiveQ3B tasks only. Source-bound conditions apply once, no invented quartercredit; other reading and allwriting retain no added language penalty.',
   'Preserve all23written and4aural originalAtlas anchors and their crops. Correct only physicalschemeband21to20; no originalIDs oraliases exist for this older sitting andnone are added.',
  ],
  'sourceDiscrepancies': ['The explicit blank writtenphysicalpage5 footer says Page5of2; physical source identity remains5 ofthe20-page original.',
   'Listening C1(i)(a)/(b) retains the paper’s roman-then-letter reference while the canonical key retains letter/roman order.'],
  'atlasSourceSpans': {**{f'written{i}': [3] for i in range(1, 5)}, **{f'written{i}': [4] for i in range(5, 8)},
    **{f'written{i}': [7] for i in range(8, 16)}, 'written16': [8], 'written17': [8], 'written18': [8, 9],
    'written19': [11], 'written20': [11], 'written21': [11], 'written22': [12, 13, 14], 'written23': [15, 16, 17, 18]},
 }

if __name__ == '__main__':
 data = build()
 (Path(__file__).parent / 'reviews/japanese-2012-hl-census.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
 print(f'{len(TASKS)} independently counted tasks; {data["checksums"]}')
