import React, { useEffect, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, ArrowUpRight, Check, Eye, EyeOff, LayoutGrid, RotateCcw, School } from 'lucide-react';

type Direction = 'open' | 'horizon' | 'hours' | 'invitation';
type Stage = 'welcome' | 'login' | 'signup' | 'school' | 'forgot';
const directions: { id: Direction; name: string; note: string; detail: string }[] = [
  { id: 'open', name: 'The open page', note: 'Big type. Open space. A confident first step.', detail: 'The closest evolution of the current screen, with a stronger editorial layout and the character stepping across its baseline.' },
  { id: 'horizon', name: 'Paper horizon', note: 'A little colour. A sense of somewhere to go.', detail: 'Layers of paper lead into the app. Move over the illustration to shift the horizon; opening the form settles the layers into place.' },
  { id: 'hours', name: 'After hours', note: 'A quiet dark room. A bright place to begin.', detail: 'An ink-dark introduction alongside a crisp white entrance, carrying the mood of the after-hours study room into sign-in.' },
  { id: 'invitation', name: 'The invitation', note: 'A personal note, with a little paper personality.', detail: 'An oversized invitation with an illustrated stamp, a folded corner and clear ways in. The card straightens as you start.' },
];

const Guy = ({ className = '' }: { className?: string }) => <img className={`entry-guy ${className}`} src="/assets/landing/starguy-512.png" alt="The Nextstepuni character standing on an orange star" draggable={false} />;
const Wordmark = () => <span className="entry-wordmark">nextstepuni</span>;
const GoogleMark = () => <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
  <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z" fill="#4285F4" />
  <path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z" fill="#34A853" />
  <path d="M3.964 10.71c-.18-.54-.282-1.117-.282-1.71 0-.593.102-1.17.282-1.71V4.958H.957C.347 6.173 0 7.548 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z" fill="#FBBC05" />
  <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z" fill="#EA4335" />
</svg>;

function Entrance({ stage, setStage, notify }: { stage: Stage; setStage: (s: Stage) => void; notify: (s: string) => void }) {
  const [showPassword, setShowPassword] = useState(false);
  const titles: Record<Stage, string> = { welcome: 'Your study,\nyour way.', login: 'Good to have\nyou back.', signup: 'A good place\nto begin.', school: 'Your school\nspace.', forgot: 'Let’s get you\nback in.' };
  const subtitles: Record<Stage, string> = { welcome: 'Your subjects. Your ambitions. A little room to grow.', login: 'Pick up where you left off.', signup: 'Make a little room for what comes next.', school: 'For counsellors, teachers and school staff.', forgot: 'Enter your email to reset your password.' };
  const submit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    notify(stage === 'forgot' ? 'Preview: the password-reset email would be sent here.' : stage === 'signup' ? 'Preview: this would continue into your account setup.' : 'Preview: this would open your home screen.');
  };
  return <div className={`entrance entrance-${stage}`} key={stage}>
    {stage !== 'welcome' && <button className="entry-back" onClick={() => setStage(stage === 'forgot' ? 'login' : 'welcome')}><ArrowLeft size={15} /> Back</button>}
    <p className="entry-eyebrow">{stage === 'welcome' ? 'A little something for your future' : stage === 'signup' ? 'Start your next chapter' : stage === 'school' ? 'School sign-in' : 'Welcome back'}</p>
    <h2>{titles[stage].split('\n').map((line, i) => <React.Fragment key={line}>{i > 0 && <br />}{line}</React.Fragment>)}</h2>
    <p className="entrance-subtitle">{subtitles[stage]}</p>
    {stage === 'welcome' ? <div className="entry-welcome-actions">
      <button className="entry-primary" onClick={() => setStage('signup')}>Create your account <ArrowUpRight size={20} /></button>
      <button className="entry-secondary" onClick={() => setStage('login')}>Log in <ArrowRight size={19} /></button>
      <div className="entry-or"><span />or<span /></div>
      <button className="entry-google" onClick={() => notify('Preview: Google sign-in would open here.')}><GoogleMark /> Continue with Google</button>
    </div> : <form onSubmit={submit} className="entry-form" autoComplete="off">
      {stage === 'signup' && <label>Your name<input name="preview-name" placeholder="First name" required autoComplete="off" /></label>}
      <label>Email address<input name="preview-email" type="email" placeholder={stage === 'school' ? 'you@school.ie' : 'you@example.com'} required autoComplete="off" /></label>
      {stage !== 'forgot' && <label>Password<div className="entry-password"><input name="preview-password" type={showPassword ? 'text' : 'password'} placeholder="Your password" required minLength={8} autoComplete="new-password" /><button type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={() => setShowPassword(s => !s)}>{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button></div></label>}
      {stage === 'login' && <button type="button" className="entry-forgot" onClick={() => setStage('forgot')}>Forgot your password?</button>}
      <button className="entry-primary" type="submit">{stage === 'signup' ? 'Create your account' : stage === 'forgot' ? 'Send reset link' : 'Log in'}<ArrowRight size={20} /></button>
      {stage === 'login' && <><div className="entry-or"><span />or<span /></div><button className="entry-google" type="button" onClick={() => notify('Preview: Google sign-in would open here.')}><GoogleMark /> Continue with Google</button></>}
      {stage === 'signup' && <p className="entry-terms">By continuing, you agree to our Terms and Privacy Policy.</p>}
    </form>}
    {stage === 'welcome' && <button className="entry-school" onClick={() => setStage('school')}><School size={16} /> School sign-in <span>for counsellors & staff</span><ArrowUpRight size={14} /></button>}
    {stage === 'login' && <p className="entry-switch">New here? <button onClick={() => setStage('signup')}>Create your account</button></p>}
    {stage === 'signup' && <p className="entry-switch">Already have an account? <button onClick={() => setStage('login')}>Log in</button></p>}
  </div>;
}

function Concept({ direction, stage, setStage, notify }: { direction: Direction; stage: Stage; setStage: (s: Stage) => void; notify: (s: string) => void }) {
  const surface = useRef<HTMLDivElement>(null);
  const progress = stage !== 'welcome';
  const entrance = <Entrance stage={stage} setStage={setStage} notify={notify} />;
  const move = (event: React.PointerEvent<HTMLDivElement>) => {
    if (event.pointerType !== 'mouse' || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const bounds = event.currentTarget.getBoundingClientRect();
    surface.current?.style.setProperty('--drift', `${(event.clientX - bounds.left - bounds.width / 2) / bounds.width * 12}px`);
  };
  return <div ref={surface} className={`auth-concept concept-${direction}${progress ? ' is-entering' : ''}`} onPointerMove={move} onPointerLeave={() => surface.current?.style.setProperty('--drift', '0px')}>
    {direction === 'open' && <>
      <header className="concept-header"><Wordmark /><button onClick={() => notify('Preview: return to the landing page.')} className="entry-landing">A look around first <ArrowUpRight size={16} /></button></header>
      <div className="open-layout">
        <section className="open-story"><p className="entry-eyebrow">For the next bit of your life</p><h1>Small steps.<br /><em>Big things.</em></h1><div className="open-illustration"><span className="open-baseline" /><Guy /><span className="small-note">One good place to start.</span></div><p className="story-caption">A little focus today.<br />A little more possibility tomorrow.</p></section>
        <section className="open-entrance">{entrance}</section>
      </div>
      <footer className="concept-footer"><span>Made for the way you learn.</span><span>Made in Ireland.</span></footer>
    </>}
    {direction === 'horizon' && <>
      <header className="concept-header"><Wordmark /><span className="entry-eyebrow">Your next chapter starts here</span></header>
      <div className="horizon-layout"><section className="horizon-story"><div className="horizon-heading"><p className="entry-eyebrow">A little room to grow</p><h1>A world of<br /><em>your own.</em></h1><p>Your effort goes somewhere.<br />Let’s see where it takes you.</p></div><div className="paper-landscape" aria-hidden="true"><i /><i /><i /><i /></div><div className="horizon-character"><Guy /><span>Every little step counts.</span></div></section><section className="horizon-entrance">{entrance}<span className="paper-tab" aria-hidden="true" /></section></div>
      <footer className="concept-footer"><span>Study. Explore. Find your feet.</span><button onClick={() => notify('Preview: return to the landing page.')} className="entry-landing">A look around first <ArrowUpRight size={16} /></button></footer>
    </>}
    {direction === 'hours' && <>
      <section className="hours-story"><header><Wordmark /><span className="entry-eyebrow">After hours. Before everything.</span></header><div className="hours-heading"><p className="entry-eyebrow">A little focus goes a long way</p><h1>The next bit<br /><em>is yours.</em></h1></div><div className="hours-illustration"><div className="hours-disc" aria-hidden="true" /><Guy /><span className="hours-line" aria-hidden="true" /></div><footer><p>Make some space for your future.<br />We’ll help with the next step.</p><span className="hours-coordinate">Here, you begin. ↗</span></footer></section>
      <section className="hours-entrance"><button onClick={() => notify('Preview: return to the landing page.')} className="entry-landing">A look around first <ArrowUpRight size={16} /></button>{entrance}<span className="hours-foot">Your subjects. Your pace. Your possibilities.</span></section>
    </>}
    {direction === 'invitation' && <>
      <header className="concept-header"><Wordmark /><button onClick={() => notify('Preview: return to the landing page.')} className="entry-landing">A look around first <ArrowUpRight size={16} /></button></header>
      <div className="invitation-desk"><div className="invitation-underleaf" aria-hidden="true" /><article className="invitation-paper"><div className="invitation-note"><span className="entry-eyebrow">An invitation to begin</span><div className="invitation-stamp"><Guy /><span>ONE SMALL STEP</span></div><h1>The next<br />chapter<br /><em>is yours.</em></h1><p>To the curious.<br />The figuring-it-out.<br />The not-quite-sure-yet.</p><span className="invitation-signoff">There’s a place for you here.</span></div><section className="invitation-entrance">{entrance}</section><span className="invitation-fold" aria-hidden="true" /></article></div>
      <footer className="concept-footer"><span>A little encouragement. A good place to start.</span><span>Nextstepuni · Made in Ireland</span></footer>
    </>}
  </div>;
}

function Miniature({ direction, choose }: { direction: typeof directions[number]; choose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const observer = new ResizeObserver(([entry]) => ref.current?.style.setProperty('--mini-scale', String(entry.contentRect.width / 1200)));
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  return <article className="direction-card" role="button" tabIndex={0} onClick={choose} onKeyDown={event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); choose(); } }} aria-label={`Explore ${direction.name}`}><div ref={ref} className="direction-mini"><div className="direction-mini-page" inert><Concept direction={direction.id} stage="welcome" setStage={() => {}} notify={() => {}} /></div></div><div className="direction-card-caption"><div><h2>{direction.name}</h2><p>{direction.note}</p></div><ArrowUpRight size={23} /></div></article>;
}

export default function SignInDirections() {
  const params = new URLSearchParams(location.search);
  const initial = directions.find(d => d.id === params.get('direction'))?.id ?? 'open';
  const [direction, setDirection] = useState<Direction>(initial);
  const [stage, setStage] = useState<Stage>('welcome');
  const [compare, setCompare] = useState(false);
  const [notice, setNotice] = useState('');
  const current = directions.find(d => d.id === direction)!;
  const select = (id: Direction) => {
    setDirection(id); setStage('welcome'); setCompare(false); setNotice('');
    history.replaceState(null, '', `?direction=${id}`);
  };
  useEffect(() => { if (!notice) return; const timeout = setTimeout(() => setNotice(''), 6500); return () => clearTimeout(timeout); }, [notice]);
  return <main className="entry-review">
    <header className="review-toolbar"><a className="review-label" href="/sign-in-directions.html">Entry <span>/</span> Directions</a><nav aria-label="Sign-in directions">{directions.map((d, i) => <button key={d.id} aria-pressed={!compare && direction === d.id} onClick={() => select(d.id)}><span>0{i + 1}</span>{d.name}</button>)}</nav><button className={`review-compare${compare ? ' active' : ''}`} onClick={() => setCompare(c => !c)} aria-pressed={compare}><LayoutGrid size={16} /><span>Compare all</span></button></header>
    <div className="review-context"><p>{compare ? 'Four ways to say welcome. Choose one to explore.' : current.note}</p><span>Design preview · No account details saved</span></div>
    {compare ? <section className="direction-grid" aria-label="Compare sign-in designs">{directions.map(d => <Miniature key={d.id} direction={d} choose={() => select(d.id)} />)}</section> : <><div className="review-stage" key={direction}><Concept direction={direction} stage={stage} setStage={s => { setStage(s); setNotice(''); }} notify={setNotice} /></div><footer className="review-footer"><p><b>{current.name}</b>{current.detail}</p><div className="review-states" role="group" aria-label="Preview screen"><button aria-pressed={stage === 'welcome'} onClick={() => setStage('welcome')}>Welcome</button><button aria-pressed={stage === 'login'} onClick={() => setStage('login')}>Log in</button><button aria-label="Restart preview" onClick={() => { setStage('welcome'); setNotice(''); }}><RotateCcw size={15} /></button></div></footer></>}
    {notice && <div className="preview-notice" role="status"><Check size={17} />{notice}</div>}
  </main>;
}
