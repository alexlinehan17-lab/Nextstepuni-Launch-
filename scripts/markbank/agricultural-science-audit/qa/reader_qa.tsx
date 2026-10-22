// Agricultural Science reader QA page: the production VaultQuestionCard, Viewer and SessionScreen
// against the local SEC PDFs, for the cases listed in qa-cases.json. Served by vite.qa.config.ts.
import React,{useState} from 'react';
import {createRoot} from 'react-dom/client';
import '/index.css';
import VaultQuestionCard from '../../../../components/PaperTrail/VaultQuestionCard';
import atlas from '../../../../data/examTopics/agricultural-science-question-runtime.json';
import Viewer from '../../../../components/PaperTrail/Viewer';
import SessionScreen from '../../../../components/MarkBank/SessionScreen';
import {CARDS as higher} from '../../../../components/MarkBank/cards/agricultural-science/higher';
import {CARDS as ordinary} from '../../../../components/MarkBank/cards/agricultural-science/ordinary';
const originalFetch=window.fetch.bind(window);
window.fetch=async(input,init)=>{
 const url=typeof input==='string'?input:input instanceof URL?input.href:input.url;
 const decoded=decodeURIComponent(url);
 const match=decoded.match(/(20\d\d)\/(paper|scheme)\/(LC024[AG]LP000[EI]V.pdf)/);
 if(match) return originalFetch('/paper-trail-corpus/'+(match[2]==='paper'?'exampapers':'markingschemes')+'/'+match[1]+'/'+match[3],init);
 if(decoded.includes('firebasestorage.googleapis.com')&&decoded.includes('answers')) return new Response('',{status:404});
 return originalFetch(input,init);
};
import cases from './qa-cases.json';
function App(){
 const [id,setId]=useState(cases[0]),[saved,setSaved]=useState(false),[view,setView]=useState<'atlas'|'reader'|'bank'>('atlas');
 const translated=id.includes('2010')||new URLSearchParams(location.search).get('lang')==='iv';
 const join=(translated?atlas.translatedMarkBankCards:atlas.markBankCards).find(j=>j.cardId===id)!;
 const card=[...higher,...ordinary].find(c=>c.id===id)!;
 const sibling={subjectId:'agricultural-science',year:card.year,level:card.level,lang:translated?'iv' as const:'ev' as const,fileid:join.fileid,paperKey:'single',n:join.n};
 if(view==='bank')return <SessionScreen cards={[card]} subjectLabel="Agricultural Science" onGrade={()=>{}} onExit={()=>setView('atlas')} onFinish={()=>setView('atlas')}/>;
 return <main style={{padding:16,background:'#faf8f5',minHeight:'100vh'}}><nav style={{display:'flex',flexWrap:'wrap',gap:12,marginBottom:16}}><select style={{maxWidth:'100%'}} aria-label="Question" value={id} onChange={e=>setId(e.target.value)}>{cases.map(c=><option key={c}>{c}</option>)}</select><button onClick={()=>setView('bank')}>Mark Bank</button></nav><section style={{width:860,maxWidth:'100%'}} key={id}><VaultQuestionCard sibling={sibling} saved={saved} onToggleReview={()=>setSaved(!saved)} onOpenInPaper={()=>setView('reader')}/></section>{view==='reader'&&<Viewer title="Agricultural Science" paper={{url:`/paper-trail-corpus/exampapers/${card.year}/${join.fileid}`,label:'Paper',bytes:0}} scheme={{url:`/paper-trail-corpus/markingschemes/${card.year}/${join.fileid}`,label:'Marking scheme',bytes:0}} initialPaperPage={card.sourceMaterial?.pages[0]} answersUrl={`/paper-answers/${card.year}/${join.fileid}.json`} focusQuestion={join.n} onClose={()=>setView('atlas')}/>}</main>;
}
createRoot(document.getElementById('root')!).render(<App/>);
