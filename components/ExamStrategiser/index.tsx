/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Strategiser — top-level. Three peer views:
 *   - Practice: subject tabs → strategy preamble → question list → player
 *   - Trap Patterns: cross-subject trap library, with example links that
 *     navigate back into Practice mode at the linked question
 *   - Necessary Knowledge: the hidden curriculum — command words, PCLM,
 *     timing, examiner pet peeves, marking-scheme grammars
 */

import React, { useMemo, useState } from 'react';
import { EXAM_SUBJECTS } from '../../data/examQuestions';
import { type ExamQuestion, type ExamSubject } from '../../types/examStrategiser';
import QuestionList from './QuestionList';
import QuestionPlayer from './QuestionPlayer';
import SubjectStrategyPanel from './SubjectStrategyPanel';
import TrapLibrary from './TrapLibrary';
import NecessaryKnowledge, { type KnowledgeModuleId } from './knowledge/NecessaryKnowledge';
import CommandWordDecoder from './knowledge/modules/CommandWordDecoder';
import PCLMAllocator from './knowledge/modules/PCLMAllocator';
import TimeAllocationCalculator from './knowledge/modules/TimeAllocationCalculator';
import ExaminerPetPeeveTrainer from './knowledge/modules/ExaminerPetPeeveTrainer';
import MarkingSchemeGrammarExplainer from './knowledge/modules/MarkingSchemeGrammarExplainer';
import SrpIdentifier from './knowledge/modules/SrpIdentifier';
import WorkingShownAllocator from './knowledge/modules/WorkingShownAllocator';
import SanityCheckTrainer from './knowledge/modules/SanityCheckTrainer';
import SpotTheTrap from './knowledge/modules/SpotTheTrap';
import SubTaskCeilingVisualiser from './knowledge/modules/SubTaskCeilingVisualiser';
import ComparativeTextsLinker from './knowledge/modules/ComparativeTextsLinker';
import RsrSectionAllocator from './knowledge/modules/RsrSectionAllocator';
import PhraseMatch from './knowledge/modules/PhraseMatch';
import OralAuthenticityCoach from './knowledge/modules/OralAuthenticityCoach';

const TEAL = '#2A7D6F';

type View = 'practice' | 'patterns' | 'knowledge';

const ExamStrategiser: React.FC = () => {
  const [view, setView] = useState<View>('practice');
  const [subject, setSubject] = useState<ExamSubject>('english');
  const [activeQuestion, setActiveQuestion] = useState<ExamQuestion | null>(null);
  const [activeKnowledgeModule, setActiveKnowledgeModule] = useState<KnowledgeModuleId | null>(null);

  const questions = useMemo(
    () => EXAM_SUBJECTS.find(s => s.id === subject)?.questions ?? [],
    [subject],
  );

  /** Cross-view navigation — clicking a trap-pattern example switches to
   *  Practice mode at the right subject and opens the question. */
  const openQuestionById = (questionId: string) => {
    for (const meta of EXAM_SUBJECTS) {
      const q = meta.questions.find(qq => qq.id === questionId);
      if (q) {
        setSubject(meta.id);
        setActiveQuestion(q);
        setView('practice');
        return;
      }
    }
  };

  // Question-player view — full takeover when a question is active.
  if (activeQuestion) {
    return (
      <div className="max-w-4xl mx-auto w-full">
        <QuestionPlayer
          question={activeQuestion}
          onBackToList={() => setActiveQuestion(null)}
        />
      </div>
    );
  }

  // Knowledge module view — full takeover when a module is open.
  if (view === 'knowledge' && activeKnowledgeModule) {
    return (
      <div className="max-w-4xl mx-auto w-full">
        <KnowledgeModuleView
          moduleId={activeKnowledgeModule}
          onBack={() => setActiveKnowledgeModule(null)}
        />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto w-full space-y-6">
      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Exam Strategiser
        </p>
        <h1 className="font-serif" style={{ fontSize: 28, fontWeight: 600, color: '#1A1A1A', marginTop: 4, lineHeight: 1.2 }}>
          Real questions, decoded.
        </h1>
        <p className="font-sans max-w-xl" style={{ fontSize: 14, color: '#78716C', marginTop: 8, lineHeight: 1.55 }}>
          Predict before you see the answers. Then we walk through the question the way an examiner would — what to spot, what to avoid, where the marks live.
        </p>
      </header>

      {/* Top-level view switcher */}
      <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit">
        {([
          { id: 'practice', label: 'Practice' },
          { id: 'patterns', label: 'Trap Patterns' },
          { id: 'knowledge', label: 'Necessary Knowledge' },
        ] as const).map(opt => {
          const active = opt.id === view;
          return (
            <button
              key={opt.id}
              type="button"
              onClick={() => setView(opt.id)}
              className="rounded-lg transition-colors font-sans"
              style={{
                padding: '8px 16px',
                fontSize: 13,
                fontWeight: 600,
                backgroundColor: active ? '#FFFFFF' : 'transparent',
                color: active ? TEAL : '#78716C',
                border: 'none',
                cursor: 'pointer',
                boxShadow: active ? '0 1px 2px rgba(0,0,0,0.04)' : 'none',
              }}
            >
              {opt.label}
            </button>
          );
        })}
      </div>

      {view === 'practice' && (
        <>
          {/* Subject tabs */}
          <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit">
            {EXAM_SUBJECTS.map(s => {
              const active = s.id === subject;
              return (
                <button
                  key={s.id}
                  type="button"
                  onClick={() => setSubject(s.id)}
                  className="rounded-lg transition-colors font-sans"
                  style={{
                    padding: '8px 16px',
                    fontSize: 13,
                    fontWeight: 600,
                    backgroundColor: active ? '#FFFFFF' : 'transparent',
                    color: active ? TEAL : '#78716C',
                    border: 'none',
                    cursor: 'pointer',
                    boxShadow: active ? '0 1px 2px rgba(0,0,0,0.04)' : 'none',
                  }}
                >
                  {s.label}
                </button>
              );
            })}
          </div>

          <SubjectStrategyPanel subject={subject} />

          <QuestionList questions={questions} onSelect={(q) => setActiveQuestion(q)} />
        </>
      )}

      {view === 'patterns' && <TrapLibrary onOpenQuestion={openQuestionById} />}

      {view === 'knowledge' && (
        <NecessaryKnowledge onOpenModule={setActiveKnowledgeModule} />
      )}
    </div>
  );
};

const KnowledgeModuleView: React.FC<{ moduleId: KnowledgeModuleId; onBack: () => void }> = ({ moduleId, onBack }) => {
  switch (moduleId) {
    case 'command-words': return <CommandWordDecoder onBack={onBack} />;
    case 'pclm': return <PCLMAllocator onBack={onBack} />;
    case 'time-allocation': return <TimeAllocationCalculator onBack={onBack} />;
    case 'pet-peeves': return <ExaminerPetPeeveTrainer onBack={onBack} />;
    case 'marking-grammar': return <MarkingSchemeGrammarExplainer onBack={onBack} />;
    case 'srp-identifier': return <SrpIdentifier onBack={onBack} />;
    case 'working-shown': return <WorkingShownAllocator onBack={onBack} />;
    case 'sanity-check': return <SanityCheckTrainer onBack={onBack} />;
    case 'spot-the-trap': return <SpotTheTrap onBack={onBack} />;
    case 'ceiling-visualiser': return <SubTaskCeilingVisualiser onBack={onBack} />;
    case 'comparative-linker': return <ComparativeTextsLinker onBack={onBack} />;
    case 'rsr-allocator': return <RsrSectionAllocator onBack={onBack} />;
    case 'phrase-match': return <PhraseMatch onBack={onBack} />;
    case 'oral-coach': return <OralAuthenticityCoach onBack={onBack} />;
  }
};

export default ExamStrategiser;
