import React, { useEffect, useRef, useState } from 'react';
import {
  ArrowRight,
  ArrowUpRight,
  Check,
  GraduationCap,
  Plus,
  Volume2,
  VolumeX,
  X,
} from 'lucide-react';
import Avatar from './Avatar';
import { WelcomeCharacter } from './WelcomeCharacter';
import { PERSONAL_STAR_CREW } from '../data/personalStarCrew';
import { useModal } from '../hooks/useModal';
import { useDeckSound } from './immersiveDeck/useDeckSound';
import './account-live.css';

export const AuthWordmark = () => (
  <span className="auth-live-wordmark">
    nextstepuni<span>.</span>
  </span>
);
interface AccountCardProps {
  children: React.ReactNode;
  devButton?: React.ReactNode;
  view: string;
  registerStep: number;
  avatar: string;
  name: string;
  school: string;
  busy: boolean;
  onAvatarChange: (avatar: string) => void;
  onWelcome: () => void;
  onSchoolAccess: () => void;
}
export default function AccountCard({
  children,
  devButton,
  view,
  registerStep,
  avatar,
  name,
  school,
  busy,
  onAvatarChange,
  onWelcome,
  onSchoolAccess,
}: AccountCardProps) {
  const [pickerOpen, setPickerOpen] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(() => {
    try {
      return localStorage.getItem('nextstepuni:account-sound') !== 'off';
    } catch {
      return true;
    }
  });
  const { play, setEnabled } = useDeckSound();
  useEffect(() => {
    setEnabled(soundEnabled);
  }, [soundEnabled, setEnabled]);
  const toggleSound = () => {
    const enabled = !soundEnabled;
    setEnabled(enabled);
    setSoundEnabled(enabled);
    try {
      localStorage.setItem('nextstepuni:account-sound', enabled ? 'on' : 'off');
    } catch {
      /* Storage can be unavailable in private webviews. */
    }
    if (enabled) play('tap');
  };
  const playControlSound = (event: React.MouseEvent<HTMLElement>) => {
    const button =
      event.target instanceof Element ? event.target.closest('button') : null;
    if (
      !button ||
      !event.currentTarget.contains(button) ||
      button.matches(':disabled')
    )
      return;
    const cue = button.dataset.accountSound;
    if (cue === 'off') return;
    play(cue === 'save' || cue === 'swipe' || cue === 'skip' ? cue : 'tap');
  };
  const picker = useRef<HTMLDivElement>(null);
  useModal(pickerOpen, () => setPickerOpen(false), picker);
  return (
    <main
      className="auth-live theme-compat"
      data-view={view}
      onClickCapture={playControlSound}
    >
      <section className="auth-live-shell" aria-label="NextStepUni account">
        <header className="auth-live-brandbar">
          <button
            type="button"
            onClick={onWelcome}
            disabled={busy}
            aria-label="NextStepUni welcome"
          >
            <AuthWordmark />
          </button>
          <div className="auth-live-header-actions">
            <button
              type="button"
              className="auth-live-quiet auth-live-sound"
              data-account-sound="off"
              aria-label={soundEnabled ? 'Mute sounds' : 'Turn sounds on'}
              aria-pressed={soundEnabled}
              onClick={toggleSound}
            >
              {soundEnabled ? (
                <Volume2 size={17} aria-hidden="true" />
              ) : (
                <VolumeX size={17} aria-hidden="true" />
              )}
              <span>Sound {soundEnabled ? 'on' : 'off'}</span>
            </button>
            <button
              type="button"
              className="auth-live-quiet auth-live-school-access"
              disabled={busy}
              onClick={onSchoolAccess}
            >
              <GraduationCap size={17} aria-hidden="true" />
              {view === 'gc' ? 'Student sign-in' : 'For schools'}
              <ArrowUpRight size={15} aria-hidden="true" />
            </button>
          </div>
        </header>
        <div className="auth-live-layout">
          <aside className="auth-live-identity">
            <h2>
              Built around
              <br />
              how you learn<span>.</span>
            </h2>
            <WelcomeCharacter showCue />
            <div className="auth-live-pass">
              <div className="auth-live-pass-top">
                <span>YOUR SPACE</span>
                <span>
                  {avatar ? (
                    <>
                      <Check size={12} aria-hidden="true" />
                      Your crew, chosen
                    </>
                  ) : name.trim() ? (
                    'Taking shape'
                  ) : (
                    'Made for you'
                  )}
                </span>
              </div>
              <div className="auth-live-pass-person">
                <button
                  type="button"
                  className="auth-live-avatar"
                  data-character-chosen={Boolean(avatar)}
                  disabled={busy}
                  aria-label={
                    avatar
                      ? 'Change your Star Crew character'
                      : 'Choose your Star Crew character'
                  }
                  onClick={() => setPickerOpen(true)}
                >
                  {avatar ? (
                    <Avatar
                      seed={avatar}
                      alt=""
                      className="auth-live-avatar-art"
                    />
                  ) : (
                    <span className="auth-live-crew-waiting" aria-hidden="true">
                      <i />
                      <i />
                      <span>
                        <Plus size={19} />
                      </span>
                    </span>
                  )}
                </button>
                <div>
                  <strong>{name.trim() || 'Your name here'}</strong>
                  <span>
                    <GraduationCap size={14} aria-hidden="true" />
                    {school || 'Your school. Your next step.'}
                  </span>
                </div>
                <ArrowUpRight size={17} aria-hidden="true" />
              </div>
              <div className="auth-live-pass-bottom">
                <span>Personalised study</span>
                <span>Examiner-grounded</span>
              </div>
            </div>
          </aside>
          <div className="auth-live-deck">
            <div className="auth-live-sheet" aria-hidden="true" />
            <div
              className="auth-live-sheet auth-live-sheet-two"
              aria-hidden="true"
            />
            <div className="auth-live-card">
              {view === 'register' && (
                <span
                  className="auth-live-sr"
                  role="status"
                  aria-label={`Account creation, step ${registerStep} of 4`}
                >
                  Step {registerStep} of 4
                </span>
              )}
              {children}
            </div>
          </div>
        </div>
      </section>
      {devButton && <div className="auth-live-footer">{devButton}</div>}
      {pickerOpen && (
        <div className="auth-live-overlay">
          <div
            ref={picker}
            role="dialog"
            aria-modal="true"
            aria-labelledby="auth-crew-title"
            className="auth-live-dialog"
          >
            <button
              type="button"
              className="auth-live-dialog-close"
              aria-label="Close character picker"
              onClick={() => setPickerOpen(false)}
            >
              <X size={19} />
            </button>
            <h2 id="auth-crew-title">Meet your Star Crew.</h2>
            <p>Choose a character to make this space yours.</p>
            <div
              className="auth-live-crew"
              role="group"
              aria-label="Your Star Crew character"
            >
              {PERSONAL_STAR_CREW.map((item) => (
                <button
                  type="button"
                  key={item.id}
                  data-account-sound="save"
                  aria-label={`Choose ${item.name} avatar`}
                  aria-pressed={avatar === item.id}
                  onClick={() => {
                    onAvatarChange(item.id);
                    setPickerOpen(false);
                  }}
                >
                  <Avatar
                    seed={item.id}
                    alt=""
                    className="auth-live-crew-art"
                  />
                  <span>{item.name.replace(/^The /, '')}</span>
                  {avatar === item.id && <Check size={14} aria-hidden="true" />}
                </button>
              ))}
            </div>
            <button
              type="button"
              className="auth-live-quiet"
              onClick={() => setPickerOpen(false)}
            >
              Back to your account <ArrowRight size={15} aria-hidden="true" />
            </button>
          </div>
        </div>
      )}
    </main>
  );
}
