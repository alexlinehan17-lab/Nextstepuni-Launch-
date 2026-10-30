import React from 'react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import PdfRuler, { printedCentimetres } from '../components/MarkBank/PdfRuler';

describe('physical Mathematics diagram measurements', () => {
  it('uses PDF physical dimensions for both axes', () => {
    expect(printedCentimetres({ x: 0, y: 0 }, { x: .5, y: 0 }, 144, 72)).toBeCloseTo(2.54);
    expect(printedCentimetres({ x: 0, y: 0 }, { x: 0, y: 1 }, 144, 72)).toBeCloseTo(2.54);
    expect(printedCentimetres({ x: 0, y: 0 }, { x: 1, y: 1 }, 216, 288)).toBeCloseTo(12.7);
  });

  it('reports the same length after zoom and supports keyboard placement', async () => {
    const onMeasure = vi.fn();
    const pdf = { getPage: async () => ({ getViewport: () => ({ width: 600, height: 800 }) }) } as unknown as PDFDocumentProxy;
    render(<PdfRuler pdf={pdf} page={16} onMeasure={onMeasure} />);
    const ruler = await screen.findByRole('button', { name: /Printed-page ruler/ });
    const rect = (width: number) => ({ left: 0, top: 0, width, height: width * 4 / 3 }) as DOMRect;
    vi.spyOn(ruler, 'getBoundingClientRect').mockReturnValue(rect(300));
    fireEvent.click(ruler, { detail: 1, clientX: 0, clientY: 0 });
    fireEvent.click(ruler, { detail: 1, clientX: 36, clientY: 0 });
    expect(onMeasure).toHaveBeenLastCalledWith(2.54);
    vi.mocked(ruler.getBoundingClientRect).mockReturnValue(rect(600));
    fireEvent.click(ruler, { detail: 1, clientX: 0, clientY: 0 });
    fireEvent.click(ruler, { detail: 1, clientX: 72, clientY: 0 });
    expect(onMeasure).toHaveBeenLastCalledWith(2.54);
    fireEvent.click(ruler, { detail: 0 });
    fireEvent.keyDown(ruler, { key: 'ArrowRight', shiftKey: true });
    fireEvent.click(ruler, { detail: 0 });
    expect(onMeasure.mock.calls.at(-1)![0]).toBeCloseTo(10 * 2.54 / 72);
  });
});
