"""Reviewed 2024 Higher reading boundaries, with complete two-page passages.

Paper PDF pages 3–7 and scheme PDF pages 18–25 were visually inspected.
This certifies the reading section only, not the complete paper or archive.
"""
from __future__ import annotations
import copy
import hashlib
import re
from pathlib import Path
import fitz
from irish_higher_routes import HASHES, compact

ROOT = Path(__file__).resolve().parents[3]
DECISION_KEYS = {'A1a','A2bi','A3a','A3bi','A3bii','A4a','A4bi','A5a','A5bi','A6b',
                 'B1a','B1bi','B3a','B4bi','B4bii','B5bii','B6b'}
# These four two-answer parts have equal, independently usable one-mark slots.
ONE_MARK_SLOTS = {'B1bi':'Sampla','B4bi':'Dúshlán','B4bii':'Cúis','B5bii':'Ceist'}


def award(key, label, marks, guidance, kind='exact', permitted=None):
    return dict(id=key,label=label,kind='award',maxMarks=marks,
                permittedMarks=permitted or list(range(marks+1)),guidanceKind=kind,
                guidance=[compact(guidance)])


def apply_reading_review(cards):
    by_id = {c['id']:c for c in cards}
    old_ids = set(by_id)
    docs=[]
    for kind,file,expected in [('exampapers','LC001ALP200IV.pdf',HASHES[2024][0]),
                               ('markingschemes','LC001ALP000IV.pdf',HASHES[2024][1])]:
        path=ROOT/f'paper-trail-corpus/{kind}/2024/{file}'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,'Source changed: repeat reading review'
        docs.append(fitz.open(path))
    paper,scheme=docs
    # Retain page offsets so every slice carries its actual cross-page extent.
    scheme_text=''; page_spans=[]
    for n in range(19,26):
        text=compact(re.sub(r'(?m)^\s*\d+\s*$', '',scheme[n-1].get_text()))+' '
        start=len(scheme_text);scheme_text+=text;page_spans.append((n,start,len(scheme_text)))
    b_start=scheme_text.index('LÉAMHTHUISCINT B (50 marc)')
    passages={'A':(0,b_start),'B':(b_start,len(scheme_text))}
    questions={}; decisions=[]; reviewed=[]; added=[]; atomic=[]
    found_decisions=set()

    def scheme_slice(start,end):
        pages=[n for n,a,b in page_spans if a<end and b>start]
        return scheme_text[start:end].strip(),pages

    def add(passage,number,part,prompt,criteria,scheme_pages,*,suffix='',slot=None,atomic_task=True):
        parent=by_id[f'irish-2024-hl-p2-reading-{passage.lower()}-q{number}']
        card=copy.deepcopy(parent)
        card.pop('additionalTopicIds',None)
        key=f'reading-{passage.lower()}-q{number}-{part}'+suffix
        identifier='irish-2024-hl-p2-'+key
        part_label={'a':'(a)','bi':'(b)(i)','bii':'(b)(ii)','b':'(b)'}[part]
        label=f'Léamhthuiscint {passage} · Ceist {number}{part_label}'
        if slot: label+=' · '+slot
        topic='irish-3-3' if number==6 and part=='a' else parent['topicId']
        marks=sum(c['maxMarks'] for c in criteria)
        text=f'{number}{part_label} {prompt}'
        instruction='Don chárta seo: '+label+'.'
        if slot:
            note=(f'Don chárta seo: tabhair freagra amháin don chuid seo ({slot.lower()}, 1 mharc).'
                  if number<6 else 'Don chárta seo: mínigh léargas amháin agus tabhair sampla cruinn as an sliocht i d’fhocail féin (6 mharc).')
            # The original complete instruction remains above the practice scope.
            text+=' '+note
            instruction=note
        card.update(id=identifier,questionRef='2024 HL Paper 2 '+label,questionText=text,
                    totalMarks=marks,topicId=topic,conceptId='irish-'+key,
                    criteria=copy.deepcopy(criteria),schemePage=scheme_pages[0],schemePages=scheme_pages,
                    paperPage=5 if passage=='A' else 7,paperTraceScore=1,schemeTraceScore=1,
                    reviewedAt='2026-10-07',reviewedPaperPages=[4,5] if passage=='A' else [6,7],
                    atlasQuestionId=f'R-{passage}-{number}-{part}'+suffix,
                    practiceInstruction=instruction,
                    taskRequirements=['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                                      'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.'],
                    markingGuideNote='SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. Retained whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
        if number==6 and part=='a': card['additionalTopicIds']=[parent['topicId']]
        if identifier in by_id: cards[cards.index(by_id[identifier])]=card
        else: cards.append(card)
        by_id[identifier]=card;reviewed.append(identifier);added.append(identifier)
        if atomic_task:atomic.append(identifier)
        return card

    for passage,question_page in [('A',5),('B',7)]:
        raw=compact(paper[question_page-1].get_text()).split('Ceisteanna ',1)[1]
        lo,hi=passages[passage]
        markers=list(re.finditer(r'\b([1-6])\.\s*\(a\)',scheme_text[lo:hi]))
        assert [int(m[1]) for m in markers]==list(range(1,7))
        for number in range(1,7):
            match=re.search(rf'\b{number}\.\s*\(a\)(.*?)(?=\({7 if number<6 else 15} mh?arc\))',raw)
            assert match,(passage,number,'Missing paper question')
            body=match[1]
            if number<6:
                a,rest=re.split(r'\(b\)\s*\(i\)',body,maxsplit=1)
                bi,bii=rest.split('(ii)',1)
                prompts={'a':a.strip(),'bi':bi.strip(),'bii':bii.strip()}
            else:
                a,b=body.split('(b)',1);prompts={'a':a.strip(),'b':b.strip()}
            start=lo+markers[number-1].start()
            end=lo+markers[number].start() if number<6 else hi
            block=scheme_text[start:end]
            heads=[('a',re.search(r'\(a\)',block))]
            if number<6:heads += [('bi',re.search(r'\(b\)\s*\(i\)',block)),('bii',re.search(r'\(ii\)',block))]
            else:heads += [('b',re.search(r'\(b\)',block))]
            assert all(m for _,m in heads),(passage,number,'Missing scheme part')
            members=[]
            for index,(part,head) in enumerate(heads):
                key=f'{passage}{number}{part}'
                prompt=prompts[part]
                if re.search(r'\b(roghnaigh|rogha|nó|dhá|amháin)\b',prompt,re.I):
                    assert key in DECISION_KEYS,('Unclassified raw selection',key,prompt)
                    found_decisions.add(key)
                    reason=('Two own-word supporting points depend on one shared opinion; keep the full 12-mark response.' if key=='A6b' else
                            'Two open insights, independently priced at six each; retain both one-insight practice slots and the complete response.' if key=='B6b' else
                            'Two required open answers, each priced at one mark. Add both one-mark practice slots; retain the complete two-answer part.' if key in ONE_MARK_SLOTS else
                            'A source-retrieval instruction, not a printed finite menu of different tasks. Accepted scheme answers are examples/alternatives to this same task. Two-answer three-mark allocations stay together because two marks go to the first correct answer, not a fixed printed position.')
                    if key=='B1a': reason+=' “roghnaigh” refers to the dictionary publisher’s action, not a choice offered to the candidate.'
                    decisions.append(dict(key=key,quote=prompt,reason=reason))
                substart=start+head.start()
                subend=start+heads[index+1][1].start() if index+1<len(heads) else end
                guide,scheme_pages=scheme_slice(substart,subend)
                if number<6:
                    tariff=int(re.search(r'\{(\d+) mh?arc',guide)[1])
                    assert tariff==(3 if part=='a' else 2),(key,tariff)
                    criterion=award(part,'Freagra '+{'a':'(a)','bi':'(b)(i)','bii':'(b)(ii)'}[part],tariff,guide)
                    member=add(passage,number,part,prompt,[criterion],scheme_pages,atomic_task=key not in ONE_MARK_SLOTS)
                    members.append(member)
                    if key in ONE_MARK_SLOTS:
                        assert re.search(r'1 mharc \+ 1 mharc',guide),(key,'Unverified one-mark slots')
                        for slot in [1,2]:
                            label=ONE_MARK_SLOTS[key]+f' {slot}'
                            add(passage,number,part,prompt,[award(f'{part}-{slot}',label,1,
                                'Aon fhreagra ceart don chuid seo = 1 mharc. Ní féidir an freagra céanna a áireamh faoi dhó. '+guide)],
                                scheme_pages,suffix=f'-{slot}',slot=label)
                elif part=='a':
                    assert 'gcéad mhír' in guide and 'ceart agus marc amháin' in guide
                    member=add(passage,number,part,prompt,[award('grammar','An dá mhír ghramadaí',3,guide,permitted=[0,2,3])],scheme_pages)
                    members.append(member)
                elif passage=='A':
                    assert 'Tuairim (T) = 2 mharc' in guide and '5 mharc + 5 mharc' in guide and 'Gan tuairim luaite' in guide
                    member=add(passage,number,part,prompt,[award('opinion','Tuairim agus dhá phointe tacaíochta',12,guide,'indicative')],scheme_pages)
                    members.append(member)
                else:
                    assert 'Léargas 1 (L1) = 2 mharc' in guide and 'Léargas 2 (L2) = 2 mharc' in guide
                    criteria=[award(f'insight-{slot}',f'Léargas {slot}',6,
                        f'An léargas seo = 2 mharc; míniú i d’fhocail féin le sampla cruinn = 4 mharc. Gan léargas luaite/intuigthe, ní féidir glacadh leis an sampla. '+guide,'indicative') for slot in [1,2]]
                    member=add(passage,number,part,prompt,criteria,scheme_pages,atomic_task=False)
                    members.append(member)
                    for slot in [1,2]:
                        add(passage,number,part,prompt,[criteria[slot-1]],scheme_pages,suffix=f'-{slot}',slot=f'Léargas {slot}')
            # Preserve the twelve historical whole-question IDs and text. The
            # explicit scheme replaces the former fuzzy single-page excerpt.
            parent_id=f'irish-2024-hl-p2-reading-{passage.lower()}-q{number}'
            parent=by_id[parent_id]
            parent.update(criteria=[copy.deepcopy(c) for m in members for c in m['criteria']],
                          schemePages=sorted({n for m in members for n in m['schemePages']}),
                          reviewedAt='2026-10-07',reviewedPaperPages=[4,5] if passage=='A' else [6,7],
                          atlasQuestionId=str(number+(6 if passage=='B' else 0)),
                          markingGuideNote='Retained complete printed question. Score each published part separately using these SEC allocations. Two-answer grammar is one 0/2/3 placement; opinion and insight conditions remain inside their respective response awards.')
            parent['schemePage']=parent['schemePages'][0]
            if number==6:parent['additionalTopicIds']=['irish-3-3']
            assert sum(c['maxMarks'] for c in parent['criteria'])==parent['totalMarks']
            reviewed.append(parent_id)
            questions[f'{passage}{number}']=[m['id'] for m in members]
    assert found_decisions==DECISION_KEYS,('Stale selection keys',DECISION_KEYS-found_decisions)
    assert len(added)==44 and len(set(added))==44
    assert len(atomic)==39 and sum(by_id[k]['totalMarks'] for k in atomic)==100
    assert sum(by_id[k]['totalMarks'] for k in atomic if '-reading-a-' in k)==50
    assert sum(by_id[k]['totalMarks'] for k in atomic if '-reading-b-' in k)==50
    assert old_ids <= set(by_id)
    return cards,dict(year=2024,level='higher',paperFileid='LC001ALP200IV.pdf',
                      paperSha256=HASHES[2024][0],schemeSha256=HASHES[2024][1],
                      reviewDate='2026-10-07',reviewedPaperPages=[3,4,5,6,7],reviewedSchemePages=list(range(18,26)),
                      scope='Complete reading-section boundary review only; literature and full-paper completion remain pending.',
                      selectionDecisions=decisions,cardIds=reviewed,addedCardIds=added,atomicCardIds=atomic,
                      retainedWholeQuestionMembers=questions,
                      boundaries=['30 printed (a)/(b)(i)/(b)(ii) tasks; four two-answer tasks also expose eight independent one-mark slots.',
                                  'Two grammar pairs stay whole at 3 marks: 0/2/3, with no invented fixed first/second tariff.',
                                  'A6(b) stays whole: shared opinion=2 plus supporting points=5+5; no opinion means no supporting-point credit.',
                                  'B6(b) has two independent six-mark insights and a retained complete twelve-mark response.',
                                  '39 non-overlapping atomic tasks total 100 marks. The 12 historical whole questions and five complete subparts overlap these practice tasks.'],
                      sourcePolicy='Every task includes both complete passage pages. The original full-response sixty-word guidance is retained; no per-insight word limit is invented.')
