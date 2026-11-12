#!/usr/bin/env python3
"""Rebuild irish-higher-2026-p2-source-review.json from the official paper (see _ledger.py).

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
import json,re,hashlib,sys
from pathlib import Path
import fitz
ROOT=Path(str(_REPO))
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from irish_higher_2026_p2 import DIRECTIVE,clean
REQ='Required answers; no finite task menu.'
READ='Both reading passages and every question in each are required; each printed part is also a practice card.'
TEXT='Source-text wording inside a reading passage or poem, not a candidate instruction.'
Q2='Closed choice: Q2A or Q2B, then (a) or (b); 2A(a) itself offers Cáca Milis or An Lasair Choille and 2B(a) a film or a play. Six whole 30-mark routes.'
Q3='Closed choice: Q3A or Q3B, then (a) or (b). Four whole 30-mark routes, each answering (i), (ii) and (iii).'
Q4='Closed choose-one of 4A–4F: six whole 40-mark routes.'
TWO='Two required answers. Where the scheme prices them 1 mharc + 1 mharc, each answer is also a one-mark practice slot; where it prices 2 mharc + 1 mharc (order-dependent) the part stays whole.'
ONE='One required answer; the accepted list is the key for one task.'
POINTS='Two independent six-mark points (P1, P2): practice slots plus the whole part.'
OPIN='Opinion (2) and two reasons (5 + 5) stay inside one response.'
POEM='Required content within the selected poem route; “pointe amháin” is the minimum support, not a selection.'
STRUCT='Section heading / structure statement, not a separate route.'
rules=[(3,'Freagair gach ceist (Ceist 1',REQ),(3,'Freagair Léamhthuiscint A (50',READ),(3,'Tá Ceist 1 ‐ 5 ar aon mharc','Equal 7-mark questions 1–5; answer-language rule, not a selection.'),
 (3,'Freagair Ceist 2A (30',Q2),(3,'2A (a) nó 2A (b)',Q2),(3,'2B (a) nó 2B (b)',Q2),(3,'Freagair Ceist 3A (30',Q3),(3,'3A (a) nó 3A (b)',Q3),(3,'3B (a) nó 3B (b)',Q3),
 (3,'2B. Prós Roghnach',Q2),(3,'3B. Filíocht Roghnach',Q3),(3,'nó',STRUCT),(3,'Ceist 4 (A, B, C, D, E nó F)',Q4),
 (4,'Freagair Léamhthuiscint A agus',READ),(4,'Léigh an sliocht',READ),(4,'Stanislaus Ní Chinnéide, nó',TEXT),(4,'roghnaigh sí a bheith',TEXT),(4,'idir an dá linn',TEXT),
 (5,'nuair a roghnaigh sí',ONE),(5,'Tabhair dhá phointe eolais',POINTS),
 (6,'Léigh an sliocht',READ),(6,'rogha leathan',TEXT),(6,'uair nó dhó',TEXT),(6,'athúsáid nó a dheisiú',TEXT),(6,'arís nó iad a roinnt',TEXT),(6,'roghanna inbhuanaithe',TEXT),(6,'nó olla, nó',TEXT),
 (7,'ar cíos nó ar',TEXT),(7,'rud amháin a dhéanann',ONE),(7,'dhá bhealach a bhfuil déantús',TWO),(7,'dhá dheis',TWO),(7,'dhá rud faoi na héadaí',TWO),(7,'dhá rud atá á ndéanamh',TWO),(7,'dhá chúis',TWO),(7,'dhá bhealach a bhfuil a gcúl',TWO),(7,'Tabhair dhá fháth',OPIN),
 (8,'Freagair Ceist 2A (Prós',Q2),(8,'Freagair do rogha ceann amháin de (a) nó (b) thíos.',Q2),(8,'Cáca Milis nó ar an dráma',Q2),(8,'nó',Q2),(8,'ngearrscéal Dís',Q2),(8,'Prós Roghnach',Q2),
 (8,'Níl cead aon ábhar','Restriction on content, not a route.'),(8,'scannán roghnach nó ar an dráma roghnach',Q2),(8,'Maidir leis an scannán roghnach',Q2),(8,'Maidir leis an dráma roghnach',Q2),(8,'ngearrscéal roghnach',Q2),(8,'Maidir le gearrscéal roghnach',Q2),(8,'PRÓS AINMNITHE nó PRÓS ROGHNACH',STRUCT),
 (9,'Freagair Ceist 3A (Filíocht',Q3),(9,'Freagair do rogha ceann amháin de (a) nó (b).',Q3),(9,'pointe amháin',POEM),(9,'(iii) Cé a chum',POEM),(9,'FILÍOCHT AINMNITHE nó',STRUCT),(9,'Cliabh dhá dhroim',TEXT),
 (10,'nó',Q3),(10,'Roghnaíonn an file',POEM),(10,'pointe amháin',POEM),(10,'(iii) Cé a chum',POEM),(10,'(nó ar chrann ar bith)',TEXT),
 (11,'3B. Filíocht Roghnach',Q3),(11,'Freagair do rogha ceann amháin',Q3),(11,'Níl cead aon ábhar','Restriction on content, not a route.'),(11,'dán nua‐aimseartha roghnach',Q3),(11,'príomhthéama an dáin, dar leat.',POEM),
 (11,'Déan plé ar an',POEM),(11,'pointe amháin',POEM),(11,'(iii) Cé a chum',POEM),(11,'nó',Q3),(11,'(ii) An bhfuil teideal',POEM),
 (12,'Ceist 4 (A, B, C, D, E nó F)',Q4),(12,'an dá thréith','4B asks for the two main traits: required content of one essay, not a pool.'),(12,'Freagair (i), (ii) agus (iii)','4F: all three parts required in one route.'),
 (12,'(i) Cad é príomhthéama',POEM),(12,'Déan plé ar an bhforbairt',POEM),(12,'Tabhair dhá fháth','4F(iii): two required reasons inside one 9-mark part (1 + 4 + 4).'),(12,'Bíodh tagairtí cruinne',POEM),
 (13,'ar dhá chois',TEXT),(16,'D’fhéadfadh sé','Copyright statement, not a task.'),(16,'Gaolmhar, 2000','Copyright statement, not a task.'),(16,'a eascraíonn as','Copyright statement, not a task.')]
paper=ROOT/'paper-trail-corpus/exampapers/2026/LC001ALP200IV.pdf';scheme=ROOT/'paper-trail-corpus/markingschemes/2026/LC001ALP100IV.pdf'
d=fitz.open(paper);decisions=[]
for i,p in enumerate(d,1):
    for line in p.get_text().splitlines():
        raw=clean(line)
        if not DIRECTIVE.search(raw):continue
        hits=sorted([(len(k),r) for pg,k,r in rules if pg==i and (k==raw if k=='nó' else k in raw)],reverse=True)
        assert hits and (len(hits)==1 or hits[0][0]>hits[1][0]),(i,raw,hits)
        decisions.append(dict(page=i,raw=raw,decision=hits[0][1]))
ledger=dict(year=2026,level='higher',paperFileid='LC001ALP200IV.pdf',schemeFileid='LC001ALP100IV.pdf',
 paperSha256=hashlib.sha256(paper.read_bytes()).hexdigest(),schemeSha256=hashlib.sha256(scheme.read_bytes()).hexdigest(),
 reviewDate='2026-10-11',status='reviewed',reviewedPaperPages=list(range(1,17)),reviewedSchemePages=list(range(17,50)),
 schemeScope='Combined Paper 1 and Paper 2 scheme. PDF 17–24 reading (general notes, annotation key, both passages); 25–26 literature annotation key, Gaeilge 5 and prose category tables; 27–31 prose; 32–39 poetry; 40–48 additional literature; 49 modified marking (SMM). PDF 1–16 and 50–52 belong to Paper 1 or are blank.',
 reviewMethod='Visual inspection of every paper page (including cover, blank 2/14/15 and acknowledgements 16) and every applicable scheme page; cross-checked extracted text.',
 selectionDecisions=decisions,
 nonPoolDecisions=['Reading: all twelve questions are required; each printed part is a practice card at its published tariff. “1 mharc + 1 mharc” answers expose one-mark slots; “2 mharc + 1 mharc” items (grammar 6(a), B4(a), B5(a)) stay whole as 0/2/3.',
   'A6(b) has two independent six-mark points (P1, P2) with practice slots; B6(b) keeps opinion 2 + two reasons 5 + 5 inside one response.',
   'Prose, poetry and Q4 choices are closed printed routes (6 + 4 + 6); the optional film/play/story/poem itself is open content chosen by the candidate.',
   'Scheme lists of accepted points and supporting notes are indicative answer keys, not route pools.',
   'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.'],
 sourceFindings=['Paper 2 = 200: Ceist 1 reading 100 (A 50 + B 50: Q1–5 at 7 = 3 + 2 + 2; Q6 15 = 3 + 12), Ceist 2 prose 30, Ceist 3 poetry 30, Ceist 4 additional literature 40.',
   'Reading grammar 6(a): 2 marks for the first correct item and 1 for the other (0/2/3). A5(a) loses a mark for each of faisnéis/cúnamh dlíthiúil/tacaíochtaí omitted. B2(a) any three of four elements. B5(b)(ii) needs “chun ábhair nua a dhéanamh díobh” for the second mark.',
   'A6(b): two points P1 + P2 at 6 each (Léiriú table 6/5/4/3/2/0–1), own words; B6(b): opinion 2 + reasons F1/F2 at 5 each (table 5/4/3/2/0–1). Direct lifts from the passage are bracketed and earn no credit.',
   'Prose 25 Eolas + 5 Gaeilge; one aspect only discussed → Eolas marked out of 18. Poetry (i) 13 / (ii) 5 / (iii) 7 + Gaeilge 5; prescribed (i) with one image only → out of 10; (iii) wrong or missing poet name → 0 for the part. Q4 Eolas 35 + Gaeilge 5; 4B with one trait → out of 25; 4F (i) 19 (theme 2 + 17), (ii) 7, (iii) 9 (Tá/Níl 1 + 4 + 4).',
   'Paper vs scheme wording: none affecting answers. The scheme spells “dírbheathaIsnéis” (4B) with a capital I; original kept.'],
 remainingWork=[])
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = [('Closed choice: Q2A or Q2B, then (a) or (b); 2A(a) itself offers Cáca Milis or An Lasair Choille and 2B(a) a film or a play. Six whole 30-mark routes.',
  'Closed choice: Q2A or Q2B, then (a) or (b); 2A(a) itself offers Cáca Milis or An Lasair Choille (different texts and Atlas headings: one card each) and '
  '2B(a) a film or a play (one grid and one Atlas heading: one card carrying both). Five whole 30-mark cards.')]
RECORDED = {'runtimeVerification': {'date': '2026-10-11',
                         'viewport': [390, 844],
                         'markBankRoutes': 6,
                         'atlasRoutes': 6,
                         'sourceReader': 'Reading cards render both passage pages; prose/poetry/Q4 routes render their printed page(s) (4F: 2 pages); '
                                         'navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Each route rendered its paper pages plus its scheme pages (R-A-6 2+2, F-3A-a 1+3, X-4F 2+4); section 1 rendered 7 scheme '
                                  'pages.',
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
    finish(LEDGER, 'irish-higher-2026-p2-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
