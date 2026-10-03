import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, ArrowUpRight, Check, Search, X } from 'lucide-react';
import KobraScope from '../approved-ui-runtime';
import { Button } from '../approved-ui-runtime';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../approved-ui-runtime';
import { Artwork } from '../learning/shared';
import { StudySubjectArtwork } from '../study/StudySubjectPicker';
import { libraryTopicIds, libraryYearsLabel } from './libraryGroups';
import { markBankCurriculumMenu } from './curriculumMenu';
import { SUBJECTS, LEVEL_LABEL, levelsFor, type Level } from './deck';
import { completeListeningExercises, resolveSessionQueue } from './sessionPlanning';
import type { DeckState } from './store';
import type { SecCard } from '../../types/markBank';
import './mark-bank-library.css';

const serial = (n:number)=>String(n).padStart(2,'0');
const shortTitle = (title:string)=>title;
const unitTitle = (title:string)=>title.replace(/^(Core|Elective|Optional) Unit \d+:\s*/, '');

interface Props {
 examDate?:string|null; subjectId:string; level:Level; cards:SecCard[]; state:DeckState; now:()=>number;
 chooseSubject:(id:string)=>void; chooseLevel:(level:Level)=>void; canSelectSubject:(name:string)=>boolean;
 onStart:(topicId?:string,queue?:SecCard[])=>void; busy:boolean; ready:boolean; loading:boolean; error:boolean; onRetry:()=>void; online:boolean;
}
export default function MarkBankLibrary({examDate,subjectId,level,cards,state,now,chooseSubject,chooseLevel,canSelectSubject,onStart,busy,ready,loading,error,onRetry,online}:Props){
 const base=SUBJECTS.find(item=>item.id===subjectId) ?? SUBJECTS[0];
 const menu=useMemo(()=>markBankCurriculumMenu(subjectId,level,examDate,cards),[subjectId,level,examDate,cards]);
 const groups=menu.strands;
 const cardsByTopic=useMemo(()=>{
   const grouped=new Map<string,SecCard[]>();
   for(const card of cards)for(const id of libraryTopicIds(card,menu.spec)){const list=grouped.get(id) ?? [];list.push(card);grouped.set(id,list);}
   return grouped;
 },[cards,menu.spec]);
 const subject={...base,groups};
 const availableSubjects=SUBJECTS.filter(item=>canSelectSubject(item.title));
 const subjectLevels=levelsFor(subjectId);
 const [groupId,setGroupId]=useState(groups.find(g=>g.topics.some(t=>cardsByTopic.has(t.id)))?.id ?? groups[0]?.id ?? '');
 const [selectedId,setSelectedId]=useState(groups.flatMap(g=>g.topics).find(t=>cardsByTopic.has(t.id))?.id ?? groups[0]?.topics[0]?.id ?? '');
 const [query,setQuery]=useState(''); const [availableOnly,setAvailableOnly]=useState(false); const [amount,setAmount]=useState(6);
 const searchRef=useRef<HTMLInputElement>(null); const detailRef=useRef<HTMLElement>(null);
 const allTopics=useMemo(()=>groups.flatMap(group=>group.topics.map(topic=>({...topic,group}))),[groups]);
 const group=groups.find(item=>item.id===groupId) ?? groups[0];
 const selected=allTopics.find(item=>item.id===selectedId) ?? allTopics[0];
 const deck=useMemo(()=>({topics:allTopics.map(topic=>{const list=cardsByTopic.get(topic.id) ?? [];return {id:topic.id,count:list.length,years:[...new Set(list.map(c=>c.year))].sort()};})}),[allTopics,cardsByTopic]);
 const selectedCards=useMemo(()=>cardsByTopic.get(selected?.id ?? '') ?? [],[cardsByTopic,selected?.id]);
 const selectedData=deck.topics.find(item=>item.id===selected?.id) ?? {count:0,years:[]};
 const activeTopics=deck.topics.filter(item=>item.count>0).length;
 const groupCount=new Set((group?.topics ?? []).flatMap(topic=>(cardsByTopic.get(topic.id) ?? []).map(card=>card.id))).size;
 const visible=(query.trim()?allTopics:allTopics.filter(item=>item.group.id===group?.id)).filter(topic=>(!availableOnly || (deck.topics.find(d=>d.id===topic.id)?.count ?? 0)>0) && `${topic.title} ${topic.group.title}`.toLowerCase().includes(query.trim().toLowerCase()));
 const queue=resolveSessionQueue(selectedCards,state.cards,now(),state.examTs,amount);
 useEffect(()=>{const handler=(event:KeyboardEvent)=>{if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==='k'){event.preventDefault();searchRef.current?.focus();}};window.addEventListener('keydown',handler);return ()=>window.removeEventListener('keydown',handler);},[]);
 function chooseTopic(id:string){setSelectedId(id);setAmount(6);if(window.innerWidth<1100)requestAnimationFrame(()=>detailRef.current?.scrollIntoView({block:'start',behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));}
 function begin(index?:number){if(!ready||busy)return; const seed=index===undefined?queue:completeListeningExercises([selectedCards[index],...queue,...selectedCards],selectedCards,amount);onStart(selected.id,seed);}
 if(!group || !selected)return <p>No topics are available for this subject.</p>;
 return <KobraScope className="mb-live-route"><main className="mb-library" aria-busy={busy || loading}>
      <header className="mb-masthead">
        <div><p className="mb-kicker">THE PRACTICE LIBRARY</p><h1>The Mark <em>Bank.</em></h1><p className="mb-intro">Real questions. Your own answers. The marks behind them.</p></div>
        <div className="mb-masthead-aside"><Artwork src="/assets/tools/mark-bank.png" size={94}/><span>ONE QUESTION<br/>AT A TIME.</span></div>
      </header>
      <div className="mb-toolbar">
        <div className="mb-subject-control"><span className="mb-kicker">YOUR SUBJECT</span><Select value={subjectId} items={availableSubjects.map(s => ({value:s.id,label:s.title}))} onValueChange={value => value && chooseSubject(value)}><SelectTrigger aria-label="Choose subject"><SelectValue/></SelectTrigger><SelectContent align="start" alignItemWithTrigger={false}>{availableSubjects.map(s => <SelectItem key={s.id} value={s.id}>{s.title}</SelectItem>)}</SelectContent></Select></div>
        <div className="mb-level-control"><span className="mb-kicker">PAPER LEVEL</span><div role="group" aria-label="Paper level">{subjectLevels.map(value => <button key={value} aria-pressed={level === value} onClick={() => chooseLevel(value)}>{LEVEL_LABEL[value]}</button>)}</div></div>
        <label className="mb-search"><Search size={19}/><input data-slot="input" ref={searchRef} placeholder={`Search ${subject.title.toLowerCase()} topics…`} aria-label="Search topics" value={query} onChange={event => setQuery(event.target.value)}/>{query ? <button type="button" onClick={() => setQuery('')} aria-label="Clear search"><X size={17}/></button> : <kbd>⌘ K</kbd>}</label>
      </div>
      <p className="mb-source-note">{menu.current ? `Your syllabus: ${menu.spec?.title}.` : "Your cohort map is being verified."} Questions retain their original paper year. Archived topics are labelled in the index.</p>
      {loading && <p role="status">Loading this question bank…</p>}
      {error && <div role="alert"><p>The questions could not be loaded.</p><Button variant="outline" onClick={onRetry}>Try again</Button></div>}
      {!online && <p className="mb-source-note">You’re offline. Reviews save on this device and sync when your connection returns.</p>}
      <div className="mb-layout">
        <aside className="mb-contents"><div className="mb-contents-title"><p className="mb-kicker">THE SUBJECT INDEX</p><span>{serial(subject.groups.length)}</span></div><nav aria-label="Subject units">{subject.groups.map((item, index) => <button key={item.id} onClick={() => {setGroupId(item.id);setQuery('');setSelectedId(item.topics.find(topic => deck.topics.some(data => data.id === topic.id && data.count > 0))?.id ?? item.topics[0].id);setAmount(6);}} aria-current={!query && group.id === item.id ? 'true' : undefined}><span>{serial(index + 1)}</span><strong>{unitTitle(item.title)}{item.label === "Original paper topics" && <small className="mb-archive-label">Original paper topics</small>}</strong>{group.id === item.id && !query && <ArrowRight size={15}/>}</button>)}</nav><div className="mb-index-note"><StudySubjectArtwork subject={subject.title} size={66}/><p><strong>{cards.length.toLocaleString()} questions</strong><span>Across {activeTopics} topics</span></p></div></aside>
        <section className="mb-topics" aria-labelledby="mb-topics-heading">
          <div className="mb-section-heading"><p className="mb-kicker">{query ? 'SEARCH THE BANK' : `${serial(subject.groups.findIndex(item=>item.id===group.id)+1)} / ${group.label || 'SUBJECT UNIT'}`}</p><h2 id="mb-topics-heading">{query ? `Results for “${query}”` : unitTitle(group.title)}</h2><div><span>{query ? `${visible.length} matching topics` : `${group.topics.length} topics · ${groupCount} questions`}</span><button className="mb-availability" aria-pressed={availableOnly} onClick={() => setAvailableOnly(!availableOnly)}><span aria-hidden="true">{availableOnly && <Check size={12}/>}</span>Available only</button></div></div>
          <div className="mb-topic-list">{visible.map(topic => { const data = deck.topics.find(item => item.id === topic.id)!; return <div className="mb-topic-entry" key={topic.id}><button className="mb-topic-row" aria-pressed={selected.id === topic.id} onClick={() => chooseTopic(topic.id)}><span className="mb-topic-code">{topic.code || topic.id.split('-').slice(-2).join('.')}</span><span className="mb-topic-copy"><strong>{shortTitle(topic.title)}</strong><small>{data.count > 0 ? `${data.count} ${data.count === 1 ? 'question' : 'questions'}${data.years.length ? ` · ${libraryYearsLabel(data.years)}` : ''}` : 'No questions in this corpus'}</small></span><ArrowUpRight size={20}/></button></div>})}</div>
          {!visible.length && <div className="mb-empty"><h3>No topics found.</h3><p>Try a different phrase or show every topic.</p><Button variant="outline" onClick={() => {setQuery('');setAvailableOnly(false);}}>Reset filters</Button></div>}
          <p className="mb-source-note">Question counts include distinct answer routes. Examination material © State Examinations Commission.</p>
        </section>
        <aside className="mb-practice" ref={detailRef} aria-label="Selected topic"><div className="mb-practice-paper"><p className="mb-kicker">{subject.title} / {LEVEL_LABEL[level]}</p><h2>{shortTitle(selected.title)}</h2><div className="mb-file-facts"><div><strong>{selectedCards.length}</strong><span>{selectedCards.length === 1 ? 'question to explore' : 'questions to explore'}</span></div><div><strong>{selectedData.years.length || '—'}</strong><span>{selectedData.years.length === 1 ? 'exam year' : 'exam years'}</span></div></div>{selectedCards.length > 0 ? <><div className="mb-size-picker"><label>A little practice</label><div role="group" aria-label="Questions per practice">{[...new Set([3,6,12].map(n => Math.min(n,selectedCards.length)))].map(n => <button aria-label={`${n} questions`} aria-pressed={Math.min(amount, selectedCards.length) === n} key={n} onClick={() => setAmount(n)}>{n}<span> questions</span></button>)}</div></div><Button className="mb-start" disabled={busy || !ready} onClick={() => begin()}>Start {queue.length} {queue.length === 1 ? 'question' : 'questions'} <ArrowRight size={18}/></Button><p className="mb-start-note">Write an answer. Then open the scheme.</p><div className="mb-in-file"><p className="mb-kicker">INSIDE THIS TOPIC</p>{selectedCards.slice(0,3).map((sample, index) => <button key={sample.id} onClick={() => begin(index)}><span><strong>{sample.stem || selected.title}</strong><small>{sample.questionRef}</small></span><span>{sample.totalMarks}<small>marks</small></span></button>)}</div></> : <div className="mb-empty-topic"><p>No questions are available for this topic in the current corpus.</p><p>You can still explore the rest of the subject index.</p></div>}</div></aside>
      </div>

    </main></KobraScope>;
}
