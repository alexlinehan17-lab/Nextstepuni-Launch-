import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import CourseworkStudio from '../components/CourseworkStudio/CourseworkStudio';
import { courseworkDemo } from '../components/CourseworkStudio/demo';
import { emptyWorkspace, type CourseworkWorkspace } from '../components/CourseworkStudio/model';
import type { CourseworkStore } from '../components/CourseworkStudio/store';
function memoryStore(value:CourseworkWorkspace=courseworkDemo()):CourseworkStore {
  let saved=structuredClone(value);
  return {load:vi.fn(async()=>structuredClone(saved)),save:vi.fn(async(_owner,next)=>{saved={...structuredClone(next),revision:saved.revision+1};return saved;})};
}
describe('Coursework Studio working flows',()=>{
  test('captures an observation, persists it and restores it on reopening',async()=>{
    const store=memoryStore();const mounted=render(<CourseworkStudio uid="student1" storage={store}/>);
    await screen.findByRole('heading',{name:'The changing working day'});
    fireEvent.click(screen.getByRole('button',{name:'Capture evidence'}));
    const dialog=screen.getByRole('dialog');
    fireEvent.change(within(dialog).getByLabelText('Type of evidence'),{target:{value:'Observation'}});
    fireEvent.change(within(dialog).getByLabelText('Give it a useful name'),{target:{value:'A real observation'}});
    fireEvent.change(within(dialog).getByLabelText('What did you find, do or notice?'),{target:{value:'I noticed a question that needs more evidence.'}});
    fireEvent.click(within(dialog).getByRole('button',{name:'Save evidence'}));
    await waitFor(()=>expect(store.save).toHaveBeenCalled());
    await waitFor(()=>expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
    mounted.unmount();render(<CourseworkStudio uid="student1" storage={store}/>);
    expect(await screen.findByRole('button',{name:/A real observation/})).toBeInTheDocument();
  });
  test('a failed write keeps the open form and does not pretend the note was saved',async()=>{
    const store=memoryStore();store.save=vi.fn(async()=>{throw new Error('Device storage is full.');});
    render(<CourseworkStudio uid="student1" storage={store}/>);await screen.findByRole('heading',{name:'The changing working day'});
    fireEvent.click(screen.getByRole('button',{name:'Capture evidence'}));
    fireEvent.change(screen.getByLabelText('Give it a useful name'),{target:{value:'Keep this draft'}});
    fireEvent.change(screen.getByLabelText('What did you find, do or notice?'),{target:{value:'These are my unsaved notes.'}});
    fireEvent.click(screen.getByRole('button',{name:'Save evidence'}));
    await waitFor(()=>expect(screen.getAllByText('Device storage is full.').length).toBeGreaterThan(0));
    expect(screen.getByLabelText('Give it a useful name')).toHaveValue('Keep this draft');
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });
  test('the empty state creates a real year-scoped workspace',async()=>{
    const store=memoryStore(emptyWorkspace());render(<CourseworkStudio uid="student2" examDate="2028-06-01" storage={store}/>);
    fireEvent.click(await screen.findByRole('button',{name:'Start my first project'}));
    fireEvent.change(screen.getByLabelText('Subject'),{target:{value:'geography'}});
    fireEvent.change(screen.getByLabelText('Project name'),{target:{value:'My fieldwork'}});
    fireEvent.click(screen.getByRole('button',{name:'Create my workspace'}));
    await screen.findByRole('heading',{name:'My fieldwork'});
    fireEvent.click(screen.getByRole('tab',{name:'Brief'}));
    expect(await screen.findByText(/2028: 40% Applied Geography Project/)).toBeInTheDocument();
  });
  test('review drafts survive tab navigation and can be saved later',async()=>{
    const store=memoryStore();render(<CourseworkStudio uid="student1" storage={store}/>);await screen.findByRole('heading',{name:'The changing working day'});
    fireEvent.click(screen.getByRole('tab',{name:'Review'}));
    fireEvent.change(screen.getByLabelText('What changed in my thinking? What will I ask my teacher?'),{target:{value:'I need to check my assumptions.'}});
    fireEvent.click(screen.getByRole('tab',{name:'Overview'}));fireEvent.click(screen.getByRole('tab',{name:'Review'}));
    expect(screen.getByLabelText('What changed in my thinking? What will I ask my teacher?')).toHaveValue('I need to check my assumptions.');
    fireEvent.click(screen.getByRole('button',{name:'Save review notes'}));
    await waitFor(()=>expect(store.save).toHaveBeenCalled());
  });
  test('LCA is not silently mapped to the LCE workflow',()=>{
    render(<CourseworkStudio isLca storage={memoryStore()}/>);
    expect(screen.getByText(/LCA uses a different module and task system/)).toBeInTheDocument();
    expect(screen.queryByRole('button',{name:'New project'})).not.toBeInTheDocument();
  });
});
