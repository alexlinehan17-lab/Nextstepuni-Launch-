import React, { useEffect, useMemo, useState } from 'react';
import { Check, ChevronRight, Search } from 'lucide-react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { VISION_CARDS, VISION_CARD_ART, NORTH_STAR_CATEGORIES } from '../northStarData';
import type { DirectionItemState, DirectionProfile, NorthStar } from '../types';
import { createDirectionProfile, getNorthStarDisplayText, hasStudentAuthoredNorthStar, normaliseDirectionProfile } from '../services/directionProfile';
import { saveInBackground } from '../utils/firestoreWrite';
import PageHeader from './ui/PageHeader';
import { Button } from './ui/Button';
import { Menu } from './ui/Menu';
import { PressBox } from './ui/List';
import ThemeArtwork from './ThemeArtwork';
import './my-direction.css';
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

  // The look (r5-my-direction, agreed 26 Nov 2026): the frame's bar with one
  // Back; the compass, the quote and each vision drawing at full size; the
  // vision ideas and next moves on the page between thin rules; "Edit my
  // direction" under the quote; each idea's place is the shared menu.
  return (
    <main className="md-page min-h-screen">
      <div className="md-bar"><div className="md-width"><PageHeader onBack={onBack} title="My Direction" /></div></div>
      <div className={`md-width md-body ${loaded ? '' : 'opacity-70'}`}>
        <section className="md-north" aria-labelledby="md-quote">
          <ThemeArtwork className="md-compass" src="/assets/training/north-star-compass.png" transparentBackground alt="" />
          <p className="t-label md-label">Your North Star · {category?.label ?? 'Your next chapter'}</p>
          <h2 id="md-quote" className="t-display md-quote">{hasStudentAuthoredNorthStar(northStar) ? `“${getNorthStarDisplayText(northStar)}”` : getNorthStarDisplayText(northStar)}</h2>
          <p className="t-sub">A direction to move towards. And room to change your mind.</p>
          <Button arrow="forward" className="md-edit" onClick={onEditNorthStar}>Edit my direction</Button>
        </section>
        <section className="md-sec" aria-labelledby="md-vision-title">
          <p className="t-label md-label">Your vision board</p>
          <h2 id="md-vision-title" className="t-title">A glimpse of what could be.</h2>
          <p className="t-sub">Move each idea as your thinking develops. Nothing here locks you into a path.</p>
          <div className="md-ideas">{profile.visionItems.map(item => {
            const card = cardsById.get(item.id);
            if (!card) return null;
            const artwork = VISION_CARD_ART[card.id];
            return <article className="md-idea" key={item.id}>
              {artwork && <ThemeArtwork src={artwork} transparentBackground alt="" />}
              <h3 className="t-heading">{card.label}</h3>
              <Menu label={`Where ${card.label} sits`} className="md-state" value={item.state} onChange={state => updateState(item.id, state)}
                options={STATES.map(state => ({ value: state.id, label: state.label }))} />
            </article>;
          })}</div>
        </section>
        <section className="md-sec" aria-label="Next moves">
          <p className="t-label md-label">Next moves</p>
          <div className="md-doors">
            <PressBox className="md-door" onPress={onOpenFutureFinder}><Search className="md-door-icon" size={20} strokeWidth={1.75} aria-hidden="true" /><span className="md-door-words"><span className="t-row">Explore fitting routes</span><span className="t-meta">Turn interests into courses and pathways.</span></span><ChevronRight className="md-door-chev" size={20} strokeWidth={1.75} aria-hidden="true" /></PressBox>
            <PressBox className="md-door" onPress={onOpenPointsPassport}><Check className="md-door-icon" size={20} strokeWidth={1.75} aria-hidden="true" /><span className="md-door-words"><span className="t-row">Check what is within reach</span><span className="t-meta">Connect targets to your projected points.</span></span><ChevronRight className="md-door-chev" size={20} strokeWidth={1.75} aria-hidden="true" /></PressBox>
          </div>
        </section>
      </div>
    </main>
  );
};

export default MyDirection;
