/**
 * The email-link pages, rebuilt on Kobra (review section 08).
 *
 * The same three screens and words as the "Now" pane: the verify-email
 * success state (AuthActionPage → AuthActionCard + AuthActionSuccess), the
 * reset form (ResetPasswordPage, ready state, for a sample address) and the
 * forced change after a guidance counsellor resets a password
 * (ChangePasswordModal in AppRouter.tsx). Each is a Kobra Card with Input and
 * Button; a failed submit is the runtime Alert drawn as a hairline row.
 * Password feedback is ink while short and mint once long enough (never
 * orange), and both forms read the rule from utils/passwordPolicy
 * (MIN_PASSWORD_LENGTH / MAX_PASSWORD_LENGTH / passwordLengthError) instead of
 * the forced screen's hard-coded 12 and 128.
 * Everything is local review state; nothing reaches Firebase.
 */
import { useEffect, useId, useRef, useState, type ReactNode } from 'react';
import { Check, Eye, EyeOff } from 'lucide-react';
import { Alert, AlertDescription, Button, Card, CardContent, Input } from '../../components/approved-ui-runtime';
import { MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, passwordLengthError } from '../../utils/passwordPolicy';
import './email-link.css';

const SAMPLE_EMAIL = 'sample.student@example.com';

/** AuthActionCard: the hairline card every email-action screen sits in. */
function ActionCard({ kicker = true, children }: { kicker?: boolean; children: ReactNode }) {
  return (
    <Card className="kr-el-card">
      <CardContent className="kr-el-content">
        {kicker && <p className="kr-el-kicker">NEXTSTEPUNI</p>}
        {children}
      </CardContent>
    </Card>
  );
}

/** AuthActionSuccess: a mint mark, the outcome, and the way to sign in. */
function ActionSuccess({ title, message, onSignIn }: { title: string; message: string; onSignIn?: () => void }) {
  return (
    <div className="kr-el-success">
      <span className="kr-el-done-mark" aria-hidden="true"><Check /></span>
      <h2 className="kr-el-title">{title}</h2>
      <p className="kr-el-body">{message}</p>
      <Button className="kr-el-primary" onClick={onSignIn}>Sign in</Button>
    </div>
  );
}

/** The live length rule: ink while short, mint once it fits. */
function LengthFeedback({ id, value }: { id: string; value: string }) {
  const short = MIN_PASSWORD_LENGTH - value.length;
  if (value.length > 0 && short > 0) {
    return <p id={id} className="kr-el-rule">{short} more character{short !== 1 ? 's' : ''} needed</p>;
  }
  if (value.length >= MIN_PASSWORD_LENGTH && value.length <= MAX_PASSWORD_LENGTH) {
    return <p id={id} className="kr-el-rule" data-valid=""><span className="kr-el-rule-mark" aria-hidden="true"><Check /></span>Looks good</p>;
  }
  return null;
}

/** A password Input with its reveal toggle inside the field's frame. */
function PasswordField({ id, label, value, onChange, placeholder, limits }: {
  id: string; label: string; value: string; onChange: (value: string) => void; placeholder: string; limits?: boolean;
}) {
  const [shown, setShown] = useState(false);
  return (
    <div className="kr-el-field">
      <label htmlFor={id} className="kr-el-label">{label}</label>
      <div className="kr-el-password">
        <Input
          id={id}
          type={shown ? 'text' : 'password'}
          value={value}
          placeholder={placeholder}
          autoComplete="new-password"
          // No autoFocus: the real pages have it, but here it would scroll the review page.
          minLength={limits ? MIN_PASSWORD_LENGTH : undefined}
          maxLength={limits ? MAX_PASSWORD_LENGTH : undefined}
          aria-describedby={value ? `${id}-rule` : undefined}
          onChange={event => onChange(event.target.value)}
        />
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="kr-el-reveal"
          aria-label={shown ? 'Hide password' : 'Show password'}
          aria-pressed={shown}
          onClick={() => setShown(value => !value)}
        >
          {shown ? <EyeOff aria-hidden="true" /> : <Eye aria-hidden="true" />}
        </Button>
      </div>
      <LengthFeedback id={`${id}-rule`} value={value} />
    </div>
  );
}

function useSaving() {
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => () => { if (timer.current) clearTimeout(timer.current); }, []);
  return (then: () => void) => { timer.current = setTimeout(then, 900); };
}

/** ResetPasswordPage, ready state, then its "Password updated" outcome. */
function ResetPassword() {
  const id = useId();
  const [stage, setStage] = useState<'ready' | 'submitting' | 'done'>('ready');
  const [newPassword, setNewPassword] = useState('');
  const [error, setError] = useState('');
  const later = useSaving();

  const submit = () => {
    const validationError = passwordLengthError(newPassword);
    if (validationError) { setError(validationError); return; }
    setStage('submitting');
    setError('');
    later(() => { setNewPassword(''); setStage('done'); });
  };

  if (stage === 'done') {
    // In the app Sign in returns to the sign-in page; here it replays the form.
    return <ActionSuccess title="Password updated" message="You can now sign in with your new password." onSignIn={() => setStage('ready')} />;
  }
  return (
    <div>
      <h2 className="kr-el-title">Set a new password</h2>
      <p className="kr-el-body kr-el-for">For <span>{SAMPLE_EMAIL}</span></p>
      <form onSubmit={event => { event.preventDefault(); submit(); }} className="kr-el-form">
        <PasswordField
          id={`${id}-new`}
          label="New password"
          value={newPassword}
          onChange={value => { setNewPassword(value); setError(''); }}
          placeholder={`At least ${MIN_PASSWORD_LENGTH} characters`}
          limits
        />
        {error && <Alert variant="error" className="kr-el-alert"><AlertDescription>{error}</AlertDescription></Alert>}
        <Button type="submit" className="kr-el-primary" disabled={stage === 'submitting' || passwordLengthError(newPassword) !== null}>
          {stage === 'submitting' ? 'Saving…' : 'Set password'}
        </Button>
      </form>
    </div>
  );
}

/** ChangePasswordModal: the forced change after a guidance counsellor reset. */
function ForcedChange() {
  const id = useId();
  const [newPassword, setNewPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const later = useSaving();

  const handleChangePassword = () => {
    const validationError = passwordLengthError(newPassword);
    if (validationError) { setError(validationError); return; }
    setIsLoading(true); setError('');
    // In the app: the changeOwnPassword callable, then sign out.
    later(() => { setIsLoading(false); setNewPassword(''); });
  };

  return (
    <div>
      <h2 className="kr-el-title">Set a new password</h2>
      <p className="kr-el-body kr-el-lede">Your password was reset by your guidance counsellor. Please choose a new password to continue.</p>
      <div className="kr-el-form">
        <PasswordField
          id={`${id}-new`}
          label="New Password"
          value={newPassword}
          onChange={value => { setNewPassword(value); setError(''); }}
          placeholder="Choose a new password"
        />
        {error && <Alert variant="error" className="kr-el-alert"><AlertDescription>{error}</AlertDescription></Alert>}
        <Button className="kr-el-primary" onClick={handleChangePassword} disabled={isLoading || passwordLengthError(newPassword) !== null}>
          {isLoading ? 'Saving...' : 'Set Password'}
        </Button>
      </div>
    </div>
  );
}

export default function EmailLinkAfter() {
  return (
    <section className="kr-section kr-el" aria-label="Email-link pages on Kobra">
      <div className="kr-el-screen">
        <p className="kr-el-caption">1 · Verify email</p>
        <ActionCard>
          <ActionSuccess title="Email confirmed" message="Thanks. Your email address is confirmed. You can sign in now." />
        </ActionCard>
      </div>
      <div className="kr-el-screen">
        <p className="kr-el-caption">2 · Reset password</p>
        <ActionCard><ResetPassword /></ActionCard>
      </div>
      <div className="kr-el-screen">
        <p className="kr-el-caption">3 · Forced password change</p>
        <ActionCard kicker={false}><ForcedChange /></ActionCard>
      </div>
    </section>
  );
}
