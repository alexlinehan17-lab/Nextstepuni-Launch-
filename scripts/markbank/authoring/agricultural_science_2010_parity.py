"""Visual review of the 2010 Irish editions, including translation defects.

Parity means the tasks were compared, not that the two schemes are identical.
The source discrepancies must accompany the original schemes in the reader.
"""
import hashlib
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]


def scan(year, fileid, hashes, classifications, supplementary=()):
    from agricultural_science_inventory import DIRECTIVE
    for kind, digest in hashes.items():
        assert hashlib.sha256((ROOT / f'paper-trail-corpus/{kind}/{year}/{fileid}').read_bytes()).hexdigest() == digest, 'Source changed; repeat visual review'
    observed, pages = [], []
    with fitz.open(ROOT / f'paper-trail-corpus/exampapers/{year}/{fileid}') as pdf:
        for index, page in enumerate(pdf):
            text = ' '.join(page.get_text().split())
            pages.append(text)
            for match in DIRECTIVE.finditer(text):
                context = text[max(0, match.start()-90):match.end()+230]
                key = hashlib.sha256(f'{hashes["exampapers"]}|{index+1}|{match.start()}|{context}'.encode()).hexdigest()[:16]
                assert key in classifications, f'Unclassified cue {key}: {context}'
                kind, reason = classifications[key]
                observed.append(dict(id=key, page=index+1, cue=match.group(), context=context, classification=kind, reason=reason))
    assert {cue['id'] for cue in observed} == set(classifications), 'Stale selection classification'
    for page, wording, _, _ in supplementary:
        assert pages[page-1].count(wording) == 1, f'Stale supplementary selection: {wording}'
    return observed, [dict(page=p, wording=w, classification=k, reason=r) for p,w,k,r in supplementary]


def paper_reviews():
    result = []
    for level, letter, hashes, page_counts, cues, extra, notes in [
        ('higher', 'A', {
            'exampapers':'a70bf69bcd6b598cf3d258105870afeb54fa52c3ec637d8d8a0212f113837042',
            'markingschemes':'461837ea374e65d3a33802131ba9b476dea93ec3d3e48a93753f27f3bf220248',
        }, (8,12), {
            '1596f9b705b57549':('independent-task-selection','Q1: select six separately priced tasks; all ten and the internal Q1(d) boundary correspond to the English ledger.'),
            '8c8365cdbc2b1501':('independent-task-selection','Q4: select two independently priced experiments; all four are represented by the English ledger.'),
            'd8d42a0d3d699fb6':('closed','Q7(a): the same three-of-four genetics terms as English; four complete routes.'),
            'df55007fddb4691c':('independent-task-selection','Q8: select two independent 24-mark tasks. Q8(c) has its own internal three-of-four routes.'),
            '4e757ccca4f2d193':('independent-task-selection','Second regex match within the same Q8 outer selection; it does not create an extra pool.'),
        }, [
            (2,'SÉ CHEIST LE FREAGAIRT','exam-selection','Six examination questions, not a combined practice task.'),
            (3,'NÓ Rogha a Dó','closed','Both Q3 options match the separately reviewed English tasks.'),
            (3,'ceann amháin ar bith de na galair','closed','Q3 Option Two disease choice: hoose or grass tetany, two complete routes.'),
            (3,'mhodh saotharlainne nó ar mhodh páirce','open','Laboratory/field are settings; no finite pool of named experimental responses.'),
            (5,'dtrí cinn ar bith de na péirí','closed','Q8(c): choose three of four comparisons, four routes.'),
            (5,'cheithre cinn ar bith','independent-task-selection','Q9: four separately priced explanations chosen from five, all five retained.'),
        ], [
            {'questionN':'7','questionRef':'Q7(b)','paperPage':4,'schemePage':10,
             'note':'Source lettering differs: the Irish question uses D/d for black/brown coats, but its official scheme prints B/b. Read Bb and bb in the scheme as Dd and dd respectively when answering this Irish question.'},
        ]),
        ('ordinary', 'G', {
            'exampapers':'3fc25d232f647d8f69253fe013851c4af674a786fa5d77e84e5288d688710d2f',
            'markingschemes':'41a9cc8a3f98ddebc0918c5e28fef44b11c19149f0151cca14931b87238e36e5',
        }, (12,13), {
            '89a886161f8fc6b4':('exam-selection','Section One: six independent questions, all seven retained.'),
            'fb4e129034265e1d':('open','Q1(b): two mineral particle types, with no printed finite pool.'),
            'b751aadca4f6be00':('answer-identification','Q2: match each activity to an appropriate machine, not arbitrary machine-selection routes.'),
            '263792c10f064029':('answer-identification','Q3(a): identify two dairy breeds. The scheme accepts Friesian, Jersey and Simmental; incorrect breed pairs are not examination routes.'),
            '1827828fcb1543d0':('exam-selection','Section Two: three independent 60-mark questions, all six retained.'),
            'e3ccc0d05d6bfbed':('independent-task-selection','Q12: two of four separately priced parts; retain all published internal tasks, not pairs of unrelated exam responses.'),
        }, [
            (7,'Ainmnigh barr fréimhe nó barr gráin','open','Q9(c): name an appropriate crop; root/cereal are open categories, not a finite pool of crop names.'),
        ], [
            {'questionN':'6','questionRef':'Q6(b)','paperPage':5,'schemePage':5,
             'note':'The Irish scheme prints “Clóraplast” for the green pigment. The English scheme for this same question gives “Chlorophyll”. The original Irish scheme is shown unchanged.'},
            {'questionN':'8','questionRef':'Q8(c)','paperPage':6,'schemePage':7,
             'note':'The Irish scheme explicitly describes a method name plus two matching points (3 × 3 marks). The English scheme allows the name to count as one of three points. Follow the instructions in the displayed edition.'},
            {'questionN':'9','questionRef':'Q9(f)','paperPage':7,'schemePage':9,
             'note':'The Irish scheme prints 4 + 4 + 6 + 6 for Q9(f), while the English scheme prints 4 + 4 + 4 + 6. The Irish allocations therefore total 62 for the printed 60-mark question. This source discrepancy is preserved.'},
            {'questionN':'12','questionRef':'Q12(a)(iii), Q12(d)(ii)','paperPage':9,'schemePage':12,
             'note':'For Q12(a)(iii), the Irish scheme says four points; the English scheme says three but prints four awards. For Q12(d)(ii), the Irish scheme prints 4 + 4 + 6 + 6 (20); the English scheme prints 4 + 4 + 4 + 6 (18). The Irish Q12(d) allocations total its printed 30 marks.'},
            {'questionN':'13','questionRef':'Q13(b)','paperPage':10,'schemePage':13,
             'note':'Source lettering differs: the Irish pig crosses use C/c, but the Irish scheme retains E/e. Read E, e, EE and Ee in that scheme as C, c, CC and Cc respectively. The pea passage also uses A/a where the English paper uses T/t.'},
        ]),
    ]:
        fileid = f'LC024{letter}LP000IV.pdf'
        observed, supplementary = scan(2010,fileid,hashes,cues,extra)
        result.append({
            'year':2010,'level':level,'lang':'iv','paperFileid':fileid,'hashes':hashes,
            'wholePaperVisualReview':'reviewed','schemeBoundaryReview':'reviewed',
            'paperPagesInspected':list(range(1,page_counts[0]+1)),
            'schemePagesInspected':list(range(1,page_counts[1]+1)),
            'selectionDirectives':observed,'supplementarySelections':supplementary,
            'translationParity':'All original pages visually inspected. Printed tasks, diagrams and finite choices compared with English; source differences below prevent treating the schemes as identical.',
            'sourceNotes':notes,
            'remaining':['Irish practice-task crop bindings and reader QA','Corpus-wide reconciliation'],
        })
    return result
