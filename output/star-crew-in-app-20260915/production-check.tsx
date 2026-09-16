import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import LoginPage from '../../components/LoginPage';
import Onboarding from '../../components/Onboarding';
import HomeNextStep from '../../components/HomeNextStep';
import StudySessionSetup from '../../components/study/StudySessionSetup';
import { initialDraft, draftKey } from '../../components/onboarding/model';
import '../../index.css';
const params = new URLSearchParams(location.search);
const page = params.get('page') || 'account';
const step = page === 'grades' ? 'grades' : 'subjects';
if (page === 'subjects' || page === 'grades') localStorage.setItem(draftKey('star-crew-ui-qa', 'fresh'), JSON.stringify({...initialDraft(), step, year:'6th', subjects:['English','Irish','Mathematics'], configs:{English:{level:'higher',current:'H3',target:'H1',reviewed:true},Irish:{level:'higher',current:'H3',target:'H1',reviewed:true},Mathematics:{level:'higher',current:'H3',target:'H1',reviewed:true}}}));
function Study() {
 const [subject,setSubject] = useState('Irish');
 return <StudySessionSetup subjects={['Politics & Society','Geography','Mathematics','Applied Maths','English','Irish','Accounting'].map(subjectName=>({subjectName,level:'higher'}))} selectedSubject={subject} onSubject={setSubject} selectedType="practice" onType={()=>{}} selectedMinutes={25} onMinutes={()=>{}} todayBlocks={[]} onBlock={()=>{}} sessionCount={0} todayMinutes={0} reflectionCount={0} onReflections={()=>{}} onBack={()=>{}} onStart={()=>{}} canStart startHint={null}/>;
}
createRoot(document.getElementById('production-check')!).render(params.has('mobile') ? <iframe data-app-preview="mobile" title="Mobile production components" src={`production-check.html?page=${page}`} style={{display:'block',width:390,height:900,border:'1px solid #ddd',margin:'20px auto'}}/> : page === 'account' ? <LoginPage handleLoginSuccess={()=>{}}/> : page === 'study' ? <Study/> : page === 'home' ? <HomeNextStep blocks={[{subjectName:'Irish',sessionType:'revision',durationMinutes:25},{subjectName:'Music',sessionType:'practice',durationMinutes:20}]} completions={[]} hasProfile onProgress={()=>{}} onStudy={()=>{}}/> : <Onboarding userId="star-crew-ui-qa" userName="Aoife" onComplete={()=>{}} onSkip={()=>{}}/>);
