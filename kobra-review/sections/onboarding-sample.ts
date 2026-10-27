/**
 * Dev-only (Kobra review, 27 Oct 2026). Sample answers for the onboarding
 * review: the "Now" pane (kobra-review/before/OnboardingBefore.tsx) and the
 * Kobra rebuild (OnboardingAfter.tsx) both seed the REAL setup draft with
 * these, so either pane can open at any step. Nothing here is an account.
 */
import { DAYS_OF_WEEK } from '../../components/subjectData';
import { draftKey, initialDraft, type SetupDraft, type SetupStep } from '../../components/onboarding/model';
import { setGuestPhase } from '../../components/onboarding/guest';

export const SAMPLE_NAME = 'Aoife Byrne';

export const SAMPLE_STEPS: { step: SetupStep; label: string }[] = [
  { step: 'welcome', label: 'Welcome' },
  { step: 'year', label: 'School year' },
  { step: 'north', label: 'North Star' },
  { step: 'vision', label: 'Vision board' },
  { step: 'subjects', label: 'Subjects' },
  { step: 'grades', label: 'Grades' },
  { step: 'schedule', label: 'Exam date and week' },
  { step: 'summary', label: 'Summary' },
];

const reviewed = (level: 'higher' | 'ordinary' | 'foundation', current: string, target: string) =>
  ({ level, current, target, reviewed: true }) as SetupDraft['configs'][string];

/** A 5th Year with six subjects; grades are filled up to the step asked for. */
export function sampleDraft(step: SetupStep): SetupDraft {
  const base = initialDraft();
  if (step === 'welcome') return base;
  const later = ['subjects', 'grades', 'schedule', 'summary'].includes(step);
  const draft: SetupDraft = {
    ...base,
    step,
    year: '5th',
    category: step === 'year' || step === 'north' ? null : 'options-freedom',
    vision: ['vision', 'subjects', 'grades', 'schedule', 'summary'].includes(step) ? ['real-choices', 'see-world'] : [],
    subjects: later ? ['English', 'Irish', 'Mathematics', 'Biology', 'French', 'Geography'] : [],
    configs: {},
    rest: ['Friday', 'Saturday'],
    dateConfirmed: step === 'summary',
    gradeSubject: null,
  };
  if (step === 'year') {
    // Subjects already chosen, so picking a Junior Cycle year opens the warning dialog.
    draft.subjects = ['English', 'Mathematics', 'Biology'];
    draft.category = 'options-freedom';
  }
  if (later) {
    const all = step === 'schedule' || step === 'summary';
    draft.configs = {
      English: reviewed('higher', 'H3', 'H2'),
      Irish: reviewed('higher', 'H4', 'H3'),
      Mathematics: all ? reviewed('higher', 'H4', 'H2') : { level: 'higher', current: '', target: '', reviewed: false },
      Biology: all ? reviewed('higher', 'H3', 'H1') : { level: null, current: '', target: '', reviewed: false },
      French: all ? reviewed('ordinary', 'O2', 'H4') : { level: null, current: '', target: '', reviewed: false },
      Geography: all ? reviewed('higher', 'H2', 'H1') : { level: null, current: '', target: '', reviewed: false },
    };
    if (step === 'subjects') draft.configs = {};
    if (step === 'grades') draft.gradeSubject = 'Mathematics';
  }
  if (step === 'north' || step === 'year') draft.rest = [...DAYS_OF_WEEK];
  return draft;
}

/** Write the sample draft where the real flow reads it on mount. */
export function seedSampleDraft(userId: string, step: SetupStep) {
  try {
    localStorage.setItem(draftKey(userId, 'fresh'), JSON.stringify(sampleDraft(step)));
  } catch { /* private mode: the flow starts at Welcome */ }
}

/**
 * The real flow records funnel steps to Firestore; a review pane has no
 * account, so it must record nothing. The guest-setup marker is the app's own
 * switch for that (utils/funnel.ts returns early while it is set). It lives in
 * this tab's sessionStorage only and is removed when the page goes away.
 */
export function silenceFunnel() {
  setGuestPhase('onboarding');
  window.addEventListener('pagehide', () => {
    try { sessionStorage.removeItem('nsu:guest-setup:phase'); } catch { /* storage unavailable */ }
  }, { once: true });
}
