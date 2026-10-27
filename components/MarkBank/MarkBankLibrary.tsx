/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Mark Bank library on Kobra: subject Select, level Tabs, a Kobra Input
 * search with the ⌘K hint, an "Available only" Checkbox, the subject index
 * with ink markers, hairline topic rows (the chosen one in an ink ring) and
 * the practice card with a ToggleGroup for its size. Loading draws a local
 * skeleton (the runtime has no Skeleton); a failed load is an Alert with a
 * retry. Props and the session wiring are MarkBank.tsx's, unchanged.
 */

import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, ArrowUpRight, RotateCcw, Search, X } from 'lucide-react';
import KobraScope, {
  Alert, AlertAction, AlertTitle, Button, Checkbox, Input, Kbd,
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
  Tabs, TabsList, TabsTrigger, ToggleGroup, ToggleGroupItem,
} from '../approved-ui-runtime';
import ThemeArtwork from '../ThemeArtwork';
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

/** MarkBank keys this screen by deck, so a new subject or level mounts a new
 * instance. The control that made the change is focused again on it, so a
 * keyboard user is not dropped back to the top of the page. */
let refocusAfterRemount: { control: 'subject' | 'level'; at: number } | null = null;

const Mark = () => <span className="mb-mark" aria-hidden="true"><span /></span>;
const Skeleton = ({ className = '' }: { className?: string }) => <span className={`mb-skeleton ${className}`} aria-hidden="true" />;

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
 const subjectRef=useRef<HTMLDivElement>(null); const levelRef=useRef<HTMLDivElement>(null);
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
 const sizes=[...new Set([3,6,12].map(n=>Math.min(n,selectedCards.length)))];
 const failed=error && !loading;
 const settled=!loading && !failed;
 useEffect(()=>{const handler=(event:KeyboardEvent)=>{if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==='k'){event.preventDefault();searchRef.current?.focus();}};window.addEventListener('keydown',handler);return ()=>window.removeEventListener('keydown',handler);},[]);
 useEffect(()=>{
   const pending=refocusAfterRemount; refocusAfterRemount=null;
   if(!pending || Date.now()-pending.at>1500)return;
   const target=pending.control==='level'
     ? levelRef.current?.querySelector<HTMLElement>('[data-slot=tabs-trigger][aria-selected=true]')
     : subjectRef.current?.querySelector<HTMLElement>('[data-slot=select-trigger]');
   target?.focus();
 },[]);
 function pickSubject(id:string){if(id===subjectId)return;refocusAfterRemount={control:'subject',at:Date.now()};chooseSubject(id);}
 function pickLevel(next:Level){if(next===level)return;refocusAfterRemount={control:'level',at:Date.now()};chooseLevel(next);}
 function chooseTopic(id:string){setSelectedId(id);setAmount(6);if(window.innerWidth<1100)requestAnimationFrame(()=>detailRef.current?.scrollIntoView({block:'start',behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));}
 function begin(index?:number){if(!ready||busy)return; const seed=index===undefined?queue:completeListeningExercises([selectedCards[index],...queue,...selectedCards],selectedCards,amount);onStart(selected.id,seed);}
 if(settled && (!group || !selected))return <p>No topics are available for this subject.</p>;
 return <KobraScope className="mb-live-route"><main className="mb-library" aria-busy={busy || loading}>
      <header className="mb-masthead">
        <div>
          <p className="mb-kicker mb-masthead-kicker">THE PRACTICE LIBRARY</p>
          <h1>The Mark <em>Bank.</em></h1>
          <p className="mb-intro">Flashcards made from real exam questions. Answer, check the marks, and each one comes back just before you’d forget it.</p>
        </div>
        <div className="mb-masthead-aside"><ThemeArtwork src="/assets/tools/mark-bank.png" alt="" width={94} height={94} className="mb-masthead-art"/><span>ONE QUESTION<br/>AT A TIME.</span></div>
      </header>

      <div className="mb-toolbar">
        <div className="mb-field" ref={subjectRef}>
          <span className="mb-kicker">YOUR SUBJECT</span>
          <Select value={subjectId} items={availableSubjects.map(s => ({value:s.id,label:s.title}))} onValueChange={value => value && pickSubject(value)}>
            <SelectTrigger aria-label="Choose subject"><SelectValue/></SelectTrigger>
            <SelectContent align="start" alignItemWithTrigger={false}>{availableSubjects.map(s => <SelectItem key={s.id} value={s.id}>{s.title}</SelectItem>)}</SelectContent>
          </Select>
        </div>
        <div className="mb-field mb-level" ref={levelRef}>
          <span className="mb-kicker">PAPER LEVEL</span>
          <Tabs value={level} onValueChange={value => pickLevel(value as Level)}>
            <TabsList aria-label="Paper level">{subjectLevels.map(value => <TabsTrigger key={value} value={value}>{LEVEL_LABEL[value]}</TabsTrigger>)}</TabsList>
          </Tabs>
        </div>
        <div className="mb-search">
          <Search className="mb-search-icon" aria-hidden="true"/>
          <Input ref={searchRef} placeholder={`Search ${subject.title.toLowerCase()} topics…`} aria-label="Search topics" aria-keyshortcuts="Meta+K Control+K" autoComplete="off" value={query} onChange={event => setQuery(event.target.value)}/>
          {query
            ? <Button variant="ghost" size="icon-sm" className="mb-search-clear" aria-label="Clear search" onClick={() => {setQuery('');searchRef.current?.focus();}}><X aria-hidden="true"/></Button>
            : <Kbd className="mb-search-kbd" aria-hidden="true">⌘ K</Kbd>}
        </div>
      </div>
      <p className="mb-source-note">{menu.current ? `Your syllabus: ${menu.spec?.title}.` : "Your cohort map is being verified."} Questions retain their original paper year. Archived topics are labelled in the index.</p>
      {loading && <p className="mb-sr" role="status">Loading this question bank…</p>}
      {!online && <p className="mb-source-note">You’re offline. Reviews save on this device and sync when your connection returns.</p>}

      <div className="mb-layout">
        <aside className="mb-contents" aria-label="The subject index">
          <div className="mb-contents-title"><p className="mb-kicker">THE SUBJECT INDEX</p>{groups.length > 0 && <span>{serial(subject.groups.length)}</span>}</div>
          {groups.length > 0
            ? <nav className="mb-index-list" aria-label="Subject units">{subject.groups.map((item, index) => <button type="button" className="mb-index-row" key={item.id} onClick={() => {setGroupId(item.id);setQuery('');setSelectedId(item.topics.find(topic => deck.topics.some(data => data.id === topic.id && data.count > 0))?.id ?? item.topics[0].id);setAmount(6);}} aria-current={!query && group?.id === item.id ? 'true' : undefined}><Mark/><span className="mb-serial">{serial(index + 1)}</span><span className="mb-index-title">{unitTitle(item.title)}{item.label === "Original paper topics" && <small className="mb-archive-label">Original paper topics</small>}</span></button>)}</nav>
            : <div className="mb-index-list" aria-hidden="true">{[0,1,2,3].map(row => <div className="mb-index-row mb-index-row-skeleton" key={row}><Skeleton className="mb-skeleton-mark"/><Skeleton className="mb-skeleton-serial"/><Skeleton className="mb-skeleton-line"/></div>)}</div>}
          {settled && <p className="mb-index-note"><strong>{cards.length.toLocaleString()} questions</strong><span>Across {activeTopics} topics</span></p>}
        </aside>

        <section className="mb-topics" aria-labelledby={group ? 'mb-topics-heading' : undefined}>
          {group
            ? <div className="mb-section-heading">
                <p className="mb-kicker">{query ? 'SEARCH THE BANK' : `${serial(subject.groups.findIndex(item=>item.id===group.id)+1)} / ${group.label || 'SUBJECT UNIT'}`}</p>
                <h2 id="mb-topics-heading">{query ? `Results for “${query}”` : unitTitle(group.title)}</h2>
                <div className="mb-section-meta">
                  <span>{query ? `${visible.length} matching topics` : settled ? `${group.topics.length} topics · ${groupCount} questions` : `${group.topics.length} topics`}</span>
                  <label className="mb-availability"><Checkbox checked={availableOnly} disabled={!settled} onCheckedChange={checked => setAvailableOnly(Boolean(checked))}/>Available only</label>
                </div>
              </div>
            : <div className="mb-section-heading mb-section-heading-skeleton" aria-hidden="true"><Skeleton className="mb-skeleton-short"/><Skeleton className="mb-skeleton-title"/></div>}

          {loading && <ul className="mb-topic-list" aria-hidden="true">{[0,1,2].map(row => <li key={row}><div className="mb-topic-row mb-topic-row-skeleton"><Skeleton className="mb-skeleton-code"/><span className="mb-topic-copy"><Skeleton className="mb-skeleton-line"/><Skeleton className="mb-skeleton-short"/></span></div></li>)}</ul>}

          {failed && <Alert variant="error" className="mb-error">
            <AlertTitle>The questions could not be loaded.</AlertTitle>
            <AlertAction><Button variant="outline" className="nsu-ink-outline" onClick={onRetry}><RotateCcw aria-hidden="true"/>Try again</Button></AlertAction>
          </Alert>}

          {settled && selected && <>
            {visible.length > 0 && <ul className="mb-topic-list">{visible.map(topic => { const data = deck.topics.find(item => item.id === topic.id)!; return <li key={topic.id}><button type="button" className="mb-topic-row" aria-pressed={selected.id === topic.id} onClick={() => chooseTopic(topic.id)}><span className="mb-topic-code">{topic.code || topic.id.split('-').slice(-2).join('.')}</span><span className="mb-topic-copy"><strong>{shortTitle(topic.title)}</strong><small>{data.count > 0 ? `${data.count} ${data.count === 1 ? 'question' : 'questions'}${data.years.length ? ` · ${libraryYearsLabel(data.years)}` : ''}` : 'No questions in this corpus'}</small></span><ArrowUpRight className="mb-topic-arrow" aria-hidden="true"/></button></li>;})}</ul>}
            {!visible.length && <div className="mb-empty"><h3>No topics found.</h3><p>Try a different phrase or show every topic.</p><Button variant="outline" className="nsu-ink-outline" onClick={() => {setQuery('');setAvailableOnly(false);}}>Reset filters</Button></div>}
          </>}
          <p className="mb-source-note">Question counts include distinct answer routes. Examination material © State Examinations Commission.</p>
        </section>

        {!failed && <aside className="mb-practice" ref={detailRef} aria-label="Selected topic"><div className="mb-practice-paper nsu-paper-card">
          {loading || !selected
            ? <div className="mb-practice-skeleton" aria-hidden="true"><Skeleton className="mb-skeleton-short"/><Skeleton className="mb-skeleton-title"/><Skeleton className="mb-skeleton-title mb-skeleton-title-end"/><span className="mb-practice-skeleton-facts"><Skeleton className="mb-skeleton-figure"/><Skeleton className="mb-skeleton-figure"/></span><Skeleton className="mb-skeleton-button"/></div>
            : <>
              <p className="mb-kicker">{subject.title} / {LEVEL_LABEL[level]}</p>
              <h2>{shortTitle(selected.title)}</h2>
              <dl className="mb-file-facts">
                <div><dt>{selectedCards.length === 1 ? 'question to explore' : 'questions to explore'}</dt><dd>{selectedCards.length}</dd></div>
                <div><dt>{selectedData.years.length === 1 ? 'exam year' : 'exam years'}</dt><dd>{selectedData.years.length || '—'}</dd></div>
              </dl>
              {selectedCards.length > 0 ? <>
                <p className="mb-size-label">A little practice</p>
                <ToggleGroup className="mb-size" variant="outline" aria-label="Questions per practice" value={[String(Math.min(amount, selectedCards.length))]} onValueChange={values => {if(values[0])setAmount(Number(values[0]));}}>
                  {sizes.map(n => <ToggleGroupItem key={n} value={String(n)} aria-label={`${n} questions`}>{n}</ToggleGroupItem>)}
                </ToggleGroup>
                <Button className="mb-start" disabled={busy || !ready} onClick={() => begin()}>Start {queue.length} {queue.length === 1 ? 'question' : 'questions'}<ArrowRight aria-hidden="true"/></Button>
                <p className="mb-start-note">Write an answer. Then open the scheme.</p>
                <div className="mb-in-file">
                  <p className="mb-kicker">INSIDE THIS TOPIC</p>
                  <ul>{selectedCards.slice(0,3).map((sample, index) => <li key={sample.id}><button type="button" className="mb-sample" onClick={() => begin(index)}><span className="mb-sample-copy"><strong>{sample.stem || selected.title}</strong><small>{sample.questionRef}</small></span><span className="mb-sample-marks">{sample.totalMarks}<small>marks</small></span></button></li>)}</ul>
                </div>
              </> : <div className="mb-empty-topic"><p>No questions are available for this topic in the current corpus.</p><p>You can still explore the rest of the subject index.</p></div>}
            </>}
        </div></aside>}
      </div>
    </main></KobraScope>;
}
