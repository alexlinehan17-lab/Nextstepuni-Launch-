#!/usr/bin/env python3
"""Rebuild irish-higher-2023-p2-source-review.json from the official paper (see _ledger.py).

AMENDMENTS and RECORDED carry the later, dated edits.
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
"""Write the 2023 Higher Paper 2 source-review ledger: every raw directive line classified."""
import fitz  # noqa: E402
from irish_higher_2023_p2 import DIRECTIVE, clean, PAPER_SHA, SCHEME_SHA  # noqa: E402

paper = fitz.open('paper-trail-corpus/exampapers/2023/LC001ALP200IV.pdf')
lines = list(dict.fromkeys((i, clean(l)) for i, p in enumerate(paper, 1) for l in p.get_text().splitlines() if DIRECTIVE.search(clean(l))))
Q2 = 'Closed choice: Q2A (Prós Ainmnithe) or Q2B (Prós Roghnach), then (a) or (b): four whole 30-mark routes (Oisín i dTír na nÓg, Dís, optional folktale, optional short story).'
Q3 = 'Closed choice: Q3A or Q3B, then (a) or (b): four whole 30-mark routes, each answering (i), (ii) and (iii).'
Q4 = 'Closed choose-one of 4A–4F: six whole 40-mark routes.'
BOTH = 'Both reading passages and every question in each are required; each printed part is also a practice card.'
SRC = 'Source-text wording inside a reading passage or poem, not a candidate instruction.'
TWO_ORDERED = 'Two required answers inside one printed part, priced 2 mharc + 1 mharc (order-dependent): the part stays whole at 0/2/3.'
TWO_SLOTS = 'Two required answers inside one printed part, priced 1 mharc + 1 mharc: each answer is also a one-mark practice slot.'
ONE = 'One required answer; the accepted list is the key for one task.'
POEM_ONE = 'Required content within the selected poem route; “pointe amháin” is the minimum support, not a selection.'
D = {
    'Freagair gach ceist (Ceist 1, Ceist 2, Ceist 3 agus Ceist 4).': 'Required answers; no finite task menu.',
    'Ceist 1: Freagair Léamhthuiscint A (50 marc) agus Léamhthuiscint B (50 marc).': BOTH,
    'Tá Ceist 1 - 5 ar aon mharc. Glacfar le freagraí i d’fhocail féin nó': 'Equal 7-mark questions 1–5; answer-language rule, not a selection.',
    'Freagair Ceist 2A (30 marc) nó Ceist 2B (30 marc).': Q2,
    'Freagair ceist amháin as do rogha de 2A (a) nó 2A (b).': Q2,
    'nó': 'Separates printed alternatives (2A/2B and 3A/3B on page 3; 2A(a)/(b), 2B(a)/(b), 3A(a)/(b), 3B(a)/(b) on pages 8–11); each is a whole route, never combined.',
    '2B. Prós Roghnach': Q2,
    'Freagair ceist amháin as do rogha de 2B (a) nó 2B (b).': Q2,
    'Freagair Ceist 3A (30 marc) nó Ceist 3B (30 marc).': Q3,
    'Freagair ceist amháin as do rogha de 3A (a) nó 3A (b).': Q3,
    '3B. Filíocht Roghnach': Q3,
    'Freagair ceist amháin as do rogha de 3B (a) nó 3B (b).': Q3,
    'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F).': Q4,
    'Freagair Léamhthuiscint A agus Léamhthuiscint B anseo.': BOTH,
    'Léigh an sliocht seo a leanas agus freagair na ceisteanna ar fad a ghabhann leis.': BOTH,
    'don gheimhreadh ar Oileán Ross. Roghnaigh': SRC,
    'Bhain tubaiste do Tom lá amháin. Ba bheag': SRC,
    'Theas a bhuachan. Roghnaigh sé Tom Crean mar': SRC,
    'ar Crean nuair nár roghnaíodh eisean agus bhí air': SRC,
    'le hithe aige ach trí bhriosca agus dhá phíosa': SRC,
    '1. D’ainmnigh an Coimisiún Eorpach an bhliain': SRC,
    'agus áitiúla in 2024 nó a bheith páirteach san': SRC,
    '(b) (i) Scríobh síos cineál amháin taighde a bheidh ar siúl ag na heolaithe mara ar an RV Tom Crean.': ONE,
    '2. (a) Scríobh síos dhá phointe eolais faoi mhuintir Tom Crean agus é ag fás aníos gar d’Abhainn an Scáil': TWO_ORDERED,
    '(b) (i) Scríobh síos dhá phointe eolais faoin gcruatan a d’fhulaing Crean agus na fir eile ar an turas': TWO_SLOTS,
    '(ii) Cén tubaiste a bhain do Tom Crean lá amháin agus é ag cabhrú leis an long a scaoileadh?': '“lá amháin” is part of the question wording (one day), not a count of answers; one required answer.',
    '(b) (i) Luaigh dhá phointe eolais faoin siúl ab éigean do Crean a dhéanamh chun cabhair a lorg': TWO_SLOTS,
    '(b) (i) Tabhair pointe amháin eolais faoin turas farraige a rinne Shackleton agus a chriú ó Oileán': ONE,
    '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé ar dhá thréith de chuid Tom Crean, dar leat.':
        'Two independent six-mark traits (trait 2 + support 4 each): practice slots plus the whole part; own words required.',
    'Bíodh sampla amháin ón sliocht agat, i d’fhocail féin, ag tacú le gach tréith a luann tú':
        'One supporting example per trait, inside each six-mark trait award; not a selection.',
    '(b) (i) Scríobh síos príomhchuspóir amháin a leagadh amach do Bhliain Eorpach na hÓige. (Alt 1)': ONE,
    '2. (a) Luaigh dhá aidhm de chuid na n-imeachtaí a d’eagraigh an eagraíocht Léargas in Éirinn le linn': TWO_ORDERED,
    '3. (a) Scríobh síos dhá shlí a mbaineann mic léinn na n-institiúidí tríú leibhéal tairbhe as clár Erasmus+.': TWO_ORDERED,
    '(b) (i) Tabhair dhá phointe eolais faoin obair dheonach a dhéanann na daoine óga ar fud na hEorpa': TWO_SLOTS,
    '(ii) Luaigh an dá rud a fhoghlaimíonn scoláirí dara leibhéal sa togra ‘Clár Scoileanna Ambasadóra': TWO_SLOTS,
    '4. (a) Scríobh síos dhá rud a dúirt Harry McCann faoin gcaoi ar chuir paindéim Covid-19 isteach': TWO_ORDERED,
    '(b) (i) Scríobh síos pointe amháin eolais faoi óige dhaonra an Aontais Eorpaigh. (Alt 5)': ONE,
    'dar leat? Tabhair dhá phointe eolais, i d’fhocail féin, as an sliocht, mar thacaíocht le do fhreagra.':
        'Opinion (2) and two supported points (5 + 5) stay inside one response, as in 2026 B 6(b); own words required.',
    'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach).': Q2,
    'Freagair do rogha ceann amháin de (a) nó (b) thíos.': Q2 + ' Printed for 2A, 2B (page 8) and 3B (page 11).',
    'Déan plé ar an dá thréith is mó, dar leat, a bhaineann le hOisín mar a léirítear iad':
        '2A(a): two traits discussed inside one 25-mark Eolas award (18 if only one trait); not a selection.',
    'Prós Roghnach': Q2,
    'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.': 'Restriction on content, not a route.',
    'Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé ar an':
        'Optional folktale chosen by the candidate: open content inside one route (two traits of the main character).',
    'Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé ar mheon':
        'Optional short story chosen by the candidate: open content inside one route.',
    'PRÓS AINMNITHE nó PRÓS ROGHNACH 30 marc': 'Section heading / structure statement, not a separate route.',
    'Freagair Ceist 3A (Filíocht Ainmnithe) nó Ceist 3B (Filíocht Roghnach).': Q3,
    'Freagair do rogha ceann amháin de (a) nó (b).': Q3,
    '(Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.)': POEM_ONE,
    'FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH 30 marc': 'Section heading / structure statement, not a separate route.',
    '(nó ar chrann ar bith)': SRC,
    '(iii) Cén mheadaracht atá sa dán seo? Scríobh pointe amháin eolais faoin meadaracht seo': POEM_ONE,
    'Filíocht Roghnach': Q3,
    'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.': 'Restriction on content, not a route.',
    'Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa,': 'Optional poem chosen by the candidate: open content inside one route.',
    'Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú':
        'Optional poem chosen by the candidate: open content inside one route.',
    'Tabhair dhá phointe eolais faoin teicníc sin sa dán.': 'Required content within the selected poem route (technique 1 + two points 3 + 3); not a selection.',
    'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.': Q4,
    'Freagair (i), (ii) agus (iii) thíos.': '4F: all three parts required in one route.',
    'Is leor dhá phointe eolais. Bíodh tagairtí cruinne agat do théacs an dáin i do fhreagra.':
        '4F(iii): two required points inside one 9-mark part (5 + 4); not a selection.',
    'Nó sin é deir sibh liom –': SRC,
    'Níl baint agam le rogha bhúr gcroí –': SRC,
    'Níl rogha agam i bhúr dtodhchaí': SRC,
}


def decide(p, r):
    if r in D:
        return D[r]
    if p == 16:
        return 'Copyright statement, not a task.'
    raise SystemExit(f'Unclassified directive: {p} {r}')


out = [dict(page=p, raw=r, decision=decide(p, r)) for p, r in lines]
ledger = dict(
    year=2023, level='higher', paperFileid='LC001ALP200IV.pdf', schemeFileid='LC001ALP000IV.pdf', paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
    reviewDate='2026-10-12', status='reviewed', reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=list(range(18, 51)),
    schemeScope=('Combined Paper 1 and Paper 2 scheme. PDF 18 reading notes and annotation key; 19–22 Léamhthuiscint A; 22–26 Léamhthuiscint B; '
                 '27 literature annotation key; 28 literature notes, Gaeilge 5 and prose 25/18 tables; 29–31 prose; 32–39 poetry; 40 Ceist 4 notes and '
                 '35/25 table; 41–49 additional literature; 50 modified marking (SMM). PDF 1–17 belong to Paper 1; 51–52 blank.'),
    reviewMethod=('Visual inspection of every paper page (1 cover with the COVID-19 adjustment note, 2 and 14–15 blank, 3 instructions, '
                  '16 acknowledgements) and every applicable scheme page; cross-checked extracted text.'),
    selectionDecisions=out,
    nonPoolDecisions=[
        'Reading: all twelve questions are required; each printed part is a practice card at its published tariff. “1 mharc + 1 mharc” answers expose '
        'one-mark slots (A3(b)(i), A4(b)(i), B2(b)(ii), B3(b)(i), B3(b)(ii)); “2 mharc + 1 mharc” items (A2(a), B2(a), B3(a), B4(a), B5(a) and both 6(a)) '
        'stay whole as 0/2/3.',
        'A 6(b) has two independent six-mark traits (trait 2 + support 4) with practice slots; B 6(b) is an opinion (2) and two supported points (5 + 5) '
        'inside one response (no slots, as in 2026 B 6(b)). Both must be in the candidate’s own words.',
        'Single-answer parts allow only the mark values the scheme prints for them (0, the printed partials and the full tariff); A3(a) prints its '
        'partial as “bronntar 2 mharc”.',
        'Prose, poetry and Q4 choices are closed printed routes (4 + 4 + 6) and were already carded (IDs retained); the optional folktale, short story '
        'or poem itself is open content chosen by the candidate.',
        'Scheme lists of accepted points and supporting notes are indicative answer keys, not route pools.',
        'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.'],
    sourceFindings=[
        'Paper 2 = 200: Léamhthuiscint A 50 + B 50 (Q1–5 at 7 = (a) 3 + (b)(i) 2 + (b)(ii) 2; Q6 at 15 = (a) 3 + (b) 12), Prós 30, Filíocht 30, '
        'Litríocht Bhreise 40.',
        'Reading A “Tom Crean – Taiscéalaí Ciarraíoch an Antartaigh” (paper 4–5, scheme PDF 19–22); B “2022: Bliain Eorpach na hÓige” (paper 6–7, '
        'scheme PDF 22–26).',
        'Literature language: 5 marks for Gaeilge in every literature answer (scheme PDF 28); prose 25 Eolas (18 column for a one-aspect answer); '
        'poetry printed (i) 15, (ii) 6, (iii) 9 on the paper, assessed as Eolas 13, 5, 7 plus Gaeilge 5 once; Q4 Eolas 35 (25 for 4A with one '
        'character); 4F printed (i) 20, (ii) 10, (iii) 10, assessed as Eolas 19, 7, 9 (5 + 4) plus Gaeilge 5.',
        'Paper vs scheme wording: A1(b)(ii) the scheme adds “soir” (cuairt ghearr soir); B6(b) the paper says “Bliain Eorpach na hÓige 2022”, the '
        'scheme omits “2022”; 4F(iii) the paper adds “sa dán”. Cards keep the paper wording.',
        'Scheme layout: the text layer stores each poetry band table (Plé 11/13, Marc as 5) and the 4F Marc as 7 table after the following '
        'sub-question; the generator returns each table to the sub-question it is printed beside.',
        'Cover (PDF 1, printed as an image): the 2023 papers were adjusted to compensate for COVID-19 learning disruption. The cards follow the '
        'printed 2023 structure; the note offers no choice.',
        'Legacy corrections (IDs, totals and topics unchanged): the twelve whole reading questions each had one undivided criterion; the four poetry '
        'routes had one undivided 25-mark Eolas criterion, and for both prescribed poems (3A) its guidance began at (ii), with the (i) scheme missing; '
        'every literature route carried a paraphrased Gaeilge band (“sásúil”) instead of the printed table. All now carry the lifted 2023 scheme text '
        'and part tariffs.'],
    remainingWork=[])
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = []
RECORDED = {'runtimeVerification': {'date': '2026-10-13',
                         'viewport': [390, 844],
                         'markBankRoutes': 5,
                         'atlasRoutes': 5,
                         'sourceReader': 'A retained whole reading question (A 6), an A 6(b) trait slot, a one-mark answer slot, a prescribed poem and 4F rendered '
                                         'their paper pages (passage pages 4–5/6–7, poem pages 9 and 13); navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Each route rendered its paper pages plus reviewed scheme pages (frozen reading Ceist 6 2+2, R-B-6-b 2+2, 3A(a) 1+3, 4F 2+3, '
                                  '2B(a) 1+2).',
                         'browserErrors': []}}
KEY_ORDER = ['year', 'level', 'paperFileid', 'schemeFileid', 'paperSha256', 'schemeSha256', 'reviewDate', 'status', 'reviewedPaperPages',
             'reviewedSchemePages', 'schemeScope', 'reviewMethod', 'selectionDecisions', 'nonPoolDecisions', 'sourceFindings', 'remainingWork',
             'runtimeVerification']

if __name__ == '__main__':
    finish(LEDGER, 'irish-higher-2023-p2-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
