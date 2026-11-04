import React from 'react';
import {act,cleanup,fireEvent,render,screen,waitFor} from '@testing-library/react';
import {afterEach,expect,test,vi} from 'vitest';
import {ReadingSection,MicroCommitment,Highlight} from '@/components/ModuleShared';
import {TriageSimulator} from '@/components/ExamHallStrategiesModule';
import {BrandedAutopilot} from '@/components/learning/BrandedFeatures';
import {BrandedGrades,BrandedRecallChart,BrandedSupport,BrandedBackwardSorter} from '@/components/learning/WideFeatures';
import {ALL_COURSES} from '@/courseData';
import {MODULE_SECTIONS} from '@/moduleSections';
import type {ModuleTheme} from '@/types';

const account=vi.hoisted(()=>({loadedData:{studentProfile:{subjects:[{subjectName:'Biology',level:'higher',currentGrade:'H4',targetGrade:'H2'}]}}}));
const drafts=vi.hoisted(()=>({values:new Map<string,string>([['if-text','If I finish dinner'],['then-text','I will recall one topic']])}));
vi.mock('@/contexts/AuthContext',()=>({useAuth:()=>account}));
vi.mock('@/hooks/useModuleDraft',()=>({useModuleDraft:(_moduleId:string,key:string,initial:string)=>{const [value,setValue]=React.useState(drafts.values.get(key)??initial);return [value,(next:string)=>{drafts.values.set(key,next);setValue(next)}]}}));
afterEach(()=>{cleanup();vi.useRealTimers();document.documentElement.classList.remove('dark')});
const theme={} as ModuleTheme;
const Reader=({children}:{children:React.ReactNode})=><div className="nsu-module-reader">{children}</div>;
for(const mode of ['light','dark']){
 test(`${mode}: both focus placements use the regular thinker`,()=>{
  document.documentElement.classList.toggle('dark',mode==='dark');
  const v=render(<Reader><ReadingSection title="Scaffolding Your Focus." eyebrow="Step 8" icon={()=>null} theme={theme}><MicroCommitment artwork="thinker" theme={theme}>One small action.</MicroCommitment></ReadingSection></Reader>);
  const images=v.container.querySelectorAll('img');expect(images).toHaveLength(2);images.forEach(img=>expect(img.getAttribute('src')).toContain('star-crew/companions/thinker.png'));
 });
 test(`${mode}: triage markers survive correct and incorrect answers, completion and restart`,()=>{
  document.documentElement.classList.toggle('dark',mode==='dark');vi.useFakeTimers();
  const v=render(<Reader><TriageSimulator/></Reader>);fireEvent.click(screen.getByRole('button',{name:'Start Triage'}));
  expect(v.container.querySelectorAll('[data-triage-progress]')).toHaveLength(8);expect(v.container.querySelectorAll('[data-triage-progress=pending]')).toHaveLength(7);
  const correct=['green','red','green','amber','green','red','amber','green'];
  for(let i=0;i<correct.length;i++){
   fireEvent.click(v.container.querySelector(`[data-triage-choice=${i===0?'red':correct[i]}]`)!);
   const buttons=[...v.container.querySelectorAll<HTMLButtonElement>('[data-triage-choice]')];expect(buttons).toHaveLength(3);buttons.forEach(b=>{expect(b).toBeDisabled();expect(b.querySelector('[data-triage-choice-marker]')).toBeInTheDocument()});
   expect(v.container.querySelector(`[data-triage-choice=${correct[i]}]`)).toHaveAttribute('data-selected','true');
   expect(v.container.querySelectorAll('[data-triage-progress]')[i]).toHaveAttribute('data-triage-progress',i===0?'incorrect':'correct');
   act(()=>{vi.advanceTimersByTime(1800)});
  }
  expect(screen.getByText('7/8')).toBeInTheDocument();fireEvent.click(screen.getByRole('button',{name:'Run Drill Again'}));expect(v.container.querySelectorAll('[data-triage-progress=pending]')).toHaveLength(7);expect(v.container.querySelectorAll('[data-triage-progress=current]')).toHaveLength(1);
 });
}
test('grades use the actual onboarding profile without another form',()=>{const v=render(<BrandedGrades/>);expect(screen.getByText('Biology')).toBeInTheDocument();expect(screen.getByText('H4')).toBeInTheDocument();expect(screen.getByText('H2')).toBeInTheDocument();expect(v.container.querySelector('input')).toBeNull();expect(v.container.textContent).not.toContain('Sample onboarding profile')});
test('recall comparison keeps the sourced one-week group scores and accurately describes the conditions',()=>{const v=render(<BrandedRecallChart/>);expect(screen.getByText(/one week later/)).toBeInTheDocument();expect(screen.getByText('Four reading periods')).toBeInTheDocument();expect(screen.getByText('One reading period + three recall tests')).toBeInTheDocument();fireEvent.click(screen.getByRole('button',{name:'Reveal the results'}));expect([...v.container.querySelectorAll('output')].map(e=>e.textContent)).toEqual(['40%','61%']);expect(screen.getByRole('link')).toHaveAttribute('href','https://learninglab.psych.purdue.edu/downloads/2006/2006_Roediger_Karpicke_PsychSci.pdf');expect(v.container.textContent).not.toContain('same study time')});
test('saved If–Then fields survive the reviewed control replacement and edits',()=>{const first=render(<BrandedAutopilot/>);const inputs=screen.getAllByRole('textbox');expect(inputs[0]).toHaveValue('If I finish dinner');expect(inputs[1]).toHaveValue('I will recall one topic');fireEvent.change(inputs[1],{target:{value:'I will recall two topics'}});first.unmount();render(<BrandedAutopilot/>);expect(screen.getAllByRole('textbox')[1]).toHaveValue('I will recall two topics')});
test('opening another definition closes the first, and Escape returns focus',async()=>{render(<><Highlight description="About you" theme={theme}>Internal</Highlight><Highlight description="Outside you" theme={theme}>External</Highlight></>);fireEvent.click(screen.getByRole('button',{name:'Internal'}));fireEvent.click(screen.getByRole('button',{name:'External'}));await waitFor(()=>expect(screen.getAllByRole('note')).toHaveLength(1));expect(screen.getByRole('note')).toHaveTextContent('Outside you');fireEvent.keyDown(document,{key:'Escape'});await waitFor(()=>expect(screen.queryByRole('note')).toBeNull());expect(screen.getByRole('button',{name:'External'})).toHaveFocus()});
test('removed WRAP section is absent from the actual section metadata and course count',()=>{const sections=MODULE_SECTIONS['exam-crisis-management-protocol'];expect(sections).toHaveLength(6);expect(sections.some(s=>/Personal Crisis Plan|WRAP/.test(s.title))).toBe(false);expect(sections.at(-1)?.title).toBe('The 7-Day Countdown');expect(ALL_COURSES.find(c=>c.id==='exam-crisis-management-protocol')?.sectionsCount).toBe(6);const v=render(<BrandedSupport/>);expect(v.container).toBeEmptyDOMElement()});
test('backwards planning can be completed with the visible keyboard controls',()=>{render(<BrandedBackwardSorter/>);fireEvent.click(screen.getByRole('button',{name:'Move Set your target grade (The Goal) up'}));fireEvent.click(screen.getByRole('button',{name:'Check order'}));expect(screen.getByRole('status')).toHaveTextContent('That’s the order')});
