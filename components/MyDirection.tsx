import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight, Check, Search } from 'lucide-react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { VISION_CARDS, VISION_CARD_ART, NORTH_STAR_CATEGORIES } from '../northStarData';
import type { DirectionItemState, DirectionProfile, NorthStar } from '../types';
import { createDirectionProfile, getNorthStarDisplayText, hasStudentAuthoredNorthStar, normaliseDirectionProfile } from '../services/directionProfile';
import { saveInBackground } from '../utils/firestoreWrite';
import './student-screens.css';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';

interface MyDirectionProps {
  uid: string;
  northStar: NorthStar;
  onBack: () => void;
  onEditNorthStar: () => void;
  onOpenFutureFinder: () => void;
  onOpenPointsPassport: () => void;
}

const STATES: Array<{ id: DirectionItemState; label: string }> = [
  { id: 'curious', label: 'Curious' },
  { id: 'exploring', label: 'Exploring' },
  { id: 'serious-option', label: 'Serious option' },
  { id: 'current-target', label: 'Current target' },
  { id: 'not-for-me', label: 'Not for me' },
];

const MyDirection: React.FC<MyDirectionProps> = ({
  uid, northStar, onBack, onEditNorthStar, onOpenFutureFinder, onOpenPointsPassport,
}) => {
  const { rawProgressDoc, updateDemoProgress } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const [profile, setProfile] = useState<DirectionProfile>(() => createDirectionProfile(northStar));
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (isDemo) {
      setProfile(normaliseDirectionProfile(rawProgressDoc.directionProfile, northStar));
      setLoaded(true);
      return;
    }
    let live = true;
    getDoc(doc(db, 'progress', uid)).then(snapshot => {
      if (!live) return;
      setProfile(normaliseDirectionProfile(snapshot.data()?.directionProfile, northStar));
      setLoaded(true);
    }).catch(() => {
      if (live) setLoaded(true);
    });
    return () => { live = false; };
  }, [uid, northStar, isDemo, rawProgressDoc.directionProfile]);

  const cardsById = useMemo(() => new Map(VISION_CARDS.map(card => [card.id, card])), []);
  const category = NORTH_STAR_CATEGORIES.find(item => item.id === northStar.category);

  const updateState = (id: string, state: DirectionItemState) => {
    const now = new Date().toISOString();
    const next: DirectionProfile = {
      ...profile,
      reviewedAt: now,
      visionItems: profile.visionItems.map(item => item.id === id ? { ...item, state, updatedAt: now } : item),
    };
    setProfile(next);
    if (isDemo) updateDemoProgress(current => ({ ...current, directionProfile: next }));
    else saveInBackground(setDoc(doc(db, 'progress', uid), { directionProfile: next }, { merge: true }), 'MyDirection.updateState');
  };

  return (
    <main className="direction-page min-h-screen">
      <header className="direction-navigation"><div><button type="button" onClick={onBack} aria-label="Back"><ArrowLeft size={21} /></button><h1>My Direction</h1></div><button type="button" className="student-secondary" onClick={onEditNorthStar}>Edit my direction <ArrowRight size={18} /></button></header>
      <div className={`direction-body ${loaded ? '' : 'opacity-70'}`}>
        <section className="direction-north-star">
          <img src="/assets/training/north-star-compass.png" alt="" />
          <p className="student-eyebrow">Your North Star · {category?.label ?? 'Your next chapter'}</p>
          <h2>{hasStudentAuthoredNorthStar(northStar) ? `“${getNorthStarDisplayText(northStar)}”` : getNorthStarDisplayText(northStar)}</h2>
          <p>A direction to move towards. And room to change your mind.</p>
        </section>
        <section className="direction-vision">
          <p className="student-eyebrow">Your vision board</p><h2>A glimpse of what could be.</h2><p>Move each idea as your thinking develops. Nothing here locks you into a path.</p>
          <div className="direction-cards">{profile.visionItems.map(item => {
            const card = cardsById.get(item.id);
            if (!card) return null;
            const artwork = VISION_CARD_ART[card.id];
            return <article className="student-ink-card direction-card" key={item.id}>
              {artwork && <img src={artwork} alt="" />}
              <h3>{card.label}</h3>
              <label className="sr-only" htmlFor={`direction-${item.id}`}>Where {card.label} sits</label>
              <select id={`direction-${item.id}`} value={item.state} onChange={event => updateState(item.id, event.target.value as DirectionItemState)}>{STATES.map(state => <option key={state.id} value={state.id}>{state.label}</option>)}</select>
            </article>;
          })}</div>
        </section>
        <section className="direction-next"><p className="student-eyebrow">Next moves</p><div>
          <button type="button" className="student-ink-card" onClick={onOpenFutureFinder}><Search size={22} /><span><strong>Explore fitting routes</strong><small>Turn interests into courses and pathways.</small></span><ArrowRight size={19} /></button>
          <button type="button" className="student-ink-card" onClick={onOpenPointsPassport}><Check size={22} /><span><strong>Check what is within reach</strong><small>Connect targets to your projected points.</small></span><ArrowRight size={19} /></button>
        </div></section>
      </div>
    </main>
  );
};

export default MyDirection;
