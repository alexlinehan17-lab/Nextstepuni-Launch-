import React, { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import StarCrewArtwork from '../../components/StarCrewArtwork';
import { PERSONAL_STAR_CREW } from '../../data/personalStarCrew';
import { ATHLETE_RANKS, getRankForPoints, getNextRank, getRankProgress } from '../../gamificationConfig';
import './studio.css';

const directions = [
  { id: 'combined', number: '01/02', title: 'Your combination', mood: 'The selected pairing', headline: 'Your character. A little post.', description: 'The Star Crew progress ring and the folded-note notification button, together. A personal marker of progress beside a small paper home for your updates.', level: 'Your chosen Star Crew character sits inside the orange progress ring, with your current rank and the distance to the next one.', notification: 'The folded paper note keeps its ink outline and offset shadow. An orange badge appears when you have unread updates.', note: 'Your picks: the progress ring from direction 01 and the folded note from direction 02.', action: 'Open your notes' },
  { id: 'orbit', number: '01', title: 'Your little orbit', mood: 'Personal & playful', headline: 'Your character. Your momentum.', description: 'Your chosen character sits inside the progress ring. A small envelope becomes the home for school messages and little milestones.', level: 'A ring that fills around your own Star Crew character. The next rank is one click away.', notification: 'A circular envelope with an orange unread count. Opens a clean, illustrated inbox.', note: 'My pick: the strongest family resemblance to the Star Crew, while staying compact.', action: 'Open your post' },
  { id: 'ticket', number: '02', title: 'The paper trail', mood: 'Tactile & collectible', headline: 'A little record of showing up.', description: 'A numbered progress ticket, a perforated edge and a folded paper notification. Something that feels like it belongs in your study notebook.', level: 'Your rank becomes a numbered ticket. A segmented line quietly records the distance to the next one.', notification: 'A folded note with a bold count. It opens into a little stack of updates.', note: 'The most distinctive object: a nice match for the study receipt and achievement stamps.', action: 'Open your notes' },
  { id: 'post', number: '03', title: 'A note for you', mood: 'Warm & conversational', headline: 'A little encouragement, up here.', description: 'A small companion keeps you company along the progress line. Notifications arrive as post, with a paper note peeking out of its pocket.', level: 'The Stargazer sits beside a simple progress line. Your rank, streak and points stay easy to read.', notification: 'A miniature post pocket with a clear label. New notes lift gently when you open it.', note: 'The warmest direction. Especially good if school messages should feel more personal.', action: 'Open your post pocket' },
  { id: 'quiet', number: '04', title: 'Quiet confidence', mood: 'Editorial & understated', headline: 'Just the important little things.', description: 'Strong type, a fine orange line and a simple updates count. Character appears when you open the details, keeping the everyday header very light.', level: 'A short rank label and an orange underline. Extra detail lives in the progress panel.', notification: 'A plain “Updates” control with an ink count. No symbol to decode.', note: 'The calmest option: the page keeps the attention, with personality one click away.', action: 'Open your updates' },
] as const;
type Direction = typeof directions[number];
type Variant = Direction['id'];
type Panel = 'progress' | 'notifications' | null;
const previewParams = new URLSearchParams(location.search);
const phoneReview = previewParams.get('review') === 'phone';
const initialDirection = directions.find(d => d.id === previewParams.get('direction'))?.id ?? 'combined';
const messages = [
  { id: 'teacher', kind: 'FROM YOUR GUIDANCE COUNSELLOR', time: 'Today', title: 'A little help with what’s next.', body: 'Our college choices session is on Thursday. Bring along one course you’re curious about.', from: 'Your guidance counsellor' },
  { id: 'progress', kind: 'YOUR PROGRESS', time: 'Today', title: 'Eighteen days of showing up.', body: 'Those small study sessions are adding up. Take a moment to see how far you’ve come.', from: 'Nextstepuni' },
  { id: 'school', kind: 'FROM YOUR SCHOOL', time: 'Yesterday', title: 'A date for your notebook.', body: 'The next study workshop is on Friday at 11.00. Your school will share the room details.', from: 'Your school' },
];

function Crew({ id = 'reader', size = 56, className = '' }: { id?: string; size?: number; className?: string }) {
  const artwork = PERSONAL_STAR_CREW.find(a => a.id === `star-crew:${id}`) ?? PERSONAL_STAR_CREW[1];
  return <StarCrewArtwork artwork={artwork} className={`crew ${className}`} style={{ width: size, height: size }} fallback={<span>n.</span>} />;
}
function Envelope({ pocket = false }: { pocket?: boolean }) {
  return <span className={pocket ? 'post-pocket' : 'envelope'} aria-hidden="true">{pocket && <span className="post-letter"><i /><i /></span>}<span className="envelope-body" /><span className="envelope-fold" /></span>;
}
function Stats({ points }: { points: number }) {
  return <span className="mini-stats"><span><strong>18</strong><small>day streak</small></span><span><strong>{points.toLocaleString('en-IE')}</strong><small>Journey Points</small></span></span>;
}
function Rail({ value }: { value: number }) {
  return <span className="progress-rail" role="progressbar" aria-label="Progress to next rank" aria-valuemin={0} aria-valuemax={100} aria-valuenow={value}><span style={{ width: `${value}%` }} /></span>;
}
function HeaderControls({ variant, earned, balance, unread, avatar, panel = null, onPanel, miniature = false }: { variant: Variant; earned: number; balance: number; unread: number; avatar: string; panel?: Panel; onPanel?: (panel: Panel) => void; miniature?: boolean }) {
  const rank = getRankForPoints(earned), next = getNextRank(rank), progress = getRankProgress(earned, rank, next);
  const rankIndex = ATHLETE_RANKS.findIndex(r => r.id === rank.id) + 1;
  const direction = directions.find(d => d.id === variant)!;
  const toggle = (p: Panel) => onPanel?.(panel === p ? null : p);
  return <div className={`header-controls variant-${variant}${miniature ? ' is-miniature' : ''}`}>
    <button className="rank-control" onClick={() => toggle('progress')} aria-label={`${rank.title}, ${progress}% towards ${next?.title}. Open progress`} aria-expanded={panel === 'progress'} tabIndex={miniature ? -1 : 0}>
      {(variant === 'orbit' || variant === 'combined') && <><span className="crew-ring" style={{ '--progress': `${progress}%` } as React.CSSProperties}><Crew id={avatar} size={49} /></span><span className="rank-copy"><strong>{rank.title}</strong><small>{progress}% to {next?.title}</small></span><Stats points={balance} /></>}
      {variant === 'ticket' && <><span className="ticket-number"><small>RANK</small><strong>{String(rankIndex).padStart(2, '0')}</strong></span><span className="rank-copy"><strong>{rank.title}</strong><Rail value={progress} /></span><Stats points={balance} /></>}
      {variant === 'post' && <><img className="bar-companion" src="/assets/star-crew/personal/08-stargazer-transparent.png" alt="" /><span className="rank-copy"><strong>{rank.title}<span className="little-arrow">↗</span></strong><Rail value={progress} /></span><Stats points={balance} /></>}
      {variant === 'quiet' && <><span className="rank-copy"><strong>{rank.title}<span className="little-arrow">↗</span></strong><Rail value={progress} /></span><Stats points={balance} /></>}
    </button>
    <button className={`notification-control${unread ? ' has-unread' : ''}${panel === 'notifications' ? ' is-open' : ''}`} onClick={() => toggle('notifications')} aria-label={`${direction.action}, ${unread} unread notifications`} aria-expanded={panel === 'notifications'} tabIndex={miniature ? -1 : 0}>
      {variant === 'orbit' && <><Envelope />{unread > 0 && <span className="unread-count">{unread}</span>}</>}
      {(variant === 'ticket' || variant === 'combined') && <><span className="folded-sheet" aria-hidden="true"><i /><i /></span>{unread > 0 && <span className="unread-count">{unread}</span>}</>}
      {variant === 'post' && <><Envelope pocket /><span className="notification-label">Your post</span>{unread > 0 && <span className="unread-count">{unread}</span>}</>}
      {variant === 'quiet' && <><span className="notification-label">Updates</span><span className="unread-count">{unread || '—'}</span></>}
    </button>
  </div>;
}

function Studio() {
  const [variant, setVariant] = useState<Variant>(initialDirection);
  const [device, setDevice] = useState<'desktop' | 'phone'>('desktop');
  const [earned, setEarned] = useState(6200);
  const [balance, setBalance] = useState(5065);
  const [read, setRead] = useState<string[]>([]);
  const [panel, setPanel] = useState<Panel>(phoneReview ? 'notifications' : null);
  const [opened, setOpened] = useState<string | null>(null);
  const [avatar, setAvatar] = useState('reader');
  const [status, setStatus] = useState('Try the progress control or open your notifications.');
  const [celebrating, setCelebrating] = useState(false);
  const celebration = useRef<HTMLDialogElement>(null);
  const panelRoot = useRef<HTMLDivElement>(null);
  const panelTitle = useRef<HTMLHeadingElement>(null);
  const canvas = useRef<HTMLDivElement>(null);
  const direction = directions.find(d => d.id === variant)!;
  const rank = getRankForPoints(earned), next = getNextRank(rank), progress = getRankProgress(earned, rank, next);
  const unread = messages.filter(m => !read.includes(m.id)).length;
  const message = messages.find(m => m.id === opened);

  useEffect(() => {
    if (panel) panelTitle.current?.focus({ preventScroll: true });
  }, [panel]);
  useEffect(() => {
    if (!panel) return;
    const dismiss = (event: PointerEvent) => {
      if (event.target instanceof Element && !panelRoot.current?.contains(event.target) && !event.target.closest('.header-controls')) setPanel(null);
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') { setPanel(null); canvas.current?.querySelector<HTMLButtonElement>(panel === 'progress' ? '.rank-control' : '.notification-control')?.focus(); }
    };
    document.addEventListener('pointerdown', dismiss); document.addEventListener('keydown', escape);
    return () => { document.removeEventListener('pointerdown', dismiss); document.removeEventListener('keydown', escape); };
  }, [panel]);

  const choose = (id: Variant) => { setVariant(id); setPanel(null); setOpened(null); setStatus(`Now previewing ${directions.find(d => d.id === id)!.title}.`); };
  const reset = () => { setEarned(6200); setBalance(5065); setRead([]); setPanel(null); setOpened(null); setStatus('Preview reset. Three new notifications, and your next rank ahead.'); };
  const gain = () => { setEarned(n => n + 120); setBalance(n => n + 120); setStatus('Sample session complete. +120 points — watch the progress move.'); };
  const celebrate = () => { setEarned(7200); setBalance(6065); setPanel(null); setCelebrating(true); celebration.current?.showModal(); setStatus('Level-up preview: Driven becomes Elite.'); };
  const openMessage = (id: string) => { setOpened(id); setRead(items => items.includes(id) ? items : [...items, id]); };
  const setPreviewPanel = (p: Panel) => { setPanel(p); setOpened(null); };

  return <div className={`header-studio${phoneReview ? ' is-phone-review' : ''}`}>
    <header className="studio-masthead"><a href="#top" className="wordmark">nextstepuni</a><span>THE LITTLE DETAILS <b>HEADER STUDIES / YOUR SELECTED PAIRING</b></span></header>
    <main id="top">
      <section className="studio-intro"><div><p className="eyebrow">A familiar face. A little momentum.</p><h1>Your favourites.<br /><span>Together, up here.</span></h1></div><div className="intro-note"><span className="ink-dot" /><p>The Star Crew ring.<br />The little folded note.<br /><strong>Your chosen pairing, together.</strong></p><small>Interactive design study · sample student data</small></div></section>
      <nav className="direction-tabs" aria-label="Design directions">{directions.map(d => <button key={d.id} onClick={() => choose(d.id)} aria-pressed={variant === d.id}><span>{d.number}</span><strong>{d.title}</strong><small>{d.mood}</small></button>)}</nav>

      <section className="current-direction" aria-labelledby="direction-title">
        <div className="direction-heading"><div><p className="eyebrow">{direction.number} / {direction.mood}</p><h2 id="direction-title">{direction.headline}</h2></div><div className="device-switch" aria-label="Preview size"><button onClick={() => {setDevice('desktop');setPanel(null);}} aria-pressed={device === 'desktop'}>Desktop</button><button onClick={() => {setDevice('phone');setPanel(null);}} aria-pressed={device === 'phone'}>Phone</button></div></div>
        <div className={`canvas-wrap device-${device}`}>
          <div className={`app-canvas design-${variant}`} ref={canvas}>
            <div className="context-header"><span className="context-brand">nextstepuni<span>STUDENT SPACE</span></span><HeaderControls variant={variant} earned={earned} balance={balance} unread={unread} avatar={avatar} panel={panel} onPanel={setPreviewPanel} /></div>
            <div className="context-body"><div className="context-topline"><span>WEDNESDAY, 16 SEPTEMBER</span><span>HOME / YOUR NEXT STEP</span></div><div className="context-greeting"><div><h2>Good evening, Aoife.</h2><p>A little focus today. A little further tomorrow.</p></div><img src="/assets/star-crew/companions/thinker.png" alt="The Thinker" /></div><div className="context-lower"><section><p className="eyebrow">UP NEXT</p><h3>A little Irish practice.</h3><p>25 minutes · Active recall</p><button onClick={gain}>Try a completed session <span>↗</span></button></section><section className="context-week"><p className="eyebrow">YOUR WEEK, SO FAR</p><strong>Small steps add up.</strong><div className="week-markers">{['M','T','W','T','F','S','S'].map((d,i) => <span key={i}><i className={i < 3 ? 'done' : ''} />{d}</span>)}</div><p>Three days. Three good starts.</p></section></div></div>
            {panel && <div className={`header-popover popover-${panel}`} ref={panelRoot} role="region" aria-labelledby="popover-title">
              <div className="popover-top"><p className="eyebrow">{panel === 'progress' ? 'EVERY LITTLE STEP' : variant === 'ticket' ? 'NOTES & LITTLE MILESTONES' : 'A LITTLE POST FOR YOU'}</p><button onClick={() => setPanel(null)} aria-label="Close panel">×</button></div>
              {panel === 'progress' ? <><div className="progress-intro"><div><h3 id="popover-title" ref={panelTitle} tabIndex={-1}>{rank.title}.<br />And moving.</h3><p>{Math.max(0, (next?.minPoints ?? earned) - earned).toLocaleString('en-IE')} points to {next?.title ?? 'your next chapter'}.</p></div><Crew id={avatar} size={86} /></div><div className="detail-rail"><Rail value={progress} /><div><span>{rank.title}</span><span>{next?.title} ↗</span></div></div><div className="progress-numbers"><div><strong>{earned.toLocaleString('en-IE')}</strong><span>points earned</span></div><div><strong>{balance.toLocaleString('en-IE')}</strong><span>JP available</span></div><div><strong>18</strong><span>day streak</span></div></div><p className="points-explanation">Your rank follows all the points you’ve earned. Journey Points are the balance you can use on your island.</p><button className="panel-action" onClick={celebrate}>Preview the next rank <span>↗</span></button></> : <>{message ? <><button className="back-to-post" onClick={() => setOpened(null)}>← All updates</button><p className="eyebrow message-origin">{message.kind}</p><h3 id="popover-title" ref={panelTitle} tabIndex={-1}>{message.title}</h3><p className="message-body">{message.body}</p><p className="message-signoff">A little encouragement,<br /><strong>{message.from}</strong></p><span className="read-receipt">Opened · {message.time}</span></> : <><div className="inbox-intro"><div><h3 id="popover-title" ref={panelTitle} tabIndex={-1}>{variant === 'ticket' ? 'A few little notes.' : variant === 'quiet' ? 'Your updates.' : 'You’ve got post.'}</h3><p>{unread ? `${unread} new things to catch up on.` : 'All caught up. A little room to focus.'}</p></div><img src="/assets/star-crew/companions/listener-transparent.png" alt="The Listener" /></div><div className="message-list">{messages.map(m => <button key={m.id} onClick={() => openMessage(m.id)} className={read.includes(m.id) ? 'is-read' : ''}><span className="message-dot" /><span><small>{m.kind}</small><strong>{m.title}</strong><span>{m.time}</span></span><i>↗</i></button>)}</div><button className="mark-read" disabled={!unread} onClick={() => {setRead(messages.map(m=>m.id));setStatus('All notifications marked as read in this preview.');}}>{unread ? 'Mark all as read' : 'All caught up'}</button></>}</>}
            </div>}
          </div>
        </div>
        <div className="preview-tools"><div><span className="eyebrow">TRY A LITTLE MOMENT</span><button onClick={gain}>+120 points</button><button onClick={celebrate}>Preview a level-up ↗</button><button onClick={reset}>Reset</button></div><label>YOUR CHARACTER<select value={avatar} onChange={e => setAvatar(e.target.value)}><option value="reader">Reader</option><option value="maker">Maker</option><option value="stargazer">Stargazer</option><option value="hugger">Hugger</option></select></label></div>
        <p className="preview-status" role="status">{status}</p>
        <div className="direction-details"><p className="direction-description">{direction.description}</p><div><span className="eyebrow">THE LEVEL BAR</span><p>{direction.level}</p></div><div><span className="eyebrow">THE NOTIFICATIONS</span><p>{direction.notification}</p></div></div>
        <div className="designer-note"><span>↳</span><p>{direction.note}</p></div>
      </section>

      <section className="comparison" aria-labelledby="comparison-title"><div className="comparison-heading"><p className="eyebrow">SIDE BY SIDE</p><h2 id="comparison-title">A different kind of hello.</h2><p>Same information. Four different feelings.</p></div><div className="comparison-grid">{directions.filter(d => d.id !== 'combined').map(d => <article key={d.id} className={variant === d.id ? 'is-current' : ''}><div className="comparison-label"><span>{d.number}</span><span>{d.mood}</span></div><div className="mini-control-stage" inert><HeaderControls variant={d.id} earned={6200} balance={5065} unread={3} avatar={avatar} miniature /></div><h3>{d.title}</h3><p>{d.description}</p><button className="comparison-try" onClick={() => {choose(d.id);document.getElementById('direction-title')?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});}}>Try this direction <span>↗</span></button></article>)}</div></section>
      <footer className="studio-footer"><span className="wordmark">nextstepuni</span><p>Little details. A familiar feeling.</p><span>DESIGN EXPLORATION / SEPTEMBER 2026</span></footer>
    </main>
    <dialog ref={celebration} className={`rank-celebration celebration-${variant}`} onClose={() => setCelebrating(false)} onClick={e => {if(e.target === e.currentTarget)celebration.current?.close();}} aria-labelledby="celebration-title"><div className={celebrating?'celebration-content play':'celebration-content'}><button className="celebration-close" aria-label="Close level-up preview" onClick={() => celebration.current?.close()}>×</button><p className="eyebrow">ANOTHER STEP, TAKEN.</p><Crew id={avatar} size={150} /><p className="new-rank-label">YOUR NEW RANK</p><h2 id="celebration-title">Elite.</h2><p>One session at a time.<br />Look how far you’ve come.</p><div className="rank-journey"><span>Driven</span><span>——→</span><strong>Elite</strong></div><button className="celebration-continue" onClick={() => celebration.current?.close()}>Keep going, at my pace <span>↗</span></button><small>Level-up animation preview</small></div></dialog>
  </div>;
}

createRoot(document.getElementById('root')!).render(<Studio />);
