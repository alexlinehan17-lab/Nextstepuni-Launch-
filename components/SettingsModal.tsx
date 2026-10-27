/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Settings, on Kobra (approved review, 25 Oct 2026): one paper panel in the
 * runtime's Dialog, sections divided by hairline rules, Switch rows for the
 * preferences and outline Button rows for everything that goes somewhere
 * (settings-modal.css). The Light / Dark picker is the one the app already
 * had, kept on purpose (Alex, 25 Oct): two miniatures of the app, an ink
 * border and a check on the chosen one.
 */

import React, { useEffect, useRef, useState, useId } from 'react';
import { X, Check, RefreshCw, LogOut, ChevronRight, Compass, GraduationCap, ArrowRight, ShieldCheck, FileText, Trash2 } from 'lucide-react';
import KobraScope, { Button, Dialog, DialogContent, DialogHeader, DialogTitle, Switch } from './approved-ui-runtime';
import { useStudyNotifications } from '../hooks/useStudyNotifications';
import { LegalModal, type LegalDoc } from './legal/LegalModal';
import { DataRightsModal } from './account/DataRightsModal';
import { AVATAR_SEEDS, nextYearAction, yearGroupLabel, yearGroupToCurriculumLevel } from '../utils/authUtils';
import { getAvatarName, getPersonalStarCrew } from '../data/personalStarCrew';
import { type YearGroup } from './subjectData';
import CrewIllustration from './CrewIllustration';
import './settings-modal.css';

import { type UserSettings } from '../types';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  userName?: string;
  userSchool?: string;
  hasStudyProfile?: boolean;
  hasNorthStar?: boolean;
  onStartProfileSetup?: () => void;
  /** Phase 8: current year group, used by the School Year section to
   *  render the "I'm now in X" forward-progression button. */
  userYearGroup?: YearGroup;
  onChangeSubjects?: () => void;
  onResetNorthStar?: () => void;
  /** Phase 8: opens the year transition flow (quiet bump confirm /
   *  TY-vs-5th picker / graduation confirm depending on current year). */
  onAdvanceYear?: () => void;
  onLogout?: () => void;
}

/** A row that goes somewhere: a Kobra outline Button drawn as a hairline row. */
function RowButton({ icon, label, detail, onClick }: {
  icon: React.ReactNode; label: string; detail?: string; onClick: () => void;
}) {
  return (
    <Button variant="outline" className="st-row-button" onClick={onClick}>
      <span className="st-row-icon" aria-hidden="true">{icon}</span>
      <span className="st-row-text">
        <span className="st-label">{label}</span>
        {detail && <> <span className="st-detail">{detail}</span></>}
      </span>
      <ChevronRight aria-hidden="true" className="st-chevron" />
    </Button>
  );
}

const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen, onClose, settings, updateSetting,
  userName, userSchool, userYearGroup, hasStudyProfile = true, hasNorthStar = true,
  onStartProfileSetup, onChangeSubjects, onResetNorthStar, onAdvanceYear, onLogout,
}) => {
  // Junior Cycle always runs in Essentials Mode (simpler, shorter modules) — the
  // toggle is shown as locked-on rather than editable. See useEssentialsMode.
  const isJunior = userYearGroup ? yearGroupToCurriculumLevel(userYearGroup) === 'junior' : false;
  const [showSaved, setShowSaved] = useState(false);
  const [legalDoc, setLegalDoc] = useState<LegalDoc | null>(null);
  const [dataRightsOpen, setDataRightsOpen] = useState(false);
  const flashTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const notify = useStudyNotifications();
  const id = useId();

  useEffect(() => {
    return () => {
      if (flashTimerRef.current) clearTimeout(flashTimerRef.current);
    };
  }, []);

  const flash = () => {
    setShowSaved(true);
    flashTimerRef.current = setTimeout(() => setShowSaved(false), 1200);
  };

  const schoolLabel = userSchool
    ? userSchool
        .replace(/[_-]+/g, ' ')
        .replace(/\b\w/g, character => character.toUpperCase())
    : '';

  // The legal reader and the delete-account flow open above this dialog and
  // own Escape and their backdrop while they are up. The Kobra Dialog hears
  // that Escape first, so it stands aside and lets the key reach them.
  const nestedOpen = legalDoc !== null || dataRightsOpen;

  return (
    <>
    <Dialog
      open={isOpen}
      onOpenChange={(open, details) => {
        if (open) return;
        if (nestedOpen) { details.cancel(); details.allowPropagation(); return; }
        onClose();
      }}
    >
      <DialogContent size="sm" showCloseButton={false} className="nsu-settings nsu-paper-card">
        {/* The dialog portals out of any page scope, so it carries its own. */}
        <KobraScope className="st-scope">
          <DialogHeader className="st-head">
            <DialogTitle id="settings-dialog-title" className="st-title">Settings</DialogTitle>
            <div className="st-head-end">
              <p className="st-saved" role="status" aria-live="polite">
                {showSaved && <span><Check aria-hidden="true" />Saved!</span>}
              </p>
              <Button variant="outline" size="icon" className="st-close" aria-label="Close" onClick={onClose}>
                <X aria-hidden="true" />
              </Button>
            </div>
          </DialogHeader>

          <div className="st-body">
            {/* Account */}
            {(userName || userSchool) && (
              <section className="st-group">
                <h3 className="st-eyebrow">Account</h3>
                <div className="st-identity">
                  {getPersonalStarCrew(settings.avatar) && <CrewIllustration character={settings.avatar} className="st-identity-art" />}
                  <div className="st-row-text">
                    {userName && <p className="st-label">{userName}</p>}
                    {userSchool && <p className="st-detail">School · {schoolLabel}</p>}
                  </div>
                </div>
              </section>
            )}

            {(!hasStudyProfile || !userYearGroup) && onStartProfileSetup && (
              <section className="st-group">
                <div className="st-prompt">
                  <p className="st-kicker">Personalise your app</p>
                  <h3 className="st-prompt-title">Finish your study profile.</h3>
                  <p className="st-prompt-copy">Add your year and subjects to unlock tailored sessions, recommendations and exam tools.</p>
                  <Button className="st-primary" onClick={() => { onClose(); onStartProfileSetup(); }}>
                    Set up my profile
                    <ArrowRight aria-hidden="true" />
                  </Button>
                </div>
              </section>
            )}

            {/* Avatar: eight hairline tiles, an ink ring and a filled marker on
                the chosen one. They stay pressable buttons (journeyWelcome test). */}
            <section className="st-group">
              <h3 id={`${id}-crew`} className="st-eyebrow">Your Star Crew character</h3>
              <div className="st-crew" role="group" aria-labelledby={`${id}-crew`}>
                {AVATAR_SEEDS.map(seed => (
                  <button
                    key={seed}
                    type="button"
                    aria-label={`Select ${getAvatarName(seed)} avatar`}
                    aria-pressed={settings.avatar === seed}
                    title={getAvatarName(seed)}
                    onClick={() => {
                      updateSetting('avatar', seed);
                      flash();
                    }}
                    className="st-crew-option"
                  >
                    <span className="st-crew-mark" aria-hidden="true" />
                    <CrewIllustration character={seed} className="st-crew-art" />
                    <span className="st-crew-name">{getAvatarName(seed).replace(/^The /, '')}</span>
                  </button>
                ))}
              </div>
            </section>

            {/* Preferences */}
            <section className="st-group">
              <h3 className="st-eyebrow">Preferences</h3>
              <div className="st-rows">
                {/* Appearance — two miniatures of the app itself, pick one.
                    A preview says what a "Dark Mode" label can't. */}
                <div role="group" aria-label="Appearance" className="st-theme">
                  {[{ dark: false, label: 'Light' }, { dark: true, label: 'Dark (Beta)' }].map(opt => {
                    const active = settings.darkMode === opt.dark;
                    return (
                      <button
                        key={opt.label}
                        type="button"
                        aria-pressed={active}
                        onClick={() => {
                          if (!active) { updateSetting('darkMode', opt.dark); flash(); }
                        }}
                        className="st-theme-option"
                      >
                        <span className="st-theme-preview" data-dark={opt.dark || undefined} aria-hidden="true">
                          <span className="st-theme-rail" />
                          <span className="st-theme-lines"><i /><i /><i /><i /></span>
                        </span>
                        <span className="st-theme-name">
                          {opt.label}
                          {active && <Check size={13} strokeWidth={2.6} aria-hidden="true" />}
                        </span>
                      </button>
                    );
                  })}
                </div>

                {/* Essentials mode toggle. Junior Cycle is always on (locked);
                    senior students can toggle it. */}
                <label className="st-row st-switch-row" data-locked={isJunior || undefined}>
                  <span className="st-row-text">
                    <span className="st-label">Essentials Mode</span>
                    <span id={`${id}-essentials`} className="st-detail">
                      {isJunior ? 'Always on for Junior Cycle — shorter modules with simpler language' : 'Shorter modules with simpler language'}
                    </span>
                  </span>
                  <Switch
                    checked={isJunior || settings.essentialsMode}
                    aria-label={isJunior ? 'Essentials Mode is always on for Junior Cycle' : 'Use Essentials Mode'}
                    aria-describedby={`${id}-essentials`}
                    disabled={isJunior}
                    onCheckedChange={() => {
                      if (isJunior) return;
                      updateSetting('essentialsMode', !settings.essentialsMode);
                      flash();
                    }}
                  />
                </label>

                {/* Study timer notification. Hidden where this device cannot
                    show one (iPhone and iPad Safari tabs). */}
                {notify.available && (
                  <div>
                    <label className="st-row st-switch-row">
                      <span className="st-row-text">
                        <span className="st-label">Study timer notifications</span>
                        <span id={`${id}-notify`} className="st-detail">One notification when your study time is up</span>
                      </span>
                      <Switch
                        checked={notify.enabled}
                        aria-label="Notify me when my study time is up"
                        aria-describedby={`${id}-notify`}
                        onCheckedChange={() => {
                          if (notify.enabled) { notify.turnOff(); flash(); }
                          else void notify.turnOn().then(permission => { if (permission === 'granted') flash(); });
                        }}
                      />
                    </label>
                    {notify.blocked && (
                      <p role="status" className="st-hint">{notify.hint}</p>
                    )}
                  </div>
                )}
              </div>
            </section>

            {/* School Year (Phase 8) — forward-progression action.
                Renders for any logged-in student. If userYearGroup is
                unknown (legacy account, pre-Phase-8), we still surface
                the section with an empty-state CTA so the flow is
                discoverable instead of silently hidden. */}
            {onAdvanceYear && (() => {
              const action = userYearGroup ? nextYearAction(userYearGroup) : null;
              const isGraduated = userYearGroup === 'graduated';
              return (
                <section className="st-group">
                  <h3 className="st-eyebrow">School Year</h3>
                  <div className="st-row st-year">
                    <span className="st-year-text">
                      <GraduationCap aria-hidden="true" />
                      <span className="st-label">
                        {!userYearGroup
                          ? "We don't have your school year on file."
                          : isGraduated
                            ? "You've completed your Leaving Cert."
                            : `You're in ${yearGroupLabel(userYearGroup)}.`}
                      </span>
                    </span>
                    {!action && onStartProfileSetup ? (
                      <Button variant="outline" className="nsu-ink-outline st-action" onClick={() => { onClose(); onStartProfileSetup(); }}>
                        Add my school year
                      </Button>
                    ) : !action || action.kind === 'terminal' ? (
                      <p className="st-terminal">
                        {action?.label ?? 'Set your school year so we can tune content to where you are.'}
                      </p>
                    ) : (
                      <Button variant="outline" className="nsu-ink-outline st-action" onClick={() => { onClose(); onAdvanceYear(); }}>
                        {action.label}
                        <ArrowRight aria-hidden="true" />
                      </Button>
                    )}
                  </div>
                </section>
              );
            })()}

            {/* Legal — Privacy Notice + Terms (audit 2026-06-01, B4) */}
            <section className="st-group">
              <h3 className="st-eyebrow">Legal</h3>
              {/* Non-affiliation disclaimer, shown without opening a document.
                  Google Play's Misleading Claims policy requires any app
                  carrying government information to state plainly that it does
                  not represent the government entity, and to be easy to see —
                  the full source list lives in Terms of Use. */}
              <p className="st-note">
                NextStepUni is an independent study app. It is not affiliated with or
                endorsed by the State Examinations Commission, the Department of Education,
                the CAO, SUSI, or any other government body. See{' '}
                <Button variant="link" className="st-inline-link" onClick={() => setLegalDoc('terms')}>
                  Terms of Use
                </Button>{' '}
                for the official sources we draw on.
              </p>
              <div className="st-rows">
                <RowButton icon={<ShieldCheck />} label="Privacy Notice" onClick={() => setLegalDoc('privacy')} />
                <RowButton icon={<FileText />} label="Terms of Use" onClick={() => setLegalDoc('terms')} />
              </div>
            </section>

            {/* Account — its own section on purpose.
                App Review rejected 1.0 (1) under Guideline 5.1.1(v) saying the
                app had no way to delete an account. It did: this button, then
                "Delete my account". But it was labelled "Download or delete my
                data", sat third in the LEGAL list under Privacy Notice and
                Terms, and wore a database icon — so it read as a GDPR export
                control and a reviewer scanning for the words "Delete Account"
                went straight past it. The feature was never the problem; the
                wording was. Keep "Delete Account" in this label. */}
            <section className="st-group">
              <h3 className="st-eyebrow">Account</h3>
              <RowButton
                icon={<Trash2 />}
                label="Delete Account"
                detail="Permanently erase your account, or download your data first."
                onClick={() => setDataRightsOpen(true)}
              />
            </section>

            <section className="st-group">
              <h3 className="st-eyebrow">Actions</h3>
              {(onChangeSubjects || onResetNorthStar) && (
                <div className="st-rows">
                  {onChangeSubjects && (
                    <RowButton icon={<RefreshCw />} label="Change Subjects" onClick={() => { onClose(); onChangeSubjects(); }} />
                  )}
                  {onResetNorthStar && (
                    <RowButton icon={<Compass />} label={hasNorthStar ? 'Edit North Star' : 'Set North Star'} onClick={() => { onClose(); onResetNorthStar(); }} />
                  )}
                </div>
              )}
              {onLogout && (
                <Button variant="ghost" className="st-quiet" onClick={() => { onClose(); onLogout(); }}>
                  <LogOut aria-hidden="true" />
                  Sign Out
                </Button>
              )}
            </section>
          </div>
        </KobraScope>
      </DialogContent>
    </Dialog>
    <LegalModal doc={legalDoc} onClose={() => setLegalDoc(null)} onDocumentChange={setLegalDoc} />
    <DataRightsModal
      open={dataRightsOpen}
      onClose={() => setDataRightsOpen(false)}
      onAccountDeleted={() => { setDataRightsOpen(false); onClose(); onLogout?.(); }}
    />
    </>
  );
};

export default SettingsModal;
