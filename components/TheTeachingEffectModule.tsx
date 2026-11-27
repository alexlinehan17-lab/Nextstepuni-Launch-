/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { motion } from 'framer-motion';
import { Brain,Flag,Lightbulb,MessageSquare,Users } from 'lucide-react';
import React,{ useId,useMemo,useState } from 'react';
import { TEACHING_EFFECT_REFERENCE_LIST } from '../data/references/teachingEffect';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { limeTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerLine,AnswerTick,ExerciseLabel,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { AreaField } from './ui/Field';

const theme = limeTheme;

// --- INTERACTIVE COMPONENTS ---

// 1. TEACH VS TEST COMPARISON (Planning Paradox style dual-chart)
const TeachVsTestComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const xLabels = ['Study', 'Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 30'];

  // Preparing for a Test: raw recall starts high but fades; organization stays low
  const testRecall = [0.70, 0.65, 0.55, 0.42, 0.30, 0.20];
  const testOrganization = [0.20, 0.22, 0.25, 0.22, 0.18, 0.15];

  // Preparing to Teach: raw recall moderate but stable; organization climbs strongly
  const teachRecall = [0.55, 0.52, 0.50, 0.48, 0.45, 0.42];
  const teachOrganization = [0.30, 0.45, 0.58, 0.68, 0.75, 0.80];

  const buildArea = (data: number[]) => {
    const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
    let d = `M ${pts[0].x} ${toY(0)} L ${pts[0].x} ${pts[0].y}`;
    for (let i = 1; i < pts.length; i++) {
      const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
      const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
      d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
    }
    d += ` L ${pts[pts.length - 1].x} ${toY(0)} Z`;
    return d;
  };

  const buildLine = (data: number[]) => {
    const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
    let d = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 1; i < pts.length; i++) {
      const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
      const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
      d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
    }
    return d;
  };

  // Phase words are ink (never a green or red sentence); the fading ones are quieter.
  const testPhases = [
    { label: 'Memorising facts', x1: 0, x2: 0.33, color: "var(--ink-primary)" },
    { label: 'Fading', x1: 0.33, x2: 0.66, color: "var(--ink-muted)" },
    { label: 'Fragmented', x1: 0.66, x2: 1, color: "var(--ink-muted)" },
  ];
  const teachPhases = [
    { label: 'Building framework', x1: 0, x2: 0.33, color: "var(--ink-primary)" },
    { label: 'Deepening', x1: 0.33, x2: 0.66, color: "var(--ink-primary)" },
    { label: 'Teachable', x1: 0.66, x2: 1, color: "var(--ink-primary)" },
  ];

  const Chart = ({ recall, organization, phases, areaColor, areaId, label }: {
    recall: number[]; organization: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
    areaColor: string; areaId: string; label: string;
  }) => (
    <svg viewBox={`0 0 ${W} ${H}`} className="ex-figure-art w-full h-auto">
      <defs>
        <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
          <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
        </linearGradient>
      </defs>
      {/* Grid lines */}
      {[0.25, 0.5, 0.75, 1.0].map(v => (
        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--hairline)" strokeDasharray="3 3" />
      ))}
      {/* Baseline */}
      <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--outline-soft)" />
      {/* Recall area */}
      <motion.path
        d={buildArea(recall)}
        fill={`url(#${areaId})`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      />
      {/* Recall line (solid) */}
      <motion.path
        d={buildLine(recall)}
        fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut' }}
      />
      {/* Organization line (dashed) */}
      <motion.path
        d={buildLine(organization)}
        fill="none" stroke="var(--ink-primary)" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
      />
      {/* Recall dots */}
      {recall.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (recall.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
          initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
        />
      ))}
      {/* Y-axis labels */}
      <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="var(--ink-muted)" fontWeight="600" style={{ fontFamily: 'var(--font-ui)' }}>High</text>
      <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="var(--ink-muted)" fontWeight="600" style={{ fontFamily: 'var(--font-ui)' }}>Low</text>
      {/* X-axis labels */}
      {xLabels.map((m, i) => (
        <text key={m} x={toX(i / (xLabels.length - 1))} y={toY(0) + 14} fontSize="9" fill="var(--ink-muted)" textAnchor="middle" fontWeight="600" style={{ fontFamily: 'var(--font-ui)' }}>{m}</text>
      ))}
      {/* Phase labels */}
      {phases.map((p, i) => (
        <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700" style={{ fontFamily: 'var(--font-ui)' }}>{p.label}</text>
      ))}
      {/* Chart label */}
      <text x={W / 2} y={14} fontSize="11" fill="var(--ink-secondary)" textAnchor="middle" fontWeight="700" style={{ fontFamily: 'var(--font-ui)' }}>{label}</text>
      {/* Legend */}
      <line x1={W - padR - 120} x2={W - padR - 104} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 100} y={17} fontSize="8" fill="var(--ink-muted)" style={{ fontFamily: 'var(--font-ui)' }}>Raw Recall</text>
      <line x1={W - padR - 54} x2={W - padR - 38} y1={14} y2={14} stroke="var(--ink-primary)" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 34} y={17} fontSize="8" fill="var(--ink-muted)" style={{ fontFamily: 'var(--font-ui)' }}>Organized</text>
    </svg>
  );

  return (
    <ExerciseSheet title="The Teach vs. Test Effect" sub="Same material. Different expectation. Dramatically different outcomes." name="TeachVsTestComparison">
      {!revealed ? (
        <div className="ex-stack">
          <p className="t-sub">What happens when you study to teach versus study to pass a test? The difference is not just how much you remember, but how you organize what you know.</p>
          <div className="ex-actions">
            <Button onClick={() => setRevealed(true)}>
              Reveal the Effect
            </Button>
          </div>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="flex flex-col gap-5">
          {/* The two charts on the sheet, no tinted boxes: ink for test prep, the green line for teaching prep */}
          <div className="grid md:grid-cols-2 gap-4">
            <div className="ex-figure">
              <Chart recall={testRecall} organization={testOrganization} phases={testPhases}
                areaColor="var(--ink-secondary)" areaId="test-grad" label="Preparing for a Test" />
            </div>
            <div className="ex-figure">
              <Chart recall={teachRecall} organization={teachOrganization} phases={teachPhases}
                areaColor="var(--success-hex)" areaId="teach-grad" label="Preparing to Teach" />
            </div>
          </div>
          {/* What each chart says: words you read, under a hairline, side by side on a laptop */}
          <div className="grid md:grid-cols-2 gap-4">
            <div className="ex-block">
              <p className="ex-block-text"><strong className="text-ink-primary">Test preppers</strong> take in facts quickly but store them as loose, disconnected pieces. Without any structure holding them together, those facts fade fast and fall apart under pressure.</p>
            </div>
            <div className="ex-block">
              <p className="ex-block-text"><strong className="text-ink-primary">Teaching preppers</strong> build a mental framework from the start. Even though they take in less at first, the organised structure means the knowledge sticks around and is easy to pull up when they need it.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

// 2. EXPLAIN IT BACK CHALLENGE
const ORIGINAL_CONCEPT = "Natural selection is the process by which organisms with traits better suited to their environment survive and reproduce at higher rates, passing those traits to the next generation. Over time, this differential survival and reproduction leads to changes in the inherited characteristics of a population, driving the adaptation of species to their environments.";

const ExplainItBackChallenge = () => {
  const [userText, setUserText] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const explanationLabelId = useId();

  const originalWords = useMemo(() => {
    const words = ORIGINAL_CONCEPT.toLowerCase().replace(/[.,;:!?'"()]/g, '').split(/\s+/);
    // Filter to meaningful words (skip common ones)
    const common = new Set(['the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'and', 'or', 'but', 'not', 'this', 'that', 'it', 'its', 'their', 'which', 'as', 'over', 'leads', 'more', 'than']);
    return new Set(words.filter(w => w.length > 3 && !common.has(w)));
  }, []);

  const analysis = useMemo(() => {
    if (!userText.trim()) return { wordCount: 0, jargonWords: [], simplicityScore: 0 };
    const words = userText.trim().split(/\s+/);
    const wordCount = words.length;
    const userWordsLower = userText.toLowerCase().replace(/[.,;:!?'"()]/g, '');
    const jargonWords: string[] = [];
    originalWords.forEach(ow => {
      if (userWordsLower.includes(ow)) {
        jargonWords.push(ow);
      }
    });
    // Simplicity: shorter is better (if key ideas preserved). Scale: 100 = very concise, 0 = very verbose
    const originalLen = ORIGINAL_CONCEPT.split(/\s+/).length;
    const ratio = wordCount / originalLen;
    const simplicityScore = ratio <= 0.5 ? 100 : ratio <= 1.0 ? Math.round(100 - (ratio - 0.5) * 120) : Math.max(0, Math.round(40 - (ratio - 1.0) * 60));
    return { wordCount, jargonWords, simplicityScore };
  }, [userText, originalWords]);

  const handleSubmit = () => {
    if (userText.trim().length > 10) setSubmitted(true);
  };

  const handleReset = () => {
    setUserText('');
    setSubmitted(false);
  };

  const isGood = analysis.jargonWords.length <= 2 && analysis.simplicityScore >= 60;
  const isMid = !isGood && analysis.jargonWords.length <= 5;

  return (
    <ExerciseSheet label="Feynman Technique" title="Explain It Back Challenge" sub="Explain this definition in simple terms — as if to a 12-year-old." name="ExplainItBackChallenge">
      {/* Zone 1 — the definition: words you start from, under their labels, not in a box */}
      <div className="ex-thought">
        <div className="flex items-baseline justify-between gap-3">
          <ExerciseLabel>The Definition</ExerciseLabel>
          <span className="ex-label">Biology</span>
        </div>
        <p className="ex-quote">{ORIGINAL_CONCEPT}</p>
      </div>

      {!submitted ? (
        <>
          {/* Connector */}
          <div className="ex-connector">
            <i aria-hidden="true" />
            <span className="ex-label">NOW EXPLAIN IT</span>
            <i aria-hidden="true" />
          </div>

          {/* Zone 2 — Response: its label and its aim above the field */}
          <div className="flex items-baseline justify-between gap-3">
            <p id={explanationLabelId} className="ex-label">Your Explanation</p>
            <span className="t-meta">Aim for 2–3 sentences</span>
          </div>
          <AreaField
            aria-labelledby={explanationLabelId}
            value={userText}
            onChange={(e) => setUserText(e.target.value)}
            placeholder="Imagine you're explaining this to a younger sibling..."
            rows={4}
          />

          {/* Live stats: three counts in a row under a hairline (the green tick where a count is good) */}
          {userText.trim().length > 0 && (
            <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-3 gap-2 pt-3 border-t border-hairline">
              <div className="flex flex-col items-center gap-1 text-center">
                <p className="m-0 t-heading text-ink-primary">{analysis.wordCount}</p>
                <p className="m-0 t-meta">Words</p>
              </div>
              <div className="flex flex-col items-center gap-1 text-center">
                <p className="m-0 t-heading text-ink-primary inline-flex items-center gap-1.5">{analysis.jargonWords.length}{analysis.jargonWords.length > 5 ? null : <AnswerTick />}</p>
                <p className="m-0 t-meta">Borrowed</p>
              </div>
              <div className="flex flex-col items-center gap-1 text-center">
                <p className="m-0 t-heading text-ink-primary inline-flex items-center gap-1.5">{analysis.simplicityScore}%{analysis.simplicityScore >= 60 ? <AnswerTick /> : null}</p>
                <p className="m-0 t-meta">Simplicity</p>
              </div>
            </MotionDiv>
          )}

          {analysis.jargonWords.length > 0 && (
            <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col gap-2">
              <ExerciseLabel>Words borrowed from original:</ExerciseLabel>
              {/* the words as plain words, spaced apart (no tags) */}
              <div className="flex flex-wrap gap-x-4 gap-y-1">
                {analysis.jargonWords.map((w, i) => (
                  <span key={i} className="t-sub">{w}</span>
                ))}
              </div>
            </MotionDiv>
          )}

          <div className="ex-actions">
            <Button
              onClick={handleSubmit}
              {...{ disabled: userText.trim().length <= 10 }}
              aria-pressed={!!(userText.trim().length > 10)}
            >
              Submit Explanation
            </Button>
          </div>
        </>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col gap-5">
          {/* Side by side comparison: two blocks of words under a hairline */}
          <div className="grid md:grid-cols-2 gap-4">
            <div className="ex-block">
              <span className="ex-label">Original</span>
              <p className="ex-block-text">{ORIGINAL_CONCEPT}</p>
            </div>
            <div className="ex-block">
              <span className="ex-label">Your Explanation</span>
              <p className="ex-block-text text-ink-primary">{userText}</p>
            </div>
          </div>

          {/* Stats row */}
          <div className="grid grid-cols-3 gap-2 pt-3 border-t border-hairline">
            <div className="flex flex-col items-center gap-1 text-center">
              <p className="m-0 t-heading text-ink-primary">{analysis.wordCount}</p>
              <p className="m-0 t-meta">Words</p>
            </div>
            <div className="flex flex-col items-center gap-1 text-center">
              <p className="m-0 t-heading text-ink-primary inline-flex items-center gap-1.5">{analysis.jargonWords.length}{analysis.jargonWords.length > 5 ? null : analysis.jargonWords.length > 2 ? null : <AnswerTick />}</p>
              <p className="m-0 t-meta">Borrowed</p>
            </div>
            <div className="flex flex-col items-center gap-1 text-center">
              <p className="m-0 t-heading text-ink-primary inline-flex items-center gap-1.5">{analysis.simplicityScore}%{analysis.simplicityScore >= 60 ? <AnswerTick /> : null}</p>
              <p className="m-0 t-meta">Simplicity</p>
            </div>
          </div>

          {/* Feedback: a line in ink; the typed tick stays, in the tick's green */}
          <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            {isGood ? (
              <AnswerLine tone="note">
                <span style={{ color: 'var(--success-hex)' }}>✓</span>{' '}
                <b>Explanation approved.</b> Nice one! You properly rebuilt that in your own words. That's exactly the kind of explaining that makes things stick long-term.
              </AnswerLine>
            ) : (
              <AnswerLine tone="note">
                {isMid
                  ? "Good effort, but some of your phrasing is pretty close to the original. Try pushing further — can you explain it using a totally different comparison or example?"
                  : "This reads like you're echoing the original rather than rebuilding it. Try closing the original, and explain it as if to a younger sibling. Use everyday examples."}
              </AnswerLine>
            )}
          </MotionDiv>

          <div className="ex-actions">
            <TextButton tone="quiet" onClick={handleReset}>
              Try again
            </TextButton>
          </div>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const TheTeachingEffectModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'protege-effect', title: 'Why Teaching Beats Testing', eyebrow: '01 // The Discovery', icon: Users },
    { id: 'explaining-forces-restructuring', title: 'Explaining Changes How You Think', eyebrow: '02 // How It Works', icon: Brain },
    { id: 'self-explanation-advantage', title: 'You Don\'t Need an Audience', eyebrow: '03 // Going Solo', icon: MessageSquare },
    { id: 'feynman-multiplier', title: 'The Simplicity Technique', eyebrow: '04 // The Technique', icon: Lightbulb },
    { id: 'teaching-protocol', title: 'Putting It All Together', eyebrow: '05 // Your System', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="46"
      moduleTitle="The Teaching Effect"
      moduleSubtitle="Learn It by Teaching It"
      moduleDescription="Want to actually remember what you study? Pretend you have to explain it to someone else. Seriously — it changes how your brain stores everything, even if you never teach a single person."
      theme={theme}
      sections={sections}
      references={TEACHING_EFFECT_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Teach It Forward"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why Teaching Beats Testing." eyebrow="Step 1" icon={Users} theme={theme}>
              {essentials ? (
                <>
                  <p><Highlight description="Two groups studied the same material. The 'teach it' group massively outperformed the 'test' group." theme={theme}>In one experiment</Highlight>, students told to prepare to teach outperformed students told to prepare for a test.<Cite n={1} /> The key: <Highlight description="Nobody actually taught. Just expecting to teach changed how they studied." theme={theme}>neither group actually taught anyone</Highlight>. Just believing you will teach changes how your brain processes material. This is <Highlight description="Your brain shifts from 'remember this' to 'explain this' — building connections automatically." theme={theme}>the teaching effect</Highlight>. Your brain shifts from storing facts to building connections.</p>
                </>
              ) : (
                <>
                  <p>Here is something that might surprise you. <Highlight description="Researchers gave two groups the exact same material to study. One group was told they'd be tested on it. The other was told they'd have to teach it to someone else afterwards. Same stuff, different mindset — and the 'teach it' group absolutely smashed it on every type of question." theme={theme}>In one experiment</Highlight>, two groups of students were given the exact same material to study. One group was told: "You will be tested on this." The other group was told: "You will teach this to another student afterwards."</p>
                  <p>The results were striking. The group who expected to teach remembered more and organised it better, especially the main points.<Cite n={1} /> But here is the mad part: <Highlight description="Nobody in the 'teach it' group actually taught anyone. Just thinking they'd have to teach was enough to change how their brains processed the material. So the magic isn't in the teaching itself — it's in how you prepare when you think you'll have to explain it." theme={theme}>neither group actually taught anyone</Highlight>. Just believing they would have to teach changed HOW they processed the material. Instead of passively absorbing facts, they started organising information, spotting the key ideas, and building explanations in their head — all without being told to do so.</p>
                  <p>This is <Highlight description="When you think you'll have to teach something, your brain shifts from 'how do I remember this?' to 'how do I explain this?' That one shift completely changes how you process information. You don't just store random facts — you build connections between them, because you know someone else would need to follow your thinking." theme={theme}>the teaching effect</Highlight>: teaching — even imagined teaching — restructures how you know things. When you expect to teach, your brain shifts from "How do I remember this?" to "How do I explain this?" That one shift changes everything. You stop just storing facts and start building connections between them, because you know someone else would need to follow your thinking.</p>
                </>
              )}
              <TeachVsTestComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Explaining Changes How You Think." eyebrow="Step 2" icon={Brain} theme={theme}>
              {essentials ? (
                <p><Highlight description="Explaining forces you to rebuild your understanding." theme={theme}>Explaining forces you to restructure what you know</Highlight>.<Cite n={2} /> There are two types. <Highlight description="Repeating the textbook word-for-word without transforming it." theme={theme}>Parroting</Highlight> is just echoing the textbook. <Highlight description="Explaining in your own words with your own examples." theme={theme}>Rebuilding</Highlight> is using your own comparisons and examples. Only rebuilding produces real learning. If your explanation sounds like the textbook, you are parroting. Use your own words and you will actually understand it.</p>
              ) : (
                <>
                  <p>So why does expecting to teach make such a big difference? It comes down to what happens when you try to explain something. <Highlight description="When you try to explain something, your brain is forced to take apart what you think you know and rebuild it in a way that actually makes sense. You can't explain something you don't truly get — so the explaining process shines a light on every gap and every bit you only half-understood." theme={theme}>Explaining forces you to restructure what you know</Highlight>.<Cite n={2} /> You can't explain something you don't truly understand, so the act of explaining — or even just preparing to explain — exposes every gap, every shallow connection, every concept you thought you understood but actually just recognised.</p>
                  <p>There are two types of explaining, and they are very different. The first is <Highlight description="This is when you basically parrot back the textbook definition without really changing anything. If your explanation uses the exact same words as the book, you're just repeating — not understanding. It feels like you know it, but you haven't actually processed it deeply." theme={theme}>parroting</Highlight> — simply repeating facts back in roughly the same form you received them. "Photosynthesis is the process by which plants convert light energy into chemical energy." That's parroting. You haven't transformed anything; you've just echoed the textbook. The second type is <Highlight description="This is when you come up with your own way to explain it — your own comparisons, your own examples, your own way of connecting the dots. This is where real learning happens, because you're actually rebuilding the idea in your own head rather than just copying someone else's version." theme={theme}>rebuilding</Highlight> — coming up with your own connections, comparisons, and examples. "It's like the plant is running a solar-powered factory — light is the electricity, CO2 and water are the raw materials, and glucose is the product that comes off the assembly line."</p>
                  <p>Only rebuilding produces real learning. The test is simple: if your explanation uses the exact same words as the textbook, you're just parroting. If you use your own comparisons, your own examples, your own structure — you're rebuilding. And it's rebuilding that gives you the deep, connected understanding that works on new problems and holds up under exam pressure.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="You Don't Need an Audience." eyebrow="Step 3" icon={MessageSquare} theme={theme}>
              {essentials ? (
                <>
                  <p>You do not need someone to teach. <Highlight description="In classic studies of physics learning, the students who spontaneously explained each worked example to themselves went on to solve far more new problems." theme={theme}>In studies of self-explanation</Highlight>, the students who spontaneously explained each step to themselves went on to solve far more new problems.<Cite n={2} /> <Highlight description="Pausing to put what you learned into your own words." theme={theme}>Explaining to yourself</Highlight> works almost as well as teaching someone else.</p>
                  <ConceptCardGrid
                    cards={[
                      { number: 1, term: "More Connections", description: "You make more connections between new stuff and things you already know." },
                      { number: 2, term: "Catch Misunderstandings", description: "You catch your own misunderstandings in real-time — trying to explain something exposes gaps that just re-reading never would." },
                      { number: 3, term: "Helps Most If You're Struggling", description: "It narrows the gap between students who find things easy and students who find things hard. So if you feel behind or confused, this is especially for you." },
                    ]}
                  />
                </>
              ) : (
                <>
                  <p>You might be thinking: "Grand, but I don't have someone to teach." Here's the good news — you don't need another person. <Highlight description="In classic studies of how students learn from worked examples, the ones who spontaneously explained to themselves why each step was taken went on to solve far more new problems. No audience needed — generating your own explanations is linked to deeper learning." theme={theme}>In classic studies with physics students</Highlight>, the ones who spontaneously explained to themselves why each step was taken went on to solve far more new problems.<Cite n={2} /></p>
                  <p><Highlight description="Explaining things to yourself means pausing while you're studying to put what you just learned into your own words. It works almost as well as explaining to another person because the hard work is the same — you have to pull the information together and make sense of it. Who's listening doesn't really matter; it's the thinking that counts." theme={theme}>Explaining to yourself</Highlight> — pausing after each concept to put it in your own words — works almost as well as explaining to another person. Here's why it's so powerful.</p>
                  <ConceptCardGrid
                    cards={[
                      { number: 1, term: "More Connections", description: "You make more connections between new stuff and things you already know." },
                      { number: 2, term: "Catch Misunderstandings", description: "You catch your own misunderstandings in real-time — trying to explain something exposes gaps that just re-reading never would." },
                      { number: 3, term: "Helps Most If You're Struggling", description: "It narrows the gap between students who find things easy and students who find things hard. So if you feel behind or confused, this is especially for you." },
                    ]}
                  />
                  <p>This is a proper equaliser. If you're struggling with a topic, your instinct is probably to re-read it more slowly. But that's the wrong move. Stop reading and start explaining — even if it's just to yourself. Even if your explanation is messy and full of gaps, the process of trying to put it into words is doing the heavy lifting that re-reading never will.</p>
                </>
              )}
              <ExplainItBackChallenge />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Simplicity Technique." eyebrow="Step 4" icon={Lightbulb} theme={theme}>
              {essentials ? (
                <p><Highlight description="Generating your own explanations is linked to deeper learning than passively reading." theme={theme}>Actively creating explanations</Highlight> is linked to deeper learning than passively reading.<Cite n={2} /> <Highlight description="Write the topic, explain it simply, notice where you get stuck, fill the gap." theme={theme}>Here is the technique</Highlight>. Write the topic on a blank page. Explain it as if to a younger sibling. When you stumble, go back and fill that gap. The places you stumble are exactly what you need to learn. If you can explain it to a 12-year-old, you truly get it.</p>
              ) : (
                <>
                  <p>Everything we've covered so far points to one simple idea: <Highlight description="When you actively create something — an explanation, a comparison, an example — rather than just passively reading, your learning goes through the roof. It's one of the most effective things you can do while studying. Even explaining to an imaginary audience works brilliantly." theme={theme}>actively creating explanations</Highlight> (even to an imaginary audience) is one of the most powerful things you can do while studying.<Cite n={2} /> It works because producing something forces your brain to do the hard work that passive reading skips over.</p>
                  <p>There's a brilliant four-step technique built around this idea. <Highlight description="This is a dead-simple four-step method. Write the topic at the top of a blank page, explain it as simply as you can (like you're talking to a younger sibling), notice where you get stuck, then go back to your notes and fill that specific gap. Each place you stumble is showing you exactly what you need to learn next." theme={theme}>Here's how it works</Highlight>. Step one: write the topic at the top of a blank page. Step two: explain it as if you were talking to a younger sibling — no jargon, no textbook phrases, just clear simple language with real examples. Step three: when you stumble — when you hit a point where your explanation breaks down or gets vague — go back to your notes and fill that specific gap. Step four: simplify even further and come up with comparisons that make it click.</p>
                  <p>The magic is in step three. The places where you stumble ARE the things you need to learn. Every moment where your explanation breaks down is a moment where your understanding has a hole in it. Without this technique, those holes stay invisible — your brain papers over them with a feeling of "yeah, I know this." This technique makes them visible, specific, and fixable. After each round, your explanation gets smoother and your understanding gets deeper. If you can explain a concept to a 12-year-old, you truly get it.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Putting It All Together." eyebrow="Step 5" icon={Flag} theme={theme}>
              {essentials ? (
                <>
                  <p><Highlight description="Reviews of study techniques rank self-testing among the most effective and highlighting and re-reading among the least." theme={theme}>Explaining and testing yourself</Highlight> beat highlighting and re-reading every time.<Cite n={3} /> Before studying, tell yourself "I will teach this." Take <Highlight description="Notes in your own words with your own examples." theme={theme}>notes in your own words</Highlight>. After studying, explain it out loud. For tough concepts, use the simplicity technique. <Highlight description="Write down where your explanation breaks down." theme={theme}>Track your stumble points</Highlight>. They become your study to-do list.</p>
                </>
              ) : (
                <>
                  <p>Let's bring everything together into a system you can use every time you sit down to study. Here's what it comes down to: <Highlight description="When you look at what actually works for learning, self-testing comes out near the top and self-explanation rates well too — while highlighting, re-reading, and summarising (which is what most of us spend our time doing) are among the least effective things you can do. This system swaps out the stuff that doesn't work for the stuff that does." theme={theme}>explaining things to yourself and testing yourself</Highlight> are among the most effective study techniques. Highlighting, re-reading, and summarising — the things most students spend their time on — are some of the least effective.<Cite n={3} /> This system is about swapping the stuff that doesn't work for the stuff that does.</p>
                  <p>Here's the system. Before each study session, set the intention: "I'm going to teach this to someone." That one mental shift changes how you process everything, even before you open a book. While studying, take <Highlight description="These are notes where you put things in your own words, draw connections to other topics, and come up with your own examples — instead of just copying the textbook word for word. It's the same idea as 'rebuilding' rather than 'parroting'. The Note-Taking Paradox module goes deeper on this." theme={theme}>notes in your own words</Highlight> — rephrase concepts, draw connections, and come up with your own examples rather than copying the textbook. After studying, explain the material out loud. It doesn't matter who you explain it to — a friend, your mam, the dog, the wall. The audience genuinely doesn't matter; it's the act of putting it into words that does the work.</p>
                  <p>For concepts that feel tough, use the simplicity technique from the last section. Write the concept, explain it simply, and spot your stumble points. Those stumble points become your to-do list for the next session. <Highlight description="When you write down the places where you got stuck, each study session gives you a clear list of what to work on next time. Over time, your stumble points list gets shorter as you fill the gaps, and you can actually see yourself making progress. This is way better than just re-reading everything and hoping for the best." theme={theme}>Track your stumble points</Highlight> — they are the most valuable thing you get from any study session, because they tell you exactly where your understanding breaks down. A stumble point you spot today is a mark saved in the exam tomorrow.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Pick one topic you're currently studying. Set a timer for 5 minutes and explain it out loud as if teaching a classmate who missed the lesson. No notes allowed. When you stumble — and you will — write down the exact point where you got stuck. That stumble point is your most valuable study target for tomorrow.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheTeachingEffectModule;
