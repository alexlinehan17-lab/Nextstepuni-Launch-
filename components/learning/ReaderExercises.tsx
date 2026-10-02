import { useEffect, useState } from 'react';
import { motion, useReducedMotion } from 'motion/react';
import { ArrowRight, RotateCcw } from 'lucide-react';
import { Button } from '../approved-ui-runtime';
import { Artwork, Eyebrow } from './shared';

const focused = Array.from({ length: 20 }, (_, i) => [
  160 + (i % 5) * 39,
  39 + Math.floor(i / 5) * 47,
]);
const diffuse = [
  [65, 58],
  [210, 31],
  [389, 48],
  [500, 110],
  [445, 201],
  [269, 179],
  [96, 207],
  [178, 110],
];
const routes = {
  focused: {
    d: 'M165 41 196 81 237 47 273 96 242 145 286 181 323 143',
    x: [165, 196, 237, 273, 242, 286, 323],
    y: [41, 81, 47, 96, 145, 181, 143],
  },
  diffuse: {
    d: 'M65 58 269 179 389 48 96 207 500 110 445 201',
    x: [65, 269, 389, 96, 500, 445],
    y: [58, 179, 48, 207, 110, 201],
  },
};

export function PinballExercise({
  initialMode = 'focused',
}: {
  initialMode?: 'focused' | 'diffuse';
}) {
  const [mode, setMode] = useState(initialMode);
  const [replay, setReplay] = useState(0);
  const reduced = useReducedMotion();
  const route = routes[mode];
  return (
    <section className="mr-exercise mr-pinball" aria-labelledby="pinball-title">
      <header>
        <div>
          <Eyebrow>Try the idea</Eyebrow>
          <h3 id="pinball-title">Give a thought some room.</h3>
        </div>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Replay the pinball illustration"
          onClick={() => setReplay(replay + 1)}
        >
          <RotateCcw />
        </Button>
      </header>
      <div className="mr-mode-buttons" role="group" aria-label="Pinball thinking mode">
        <Button
          variant="outline"
          aria-pressed={mode === 'focused'}
          onClick={() => setMode('focused')}
        >
          Focused mode
        </Button>
        <Button
          variant="outline"
          aria-pressed={mode === 'diffuse'}
          onClick={() => setMode('diffuse')}
        >
          Diffuse mode
        </Button>
      </div>
      <svg
        className="mr-pinball-board"
        viewBox="0 0 560 245"
        role="img"
        aria-label={
          mode === 'focused'
            ? 'A visual metaphor: closely spaced bumpers and a short path between nearby ideas.'
            : 'A visual metaphor: widely spaced bumpers and a path reaching across distant ideas.'
        }
      >
        <defs>
          <pattern id="pinball-grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <circle cx="1" cy="1" r=".8" fill="currentColor" opacity=".15" />
          </pattern>
        </defs>
        <rect width="560" height="245" fill="url(#pinball-grid)" />
        {(mode === 'focused' ? focused : diffuse).map(([x, y], index) => (
          <motion.circle
            key={`${mode}-${index}`}
            cx={x}
            cy={y}
            r={mode === 'focused' ? 8 : 11}
            fill="var(--nsu-surface)"
            stroke="var(--muted-foreground)"
            strokeWidth="1.4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          />
        ))}
        <motion.path
          key={`${mode}-${replay}-path`}
          d={route.d}
          fill="none"
          stroke="var(--rs-orange)"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          initial={{ pathLength: reduced ? 1 : 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: reduced ? 0 : 3.5, ease: 'linear' }}
        />
        <motion.circle
          key={`${mode}-${replay}-ball`}
          r="5"
          fill="var(--rs-orange)"
          initial={{ cx: route.x[0], cy: route.y[0] }}
          animate={{
            cx: reduced ? route.x.at(-1) : route.x,
            cy: reduced ? route.y.at(-1) : route.y,
          }}
          transition={{ duration: reduced ? 0 : 3.5, ease: 'linear' }}
        />
      </svg>
      <p aria-live="polite">
        {mode === 'focused'
          ? 'Close connections. Familiar steps. A useful way to think about focused practice.'
          : 'More room to roam. A useful way to picture connections between distant ideas.'}
      </p>
      <small>An illustration of the lesson’s pinball metaphor.</small>
    </section>
  );
}

// Same anagrams and hints as the current Bimodal Brain module.
const puzzles = [
  { letters: 'CSJUETI', answer: 'JUSTICE', hint: 'It’s something you find in a courtroom.' },
  { letters: 'ATECRHE', answer: 'TEACHER', hint: 'Found in every school.' },
  { letters: 'LEMPROB', answer: 'PROBLEM', hint: 'What you’re trying to solve right now.' },
];
export function IncubationExercise() {
  const [puzzle, setPuzzle] = useState(0);
  const [phase, setPhase] = useState<'focus' | 'break' | 'return' | 'solved' | 'revealed'>('focus');
  const [answer, setAnswer] = useState('');
  const [remaining, setRemaining] = useState(15);
  const [error, setError] = useState(false);
  const [hint, setHint] = useState(false);
  useEffect(() => {
    if (phase !== 'break') return;
    const timer = setInterval(() => setRemaining((value) => Math.max(0, value - 1)), 1000);
    return () => clearInterval(timer);
  }, [phase]);
  useEffect(() => {
    if (phase === 'break' && remaining === 0) setPhase('return');
  }, [remaining, phase]);
  const reset = () => {
    setPuzzle((puzzle + 1) % puzzles.length);
    setAnswer('');
    setError(false);
    setHint(false);
    setPhase('focus');
    setRemaining(15);
  };
  return (
    <section className="mr-exercise" aria-labelledby="incubation-title">
      <header>
        <div>
          <Eyebrow>Try the idea</Eyebrow>
          <h3 id="incubation-title">Work on it. Walk away. Return.</h3>
        </div>
        <span className="mr-exercise-counter">{puzzle + 1} / 3</span>
      </header>
      {phase === 'break' ? (
        <div className="mr-break">
          <Artwork src="/assets/star-crew/companions/thinker.png" size={110} />
          <h4>A little room to wander.</h4>
          <p>Look away from the screen. Let the word sit for a moment.</p>
          <span className="mr-break-time" aria-label={`${remaining} seconds left`}>
            {String(remaining).padStart(2, '0')}
            <small>s</small>
          </span>
          <Button variant="outline" onClick={() => setPhase('return')}>
            I’m ready to return <ArrowRight />
          </Button>
        </div>
      ) : phase === 'solved' || phase === 'revealed' ? (
        <div className="mr-puzzle-result" aria-live="polite">
          <h4>{phase === 'solved' ? 'There it is.' : 'The word was…'}</h4>
          <p className="mr-letters">{puzzles[puzzle].answer}</p>
          <p>Did returning to the problem feel any different?</p>
          <Button variant="outline" onClick={reset}>
            Try another word <RotateCcw />
          </Button>
        </div>
      ) : (
        <>
          <p>
            {phase === 'return'
              ? 'Come back with fresh eyes. Can you see the word now?'
              : 'Find the seven-letter word. If you get stuck, try a short break.'}
          </p>
          <div
            className="mr-letters"
            aria-label={`Letters: ${puzzles[puzzle].letters.split('').join(', ')}`}
          >
            {puzzles[puzzle].letters.split('').map((letter, i) => (
              <span key={i}>{letter}</span>
            ))}
          </div>
          <form
            onSubmit={(event) => {
              event.preventDefault();
              const correct = answer.trim().toUpperCase() === puzzles[puzzle].answer;
              setError(!correct);
              if (correct) setPhase('solved');
            }}
          >
            <label htmlFor="puzzle-answer">Your word</label>
            <div className="mr-answer-row">
              <input
                id="puzzle-answer"
                value={answer}
                autoComplete="off"
                maxLength={12}
                aria-invalid={error}
                aria-describedby={error ? 'puzzle-error' : undefined}
                onChange={(event) => {
                  setAnswer(event.target.value);
                  setError(false);
                }}
                placeholder="Type your answer…"
              />
              <Button variant="outline" type="submit" disabled={!answer.trim()}>
                Try it <ArrowRight />
              </Button>
            </div>
            {error && (
              <p id="puzzle-error" role="status">
                Not quite. Try a hint, or come back to it after a break.
              </p>
            )}
          </form>
          <div className="mr-exercise-actions">
            <Button
              variant="outline"
              onClick={() => {
                setRemaining(15);
                setPhase('break');
              }}
            >
              Take a 15-second break
            </Button>
            <Button variant="ghost" onClick={() => setHint(!hint)} aria-expanded={hint}>
              {hint ? 'Hide hint' : 'A little hint'}
            </Button>
            {phase === 'return' && (
              <Button variant="ghost" onClick={() => setPhase('revealed')}>
                Reveal word
              </Button>
            )}
          </div>
          {hint && (
            <p className="mr-hint" role="status">
              {puzzles[puzzle].hint}
            </p>
          )}
        </>
      )}
    </section>
  );
}
