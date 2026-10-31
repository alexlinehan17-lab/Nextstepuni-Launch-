import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, waitFor, fireEvent } from "@testing-library/react";
import Lenis from "lenis";
import {saveAttemptFirst,loadAttemptFirst,readAnswer} from "../components/PaperTrail/answerDeskStore";
import Viewer from "../components/PaperTrail/Viewer";
import { topicsForPaper } from "../components/PaperTrail/topics";
vi.mock("../components/PaperTrail/pdfjsLoader", () => ({
  loadPdfjs: () => new Promise(() => {}),
}));
vi.mock("../components/PaperTrail/pdfCache", () => ({
  fetchPdfCached: vi.fn(() => Promise.resolve(null)),
}));
const paper = { url: "/test-paper.pdf", label: "Paper", bytes: 100 };
const scheme = { url: "/test-scheme.pdf", label: "Scheme", bytes: 100 };
beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal(
    "fetch",
    vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ v: 1, q: [] }),
      }),
    ),
  );
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});
describe("Paper Trail previews", () => {
  it("makes verified French audio available while the aural booklet loads", () => {
    render(<Viewer title="2026 French listening" paper={paper}
      topics={topicsForPaper('french', 2026, 'ordinary', 'ev', 'LC010GLPA00BV.pdf')!}
      onClose={() => {}} />);
    const player = screen.getByRole('dialog').querySelector('audio');
    expect(player).toHaveAttribute('src', 'https://www.examinations.ie/archive/exampapers/2026/LC010CLP017EV.mp3');
    expect(player).toHaveAttribute('controls');
  });
  it("exempts the portalled viewer from the landing page scroll controller", () => {
    render(<Viewer title="Test paper" paper={paper} onClose={() => {}} />);
    const pageScroll = new Lenis();
    pageScroll.stop();
    try {
      const outside = new WheelEvent("wheel", {
        bubbles: true,
        cancelable: true,
        deltaY: 120,
      });
      document.body.dispatchEvent(outside);
      expect(outside.defaultPrevented).toBe(true);
      const inside = new WheelEvent("wheel", {
        bubbles: true,
        cancelable: true,
        deltaY: 120,
      });
      screen.getByRole("dialog").dispatchEvent(inside);
      expect(inside.defaultPrevented).toBe(false);
    } finally {
      pageScroll.destroy();
    }
  });
  it("opens with Answers enabled and requests its map without requiring a click", async () => {
    saveAttemptFirst("anon",false);
    render(
      <Viewer
        title="Test paper"
        paper={paper}
        scheme={scheme}
        answersUrl="/answer-map.json"
        initialAnswersOn
        onClose={() => {}}
      />,
    );
    expect(
      screen.getByRole("button", {
        name: "Show the marking scheme beside each question",
      }),
    ).toHaveAttribute("aria-pressed", "true");
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/answer-map.json"));
    expect(fetch).toHaveBeenCalledTimes(1);
  });
  it("leaves normal app opens unchanged, with Answers off", () => {
    saveAttemptFirst("anon",false);
    render(
      <Viewer
        title="Test paper"
        paper={paper}
        scheme={scheme}
        answersUrl="/answer-map.json"
        onClose={() => {}}
      />,
    );
    expect(
      screen.getByRole("button", {
        name: "Show the marking scheme beside each question",
      }),
    ).toHaveAttribute("aria-pressed", "false");
    expect(fetch).not.toHaveBeenCalled();
  });
});


describe('Paper Trail desktop question workspace', () => {
  it('keeps Paper/Scheme switching available beside the answer workspace', () => {
    saveAttemptFirst("anon",false);
    const matchMedia = vi.spyOn(window, 'matchMedia').mockImplementation(query => ({matches:query === '(min-width: 768px)', media:query, onchange:null, addListener:vi.fn(), removeListener:vi.fn(), addEventListener:vi.fn(), removeEventListener:vi.fn(), dispatchEvent:vi.fn()}));
    try {
      render(<Viewer title="Test paper" paper={paper} scheme={scheme} answersUrl="/answer-map.json" initialAnswersOn onClose={() => {}} />);
      expect(screen.getByRole('complementary', {name:'Question workspace'})).toBeInTheDocument();
      expect(screen.getByRole('tab', {name:'Paper'})).toHaveAttribute('aria-selected','true');
      fireEvent.click(screen.getByRole('tab', {name:'Scheme'}));
      expect(screen.getByRole('tab', {name:'Scheme'})).toHaveAttribute('aria-selected','true');
      expect(screen.queryByRole('complementary', {name:'Question workspace'})).not.toBeInTheDocument();
      fireEvent.click(screen.getByRole('tab', {name:'Paper'}));
      expect(screen.getByRole('complementary', {name:'Question workspace'})).toBeInTheDocument();
    } finally {matchMedia.mockRestore();}
  });
});

describe('Attempt first in the real reader',()=>{
 it('defaults on even when an older caller requested automatic answers',async()=>{
  render(<Viewer title="Test paper" paper={paper} scheme={scheme} answersUrl="/answer-map.json" initialAnswersOn onClose={()=>{}}/>);
  expect(screen.getByRole('switch',{name:'Attempt first'})).toBeChecked();
  expect(screen.getByRole('complementary',{name:'Your answer desk'})).toBeInTheDocument();
  expect(screen.queryByRole('button',{name:'Show the marking scheme beside each question'})).not.toBeInTheDocument();
  expect(screen.getByText('Scheme hidden until you choose to reveal.')).toBeInTheDocument();
  await waitFor(()=>expect(fetch).toHaveBeenCalledWith('/answer-map.json'));
 });
 it('preserves a draft through off/on, remembers off after reopening, and restores it when enabled',()=>{
  const props={title:'Test paper',paper,scheme,storageNs:'student|paper',onClose:()=>{}};
  const view=render(<Viewer {...props}/>);
  fireEvent.change(screen.getByLabelText('Your attempt'),{target:{value:'My method before the reveal'}});
  fireEvent.click(screen.getByRole('switch',{name:'Attempt first'}));
  expect(screen.queryByRole('complementary',{name:'Your answer desk'})).not.toBeInTheDocument();
  view.unmount();render(<Viewer {...props}/>);
  expect(screen.getByRole('switch',{name:'Attempt first'})).not.toBeChecked();
  fireEvent.click(screen.getByRole('switch',{name:'Attempt first'}));
  expect(screen.getByLabelText('Your attempt')).toHaveValue('My method before the reveal');
 });
 it('keeps both attempts and reflection, hides the scheme on retry, and restores work on reopen',()=>{
  const props={title:'Test paper',paper,scheme,storageNs:'student|paper',onClose:()=>{}};
  const view=render(<Viewer {...props}/>);
  fireEvent.change(screen.getByLabelText('Your attempt'),{target:{value:'First answer'}});
  // A paper without question links deliberately opens the full original scheme.
  fireEvent.click(screen.getByRole('button',{name:'Keep my attempt & reveal'}));
  expect(screen.getByRole('tab',{name:'Scheme'})).toHaveAttribute('aria-selected','true');
  fireEvent.click(screen.getByRole('tab',{name:'Paper'}));
  expect(screen.getByText('First answer')).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText('One thing to take into the next attempt.'),{target:{value:'Include the original cost.'}});
  fireEvent.click(screen.getByRole('button',{name:'Try again without the scheme'}));
  expect(screen.queryByText('First answer')).not.toBeInTheDocument();
  expect(screen.getByText('Scheme and comparison hidden.')).toBeInTheDocument();
  expect(screen.getByLabelText('Your second attempt')).toHaveValue('');
  fireEvent.change(screen.getByLabelText('Your second attempt'),{target:{value:'Better answer'}});
  fireEvent.click(screen.getByRole('button',{name:'Keep both attempts'}));
  view.unmount();render(<Viewer {...props}/>);
  expect(screen.getByText('First answer')).toBeInTheDocument();expect(screen.getByText('Better answer')).toBeInTheDocument();expect(screen.getByText('Include the original cost.')).toBeInTheDocument();
  expect(readAnswer('student|paper','page:1').record.first?.text).toBe('First answer');
 });
 it('starts a separate workspace if the same viewer changes papers',()=>{
  const view=render(<Viewer title="First paper" paper={paper} storageNs="student|paper1" onClose={()=>{}}/>);
  fireEvent.change(screen.getByLabelText('Your attempt'),{target:{value:'Paper one work'}});
  view.rerender(<Viewer title="Second paper" paper={{...paper,url:'/paper2.pdf'}} storageNs="student|paper2" onClose={()=>{}}/>);
  expect(screen.getByLabelText('Your attempt')).toHaveValue('');
  expect(readAnswer('student|paper1','page:1').record.draft.text).toBe('Paper one work');
 });
});


describe('Attempt-first save failures',()=>{
 it('keeps unsaved text in memory, shows an honest error and lets the student cancel leaving',()=>{
  const onClose=vi.fn();
  render(<Viewer title="Test" paper={paper} scheme={scheme} storageNs="student|save-failure" onClose={onClose}/>);
  vi.spyOn(Storage.prototype,'setItem').mockImplementation(()=>{throw new DOMException('Full','QuotaExceededError');});
  const confirm=vi.spyOn(window,'confirm').mockReturnValue(false);
  fireEvent.change(screen.getByLabelText('Your attempt'),{target:{value:'Do not lose my method'}});
  expect(screen.getByRole('alert')).toHaveTextContent('could not save');
  fireEvent.click(screen.getByRole('button',{name:'Close viewer'}));
  expect(confirm).toHaveBeenCalled();expect(onClose).not.toHaveBeenCalled();
  expect(screen.getByLabelText('Your attempt')).toHaveValue('Do not lose my method');
  const leaving=new Event('beforeunload',{cancelable:true});window.dispatchEvent(leaving);
  expect(leaving.defaultPrevented).toBe(true);
 });
 it('retains written work even when no marking scheme is linked',()=>{
  render(<Viewer title="Test" paper={paper} storageNs="student|no-scheme" onClose={()=>{}}/>);
  fireEvent.change(screen.getByLabelText('Your attempt'),{target:{value:'Work without a scheme'}});
  expect(screen.getByRole('button',{name:'Keep my attempt & reveal'})).toBeDisabled();
  expect(readAnswer('student|no-scheme','page:1').record.draft.text).toBe('Work without a scheme');
 });
});


describe('Existing study tools alongside Attempt first',()=>{
 it('keeps Triage, Self-mark and Full Loop discoverable without replacing the saved default',async()=>{
  render(<Viewer title="Test" paper={paper} scheme={scheme} answersUrl="/answer-map.json" storageNs="student|tools" onClose={()=>{}}/>);
  fireEvent.change(screen.getByLabelText('Your attempt'),{target:{value:'My kept work'}});
  fireEvent.click(screen.getByRole('button',{name:'Study tools for this paper'}));
  expect(await screen.findByRole('menuitem',{name:/Triage/})).toBeInTheDocument();
  expect(screen.getByRole('menuitemcheckbox',{name:/Self-mark/})).toBeInTheDocument();
  fireEvent.click(screen.getByRole('menuitemcheckbox',{name:/The Full Loop/}));
  expect(screen.getByRole('switch',{name:'Attempt first'})).not.toBeChecked();
  expect(loadAttemptFirst('student|tools')).toBe(true);
  fireEvent.click(screen.getByRole('switch',{name:'Attempt first'}));
  expect(screen.getByLabelText('Your attempt')).toHaveValue('My kept work');
 });
});

describe('Resizable answer desk',()=>{
 it('supports keyboard resizing and collapse without changing the attempt or mode preference',()=>{
  const matchMedia=vi.spyOn(window,'matchMedia').mockImplementation(query=>({matches:query==='(min-width: 768px)',media:query,onchange:null,addListener:vi.fn(),removeListener:vi.fn(),addEventListener:vi.fn(),removeEventListener:vi.fn(),dispatchEvent:vi.fn()}));
  render(<Viewer title="Test" paper={paper} scheme={scheme} storageNs="student|resize" onClose={()=>{}}/>);
  fireEvent.change(screen.getByLabelText('Your attempt'),{target:{value:'Keep this answer while I resize.'}});
  const handle=screen.getByRole('separator',{name:'Resize answer desk'});
  expect(handle).toHaveAttribute('aria-orientation','vertical');
  const original=Number(handle.getAttribute('aria-valuenow'));
  fireEvent.keyDown(handle,{key:'ArrowLeft'});
  expect(Number(handle.getAttribute('aria-valuenow'))).toBeGreaterThan(original);
  fireEvent.click(screen.getByRole('button',{name:'Minimise answer desk'}));
  expect(screen.queryByLabelText('Your attempt')).not.toBeVisible();
  expect(screen.getByRole('switch',{name:'Attempt first'})).toBeChecked();
  fireEvent.click(screen.getByRole('button',{name:'Expand answer desk'}));
  expect(screen.getByLabelText('Your attempt')).toHaveValue('Keep this answer while I resize.');
  expect(Number(screen.getByRole('separator',{name:'Resize answer desk'}).getAttribute('aria-valuenow'))).toBeGreaterThan(original);
  matchMedia.mockRestore();
 });
});
