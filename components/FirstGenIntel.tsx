/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  GraduationCap, ArrowRight, ArrowLeft, MapPin, Clock, BookOpen,
  Users, Coffee, HelpCircle, Mail, Calendar, CheckCircle,
  ChevronRight, Star, AlertCircle, MessageCircle, Lightbulb,
} from 'lucide-react';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useToast } from './Toast';

const MotionDiv = motion.div as any;

// ─── Types ───────────────────────────────────────────────────────────────────

interface FirstGenIntelProps {
  uid: string;
}

interface StageContent {
  id: string;
  title: string;
  icon: React.ElementType;
  scenes: Scene[];
}

interface Scene {
  heading: string;
  body: string;
  tip?: string;
  tipLabel?: string;
  realTalk?: string;
}

// ─── Content: Irish College System ───────────────────────────────────────────

const STAGES: StageContent[] = [
  {
    id: 'before',
    title: 'Before You Arrive',
    icon: Calendar,
    scenes: [
      {
        heading: 'The CAO offer is in. Now what?',
        body: 'You\'ve accepted your offer — well done. Now there\'s a gap between accepting and arriving. Use it. Most colleges send a "New Student" email pack in July or August. Read every word. It will have your student number, registration instructions, and orientation dates.',
        tip: 'Create a dedicated email folder for college correspondence. You\'ll get a lot of it and losing a registration email is stressful.',
        tipLabel: 'Practical Tip',
      },
      {
        heading: 'Registration & fees',
        body: 'Registration usually opens online in August. You\'ll need your student number and CAO offer details. If you have a SUSI grant, you still need to register — the grant covers fees but you need to confirm your place. If SUSI hasn\'t come through yet, don\'t panic — contact the college\'s fees office, they deal with this every year.',
        tip: 'SUSI applications open in spring. If you haven\'t applied yet, do it immediately. Processing takes weeks. Late applicants often wait longer for payments.',
        tipLabel: 'SUSI Note',
        realTalk: 'If you\'re worried about money, every college has a Student Assistance Fund (SAF) — emergency money for students in financial difficulty. No shame in it. It\'s literally there for you.',
      },
      {
        heading: 'What to expect on day one',
        body: 'Orientation week (usually the week before lectures start) is designed to stop you feeling lost. There\'ll be campus tours, society sign-ups, and talks about how your course works. Go to everything — even the stuff that sounds boring. This is where you learn the layout, meet people, and ask questions without judgement.',
        realTalk: 'You might look around and feel like everyone else knows what they\'re doing. They don\'t. First-years are all figuring it out together. The ones who look confident are usually just better at faking it.',
      },
    ],
  },
  {
    id: 'lectures',
    title: 'Lectures & Tutorials',
    icon: BookOpen,
    scenes: [
      {
        heading: 'What\'s a lecture?',
        body: 'A lecture is a talk by a lecturer to a large group — could be 30 people, could be 300. You sit, listen, and take notes. Nobody takes attendance in most lectures (some do — your course handbook will say). The lecturer won\'t check if you\'re keeping up. That\'s on you.',
        tip: 'Sit near the front. It sounds cringey, but you\'ll hear better, focus better, and the lecturer will recognise your face — which matters when you need help later.',
        tipLabel: 'What Good Students Do',
      },
      {
        heading: 'What\'s a tutorial?',
        body: 'Tutorials (or "tuts") are smaller group sessions — 15-25 people. A tutor (could be a lecturer or a postgrad student) goes through problems, questions, or discussion topics from the lectures. This is where you actually learn. Come prepared: review the lecture material before the tutorial.',
        realTalk: 'Tutorials are where the magic happens. If you skip anything, don\'t skip these. The students who struggle most are the ones who ghost tutorials and then can\'t follow the next lecture.',
      },
      {
        heading: 'Labs, practicals & workshops',
        body: 'Depending on your course, you might have labs (science), studio sessions (art/design), or workshops (engineering, IT). These are usually mandatory and attendance-tracked. You\'ll often submit work from these sessions. They count toward your final grade — don\'t treat them as optional.',
        tip: 'Lab coats, safety glasses, USB drives, specific software — check your course requirements before week 1. Don\'t be the person scrambling on day one.',
        tipLabel: 'Prep Tip',
      },
    ],
  },
  {
    id: 'grades',
    title: 'How Grades Work',
    icon: Star,
    scenes: [
      {
        heading: 'The honours system (not GPA)',
        body: 'Irish colleges use an honours classification system for Level 8 degrees. Your final degree result is one of these: First Class Honours (1st) — 70%+, Second Class Honours Grade I (2:1) — 60-69%, Second Class Honours Grade II (2:2) — 50-59%, Third Class Honours — 40-49%, Pass — 35-39%. Most employers and postgrad courses look for a 2:1 or above. A First is excellent but not essential.',
        tip: 'First year usually doesn\'t count toward your final degree classification — it\'s pass/fail. But the study habits you build (or don\'t) in first year will follow you. Treat it seriously.',
        tipLabel: 'First Year Truth',
      },
      {
        heading: 'ECTS credits',
        body: 'Each module (subject) is worth a certain number of ECTS credits — usually 5 or 10. A full year is 60 credits. You need to pass enough credits each year to progress. If you fail a module, you\'ll usually get a chance to repeat it in August/September exams. Failing too many means you might have to repeat the year.',
        realTalk: 'The credit system means every module matters. You can\'t just ace three subjects and ignore two — you need to pass them all. Spread your effort.',
      },
      {
        heading: 'Continuous assessment vs exams',
        body: 'Most modules combine continuous assessment (CA) and end-of-semester exams. CA includes assignments, projects, presentations, lab reports, and in-class tests — typically 20-50% of your final grade. Exams cover the rest. The split varies by module — check your course handbook.',
        tip: 'CA marks are free points. Seriously. Assignments you can work on at home, with resources, over days or weeks — versus a 2-hour exam under pressure. Maximise your CA grades.',
        tipLabel: 'Strategy',
      },
    ],
  },
  {
    id: 'survival',
    title: 'Daily Survival Guide',
    icon: Coffee,
    scenes: [
      {
        heading: 'Gaps between lectures',
        body: 'You\'ll have gaps — sometimes 2-3 hours between classes. This is where your week is won or lost. What NOT to do: go home, scroll your phone for 2 hours, or sit in the canteen all day. What TO do: go to the library, review the lecture you just had, start that assignment, or read ahead for the next class.',
        tip: 'The library is your second home. Find a regular spot. Treat your gaps as built-in study sessions.',
        tipLabel: 'Key Habit',
        realTalk: 'Nobody is going to make you study during gaps. There\'s no bell, no teacher, no parent. The discipline gap is the single biggest reason students struggle in first year.',
      },
      {
        heading: 'Money & budgeting',
        body: 'If you\'re on a SUSI grant or working part-time, money will be tight. Free resources: the library has textbooks (don\'t buy them until you know you need them), the SU often has free/cheap food events, and there\'s usually a book exchange in September. Most student clubs and societies are free to join.',
        tip: 'Don\'t buy textbooks in week 1. Wait until the lecturer confirms you actually need them. Many modules provide notes online or use library copies. Check if older students are selling theirs.',
        tipLabel: 'Save Money',
      },
      {
        heading: 'The social side',
        body: 'College social life doesn\'t have to mean drinking. Join societies and clubs — they\'re the fastest way to make friends with similar interests. Most colleges have 50-100+ clubs: sports, gaming, debating, drama, volunteering, and more. Sign up at the Freshers\' Fair in week 1. Even if you\'re shy — commit to showing up twice.',
        realTalk: 'If you don\'t drink, you\'re not alone. Plenty of students don\'t. The "college drinking culture" stereotype is louder than reality. Find your people through societies — they\'re there.',
      },
    ],
  },
  {
    id: 'help',
    title: 'Getting Help',
    icon: HelpCircle,
    scenes: [
      {
        heading: 'How to email a lecturer',
        body: 'This might sound small but it trips up a lot of first-years. Use your college email (not your personal one). Subject line: the module code and a clear topic. Start with "Dear Dr./Prof. [Surname]" (check their title on the college website). Be specific about your question. Sign off with your name and student number.',
        tip: 'Example: "Dear Dr. Murphy, I\'m in your BT1234 Economics module. I\'m struggling with the concept of elasticity from this week\'s lecture. Would it be possible to discuss this during your office hours? Thanks, [Your Name], Student No. 12345678"',
        tipLabel: 'Template',
      },
      {
        heading: 'Office hours',
        body: 'Most lecturers have set "office hours" — times when you can drop in or book a slot to ask questions. These are published on the module page or the lecturer\'s staff profile. Use them. Lecturers expect students to show up. Going to office hours is not a sign of weakness — it\'s what the best students do.',
        realTalk: 'Lecturers can\'t help you if they don\'t know you\'re struggling. They\'re not mind readers. The students who ask for help early almost always do better than the ones who suffer in silence.',
      },
      {
        heading: 'Student support services',
        body: 'Every college has support services — and they\'re free: Counselling service (mental health, stress, anxiety), Disability/access service (learning support, exam accommodations), Academic writing centre (essay help, referencing), Maths/stats support, Career service, Students\' Union welfare officer. These exist because students need them. Using them is normal, not a sign of failure.',
        tip: 'Book counselling early in the semester, not when you\'re in crisis. Wait times can be 2-3 weeks at peak times. Proactive beats reactive.',
        tipLabel: 'Timing',
      },
    ],
  },
  {
    id: 'hidden',
    title: 'The Hidden Curriculum',
    icon: Lightbulb,
    scenes: [
      {
        heading: 'Things nobody tells you',
        body: 'Nobody explains that you need to read beyond the lecture slides. Nobody tells you that sitting in the back corner looking at your phone means you\'ll retain almost nothing. Nobody warns you that missing week 3 means week 4 won\'t make sense. College assumes you\'ll figure these things out. Now you know.',
        realTalk: 'The "hidden curriculum" is all the unwritten rules that students from educated families absorb at the dinner table. If your parents didn\'t go to college, you have to learn these rules explicitly. That\'s what this guide is for.',
      },
      {
        heading: 'Academic integrity',
        body: 'Plagiarism (copying someone else\'s work) is taken very seriously. Colleges use Turnitin and other software to check assignments. The rule is simple: if it\'s not your own words or ideas, reference the source. Every college has a referencing guide (Harvard, APA, etc.) — learn your course\'s required style in week 1. When in doubt, cite.',
        tip: 'The academic writing centre will teach you how to reference properly. Go in week 2, not week 10 when your first essay is due.',
        tipLabel: 'Critical',
      },
      {
        heading: 'You belong here',
        body: 'Imposter syndrome is real. You might feel like you got in by accident, or that everyone else is smarter. This is especially common for first-gen students. Here\'s the truth: you earned your place. The CAO system is points-based and objective. You met the requirement. You belong. The feeling of not belonging fades — but only if you stay, show up, and engage.',
        realTalk: 'Every year, thousands of students from every background walk into Irish colleges feeling the exact same fear. The ones who succeed aren\'t the ones who feel no fear — they\'re the ones who feel it and keep going anyway.',
      },
    ],
  },
];

// ─── Component ───────────────────────────────────────────────────────────────

const FirstGenIntel: React.FC<FirstGenIntelProps> = ({ uid }) => {
  const { showToast } = useToast();
  const [phase, setPhase] = useState<'intro' | 'guide' | 'complete'>('intro');
  const [stageIdx, setStageIdx] = useState(0);
  const [sceneIdx, setSceneIdx] = useState(0);
  const [completedStages, setCompletedStages] = useState<string[]>([]);

  // Load progress
  useEffect(() => {
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        const data = snap.data()?.firstGenIntel;
        if (data?.completedStages) {
          setCompletedStages(data.completedStages);
          if (data.completedStages.length >= STAGES.length) {
            setPhase('complete');
          }
        }
      } catch (e) {
        console.error('Failed to load First Gen Intel data:', e);
      }
    })();
  }, [uid]);

  // Save progress
  const saveProgress = useCallback(async (completed: string[]) => {
    try {
      await setDoc(doc(db, 'progress', uid), {
        firstGenIntel: { completedStages: completed, savedAt: new Date().toISOString() },
      }, { merge: true });
    } catch (e) {
      console.error('Failed to save First Gen Intel:', e);
    }
  }, [uid]);

  const stage = STAGES[stageIdx];
  const scene = stage?.scenes[sceneIdx];
  const totalScenes = STAGES.reduce((sum, s) => sum + s.scenes.length, 0);
  const currentSceneGlobal = STAGES.slice(0, stageIdx).reduce((sum, s) => sum + s.scenes.length, 0) + sceneIdx;

  const handleNext = () => {
    if (sceneIdx < stage.scenes.length - 1) {
      setSceneIdx(sceneIdx + 1);
    } else if (stageIdx < STAGES.length - 1) {
      // Mark stage complete
      const updated = [...new Set([...completedStages, stage.id])];
      setCompletedStages(updated);
      saveProgress(updated);
      setStageIdx(stageIdx + 1);
      setSceneIdx(0);
    } else {
      // All done
      const updated = [...new Set([...completedStages, stage.id])];
      setCompletedStages(updated);
      saveProgress(updated);
      setPhase('complete');
    }
  };

  const handleBack = () => {
    if (sceneIdx > 0) {
      setSceneIdx(sceneIdx - 1);
    } else if (stageIdx > 0) {
      const prevStage = STAGES[stageIdx - 1];
      setStageIdx(stageIdx - 1);
      setSceneIdx(prevStage.scenes.length - 1);
    }
  };

  const jumpToStage = (idx: number) => {
    setStageIdx(idx);
    setSceneIdx(0);
    setPhase('guide');
  };

  // ── Intro Phase ──
  if (phase === 'intro') {
    return (
      <div className="space-y-6">
        <div className="text-center py-6">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-violet-100 dark:bg-violet-900/30 mb-4">
            <GraduationCap size={32} className="text-violet-600 dark:text-violet-400" />
          </div>
          <h2 className="font-serif text-2xl font-bold text-zinc-900 dark:text-white">First Gen Intel</h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 max-w-sm mx-auto leading-relaxed">
            The honest guide to Irish college that nobody gives you. Everything a first-generation student needs to know — from registration to surviving first year.
          </p>
        </div>

        {/* Stage overview */}
        <div className="space-y-2">
          {STAGES.map((s, idx) => {
            const Icon = s.icon;
            const isComplete = completedStages.includes(s.id);
            return (
              <button
                key={s.id}
                onClick={() => jumpToStage(idx)}
                className="w-full flex items-center gap-4 p-4 rounded-xl bg-white/60 dark:bg-white/5 border border-zinc-200/60 dark:border-white/10 hover:bg-white dark:hover:bg-white/10 transition-all text-left"
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
                  isComplete
                    ? 'bg-emerald-100 dark:bg-emerald-900/30'
                    : 'bg-violet-100 dark:bg-violet-900/30'
                }`}>
                  {isComplete ? (
                    <CheckCircle size={20} className="text-emerald-500" />
                  ) : (
                    <Icon size={20} className="text-violet-600 dark:text-violet-400" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{s.title}</p>
                  <p className="text-[11px] text-zinc-400 dark:text-zinc-500">{s.scenes.length} sections</p>
                </div>
                <ChevronRight size={16} className="text-zinc-300 dark:text-zinc-600 shrink-0" />
              </button>
            );
          })}
        </div>

        <button
          onClick={() => setPhase('guide')}
          className="w-full py-3.5 rounded-xl text-sm font-bold text-white bg-violet-500 hover:bg-violet-600 shadow-lg shadow-violet-500/20 transition-all"
        >
          {completedStages.length > 0 ? 'Continue Reading' : 'Start the Guide'}
        </button>
      </div>
    );
  }

  // ── Complete Phase ──
  if (phase === 'complete') {
    return (
      <div className="space-y-6">
        <div className="text-center py-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-emerald-100 dark:bg-emerald-900/30 mb-4">
            <CheckCircle size={32} className="text-emerald-500" />
          </div>
          <h2 className="font-serif text-2xl font-bold text-zinc-900 dark:text-white">You're Ready</h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 max-w-sm mx-auto leading-relaxed">
            You've read through the complete guide. You now know more about how Irish college works than most first-years do on day one. That's a real advantage.
          </p>
        </div>

        <div className="bg-violet-50 dark:bg-violet-900/15 border border-violet-200 dark:border-violet-800/30 rounded-xl p-5">
          <p className="text-sm font-bold text-violet-700 dark:text-violet-300 mb-2">Remember:</p>
          <ul className="space-y-2">
            {[
              'You earned your place. The CAO system is objective.',
              'Ask for help early — it\'s what the best students do.',
              'Gaps between lectures are where your week is won or lost.',
              'CA marks are free points. Maximise them.',
              'Feeling lost is normal. Staying is what matters.',
            ].map((item, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-violet-600 dark:text-violet-400">
                <CheckCircle size={12} className="text-violet-500 shrink-0 mt-0.5" />
                {item}
              </li>
            ))}
          </ul>
        </div>

        <button
          onClick={() => { setPhase('intro'); }}
          className="w-full py-3 rounded-xl text-sm font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-all"
        >
          Back to Sections
        </button>
      </div>
    );
  }

  // ── Guide Phase ──
  const StageIcon = stage.icon;

  return (
    <div className="space-y-5">
      {/* Progress bar */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <StageIcon size={14} className="text-violet-500" />
            <span className="text-[10px] font-bold uppercase tracking-widest text-violet-500">
              {stage.title}
            </span>
          </div>
          <span className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500">
            {currentSceneGlobal + 1} / {totalScenes}
          </span>
        </div>
        <div className="w-full h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
          <MotionDiv
            className="h-full bg-violet-500 rounded-full"
            animate={{ width: `${((currentSceneGlobal + 1) / totalScenes) * 100}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      {/* Scene content */}
      <AnimatePresence mode="wait">
        <MotionDiv
          key={`${stageIdx}-${sceneIdx}`}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.25 }}
          className="space-y-4"
        >
          <h3 className="font-serif text-xl font-bold text-zinc-900 dark:text-white leading-snug">
            {scene.heading}
          </h3>

          <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed whitespace-pre-line">
            {scene.body}
          </p>

          {/* Tip box */}
          {scene.tip && (
            <div className="bg-violet-50 dark:bg-violet-900/15 border border-violet-200 dark:border-violet-800/30 rounded-xl p-4">
              <div className="flex items-start gap-3">
                <Lightbulb size={16} className="text-violet-500 shrink-0 mt-0.5" />
                <div>
                  {scene.tipLabel && (
                    <p className="text-[10px] font-bold uppercase tracking-widest text-violet-500 mb-1">{scene.tipLabel}</p>
                  )}
                  <p className="text-xs text-violet-700 dark:text-violet-300 leading-relaxed">{scene.tip}</p>
                </div>
              </div>
            </div>
          )}

          {/* Real Talk box */}
          {scene.realTalk && (
            <div className="bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-4">
              <div className="flex items-start gap-3">
                <MessageCircle size={16} className="text-amber-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-amber-500 mb-1">Real Talk</p>
                  <p className="text-xs text-zinc-600 dark:text-zinc-400 leading-relaxed italic">{scene.realTalk}</p>
                </div>
              </div>
            </div>
          )}
        </MotionDiv>
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex items-center gap-3 pt-2">
        <button
          onClick={handleBack}
          disabled={stageIdx === 0 && sceneIdx === 0}
          className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-sm font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <ArrowLeft size={14} /> Back
        </button>
        <div className="flex-1" />
        <button
          onClick={handleNext}
          className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl text-sm font-bold text-white bg-violet-500 hover:bg-violet-600 shadow-sm transition-all"
        >
          {stageIdx === STAGES.length - 1 && sceneIdx === stage.scenes.length - 1
            ? 'Finish'
            : sceneIdx === stage.scenes.length - 1
              ? 'Next Section'
              : 'Next'
          }
          <ArrowRight size={14} />
        </button>
      </div>

      {/* Stage dots */}
      <div className="flex items-center justify-center gap-1.5 pt-2">
        {STAGES.map((s, idx) => (
          <button
            key={s.id}
            onClick={() => jumpToStage(idx)}
            className={`w-2 h-2 rounded-full transition-all ${
              idx === stageIdx
                ? 'bg-violet-500 w-4'
                : completedStages.includes(s.id)
                  ? 'bg-emerald-400'
                  : 'bg-zinc-300 dark:bg-zinc-700'
            }`}
          />
        ))}
      </div>
    </div>
  );
};

export default FirstGenIntel;
