/**
 * Dev-only "Now" pane for the Kobra review (27 Oct 2026): the REAL onboarding,
 * components/onboarding/SetupFlow.tsx (the phone flow) and DesktopSetup.tsx
 * (the desktop flow), mounted on local sample answers. Both share one hook and
 * onboarding.css, exactly as components/Onboarding.tsx mounts them, inside the
 * same SoundEffects wrapper.
 *
 * The strip at the top is the review harness, not the screen: it switches
 * between the two flows and can open either at any step with sample answers
 * (kobra-review/sections/onboarding-sample.ts), written to the draft the flow
 * reads on mount. No account, no network: the funnel is silenced with the
 * app's own guest marker, and "Start Learning" / "Skip for now" only restart.
 *
 * The flow is `position: fixed; inset: 0`, so it is held in a transformed box
 * (a containing block for fixed children) under the harness strip.
 */
import { useState, type CSSProperties } from 'react';
import SetupFlow from '../../components/onboarding/SetupFlow';
import DesktopSetup from '../../components/onboarding/DesktopSetup';
import { SoundEffects } from '../../components/approved-ui-runtime';
import type { SetupStep } from '../../components/onboarding/model';
import { SAMPLE_NAME, SAMPLE_STEPS, seedSampleDraft, silenceFunnel } from '../sections/onboarding-sample';

silenceFunnel();

const USER_ID = 'kobra-review-now';
const params = new URLSearchParams(window.location.search);
const firstStep = (SAMPLE_STEPS.find(item => item.step === params.get('step'))?.step ?? 'welcome') as SetupStep;
seedSampleDraft(USER_ID, firstStep);
// ?settle=1 (screenshots only): finish entrance animations that headless virtual time leaves part-way.
if (params.get('settle')) setInterval(() => document.getAnimations().forEach(a => { try { if (a.effect?.getComputedTiming().iterations !== Infinity) a.finish(); } catch { /* ignore */ } }), 700);

const bar: CSSProperties = {
  display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '8px 14px', minHeight: 48, padding: '8px 14px',
  borderBottom: '1px dashed #a1a1aa', background: '#fff', color: '#3f3f46', font: "500 12px/1.3 'DM Sans', sans-serif",
};
const control: CSSProperties = {
  minHeight: 32, padding: '4px 10px', border: '1px solid #71717a', borderRadius: 8, background: '#fff', color: '#18181b',
  font: "500 12px/1 'DM Sans', sans-serif", cursor: 'pointer',
};

export default function OnboardingBefore() {
  const [flow, setFlow] = useState<'phone' | 'desktop'>(params.get('flow') === 'desktop' ? 'desktop' : 'phone');
  const [run, setRun] = useState(0);
  const [step, setStep] = useState<SetupStep>(firstStep);
  const restart = (next: SetupStep) => {
    seedSampleDraft(USER_ID, next);
    setStep(next);
    setRun(value => value + 1);
  };
  const props = {
    userId: USER_ID,
    userName: SAMPLE_NAME,
    onComplete: async () => { restart('welcome'); },
    onSkip: () => restart('welcome'),
  };
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <div style={bar} role="group" aria-label="Review harness">
        <span>Review harness: sample answers, no account</span>
        <span style={{ display: 'inline-flex', gap: 6 }}>
          {(['phone', 'desktop'] as const).map(value => (
            <button key={value} type="button" aria-pressed={flow === value} style={{ ...control, ...(flow === value ? { background: '#18181b', color: '#fff', borderColor: '#18181b' } : null) }}
              onClick={() => { setFlow(value); setRun(n => n + 1); }}>
              {value === 'phone' ? 'Phone flow' : 'Desktop flow'}
            </button>
          ))}
        </span>
        <label style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
          Open at
          <select value={step} style={control} onChange={event => restart(event.target.value as SetupStep)}>
            {SAMPLE_STEPS.map(item => <option key={item.step} value={item.step}>{item.label}</option>)}
          </select>
        </label>
      </div>
      <div style={{ position: 'relative', flex: 1, minHeight: 0, transform: 'translateZ(0)', overflow: 'hidden' }}>
        <SoundEffects>
          {flow === 'phone'
            ? <SetupFlow key={`phone-${run}`} {...props} />
            : <DesktopSetup key={`desktop-${run}`} {...props} />}
        </SoundEffects>
      </div>
    </div>
  );
}
