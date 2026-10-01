import React from 'react';
import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import { FieldShell, TextField } from '@/components/ui/FormControls';

test('associates a field label and local validation with the input', () => {
  render(<FieldShell label="Email" error="Check the email address."><TextField type="email" /></FieldShell>);
  const input = screen.getByRole('textbox', { name: 'Email' });
  expect(input).toHaveAttribute('aria-invalid', 'true');
  expect(input).toHaveAccessibleDescription('Check the email address.');
});

test('keeps existing guidance and entered data when adding or removing an error', () => {
  const { rerender } = render(<><span id="existing-note">Use your school address.</span><FieldShell label="Email" hint="You can change this later." error="Check the email address."><TextField id="email" defaultValue="DDWE" aria-describedby="existing-note" /></FieldShell></>);
  const input = screen.getByLabelText('Email');
  expect(input).toHaveAccessibleDescription('Use your school address. You can change this later. Check the email address.');
  rerender(<><span id="existing-note">Use your school address.</span><FieldShell label="Email" hint="You can change this later."><TextField id="email" defaultValue="DDWE" aria-describedby="existing-note" /></FieldShell></>);
  expect(input).toHaveValue('DDWE');
  expect(input).not.toHaveAttribute('aria-invalid', 'true');
  expect(input).toHaveAccessibleDescription('Use your school address. You can change this later.');
});
