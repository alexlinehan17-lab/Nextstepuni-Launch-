/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Starguy · Instruments — five ideas for the one character, in the browser.
 *
 * THE THESIS. A mascot reacts to the user. An instrument makes something
 * legible that was not legible before. Starguy has five channels and no face:
 * he can look across and up, lean about the star, squash and stretch, and
 * change gait. Nothing there can smile, so nothing here tries to. Each idea
 * below maps one real thing about answering an exam question onto one thing
 * the rig can actually do, and none of them needs him redrawn.
 *
 * Dev only, like rive-lab: served by Vite, outside the production build.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { animate, useMotionValue } from 'framer-motion';
import { StarguyFigure } from './components/landing/starguy/StarguyFigure';
import { markAnswer } from './components/landing/marking/marker';
import { MARK_SUBJECTS } from './components/landing/fx-d/examinerData';
import './index.css';

const INK = '#1A1A1A';
const ORANGE = '#F26B1F';
const ORANGE_TEXT = '#B84A0C';
const MUTED = '#5F5A55';
const SERIF = "'Source Serif 4', Georgia, serif";

/* ── shared chrome ─────────────────────────────────────────────────────── */

const Instrument: React.FC<{
  numeral: string; title: string; thesis: string; channel: string;
  children: React.ReactNode;
}> = ({ numeral, title, thesis, channel, children }) => (
  <section style={{ borderTop: `1.5px solid ${INK}`, padding: '54px 0 64px' }}>
    <div style={{ display: 'flex', alignItems: 'baseline', gap: 14, marginBottom: 6 }}>
      <span style={{ fontFamily: SERIF, fontSize: 13, color: ORANGE_TEXT, letterSpacing: '0.08em' }}>{numeral}</span>
      <h2 style={{ fontFamily: SERIF, fontSize: 27, margin: 0, fontWeight: 600, letterSpacing: '-0.01em' }}>{title}</h2>
    </div>
    <p style={{ margin: '0 0 4px', maxWidth: 620, fontSize: 14.5, lineHeight: 1.55, color: MUTED }}>{thesis}</p>
    <p style={{ margin: '0 0 30px', fontSize: 11.5, letterSpacing: '0.13em', textTransform: 'uppercase', color: ORANGE_TEXT }}>{channel}</p>
    {children}
  </section>
);

const Stage: React.FC<{ children: React.ReactNode; width?: number }> = ({ children, width = 176 }) => (
  <div style={{ width, flex: `0 0 ${width}px` }}>{children}</div>
);

const Field: React.FC<React.TextareaHTMLAttributes<HTMLTextAreaElement>> = props => (
  <textarea
    {...props}
    style={{
      width: '100%', minHeight: 104, resize: 'vertical', padding: '13px 15px',
      border: `1.5px solid ${INK}`, borderRadius: 12, fontFamily: 'inherit',
      fontSize: 14.5, lineHeight: 1.55, color: INK, background: '#fff', outline: 'none',
      ...props.style,
    }}
  />
);

const Quote: React.FC<{ ref_: string; children: React.ReactNode }> = ({ ref_, children }) => (
  <>
    <p style={{ margin: '0 0 2px', fontSize: 15.5, lineHeight: 1.5 }}>{children}</p>
    <p style={{ margin: '0 0 16px', fontSize: 12, color: MUTED }}>{ref_}</p>
  </>
);

/* ── I. The nod ────────────────────────────────────────────────────────── */

const NOD_QUESTION = MARK_SUBJECTS
  .flatMap(s => s.questions)
  .find(q => q.ref === '2022 HL Q6(k)')!;

const TheNod: React.FC = () => {
  const lookY = useMotionValue(0);
  const lookX = useMotionValue(0);
  const [answer, setAnswer] = useState('');
  const result = useMemo(() => markAnswer(answer, NOD_QUESTION.points), [answer]);
  const landed = useRef<Set<string>>(new Set());

  useEffect(() => {
    for (const hit of result.hits) {
      if (hit.matched && !landed.current.has(hit.id)) {
        landed.current.add(hit.id);
        // A nod, not a bounce: down on the beat, back up a little slower,
        // the way a person listening acknowledges without interrupting.
        animate(lookY, [0, 1, 0], { duration: 0.62, times: [0, 0.34, 1], ease: ['easeIn', 'easeOut'] });
      } else if (!hit.matched) {
        landed.current.delete(hit.id);
      }
    }
  }, [result, lookY]);

  return (
    <div style={{ display: 'flex', gap: 34, alignItems: 'flex-end' }}>
      <Stage><StarguyFigure lookX={lookX} lookY={lookY} /></Stage>
      <div style={{ flex: 1, minWidth: 0 }}>
        <Quote ref_={`${NOD_QUESTION.ref} · ${NOD_QUESTION.total} marks · ${NOD_QUESTION.subject}`}>
          {NOD_QUESTION.question}
        </Quote>
        <Field
          value={answer}
          onChange={e => setAnswer(e.target.value)}
          placeholder="Write your answer. He nods when you land something the scheme credits."
        />
        <div style={{ display: 'flex', gap: 7, marginTop: 13, alignItems: 'center' }}>
          {result.hits.map(h => (
            <span key={h.id} aria-hidden style={{
              width: 15, height: 15, borderRadius: 3,
              border: `1.5px solid ${h.matched ? ORANGE : INK}`,
              background: h.matched ? ORANGE : 'transparent',
              transition: 'background 180ms ease, border-color 180ms ease',
            }} />
          ))}
          <span style={{ fontSize: 12.5, color: MUTED, marginLeft: 6 }}>
            {result.earned} of {result.total} marks — but he told you before the number did.
          </span>
        </div>
      </div>
    </div>
  );
};

/* ── II. The balance ───────────────────────────────────────────────────── */

const FOR_WORDS = ['benefit', 'advantage', 'gain', 'supports', 'improves', 'helps', 'increases', 'positive', 'strength', 'because it allows'];
const AGAINST_WORDS = ['however', 'but', 'cost', 'risk', 'drawback', 'disadvantage', 'limits', 'reduces', 'harms', 'negative', 'weakness', 'on the other hand'];

const weigh = (text: string) => {
  const t = ` ${text.toLowerCase()} `;
  const count = (words: string[]) => words.reduce((n, w) => n + (t.split(w).length - 1), 0);
  return { forSide: count(FOR_WORDS), againstSide: count(AGAINST_WORDS) };
};

const TheBalance: React.FC = () => {
  const lean = useMotionValue(0);
  const [answer, setAnswer] = useState('');
  const { forSide, againstSide } = useMemo(() => weigh(answer), [answer]);

  useEffect(() => {
    const total = forSide + againstSide;
    // Upright is balance. The tilt is the imbalance, not the volume: an essay
    // that argues six points each way stands as straight as one arguing one.
    const tilt = total === 0 ? 0 : ((againstSide - forSide) / total) * 11;
    animate(lean, tilt, { type: 'spring', stiffness: 120, damping: 18 });
  }, [forSide, againstSide, lean]);

  const total = forSide + againstSide;
  return (
    <div style={{ display: 'flex', gap: 34, alignItems: 'flex-end' }}>
      <Stage><StarguyFigure lean={lean} /></Stage>
      <div style={{ flex: 1, minWidth: 0 }}>
        <Quote ref_="The shape every “Discuss” question wants, and the one students most often miss.">
          Discuss the effects of foreign direct investment on the Irish economy.
        </Quote>
        <Field
          value={answer}
          onChange={e => setAnswer(e.target.value)}
          placeholder="Argue one side and he tips. Argue both and he stands up straight."
        />
        <p style={{ marginTop: 13, fontSize: 12.5, color: MUTED }}>
          {total === 0
            ? 'He is upright because you have not argued anything yet — not because you are balanced.'
            : `${forSide} for, ${againstSide} against. ${Math.abs(forSide - againstSide) <= 1 ? 'Level.' : 'He is carrying the heavier side.'}`}
        </p>
      </div>
    </div>
  );
};

/* ── III. The weight ───────────────────────────────────────────────────── */

const TARIFFS = [4, 6, 12, 25, 50, 75];

const TheWeight: React.FC = () => {
  const squash = useMotionValue(0);
  const [marks, setMarks] = useState(4);
  useEffect(() => {
    // 4 marks is a line. 75 is most of an hour. The press is logarithmic
    // because the difference between 4 and 12 is felt far more than 50 to 75.
    const load = Math.log(marks / 4) / Math.log(75 / 4);
    animate(squash, load, { type: 'spring', stiffness: 90, damping: 20 });
  }, [marks, squash]);

  return (
    <div style={{ display: 'flex', gap: 34, alignItems: 'flex-end' }}>
      <Stage><StarguyFigure squash={squash} /></Stage>
      <div style={{ flex: 1, minWidth: 0 }}>
        <p style={{ margin: '0 0 18px', maxWidth: 560, fontSize: 15.5, lineHeight: 1.5 }}>
          A tariff is a number until it is a feeling. Press one and watch what it asks of him.
        </p>
        <div style={{ display: 'flex', gap: 9, flexWrap: 'wrap' }}>
          {TARIFFS.map(m => (
            <button
              key={m}
              onClick={() => setMarks(m)}
              style={{
                border: `1.5px solid ${INK}`, borderRadius: 999, padding: '7px 17px',
                background: m === marks ? INK : '#fff', color: m === marks ? '#fff' : INK,
                fontFamily: 'inherit', fontSize: 13.5, cursor: 'pointer',
                transition: 'background 140ms ease, color 140ms ease',
              }}
            >{m} marks</button>
          ))}
        </div>
        <p style={{ marginTop: 15, fontSize: 12.5, color: MUTED, maxWidth: 560 }}>
          Same drawing, same pose, different bearing. Nobody has to be told that the
          75-mark question is the long one.
        </p>
      </div>
    </div>
  );
};

/* ── IV. The reader ────────────────────────────────────────────────────── */

const READING = [
  'A uniform beam of length 6 m and weight 400 N rests horizontally',
  'on two supports, one at each end. A load of 900 N is placed 2 m',
  'from the left-hand support. Find the reaction at each support.',
];

const TheReader: React.FC = () => {
  const lookX = useMotionValue(-1);
  const lookY = useMotionValue(-1);
  const [line, setLine] = useState(0);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (!running) return;
    let cancelled = false;
    const readLine = async (n: number): Promise<void> => {
      if (cancelled) return;
      setLine(n);
      // Down the page a line, then across it — the two movements a pair of
      // eyes actually makes. He is not watching you; he is reading this.
      await animate(lookY, -1 + (n / (READING.length - 1)) * 2, { duration: 0.22 }).finished;
      await animate(lookX, 1, { duration: 1.45, ease: 'linear' }).finished;
      if (cancelled) return;
      await animate(lookX, -1, { duration: 0.16, ease: 'easeInOut' }).finished;
      return readLine((n + 1) % READING.length);
    };
    void readLine(0);
    return () => { cancelled = true; };
  }, [running, lookX, lookY]);

  return (
    <div style={{ display: 'flex', gap: 34, alignItems: 'flex-end' }}>
      <Stage><StarguyFigure lookX={lookX} lookY={lookY} /></Stage>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ border: `1.5px solid ${INK}`, borderRadius: 12, padding: '18px 20px', fontFamily: SERIF, fontSize: 16, lineHeight: 1.85 }}>
          {READING.map((text, n) => (
            <div key={text} style={{
              color: running && n === line ? INK : '#B4AFA9',
              transition: 'color 220ms ease',
            }}>{text}</div>
          ))}
        </div>
        <button
          onClick={() => setRunning(r => !r)}
          style={{
            marginTop: 15, border: `1.5px solid ${INK}`, borderRadius: 999,
            padding: '8px 20px', background: running ? INK : '#fff',
            color: running ? '#fff' : INK, fontFamily: 'inherit', fontSize: 13.5, cursor: 'pointer',
          }}
        >{running ? 'Stop' : 'Read it with me'}</button>
        <p style={{ marginTop: 14, fontSize: 12.5, color: MUTED, maxWidth: 560 }}>
          Every other mascot on the internet watches the cursor. This one is looking
          at the question, which is where you should be looking too.
        </p>
      </div>
    </div>
  );
};

/* ── V. The pace ───────────────────────────────────────────────────────── */

const PAPER_MINUTES = 150;
const QUESTIONS = 6;

const ThePace: React.FC = () => {
  const speed = useMotionValue(0);
  const lean = useMotionValue(0);
  const [done, setDone] = useState(2);
  const [minutes, setMinutes] = useState(50);

  useEffect(() => {
    const shouldHaveDone = (minutes / PAPER_MINUTES) * QUESTIONS;
    const ahead = done - shouldHaveDone;          // +ahead of the clock, −behind
    // Behind the clock he strides; ahead of it he can afford to stand. The
    // gait is the instruction — nobody has to read a number off a timer.
    animate(speed, Math.max(0, Math.min(100, 46 - ahead * 34)), { type: 'spring', stiffness: 70, damping: 18 });
    animate(lean, Math.max(-6, Math.min(6, -ahead * 3.2)), { type: 'spring', stiffness: 80, damping: 20 });
  }, [done, minutes, speed, lean]);

  const shouldHaveDone = (minutes / PAPER_MINUTES) * QUESTIONS;
  const ahead = done - shouldHaveDone;
  return (
    <div style={{ display: 'flex', gap: 34, alignItems: 'flex-end' }}>
      <Stage><StarguyFigure speed={speed} lean={lean} /></Stage>
      <div style={{ flex: 1, minWidth: 0 }}>
        <p style={{ margin: '0 0 18px', maxWidth: 560, fontSize: 15.5, lineHeight: 1.5 }}>
          Two and a half hours, six questions. A countdown tells you that you are
          losing. A gait tells you how fast to walk.
        </p>
        <label style={{ display: 'block', fontSize: 13, marginBottom: 12 }}>
          Minutes gone · <strong>{minutes}</strong> of {PAPER_MINUTES}
          <input type="range" min={0} max={PAPER_MINUTES} value={minutes}
            onChange={e => setMinutes(Number(e.target.value))} style={{ width: '100%', accentColor: ORANGE }} />
        </label>
        <label style={{ display: 'block', fontSize: 13 }}>
          Questions finished · <strong>{done}</strong> of {QUESTIONS}
          <input type="range" min={0} max={QUESTIONS} value={done}
            onChange={e => setDone(Number(e.target.value))} style={{ width: '100%', accentColor: ORANGE }} />
        </label>
        <p style={{ marginTop: 14, fontSize: 12.5, color: MUTED }}>
          {Math.abs(ahead) < 0.35
            ? 'On the pace. He walks.'
            : ahead > 0
              ? `${ahead.toFixed(1)} questions ahead. He can stand still for a moment.`
              : `${Math.abs(ahead).toFixed(1)} behind. He picks the pace up, and leans into it.`}
        </p>
      </div>
    </div>
  );
};

/* ── the page ──────────────────────────────────────────────────────────── */

const Lab: React.FC = () => (
  <main style={{
    maxWidth: 940, margin: '0 auto', padding: '76px 28px 150px',
    background: '#fff', color: INK, fontFamily: 'DM Sans, system-ui, sans-serif',
  }}>
    <p style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.2em', textTransform: 'uppercase', color: ORANGE_TEXT, margin: 0 }}>
      NextStepUni · Starguy
    </p>
    <h1 style={{ fontFamily: SERIF, fontSize: 46, lineHeight: 1.08, margin: '10px 0 18px', fontWeight: 600, letterSpacing: '-0.02em', maxWidth: 660 }}>
      He has no face. That is the whole opportunity.
    </h1>
    <p style={{ maxWidth: 620, fontSize: 16, lineHeight: 1.6, color: MUTED, margin: '0 0 10px' }}>
      Starguy can look across and up, lean about the star, squash and stretch, and change
      his gait. Nothing in that list can smile, so nothing here tries to. A mascot reacts
      to you; an instrument makes something legible that was not legible before.
    </p>
    <p style={{ maxWidth: 620, fontSize: 16, lineHeight: 1.6, color: MUTED, margin: '0 0 8px' }}>
      Five ideas. Each maps one real thing about answering an exam question onto one thing
      the rig can already do. None of them needs him redrawn.
    </p>

    <Instrument
      numeral="I"
      title="The nod"
      thesis="An examiner listening to an oral nods when you say something creditworthy. Not a score, not a tick — a nod, while you are still talking. Every marking point you land, he nods once. The real scheme, the real question, no model in the loop."
      channel="channel · head, down and back"
    ><TheNod /></Instrument>

    <Instrument
      numeral="II"
      title="The balance"
      thesis="“Discuss” means both sides, and one-sidedness is the commonest way to lose marks on a long question. He leans toward whichever side you have argued more. You cannot read your own imbalance in your own prose. You can see it in him."
      channel="channel · lean about the star"
    ><TheBalance /></Instrument>

    <Instrument
      numeral="III"
      title="The weight"
      thesis="A tariff is a number until it is a feeling. Four marks is a line; seventy-five is most of an hour. Put the number on his shoulders and nobody has to be told which is the long one."
      channel="channel · squash and stretch"
    ><TheWeight /></Instrument>

    <Instrument
      numeral="IV"
      title="The reader"
      thesis="Every mascot on the internet watches your cursor. This one reads the question — down a line, across it, back to the margin, the two movements a pair of eyes actually makes. He is looking where you should be looking."
      channel="channel · head, across and down"
    ><TheReader /></Instrument>

    <Instrument
      numeral="V"
      title="The pace"
      thesis="Two and a half hours, six questions. A countdown tells a student they are losing. A gait tells them how fast to walk — and a walk is an instruction you can follow without doing arithmetic in an exam hall."
      channel="channel · gait, and a lean into it"
    ><ThePace /></Instrument>

    <div style={{ borderTop: `1.5px solid ${INK}`, paddingTop: 26, marginTop: 8 }}>
      <p style={{ fontSize: 13.5, color: MUTED, maxWidth: 620, lineHeight: 1.6, margin: 0 }}>
        All five use the rig that already shipped — <code>speed</code>, <code>lookX</code>,
        <code> lookY</code>, <code>lean</code>, <code>squash</code> — and the marking engine
        that already shipped. The drawing is untouched in every one.
      </p>
    </div>
  </main>
);

createRoot(document.getElementById('root')!).render(<React.StrictMode><Lab /></React.StrictMode>);
