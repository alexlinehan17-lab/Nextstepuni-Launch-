import React,{useState} from 'react';
import {createRoot} from 'react-dom/client';
import '../../index.css';
import Subjects from '../../components/landing/sections/Subjects';
import StudySessionFinish from '../../components/study/StudySessionFinish';
import StudyBreak from '../../components/study/StudyBreak';
import AchievementGallery from '../../components/AchievementGallery';
import CrewEmptyState from '../../components/CrewEmptyState';
import StudentHomeContent from '../../components/StudentHomeContent';
function Review(){
const initial=new URLSearchParams(location.search).get('screen')||'Subjects';
const [screen,setScreen]=useState(initial),[mode,setMode]=useState<'quick'|'full'>('quick'),[phone,setPhone]=useState(false),[saved,setSaved]=useState(false);
const embedded=new URLSearchParams(location.search).has('embedded');
return <>{!embedded&&<header id="reviewbar"><strong>nextstepuni</strong><nav>{['Subjects','Welcome','Receipt','Achievements','Empty states','Break'].map(name=><button aria-pressed={screen===name} onClick={()=>{setScreen(name);setSaved(false)}} key={name}>{name}</button>)}</nav><button onClick={()=>setPhone(!phone)}>{phone?'Desktop view':'Phone view'}</button></header>}
<div id="reviewframe" className={phone?'phone':''}>{phone?<iframe title="Phone preview" src={'?embedded=1&screen='+encodeURIComponent(screen)}/>:<>
{screen==='Subjects'&&<Subjects/>}
{screen==='Welcome'&&<StudentHomeContent userName="Aoife" userAvatarSeed="star-crew:maker" allCourses={[]} userProgress={{}} categoryTitles={{}} onSelectModule={()=>{}} onGoToModules={()=>{}} onGoToDashboard={()=>{}} onGoToLearningPaths={()=>{}} onGoToJourney={()=>{}} onGoToInnovationZone={()=>{}} onGoToStudy={()=>setScreen('Break')}/>}
{screen==='Receipt'&&(saved?<CrewEmptyState character="star-crew:hugger" title="Session preview complete." action="View receipt again" onAction={()=>setSaved(false)}>This preview hasn’t saved any activity to an account.</CrewEmptyState>:<StudySessionFinish subject="Irish" elapsedSeconds={1500} plannedSeconds={1500} practice="Revision" character="star-crew:stargazer" strategies={['Active Recall']} basePoints={20} isSaving={false} mode={mode} onModeChange={setMode} onSave={async()=>setSaved(true)} onSkip={async()=>setSaved(true)}/>)}
{screen==='Achievements'&&<div style={{maxWidth:1050,margin:'auto',padding:'50px 25px'}}><AchievementGallery unlockedAchievements={['first-step','first-module','getting-started']} achievementTimestamps={{'first-step':Date.now()-86400000,'first-module':Date.now()}}/></div>}
{screen==='Empty states'&&<div style={{maxWidth:900,margin:'40px auto',padding:'0 25px'}}><CrewEmptyState title="A little room for a plan." action="Choose your subjects" onAction={()=>setScreen('Subjects')}>Start with your subjects. We’ll help you shape a week with time to study, revisit and rest.</CrewEmptyState><hr/><CrewEmptyState character="star-crew:stargazer" eyebrow="Your possibilities" title="Nothing pinned. Plenty possible." action="Explore careers" onAction={()=>setScreen('Welcome')}>Something catch your eye? Save it to your shortlist. You don’t have to have it all figured out.</CrewEmptyState></div>}
{screen==='Break'&&<StudyBreak subject="Irish" elapsedSeconds={620} onResume={()=>setScreen('Welcome')} onLeave={()=>setScreen('Receipt')}/>}
</>}</div></>}
createRoot(document.getElementById('root')!).render(<Review/>);
