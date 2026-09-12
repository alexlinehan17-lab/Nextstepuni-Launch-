import React from 'react';
import { describe, expect, it, vi, afterEach } from 'vitest';
import { cleanup, render, screen, fireEvent, within } from '@testing-library/react';
import SubjectPicker from '../components/launchpad/SubjectPicker';
import { SubjectAccessContext } from '../components/launchpad/SubjectAccess';
import GlassStage from '../components/landing/glass/GlassStage';
import MarkBank from '../components/MarkBank/MarkBank';

const allowed = (name: string) => ['Biology', 'Mathematics'].includes(name);
const options = ['Biology', 'Chemistry', 'Mathematics', 'Home Economics'].map(label => ({value:label,label}));
afterEach(() => { cleanup(); localStorage.removeItem('mb:choice:anon'); });

describe('Landing subject access', () => {
  it('restricts the body-portal picker to Biology and Mathematics', () => {
    const select = vi.fn();
    const {container} = render(<GlassStage active={false} canSelectSubject={allowed}><SubjectPicker value="Biology" options={options} onChange={select} /></GlassStage>);
    fireEvent.click(screen.getByRole('button', {name:'Choose a subject'}));
    const dialog = screen.getByRole('dialog');
    expect(container.contains(dialog)).toBe(false);
    const chemistry = within(dialog).getByRole('button', {name:'Chemistry — available in the app'});
    expect(chemistry).toBeDisabled();
    fireEvent.click(chemistry);
    expect(select).not.toHaveBeenCalled();
    fireEvent.change(screen.getByRole('searchbox', {name:'Search subjects'}), {target:{value:'math'}});
    fireEvent.click(within(dialog).getByRole('button', {name:'Mathematics'}));
    expect(select).toHaveBeenCalledWith('Mathematics');
  });
  it('leaves subjects fully accessible outside the preview', () => {
    const select = vi.fn();
    render(<SubjectPicker value="Biology" options={options} onChange={select} />);
    fireEvent.click(screen.getByRole('button', {name:'Choose a subject'}));
    fireEvent.click(screen.getByRole('button', {name:'Chemistry'}));
    expect(select).toHaveBeenCalledWith('Chemistry');
  });
  it('does not reopen a remembered locked Mark Bank subject in the preview', () => {
    localStorage.setItem('mb:choice:anon', JSON.stringify({subjectId:'chemistry',level:'higher'}));
    render(<SubjectAccessContext.Provider value={allowed}><MarkBank studentSubjects={[{subjectName:'Chemistry',level:'higher'}, {subjectName:'Biology',level:'higher'}]} /></SubjectAccessContext.Provider>);
    expect(screen.getByRole('button', {name:'Choose a subject'})).toHaveTextContent('Biology');
  });
});
