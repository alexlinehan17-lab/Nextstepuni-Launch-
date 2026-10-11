#!/usr/bin/env python3
"""Generate visually reviewed listening tasks from pinned papers and recordings."""
from pathlib import Path
import json,re,hashlib
import fitz
from fr_writing import norm
from fr_selection import verify_paper
from fr_reviewed_tasks import write_tasks

ROOT=Path(__file__).resolve().parents[3]

def build():
    review=json.loads(Path(__file__).with_name('french-listening-review.json').read_text())
    audio=json.loads((ROOT/'data/frenchAudio.json').read_text())
    entries=[json.loads(line.strip().rstrip(',')) for line in (ROOT/'paperTrailData.ts').read_text().split('  "french": [',1)[1].split('\n  ],',1)[0].splitlines() if line.strip()]
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
            for unit in [u for u in record['tasks'] if u['level']==level]:
                section,q=unit['section'],unit['question']
                printed_section=record.get('sectionLabels',{}).get(section,section)
                page=paper[unit['paperPage']-1]
                text=page.get_text(clip=fitz.Rect(page.rect.width/2,0,page.rect.width,page.rect.height))
                assert norm(unit['prompt']) in norm(text),unit
                context = record['sectionContexts'][level][section]
                assert norm(context) in norm(page.get_text()), context
                if unit.get('contextNote'):
                    context += ' ' + unit['contextNote']
                for option in unit.get('choices',[]):assert norm(option) in norm(text),option
                scheme_pages=unit.get('schemePages',[unit['schemePage']])
                assert scheme_pages[0]==unit['schemePage']
                scheme_text='\n'.join(scheme[p-1].get_text(sort=True) for p in scheme_pages)
                scheme_citation_pages=('p.' if len(scheme_pages)==1 else 'pp.')+','.join(str(p+scheme_offset) for p in scheme_pages)
                for line in unit['answerGuide']:assert norm(line.split(' — ')[0]) in norm(scheme_text),line
                answer_guide=unit['answerGuide']
                if 'schemeChoiceIndex' in unit:
                    index=unit['schemeChoiceIndex']
                    assert isinstance(index,int) and 0<=index<len(unit['choices'])==4
                    letter=chr(97+index)
                    assert answer_guide==[f'({letter}) — {unit["totalMarks"]} Marks']
                    # Older schemes publish only the letter. Its corresponding option
                    # is checked against the paper above and reviewed with the key.
                    answer_guide=[f'({letter}) {unit["choices"][index]} — {unit["totalMarks"]} Marks']
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
                rules=['Answer in English or Irish; complete sentences are not required.',
                       'Separate points need not be on separate lines. No penalty for excess material that does not invalidate the answer. Any formulation communicating the required information is accepted.']
                if level in record.get('generalRules',{}):
                    rules=[rules[0]]+record['generalRules'][level]
                    for rule in record['generalRules'][level]:assert norm(rule) in norm(scheme[general_page-1].get_text())
                language_penalty=record.get('wrongLanguagePercent',{}).get(level,50)
                if language_penalty is not None:
                    assert re.search(rf'\b{language_penalty}\s*%',scheme[general_page-1].get_text())
                    scope='whole test or whole section' if level=='hl' else record.get('ordinaryWrongLanguageScope','whole test')
                    rules+=[f'The scheme applies a {language_penalty}% deduction to marks gained if the {scope} is answered in French. This is an aggregate penalty, outside this single-task score.']
                else:
                    assert record.get('wrongLanguageReviewNotes',{}).get(level)
                    assert not re.search(r'\d+\s*%',scheme[general_page-1].get_text())
                if level=='ol':rules+=[record.get('ordinaryAnswerRule','For a task requesting one answer, offering more than one answer earns 0 marks.')]
                if level=='ol' and record.get('ordinaryAnswerRule'):
                    assert norm(record['ordinaryAnswerRule']) in norm(scheme[general_page-1].get_text())
                for rule in record.get('additionalGeneralRules',{}).get(level,[]):
                    assert norm(rule) in norm(scheme[general_page-1].get_text())
                    rules.append(rule)
                if unit['requiredDetails']>1:rules += [f'Give {unit["requiredDetails"]} distinct details. Do not count the same information twice.']
                if unit.get('scoringRule'):
                    assert unit['scoringRule']=='higher-segment-score-applied-to-both',unit
                    assert unit['requiredDetails']==2
                    assert norm(record['specialScoringSource']) in norm(scheme[general_page-1].get_text())
                    assert unit['permittedMarks']==sorted({2*m for m in unit['segmentMarks']})
                    rules += ['Special rule for this task: score each detail using the scheme, then award the higher detail score to both segments. The task score is twice that higher score, including when the other detail earns 0.']
                rules+=unit['extraRules']
                if unit.get('choices'):rules+=['Select one answer.']
                if unit.get('answerTarget'):rules+=[f'Answer only the {unit["answerTarget"].lower()} part of this printed question. It has its own {unit["totalMarks"]}-mark allocation.']
                material=dict(kind='source-text',label=f'Section {printed_section} question sheet',title=f'Listening Section {printed_section} · original questions',pages=[unit['paperPage']],
                    attribution=f'SEC French {year} {level_name.title()} Level — © State Examinations Commission.',
                    presentationNote=f'The listening booklet’s printed page is {unit["paperPage"]+record.get("printedPageOffset",20)}; the PDF page is {unit["paperPage"]}. Listen to the recording before revealing the scheme.')
                card=dict(id=cid,subjectId='french',level=level_name,source='sec',kind='rubric',year=year,paperFileid=doc['doc']['f'].removesuffix('.pdf'),
                    section=f'L{section}',questionRef=f'{year} {level.upper()} Section {printed_section if "sectionLabels" in record else "L"+section} Q{printed_q}',questionText=unit['prompt'],stem=context,
                    totalMarks=unit['totalMarks'],topicId=tag['primary'],conceptId=f'french-listening-{tag["primary"]}',specVersion='lc-french-syllabus',
                    audioMaterial=source,sourceMaterial=material,
                    schemeCitation=f'SEC French {year} {level_name.title()} Level marking scheme, {scheme_citation_pages}; general rules p.{general_page+scheme_offset} — © State Examinations Commission.',
                    schemeRegion=dict(schemeFileid=doc['scheme']['f'],p=unit['schemePage'],r=[0,0,1,1]),
                    rubric=dict(system='french',taskRequirements=rules,answerGuide=answer_guide,
                        criteria=[dict(id='response',label='Response',maxMarks=unit['totalMarks'],permittedMarks=unit['permittedMarks'],guidance=['Use the accepted answers and partial-credit rules above.'])],
                        markingGuideNote='The score is for this printed task. Round brackets identify optional wording; accepted formulations need not repeat the scheme verbatim.'),
                    qa=dict(gates=['visual-paper-scheme-review','published-listening-tariff','complete-partial-credit','selection-review','verified-official-audio'],humanReviewedBy='agent-verified',humanReviewedAt=review['reviewedAt']))
                if unit.get('choices'):
                    card['questionChoices']=unit['choices']
                    card['questionText']+='\n'+'\n'.join(unit['choices'])
                if unit.get('answerTarget'):card['questionText']+='\nAnswer for: '+unit['answerTarget']+'.'
                cards.append(card)
                tasks.append(dict(cardId=cid,subjectId='french',level=level_name,year=year,sitting='main',paperKey='aural',lang='ev',fileid=doc['doc']['f'],n=n,parent=parent,
                    topicIds=[runtime['topics'][i][0] for i in indexes],topicId=tag['primary'],pages=[unit['paperPage']],label=f'Listening Section {printed_section} · Q{printed_q}'))
    assert len(cards)==review['expectedCards']
    (ROOT/'components/MarkBank/cards/french/listening.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n')
    write_tasks('listening',tasks)
    print(f'Wrote {len(cards)} reviewed listening tasks with verified audio and exact Atlas identities.')

if __name__=='__main__':build()
