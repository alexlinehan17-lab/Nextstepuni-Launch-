/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail viewer — zooming keeps the student on the page they were
 * reading. Zoom widens every page and page heights follow the width, so an
 * unchanged scrollTop used to land on another page while the counter still
 * named the old one (opened at page 14 of 40, Zoom in showed page 8).
 *
 * jsdom has no layout, so the reader's geometry is modelled here from the
 * same inputs a browser uses: the content wrapper's width and max-width, and
 * each page's padding-bottom aspect ratio.
 */

import React from 'react';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';
import Viewer from '../components/PaperTrail/Viewer';
import {readAnswer} from '../components/PaperTrail/answerDeskStore';
import type * as PdfjsLoader from '../components/PaperTrail/pdfjsLoader';

const PAGES = 40;
let VIEW_W = 1000;
const VIEW_H = 800;
const PAD_Y = 12; // py-3 on the content wrapper
const PAD_X = 8; // px-2
const GAP = 10; // mb-2.5 under each page

vi.mock('../components/PaperTrail/pdfjsLoader', async importOriginal => {
  const real = await importOriginal<typeof PdfjsLoader>();
  const page = {
    getViewport: ({ scale }: { scale: number }) => ({ width: 1000 * scale, height: 1414 * scale }),
    render: () => ({ promise: Promise.resolve(), cancel: () => {} }),
    cleanup: () => {},
  };
  const doc = { numPages: 40, getPage: () => Promise.resolve(page), destroy: () => Promise.resolve() };
  const lib = {
    version: 'test',
    getDocument: () => ({ promise: Promise.resolve(doc), destroy: () => Promise.resolve() }),
  };
  return { ...real, loadPdfjs: () => Promise.resolve(lib) };
});
vi.mock('../components/PaperTrail/pdfCache', () => ({
  fetchPdfCached: vi.fn(() => Promise.resolve(new ArrayBuffer(8))),
}));

// ── layout model ──
const isReader = (el: Element) => /^Paper, page /.test(el.getAttribute('aria-label') ?? '');
const readerOf = (el: Element) => el.closest<HTMLElement>('[aria-label^="Paper, page "]');
const contentWidth = (reader: HTMLElement) => {
  const wrapper = reader.querySelector<HTMLElement>('[data-page]')?.parentElement;
  if (!wrapper) return VIEW_W;
  const width = (VIEW_W * parseFloat(wrapper.style.width)) / 100;
  return wrapper.style.maxWidth ? Math.min(width, parseFloat(wrapper.style.maxWidth)) : width;
};
const pageHeight = (page: HTMLElement, width: number) => (width * parseFloat(page.style.paddingBottom)) / 100;
const pageBox = (page: HTMLElement) => {
  const reader = readerOf(page)!;
  const width = contentWidth(reader) - 2 * PAD_X;
  let top = PAD_Y;
  for (const other of reader.querySelectorAll<HTMLElement>('[data-page]')) {
    if (other === page) break;
    top += pageHeight(other, width) + GAP;
  }
  return { top, width, height: pageHeight(page, width) };
};
const scrollHeight = (reader: HTMLElement) => {
  const pages = [...reader.querySelectorAll<HTMLElement>('[data-page]')];
  const last = pages[pages.length - 1];
  if (!last) return VIEW_H;
  const box = pageBox(last);
  return box.top + box.height + GAP + PAD_Y;
};

const scroll = new WeakMap<Element, { top: number; left: number }>();
const position = (el: Element) => {
  let p = scroll.get(el);
  if (!p) scroll.set(el, (p = { top: 0, left: 0 }));
  return p;
};
const setScroll = (el: HTMLElement, axis: 'top' | 'left', value: number) => {
  const p = position(el);
  const max = axis === 'top'
    ? Math.max(0, scrollHeight(el) - VIEW_H)
    : Math.max(0, contentWidth(el) - VIEW_W);
  const next = Math.min(max, Math.max(0, value));
  if (next === p[axis]) return;
  p[axis] = next;
  // Browsers report a scroll position change with an asynchronous scroll event.
  setTimeout(() => el.dispatchEvent(new Event('scroll')), 0);
};

const saved: Array<[object, string, PropertyDescriptor | undefined]> = [];
const stub = (proto: object, key: string, descriptor: PropertyDescriptor) => {
  saved.push([proto, key, Object.getOwnPropertyDescriptor(proto, key)]);
  Object.defineProperty(proto, key, { configurable: true, ...descriptor });
};
beforeAll(() => {
  const P = HTMLElement.prototype;
  const E = Element.prototype;
  // Pages paint into canvases; jsdom has no 2D context and the model needs none.
  stub(HTMLCanvasElement.prototype, 'getContext', { value: () => null });
  stub(P, 'offsetTop', { get(this: HTMLElement) { return this.dataset.page ? pageBox(this).top : 0; } });
  stub(P, 'offsetHeight', { get(this: HTMLElement) { return this.dataset.page ? pageBox(this).height : 0; } });
  stub(E, 'clientHeight', { get(this: HTMLElement) { return isReader(this) ? VIEW_H : this.dataset?.page ? pageBox(this).height : 0; } });
  stub(E, 'clientWidth', {
    get(this: HTMLElement) {
      if (isReader(this)) return VIEW_W;
      return this.dataset?.page ? pageBox(this).width : 0;
    },
  });
  stub(E, 'scrollWidth', { get(this: HTMLElement) { return isReader(this) ? Math.max(VIEW_W, contentWidth(this)) : 0; } });
  stub(E, 'scrollTop', {
    get(this: HTMLElement) { return isReader(this) ? position(this).top : 0; },
    set(this: HTMLElement, v: number) { if (isReader(this)) setScroll(this, 'top', v); },
  });
  stub(E, 'scrollLeft', {
    get(this: HTMLElement) { return isReader(this) ? position(this).left : 0; },
    set(this: HTMLElement, v: number) { if (isReader(this)) setScroll(this, 'left', v); },
  });
  stub(E, 'scrollTo', {
    value(this: HTMLElement, opts: ScrollToOptions) {
      if (opts.top != null) this.scrollTop = opts.top;
      if (opts.left != null) this.scrollLeft = opts.left;
    },
  });
});
afterAll(() => {
  for (const [proto, key, descriptor] of saved.reverse()) {
    if (descriptor) Object.defineProperty(proto, key, descriptor);
    else delete (proto as Record<string, unknown>)[key];
  }
});
beforeEach(() => { VIEW_W = 1000; localStorage.clear(); });
afterEach(cleanup);

/** The page a student sees in the middle of the reader, from the model. */
const pageInMiddle = (reader: HTMLElement) => {
  const middle = position(reader).top + VIEW_H / 2;
  let current = 1;
  for (const page of reader.querySelectorAll<HTMLElement>('[data-page]')) {
    if (pageBox(page).top <= middle) current = Number(page.dataset.page);
    else break;
  }
  return current;
};
const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 20)));

describe('Paper Trail viewer zoom', () => {
  it('moves to the next question lower on the same page, then to a later page, retaining the original work', async () => {
    const questions=[{n:'1',pP:4,pY:[.1,.5]},{n:'2',pP:4,pY:[.6,1]},{n:'3',pP:6,pY:[.1,1]}].map(q=>({...q,mode:'pagejump',region:[{p:7}]}));
    const fetchSpy=vi.spyOn(globalThis,'fetch').mockResolvedValue({ok:true,json:async()=>({v:1,paperFileid:'paper.pdf',q:questions})} as Response);
    try {
      render(<Viewer title="Paper" paper={{url:'/paper.pdf',label:'Paper',bytes:0}} scheme={{url:'/scheme.pdf',label:'Scheme',bytes:0}} answersUrl="/map.json" storageNs="student|next-question" initialPaperPage={4} onClose={()=>{}} />);
      const reader=await screen.findByLabelText(`Paper, page 4 of ${PAGES}`);
      await waitFor(()=>expect(screen.getByLabelText('Working on')).toHaveValue('1'));
      await settle();
      fireEvent.change(screen.getByLabelText('Your attempt'),{target:{value:'Keep this first answer'}});
      fireEvent.click(screen.getByRole('button',{name:'Keep my attempt & reveal'}));
      const before=position(reader).top;
      fireEvent.click(screen.getByRole('button',{name:'Move to next question'}));
      await settle();
      expect(screen.getByLabelText('Working on')).toHaveValue('2');
      expect(position(reader).top).toBeGreaterThan(before+400);
      expect(pageInMiddle(reader)).toBe(4);
      expect(screen.getByText('Scheme hidden until you choose to reveal.')).toBeInTheDocument();
      expect(readAnswer('student|next-question','1').record.first?.text).toBe('Keep this first answer');
      fireEvent.click(screen.getByRole('button',{name:'Keep my attempt & reveal'}));
      fireEvent.click(screen.getByRole('button',{name:'Move to next question'}));
      await settle();
      expect(screen.getByLabelText('Working on')).toHaveValue('3');
      expect(pageInMiddle(reader)).toBe(6);
      fireEvent.click(screen.getByRole('button',{name:'Keep my attempt & reveal'}));
      expect(screen.queryByRole('button',{name:'Move to next question'})).not.toBeInTheDocument();
    } finally {fetchSpy.mockRestore();}
  });

  it('jumps to an entered page from the header and bounds the destination to the document', async () => {
    render(<Viewer title="Paper" paper={{url:'/paper.pdf',label:'Paper',bytes:0}} initialPaperPage={14} onClose={()=>{}} />);
    const reader=await screen.findByLabelText(`Paper, page 14 of ${PAGES}`);
    await waitFor(()=>expect(position(reader).top).toBeGreaterThan(0));
    const pageInput=screen.getByRole('spinbutton',{name:'Go to page'});
    fireEvent.change(pageInput,{target:{value:'23'}});
    fireEvent.submit(screen.getByRole('form',{name:'Page navigation'}));
    await settle();
    expect(pageInMiddle(reader)).toBe(23);
    fireEvent.change(pageInput,{target:{value:'999'}});
    fireEvent.blur(pageInput);
    await settle();
    expect(pageInMiddle(reader)).toBe(PAGES);
    expect(pageInput).toHaveValue(PAGES);
  });

  it('keeps the reading point when the viewport changes to phone width', async () => {
    render(<Viewer title="Paper" paper={{url:'/paper.pdf',label:'Paper',bytes:0}} initialPaperPage={14} onClose={()=>{}} />);
    const reader = await screen.findByLabelText(`Paper, page 14 of ${PAGES}`);
    await waitFor(() => expect(position(reader).top).toBeGreaterThan(0));
    await settle();
    VIEW_W = 390;
    fireEvent(window, new Event('resize'));
    await act(() => new Promise(resolve => setTimeout(resolve, 350)));
    await settle();
    expect(pageInMiddle(reader)).toBe(14);
    expect(reader).toHaveAttribute('aria-label', `Paper, page 14 of ${PAGES}`);
  });

  it('keeps the page being read, and the counter, through every zoom step', async () => {
    render(<Viewer title="Agricultural Science" paper={{ url: '/paper.pdf', label: 'Paper', bytes: 0 }} initialPaperPage={14} onClose={() => {}} />);
    const reader = await screen.findByLabelText(`Paper, page 14 of ${PAGES}`);
    await waitFor(() => expect(position(reader).top).toBeGreaterThan(0));
    await settle();
    expect(pageInMiddle(reader)).toBe(14);

    const zoomIn = screen.getByRole('button', { name: 'Zoom in' });
    const zoomOut = screen.getByRole('button', { name: 'Zoom out' });
    const steps = [zoomIn, zoomIn, zoomIn, zoomIn, zoomOut, zoomOut, zoomOut, zoomOut, zoomOut];
    const seen: Array<{ width: string; middle: number; label: string | null }> = [];
    for (const button of steps) {
      fireEvent.click(button);
      await settle();
      const wrapper = reader.querySelector<HTMLElement>('[data-page]')!.parentElement!;
      seen.push({ width: wrapper.style.width, middle: pageInMiddle(reader), label: reader.getAttribute('aria-label') });
    }
    expect(seen.map(s => s.width)).toEqual(['125%', '150%', '200%', '250%', '200%', '150%', '125%', '100%', '75%']);
    for (const step of seen) {
      expect(step).toMatchObject({ middle: 14, label: `Paper, page 14 of ${PAGES}` });
    }
  });

  it('keeps the horizontal middle when zooming a page wider than the reader', async () => {
    render(<Viewer title="Agricultural Science" paper={{ url: '/paper.pdf', label: 'Paper', bytes: 0 }} initialPaperPage={14} onClose={() => {}} />);
    const reader = await screen.findByLabelText(`Paper, page 14 of ${PAGES}`);
    await waitFor(() => expect(position(reader).top).toBeGreaterThan(0));
    const zoomIn = screen.getByRole('button', { name: 'Zoom in' });
    for (let i = 0; i < 3; i++) { fireEvent.click(zoomIn); await settle(); } // 200%: content 2000px wide
    reader.scrollLeft = 300; // middle of the view at (300 + 500) / 2000 = 0.4 of the page width
    await settle();
    fireEvent.click(zoomIn); // 250%: content 2500px wide
    await settle();
    expect(reader.scrollLeft).toBe(0.4 * 2500 - 500);
    expect(pageInMiddle(reader)).toBe(14);
  });
});
