/**
 * Sign up and sign in, rebuilt on Kobra (AFTER for the design review).
 *
 * The account card from components/LoginPage.tsx with the same words, views
 * and validation messages, drawn as one paper card on the white canvas: Kobra
 * Tabs for the account switch, Inputs, outline provider Buttons, a segmented
 * join code, a Select, a Checkbox, RadioGroups, a Popover and a Dialog.
 * Review only: no Firebase, no network, nothing is submitted.
 */

import { useEffect, useId, useRef, useState, type FormEvent, type ReactNode, type Ref } from 'react';
import {
  ArrowLeft, ArrowRight, ArrowUpRight, Check, Eye, EyeOff, GraduationCap, HelpCircle, Volume2, VolumeX,
} from 'lucide-react';
import KobraScope, {
  Button, Checkbox, Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle,
  Input, Popover, PopoverContent, PopoverTrigger, RadioGroup, RadioGroupItem,
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
  Tabs, TabsContent, TabsList, TabsTrigger, setSoundMuted, useSoundMuted,
} from '../../components/approved-ui-runtime';
import StarCrewArtwork from '../../components/StarCrewArtwork';
import { PERSONAL_STAR_CREW, getPersonalStarCrew } from '../../data/personalStarCrew';
import { SCHOOL_IDENTITY } from '../../data/schoolIdentity';
import { SCHOOLS, getSchoolName, type SchoolId } from '../../schoolData';
import { MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, passwordLengthError } from '../../utils/passwordPolicy';
import './sign-in.css';

type View = 'register' | 'login' | 'forgot' | 'school';
type Role = 'gc' | 'staff';

// Copy lifted from components/LoginPage.tsx.
const STEP_TITLES = ['Let’s start with you.', 'Find your people.', 'Keep it yours.', 'Meet your study self.'];
const STEP_DESCRIPTIONS = [
  'Your name, your email. Then we’ll make it yours.',
  'Connect your account to your school.',
  'A password that’s just for you.',
  'Pick the character that feels like you.',
];
const STEP_LABELS = ['Your details', 'Your school', 'Your password', 'Your Star Crew'];
const ROLES: { value: Role; label: string }[] = [
  { value: 'gc', label: 'Guidance counsellor' },
  { value: 'staff', label: 'Staff room' },
];
const USERNAME_RESET_HELP = 'Accounts made with a username can’t get reset emails. Email nextstepuniinfo@gmail.com with your username and school, and we’ll reset it for you.';
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const isUsernameLogin = (value: string) => {
  const v = value.trim().toLowerCase();
  return v.length > 0 && (!v.includes('@') || v.endsWith('@nextstep.app'));
};

/** Review fixture label: this card never signs anyone in. */
const REVIEW_NOTE = 'Review only. Nothing was sent.';
const SCHOOL_ITEMS = SCHOOLS.map(school => ({ value: school.id, label: school.name }));

// Generated join codes are twelve characters, shown as XXXX-XXXX-XXXX
// (functions/src/accessCodes.ts). The server upper-cases them and strips
// everything but letters and digits, so the cells do the same.
const CODE_LENGTH = 12;
const CODE_GROUPS = [0, 4, 8];
const cleanCode = (text: string) => text.toUpperCase().replace(/[^A-Z0-9]/g, '');

const GoogleMark = () => (
  <svg viewBox="0 0 18 18" aria-hidden="true">
    <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z" fill="#4285F4" />
    <path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z" fill="#34A853" />
    <path d="M3.964 10.71c-.18-.54-.282-1.117-.282-1.71 0-.593.102-1.17.282-1.71V4.958H.957C.347 6.173 0 7.548 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z" fill="#FBBC05" />
    <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z" fill="#EA4335" />
  </svg>
);

const AppleMark = () => (
  <svg viewBox="0 0 17 21" aria-hidden="true">
    <path d="M14.07 11.17c-.02-2.18 1.78-3.23 1.86-3.28-1.01-1.48-2.59-1.69-3.15-1.71-1.34-.14-2.61.79-3.29.79-.68 0-1.72-.77-2.83-.75-1.46.02-2.8.85-3.55 2.16-1.51 2.62-.39 6.5 1.09 8.62.72 1.04 1.58 2.21 2.71 2.17 1.09-.04 1.5-.7 2.82-.7 1.31 0 1.69.7 2.83.68 1.17-.02 1.91-1.06 2.62-2.1.83-1.21 1.17-2.38 1.19-2.44-.03-.01-2.28-.88-2.3-3.47zM11.9 4.56c.6-.73 1.01-1.74.9-2.75-.87.04-1.92.58-2.54 1.3-.55.64-1.04 1.67-.91 2.66.97.08 1.96-.49 2.55-1.21z" fill="currentColor" />
  </svg>
);

/** A labelled field with its validation message underneath. */
function Field({ id, label, error, aside, children }: {
  id: string; label: string; error?: string; aside?: ReactNode; children: ReactNode;
}) {
  return (
    <div className="kr-si-field">
      <div className="kr-si-label-row">
        <label htmlFor={id}>{label}</label>
        {aside}
      </div>
      {children}
      {error && <p id={`${id}-error`} className="kr-si-field-error" role="alert">{error}</p>}
    </div>
  );
}

function Heading({ title, lede, headingRef }: { title: string; lede: string; headingRef: Ref<HTMLHeadingElement> }) {
  return (
    <div className="kr-si-heading">
      <h2 ref={headingRef} tabIndex={-1}>{title}</h2>
      <p>{lede}</p>
    </div>
  );
}

/** The live page's "or" rule and its two provider buttons, as outline Buttons. */
function Providers({ disabled, onPress }: { disabled: boolean; onPress: () => void }) {
  return (
    <div className="kr-si-providers">
      <p className="kr-si-divider"><span>or</span></p>
      <Button type="button" variant="outline" className="nsu-ink-outline kr-si-provider" disabled={disabled} onClick={onPress}>
        <GoogleMark />Continue with Google
      </Button>
      <Button type="button" variant="outline" className="nsu-ink-outline kr-si-provider" disabled={disabled} onClick={onPress}>
        <AppleMark />Continue with Apple
      </Button>
    </div>
  );
}

/** Password with a reveal toggle: an icon Button inside the Input's frame. */
function PasswordInput({ id, value, onChange, shown, onToggle, creating, invalid }: {
  id: string; value: string; onChange: (value: string) => void; shown: boolean; onToggle: () => void;
  creating?: boolean; invalid?: boolean;
}) {
  return (
    <div className="kr-si-password">
      <Input
        id={id}
        type={shown ? 'text' : 'password'}
        value={value}
        placeholder={creating ? 'Create a password' : 'Your password'}
        autoComplete={creating ? 'new-password' : 'current-password'}
        autoCapitalize="off"
        autoCorrect="off"
        spellCheck={false}
        minLength={creating ? MIN_PASSWORD_LENGTH : undefined}
        maxLength={creating ? MAX_PASSWORD_LENGTH : undefined}
        aria-invalid={invalid || undefined}
        aria-describedby={[creating && `${id}-rule`, invalid && `${id}-error`].filter(Boolean).join(' ') || undefined}
        onChange={event => onChange(event.target.value)}
      />
      <Button
        type="button"
        variant="ghost"
        size="icon"
        className="kr-si-reveal"
        aria-label={shown ? 'Hide password' : 'Show password'}
        aria-pressed={shown}
        onClick={onToggle}
      >
        {shown ? <EyeOff aria-hidden="true" /> : <Eye aria-hidden="true" />}
      </Button>
    </div>
  );
}

/**
 * The school join code as twelve single-character Kobra Inputs in three groups
 * of four. Typing advances, Backspace steps back, arrows move, and a pasted
 * code (with or without dashes) fills every cell from the one pasted into.
 * The value is kept contiguous, so only the next empty cell can take focus.
 */
function JoinCodeEntry({ id, labelId, value, onChange, invalid }: {
  id: string; labelId: string; value: string; onChange: (value: string) => void; invalid?: boolean;
}) {
  const cells = useRef<Array<HTMLInputElement | null>>([]);
  const chars = Array.from({ length: CODE_LENGTH }, (_, index) => value[index] ?? '');
  const next = Math.min(value.length, CODE_LENGTH - 1);
  const focusCell = (index: number) => {
    const cell = cells.current[Math.max(0, Math.min(CODE_LENGTH - 1, index))];
    cell?.focus();
    cell?.select();
  };
  const write = (index: number, text: string) => {
    const typed = cleanCode(text);
    if (!typed) return;
    const start = Math.min(index, value.length);
    onChange((value.slice(0, start) + typed + value.slice(start + typed.length)).slice(0, CODE_LENGTH));
    focusCell(start + typed.length);
  };
  const cell = (index: number) => (
    <Input
      key={index}
      id={index === 0 ? id : undefined}
      ref={node => { cells.current[index] = node; }}
      className="kr-si-code-cell"
      value={chars[index]}
      tabIndex={index === next ? 0 : -1}
      inputMode="text"
      autoComplete="off"
      autoCapitalize="characters"
      autoCorrect="off"
      spellCheck={false}
      enterKeyHint={index === CODE_LENGTH - 1 ? 'done' : 'next'}
      aria-label={`Character ${index + 1} of ${CODE_LENGTH}`}
      aria-invalid={invalid || undefined}
      data-filled={chars[index] ? true : undefined}
      onMouseDown={event => {
        if (index > value.length) { event.preventDefault(); focusCell(value.length); }
      }}
      onFocus={event => event.currentTarget.select()}
      onPaste={event => { event.preventDefault(); write(index, event.clipboardData.getData('text')); }}
      onChange={event => {
        const raw = event.target.value;
        if (!raw) { onChange(value.slice(0, index) + value.slice(index + 1)); return; }
        write(index, raw.length > 1 && chars[index] ? raw.replace(chars[index], '') : raw);
      }}
      onKeyDown={event => {
        if (event.key === 'Backspace' && !chars[index] && index > 0) {
          event.preventDefault();
          onChange(value.slice(0, index - 1) + value.slice(index));
          focusCell(index - 1);
        } else if (event.key === 'ArrowLeft') { event.preventDefault(); focusCell(index - 1); }
        else if (event.key === 'ArrowRight') { event.preventDefault(); focusCell(Math.min(index + 1, value.length)); }
        else if (event.key === 'Home') { event.preventDefault(); focusCell(0); }
        else if (event.key === 'End') { event.preventDefault(); focusCell(value.length); }
      }}
    />
  );
  return (
    <div
      className="kr-si-code"
      role="group"
      aria-labelledby={labelId}
      aria-describedby={invalid ? `${id}-error` : undefined}
    >
      {CODE_GROUPS.map((start, group) => (
        <div key={start} className="kr-si-code-set">
          {group > 0 && <span className="kr-si-code-dash" aria-hidden="true" />}
          <div className="kr-si-code-cells">{[0, 1, 2, 3].map(offset => cell(start + offset))}</div>
        </div>
      ))}
    </div>
  );
}

export default function SignInAfter() {
  const uid = useId();
  const ids = {
    name: `${uid}-name`, email: `${uid}-email`, school: `${uid}-school`, code: `${uid}-code`, codeLabel: `${uid}-code-label`,
    password: `${uid}-password`, consent: `${uid}-consent`, consentNote: `${uid}-consent-note`, loginEmail: `${uid}-login-email`,
    loginPassword: `${uid}-login-password`, resetEmail: `${uid}-reset-email`, gcSchool: `${uid}-gc-school`, gcPassword: `${uid}-gc-password`,
    help: `${uid}-help`,
  };

  const [view, setView] = useState<View>('register');
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [school, setSchool] = useState<SchoolId | ''>('');
  const [joinCode, setJoinCode] = useState('');
  const [avatar, setAvatar] = useState('');
  const [agreed, setAgreed] = useState(false);
  const [schoolRole, setSchoolRole] = useState<Role>('gc');
  const [gcSchool, setGcSchool] = useState<SchoolId | ''>('');
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [error, setError] = useState('');
  const [busy, setBusy] = useState('');
  const [note, setNote] = useState('');
  const [resetSent, setResetSent] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const [codeHelpOpen, setCodeHelpOpen] = useState(false);
  const [waitingOpen, setWaitingOpen] = useState(false);
  const muted = useSoundMuted();

  // Move focus to the new heading after a step or view change the student asked
  // for (as the live page does), never on first render.
  const heading = useRef<HTMLHeadingElement>(null);
  const focusHeading = useRef(false);
  useEffect(() => {
    if (!focusHeading.current) return;
    focusHeading.current = false;
    heading.current?.focus({ preventScroll: true });
  }, [view, step, resetSent]);

  const timer = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(timer.current), []);
  useEffect(() => {
    if (countdown <= 0) return;
    const tick = window.setTimeout(() => setCountdown(value => value - 1), 1000);
    return () => window.clearTimeout(tick);
  }, [countdown]);

  const clear = () => { setError(''); setFieldErrors({}); setNote(''); };
  const reject = (id: string, message: string) => {
    setError(''); setNote('');
    setFieldErrors({ [id]: message });
    requestAnimationFrame(() => document.getElementById(id)?.focus());
  };
  const invalid = (id: string) => ({
    'aria-invalid': fieldErrors[id] ? true : undefined,
    'aria-describedby': fieldErrors[id] ? `${id}-error` : undefined,
  });
  /** Stands in for the network call: the real busy label, then the review note. */
  const pretend = (label: string, done?: () => void) => {
    clear();
    setBusy(label);
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => { setBusy(''); if (done) done(); else setNote(REVIEW_NOTE); }, 900);
  };
  const go = (next: View, moveFocus = true) => {
    if (busy) return;
    if (view === 'school' || next === 'school') setPassword('');
    setShowPassword(false);
    clear();
    focusHeading.current = moveFocus;
    setView(next);
  };
  const toStep = (next: number) => { clear(); focusHeading.current = true; setStep(next); };

  const submitRegister = (event: FormEvent) => {
    event.preventDefault();
    if (busy) return;
    if (step === 1) {
      if (!name.trim()) return reject(ids.name, 'Enter your name.');
      if (!email.trim()) return reject(ids.email, 'Enter your email address.');
      if (!EMAIL_PATTERN.test(email.trim())) return reject(ids.email, 'Check the email address, for example you@example.com.');
    }
    if (step === 2) {
      if (!school) return reject(ids.school, 'Choose your school.');
      if (!joinCode) return reject(ids.code, 'Enter the join code from your school.');
    }
    if (step === 3) {
      const problem = passwordLengthError(password);
      if (problem) return reject(ids.password, problem);
    }
    if (step < 4) return toStep(step + 1);
    pretend('Creating your account…');
  };
  const submitLogin = (event: FormEvent) => {
    event.preventDefault();
    if (busy) return;
    if (!email.trim()) return reject(ids.loginEmail, 'Enter your email or username.');
    if (!password.trim()) return reject(ids.loginPassword, 'Enter your password.');
    pretend('Signing in…');
  };
  const sendReset = (event?: FormEvent) => {
    event?.preventDefault();
    if (busy || countdown > 0) return;
    if (!email.trim()) return reject(ids.resetEmail, 'Enter your email address.');
    if (isUsernameLogin(email)) return reject(ids.resetEmail, USERNAME_RESET_HELP);
    if (!EMAIL_PATTERN.test(email.trim())) return reject(ids.resetEmail, 'Check the email address, for example you@example.com.');
    pretend('Sending…', () => { focusHeading.current = true; setResetSent(true); setCountdown(90); setNote(REVIEW_NOTE); });
  };
  const submitSchool = (event: FormEvent) => {
    event.preventDefault();
    if (busy) return;
    if (!gcSchool || !password.trim()) { setNote(''); setError('Please select your school and enter your password.'); return; }
    pretend('Signing in…');
  };

  const crew = avatar ? getPersonalStarCrew(avatar) : undefined;
  const schoolName = school ? getSchoolName(school) : '';
  const status = (
    <>
      {error && !busy && <p className="kr-si-error" role="alert">{error}</p>}
      <p className="kr-si-note" role="status">{busy ? '' : note}</p>
    </>
  );

  const emailField = (id: string, signingIn = false) => (
    <Field id={id} label={signingIn ? 'Email or username' : 'Email'} error={fieldErrors[id]}>
      <Input
        id={id}
        {...invalid(id)}
        type={signingIn ? 'text' : 'email'}
        inputMode="email"
        autoComplete={signingIn ? 'username' : 'email'}
        autoCapitalize="off"
        autoCorrect="off"
        spellCheck={false}
        value={email}
        placeholder={signingIn ? 'Email or username' : 'you@example.com'}
        onChange={event => { setEmail(event.target.value); clear(); }}
      />
    </Field>
  );
  const passwordField = (id: string, creating = false) => (
    <Field id={id} label="Password" error={fieldErrors[id]}>
      <PasswordInput
        id={id}
        value={password}
        creating={creating}
        invalid={Boolean(fieldErrors[id])}
        shown={showPassword}
        onToggle={() => setShowPassword(value => !value)}
        onChange={value => { setPassword(value); clear(); }}
      />
      {creating && (
        <p id={`${id}-rule`} className="kr-si-rule" data-valid={password.length >= MIN_PASSWORD_LENGTH || undefined}>
          {password.length >= MIN_PASSWORD_LENGTH && <Check aria-hidden="true" />}
          At least {MIN_PASSWORD_LENGTH} characters. Try a memorable phrase.
        </p>
      )}
    </Field>
  );
  const schoolSelect = (id: string, value: SchoolId | '', onChange: (value: SchoolId | '') => void) => (
    <Select value={value || null} items={SCHOOL_ITEMS} onValueChange={next => onChange((next as SchoolId | null) ?? '')}>
      <SelectTrigger id={id} {...invalid(id)} className="kr-si-select">
        <span className="kr-si-select-text">
          <small>{value ? 'Your school' : 'Find your school'}</small>
          <SelectValue placeholder="Choose a school" />
        </span>
      </SelectTrigger>
      <SelectContent className="kr-si-select-menu" align="start" alignItemWithTrigger={false}>
        {SCHOOLS.map(item => (
          <SelectItem key={item.id} value={item.id}>
            <span className="kr-si-select-item">
              <span>{item.name}</span>
              {SCHOOL_IDENTITY[item.id].fullName !== item.name && <small>{SCHOOL_IDENTITY[item.id].fullName}</small>}
            </span>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
  const primary = (label: string, disabled = false) => (
    <Button type="submit" className="kr-si-primary" disabled={Boolean(busy) || disabled}>
      {busy || label}
      <ArrowRight aria-hidden="true" />
    </Button>
  );
  const back = (onClick: () => void) => (
    <Button type="button" variant="outline" className="nsu-ink-outline kr-si-back" disabled={Boolean(busy)} onClick={onClick}>
      <ArrowLeft aria-hidden="true" />Back
    </Button>
  );

  const register = (
    <form noValidate onSubmit={submitRegister} className="kr-si-view" key={`register-${step}`}>
      <div className="kr-si-steprow">
        <p className="kr-si-eyebrow"><span>{`0${step}`}</span>{STEP_LABELS[step - 1]}</p>
        <span className="kr-si-steps" role="img" aria-label={`Account creation, step ${step} of 4`}>
          {[1, 2, 3, 4].map(n => <i key={n} data-state={n < step ? 'done' : n === step ? 'current' : undefined} />)}
        </span>
      </div>
      <Heading headingRef={heading} title={STEP_TITLES[step - 1]} lede={STEP_DESCRIPTIONS[step - 1]} />
      {step > 1 && (
        <div className="kr-si-carry">
          <span className="kr-si-initial" aria-hidden="true">{name.trim().slice(0, 1).toUpperCase()}</span>
          <span>{name}{step > 2 && schoolName && <small>{schoolName}</small>}</span>
          <Check aria-hidden="true" />
        </div>
      )}
      <fieldset className="kr-si-fields" disabled={Boolean(busy)} aria-label={STEP_LABELS[step - 1]}>
        {step === 1 && (
          <>
            <Field id={ids.name} label="Your Name" error={fieldErrors[ids.name]}>
              <Input
                id={ids.name}
                {...invalid(ids.name)}
                value={name}
                placeholder="First and last name"
                autoComplete="name"
                onChange={event => { setName(event.target.value); clear(); }}
              />
            </Field>
            {emailField(ids.email)}
          </>
        )}
        {step === 2 && (
          <>
            <Field id={ids.school} label="School" error={fieldErrors[ids.school]}>
              {schoolSelect(ids.school, school, value => { setSchool(value); setJoinCode(''); clear(); })}
            </Field>
            <div className="kr-si-field">
              <div className="kr-si-label-row">
                <span id={ids.codeLabel} className="kr-si-label">School join code</span>
                <span className="kr-si-detail">From your school</span>
              </div>
              <JoinCodeEntry
                id={ids.code}
                labelId={ids.codeLabel}
                value={joinCode}
                invalid={Boolean(fieldErrors[ids.code])}
                onChange={value => { setJoinCode(value); clear(); }}
              />
              {fieldErrors[ids.code] && <p id={`${ids.code}-error`} className="kr-si-field-error" role="alert">{fieldErrors[ids.code]}</p>}
              <Popover open={codeHelpOpen} onOpenChange={setCodeHelpOpen}>
                <PopoverTrigger render={<Button type="button" variant="outline" size="sm" className="nsu-ink-outline kr-si-help" />}>
                  <HelpCircle aria-hidden="true" />Where do I find my join code?
                </PopoverTrigger>
                <PopoverContent className="kr-si-popover" align="start" side="bottom" aria-labelledby={ids.help}>
                  <KobraScope className="kr-page">
                    <div className="kr-si-pop">
                      <h3 id={ids.help}>Let’s find your code.</h3>
                      <p>Ask the teacher or guidance counsellor who introduced NextStepUni. They can confirm your school’s join code.</p>
                      <p>Check your school’s welcome message, too. Your entered details will stay here while you check.</p>
                      <Button type="button" className="kr-si-pop-close" onClick={() => setCodeHelpOpen(false)}>Back to your details</Button>
                    </div>
                  </KobraScope>
                </PopoverContent>
              </Popover>
            </div>
          </>
        )}
        {step === 3 && passwordField(ids.password, true)}
        {step === 4 && (
          <>
            <div className="kr-si-field">
              <RadioGroup
                value={avatar}
                onValueChange={value => { setAvatar(String(value)); clear(); }}
                aria-label="Choose your Star Crew character"
                className="kr-si-crew"
              >
                {PERSONAL_STAR_CREW.map(item => (
                  <label key={item.id} className="kr-si-crew-item" data-selected={avatar === item.id || undefined}>
                    <StarCrewArtwork artwork={item} className="kr-si-crew-illustration" loading="eager" fallback={null} />
                    <span className="kr-si-crew-name">{item.name.replace(/^The /, '')}</span>
                    <RadioGroupItem value={item.id} />
                  </label>
                ))}
              </RadioGroup>
              <p className="kr-si-detail kr-si-crew-pick" aria-live="polite">
                {crew ? <><strong>{crew.name}</strong> You can change this any time.</> : 'You can change this any time.'}
              </p>
            </div>
            <div className="kr-si-consent">
              <label className="kr-si-consent-row">
                <Checkbox
                  id={ids.consent}
                  className="kr-si-checkbox"
                  checked={agreed}
                  onCheckedChange={checked => { setAgreed(checked); clear(); }}
                  aria-label="I have read the Privacy Notice and agree to the Terms of Use"
                  aria-describedby={ids.consentNote}
                />
                <span>
                  I have read the{' '}
                  <a href="/privacy" target="_blank" rel="noreferrer">Privacy Notice</a>{' '}
                  and agree to the{' '}
                  <a href="/terms" target="_blank" rel="noreferrer">Terms of Use</a>.
                </span>
              </label>
              <p id={ids.consentNote} className="kr-si-detail">
                By ticking this box, I also confirm that I am aged 16 or over and eligible for my school’s programme. This is not blanket consent to use my information.
              </p>
            </div>
          </>
        )}
      </fieldset>
      {status}
      <div className="kr-si-actions">
        {step > 1 && back(() => toStep(step - 1))}
        {primary(step === 4 ? 'Create my account' : 'Continue', step === 4 && (!avatar || !agreed))}
      </div>
      {step < 4 && <p className="kr-si-key" aria-hidden="true"><kbd>↵</kbd> Press Enter to continue</p>}
      {step === 1 && <Providers disabled={Boolean(busy)} onPress={() => { clear(); setNote(REVIEW_NOTE); }} />}
    </form>
  );

  const login = (
    <form noValidate onSubmit={submitLogin} className="kr-si-view" key="login">
      <Heading headingRef={heading} title="Good to see you." lede="Your space is right where you left it." />
      <fieldset className="kr-si-fields" disabled={Boolean(busy)}>
        {emailField(ids.loginEmail, true)}
        {passwordField(ids.loginPassword)}
        <div className="kr-si-forgot-row">
          <Button type="button" variant="ghost" className="kr-si-quiet" onClick={() => { setResetSent(false); go('forgot'); }}>
            Forgot password?
          </Button>
        </div>
      </fieldset>
      {status}
      <div className="kr-si-actions">{primary('Sign in')}</div>
      <Providers disabled={Boolean(busy)} onPress={() => { clear(); setNote(REVIEW_NOTE); }} />
    </form>
  );

  const forgot = resetSent ? (
    <div className="kr-si-view" key="forgot-sent">
      <Heading
        headingRef={heading}
        title="Check your inbox."
        lede={`We sent a reset link to ${email.trim()}. Only the newest email works, so if you ask again, open the latest one.`}
      />
      <p role="status" className="kr-si-sr">Password reset email sent.</p>
      <div className="kr-si-stack">
        <Button type="button" variant="outline" className="nsu-ink-outline kr-si-wide" onClick={() => { setResetSent(false); setCountdown(0); clear(); }}>
          Change email address
        </Button>
        <Button type="button" variant="outline" size="sm" className="nsu-ink-outline kr-si-help" onClick={() => setWaitingOpen(true)}>
          <HelpCircle aria-hidden="true" />Still waiting?
        </Button>
      </div>
      {status}
      <div className="kr-si-actions">
        {back(() => go('login'))}
        <Button
          type="button"
          className="kr-si-primary"
          disabled={Boolean(busy) || countdown > 0}
          onClick={() => pretend('Sending…', () => { setCountdown(90); setNote(REVIEW_NOTE); })}
        >
          {busy || (countdown > 0 ? `Resend in ${countdown}s` : 'Resend email')}
        </Button>
      </div>
    </div>
  ) : (
    <form noValidate onSubmit={sendReset} className="kr-si-view" key="forgot">
      <Heading headingRef={heading} title="Let’s get you back in." lede="Enter your email and we’ll send you a reset link." />
      <fieldset className="kr-si-fields" disabled={Boolean(busy)}>{emailField(ids.resetEmail)}</fieldset>
      {status}
      <div className="kr-si-actions">
        {back(() => go('login'))}
        {primary('Send Reset Link')}
      </div>
    </form>
  );

  const schoolAccess = (
    <form noValidate onSubmit={submitSchool} className="kr-si-view" key="school">
      <p className="kr-si-eyebrow kr-si-context"><GraduationCap aria-hidden="true" />School access</p>
      <Heading headingRef={heading} title="Hello, school team." lede="Sign in to your school’s shared workspace." />
      <fieldset className="kr-si-fields" disabled={Boolean(busy)}>
        <RadioGroup
          value={schoolRole}
          onValueChange={value => { setSchoolRole(value as Role); setPassword(''); clear(); }}
          aria-label="School role"
          className="kr-si-roles"
        >
          {ROLES.map(role => (
            <label key={role.value} className="kr-si-role" data-selected={schoolRole === role.value || undefined}>
              <RadioGroupItem value={role.value} />
              <span className="kr-si-role-name">{role.label}</span>
            </label>
          ))}
        </RadioGroup>
        <Field id={ids.gcSchool} label="School">
          {schoolSelect(ids.gcSchool, gcSchool, value => { setGcSchool(value); clear(); })}
        </Field>
        {passwordField(ids.gcPassword)}
      </fieldset>
      {status}
      <div className="kr-si-actions">
        {back(() => go('login'))}
        {primary('Sign in')}
      </div>
    </form>
  );

  return (
    <section className="kr-section kr-si">
      <header className="kr-si-bar">
        <span className="kr-si-wordmark">nextstepuni<span>.</span></span>
        <div className="kr-si-bar-actions">
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="nsu-ink-outline"
            aria-label={muted ? 'Turn sounds on' : 'Mute sounds'}
            aria-pressed={!muted}
            onClick={() => setSoundMuted(!muted)}
          >
            {muted ? <VolumeX aria-hidden="true" /> : <Volume2 aria-hidden="true" />}
            <span>Sound {muted ? 'off' : 'on'}</span>
          </Button>
          <Button type="button" variant="outline" size="sm" className="nsu-ink-outline" disabled={Boolean(busy)} onClick={() => go(view === 'school' ? 'login' : 'school')}>
            <GraduationCap aria-hidden="true" />
            {view === 'school' ? 'Student sign-in' : 'For schools'}
            <ArrowUpRight aria-hidden="true" />
          </Button>
        </div>
      </header>

      <div className="kr-si-card nsu-paper-card">
        {view === 'register' || view === 'login' ? (
          <Tabs value={view} onValueChange={value => go(value as View, false)} className="kr-si-tabs">
            <TabsList aria-label="Account options">
              <TabsTrigger value="register" disabled={Boolean(busy)}>Create account</TabsTrigger>
              <TabsTrigger value="login" disabled={Boolean(busy)}>Log in</TabsTrigger>
            </TabsList>
            <TabsContent value="register">{register}</TabsContent>
            <TabsContent value="login">{login}</TabsContent>
          </Tabs>
        ) : view === 'forgot' ? forgot : schoolAccess}
      </div>

      {(view !== 'register' || step < 4) && (
        <nav className="kr-si-legal" aria-label="Legal documents">
          <a href="/privacy" target="_blank" rel="noreferrer">Privacy Notice</a>
          <a href="/terms" target="_blank" rel="noreferrer">Terms of Use</a>
        </nav>
      )}
      <p className="kr-si-review">Review build: nothing typed here leaves this page.</p>

      <Dialog open={waitingOpen} onOpenChange={setWaitingOpen}>
        <DialogContent className="kr-si-dialog">
          <KobraScope className="kr-page">
            <div className="kr-si-dialog-body">
              <DialogHeader>
                <DialogTitle>Still waiting?</DialogTitle>
                <DialogDescription>
                  School email can take a few minutes to arrive. Check your spam or junk folder, then confirm the email address you used for your account.
                </DialogDescription>
              </DialogHeader>
              <p>If you asked more than once, only the newest email works. Earlier links stop working.</p>
              <p>If you signed in with Apple or Google, go back and use the same sign-in option.</p>
              <DialogFooter>
                <Button
                  type="button"
                  variant="outline"
                  className="nsu-ink-outline"
                  onClick={() => { setWaitingOpen(false); setResetSent(false); setCountdown(0); clear(); }}
                >
                  Check email address
                </Button>
                <Button type="button" className="kr-si-primary" onClick={() => setWaitingOpen(false)}>Back to password recovery</Button>
              </DialogFooter>
            </div>
          </KobraScope>
        </DialogContent>
      </Dialog>
    </section>
  );
}
