/**
 * Settings, rebuilt on Kobra (AFTER for the design review).
 *
 * The same sections, order and copy as components/SettingsModal.tsx, drawn as
 * one paper card: hairline section rules, Kobra RadioGroup / Tabs / Switch /
 * Button, and a real Kobra Dialog showing the same panel in its modal form.
 * Every value is local review state; nothing touches an account or the page
 * theme.
 */

import { useEffect, useId, useRef, useState, type ReactNode } from 'react';
import {
  AppWindow, ArrowRight, Check, ChevronRight, Compass, FileText, GraduationCap, LogOut, RefreshCw, ShieldCheck, Trash2,
} from 'lucide-react';
import KobraScope, {
  Button, Dialog, DialogContent, DialogHeader, DialogTitle, RadioGroup, RadioGroupItem, Switch, Tabs, TabsList, TabsTrigger,
} from '../../components/approved-ui-runtime';
import CrewIllustration from '../../components/CrewIllustration';
import { PERSONAL_STAR_CREW } from '../../data/personalStarCrew';
import { nextYearAction, yearGroupLabel } from '../../utils/authUtils';
import type { YearGroup } from '../../components/subjectData';
import './settings.css';

/** Four of the Star Crew, as the brief asks; the real picker lists them all. */
const CREW = PERSONAL_STAR_CREW.slice(0, 4);

interface SettingsState {
  avatar: string;
  darkMode: boolean;
  essentialsMode: boolean;
  notifications: boolean;
  year: YearGroup;
}

type Change = (patch: Partial<SettingsState>, flash?: boolean) => void;

/** A row that goes somewhere: a Kobra outline Button shaped as a hairline row. */
function RowButton({ icon, label, detail }: { icon: ReactNode; label: string; detail?: string }) {
  return (
    <Button variant="outline" className="kr-st-rowbtn">
      <span className="kr-st-rowbtn-icon" aria-hidden="true">{icon}</span>
      <span className="kr-st-row-text">
        <span className="kr-st-label">{label}</span>
        {detail && <span className="kr-st-detail">{detail}</span>}
      </span>
      <ChevronRight aria-hidden="true" className="kr-st-chevron" />
    </Button>
  );
}

/** A preference row: the whole hairline row is the switch's label. */
function SwitchRow({ id, label, detail, ariaLabel, checked, onCheckedChange }: {
  id: string; label: string; detail: string; ariaLabel: string; checked: boolean; onCheckedChange: (checked: boolean) => void;
}) {
  return (
    <label className="kr-st-row kr-st-switch-row">
      <span className="kr-st-row-text">
        <span className="kr-st-label">{label}</span>
        <span id={`${id}-detail`} className="kr-st-detail">{detail}</span>
      </span>
      <Switch checked={checked} onCheckedChange={onCheckedChange} aria-label={ariaLabel} aria-describedby={`${id}-detail`} />
    </label>
  );
}

function SettingsPanel({ state, onChange, saved, inDialog = false }: {
  state: SettingsState; onChange: Change; saved: boolean; inDialog?: boolean;
}) {
  const id = useId();
  const action = nextYearAction(state.year);
  const isGraduated = state.year === 'graduated';
  const advanceYear = () => {
    if (action.kind === 'bump') onChange({ year: action.next }, false);
    else if (action.kind === 'graduate') onChange({ year: 'graduated' }, false);
  };

  const savedNote = (
    <p className="kr-st-saved" role="status" aria-live="polite">
      {saved && <><Check aria-hidden="true" />Saved!</>}
    </p>
  );

  return (
    <div className="kr-st-panel">
      {inDialog ? (
        <DialogHeader className="kr-st-head">
          <DialogTitle className="kr-st-title">Settings</DialogTitle>
          {savedNote}
        </DialogHeader>
      ) : (
        <header className="kr-st-head">
          <h2 className="kr-st-title">Settings</h2>
          {savedNote}
        </header>
      )}

      <section className="kr-st-group" aria-labelledby={`${id}-account`}>
        <h3 id={`${id}-account`} className="kr-st-eyebrow">Account</h3>
        <div className="kr-st-identity">
          <CrewIllustration character={state.avatar} className="kr-st-identity-art" />
          <span className="kr-st-row-text">
            <span className="kr-st-label">Demo Student</span>
            <span className="kr-st-detail">School · Demo School</span>
          </span>
        </div>
      </section>

      <section className="kr-st-group" aria-labelledby={`${id}-crew`}>
        <h3 id={`${id}-crew`} className="kr-st-eyebrow">Your Star Crew character</h3>
        <RadioGroup
          value={state.avatar}
          onValueChange={value => onChange({ avatar: String(value) })}
          aria-labelledby={`${id}-crew`}
          className="kr-st-crew"
        >
          {CREW.map(crew => (
            <label key={crew.id} className="kr-st-crew-option" data-selected={state.avatar === crew.id}>
              <CrewIllustration character={crew.id} className="kr-st-crew-art" />
              <span className="kr-st-crew-name">{crew.name.replace(/^The /, '')}</span>
              <RadioGroupItem value={crew.id} aria-label={crew.name} />
            </label>
          ))}
        </RadioGroup>
      </section>

      <section className="kr-st-group" aria-labelledby={`${id}-prefs`}>
        <h3 id={`${id}-prefs`} className="kr-st-eyebrow">Preferences</h3>
        <div className="kr-st-rows">
          <div className="kr-st-row kr-st-appearance">
            <span id={`${id}-appearance`} className="kr-st-label">Appearance</span>
            <Tabs value={state.darkMode ? 'dark' : 'light'} onValueChange={value => onChange({ darkMode: value === 'dark' })}>
              <TabsList aria-labelledby={`${id}-appearance`}>
                <TabsTrigger value="light">Light</TabsTrigger>
                <TabsTrigger value="dark">Dark (Beta)</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
          <SwitchRow
            id={`${id}-essentials`}
            label="Essentials Mode"
            detail="Shorter modules with simpler language"
            ariaLabel="Use Essentials Mode"
            checked={state.essentialsMode}
            onCheckedChange={checked => onChange({ essentialsMode: checked })}
          />
          <SwitchRow
            id={`${id}-notify`}
            label="Study timer notifications"
            detail="One notification when your study time is up"
            ariaLabel="Notify me when my study time is up"
            checked={state.notifications}
            onCheckedChange={checked => onChange({ notifications: checked })}
          />
        </div>
      </section>

      <section className="kr-st-group" aria-labelledby={`${id}-year`}>
        <h3 id={`${id}-year`} className="kr-st-eyebrow">School Year</h3>
        <div className="kr-st-row kr-st-year">
          <span className="kr-st-year-text">
            <GraduationCap aria-hidden="true" />
            <span className="kr-st-label">
              {isGraduated ? "You've completed your Leaving Cert." : `You're in ${yearGroupLabel(state.year)}.`}
            </span>
          </span>
          {action.kind === 'terminal' ? (
            <p className="kr-st-terminal">{action.label}</p>
          ) : (
            <Button variant="outline" className="nsu-ink-outline kr-st-action" onClick={advanceYear}>
              {action.label}<ArrowRight aria-hidden="true" />
            </Button>
          )}
        </div>
      </section>

      <section className="kr-st-group" aria-labelledby={`${id}-legal`}>
        <h3 id={`${id}-legal`} className="kr-st-eyebrow">Legal</h3>
        <p className="kr-st-note">
          NextStepUni is an independent study app. It is not affiliated with or
          endorsed by the State Examinations Commission, the Department of Education,
          the CAO, SUSI, or any other government body. See{' '}
          <Button variant="link" className="kr-st-inline-link">Terms of Use</Button>{' '}
          for the official sources we draw on.
        </p>
        <div className="kr-st-rows">
          <RowButton icon={<ShieldCheck />} label="Privacy Notice" />
          <RowButton icon={<FileText />} label="Terms of Use" />
        </div>
      </section>

      {/* Keep "Delete Account" in this label (App Review, Guideline 5.1.1(v)). */}
      <section className="kr-st-group" aria-labelledby={`${id}-erase`}>
        <h3 id={`${id}-erase`} className="kr-st-eyebrow">Account</h3>
        <RowButton
          icon={<Trash2 />}
          label="Delete Account"
          detail="Permanently erase your account, or download your data first."
        />
      </section>

      <section className="kr-st-group" aria-labelledby={`${id}-actions`}>
        <h3 id={`${id}-actions`} className="kr-st-eyebrow">Actions</h3>
        <div className="kr-st-rows">
          <RowButton icon={<RefreshCw />} label="Change Subjects" />
          <RowButton icon={<Compass />} label="Edit North Star" />
        </div>
        <Button variant="ghost" className="kr-st-quiet">
          <LogOut aria-hidden="true" />Sign Out
        </Button>
      </section>
    </div>
  );
}

export default function SettingsAfter() {
  const [state, setState] = useState<SettingsState>({
    avatar: CREW[0].id,
    darkMode: false,
    essentialsMode: false,
    notifications: true,
    year: '5th',
  });
  const [saved, setSaved] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const flashTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => () => {
    if (flashTimer.current) clearTimeout(flashTimer.current);
  }, []);

  // Same "Saved!" flash as the modal; the year step opens its own flow in the
  // app, so it changes the row without claiming a save.
  const change: Change = (patch, flash = true) => {
    setState(current => ({ ...current, ...patch }));
    if (!flash) return;
    setSaved(true);
    if (flashTimer.current) clearTimeout(flashTimer.current);
    flashTimer.current = setTimeout(() => setSaved(false), 1200);
  };

  return (
    <section className="kr-section kr-st" aria-label="Settings on Kobra">
      <div className="kr-st-toolbar">
        <Button variant="outline" className="nsu-ink-outline kr-st-action" onClick={() => setDialogOpen(true)}>
          Open as a dialog<AppWindow aria-hidden="true" />
        </Button>
      </div>

      <div className="kr-st-card nsu-paper-card">
        <SettingsPanel state={state} onChange={change} saved={saved} />
      </div>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent size="sm" className="kr-st-dialog">
          {/* The dialog portals out of the page scope, so it carries its own. */}
          <KobraScope className="kr-page kr-st-portal">
            <div className="kr-st kr-st-in-dialog">
              <SettingsPanel state={state} onChange={change} saved={saved} inDialog />
            </div>
          </KobraScope>
        </DialogContent>
      </Dialog>
    </section>
  );
}
