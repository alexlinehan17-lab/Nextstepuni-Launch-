/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ask the papers — loading and searching the question index that
 * scripts/landing/ask-index.mjs writes to public/assets/landing/ask/. One
 * JSON per subject: its papers (year, level, paper label, SEC file id) and
 * its questions as [paper index, printed number, page, text]. Search runs
 * on the shared marker's tokens() so "cells" finds "cell" and "digested"
 * finds "digest"; the last word typed matches as a prefix so the grid
 * lights from the first keystroke.
 */

import { tokens } from '../marking/marker';

export interface AskPaper { y: number; l: 'H' | 'O'; p: string; f: string }
export interface AskSubject { id: string; name: string; attributionName: string }
interface AskSubjectFile extends AskSubject { years: number[]; papers: AskPaper[]; q: [number, string, number, string][] }
export interface AskIndexFile { subjects: { id: string; name: string; file: string; questions: number; years: number[] }[]; years: number[] }
export type AskMode = 'topics' | 'words';
export interface AskTopic { id: string; label: string; aliases: string[] }
export interface AskTopicIndexFile {
  topics: AskTopic[];
  papers: (AskPaper & { subjectId: string })[];
  q: [number, string, number, number[]][];
}

export interface AskQuestion {
  subject: AskSubject;
  paper: AskPaper;
  /** As printed: "Q4", "Question A", or a single-text letter. */
  n: string;
  page: number;
  text: string;
  stems: Set<string>;
  list: string[];
  topics?: AskTopic[];
  /** Exact Paper Trail question identity; absent in the independent text index. */
  anchor?: string;
}
export interface AskData { subjects: AskSubject[]; years: number[]; questions: AskQuestion[]; topicQuestions: AskQuestion[]; topicCoverage: Set<string> }

export const ASK_BASE = '/assets/landing/ask/';

const getJson = async <T,>(url: string): Promise<T> => {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return (await r.json()) as T;
};

/** The shape of the grid — subjects and years — a few hundred bytes, fetched on mount. */
export const loadAskIndex = (base: string = ASK_BASE): Promise<AskIndexFile> => getJson<AskIndexFile>(`${base}index.json`);

/** The questions themselves (~1 MB across the subject files), fetched on the input's first focus. */
export const loadAsk = async (index: AskIndexFile, base: string = ASK_BASE): Promise<AskData> => {
  const [files, tagged] = await Promise.all([
    Promise.all(index.subjects.map(s => getJson<AskSubjectFile>(base + s.file))),
    getJson<AskTopicIndexFile>(`${base}topics.json`),
  ]);
  const subjects: AskSubject[] = [];
  const questions: AskQuestion[] = [];
  for (const f of files) {
    const subject: AskSubject = { id: f.id, name: f.name, attributionName: f.attributionName };
    subjects.push(subject);
    for (const [pi, n, page, text] of f.q) {
      const list = Array.from(new Set(tokens(text)));
      questions.push({ subject, paper: f.papers[pi], n, page, text, stems: new Set(list), list });
    }
  }
  const topicQuestions: AskQuestion[] = tagged.q.map(([pi, n, page, ids]) => {
    const paper = tagged.papers[pi];
    const subject = subjects.find(s => s.id === paper.subjectId);
    if (!subject) throw new Error(`Unknown topic-search subject: ${paper.subjectId}`);
    return { subject, paper, n: `Q${n}`, anchor: n, page, text: '', stems: new Set<string>(), list: [], topics: ids.map(id => tagged.topics[id]) };
  });
  return { subjects, years: index.years, questions, topicQuestions, topicCoverage: new Set(tagged.papers.map(p => `${p.subjectId}|${p.y}`)) };
};

/** The typed term as stems. Every word but the last must match whole; the last may be a prefix. */
export const queryTerms = (query: string): string[] => tokens(query).filter(t => /[a-z0-9]/.test(t));

export const matches = (q: Pick<AskQuestion, 'stems' | 'list'>, terms: string[]): boolean => {
  if (!terms.length) return false;
  const last = terms[terms.length - 1];
  for (let i = 0; i < terms.length - 1; i++) if (!q.stems.has(terms[i])) return false;
  if (q.stems.has(last)) return true;
  for (const s of q.list) if (s.startsWith(last)) return true;
  return false;
};

/** Match one complete topic label/alias; words cannot straddle unrelated tags. */
const topicTokens = new Map<string, { stems: Set<string>; list: string[] }>();
export const matchingTopics = (q: AskQuestion, terms: string[]): AskTopic[] =>
  (q.topics ?? []).filter(topic => [topic.label, ...topic.aliases].some(label => {
    let cached = topicTokens.get(label);
    if (!cached) {
      const list = queryTerms(label);
      cached = { list, stems: new Set(list) };
      topicTokens.set(label, cached);
    }
    return matches(cached, terms);
  })).filter((topic, i, all) => all.findIndex(t => t.label === topic.label) === i);

const isHit = (word: string, terms: string[]): boolean => {
  const ts = tokens(word);
  if (!ts.length || !terms.length) return false;
  const last = terms[terms.length - 1];
  return ts.some(t => terms.includes(t) || t.startsWith(last));
};

/** Sentences, split the way the index script splits them. */
export const sentences = (text: string): string[] =>
  text.split(/(?<=[.?!])\s+(?=[A-Z“"‘(\d])/).map(s => s.trim()).filter(Boolean);

/** The first sentence carrying the term; the opening sentence when none does on its own (a two-word term can straddle two). */
export const sentenceFor = (q: AskQuestion, terms: string[]): string => {
  const ss = sentences(q.text);
  return ss.find(s => s.split(/\s+/).some(w => isHit(w, terms))) ?? ss[0] ?? q.text;
};

/** The sentence as runs, each flagged when it carries the term, so the page can mark it. */
export const highlight = (sentence: string, terms: string[]): { text: string; hit: boolean }[] => {
  const out: { text: string; hit: boolean }[] = [];
  for (const run of sentence.split(/(\s+)/)) {
    if (!run) continue;
    const hit = !/^\s+$/.test(run) && isHit(run, terms);
    const prev = out[out.length - 1];
    if (prev && prev.hit === hit) prev.text += run;
    else out.push({ text: run, hit });
  }
  return out;
};

/** Higher before Ordinary, then paper, then the printed number. */
export const byPaperOrder = (a: AskQuestion, b: AskQuestion): number =>
  a.paper.l.localeCompare(b.paper.l) || a.paper.p.localeCompare(b.paper.p) || (parseInt(a.n.replace(/\D/g, ''), 10) || 0) - (parseInt(b.n.replace(/\D/g, ''), 10) || 0) || a.n.localeCompare(b.n);
