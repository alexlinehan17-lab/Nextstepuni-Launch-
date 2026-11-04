#!/usr/bin/env python3
"""Generate visually reviewed listening tasks from pinned papers and recordings.

Every string a card shows as the SEC's (question, context, choices, answer
lines, rules, conventions) is lifted from the booklet or scheme page by
fr_printed; the review ledger's typed text only locates it. NextStepUni's own
guidance goes to practiceNotes, never to an SEC-attributed field.
"""
from pathlib import Path
import json,re,hashlib
import fitz
from fr_writing import norm
from fr_selection import verify_paper
from fr_reviewed_tasks import write_tasks
from fr_printed import lift, doc_texts, heading_before, MARKS
import fr_printed_rules as printed_rules


def lifted_guide(groups, typed, what):
    """Each answer line as the scheme prints it. Where the printed answers carry
    no marks of their own, the printed line that carries them comes first."""
    out, first_unpriced = [], None
    for line in typed:
        try:
            out.append(lift(groups, line, what=what))
        except AssertionError:
            body = re.sub(rf'(?:\s—\s|\s=\s|\s)({MARKS})\.?$', '', line)
            out.append(lift(groups, body, marks='', what=what))
            if first_unpriced is None:
                first_unpriced = len(out) - 1
    if first_unpriced is not None and not any(re.search(rf'{MARKS}\.?$', x) for x in out[:first_unpriced]):
        out.insert(first_unpriced, heading_before(groups, typed[first_unpriced], what=what))
    return out

ROOT=Path(__file__).resolve().parents[3]

def build():
    review=json.loads(Path(__file__).with_name('french-listening-review.json').read_text())
    audio=json.loads((ROOT/'data/frenchAudio.json').read_text())
    entries=[json.loads(line.strip().rstrip(',')) for line in (ROOT/'paperTrailData.ts').read_text().split('  "french": [',1)[1].split('\n  ],',1)[0].splitlines() if line.strip()]
    entries=[entry for entry in entries if not entry.get('sitting') and entry['year']>=2010]  # reviewed window: June 2010+
    tags=json.loads((ROOT/'scripts/paper-trail/topic-tags/tags/french.json').read_text())
    runtime=json.loads((ROOT/'data/examTopics/french-runtime.json').read_text())
    cards,tasks=[],[]
    for record in review['papers']:
        year=record['year']
        for source in record['sources']:
            assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256'],source['path']
        recording=next(a for a in audio if a['year']==year)
        for level in ['hl','ol']:
            path=ROOT/f'examiner-reports/french/papers/{year}-{level}-A00-paper.pdf'
            verify_paper(path)
            paper=fitz.open(path);scheme=fitz.open(ROOT/f'examiner-reports/french/schemes/{year}-{level}.pdf')
            general_page=record.get('generalRulesPages',{}).get(level,20)
            scheme_offset=record.get('schemePrintedPageOffsets',{}).get(level,0)
            level_name='higher' if level=='hl' else 'ordinary'
            entry=next(e for e in entries if e['year']==year and e['level']==level_name and e['lang']=='ev')
            doc=next(p for p in entry['papers'] if 'A00' in p['doc']['f'])
            assert doc['doc']['f'] in recording['paperFileids']
            paper_tags=next(p for p in tags if p['year']==year and p['fileid']==doc['doc']['f'])
            aural_language,_=printed_rules.aural_language(year,level)
            general=list(printed_rules.listening_general(year,level,general_page))
            notes=printed_rules.scheme_notes(year,level)
            paper_path=ROOT/f'examiner-reports/french/papers/{year}-{level}-A00-paper.pdf'
            scheme_path=ROOT/f'examiner-reports/french/schemes/{year}-{level}.pdf'
            for unit in [u for u in record['tasks'] if u['level']==level]:
                section,q=unit['section'],unit['question']
                printed_section=record.get('sectionLabels',{}).get(section,section)
                page=paper[unit['paperPage']-1]
                text=page.get_text(clip=fitz.Rect(page.rect.width/2,0,page.rect.width,page.rect.height))
                assert norm(unit['prompt']) in norm(text),unit
                context = record['sectionContexts'][level][section]
                assert norm(context) in norm(page.get_text()), context
                paper_groups=doc_texts(paper_path,[unit['paperPage']])
                what=f'{year} {level} L{section} Q{q}'
                prompt=lift(paper_groups,unit['prompt'],marks='',what=what)
                context=lift(paper_groups,context,marks='',what=what)
                for option in unit.get('choices',[]):assert norm(option) in norm(text),option
                choices=[lift(paper_groups,option,marks='',what=what) for option in unit.get('choices',[])]
                scheme_pages=unit.get('schemePages',[unit['schemePage']])
                assert scheme_pages[0]==unit['schemePage']
                scheme_text='\n'.join(scheme[p-1].get_text(sort=True) for p in scheme_pages)
                scheme_citation_pages=('p.' if len(scheme_pages)==1 else 'pp.')+','.join(str(p+scheme_offset) for p in scheme_pages)
                for line in unit['answerGuide']:assert norm(line.split(' — ')[0]) in norm(scheme_text),line
                practice=[]
                if 'schemeChoiceIndex' in unit:
                    index=unit['schemeChoiceIndex']
                    assert isinstance(index,int) and 0<=index<len(unit['choices'])==4
                    letter=chr(97+index)
                    assert unit['answerGuide']==[f'({letter}) — {unit["totalMarks"]} Marks']
                    # Older schemes publish only the letter. The option it names is
                    # checked against the paper and reviewed with the key; it is
                    # quoted as our note, never joined to the scheme's line.
                    practice.append(f'The scheme’s answer ({letter}) is this option on the paper: “{choices[index]}”')
                answer_guide=lifted_guide(doc_texts(scheme_path,scheme_pages),unit['answerGuide'],what)
                parent=str(ord(section)-64)
                tag=next(q for q in paper_tags['q'] if q['n']==parent)
                indexes=next(m[5] for m in runtime['questionMappings'] if m[:5]==[level_name[0],'e',year-2000,'a',parent])
                n=f'L{section}-Q{q}'
                if unit.get('answerTarget'):
                    target=unit['answerTarget']
                    assert norm(target) in norm(text) and norm(target) in norm(scheme_text)
                    n+='-'+re.sub(r'\W+','-',target.lower()).strip('-')
                cid=f'fr-{year}-{level}-listening-{n.lower()}'
                printed_q=unit.get('printedQuestion',re.sub(r'(\d+)([a-z])',r'\1(\2)',q))
                if unit.get('answerTarget'):printed_q+=' — '+unit['answerTarget']
                source={**recording['source'],'label':f'Section {printed_section} · listening','title':f'{year} French · Section {printed_section}'}
                # The SEC's own rules: the booklet's instruction, then the scheme's.
                rules=[aural_language]
                mcq_instruction=printed_rules.aural_mcq_instruction(year,level,unit['paperPage']) if choices else None
                if mcq_instruction:rules.append(mcq_instruction)
                rules+=general
                for rule in record.get('generalRules',{}).get(level,[]):
                    assert norm(rule) in norm(scheme[general_page-1].get_text())
                    assert any(norm(rule) in norm(g) for g in general),rule
                language_penalty=record.get('wrongLanguagePercent',{}).get(level,50)
                if language_penalty is not None:
                    assert re.search(rf'\b{language_penalty}\s*%',scheme[general_page-1].get_text())
                    assert any(f'{language_penalty}%' in g for g in general),general
                    practice.append(f'The scheme’s {language_penalty}% deduction for answering in French is an aggregate penalty, outside this single-task score.')
                else:
                    assert record.get('wrongLanguageReviewNotes',{}).get(level)
                    assert not re.search(r'\d+\s*%',scheme[general_page-1].get_text())
                if level=='ol' and record.get('ordinaryAnswerRule'):
                    assert norm(record['ordinaryAnswerRule']) in norm(scheme[general_page-1].get_text())
                    assert any(norm(record['ordinaryAnswerRule']) in norm(g) for g in general)
                for rule in record.get('additionalGeneralRules',{}).get(level,[]):
                    assert norm(rule) in norm(scheme[general_page-1].get_text())
                    assert any(norm(rule) in norm(g) for g in general),rule
                if unit['requiredDetails']>1:practice.append(f'Give {unit["requiredDetails"]} distinct details. Do not count the same information twice.')
                if unit.get('scoringRule'):
                    assert unit['scoringRule']=='higher-segment-score-applied-to-both',unit
                    assert unit['requiredDetails']==2
                    assert norm(record['specialScoringSource']) in norm(scheme[general_page-1].get_text())
                    assert unit['permittedMarks']==sorted({2*m for m in unit['segmentMarks']})
                    rules.append(printed_rules.listening_special(year,level,general_page))
                    practice.append('Special rule for this task: score each detail using the scheme, then award the higher detail score to both segments. The task score is twice that higher score, including when the other detail earns 0.')
                practice+=unit['extraRules']
                if choices and not mcq_instruction:practice.append('Select one answer.')
                if unit.get('answerTarget'):practice.append(f'Answer only the {unit["answerTarget"].lower()} part of this printed question. It has its own {unit["totalMarks"]}-mark allocation.')
                if unit.get('contextNote'):practice.append(unit['contextNote'])
                practice.append('Use the accepted answers and partial-credit rules above.')
                material=dict(kind='source-text',label=f'Section {printed_section} question sheet',title=f'Listening Section {printed_section} · original questions',pages=[unit['paperPage']],
                    attribution=f'SEC French {year} {level_name.title()} Level — © State Examinations Commission.',
                    presentationNote=f'The listening booklet’s printed page is {unit["paperPage"]+record.get("printedPageOffset",20)}; the PDF page is {unit["paperPage"]}. Listen to the recording before revealing the scheme.')
                card=dict(id=cid,subjectId='french',level=level_name,source='sec',kind='rubric',year=year,paperFileid=doc['doc']['f'].removesuffix('.pdf'),
                    section=f'L{section}',questionRef=f'{year} {level.upper()} Section {printed_section if "sectionLabels" in record else "L"+section} Q{printed_q}',questionText=prompt,stem=context,
                    totalMarks=unit['totalMarks'],topicId=tag['primary'],conceptId=f'french-listening-{tag["primary"]}',specVersion='lc-french-syllabus',
                    audioMaterial=source,sourceMaterial=material,
                    schemeCitation=f'SEC French {year} {level_name.title()} Level marking scheme, {scheme_citation_pages}; general rules p.{general_page+scheme_offset} — © State Examinations Commission.',
                    schemeRegion=dict(schemeFileid=doc['scheme']['f'],p=unit['schemePage'],r=[0,0,1,1]),
                    rubric=dict(system='french',taskRequirements=rules,answerGuide=answer_guide,
                        criteria=[dict(id='response',label='Response',maxMarks=unit['totalMarks'],permittedMarks=unit['permittedMarks'],guidance=[])],
                        markingGuideNote='\n'.join(notes),practiceNotes=practice),
                    qa=dict(gates=['visual-paper-scheme-review','published-listening-tariff','complete-partial-credit','selection-review','verified-official-audio'],humanReviewedBy='agent-verified',humanReviewedAt=review['reviewedAt']))
                if choices:
                    card['questionChoices']=choices
                    card['questionText']+='\n'+'\n'.join(choices)
                cards.append(card)
                tasks.append(dict(cardId=cid,subjectId='french',level=level_name,year=year,sitting='main',paperKey='aural',lang='ev',fileid=doc['doc']['f'],n=n,parent=parent,
                    topicIds=[runtime['topics'][i][0] for i in indexes],topicId=tag['primary'],pages=[unit['paperPage']],label=f'Listening Section {printed_section} · Q{printed_q}'))
    assert len(cards)==review['expectedCards']
    (ROOT/'components/MarkBank/cards/french/listening.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n')
    write_tasks('listening',tasks)
    print(f'Wrote {len(cards)} reviewed listening tasks with verified audio and exact Atlas identities.')

if __name__=='__main__':build()
