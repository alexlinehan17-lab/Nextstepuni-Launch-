/**
 * Mark Bank session controls, rebuilt on Kobra for the wave 1 / 2 review (27 Oct).
 *
 * The same card as the "Now" pane, loaded with the bank's own loader
 * (loadCards), so every word of the question, the route names, the marking
 * points, their marks and the citation is the card's; the screen's own copy is
 * lifted from components/MarkBank/SessionScreen.tsx. The session is the paper
 * layout MarkBank.tsx mounts (header, question beside the scheme, one rail),
 * drawn here in the page so it can be read beside the original; Expand opens
 * the same live session full screen in the runtime Dialog.
 *
 * What changed against the current screen:
 *  - Reveal is the one primary Kobra Button; every other action is an outline
 *    Button (the paper CSS forces all of them to outline today).
 *  - The answer route is the house pill: Kobra Tabs.
 *  - The three grades are one Kobra ToggleGroup; the suggestion is an ink ring,
 *    the chosen grade an ink face. Never orange: orange must not mean correct.
 *  - Each marking point is a Kobra Checkbox row that turns mint when claimed,
 *    with its marks chip; the rail keeps the running tally.
 *  - Mark values on a priced criterion are the same ToggleGroup (second card).
 *  - The exit confirm and the source page are the runtime Dialog.
 * Nothing is stored; grading starts the card again.
 */

import { useEffect, useId, useMemo, useRef, useState } from 'react';
import { ChevronRight, Maximize2, Minimize2, X } from 'lucide-react';
import {
  Button,
  Checkbox,
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  Tabs,
  TabsList,
  TabsTrigger,
  Textarea,
  ToggleGroup,
  ToggleGroupItem,
  toast,
} from '../../components/approved-ui-runtime';
import { loadCards } from '../../components/MarkBank/deck';
import { splitForEmphasis } from '../../components/MarkBank/questionEmphasis';
import { questionParts } from '../../components/MarkBank/questionParts';
import { isPointCard as isPointKind, rowId, type MarkRow, type SecCard, type SecPointCard } from '../../types/markBank';
import './mark-bank-session.css';

type Grade = 'missed' | 'shaky' | 'got';
const GRADES: Grade[] = ['missed', 'shaky', 'got'];
const GRADE_COPY: Record<Grade, string> = { missed: 'Missed it', shaky: 'Shaky', got: 'Got it' };
/** What the screen whispers when the scheduler has no interval words of its own. */
const WHISPER: Record<Grade, string> = {
  got: "Nice. You won't see this one for a while.",
  shaky: 'Good — that one comes back soon.',
  missed: "No bother. It'll come back before you finish today.",
};

const SESSION = { subjectId: 'agricultural-science', title: 'Agricultural Science', cardId: 'agsci-2012-hl-q2b', route: 'sandy' };
const CRITERIA = { subjectId: 'construction-studies', title: 'Construction Studies', cardId: 'cons-2016-hl-q9-a' };

type PointCard = SecPointCard;
const isPointCard = (card: SecCard | undefined): card is PointCard => Boolean(card && isPointKind(card));
const marksOf = (row: MarkRow) => row.marks ?? 0;
const suggestion = (got: number, total: number): Grade => (got <= 0 ? 'missed' : got >= total ? 'got' : 'shaky');
/** The scheme's own wording minus any "Label — " prefix, as the rail names it. */
const shortName = (row: MarkRow) => {
  const tail = row.verbatim.split(/\s[—-]\s/).pop() ?? row.verbatim;
  return tail.trim().length <= 6 ? row.verbatim : tail;
};
const levelWords = (level: string) => (level === 'higher' ? 'Higher level' : level === 'common' ? 'Common level' : 'Ordinary level');
const paperHref = (card: SecCard) => {
  const file = card.paperFileid ?? '';
  return `/?view=innovation-zone&tool=paper-trail&subject=${encodeURIComponent(card.subjectId)}&year=${card.year}&level=${card.level}&lang=ev&paper=${encodeURIComponent(file.endsWith('.pdf') ? file : `${file}.pdf`)}`;
};
const sourceDetail = (pages: number) => `${pages} printed ${pages === 1 ? 'page' : 'pages'} · exact examination text`;

function useCard(subjectId: string, cardId: string) {
  const [state, setState] = useState<{ card?: SecCard; total?: number; failed?: boolean }>({});
  useEffect(() => {
    let cancelled = false;
    loadCards(subjectId, 'higher')
      .then(cards => { if (!cancelled) setState({ card: cards.find(item => item.id === cardId), total: cards.length }); })
      .catch(() => { if (!cancelled) setState({ failed: true }); });
    return () => { cancelled = true; };
  }, [subjectId, cardId]);
  return state;
}

/** The command clause carries the paper's orange rule, as it does today. */
function Clause({ text }: { text: string }) {
  const { before, marked, after } = splitForEmphasis(text);
  return <>{before}<span className="kr-mbs-command">{marked}</span>{after}</>;
}

function QuestionText({ text }: { text: string }) {
  const parts = questionParts(text);
  if (!parts) return <p className="kr-mbs-question" dir="auto"><Clause text={text} /></p>;
  return (
    <div className="kr-mbs-question">
      {parts.map((part, index) => (
        <div className="kr-mbs-part" key={`${part.label}-${index}`}>
          <span className="kr-mbs-part-label">{part.label}</span>
          <div>
            {part.body && <div dir="auto"><Clause text={part.body} /></div>}
            {part.children.map((child, childIndex) => (
              <div className="kr-mbs-part kr-mbs-part-nested" key={`${child.label}-${childIndex}`}>
                <span className="kr-mbs-part-label">{child.label}</span>
                <div dir="auto"><Clause text={child.body} /></div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

/* ----------------------------------------------------------- the session ---- */

interface Session {
  card: PointCard;
  poolTotal: number;
  route: string | null;
  setRoute: (route: string) => void;
  revealed: boolean;
  reveal: () => void;
  rows: MarkRow[];
  claims: Record<string, boolean>;
  claim: (id: string, on: boolean) => void;
  claimAll: () => void;
  interacted: boolean;
  total: number;
  got: number;
  suggested: Grade;
  pressed: Grade | null;
  commit: (grade: Grade) => void;
  whisper: string | null;
  draft: string;
  setDraft: (value: string) => void;
  done: number;
  showState: (state: 'question' | 'revealed') => void;
}

function useSession(card: PointCard | undefined, poolTotal: number): Session | null {
  const variants = card?.answerVariants ?? [];
  const firstRows = (route: string | null) => (route ? variants.find(variant => variant.id === route)?.rows : card?.rows) ?? [];
  const seeded = (route: string | null) => Object.fromEntries(firstRows(route).slice(0, 2).map((row, index) => [rowId(row, index), true]));
  const [route, setRouteState] = useState<string | null>(SESSION.route);
  const [revealed, setRevealed] = useState(true);
  const [claims, setClaims] = useState<Record<string, boolean>>({});
  const [interacted, setInteracted] = useState(true);
  const [pressed, setPressed] = useState<Grade | null>(null);
  const [whisper, setWhisper] = useState<string | null>(null);
  const [draft, setDraft] = useState('');
  const [seededFor, setSeededFor] = useState<string | null>(null);
  const timers = useRef<number[]>([]);
  useEffect(() => () => timers.current.forEach(window.clearTimeout), []);
  // The pane opens as the "Now" pane does: Sandy, revealed, the first two points claimed.
  useEffect(() => {
    if (card && seededFor !== card.id) { setClaims(seeded(SESSION.route)); setSeededFor(card.id); }
  }, [card, seededFor]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!card) return null;
  const rows = firstRows(route);
  const total = rows.reduce((sum, row) => sum + marksOf(row), 0);
  const got = rows.reduce((sum, row, index) => sum + (claims[rowId(row, index)] ? marksOf(row) : 0), 0);
  const later = (ms: number, run: () => void) => { timers.current.push(window.setTimeout(run, ms)); };

  return {
    card, poolTotal, route, revealed, rows, claims, interacted, total, got, pressed, whisper, draft, setDraft,
    suggested: suggestion(got, total),
    done: 0,
    setRoute: next => { setRouteState(next); setClaims({}); setInteracted(false); },
    reveal: () => { setWhisper(null); setInteracted(false); setRevealed(true); },
    claim: (id, on) => { setInteracted(true); setClaims(current => ({ ...current, [id]: on })); },
    claimAll: () => { setInteracted(true); setClaims(Object.fromEntries(rows.map((row, index) => [rowId(row, index), true]))); },
    commit: grade => {
      // Grades commit on the tap, as today. The chosen face holds for a beat so
      // it is seen, then the next card arrives (here: the same card, afresh).
      setPressed(grade);
      setWhisper(WHISPER[grade]);
      later(700, () => {
        setPressed(null); setRevealed(false); setClaims({}); setInteracted(false); setRouteState(null); setDraft('');
      });
      later(1800, () => setWhisper(null));
    },
    showState: state => {
      timers.current.forEach(window.clearTimeout);
      setPressed(null); setWhisper(null);
      const nextRoute = route ?? SESSION.route;
      setRouteState(nextRoute);
      if (state === 'revealed') { setRevealed(true); setClaims(seeded(nextRoute)); setInteracted(true); }
      else { setRevealed(false); setClaims({}); setInteracted(false); }
    },
  };
}

function ClaimRow({ row, id, claimed, showMarks, onClaim }: {
  row: MarkRow; id: string; claimed: boolean; showMarks: boolean; onClaim: (id: string, on: boolean) => void;
}) {
  return (
    <label className="kr-mbs-row" data-claimed={claimed || undefined}>
      <Checkbox checked={claimed} onCheckedChange={checked => onClaim(id, Boolean(checked))} />
      <span className="kr-mbs-row-copy">
        <span dir="auto">
          {row.verbatim}
          {row.accepts?.length ? <span className="kr-mbs-row-accepts">{' or '}{row.accepts.join(' or ')}</span> : null}
        </span>
        {row.contextNote && <span className="kr-mbs-row-note">{row.contextNote}</span>}
      </span>
      {showMarks && <span className="kr-mbs-chip">{marksOf(row)}m</span>}
    </label>
  );
}

function Paper({ s, expanded, onExpand, onClose }: {
  s: Session; expanded: boolean; onExpand: () => void; onClose: () => void;
}) {
  const ids = useId();
  const [sourceOpen, setSourceOpen] = useState(false);
  const { card } = s;
  const variants = card.answerVariants ?? [];
  const source = card.sourceMaterial;
  const left = Math.max(0, s.total - s.got);
  const unclaimed = s.rows.filter((row, index) => !s.claims[rowId(row, index)]).map(shortName);
  const names = unclaimed.slice(0, 3);
  const more = unclaimed.length - names.length;
  const needsRoute = variants.length > 0 && !s.route;
  const questionRef = card.questionRef.replace(/^\d{4}\s+(HL|OL)\s+/, '');

  return (
    <div className="kr-mbs-paper" data-expanded={expanded || undefined}>
      <header className="kr-mbs-head">
        <div className="kr-mbs-head-copy">
          <p className="kr-mbs-kicker">{SESSION.title} / {card.questionRef}</p>
          <h2 className="kr-mbs-title">{SESSION.title}</h2>
          <p className="kr-mbs-desc">{card.totalMarks} marks · Question {Math.min(s.done + 1, 1)} of 1 in this review</p>
        </div>
        <div className="kr-mbs-head-actions">
          <Button variant="outline" className="nsu-ink-outline" aria-label={expanded ? 'Contract to compact view' : 'Expand to full screen'} aria-pressed={expanded} onClick={onExpand}>
            {expanded ? <Minimize2 aria-hidden="true" /> : <Maximize2 aria-hidden="true" />}<span>{expanded ? 'Contract' : 'Expand'}</span>
          </Button>
          <Button variant="outline" size="icon" className="nsu-ink-outline kr-mbs-close" aria-label="Close practice" onClick={onClose}><X aria-hidden="true" /></Button>
        </div>
      </header>

      <div className="kr-mbs-workspace">
        <section className="kr-mbs-question-pane" aria-label="Question">
          <div className="kr-mbs-meta">
            <span>{SESSION.title} · {levelWords(card.level)} · {card.year} · {questionRef}</span>
            <span className="kr-mbs-total">{card.totalMarks}m</span>
          </div>
          {card.stem && <p className="kr-mbs-stem">{card.stem}</p>}
          <QuestionText text={card.questionText} />
          {card.paperFileid && <a className="kr-mbs-paper-link" href={paperHref(card)} target="_blank" rel="noopener noreferrer">Open original paper ↗</a>}
          {source && (
            <Button variant="outline" className="nsu-ink-outline kr-mbs-source" onClick={() => setSourceOpen(true)}>
              <span className="kr-mbs-source-copy">
                <span className="kr-mbs-source-label">Read {source.label}</span>
                <strong>{source.title}</strong>
                <small>{sourceDetail(source.pages.length)}</small>
              </span>
              <ChevronRight aria-hidden="true" />
            </Button>
          )}
          {variants.length > 0 && (
            <div className="kr-mbs-route">
              <p className="kr-mbs-eyebrow" id={`${ids}-route`}>Match the route you answered</p>
              <p className="kr-mbs-route-copy">This is one exam question. Choose your example so the reveal shows its exact SEC scheme.</p>
              <Tabs value={s.route ?? ''} onValueChange={value => s.setRoute(String(value))}>
                <TabsList aria-labelledby={`${ids}-route`}>
                  {variants.map(variant => <TabsTrigger key={variant.id} value={variant.id}>{variant.label}</TabsTrigger>)}
                </TabsList>
              </Tabs>
            </div>
          )}
        </section>

        <section className="kr-mbs-scheme-pane" aria-label="Scheme">
          <div className="kr-mbs-draft">
            <label className="kr-mbs-eyebrow" htmlFor={`${ids}-draft`}>Your answer</label>
            <Textarea id={`${ids}-draft`} value={s.draft} onChange={event => s.setDraft(event.target.value)} placeholder="Make a start. You can also work on paper." />
          </div>

          {!s.revealed ? (
            <div className="kr-mbs-waysin">
              <h3>Need a way into the question?</h3>
              <p>Focus one line at a time, map the instruction and hold your plan beside the exact SEC wording.</p>
              <Button variant="outline" className="nsu-ink-outline" onClick={() => toast({ message: 'Ways In opens beside the question.' })}>Open Ways In</Button>
            </div>
          ) : (
            <div className="kr-mbs-scheme">
              <div className="kr-mbs-scheme-head">
                <span className="kr-mbs-eyebrow">The scheme</span>
                <Button variant="outline" size="sm" className="nsu-ink-outline kr-mbs-all" onClick={s.claimAll}>Select all — I had them all</Button>
              </div>
              <div className="kr-mbs-instruction">
                <p className="kr-mbs-instruction-title">Select the points you actually got.</p>
                <p>Tap every point that appeared in your answer. This gives you a mark-based suggestion; you can still choose your own grade below.</p>
              </div>
              <div className="kr-mbs-rows">
                {s.rows.map((row, index) => {
                  const id = rowId(row, index);
                  return <ClaimRow key={id} row={row} id={id} claimed={Boolean(s.claims[id])} showMarks onClaim={s.claim} />;
                })}
              </div>
              <p className="kr-mbs-citation">{card.schemeCitation}</p>
            </div>
          )}
        </section>
      </div>

      <div className="kr-mbs-rail">
        {s.whisper && <p className="kr-mbs-whisper" role="status">{s.whisper}</p>}
        {!s.revealed ? (
          <Button className="kr-mbs-reveal" disabled={needsRoute} onClick={s.reveal}>
            {needsRoute ? 'Choose your answer route first' : 'Reveal the marking scheme'}
          </Button>
        ) : (
          <>
            <div className="kr-mbs-tally" data-complete={left === 0 || undefined}>
              {left === 0 ? (
                <span className="kr-mbs-tally-done">All {s.total} marks. Nothing left behind.</span>
              ) : (
                <span className="kr-mbs-tally-text">
                  <span className="kr-mbs-muted">Not claimed yet · </span>
                  <strong>{left}</strong>
                  <span className="kr-mbs-muted">{left === 1 ? ' mark' : ' marks'}</span>
                  {names.length > 0 && <> · {names.join(' · ')}{more > 0 && <span className="kr-mbs-muted"> and {more} more</span>}</>}
                </span>
              )}
              <span className="kr-mbs-score" aria-hidden="true"><b>{s.got}</b> / {s.total}</span>
            </div>
            <p className="kr-mbs-guidance" id={`${ids}-guidance`}>
              {s.interacted
                ? <>You claimed {s.got} of {s.total} marks — that looks like {GRADE_COPY[s.suggested]}.</>
                : <>No points selected yet. Select them above for a mark-based suggestion, or choose your own grade now.</>}
              <br /><em>You decide. Tap any of the three.</em>
            </p>
            <ToggleGroup
              className="kr-mbs-grades"
              variant="outline"
              aria-label="Grade this card"
              value={s.pressed ? [s.pressed] : []}
              onValueChange={values => { const next = values[0] as Grade | undefined; if (next && !s.pressed) s.commit(next); }}
            >
              {GRADES.map(grade => (
                <ToggleGroupItem key={grade} value={grade} aria-describedby={`${ids}-guidance`}
                  data-suggested={(s.interacted && grade === s.suggested) || undefined}>
                  {GRADE_COPY[grade]}
                </ToggleGroupItem>
              ))}
            </ToggleGroup>
          </>
        )}
      </div>

      {source && (
        <Dialog open={sourceOpen} onOpenChange={setSourceOpen}>
          <DialogContent size="sm" className="kr-mbs-dialog" showCloseButton={false}>
            <div className="kr-mbs kr-mbs-in-dialog">
              <DialogHeader>
                <p className="kr-mbs-kicker">{source.label}</p>
                <DialogTitle className="kr-mbs-dialog-title">{source.title}</DialogTitle>
                <DialogDescription>{source.presentationNote}</DialogDescription>
              </DialogHeader>
              <p className="kr-mbs-citation">{source.attribution}</p>
              <DialogFooter className="kr-mbs-dialog-actions">
                {card.paperFileid && <a className="kr-mbs-paper-link" href={paperHref(card)} target="_blank" rel="noopener noreferrer">Open original paper ↗</a>}
                <Button variant="outline" className="nsu-ink-outline" onClick={() => setSourceOpen(false)}>Close</Button>
              </DialogFooter>
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}

/* --------------------------------------------- a criterion priced 0 to 4 ---- */

function CriteriaCard({ card }: { card: PointCard }) {
  const ids = useId();
  const criteria = card.rows.filter(row => row.permittedMarks?.length);
  const [awarded, setAwarded] = useState<Record<string, number>>(() => (criteria[0] ? { [rowId(criteria[0], 0)]: 3 } : {}));
  const total = criteria.reduce((sum, row) => sum + marksOf(row), 0);
  const got = criteria.reduce((sum, row, index) => sum + (awarded[rowId(row, index)] ?? 0), 0);
  return (
    <div className="kr-mbs-criteria">
      <header className="kr-mbs-criteria-head">
        <p className="kr-mbs-kicker">{CRITERIA.title} / {card.questionRef}</p>
        <span className="kr-mbs-total">{card.totalMarks}m</span>
      </header>
      <div className="kr-mbs-instruction">
        <p className="kr-mbs-instruction-title">Select the points you actually got.</p>
      </div>
      {criteria.map((row, index) => {
        const id = rowId(row, index);
        const value = awarded[id];
        return (
          <section key={id} className="kr-mbs-criterion" aria-label={`Marking criterion ${index + 1}`}>
            <strong>{row.verbatim}</strong>
            {row.contextNote && <p>{row.contextNote}</p>}
            <ToggleGroup
              className="kr-mbs-marks"
              variant="outline"
              aria-label={`Marks for ${row.verbatim}`}
              value={value === undefined ? [] : [String(value)]}
              onValueChange={values => { if (values[0] !== undefined) setAwarded(current => ({ ...current, [id]: Number(values[0]) })); }}
            >
              {row.permittedMarks!.map(mark => (
                <ToggleGroupItem key={mark} value={String(mark)} aria-label={`Award ${mark} marks for ${row.verbatim}`}>{mark}</ToggleGroupItem>
              ))}
            </ToggleGroup>
          </section>
        );
      })}
      <p className="kr-mbs-guidance" id={`${ids}-guidance`}>You claimed {got} of {total} marks — that looks like {GRADE_COPY[suggestion(got, total)]}.</p>
    </div>
  );
}

/* ---------------------------------------------------------------- page ---- */

export default function MarkBankSessionAfter() {
  const ids = useId();
  const main = useCard(SESSION.subjectId, SESSION.cardId);
  const criteria = useCard(CRITERIA.subjectId, CRITERIA.cardId);
  const card = isPointCard(main.card) ? main.card : undefined;
  const s = useSession(card, main.total ?? 0);
  const [expanded, setExpanded] = useState(false);
  const [confirmExit, setConfirmExit] = useState(false);
  const criteriaCard = useMemo(() => (isPointCard(criteria.card) ? criteria.card : undefined), [criteria.card]);

  if (main.failed) return <p className="kr-pending">The {SESSION.title} deck could not be loaded.</p>;
  if (!s) return <p className="kr-pending">Loading the {SESSION.title} deck…</p>;

  const leave = () => {
    setConfirmExit(false);
    setExpanded(false);
    s.showState('question');
    toast({ message: 'Left the review. Your completed cards are safe.' });
  };

  return (
    <section className="kr-section kr-mbs" aria-label="Mark Bank session on Kobra">
      <div className="kr-mbs-preview">
        <span className="kr-mbs-eyebrow" id={`${ids}-state`}>Preview state</span>
        <Tabs value={s.revealed ? 'revealed' : 'question'} onValueChange={value => s.showState(value as 'question' | 'revealed')}>
          <TabsList aria-labelledby={`${ids}-state`}>
            <TabsTrigger value="question">Question</TabsTrigger>
            <TabsTrigger value="revealed">Scheme revealed</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      <Paper s={s} expanded={false} onExpand={() => setExpanded(true)} onClose={() => setConfirmExit(true)} />

      {criteriaCard && (
        <div className="kr-mbs-aside">
          <p className="kr-mbs-eyebrow">A card whose scheme prices each criterion</p>
          <CriteriaCard card={criteriaCard} />
        </div>
      )}

      <Dialog open={expanded} onOpenChange={setExpanded}>
        <DialogContent className="kr-mbs-full" showCloseButton={false}>
          <div className="kr-mbs kr-mbs-in-dialog kr-mbs-in-full">
            <Paper s={s} expanded onExpand={() => setExpanded(false)} onClose={() => setConfirmExit(true)} />
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={confirmExit} onOpenChange={setConfirmExit}>
        <DialogContent size="sm" className="kr-mbs-dialog" showCloseButton={false}>
          <div className="kr-mbs kr-mbs-in-dialog">
            <DialogHeader>
              <p className="kr-mbs-kicker kr-mbs-kicker-quiet">Leave session?</p>
              <DialogTitle className="kr-mbs-dialog-title">Your completed cards are safe.</DialogTitle>
              <DialogDescription>You have finished {s.done} of 1. This exercise will stay ungraded and return next time.</DialogDescription>
            </DialogHeader>
            <DialogFooter className="kr-mbs-dialog-actions kr-mbs-dialog-stack">
              <Button autoFocus className="kr-mbs-keep" onClick={() => setConfirmExit(false)}>Keep reviewing</Button>
              <Button variant="outline" className="nsu-ink-outline" onClick={leave}>Leave review</Button>
            </DialogFooter>
          </div>
        </DialogContent>
      </Dialog>
    </section>
  );
}
