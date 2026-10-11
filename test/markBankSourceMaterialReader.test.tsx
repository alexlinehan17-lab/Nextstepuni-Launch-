import React from 'react';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SourceMaterialReader from '../components/MarkBank/SourceMaterialReader';
import sourceReview from '../scripts/markbank/authored/english-source-review.json';
import type { CardSourceMaterial } from '../types/markBank';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';
import { paperStoragePath, paperUrl } from '../components/PaperTrail/storage';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn().mockResolvedValue({}) }));
vi.mock('../components/PaperTrail/CropView', () => ({ default: () => <div>Official PDF page</div> }));

afterEach(() => { cleanup(); vi.clearAllMocks(); });

describe('Mark Bank source reader provenance', () => {
  it('opens attributed reading links for poems absent from the examination', async () => {
    const source = sourceReview.attachments['english-2014-ol-p2-prescribed-c-q2-iii'].additionalSources[0] as CardSourceMaterial;
    render(<SourceMaterialReader source={source} subjectId="english" year={2014} paperFileid="LC002GLP200EV" />);
    const trigger = screen.getByRole('button', { name: /Read OTHER STUDIED POEMS/ });
    fireEvent.click(trigger);
    expect(screen.getByRole('dialog')).toBeTruthy();
    expect(screen.getByText(source.presentationNote)).toBeTruthy();
    expect(vaultPdf).not.toHaveBeenCalled();
    expect(screen.queryByRole('button', { name: 'Zoom in' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Next source page' })).toBeNull();
    for (const reading of source.readings!) {
      const link = screen.getByRole('link', { name: `Read ${reading.title} Opens in a new tab` });
      expect(link.getAttribute('href')).toBe(reading.sourceUrl);
      expect(link.getAttribute('target')).toBe('_blank');
      expect(screen.getByText(reading.location)).toBeTruthy();
    }
    fireEvent.keyDown(document.body, { key: 'Escape' });
    expect(screen.queryByRole('dialog')).toBeNull();
    await waitFor(() => expect(document.activeElement).toBe(trigger));
  });

  it('opens the two Yeats reading editions without loading or claiming the parent exam PDF', async () => {
    const source = sourceReview.attachments['english-2010-ol-p2-prescribed-d-q2-iii'] as CardSourceMaterial;
    render(<SourceMaterialReader source={source} subjectId="english" year={2010} paperFileid="LC002GLP200EV" />);
    const trigger = screen.getByRole('button', { name: /Read THE TWO NAMED POEMS/ });
    fireEvent.click(trigger);
    expect(screen.getByRole('dialog')).toBeTruthy();
    expect(screen.getByText(source.presentationNote)).toBeTruthy();
    expect(screen.getByText('I hear it in the deep heart’s core.')).toBeTruthy();
    expect(screen.getByText('In balance with this life, this death.')).toBeTruthy();
    expect(vaultPdf).not.toHaveBeenCalled();
    expect(screen.queryByText(/printed page|exact examination text/i)).toBeNull();
    expect(screen.getByRole('link').getAttribute('href')).toBe(source.texts![0].sourceUrl);
    fireEvent.click(screen.getByRole('button', { name: 'Next poem' }));
    expect(screen.getByRole('link').getAttribute('href')).toBe(source.texts![1].sourceUrl);
    expect(screen.getByRole('button', { name: 'Next poem' }).hasAttribute('disabled')).toBe(true);
    fireEvent.click(screen.getByRole('button', { name: 'Previous poem' }));
    expect(screen.getByRole('link').getAttribute('href')).toBe(source.texts![0].sourceUrl);
    fireEvent.keyDown(screen.getByRole('dialog'), { key: 'Escape' });
    expect(screen.queryByRole('dialog')).toBeNull();
    await waitFor(() => expect(document.activeElement).toBe(trigger));
    fireEvent.click(trigger);
    fireEvent.click(screen.getByRole('button', { name: 'Close supplementary reading' }));
    expect(screen.queryByRole('dialog')).toBeNull();
  });

  it('retains the original SEC PDF reader for printed material', async () => {
    const source: CardSourceMaterial = {
      kind: 'source-text', label: 'UNSEEN POEM', title: 'Nettles', pages: [10],
      attribution: 'Vernon Scannell', presentationNote: 'Official examination page.',
    };
    render(<SourceMaterialReader source={source} subjectId="english" year={2010} paperFileid="LC002GLP200EV" />);
    fireEvent.click(screen.getByRole('button', { name: /Read UNSEEN POEM/ }));
    await screen.findByText('Official PDF page');
    expect(vaultPdf).toHaveBeenCalledOnce();
    expect(screen.getByText('Printed page 10')).toBeTruthy();
    expect(screen.getByRole('link', { name: 'Open the original paper' }).getAttribute('href')).toContain('#page=10');
  });

  it('loads an additional reading copy from its own examination year and file', async () => {
    const source: CardSourceMaterial = {
      kind: 'source-text', label: 'OTHER STUDIED POEM', title: 'Inversnaid', pages: [20],
      attribution: 'Gerard Manley Hopkins', sourceYear: 2021, sourceFileid: 'LC002GLP200EV',
      presentationNote: 'Reading copy from the 2021 examination.',
    };
    render(<SourceMaterialReader source={source} subjectId="english" year={2011} paperFileid="different-parent-file" />);
    fireEvent.click(screen.getByRole('button', { name: /Read OTHER STUDIED POEM/ }));
    await screen.findByText('Official PDF page');
    const expected = paperUrl(paperStoragePath('lc', 'english', 2021, 'paper', 'LC002GLP200EV.pdf'));
    expect(vaultPdf).toHaveBeenCalledWith(expected);
    expect(screen.getByRole('link', { name: 'Open the original paper' }).getAttribute('href')).toBe(expected + '#page=20');
    fireEvent.keyDown(document.body, { key: 'Escape' });
    expect(screen.queryByRole('dialog')).toBeNull();
  });
});
