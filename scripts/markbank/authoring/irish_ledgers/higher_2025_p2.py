#!/usr/bin/env python3
"""Rebuild irish-higher-2025-p2-source-review.json from the official paper (see _ledger.py).

Generated from the review-time maker; AMENDMENTS and RECORDED carry the later, dated edits.
Run with --check to verify the committed ledger is byte-identical. Run from any directory.
"""
import os
import sys
from pathlib import Path
_REPO = Path(__file__).resolve().parents[4]
os.chdir(_REPO)
sys.path.insert(0, str(_REPO / 'scripts/markbank/authoring'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ledger import finish  # noqa: E402
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
import fitz
from irish_higher_2025_p2 import DIRECTIVE, clean, PAPER_SHA, SCHEME_SHA
paper=fitz.open('paper-trail-corpus/exampapers/2025/LC001ALP200IV.pdf')
lines=list(dict.fromkeys((i,clean(l)) for i,p in enumerate(paper,1) for l in p.get_text().splitlines() if DIRECTIVE.search(clean(l))))
Q2='Closed choice: Q2A (Prós Ainmnithe) or Q2B (Prós Roghnach), then (a) or (b): four whole 30-mark routes (Hurlamaboc, Oisín i dTír na nÓg, optional novel extract, optional folktale).'
Q3='Closed choice: Q3A or Q3B, then (a) or (b): four whole 30-mark routes, each answering (i), (ii) and (iii).'
Q4='Closed choose-one of 4A–4F: six whole 40-mark routes.'
BOTH='Both reading passages and every question in each are required; each printed part is also a practice card.'
SRC='Source-text wording inside a reading passage or poem, not a candidate instruction.'
TWO='Two required answers inside one printed part. Where the scheme prices them 1 mharc + 1 mharc, each answer is also a one-mark practice slot; where it prices 2 mharc + 1 mharc (order-dependent) the part stays whole at 0/2/3.'
ONE='One required answer; the accepted list is the key for one task.'
dec={
 'go bhfuil an dá albam bheo dá chuid, Live in':SRC,
 'mbliana is dhá scór. Tríocha bliain i ndiaidh':SRC,
 'an dá chluiche sin agus mar sin, tá sé beartaithe':SRC,
 '(b) (i) Tabhair dhá shampla a léiríonn go bhfuil an bhearna rannpháirtíochta idir na hinscní':TWO,
 '(b) (i) Tabhair dhá shampla de ghníomhaíochtaí coirp a dhéanann daoine mar chaitheamh':TWO,
 'Freagair gach ceist (Ceist 1, Ceist 2, Ceist 3 agus Ceist 4).':'Required answers; no finite task menu.',
 'Freagair Léamhthuiscint A (50 marc) agus Léamhthuiscint B (50 marc).':BOTH,
 'Tá Ceist 1 ‐ 5 ar aon mharc. Glacfar le freagraí i d’fhocail féin nó':'Equal 7-mark questions 1–5; answer-language rule, not a selection.',
 'Freagair Ceist 2A (30 marc) nó Ceist 2B (30 marc).':Q2,
 'Freagair ceist amháin as do rogha de 2A (a) nó 2A (b).':Q2,
 '2B. Prós Roghnach':Q2,
 'Freagair ceist amháin as do rogha de 2B (a) nó 2B (b).':Q2,
 'Freagair Ceist 3A (30 marc) nó Ceist 3B (30 marc).':Q3,
 'Freagair ceist amháin as do rogha de 3A (a) nó 3A (b).':Q3,
 '3B. Filíocht Roghnach':Q3,
 'Freagair ceist amháin as do rogha de 3B (a) nó 3B (b).':Q3,
 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F).':Q4,
 'Freagair Léamhthuiscint A agus Léamhthuiscint B anseo.':BOTH,
 'Léigh an sliocht seo a leanas agus freagair na ceisteanna ar fad a ghabhann leis.':BOTH,
 'ag éisteacht le ceol ar an rogha leathan stáisiúin':SRC,
 '1. (a) Tabhair dhá chúis ar mhúscail díolachán uirlisí ceoil Rory Gallagher spéis mhór i measc lucht':TWO,
 '2. (a) Scríobh síos dhá rud a léiríonn go raibh féith an cheoil i dtuismitheoirí Rory. (Alt 2)':TWO,
 '4. (a) Luaigh dhá bhealach a dtéadh Rory Gallagher i gcion go mór ar a lucht féachana ag a chuid':TWO,
 '5. (a) Scríobh síos dhá dhúshlán a chruthaigh tionscal an cheoil do Rory Gallagher mar ealaíontóir.':TWO,
 '(b) (i) Scríobh síos dhá chomhartha ómóis do Rory Gallagher atá in Éirinn. (Alt 5)':TWO,
 '(b) ‘Ceoltóir as an ngnáth ba ea Rory Gallagher.’ Tabhair dhá phointe eolais, i d’fhocail féin,':'Two independent six-mark points (P1, P2): practice slots plus the whole part.',
 'rannpháirteach ar bhonn ócáideach nó eagraithe.':SRC,
 'choirp go rialta. Tá rogha leathan deiseanna':SRC,
 'd’ionad aclaíochta nó glacann siad páirt i ranganna':SRC,
 'beag beann ar aois, ar inscne, ar chumas nó':SRC,
 '2. (a) Luaigh dhá bhuntáiste a bhaineann leis an spórt. (Alt 2)':TWO,
 '(b) (i) Luaigh dhá rud a sholáthraítear ar an gCampas Náisiúnta Spórt do na lúthchleasaithe':TWO,
 '(ii) Scríobh síos dhá rud atá ag teastáil chun córas spóirt éifeachtach a fhorbairt ar mhaithe':TWO,
 '(b) ‘Tá dul chun cinn maith á dhéanamh i gcúrsaí spóirt in Éirinn.’ Tabhair dhá phointe eolais,':'Two independent six-mark points (P1, P2): practice slots plus the whole part.',
 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach).':Q2,
 'Freagair do rogha ceann amháin de (a) nó (b) thíos.':Q2+' Printed for 2A, 2B and 3B (pages 8 and 11).',
 'Freagair an cheist thíos ar an ngiota as an úrscéal Hurlamaboc.':Q2,
 'nó':'Separates printed alternatives (2A(a)/(b), 2B(a)/(b), 3A(a)/(b), 3B(a)/(b)); each is a whole route, never combined.',
 'Freagair an cheist thíos ar an scéal béaloidis Oisín i dTír na nÓg.':Q2,
 'Prós Roghnach':Q2,
 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.':'Restriction on content, not a route.',
 'Maidir leis an ngiota as an úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa,':'Optional novel extract chosen by the candidate: open content inside one route.',
 'Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas':'Optional folktale chosen by the candidate: open content inside one route.',
 'PRÓS AINMNITHE nó PRÓS ROGHNACH 30 marc':'Section heading / structure statement, not a separate route.',
 'Freagair Ceist 3A (Filíocht Ainmnithe) nó Ceist 3B (Filíocht Roghnach).':Q3,
 'Freagair do rogha ceann amháin de (a) nó (b).':Q3,
 'fhileata sin sa dán, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.)':'Required content within the selected poem route; “pointe amháin” is the minimum support, not a selection.',
 '(iii) Cén mheadaracht atá sa dán seo? Scríobh pointe amháin eolais faoin meadaracht seo':'Required content within the selected poem route; “pointe amháin” is the minimum support, not a selection.',
 'FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH 30 marc':'Section heading / structure statement, not a separate route.',
 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.':'Restriction on content, not a route.',
 '(i) Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú':'Optional poem chosen by the candidate: open content inside one route.',
 '(Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.)':'Required content within the selected poem route; “pointe amháin” is the minimum support, not a selection.',
 'Tabhair dhá phointe eolais as an dán faoin teicníc sin.':'Required content within the selected poem route (two points, 3 + 3); not a selection.',
 '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos':'Optional poem chosen by the candidate: open content inside one route.',
 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.':Q4,
 'Freagair (i), (ii) agus (iii) thíos.':'4F: all three parts required in one route.',
 'Nóta: Bain úsáid as Leagan 1 nó Leagan 2 (lgh 13‐14 thall) den dán i do fhreagraí.':'4F prints two versions of the same poem; the candidate may use either inside one route. Not a separate task.',
 'Is leor dhá phointe eolais as an dán faoin sampla sin.':'4F(ii): one example plus two points inside one 9-mark part (1 + 4 + 4).',
 '(iii) Scríobh síos tréith amháin de chuid Airt. Tabhair dhá phointe eolais as an dán faoin tréith sin.':'4F(iii): one trait plus two points inside one 9-mark part (1 + 4 + 4).',
 'Nó thairis dá dtaitneadh liom.':SRC,
 'Is ní bheidh sé acu le freagairt.':SRC,
}
out=[]
for p,r in lines:
    d=dec.get(r) or ('Copyright statement, not a task.' if p==16 else None)
    assert d,(p,r); out.append(dict(page=p,raw=r,decision=d))
ledger=dict(year=2025, level='higher', paperFileid='LC001ALP200IV.pdf', schemeFileid='LC001ALP000IV.pdf', paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
 reviewDate='2026-10-11', status='reviewed', reviewedPaperPages=list(range(1,17)), reviewedSchemePages=list(range(18,49)),
 schemeScope='Combined Paper 1 and Paper 2 scheme. PDF 18 reading notes and annotation key; 19–21 Léamhthuiscint A; 22–25 Léamhthuiscint B; 26 literature annotation key; 27 literature notes, Gaeilge 5 and prose 25/18 tables; 28–30 prose; 31–38 poetry; 39 Ceist 4 notes and 35/25 table; 40–47 additional literature; 48 modified marking (SMM). PDF 1–17 belong to Paper 1; 49–52 blank.',
 reviewMethod='Visual inspection of every paper page (pages 1–3 cover/instructions, 15 blank, 16 acknowledgements) and every applicable scheme page; cross-checked extracted text.',
 selectionDecisions=out,
 nonPoolDecisions=['Reading: all twelve questions are required; each printed part is a practice card at its published tariff. “1 mharc + 1 mharc” answers expose one-mark slots (A5(b)(i), B2(b)(i), B4(b)(i), B5(b)(i), B5(b)(ii)); “2 mharc + 1 mharc” items (A1(a), A2(a), A4(a), A5(a), B2(a) and both 6(a)) stay whole as 0/2/3.',
  'Both 6(b) parts have two independent six-mark points (P1, P2) with practice slots; the answer must be in the candidate’s own words.',
  'Single-answer parts allow only the mark values the scheme prints for them (0, the printed partials and the full tariff).',
  'Prose, poetry and Q4 choices are closed printed routes (4 + 4 + 6) and were already carded (IDs retained); the optional novel, folktale or poem itself is open content chosen by the candidate.',
  'Scheme lists of accepted points and supporting notes are indicative answer keys, not route pools.',
  'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.'],
 sourceFindings=['Paper 2 = 200: Léamhthuiscint A 50 + B 50 (Q1–5 at 7 = (a) 3 + (b)(i) 2 + (b)(ii) 2; Q6 at 15 = (a) 3 + (b) 12), Prós 30, Filíocht 30, Litríocht Bhreise 40.',
  'Reading A “Rory Gallagher – Laoch ceoil” (paper 4–5, scheme PDF 19–21); B “Cúrsaí spóirt in Éirinn” (paper 6–7, scheme PDF 22–25).',
  'Literature language: 5 marks for Gaeilge in every literature answer (scheme PDF 27); prose 25 Eolas (18 when only one required aspect is discussed); poetry (i) 13, (ii) 5, (iii) 7; Q4 Eolas 35 (25 for one aspect); 4F (i) 17, (ii) 9, (iii) 9.',
  'Legacy corrections (IDs, totals and topics unchanged): the twelve whole reading questions each had one undivided criterion and one (Ceist 3 A) had lost its (a) key; the poetry routes had one 25-mark Eolas criterion with the (i) scheme missing; every literature route carried a paraphrased Gaeilge band (“sásúil”) instead of the printed table. All now carry the lifted 2025 scheme text and part tariffs.'],
 remainingWork=[])
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = [('Legacy corrections (IDs, totals and topics unchanged): the twelve whole reading questions each had one undivided criterion and one (Ceist 3 A) had lost its '
  '(a) key; the poetry routes had one 25-mark Eolas criterion with the (i) scheme missing; every literature route carried a paraphrased Gaeilge band '
  '(“sásúil”) instead of the printed table. All now carry the lifted 2025 scheme text and part tariffs.',
  'Legacy corrections (IDs, totals and topics unchanged): the twelve whole reading questions each had one undivided criterion and Léamhthuiscint A Ceist 3 had '
  'lost its (a) key while carrying the Ceist 4–5 keys; the poetry routes had one 25-mark Eolas criterion with the (i) scheme missing; every literature route '
  'carried a paraphrased Gaeilge band (“sásúil”) instead of the printed table. All now carry the lifted 2025 scheme text and part tariffs.')]
RECORDED = {'runtimeVerification': {'date': '2026-10-12',
                         'viewport': [390, 844],
                         'markBankRoutes': 5,
                         'atlasRoutes': 5,
                         'sourceReader': 'A retained whole reading question, a 6(b) point slot, a one-mark answer slot, a prescribed poem and 4F rendered '
                                         'their paper pages (passage pages 4–5/6–7, poem pages 13–14); navigation, close/focus return and overflow checks '
                                         'passed.',
                         'atlas': 'Each route rendered its paper pages plus reviewed scheme pages (frozen reading Ceist 3 2+2, slot 2+1, 3A(a) 1+3, 4F 3+3, '
                                  '2B(a) 1+2).',
                         'browserErrors': []}}
KEY_ORDER = ['year',
 'level',
 'paperFileid',
 'schemeFileid',
 'paperSha256',
 'schemeSha256',
 'reviewDate',
 'status',
 'reviewedPaperPages',
 'reviewedSchemePages',
 'schemeScope',
 'reviewMethod',
 'selectionDecisions',
 'nonPoolDecisions',
 'sourceFindings',
 'remainingWork',
 'runtimeVerification']

if __name__ == '__main__':
    finish(LEDGER, 'irish-higher-2025-p2-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
