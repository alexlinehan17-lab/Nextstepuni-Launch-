import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import CourseworkStudio from '../components/CourseworkStudio/CourseworkStudio';
import { courseworkDemo } from '../components/CourseworkStudio/demo';
import { parseBackup, reviewExport, type CourseworkWorkspace } from '../components/CourseworkStudio/model';
import { emptySupport, feedbackRecords, newFeedback } from '../components/CourseworkStudio/supportState';
import { courseworkResources } from '../data/curriculum/courseworkResources';
import type { CourseworkStore } from '../components/CourseworkStudio/store';
function memoryStore(value=courseworkDemo()) {
  let saved=structuredClone(value);
  const storage:CourseworkStore={load:vi.fn(async()=>structuredClone(saved)),save:vi.fn(async(_owner,next)=>{saved=parseBackup(JSON.stringify({...next,revision:saved.revision+1}));return structuredClone(saved);})};
  return {storage,get:()=>saved};
}
async function open(storage:CourseworkStore) {const mounted=render(<CourseworkStudio uid="integration-student" storage={storage}/>);await screen.findByRole('heading',{name:'The changing working day'});return mounted;}
const fill=(label:string,value:string)=>fireEvent.change(screen.getByLabelText(new RegExp(label)),{target:{value}});
const click=(name:string)=>fireEvent.click(screen.getByRole('button',{name}));
const tab=(name:string)=>fireEvent.click(screen.getByRole('tab',{name}));
async function saved(text:string){await screen.findByText(text);}

describe('Integrated coursework support',()=>{
  test('a small restart becomes a real plan step and saved drafts reopen',async()=>{
    const store=memoryStore();let mounted=await open(store.storage);click('Find a way back in');
    fill('The next action I am choosing','Compare one source with my question.');click('Save draft');await saved('Draft saved on this device.');
    mounted.unmount();mounted=await open(store.storage);click('Find a way back in');
    expect(screen.getByLabelText('The next action I am choosing')).toHaveValue('Compare one source with my question.');
    click('Save next step to Plan');await saved('Your next step is saved in Plan.');
    expect(store.get().projects[0].milestones.at(-1)).toMatchObject({label:'Compare one source with my question.',minutes:15,done:false});
    click('View saved work');expect(await screen.findByText('Compare one source with my question.')).toBeInTheDocument();
    mounted.unmount();
  });
  test('resource shelf and takeaway persist with source provenance',async()=>{
    const store=memoryStore();await open(store.storage);tab('Evidence3');click('Resource desk');
    const article=screen.getByRole('heading',{name:'A starting point for Irish business data'}).closest('article')!;
    fireEvent.click(within(article).getByRole('button',{name:'Keep on my shelf'}));await saved('Resource shelf saved.');
    fireEvent.click(within(article).getByRole('button',{name:'Open resource notes'}));
    fill('A detail worth keeping from the resource','The source describes businesses at sector level.');fill('How this helps my question','Useful context, not a measure of wellbeing in my café.');
    expect(screen.getByRole('button',{name:'Save takeaway to Evidence'})).toBeDisabled();
    fill('Page, section, table or access detail','Project resources by theme, accessed 30 October 2026');click('Save takeaway to Evidence');await saved('Takeaway saved in Evidence.');
    const project=store.get().projects[0];expect(project.support?.bookmarks).toContain('data-cso-business-2027');expect(project.evidence.at(-1)).toMatchObject({kind:'Source',author:'Central Statistics Office',locator:'Project resources by theme, accessed 30 October 2026',notes:'The source describes businesses at sector level.'});expect(project.evidence.at(-1)?.url).toContain('cso.ie');
  });
  test('feedback preserves the raw comment and creates one linked action, including on repeated saves',async()=>{
    const store=memoryStore();await open(store.storage);tab('Review');click('Put feedback to work');
    expect(screen.getByLabelText(/The feedback I received/)).toHaveValue('');
    fill('The feedback I received','Explain how this statistic supports your point.');fill('What I think my teacher is asking for','I have a number but no explanation.');fill('One action I will take','Explain the measure in paragraph two.');fill('What I will be able to show afterwards','A traced source and a justified connection.');
    click('Save feedback and action');await saved('Feedback saved in Evidence, with a linked next step in Plan.');
    const first=store.get().projects[0];expect(first.evidence.at(-1)?.notes).toContain('Original comment: Explain how this statistic supports your point.');expect(first.milestones.at(-1)).toMatchObject({evidenceId:first.evidence.at(-1)?.id,label:'Explain the measure in paragraph two.'});
    fill('One action I will take','Explain the measure and its population.');click('Save feedback and action');await saved('Feedback saved in Evidence, with a linked next step in Plan.');
    expect(store.get().projects[0].evidence).toHaveLength(first.evidence.length);expect(store.get().projects[0].milestones).toHaveLength(first.milestones.length);
    expect(reviewExport(store.get().projects[0])).toContain('A traced source and a justified connection.');
  });
  test('failed feedback save retains inputs, and clarification saves as a teacher step',async()=>{
    const store=memoryStore(),goodSave=store.storage.save;store.storage.save=vi.fn(async()=>{throw Error('Storage full');});await open(store.storage);tab('Review');click('Put feedback to work');
    fill('The feedback I received','Narrow this down.');click('I need to clarify it first');fill('The question I will bring to my teacher','Should I narrow the setting or the outcome?');click('Save feedback and teacher question');
    await waitFor(()=>expect(screen.getAllByText('Storage full').length).toBeGreaterThan(0));expect(screen.getByLabelText(/The feedback I received/)).toHaveValue('Narrow this down.');expect(store.get().projects[0].evidence).toHaveLength(3);
    store.storage.save=goodSave;click('Save feedback and teacher question');await saved('Feedback saved in Evidence, with a linked next step in Plan.');expect(store.get().projects[0].milestones.at(-1)?.setting).toBe('With my teacher');
  });
  test('pressure test preserves evidence and the original claim while revising a connection',async()=>{
    const store=memoryStore();const initial=structuredClone(store.get().projects[0]);await open(store.storage);tab('Connections');click('Pressure-test this claim');
    const group=screen.getByRole('group',{name:'Role of '+initial.evidence[0].title});fireEvent.click(within(group).getByRole('button',{name:'Supports'}));fireEvent.click(within(group).getByRole('button',{name:'Set aside'}));
    fill('The claim I can defend, or question still open','I need more direct evidence before drawing a conclusion.');fill('The limit I would keep visible','These notes record a process, not workplace findings.');fill('One thing I would investigate next','Agree a feasible source of direct evidence.');click('Save revised connection');await saved('Revised connection saved. Your original claim is retained in its pressure-test record.');
    const project=store.get().projects[0];expect(project.evidence).toEqual(initial.evidence);expect(project.connections).toHaveLength(1);expect(project.connections[0].pressureReview).toMatchObject({originalClaim:initial.connections[0].claim,withheld:initial.evidence[0].id});
  });
  test('fictional practice stays outside student evidence and survives reopening',async()=>{
    const store=memoryStore();const before=structuredClone(store.get().projects[0]);const mounted=await open(store.storage);tab('Connections');click('Pressure-test a claim');click('Try the worked example');
    fill('My practice claim or question','A benefit is possible under specific conditions.');fill('My practice limitation','The fictional evidence cannot establish a general effect.');fill('What I would investigate next in this example','Look for a competing explanation.');click('Save practice reflection');await saved('Practice reflection saved separately from your project evidence.');
    const project=store.get().projects[0];expect(project.evidence).toEqual(before.evidence);expect(project.connections).toEqual(before.connections);expect(reviewExport(project)).not.toContain('A benefit is possible under specific conditions.');
    mounted.unmount();await open(store.storage);tab('Connections');click('Pressure-test a claim');click('Try the worked example');expect(screen.getByLabelText('My practice claim or question')).toHaveValue('A benefit is possible under specific conditions.');
  });
  test('unsaved support drafts survive closing and changing projects',async()=>{
    const store=memoryStore();await open(store.storage);click('Find a way back in');fill('The next action I am choosing','A draft for Business only.');click('Close');
    fireEvent.click(screen.getByRole('button',{name:/Biology.*2027/}));click('Find a way back in');expect(screen.getByLabelText('The next action I am choosing')).toHaveValue('');click('Close');fireEvent.click(screen.getByRole('button',{name:/Business.*2027/}));click('Find a way back in');expect(screen.getByLabelText('The next action I am choosing')).toHaveValue('A draft for Business only.');
  });
});

describe('Support data boundaries',()=>{
  test('old backups and additive fields round-trip, invalid nested records fail',()=>{
    const old=courseworkDemo();expect(parseBackup(JSON.stringify(old))).toEqual(old);
    const draft={...newFeedback(),comment:'Original',meaning:'Meaning',action:'Action',proof:'Finish line'};
    const p=old.projects[0];Object.assign(p,feedbackRecords(p,draft,'2026-10-30'),{support:{...emptySupport(),drafts:{feedback:draft}}});expect(parseBackup(JSON.stringify(old))).toEqual(old);
    const bad=structuredClone(old);bad.projects[0].milestones.at(-1)!.evidenceId='missing';expect(()=>parseBackup(JSON.stringify(bad))).toThrow();
    const badReview=structuredClone(old);badReview.projects[0].connections[0].pressureReview={originalClaim:'Original',roles:{missing:'Supports'},withheld:'',next:'Find evidence',testedAt:'2026-10-30'};expect(()=>parseBackup(JSON.stringify(badReview))).toThrow();
    const corrupt=structuredClone(old) as CourseworkWorkspace;corrupt.projects[0].support!.drafts.restart={id:'r',blocker:'unknown',note:'',minutes:15,checked:[]};expect(()=>parseBackup(JSON.stringify(corrupt))).toThrow();
  });
  test('subject and cohort resources do not leak annual briefs across years',()=>{
    const ids=(subject:string,year:number)=>courseworkResources(subject,year).map(r=>r.id);
    expect(ids('business',2027)).toContain('source-businessBrief');expect(ids('business',2028)).not.toContain('source-businessBrief');expect(ids('business',2028)).not.toContain('data-cso-business-2027');expect(ids('biology',2027)).not.toContain('data-cso-business-2027');
    expect(ids('geography',2027)).toContain('source-geoOld');expect(ids('geography',2027)).not.toContain('source-geoNew');expect(ids('geography',2028)).toContain('source-geoNew');expect(ids('geography',2028)).not.toContain('source-geoOld');
    expect(courseworkResources('biology',2027).find(r=>r.id==='guide-question')?.prompts.join(' ')).toContain('variable');expect(ids('english',2027)).toEqual([]);
  });
});
