/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "How They Did It" — a card deck of real people who overcame a specific
 * disadvantage a Leaving Cert student might share. Filter by your own barrier,
 * swipe through the deck, then a fast struggle-led reveal: the hook → their words
 * → the hard part → the moves (tap to flip) → where they are now → one move to
 * steal.
 *
 * Look (area 7b, boards c-tools2-how and r5-how-they-did-it): the featured story is
 * the one raised sheet (its drawing, name, hook, Read their story, then the move to
 * borrow with Save and Next beside it); the filters swipe in one row; a story is a
 * task with one way back (the bar's Back steps back a beat), the three moves are
 * cards you turn over and the next beat is pinned. Stories, saving and sound are as
 * they were.
 */

import React, { useMemo, useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowUpRight, Bookmark, BookmarkCheck, ChevronDown } from 'lucide-react';
import { useHowTheyDidIt } from '../../hooks/useHowTheyDidIt';
import { PEOPLE, peopleForBarrier } from '../../howTheyDidItData';
import { BARRIERS, type Barrier, type PersonCard, type PersonMove } from '../../types/howTheyDidIt';
import { useDeckSound, initials } from '../immersiveDeck';
import { Button, TextButton } from '../ui/Button';
import { List, PaperSheet, PressBox, Row } from '../ui/List';
import { PinnedFooter } from '../ui/Bars';
import { useFrameTask } from '../ui/Frame';
import { useBackStep } from '../../contexts/NavigationContext';
import './how-they-did-it-7.css';

const fade = { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 }, transition: { duration: 0.2 } };

const barrierLabel = (b: Barrier) => BARRIERS.find((x) => x.id === b)?.label ?? '';

/** The person's drawing where there is one, their initials on the page otherwise: no tile behind it. */
const Portrait: React.FC<{ person: PersonCard; size?: 'lg' }> = ({ person, size }) => person.portraitKey
  ? <img className={`hw7-portrait${size ? ' hw7-portrait--lg' : ''}`} src={`/portraits/${person.portraitKey}.png`} alt="" />
  : <span className={`hw7-portrait hw7-initials${size ? ' hw7-portrait--lg' : ''}`} aria-hidden="true">{initials(person.name)}</span>;

/** A move you turn over: its number, its name and "Turn over"; turned, what they did. */
const MoveTile: React.FC<{ move: PersonMove; idx: number; onFlip: () => void }> = ({ move, idx, onFlip }) => {
  const [flipped, setFlipped] = useState(false);
  return (
    <PressBox className="hw7-flip" pressed={flipped} onPress={() => { setFlipped((f) => !f); onFlip(); }}>
      <span className="hw7-flip-n">{idx + 1}</span>
      {flipped
        ? <span className="hw7-flip-back"><span className="hw7-flip-title">{move.title}</span>{move.detail}</span>
        : <><span className="hw7-flip-front">{move.title}</span><span className="t-meta hw7-turn">Turn over</span></>}
    </PressBox>
  );
};

/** Expandable "see the sources" disclosure. */
const Sources: React.FC<{ sources: string[] }> = ({ sources }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="hw7-sources">
      <TextButton tone="quiet" aria-expanded={open} onClick={() => setOpen((o) => !o)}>
        Real story · {sources.length} {sources.length === 1 ? 'source' : 'sources'}
        <ChevronDown className="ui-icon hw7-chev" data-open={open || undefined} width={16} height={16} strokeWidth={2} aria-hidden="true" />
      </TextButton>
      {open && (
        <ul className="hw7-source-list">
          {sources.map((s, i) => (
            <li key={i}><a className="hw7-source" href={s} target="_blank" rel="noreferrer">
              <span>{s.replace(/^https?:\/\//, '').split('/')[0]}</span>
              <ArrowUpRight className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" />
            </a></li>
          ))}
        </ul>
      )}
    </div>
  );
};

type Beat = 'front' | 'struggle' | 'moves' | 'now';
const BEAT_IDX: Record<Beat, number> = { front: 0, struggle: 1, moves: 2, now: 3 };
const BEATS: Beat[] = ['front', 'struggle', 'moves', 'now'];

const HowTheyDidIt: React.FC<{ uid?: string; studentSubjects?: string[] }> = ({ uid }) => {
  const { state, isLoaded, markSeen, toggleSaved } = useHowTheyDidIt(uid);
  const sound = useDeckSound();
  const [filter, setFilter] = useState<Barrier | 'all'>('all');
  const [cardId, setCardId] = useState<string | null>(null);
  const [beat, setBeat] = useState<Beat>('front');
  const [showSaved, setShowSaved] = useState(false);
  const [index, setIndex] = useState(0);
  useEffect(() => { setIndex(0); }, [filter]);

  const deck = useMemo(() => (filter === 'all' ? PEOPLE : peopleForBarrier(filter)), [filter]);
  const card = cardId ? PEOPLE.find((p) => p.id === cardId) ?? null : null;
  const savedCards = useMemo(() => PEOPLE.filter((p) => state.savedIds.includes(p.id)), [state.savedIds]);

  const open = (p: PersonCard) => { setCardId(p.id); setBeat('front'); markSeen(p.id); sound.play('tap'); };

  const goBeat = (b: Beat) => { setBeat(b); sound.play('tap'); };

  // A story is a task on a phone: its next beat is pinned and the tab bar steps aside. The bar's
  // one Back steps back a beat, and from the first beat returns to the deck (board c-tools2-how).
  useFrameTask(Boolean(card));
  useBackStep(Boolean(card), () => { if (beat === 'front') setCardId(null); else setBeat(BEATS[BEAT_IDX[beat] - 1]); });
  useBackStep(!card && showSaved, () => setShowSaved(false));

  const saveFromDetail = (id: string) => {
    const wasSaved = state.savedIds.includes(id);
    toggleSaved(id);
    if (!wasSaved) sound.play('save');
  };

  const nextUnseen = (): PersonCard | null =>
    deck.find((p) => p.id !== card?.id && !state.seenIds.includes(p.id)) ?? deck.find((p) => p.id !== card?.id) ?? null;

  if (!isLoaded) return <div className="hw7"><p className="t-sub hw7-loading">Loading…</p></div>;

  // ── A story, in four beats ─────────────────────────────────────
  if (card) {
    const isSaved = state.savedIds.includes(card.id);
    const bi = BEAT_IDX[beat];
    const next = nextUnseen();
    return (
      <div className="hw7 hw7-read" data-beat={beat}>
        <div className="hw7-who">
          <Portrait person={card} size="lg" />
          <div className="hw7-who-name"><p className="t-label">{card.field} · {barrierLabel(card.barrier)}</p><h2 className="t-title">{card.name}</h2></div>
        </div>
        <div className="hw7-progress">
          <span className="hw7-steps" role="img" aria-label={`Beat ${bi + 1} of 4`}>{BEATS.map((b, i) => <i key={b} data-state={i < bi ? 'done' : i === bi ? 'now' : undefined} />)}</span>
          <span className="ui-readout">{bi + 1} of 4</span>
        </div>
        <AnimatePresence mode="wait">
          <MotionDiv key={beat} {...fade} className="hw7-beat">
            {beat === 'front' && (
              card.quote ? (
                <>
                  <p className="t-title hw7-quote">“{card.quote}”</p>
                  <p className="t-sub">{card.hook}</p>
                </>
              ) : (
                <p className="t-title hw7-quote">{card.hook}</p>
              )
            )}

            {beat === 'struggle' && (
              <section className="hw7-sec">
                <p className="t-label">The hard part</p>
                <ul className="hw7-struggle">
                  {card.struggle.map((s, i) => <li key={i}><span className="hw7-dot" aria-hidden="true" /><span>{s}</span></li>)}
                </ul>
              </section>
            )}

            {beat === 'moves' && (
              <>
                <section className="hw7-sec">
                  <div className="hw7-head"><h3 className="t-heading">What they did</h3><span className="t-meta">Tap a card to turn it</span></div>
                  <div className="hw7-flips">
                    {card.moves.map((m, i) => <MoveTile key={i} move={m} idx={i} onFlip={() => sound.play('tap')} />)}
                  </div>
                </section>
                {card.helpedBy && (
                  <section className="hw7-sec">
                    <p className="t-label">Who helped</p>
                    <p className="t-body">{card.helpedBy}</p>
                  </section>
                )}
              </>
            )}

            {beat === 'now' && (
              <>
                <section className="hw7-sec">
                  <p className="t-label">Where they are now</p>
                  <p className="hw7-now">{card.now}</p>
                  {card.strengthsLine && <p className="t-sub">{card.strengthsLine}</p>}
                </section>
                <section className="hw7-sec hw7-steal">
                  <p className="t-label">Steal this move</p>
                  <p className="t-body">{card.stealThisMove}</p>
                  <Button size="sm" className="hw7-save" aria-pressed={isSaved} onClick={() => saveFromDetail(card.id)}>
                    {isSaved ? <><BookmarkCheck size={16} aria-hidden="true" /> Saved to your playbook</> : <><Bookmark size={16} aria-hidden="true" /> Save this move</>}
                  </Button>
                </section>
                {card.sources.length > 0 && <Sources sources={card.sources} />}
              </>
            )}
          </MotionDiv>
        </AnimatePresence>
        <div className="hw7-foot-wrap frame-float frame-float-bottom">
          <PinnedFooter className="hw7-foot">
            {beat === 'front' && <Button kind="main" size="lg" block arrow="forward" onClick={() => goBeat('struggle')}>See how</Button>}
            {beat === 'struggle' && <Button kind="main" size="lg" block arrow="forward" onClick={() => goBeat('moves')}>What they did</Button>}
            {beat === 'moves' && <Button kind="main" size="lg" block arrow="forward" onClick={() => goBeat('now')}>Where they are now</Button>}
            {beat === 'now' && <>
              {next && <Button kind="main" size="lg" block arrow="forward" onClick={() => open(next)}>Next person</Button>}
              <TextButton tone="quiet" className="hw7-to-deck" onClick={() => setCardId(null)}>Back to deck</TextButton>
            </>}
          </PinnedFooter>
        </div>
      </div>
    );
  }

  // ── SAVED VIEW ("your playbook") ──────────────────────────────
  if (showSaved) {
    return (
      <div className="hw7 hw7-playbook">
        <div className="hw7-sec">
          <h2 className="t-title">Your playbook</h2>
          <p className="t-sub">The moves you saved — your own list of things to try.</p>
        </div>
        {savedCards.length === 0 ? (
          <p className="t-sub">Nothing saved yet — open a card and tap “Save this move”.</p>
        ) : (
          <List label="Your playbook">
            {savedCards.map((p) => <Row key={p.id} art={<Portrait person={p} />} title={p.name} meta={p.stealThisMove} label={`Open card: ${p.name}`} onPress={() => open(p)} />)}
          </List>
        )}
      </div>
    );
  }

  // Browsable collection; saved stories and the full sourced reading flow stay intact.
  const top = deck[index];
  const others = top ? deck.filter(p => p.id !== top.id) : [];
  return <div className="hw7 hw7-deck">
    <div className="hw7-filters" role="group" aria-label="Story situations">
      <Button size="sm" aria-pressed={filter === 'all'} onClick={() => setFilter('all')}>Everyone</Button>
      {BARRIERS.map(b => <Button size="sm" key={b.id} aria-pressed={filter === b.id} onClick={() => setFilter(b.id)}>{b.label}</Button>)}
      {state.savedIds.length > 0 && <Button size="sm" className="hw7-playbook-btn" onClick={() => setShowSaved(true)}>Your playbook ({state.savedIds.length}) <Bookmark size={16} aria-hidden="true" /></Button>}
    </div>
    {top ? <div className="hw7-layout">
      <PaperSheet className="hw7-story" label={top.name}>
        <div className="hw7-feature">
          <div className="hw7-feature-copy">
            <p className="t-label">{top.field} · {barrierLabel(top.barrier)}</p>
            <h2 className="t-title hw7-name">{top.name}</h2>
          </div>
          <Portrait person={top} />
          <p className="hw7-hook">{top.hook}</p>
        </div>
        <Button kind="main" size="lg" block arrow="forward" className="hw7-read-btn" onClick={() => open(top)}>Read their story</Button>
        <div className="hw7-borrow">
          <p className="t-label">One move to borrow</p>
          <p className="t-sub">{top.stealThisMove}</p>
          <div className="ui-pair">
            <Button aria-pressed={state.savedIds.includes(top.id)} onClick={() => toggleSaved(top.id)}><Bookmark size={16} aria-hidden="true" />{state.savedIds.includes(top.id) ? 'Saved to your playbook' : 'Save this story'}</Button>
            <Button onClick={() => setIndex((index + 1) % deck.length)}>Next story</Button>
          </div>
        </div>
      </PaperSheet>
      <section className="hw7-others" aria-label="Another way in">
        <div className="hw7-head"><h2 className="t-heading">Another way in</h2><span className="ui-readout">{others.length} more</span></div>
        <List className="hw7-people">
          {others.map(p => <Row key={p.id} over={p.field} title={p.name} meta={p.hook} label={`Read their story: ${p.name}`} onPress={() => open(p)} />)}
        </List>
      </section>
    </div> : <p className="t-sub">No more stories in this group. Choose another situation above.</p>}
  </div>;
};

export default HowTheyDidIt;
