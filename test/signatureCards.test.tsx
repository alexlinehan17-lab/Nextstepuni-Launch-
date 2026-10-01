import React from 'react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { ReaderNotes } from '@/components/learning/ReaderNotes';
import StudyJournalModal from '@/components/StudyJournalModal';
import SubjectOnboarding from '@/components/SubjectOnboarding';
import ChangeSubjectsModal from '@/components/ChangeSubjectsModal';
import LaunchpadToolCard from '@/components/launchpad/LaunchpadToolCard';
import { createDevStudentProfile } from '@/data/devStudent';
import type { StudyReflection } from '@/types';

const account = vi.hoisted(() => ({ uid: 'notes-account-a' }));
vi.mock('@/contexts/AuthContext', () => ({ useAuth: () => ({ user: account }) }));
beforeEach(() => { localStorage.clear(); account.uid = 'notes-account-a'; });
afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('approved Signature cards', () => {
  test('keeps notebook notes under the existing account and module storage key', () => {
    const key = 'nextstepuni:learning-notes:notes-account-a:drivers-manual';
    localStorage.setItem(key,'A thought from the existing notebook.');
    const props = { moduleId: 'drivers-manual', title: "The Driver’s Manual", open: true, onClose: vi.fn() };
    const { rerender } = render(<ReaderNotes {...props} />);
    expect(screen.getByRole('textbox',{ name: 'Your notes' })).toHaveValue('A thought from the existing notebook.');
    fireEvent.change(screen.getByRole('textbox',{ name: 'Your notes' }),{ target: { value: 'Choose one small action.' } });
    expect(localStorage.getItem(key)).toBe('Choose one small action.');
    account.uid = 'notes-account-b';
    rerender(<ReaderNotes {...props} />);
    expect(screen.getByRole('textbox',{ name: 'Your notes' })).toHaveValue('');
    account.uid = 'notes-account-a';
    rerender(<ReaderNotes {...props} moduleId="bimodal-brain" />);
    expect(screen.getByRole('textbox',{ name: 'Your notes' })).toHaveValue('');
    rerender(<ReaderNotes {...props} />);
    expect(screen.getByRole('textbox',{ name: 'Your notes' })).toHaveValue('Choose one small action.');
  });

  test('keeps unsaved writing visible and reports storage failure', () => {
    vi.spyOn(Storage.prototype,'setItem').mockImplementation(() => { throw new Error('Storage unavailable'); });
    render(<ReaderNotes moduleId="drivers-manual" title="The Driver’s Manual" open onClose={vi.fn()} />);
    fireEvent.change(screen.getByRole('textbox',{ name: 'Your notes' }),{ target: { value: 'Keep this copy.' } });
    expect(screen.getByRole('textbox',{ name: 'Your notes' })).toHaveValue('Keep this copy.');
    expect(screen.getByRole('status')).toHaveTextContent('Could not save on this device. Keep a copy before leaving.');
  });

  test('shows an empty journal as a dismissible card', () => {
    const onClose = vi.fn();
    render(<StudyJournalModal isOpen onClose={onClose} reflections={[]} />);
    expect(screen.getByRole('dialog',{ name: 'Study Journal' })).toHaveAttribute('aria-modal','true');
    expect(screen.getByText('0 reflections · 0 JP earned')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{ name: 'Back to study' }));
    expect(onClose).toHaveBeenCalledOnce();
  });

  test('retains journal date order, filtering, reflection text and earned points', () => {
    const reflections: StudyReflection[] = [{ dateKey:'2026-09-30',blockId:'a',subjectName:'English',sessionType:'practice',reflection:'Plan the paragraph first.',pointsEarned:25,timestamp:1 },{ dateKey:'2026-10-01',blockId:'b',subjectName:'Mathematics',sessionType:'revision',reflection:'Recall helped me find a gap.',pointsEarned:30,timestamp:2 }];
    render(<StudyJournalModal isOpen onClose={vi.fn()} reflections={reflections} />);
    expect(screen.getByText('2 reflections · 55 JP earned')).toBeInTheDocument();
    expect(screen.getAllByRole('article')[0]).toHaveTextContent('Recall helped me find a gap.');
    fireEvent.click(screen.getByRole('button',{ name:'English' }));
    expect(screen.getAllByRole('article')).toHaveLength(1);
    expect(screen.getByRole('article')).toHaveTextContent('Practice · +25 JP');
    fireEvent.click(screen.getByRole('button',{ name:'All' }));
    expect(screen.getAllByRole('article')).toHaveLength(2);
  });

  test('retains setup grade constraints, date validation, rest-day validation and save payload', () => {
    const complete = vi.fn();
    render(<SubjectOnboarding user={{uid:'test-student'}} onClose={vi.fn()} onComplete={complete} />);
    fireEvent.click(screen.getByRole('button',{ name:'Get Started' }));
    expect(screen.getByRole('dialog',{ name:'Select Your Subjects' })).toHaveFocus();
    expect(screen.getByRole('button',{ name:'Continue' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button',{ name:'English' }));
    fireEvent.click(screen.getByRole('button',{ name:'Continue' }));
    fireEvent.click(within(screen.getByRole('group',{ name:'English level' })).getByRole('button',{ name:'Ordinary' }));
    expect(within(screen.getByRole('group',{ name:'English current grade' })).getByRole('button',{ name:'O4' })).toHaveAttribute('aria-pressed','true');
    expect(within(screen.getByRole('group',{ name:'English target grade' })).getByRole('button',{ name:'O8' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button',{ name:'Continue' }));
    fireEvent.change(screen.getByLabelText('Exam start date'),{target:{value:'2000-06-02'}});
    expect(screen.getByRole('button',{ name:'Continue' })).toBeDisabled();
    const exam = `${new Date().getFullYear()+1}-06-02`;
    fireEvent.change(screen.getByLabelText('Exam start date'),{target:{value:exam}});
    fireEvent.click(screen.getByRole('button',{ name:'Continue' }));
    for(const day of ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])fireEvent.click(screen.getByRole('button',{name:`${day}, study day`}));
    expect(screen.getByRole('button',{ name:'Continue' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button',{name:'Sun, rest day'}));
    fireEvent.click(screen.getByRole('button',{ name:'Continue' }));
    fireEvent.click(screen.getByRole('button',{ name:'Save & Continue' }));
    expect(complete).toHaveBeenCalledOnce();
    expect(complete.mock.calls[0][0]).toMatchObject({ subjects:[{subjectName:'English',level:'ordinary',currentGrade:'O4',targetGrade:'O2'}],examStartDate:exam,restDays:['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'] });
  });

  test('subject editing keeps curriculum and scheduling metadata', () => {
    const profile = createDevStudentProfile(new Date());
    profile.subjects = [{subjectName:'English',level:'higher',currentGrade:'H4',targetGrade:'H2'}];
    const save = vi.fn();
    render(<ChangeSubjectsModal isOpen onClose={vi.fn()} onSave={save} currentProfile={profile} />);
    fireEvent.click(screen.getByRole('button',{ name:'Continue' }));
    fireEvent.click(within(screen.getByRole('group',{ name:'English level' })).getByRole('button',{ name:'Ordinary' }));
    fireEvent.click(screen.getByRole('button',{ name:'Save Changes' }));
    expect(save.mock.calls[0][0]).toMatchObject({ ...profile,subjects:[{subjectName:'English',level:'ordinary',currentGrade:'O4',targetGrade:'O2'}],updatedAt:expect.any(String) });
  });

  test('locked tools retain their identity and setup action while loading stays disabled', () => {
    const open = vi.fn();
    const props = { tool:'war-room' as const,title:'War Room',description:'Decide what needs your attention.',locked:true,pending:false,onClick:open };
    const { rerender } = render(<LaunchpadToolCard {...props} />);
    const card = screen.getByRole('button',{name:'Set up profile to unlock War Room'});
    expect(within(card).getByText('Decide what needs your attention.')).toBeInTheDocument();
    expect(within(card).getByText('Add your subjects to unlock')).toBeInTheDocument();
    fireEvent.click(card);expect(open).toHaveBeenCalledOnce();
    rerender(<LaunchpadToolCard {...props} pending locked={false} />);
    expect(screen.getByRole('button',{name:'Loading profile for War Room'})).toBeDisabled();
    expect(screen.getByText('Checking your profile…')).toBeInTheDocument();
  });
});
