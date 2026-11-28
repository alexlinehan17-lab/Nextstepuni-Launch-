import React, { useEffect, useState } from 'react';
import { BookOpen, Check, ChevronLeft, FileText, Plus, RotateCcw, X } from 'lucide-react';
import { Arrow, Button, Glyph, TextButton } from '../ui/Button';
import { Sheet } from '../ui/Sheet';
import { ChoiceTile, SelectionBar } from '../ui/Choice';
import { AreaField, Field } from '../ui/Field';
import { PressBox } from '../ui/List';
import { courseworkBrief } from '../../data/curriculum/coursework';
import { courseworkResources, scopePrompts, type CourseworkResource, type ResourceStage } from '../../data/curriculum/courseworkResources';
import { activeEvidence, newId, today, type CourseworkProject, type Evidence, type Milestone } from './model';
import { emptySupport, feedbackRecords, newFeedback, newPractice, newRestart, upsert, type EvidenceRole, type FeedbackDraft, type PracticeDraft, type PressureDraft, type ResourceDraft, type RestartDraft, type SupportDrafts } from './supportState';
import { practiceEvidence } from './practiceContent';
import './coursework-activities.css';

export type SupportPanel='restart'|'pressure'|'resources'|'feedback';
export interface SupportCache { drafts:SupportDrafts; dirty:boolean }
interface Props { project:CourseworkProject; panel:SupportPanel|null; connectionId?:string; saving:boolean; error:string; cache?:SupportCache; onCache:(cache:SupportCache)=>void; onClose:()=>void; onSave:(project:CourseworkProject)=>Promise<boolean>; onNavigate:(view:'Plan'|'Evidence'|'Connections'|'Review')=>void }
/** The shared Button has no `disabled`: a button that cannot go yet says so with aria-disabled and swallows the press. */
const waitFor = (blocked: boolean) => blocked ? { 'aria-disabled': true as const, onClickCapture: (event: React.MouseEvent) => { event.preventDefault(); event.stopPropagation(); } } : {};
const titles={restart:'Find a way back in.',pressure:'Pressure-test your thinking.',resources:'The resource desk.',feedback:'Put feedback to work.'};
const descriptions={restart:'Turn a blocker into a small, concrete step for your plan.',pressure:'Use your own evidence, or learn the process with a clearly fictional example.',resources:'Help matched to your subject and examination year. Keep a takeaway with its source.',feedback:'Preserve the original comment, decide what it means, and give it a next step.'};
const ROLES:EvidenceRole[]=['Supports','Challenges','Context'];

export default function CourseworkSupport({project,panel,connectionId,saving,error,cache,onCache,onClose,onSave,onNavigate}:Props) {
  const [drafts,setDrafts]=useState<SupportDrafts>(()=>cache?.drafts??project.support?.drafts??{});
  const [dirty,setDirty]=useState(cache?.dirty??false);
  const [message,setMessage]=useState('');
  const [savedView,setSavedView]=useState<'Plan'|'Evidence'|'Connections'|'Review'|null>(null);
  const [resourceId,setResourceId]=useState('');
  const [practice,setPractice]=useState(false);
  const [target,setTarget]=useState(connectionId??project.connections[0]?.id??'');
  const catalogue=courseworkResources(project.subjectId,project.examYear);
  const resource=catalogue.find(r=>r.id===resourceId);
  const support={...emptySupport(),...project.support};
  useEffect(()=>onCache({drafts,dirty}),[drafts,dirty,onCache]);
  useEffect(()=>{if(panel){setResourceId('');setMessage('');setSavedView(null);setPractice(false);if(connectionId)setTarget(connectionId);}},[panel,connectionId]);
  const patch=(next:SupportDrafts)=>{setDrafts(next);setDirty(true);setMessage('');setSavedView(null);};
  const save=async(next:CourseworkProject,label:string,view:'Plan'|'Evidence'|'Connections'|'Review'|null=null)=>{
    const ok=await onSave(next);
    if(ok){setDirty(false);setMessage(label);setSavedView(view);}
    return ok;
  };
  const saveDrafts=()=>save({...project,support:{...support,drafts}},'Draft saved on this device.');
  const navigate=(view:'Plan'|'Evidence'|'Connections'|'Review')=>{onClose();onNavigate(view);};
  const openResource=(id:string)=>{
    const match=catalogue.find(r=>r.id===id)??catalogue.find(r=>r.kind==='Official source')??catalogue[0];
    if(!match)return;
    if(!drafts.resources?.[match.id])setDrafts(d=>({...d,resources:{...d.resources,[match.id]:{id:newId(),note:'',why:'',locator:''}}}));
    setResourceId(match.id);
  };
  const restart=drafts.restart;
  const ensureRestart=()=>{if(!drafts.restart)patch({...drafts,restart:newRestart()});};
  // Initialise editable identities once, without writing to storage until a save.
  useEffect(()=>{
    if(panel==='restart'&&!drafts.restart)setDrafts(d=>({...d,restart:newRestart()}));
    if(panel==='feedback'&&!drafts.feedback)setDrafts(d=>({...d,feedback:newFeedback()}));
  },[panel,drafts.restart,drafts.feedback]);
  const connection=project.connections.find(c=>c.id===target)??project.connections[0];
  const pd:PressureDraft=connection?(drafts.pressure?.[connection.id]??{claim:connection.claim,reasoning:connection.reasoning,limitation:connection.limitation,next:connection.pressureReview?.next??'',roles:connection.pressureReview?.roles??Object.fromEntries(connection.evidenceIds.map(id=>[id,'Context' as EvidenceRole])),withheld:''}):{claim:'',reasoning:'',limitation:'',next:'',roles:{},withheld:''};
  const updatePressure=(value:PressureDraft)=>{if(connection)patch({...drafts,pressure:{...drafts.pressure,[connection.id]:value}});};
  const title=resource?.title??(practice?'Learn with a worked example.':panel?titles[panel]:'Coursework help');
  const description=resource?.publisher??(practice?'Fictional practice only. This material never becomes evidence in your project.':panel?descriptions[panel]:'');
  const footer=(
    <div className="cw7s-foot">
      <Button {...waitFor(saving||!dirty)} onClick={()=>void saveDrafts()}>Save draft</Button>
      <span role="status" className="cw7s-status">{saving?'Saving…':message|| (dirty?'Unsaved changes · save to keep on this device.':'Your saved work stays with this project.')}</span>
      {savedView&&<TextButton arrow="forward" onClick={()=>navigate(savedView)}>View saved work</TextButton>}
    </div>
  );
  return <Sheet open={!!panel} onClose={()=>{if(!saving)onClose();}} title={title} className="cw7s" footer={footer}>
    <div className="cw7s-head">
      {description&&<p className="t-sub">{description}</p>}
      <p className="t-label cw7s-context">{courseworkBrief(project.subjectId,project.examYear)?.specification.subjectName} / {project.examYear} / {project.title}</p>
    </div>
    {error&&<p className="cw7s-error" role="alert">{error}</p>}
    <fieldset disabled={saving} className="cw7s-fields">
      {(resource||practice)&&<TextButton tone="quiet" className="cw7s-back" onClick={()=>{setResourceId('');setPractice(false);}}><Glyph icon={ChevronLeft} size={16}/>Back to {panel==='restart'?'my next step':panel==='resources'?'resources':'my connections'}</TextButton>}
      {resource?<ResourceReader resource={resource} draft={drafts.resources?.[resource.id]??{id:'',note:'',why:'',locator:''}} onChange={d=>patch({...drafts,resources:{...drafts.resources,[resource.id]:d}})} onSave={async d=>{
        const old=project.evidence.find(e=>e.id===d.id);
        const item:Evidence={id:d.id,kind:resource.url?'Source':'Reflection',title:resource.title,notes:d.note,why:d.why,author:resource.url?resource.publisher:'',locator:resource.url?d.locator:'',url:resource.url??'',quote:old?.quote??'',date:old?.date??today(),files:old?.files??[],archived:false};
        await save({...project,evidence:upsert(project.evidence,item),support:{...support,drafts}},'Takeaway saved in Evidence.','Evidence');
      }}/>:practice?<Practice value={drafts.practice??newPractice()} onChange={value=>patch({...drafts,practice:value})} onSave={async value=>{await save({...project,support:{...support,drafts,practiceReflection:{claim:value.claim,limitation:value.limitation,next:value.next,savedAt:new Date().toISOString()}}},'Practice reflection saved separately from your project evidence.');}}/>:<>
        {panel==='restart'&&(restart?<Restart project={project} onNew={()=>patch({...drafts,restart:newRestart()})} hasSaved={project.milestones.some(m=>m.id===restart.id)} value={restart} onChange={value=>patch({...drafts,restart:value})} onResource={openResource} onSave={async value=>{
          const old=project.milestones.find(m=>m.id===value.id);const b=restartOptions(project).find(o=>o.id===value.blocker)!;const steps=b.steps.slice(0,value.minutes===5?1:value.minutes===15?2:3);
          const step:Milestone={id:value.id,label:value.note.trim(),date:old?.date??'',done:steps.every((_,i)=>value.checked.includes(`${value.blocker}-${i}`)),minutes:value.minutes,setting:value.blocker==='waiting'?'With my teacher':'Anywhere',details:`${b.move}\n${steps.map((s,i)=>`${value.checked.includes(`${value.blocker}-${i}`)?'Done':'To do'}: ${s}`).join('\n')}`};
          await save({...project,milestones:upsert(project.milestones,step),support:{...support,drafts,restartHidden:false}},'Your next step is saved in Plan.','Plan');
        }}/>:<Button kind="main" onClick={ensureRestart}>Begin a small step</Button>)}
        {panel==='resources'&&<Resources catalogue={catalogue} bookmarks={support.bookmarks} subject={courseworkBrief(project.subjectId,project.examYear)?.specification.subjectName??''} year={project.examYear} onOpen={openResource} onBookmark={async id=>{await save({...project,support:{...support,drafts,bookmarks:support.bookmarks.includes(id)?support.bookmarks.filter(x=>x!==id):[...support.bookmarks,id]}},'Resource shelf saved.');}}/>}
        {panel==='pressure'&&<>
          <div className="cw7s-start"><p>Keep your evidence in view as you test a conclusion or decision. The roles are your judgement; the app does not grade the claim.</p><Button arrow="forward" onClick={()=>{setPractice(true);setMessage('');}}>Try the worked example</Button></div>
          {!connection?<p className="cw7s-empty">Create a connection from your own evidence first. You can use the worked example while you get started.</p>:<>
            <label className="ui-part ui-field cw7s-pick"><span className="ui-field-label">Connection to examine</span><select className="ui-field-input cw7s-select" value={connection.id} onChange={e=>{setTarget(e.target.value);setMessage('');}}>{project.connections.map(c=><option key={c.id} value={c.id}>{c.claim.slice(0,110)}</option>)}</select></label>
            <OwnPressure project={project} value={pd} onChange={updatePressure} onSave={async value=>{
              const activeIds=new Set(activeEvidence(project).map(e=>e.id));const selected=Object.keys(value.roles).filter(id=>activeIds.has(id));
              const revised={...connection,claim:value.claim,reasoning:value.reasoning,limitation:value.limitation,evidenceIds:selected,pressureReview:{originalClaim:connection.pressureReview?.originalClaim??connection.claim,roles:Object.fromEntries(Object.entries(value.roles).filter(([id])=>project.evidence.some(e=>e.id===id))),withheld:project.evidence.some(e=>e.id===value.withheld)?value.withheld:'',next:value.next,testedAt:new Date().toISOString()}};
              await save({...project,connections:upsert(project.connections,revised),support:{...support,drafts:{...drafts,pressure:{...drafts.pressure,[connection.id]:value}}}},'Revised connection saved. Your original claim is retained in its pressure-test record.','Connections');
            }}/>
          </>}
        </>}
        {panel==='feedback'&&drafts.feedback&&<Feedback value={drafts.feedback} onChange={value=>patch({...drafts,feedback:value})} onNew={()=>patch({...drafts,feedback:newFeedback()})} onSave={async value=>{await save({...project,...feedbackRecords(project,value,today()),support:{...support,drafts}},'Feedback saved in Evidence, with a linked next step in Plan.','Plan');}}/>}
      </>}
    </fieldset>
  </Sheet>;
}

function restartOptions(project:CourseworkProject) {
  const family=courseworkBrief(project.subjectId,project.examYear)?.family??'research';
  return [
    {id:'scope',title:'My question is too big',detail:'Everything seems connected.',move:'Make one useful boundary.',prompt:'The next action I am choosing',steps:scopePrompts[family],example:'One question, decision or relationship is enough for a first move. It can become more precise as you learn.',resource:'guide-question'},
    {id:'sources',title:'I don’t know what to trust',detail:'I have material, but not clear evidence.',move:'Give one source a closer look.',prompt:'The next action I am choosing',steps:['Choose one source and record who produced it.','Find how its information was gathered and when.','Name one thing it cannot tell you about your question.'],example:'A source can be useful without answering your whole question. Decide what it can reasonably support.',resource:'guide-sources'},
    {id:'waiting',title:'I’m waiting on my teacher',detail:'One decision is holding me up.',move:'Make the question easy to answer.',prompt:'The question or decision I need help with',steps:['Write the exact decision you need help with.','Add the brief section or evidence that caused the uncertainty.','Identify a small desk-based task you can do while waiting.'],example:'Keep work requiring permission or supervision on hold. Organising references or preparing a question can still move you forward.',resource:'official'},
    {id:'overload',title:'There is too much to do',detail:'I keep circling the whole project.',move:'Leave yourself one clear next step.',prompt:'The one action I will take next',steps:['Choose one source, paragraph or decision to work on.','Describe what “finished for today” would look like.','Write the first action for your next session.'],example:'“Find the page number for this source” is a usable next step. “Finish the project” is not.',resource:'guide-sources'},
  ];
}
function Restart({project,value,onChange,onResource,onSave,onNew,hasSaved}:{onNew:()=>void;hasSaved:boolean;project:CourseworkProject;value:RestartDraft;onChange:(v:RestartDraft)=>void;onResource:(id:string)=>void;onSave:(v:RestartDraft)=>Promise<void>}) {
  const choices=restartOptions(project),choice=choices.find(b=>b.id===value.blocker)!;const steps=choice.steps.slice(0,value.minutes===5?1:value.minutes===15?2:3),complete=steps.filter((_,i)=>value.checked.includes(`${value.blocker}-${i}`)).length;
  const pct=complete/steps.length*100;
  return <>
    <div className="cw7s-ask">
      <h3>What is getting in the way?</h3>
      <div className="cw7s-blockers" role="radiogroup" aria-label="What is getting in the way?">
        {choices.map(b=><ChoiceTile key={b.id} kind="one" label={b.title} meta={b.detail} chosen={b.id===value.blocker} onClick={()=>onChange({...value,blocker:b.id})}/>)}
      </div>
    </div>
    <div className="cw7s-budget">
      <span className="cw7s-budget-lead">I have about</span>
      <div className="cw7s-minutes" role="radiogroup" aria-label="Time available">
        {[5,15,25].map(m=><ChoiceTile key={m} compact kind="one" label={<>{m} min</>} chosen={value.minutes===m} onClick={()=>onChange({...value,minutes:m})}/>)}
      </div>
      <small className="cw7s-meta">A planning allowance, not a countdown.</small>
    </div>
    <div className="cw7s-two">
      <div className="cw7s-move">
        <div className="cw7s-titled"><p className="t-label">One manageable move</p><h3>{choice.move}</h3></div>
        <div className="cw7s-count"><span className="cw7s-meta">{complete} of {steps.length} steps</span><span className="cw7s-bar" role="progressbar" aria-label="Small-step progress" aria-valuemin={0} aria-valuemax={100} aria-valuenow={pct}><i style={{width:pct+'%'}}/></span></div>
        <div className="cw7s-checklist">
          {steps.map((s,i)=>{const key=`${value.blocker}-${i}`;const on=value.checked.includes(key);return <ChoiceTile key={s} kind="several" label={s} chosen={on} onClick={()=>onChange({...value,checked:on?value.checked.filter(k=>k!==key):[...value.checked,key]})}/>;})}
        </div>
        <AreaField label={choice.prompt} rows={3} maxLength={300} value={value.note} onChange={e=>onChange({...value,note:e.target.value})}/>
        <div className="cw7s-row">
          <Button kind="main" {...waitFor(!value.note.trim())} onClick={()=>void onSave(value)}><Glyph icon={Plus} size={16}/>Save next step to Plan</Button>
          {hasSaved&&<TextButton onClick={onNew}>Start another step</TextButton>}
        </div>
      </div>
      <aside className="cw7s-note">
        <p className="t-label">Small enough to finish</p>
        <p className="cw7s-note-text">{choice.example}</p>
        <PressBox className="cw7s-shortcut" onPress={()=>onResource(choice.resource)}><Glyph icon={BookOpen} size={20}/><span className="cw7s-shortcut-words"><strong>A little help with this</strong><small>Open the relevant guide</small></span><Arrow meaning="opens" size={20} className="cw7s-chev"/></PressBox>
        <div className="cw7s-why"><span className="t-label">Why this nudge?</span><p>You chose “{choice.title.toLowerCase()}”. The move changes with your blocker and available time.</p></div>
      </aside>
    </div>
  </>;
}

function Resources({catalogue,bookmarks,subject,year,onOpen,onBookmark}:{catalogue:CourseworkResource[];bookmarks:string[];subject:string;year:number;onOpen:(id:string)=>void;onBookmark:(id:string)=>Promise<void>}) {
  const [stage,setStage]=useState<ResourceStage>('Researching'),[onlySaved,setOnlySaved]=useState(false);
  const matches=catalogue.filter(r=>onlySaved?bookmarks.includes(r.id):r.stages.includes(stage));
  return <>
    <div className="cw7s-toolbar">
      <SelectionBar label="Project stage" size="sm" options={(['Starting','Researching','Writing'] as ResourceStage[]).map(s=>({value:s,label:s}))} value={onlySaved?'':stage} onChange={s=>{setStage(s);setOnlySaved(false);}}/>
      <Button size="sm" aria-pressed={onlySaved} onClick={()=>setOnlySaved(v=>!v)}><Glyph icon={BookOpen} size={16}/>Saved {bookmarks.filter(id=>catalogue.some(r=>r.id===id)).length}</Button>
    </div>
    <p className="cw7s-meta">{subject} · {year} · {onlySaved?'Your saved shelf':stage+'. Sources show their own checked date.'}</p>
    <div className="cw7s-list">
      {matches.map(r=><article key={r.id} className="cw7s-resource">
        <div className="cw7s-kind t-label"><Glyph icon={FileText} size={16}/><span>{r.kind}</span></div>
        <div className="cw7s-resource-main">
          <div className="cw7s-titled"><h3>{r.title}</h3><small className="cw7s-meta">{r.publisher}{r.checked?' · checked '+r.checked:''}</small></div>
          <p>{r.why}</p>
          <div className="cw7s-limits"><span className="t-label">Keep in mind</span><p>{r.limit}</p></div>
          <div className="cw7s-actions">
            <Button size="sm" onClick={()=>onOpen(r.id)}>{r.url?'Open resource notes':'Try the guide'}</Button>
            <TextButton aria-pressed={bookmarks.includes(r.id)} onClick={()=>void onBookmark(r.id)}><Glyph icon={bookmarks.includes(r.id)?Check:Plus} size={16}/>{bookmarks.includes(r.id)?'On my shelf':'Keep on my shelf'}</TextButton>
          </div>
        </div>
      </article>)}
    </div>
    {!matches.length&&<p className="cw7s-empty">Keep a useful resource from one of the stages. It will appear here.</p>}
  </>;
}
function ResourceReader({resource,draft,onChange,onSave}:{resource:CourseworkResource;draft:ResourceDraft;onChange:(d:ResourceDraft)=>void;onSave:(d:ResourceDraft)=>Promise<void>}) {
  return <div className="cw7s-reader">
    <div className="cw7s-reader-meta t-label"><span>{resource.kind}</span><span>{resource.checked?'Checked '+resource.checked:'NextStepUni learning prompts'}</span></div>
    <p>{resource.why}</p>
    {resource.url&&<a className="ui-part ui-link frame-hit cw7s-source" href={resource.url} target="_blank" rel="noreferrer"><span>Open the original resource</span><Arrow meaning="leaves" size={16}/></a>}
    <h3>{resource.url?'Read with these questions in mind.':'Try this with your own question.'}</h3>
    <ol className="cw7s-prompts">{resource.prompts.map(p=><li key={p}>{p}</li>)}</ol>
    <p className="cw7s-limit">{resource.limit}</p>
    <div className="cw7s-takeaway">
      <h3>Bring something back.</h3>
      <AreaField label={resource.url?'A detail worth keeping from the resource':'My response to the guide'} rows={4} maxLength={4000} value={draft.note} onChange={e=>onChange({...draft,note:e.target.value})}/>
      <AreaField label="How this helps my question" rows={2} maxLength={2000} value={draft.why} onChange={e=>onChange({...draft,why:e.target.value})}/>
      {resource.url&&<Field label="Page, section, table or access detail" help={resource.where?'The source record points to: '+resource.where:undefined} value={draft.locator} maxLength={500} onChange={e=>onChange({...draft,locator:e.target.value})} placeholder="Enough detail to find this again"/>}
      <Button kind="main" {...waitFor(!draft.note.trim()||!draft.why.trim()||(!!resource.url&&!draft.locator.trim()))} onClick={()=>void onSave(draft)}><Glyph icon={Plus} size={16}/>Save takeaway to Evidence</Button>
    </div>
  </div>;
}

function OwnPressure({project,value,onChange,onSave}:{project:CourseworkProject;value:PressureDraft;onChange:(v:PressureDraft)=>void;onSave:(v:PressureDraft)=>Promise<void>}) {
  const evidence=activeEvidence(project);const remaining=evidence.filter(e=>e.id!==value.withheld&&value.roles[e.id]);const patch=(p:Partial<PressureDraft>)=>onChange({...value,...p});
  return <>
    <div className="cw7s-claim"><span className="t-label">Your claim or decision</span><p className="cw7s-claim-text">{value.claim}</p></div>
    <div className="cw7s-slips">
      {evidence.map((e,i)=><article key={e.id} className="cw7s-slip" data-withheld={value.withheld===e.id}>
        <div className="cw7s-slip-n ui-readout">{String(i+1).padStart(2,'0')}</div>
        <div className="cw7s-slip-main">
          <div className="cw7s-slip-meta"><span>{e.kind}</span>{value.withheld===e.id&&<b>Set aside for this test</b>}</div>
          <h3>{e.title}</h3>
          <p className="cw7s-evidence-text">{e.notes}</p>
          <div className="cw7s-roles" role="group" aria-label={`Role of ${e.title}`}>
            {ROLES.map(role=><ChoiceTile key={role} compact kind="toggle" label={role} chosen={value.roles[e.id]===role} onClick={()=>{const roles={...value.roles};if(roles[e.id]===role)delete roles[e.id];else roles[e.id]=role;patch({roles});}}/>)}
            <ChoiceTile compact kind="toggle" label={value.withheld===e.id?'Restore':'Set aside'} chosen={value.withheld===e.id} onClick={()=>patch({withheld:value.withheld===e.id?'':e.id})}/>
          </div>
        </div>
      </article>)}
    </div>
    {!evidence.length&&<p className="cw7s-empty">Capture evidence before revising this connection.</p>}
    <div className="cw7s-stress"><div className="cw7s-stress-in">
      <p className="t-label">{value.withheld?'With that note set aside':'Your evidence roles'}</p>
      <h3>{remaining.length} assigned {remaining.length===1?'piece remains':'pieces remain'}.</h3>
      <p>{remaining.filter(e=>value.roles[e.id]==='Supports').length} supports · {remaining.filter(e=>value.roles[e.id]==='Challenges').length} challenges · {remaining.filter(e=>value.roles[e.id]==='Context').length} context. These are your classifications, not a quality score.</p>
      <p>Would the same claim still follow? What would you now need to find out?</p>
    </div></div>
    <div className="cw7s-rewrite">
      <AreaField label="The claim I can defend, or question still open" rows={3} maxLength={4000} value={value.claim} onChange={e=>patch({claim:e.target.value})}/>
      <AreaField label="How the evidence supports my thinking" rows={3} maxLength={8000} value={value.reasoning} onChange={e=>patch({reasoning:e.target.value})}/>
      <AreaField label="The limit I would keep visible" rows={3} maxLength={5000} value={value.limitation} onChange={e=>patch({limitation:e.target.value})}/>
      <Field label="One thing I would investigate next" value={value.next} maxLength={500} onChange={e=>patch({next:e.target.value})}/>
      <p className="cw7s-muted">Saving updates this connection and retains its original claim. Setting evidence aside is only a thought experiment; it does not archive or delete a note.</p>
      <Button kind="main" {...waitFor(!value.claim.trim()||!value.reasoning.trim()||!value.limitation.trim()||!value.next.trim()||!evidence.some(e=>value.roles[e.id]))} onClick={()=>void onSave(value)}><Glyph icon={Check} size={16}/>Save revised connection</Button>
    </div>
  </>;
}
function Practice({value,onChange,onSave}:{value:PracticeDraft;onChange:(v:PracticeDraft)=>void;onSave:(v:PracticeDraft)=>Promise<void>}) {
  const patch=(v:Partial<PracticeDraft>)=>onChange({...value,...v});const chosen=practiceEvidence.filter(e=>value.roles[e.id]).length;
  return <>
    <div className="cw7s-practice-label">Fictional example · digital scheduling · no material is copied into your Evidence or Connections</div>
    <div className="cw7s-claim"><p className="cw7s-claim-text">“Digital scheduling improves employee wellbeing.”</p></div>
    <div className="cw7s-slips">
      {practiceEvidence.map(e=><article className="cw7s-slip" key={e.id} data-withheld={value.withheld&&e.id==='staff'}>
        <div className="cw7s-slip-n"><Glyph icon={FileText} size={16}/></div>
        <div className="cw7s-slip-main">
          <div className="cw7s-slip-meta">{e.origin}{value.withheld&&e.id==='staff'&&<b>Set aside for this test</b>}</div>
          <h3>{e.title}</h3>
          <p className="cw7s-slip-text">{e.text}</p>
          <div className="cw7s-roles" role="group" aria-label={`Practice role of ${e.title}`}>
            {ROLES.map(role=><ChoiceTile key={role} compact kind="toggle" disabled={value.withheld&&e.id==='staff'} label={role} chosen={value.roles[e.id]===role} onClick={()=>patch({roles:{...value.roles,[e.id]:role}})}/>)}
          </div>
          {value.revealed&&<div className="cw7s-reason"><span className="t-label">{value.roles[e.id]===e.role?'A useful distinction':'Another way to read this'}</span><p>{e.reason}</p></div>}
        </div>
      </article>)}
    </div>
    <div className="cw7s-compare"><Button {...waitFor(chosen<3)} onClick={()=>patch({revealed:!value.revealed})}>{value.revealed?'Hide the reasoning':'Compare with a worked reading'}</Button><span className="cw7s-meta">{chosen}/3 evidence roles chosen · no score</span></div>
    {value.revealed&&<div className="cw7s-stress"><div className="cw7s-stress-in"><h3>Take away the interview support.</h3><p>{value.withheld?'The remaining notes do not establish a general wellbeing benefit. What would you need before making that claim?':'If the strongest supporting note disappeared, would the conclusion still follow?'}</p></div><Button aria-pressed={value.withheld} onClick={()=>patch({withheld:!value.withheld})}><Glyph icon={value.withheld?RotateCcw:X} size={16}/>{value.withheld?'Restore the note':'Set the first note aside'}</Button></div>}
    <AreaField label="My practice claim or question" maxLength={4000} value={value.claim} onChange={e=>patch({claim:e.target.value})}/>
    <AreaField label="My practice limitation" maxLength={3000} value={value.limitation} onChange={e=>patch({limitation:e.target.value})}/>
    <Field label="What I would investigate next in this example" maxLength={500} value={value.next} onChange={e=>patch({next:e.target.value})}/>
    <Button kind="main" {...waitFor(!value.claim.trim()||!value.limitation.trim()||!value.next.trim())} onClick={()=>void onSave(value)}>Save practice reflection</Button>
  </>;
}
function Feedback({value,onChange,onNew,onSave}:{value:FeedbackDraft;onChange:(v:FeedbackDraft)=>void;onNew:()=>void;onSave:(v:FeedbackDraft)=>Promise<void>}) {
  const [example,setExample]=useState(false);const patch=(p:Partial<FeedbackDraft>)=>onChange({...value,...p});
  return <>
    <div className="cw7s-origin"><AreaField label="The feedback I received" help="Keep your teacher’s wording. Your interpretation belongs below." rows={3} maxLength={4000} value={value.comment} onChange={e=>patch({comment:e.target.value})} placeholder="Paste or record the actual comment."/></div>
    <div className="cw7s-mode" role="group" aria-label="How to handle feedback">
      <ChoiceTile kind="toggle" label="I can turn this into an action" chosen={value.mode==='action'} onClick={()=>patch({mode:'action'})}/>
      <ChoiceTile kind="toggle" label="I need to clarify it first" chosen={value.mode==='question'} onClick={()=>patch({mode:'question'})}/>
    </div>
    {value.mode==='action'?<div className="cw7s-flow">{[{key:'meaning',label:'What I think my teacher is asking for'},{key:'action',label:'One action I will take'},{key:'proof',label:'What I will be able to show afterwards'}].map((f,i)=><div className="cw7s-step" key={f.key}><span className="cw7s-step-n ui-readout">0{i+1}</span><AreaField label={f.label} rows={3} maxLength={3000} value={value[f.key as 'meaning'|'action'|'proof']} onChange={e=>patch({[f.key]:e.target.value})}/></div>)}</div>
      :<div className="cw7s-clarify"><h3>A precise question is progress.</h3><AreaField label="The question I will bring to my teacher" rows={4} maxLength={3000} value={value.question} onChange={e=>patch({question:e.target.value})} placeholder="When you said…, did you mean…? I was planning to…"/></div>}
    <div className="cw7s-row">
      <Button kind="main" {...waitFor(!value.comment.trim()||(value.mode==='action'?(!value.meaning.trim()||!value.action.trim()||!value.proof.trim()):!value.question.trim()))} onClick={()=>void onSave(value)}><Glyph icon={Plus} size={16}/>{value.mode==='action'?'Save feedback and action':'Save feedback and teacher question'}</Button>
      <TextButton onClick={()=>setExample(v=>!v)}>{example?'Hide example':'See a worked example'}</TextButton>
    </div>
    <details className="cw7s-another"><summary>Start another feedback record</summary><p>Save this feedback into Evidence and Plan first if you want to keep it. A saved draft is replaced when you start and save another. Starting another clears these entry fields; previously saved Evidence and Plan records remain.</p><Button onClick={onNew}>Start another comment</Button></details>
    {example&&<div className="cw7s-example"><p className="t-label">Fictional example, not a suggested answer</p><dl><dt>Feedback</dt><dd>“Explain how the evidence supports your point.”</dd><dt>Interpretation</dt><dd>I included a statistic, but did not explain its connection to my claim.</dd><dt>Action</dt><dd>Return to one paragraph and explain what the statistic measures.</dd><dt>Finish line</dt><dd>I can identify the source, explain the connection, and name a limitation.</dd></dl></div>}
  </>;
}
