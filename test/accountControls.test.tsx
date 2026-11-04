import React, { useState } from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { getSchoolName } from '../schoolData';
import { SCHOOL_NAMES } from '../functions/src/gcPasswordPolicy';
import { describe, expect, it, vi } from 'vitest';
import AccountSchoolPicker from '../components/AccountSchoolPicker';
import AccountCrewPicker from '../components/AccountCrewPicker';
import SchoolCrest from '../components/SchoolCrest';
import { Checkbox } from '../components/account-ui-runtime';

function SchoolHarness({ disabled = false }) {
  const [school, setSchool] = useState('');
  return <><label htmlFor="school">School</label><AccountSchoolPicker id="school" value={school} onChange={setSchool} disabled={disabled} /><output data-testid="selected-school">{school}</output></>;
}
describe('account Kobra controls', () => {
  it('searches full school names, selects a stable ID with the keyboard and returns focus', async () => {
    const user = userEvent.setup();
    render(<SchoolHarness />);
    const trigger = screen.getByLabelText('School');
    await user.click(trigger);
    const search = await screen.findByRole('combobox', { name: 'Search schools' });
    await user.type(search, 'community');
    expect(screen.getAllByRole('option')).toHaveLength(2);
    await user.clear(search);
    await user.type(search, 'larkin');
    await user.keyboard('{ArrowDown}{Enter}');
    await waitFor(() => expect(screen.queryByRole('listbox')).toBeNull());
    expect(screen.getByTestId('selected-school')).toHaveTextContent('larkin');
    expect(trigger).toHaveTextContent('Larkin');
    await waitFor(() => expect(trigger).toHaveFocus());
    await user.click(trigger);
    await waitFor(() => expect(screen.getByRole('combobox', { name: 'Search schools' })).toHaveFocus());
    await user.keyboard('{Escape}');
    await waitFor(() => {
      expect(screen.queryByRole('listbox')).toBeNull();
      expect(trigger).toHaveFocus();
    });
    expect(screen.getByTestId('selected-school')).toHaveTextContent('larkin');
  });
  it('renames Grace Park while preserving the school account ID', async () => {
    const user = userEvent.setup();
    render(<SchoolHarness />);
    await user.click(screen.getByLabelText('School'));
    await user.type(await screen.findByRole('combobox', { name: 'Search schools' }), 'grace');
    await user.click(screen.getByRole('option', { name: 'Grace Park Community School' }));
    expect(screen.getByTestId('selected-school')).toHaveTextContent('rosmini');
    expect(getSchoolName('rosmini')).toBe('Grace Park Community School');
    expect(SCHOOL_NAMES.rosmini).toBe('Grace Park Community School');
  });
  it('has a no-results state and cannot open while disabled', async () => {
    const user = userEvent.setup();
    const { rerender } = render(<SchoolHarness />);
    await user.click(screen.getByLabelText('School'));
    await user.type(await screen.findByRole('combobox', { name: 'Search schools' }), 'does not exist');
    expect(screen.getByText('No schools found. Try another name.')).toBeVisible();
    expect(screen.queryAllByRole('option')).toHaveLength(0);
    await user.keyboard('{Escape}');
    rerender(<SchoolHarness disabled />);
    await user.click(screen.getByLabelText('School'));
    expect(screen.queryByRole('listbox')).toBeNull();
  });
  it('keeps school names available when an ornamental crest cannot load', () => {
    const { container } = render(<><SchoolCrest school="marino" /><span>Marino</span></>);
    const img = container.querySelector('img')!;
    fireEvent.error(img);
    expect(container.querySelector('img')).toBeNull();
    expect(screen.getByText('Marino')).toBeVisible();
    expect(container.querySelector('svg')).not.toBeNull();
  });
  it('offers all eight crew with one keyboard selection and ignores disabled tile clicks', async () => {
    const user = userEvent.setup(), changed = vi.fn();
    function CrewHarness({ disabled = false }) { const [value, setValue] = useState('star-crew:maker'); return <AccountCrewPicker value={value} onChange={v => { setValue(v); changed(v); }} disabled={disabled} />; }
    const { rerender } = render(<CrewHarness />);
    expect(screen.getAllByRole('radio')).toHaveLength(8);
    const maker = screen.getByRole('radio', { name: 'Maker' });
    maker.focus();
    await user.keyboard('{ArrowRight}');
    expect(screen.getByRole('radio', { name: 'Stargazer' })).toBeChecked();
    expect(changed).toHaveBeenCalledExactlyOnceWith('star-crew:stargazer');
    rerender(<CrewHarness disabled />);
    await user.click(screen.getByText('Reader', { selector: 'label > span' }));
    expect(changed).toHaveBeenCalledTimes(1);
  });
  it('toggles the animated checkbox using Space', async () => {
    const user = userEvent.setup();
    function Consent() { const [checked, setChecked] = useState(false); return <Checkbox checked={checked} onCheckedChange={setChecked} aria-label="Agree to terms" />; }
    const { container } = render(<Consent />);
    const box = screen.getByRole('checkbox', { name: 'Agree to terms' });
    box.focus();
    await user.keyboard(' ');
    expect(box).toBeChecked();
    expect(container.querySelector('[data-slot="checkbox-indicator"] path')).not.toBeNull();
    await user.keyboard(' ');
    expect(box).not.toBeChecked();
  });
});
