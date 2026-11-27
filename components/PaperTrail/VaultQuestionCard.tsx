/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — Topic Vault question card. One past-paper question as it was
 * actually printed: the real paper crop (diagrams, tables, source material
 * included), synthesised from the answer-map anchors, with the verified
 * marking-scheme crop behind a show/hide toggle.
 *
 * Everything degrades honestly: no sidecar / no confident region / render
 * failure → a compact row that still opens the question in the full paper.
 * We never show a crop we can't stand over.
 */

import React, { lazy, Suspense, useEffect, useMemo, useRef, useState } from 'react';
import { Check, Plus } from 'lucide-react';
import { Arrow, Button, IconButton, TextButton } from '../ui/Button';
import { List, Row } from '../ui/List';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import { type PaperAnswerMap, type PaperAnswerQuestion } from '../../types/paperTrail';
import CropView from './CropView';
import SourceMaterialReader from '../MarkBank/SourceMaterialReader';
import { paperRegionFor, schemeRegionFor } from './paperRegion';
import { vaultPdf } from './vaultDocs';
import {
  answerMapUrls,
  isAnswerMap,
  mergePaperAnchorMetadata,
  resolveSibling,
} from './vaultResolve';
import { questionLabel, type TopicSibling } from './topics';
import { sittingLabel } from './sitting';
import { lensFor } from '../../data/markingLens';
import { physicalEducationTask } from './physicalEducationTasks';
const PhysicalEducationTaskCard = lazy(() => import('./PhysicalEducationTaskCard'));
import { audioForPaper } from './paperRecording';
import FrenchPaperAudio from './FrenchPaperAudio';
import AudioSourcePlayer from '../MarkBank/AudioSourcePlayer';
import { asksForQuestion, isModelSubject, markBankLinkForCards } from './atlasModel';
import { isUnpricedSectionCard, unpricedSectionChip, type SecCard } from '../../types/markBank';

const LVL: Record<string, string> = { higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common' };
// A few verified booklet formats deliberately allocate more than three pages
// to one Paper Trail card. Applied Mathematics questions can span four pages;
// Politics & Society groups the complete lettered short-answer and data-based
// sections into single local cards, which can span ten. Every other subject
// keeps the conservative default that rejects suspiciously distant anchors.
const paperCropPageLimit = (subjectId: string) =>
  subjectId === 'politics-and-society'
    ? 10
    : subjectId === 'applied-mathematics'
      ? 4
      : 3;

// Stable identity — CropView re-renders its (expensive) canvas whenever this
// callback's reference changes, so it must NOT be an inline closure per render
// (a scheme-reveal / review-star toggle would otherwise re-decode the crop).
const paperCropLabel = (p: number) => `Exam paper page ${p}, shown as an image — © State Examinations Commission`;

// Session-scoped answer-map memo (small JSON sidecars; null = miss — the card
// degrades to a plain open-in-paper row). PERMANENT misses stay memoised: a
// 404 (sidecar not published) or a shape/parse failure — the hosted fallback
// path is served by Firebase Hosting, whose SPA rewrite answers missing files
// with index.html (200), which isAnswerMap rejects — won't change this session,
// and every card in a feed re-asks as it scrolls into view. Only TRANSIENT
// failures (network throw, non-404 error status) are forgotten, so a retry
// after coming back online gets a fresh attempt.
const mapMemo = new Map<string, Promise<PaperAnswerMap | null>>();
const fetchOneMap = (url: string): Promise<PaperAnswerMap | null> => {
  let p = mapMemo.get(url);
  if (!p) {
    p = (async () => {
      try {
        const r = await fetch(url);
        if (!r.ok) {
          if (r.status !== 404) mapMemo.delete(url); // 5xx/429 may recover
          return null;
        }
        const v = await r.json().catch(() => null); // HTML from the SPA rewrite
        return isAnswerMap(v) ? v : null;
      } catch {
        mapMemo.delete(url); // offline / network blip — let a remount retry
        return null;
      }
    })();
    mapMemo.set(url, p);
  }
  return p;
};
/** Resolve a map that actually CARRIES question `n`. When both the verified
 *  Storage answer map and a hosted paper-only map carry it, retain the scheme
 *  crop and add the audited paper endpoints from the hosted map. A map numbered
 *  against a different question run must not shadow a later valid candidate. */
const fetchAnswerMap = async (urls: string[], n: string): Promise<PaperAnswerMap | null> => {
  let withoutN: PaperAnswerMap | null = null;
  let matched: PaperAnswerMap | null = null;
  for (const url of urls) {
    const m = await fetchOneMap(url);
    if (!m) continue;
    if (m.q.some(q => q.n === n)) {
      if (!matched) {
        matched = m;
      } else if (m.paperOnly === 1 && matched.paperOnly !== 1) {
        matched = mergePaperAnchorMetadata(matched, m, n);
      } else if (matched.paperOnly === 1 && m.paperOnly !== 1) {
        matched = mergePaperAnchorMetadata(m, matched, n);
      }
      continue;
    }
    withoutN = withoutN ?? m;
  }
  return matched ?? withoutN;
};

type CardState =
  | { s: 'idle' } // idle = not started OR in flight — both render the skeleton
  | { s: 'ready'; pdf: PDFDocumentProxy; q: PaperAnswerQuestion; region: NonNullable<ReturnType<typeof paperRegionFor>>; schemeUrl: string | null }
  | { s: 'fallback' };

interface Props {
  sibling: TopicSibling;
  saved: boolean;
  onToggleReview: () => void;
  onOpenInPaper: () => void;
  /** The heading this card is listed under. In the single model a question whose parts sit under several headings
   *  shows only the parts of this one, with the rest a tap away. */
  topicId?: string;
  onOpenTopic?: (topicId: string) => void;
  /** Tells the topic page whether this question showed as the printed paper or as a row into the full paper
   *  (its year then says "Opens in the full paper"). */
  onKind?: (kind: 'row' | 'printed', label?: string) => void;
  /** Name the level beside the question (default true); a topic set at one level says it once, above. */
  showLevel?: boolean;
  /** Only the printed question, as the topic page shows it (Topic Atlas's laptop panel): no line, no buttons. */
  pictureOnly?: boolean;
}

/** Printed order of a part from its reference: "Q14(c)(iv)2" reads (c), (iv), 2. Letters, roman numerals and
 *  trailing numbers each sort by their value, so (i) comes before (iv) and (a) before (b). */
const ROMAN: Record<string, number> = { i: 1, v: 5, x: 10, l: 50 };
const romanValue = (r: string) => [...r].reduce((sum, ch, i, all) => (ROMAN[ch] < (ROMAN[all[i + 1]] ?? 0) ? sum - ROMAN[ch] : sum + ROMAN[ch]), 0);
export function printedPartKey(questionRef: string): number[] {
  const address = questionRef.replace(/^\d{4} [A-Z]{2} /, '').replace(/^.*?Q\d+/, '');
  return [...address.matchAll(/\(([^)]+)\)|(\d+)|([A-Z])/g)].map(m => {
    const token = (m[1] ?? m[2] ?? m[3]).toLowerCase();
    if (/^\d+$/.test(token)) return 1000 + Number(token);
    if (/^[ivxl]+$/.test(token) && token !== 'l') return 100 + romanValue(token);
    return token.charCodeAt(0);
  });
}
const byPrintedOrder = (a: SecCard, b: SecCard) => {
  const ka = printedPartKey(a.questionRef); const kb = printedPartKey(b.questionRef);
  for (let i = 0; i < Math.max(ka.length, kb.length); i++) { const d = (ka[i] ?? -1) - (kb[i] ?? -1); if (d) return d; }
  return 0;
};

/** The parts of a printed question filed under one heading (atlasModel.ts), lifted from their Mark Bank cards. */
const PartsOnThisTopic: React.FC<{ sibling: TopicSibling; topicId: string; onOpenTopic?: (id: string) => void }> = ({ sibling, topicId, onOpenTopic }) => {
  const asks = useMemo(() => asksForQuestion(sibling.subjectId, sibling.year, sibling.level, sibling.fileid, sibling.n), [sibling]);
  const here = useMemo(() => asks.filter(a => a.topics.some(t => t.id === topicId)), [asks, topicId]);
  const [cards, setCards] = useState<SecCard[] | null>(null);
  useEffect(() => {
    let cancelled = false;
    const ids = new Set(here.map(a => a.cardId));
    import('../MarkBank/deck').then(({ loadCards }) => loadCards(here[0].subjectId, sibling.level as never))
      .then(all => { if (!cancelled) setCards(all.filter(c => ids.has(c.id)).sort(byPrintedOrder)); })
      .catch(() => { if (!cancelled) setCards([]); });
    return () => { cancelled = true; };
  }, [here, sibling.level]);
  const elsewhere = useMemo(() => {
    const counts = new Map<string, { label: string; parts: number }>();
    for (const ask of asks) {
      if (ask.topics.some(t => t.id === topicId)) continue;
      for (const t of ask.topics) { const c = counts.get(t.id) ?? { label: t.label, parts: 0 }; c.parts++; counts.set(t.id, c); }
    }
    return [...counts.entries()];
  }, [asks, topicId]);
  const marks = (cards ?? []).reduce((n, c) => n + (c.totalMarks ?? 0), 0);
  let lastStem = '';
  // The printed figures these parts point at, once each and before them: shared material travels with each topic.
  const figures = [...new Map((cards ?? []).flatMap(card => {
    const figure = 'figure' in card ? card.figure : undefined;
    return figure && !figure.solution ? [[figure.src, figure] as const] : [];
  })).values()];
  return (
    <div className="ta-parts" data-testid="atlas-parts-on-topic">
      <p className="t-label ta-parts-label">
        On this topic: {here.length} of {asks.length} parts{cards && marks ? ` · ${marks} marks` : ''}
      </p>
      {figures.map(figure => (
        <img key={figure.src} src={figure.src} alt={figure.alt} loading="lazy" className="ta-parts-figure" />
      ))}
      <ol className="ta-parts-list">
        {(cards ?? []).map(card => {
          const stem = card.stem && card.stem !== lastStem ? card.stem : '';
          if (card.stem) lastStem = card.stem;
          return (
            <li key={card.id}>
              {stem && <p className="ta-parts-stem">{stem}</p>}

              <div className="ta-parts-row">
                <span className="ui-readout ta-parts-ref">{card.questionRef.replace(/^\d{4} [A-Z]{2} /, '')}</span>
                <span className="ta-parts-text">{card.questionText}</span>
                <span className="ui-readout ta-parts-marks">{isUnpricedSectionCard(card) ? unpricedSectionChip(card.unpricedSection) : `${card.totalMarks}m`}</span>
              </div>
            </li>
          );
        })}
        {!cards && <li className="ta-parts-skel" aria-hidden="true" />}
      </ol>
      {elsewhere.length > 0 && (
        <div className="ta-parts-else">
          <span>The other parts are under</span>
          {elsewhere.map(([id, e]) => (
            <TextButton key={id} arrow="forward" onClick={() => { if (onOpenTopic) onOpenTopic(id); }} aria-disabled={!onOpenTopic || undefined}>
              {e.label} · {e.parts} {e.parts === 1 ? 'part' : 'parts'}
            </TextButton>
          ))}
        </div>
      )}
      <a href={markBankLinkForCards(here.map(a => a.cardId))} target="_blank" rel="noopener noreferrer"
        className="ui-part ui-btn ta-parts-practise">
        <span>Practise {here.length === 1 ? 'this part' : `these ${here.length} parts`} in the Mark Bank</span>
        <Arrow meaning="forward" size={20} />
      </a>
    </div>
  );
};

const LegacyVaultQuestionCard: React.FC<Props> = ({ sibling, saved, onToggleReview, onOpenInPaper, topicId, onOpenTopic, onKind, showLevel = true, pictureOnly = false }) => {
  // The single model: when this question's parts sit under several headings, the card leads with the parts filed
  // under this one and keeps the whole printed question one tap away.
  const splitParts = useMemo(() => {
    if (!topicId || !isModelSubject(sibling.subjectId)) return false;
    const asks = asksForQuestion(sibling.subjectId, sibling.year, sibling.level, sibling.fileid, sibling.n);
    const here = asks.filter(a => a.topics.some(t => t.id === topicId)).length;
    return here > 0 && here < asks.length;
  }, [sibling, topicId]);
  const [wholeOpen, setWholeOpen] = useState(false);
  const [visible, setVisible] = useState(false);
  const [state, setState] = useState<CardState>({ s: 'idle' });
  const [lensOpen, setLensOpen] = useState(false);
  const [schemeOpen, setSchemeOpen] = useState(false);
  const [schemePdf, setSchemePdf] = useState<PDFDocumentProxy | null>(null);
  const [schemeFailed, setSchemeFailed] = useState(false);
  const rootRef = useRef<HTMLDivElement | null>(null);

  const resolved = useMemo(() => resolveSibling(sibling), [sibling]);
  const audioSource = useMemo(() => audioForPaper(sibling), [sibling]);
  // Marking Lens — the scheme-grounded marks breakdown, where one is authored.
  // Independent of the crop state: it teaches even when no crop can render.
  const lens = useMemo(() => lensFor(sibling), [sibling]);

  // Render lazily — a topic feed can span dozens of multi-MB papers.
  useEffect(() => {
    const el = rootRef.current;
    if (!el || visible) return;
    if (!('IntersectionObserver' in window)) { setVisible(true); return; }
    const obs = new IntersectionObserver(
      entries => { if (entries.some(e => e.isIntersecting)) { setVisible(true); obs.disconnect(); } },
      { rootMargin: '400px 0px' },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [visible]);

  useEffect(() => {
    if (!visible || state.s !== 'idle') return;
    if (!resolved) { setState({ s: 'fallback' }); return; }
    // NB: no intermediate "loading" setState here — state.s is in the deps, so
    // a self-triggered transition re-runs this effect and its cleanup would
    // cancel the in-flight load. The skeleton renders for 'idle' anyway.
    let cancelled = false;
    (async () => {
      const map = await fetchAnswerMap(answerMapUrls(resolved), sibling.n);
      if (cancelled) return;
      const q = map?.q.find(x => x.n === sibling.n);
      const cropLimit = Math.max(
        paperCropPageLimit(sibling.subjectId),
        map?.maxCropPages ?? 0,
      );
      const region = map && q ? paperRegionFor(map.q, sibling.n, cropLimit) : null;
      if (!q || !region) { setState({ s: 'fallback' }); return; }
      try {
        const pdf = await vaultPdf(resolved.paperUrl);
        if (cancelled) return;
        setState({ s: 'ready', pdf, q, region, schemeUrl: resolved.schemeUrl });
      } catch {
        if (!cancelled) setState({ s: 'fallback' });
      }
    })();
    return () => { cancelled = true; };
  }, [visible, state.s, resolved, sibling.n]);

  // Scheme reveal — loads the scheme PDF on first open.
  useEffect(() => {
    if (!schemeOpen || schemePdf || state.s !== 'ready' || !state.schemeUrl) return;
    let cancelled = false;
    vaultPdf(state.schemeUrl)
      .then(pdf => { if (!cancelled) setSchemePdf(pdf); })
      .catch(() => { if (!cancelled) setSchemeFailed(true); });
    return () => { cancelled = true; };
  }, [schemeOpen, schemePdf, state]);

  const meta = [
    showLevel ? LVL[sibling.level] ?? sibling.level : null,
    sittingLabel(sibling.fileid),
    sibling.paperKey === 'p1' ? 'Paper 1' : sibling.paperKey === 'p2' ? 'Paper 2' : null,
    sibling.lang === 'iv' ? 'Gaeilge' : null,
  ].filter(Boolean) as string[];

  const canReveal = state.s === 'ready' && state.schemeUrl !== null && state.q.mode === 'crop';
  const onKindRef = useRef(onKind);
  onKindRef.current = onKind;
  useEffect(() => {
    if (state.s === 'ready') onKindRef.current?.('printed', state.q.label || questionLabel(sibling));
    else if (state.s === 'fallback') onKindRef.current?.('row');
  }, [state, sibling]);
  const isAccountingTask = sibling.subjectId === 'accounting' && state.s === 'ready' && Boolean(state.q.practiceTask);

  const name = (state.s === 'ready' && state.q.label) || questionLabel(sibling);
  // The laptop panel's picture: the same crop of the printed question, nothing else.
  if (pictureOnly) {
    return (
      <div ref={rootRef} className="ta-card--picture">
        {state.s === 'ready' ? (
          <div className="ta-crop ta-crop--panel">
            <CropView pdf={state.pdf} region={state.region} ariaLabel={paperCropLabel} failText="Couldn’t render this question — open the full paper." />
          </div>
        ) : null}
      </div>
    );
  }
  const reviewButton = (
    <IconButton className={state.s === 'fallback' ? 'ta-ib ta-ib--plain' : 'ta-ib'} label={saved ? 'Remove from daily review' : 'Add to daily review'} aria-pressed={saved}
      title={saved ? 'In your daily review' : 'Add to daily review'} onClick={onToggleReview}
      icon={saved ? <Check className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />
        : <Plus className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
  );
  const parts = splitParts && topicId ? <div className="ta-paper"><PartsOnThisTopic sibling={sibling} topicId={topicId} onOpenTopic={onOpenTopic} /></div> : null;
  // How the marks are given (the Marking Lens): today's words, on the page in ink.
  const lensBlock = lens ? (
    <div className="ta-lens">
      <TextButton onClick={() => setLensOpen(v => !v)} aria-expanded={lensOpen}>How the marks are given</TextButton>
      {lensOpen && (
        <div className="ta-paper ta-lens-body">
          <div className="ta-lens-head">
            <p className="t-sub">{lens.headline}</p>
            <span className="ui-readout">{lens.totalMarks} marks</span>
          </div>
          <ol className="ta-lens-parts">
            {lens.parts.map((p, i) => (
              <li key={i}>
                <span className="ta-lens-copy">
                  {p.part && <span className="t-label">{p.part}</span>}
                  <span className="ta-lens-task">{p.task}</span>
                  <span className="ui-readout">{p.notation}</span>
                  <span className="t-meta">{p.decoded}</span>
                </span>
                <span className="ta-lens-marks" aria-label={`${p.marks} marks`}>{p.marks}<span className="t-meta"> m</span></span>
              </li>
            ))}
          </ol>
          {lens.pitfall && (
            <div className="ta-lens-pitfall">
              <p className="t-label">Where marks are lost</p>
              <p className="t-sub">{lens.pitfall.text}</p>
              <p className="t-meta">{lens.pitfall.cite}</p>
            </div>
          )}
          <p className="t-label ta-lens-cite">{lens.cite} — © State Examinations Commission</p>
        </div>
      )}
    </div>
  ) : null;

  // A question that cannot show as a picture yet: a plain row into the full paper.
  if (state.s === 'fallback') {
    return (
      <div ref={rootRef} className="ta-card ta-card--row">
        <div className="ta-row-line">
          <List className="ta-qrow"><Row title={name} meta={meta.length ? meta.join(' · ') : undefined}
            label={`${[...meta, name].join(' · ')}: open it in the full paper`} onPress={onOpenInPaper} /></List>
          {reviewButton}
        </div>
        {parts}
        {lensBlock}
      </div>
    );
  }

  return (
    <div ref={rootRef} className="ta-card">
      <div className="ta-card-head">
        <span className="t-meta">{[...meta, name].join(' · ')}{state.s === 'ready' ? ', as printed' : ''}</span>
        {reviewButton}
      </div>
      {parts}
      {splitParts && (
        <TextButton className="ta-whole" onClick={() => setWholeOpen(v => !v)} aria-expanded={wholeOpen}>
          {wholeOpen ? 'Hide the whole printed question' : 'Show the whole printed question'}
        </TextButton>
      )}
      {visible && audioSource && <FrenchPaperAudio source={audioSource} />}
      {splitParts && !wholeOpen ? null : state.s === 'ready' ? (
        // The printed paper, at a readable size: white in both themes.
        <div className="ta-crop">
          {state.q.practiceTask && (
            <div className="px-1 pb-4 ta-crop-text">
              <p className="text-[13px] font-semibold whitespace-pre-line">{state.q.practiceTask.prompt}</p>
              {state.q.practiceTask.focus && <p className="text-[13px] mt-2">{state.q.practiceTask.focus}</p>}
              <p className="text-[12px] mt-2 font-semibold">{state.q.practiceTask.marks} marks · Full figures and instructions {isAccountingTask ? 'in the source reader' : 'below'}</p>
            </div>
          )}
          {state.q.audioMaterial && <AudioSourcePlayer source={state.q.audioMaterial} />}
          {state.q.practiceInstruction && <p className="mb-3 text-sm font-semibold ta-crop-text">{state.q.practiceInstruction}</p>}
          {isAccountingTask ? (
            <div className="mark-bank-theme pb-3">
              <SourceMaterialReader subjectId={sibling.subjectId} year={sibling.year} paperFileid={sibling.fileid}
                source={{ kind: 'source-table', label: `Question ${sibling.n}`, title: 'Figures, tables and instructions',
                  pages: [...new Set(state.region.map(region => region.p))],
                  regions: state.region.map(region => ({ ...region, r: region.r ?? [0, 0, 1, 1] })),
                  presentationNote: 'Original examination pages, preserving every table, figure and adjustment.',
                  attribution: '© State Examinations Commission' }} />
            </div>
          ) : <CropView
            pdf={state.pdf}
            region={state.region}
            ariaLabel={paperCropLabel}
            failText="Couldn’t render this question — open the full paper."
          />}
        </div>
      ) : (
        <div className="ta-skeleton" aria-hidden="true">
          <i style={{ width: '82%' }} /><i style={{ width: '64%' }} /><i style={{ width: '73%' }} />
        </div>
      )}

      {/* Marking scheme and Full paper: two equal buttons. */}
      {state.s === 'ready' && (
        <div className="ta-acts">
          <Button onClick={canReveal ? () => setSchemeOpen(v => !v) : onOpenInPaper} aria-expanded={canReveal ? schemeOpen : undefined}
            aria-label={canReveal ? (schemeOpen ? 'Hide the marking scheme' : 'Show the marking scheme') : 'Open beside its marking scheme'}>
            Marking scheme
          </Button>
          <Button onClick={onOpenInPaper} title="Open in the full paper">Full paper</Button>
        </div>
      )}
      {canReveal && schemeOpen && state.s === 'ready' && (
        <div className="ta-scheme">
          <p className="t-label">Marking scheme — © State Examinations Commission</p>
          {state.q.schemeNote && <p className="t-sub">{state.q.schemeNote}</p>}
          {isAccountingTask ? (
            <div className="mark-bank-theme">
              <SourceMaterialReader subjectId={sibling.subjectId} year={sibling.year} paperFileid={sibling.fileid}
                source={{ kind: 'marking-scheme', label: `Question ${sibling.n}`, title: 'Worked solution and mark allocation',
                  pages: [...new Set(schemeRegionFor(state.q).map(region => region.p))],
                  regions: schemeRegionFor(state.q).map(region => ({ ...region, r: region.r ?? [0, 0, 1, 1] })),
                  presentationNote: 'Original SEC marking scheme. Use the allocation for this task; page numbers refer to the PDF.',
                  attribution: '© State Examinations Commission' }} />
            </div>
          ) : schemePdf ? (
            <div className="ta-crop"><CropView pdf={schemePdf} region={schemeRegionFor(state.q)} trim responsive /></div>
          ) : schemeFailed ? (
            <p className="t-meta">Couldn’t load the scheme — open the question in the full paper instead.</p>
          ) : (
            <div className="ta-skeleton" aria-hidden="true"><i style={{ width: '70%' }} /></div>
          )}
        </div>
      )}
      {lensBlock}
    </div>
  );
};

/** A PE task has no printed crop: the panel's picture moves on to the next question. */
const NoPicture: React.FC<{ onKind?: Props['onKind'] }> = ({ onKind }) => {
  useEffect(() => { onKind?.('row'); }, [onKind]);
  return null;
};

const VaultQuestionCard: React.FC<Props> = props => {
  const task = physicalEducationTask(props.sibling);
  if (task && props.pictureOnly) return <NoPicture onKind={props.onKind} />;
  if (task) return <Suspense fallback={<p role="status">Loading question…</p>}>
    <PhysicalEducationTaskCard key={task.cardId} task={task} saved={props.saved} onToggleReview={props.onToggleReview} onOpenInPaper={props.onOpenInPaper} />
  </Suspense>;
  return <LegacyVaultQuestionCard {...props} />;
};
export default VaultQuestionCard;
