import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight, Check, Search } from 'lucide-react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { VISION_CARDS, VISION_CARD_ART, NORTH_STAR_CATEGORIES } from '../northStarData';
import type { DirectionItemState, DirectionProfile, NorthStar } from '../types';
import { createDirectionProfile, getNorthStarDisplayText, hasStudentAuthoredNorthStar, normaliseDirectionProfile } from '../services/directionProfile';
import { saveInBackground } from '../utils/firestoreWrite';
import NorthStarCategoryIcon from './NorthStarCategoryIcon';
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

const VISION_BLOB_COLOUR: Record<string, string> = {
  independence: '#D8E9D4',
  'family-community': '#EBC7D4',
  'career-craft': '#F5CFB0',
  'college-learning': '#C7D8EA',
  'prove-myself': '#F1C0B4',
  'options-freedom': '#BFDCD5',
  'family-people': '#EBC7D4',
  'prove-myself-jc': '#F1C0B4',
  'curiosity-craft': '#D8D0ED',
  'future-doors': '#C7E2D2',
};

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
  const activeItems = profile.visionItems.filter(item => item.state !== 'not-for-me');
  const targetCount = profile.visionItems.filter(item => item.state === 'current-target').length;

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
    <main className="min-h-screen theme-compat bg-[#FAFBF6] text-[#1A1A1A] dark:bg-zinc-950 dark:text-zinc-50">
      <header className="border-b border-[#DED9D2] dark:border-zinc-800">
        <div className="mx-auto flex max-w-6xl items-center gap-5 px-5 py-6 md:px-8">
          <button onClick={onBack} aria-label="Back" className="grid h-12 w-12 place-items-center rounded-2xl border-2 border-[#292929] bg-white shadow-[3px_3px_0_#292929] transition-transform hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-none dark:bg-zinc-900 dark:border-zinc-500 dark:shadow-[3px_3px_0_#52525b]">
            <ArrowLeft size={21} />
          </button>
          <div className="h-12 w-px bg-[#DED9D2] dark:bg-zinc-700" />
          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.22em] text-[#968B81]">Your direction</p>
            <h1 className="font-serif text-3xl font-semibold md:text-4xl">My Direction</h1>
          </div>
        </div>
      </header>

      <div className={`mx-auto max-w-6xl px-5 py-10 transition-opacity md:px-8 ${loaded ? 'opacity-100' : 'opacity-70'}`}>
        <section className="grid gap-5 md:grid-cols-[1.35fr_.65fr]">
          <div className="rounded-[28px] border-2 border-[#292929] bg-white p-7 shadow-[6px_6px_0_#292929] dark:bg-zinc-900 dark:border-zinc-600 dark:shadow-[6px_6px_0_#52525b] md:p-10">
            <div className="flex items-start justify-between gap-6">
              <div>
                <p className="mb-3 text-[11px] font-bold uppercase tracking-[0.2em] text-[#F26B1F]">North Star</p>
                <h2 className="max-w-2xl font-serif text-3xl leading-tight md:text-5xl">{category?.label ?? 'Your next chapter'}</h2>
                <p className={`mt-5 max-w-2xl text-lg leading-relaxed text-[#6F665E] dark:text-zinc-300 ${hasStudentAuthoredNorthStar(northStar) ? 'font-serif italic' : ''}`}>
                  {hasStudentAuthoredNorthStar(northStar) ? `“${getNorthStarDisplayText(northStar)}”` : getNorthStarDisplayText(northStar)}
                </p>
              </div>
              <NorthStarCategoryIcon category={northStar.category} size={80} className="-mr-1 -mt-2" />
            </div>
            <button onClick={onEditNorthStar} className="mt-8 rounded-xl border-[1.5px] border-[#292929] px-4 py-2.5 text-sm font-bold hover:bg-[#F5F1EB] dark:hover:bg-zinc-800">Review my choices</button>
          </div>

          <aside className="overflow-hidden rounded-[28px] border-2 border-[#292929] bg-white shadow-[6px_6px_0_#292929] dark:border-zinc-600 dark:bg-zinc-900 dark:shadow-[6px_6px_0_#52525b]">
            <div className="border-b border-[#DED9D2] px-7 py-5 dark:border-zinc-700">
              <p className="text-[11px] font-bold uppercase tracking-[0.2em] text-[#968B81]">Direction snapshot</p>
            </div>
            <div className="divide-y divide-[#DED9D2] dark:divide-zinc-700">
              <div className="grid grid-cols-[64px_1fr] items-center gap-4 px-7 py-6">
                <span className="font-serif text-4xl">{activeItems.length}</span>
                <div>
                  <p className="text-sm font-bold">On your board</p>
                  <p className="mt-1 text-sm leading-snug text-[#756D66] dark:text-zinc-400">Possibilities you are still considering</p>
                </div>
              </div>
              <div className="grid grid-cols-[64px_1fr] items-center gap-4 px-7 py-6">
                <span className="font-serif text-4xl">{targetCount}</span>
                <div>
                  <p className="text-sm font-bold">Current targets</p>
                  <p className="mt-1 text-sm leading-snug text-[#756D66] dark:text-zinc-400">Priorities linked to your next steps</p>
                </div>
              </div>
            </div>
          </aside>
        </section>

        <section className="mt-14">
          <div className="max-w-2xl">
            <p className="text-[11px] font-bold uppercase tracking-[0.2em] text-[#968B81]">Your vision board</p>
            <h2 className="mt-2 font-serif text-3xl md:text-4xl">Possibilities, not promises.</h2>
            <p className="mt-3 leading-relaxed text-[#756D66] dark:text-zinc-400">Move each idea as your thinking develops. Nothing here locks you into a path.</p>
          </div>

          <div className="mt-7 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {profile.visionItems.map((item, index) => {
              const card = cardsById.get(item.id);
              if (!card) return null;
              const artwork = VISION_CARD_ART[card.id];
              return (
                <article key={item.id} className="rounded-[22px] border-[1.5px] border-[#292929] bg-white p-5 dark:bg-zinc-900 dark:border-zinc-600">
                  <div className="flex items-start justify-between gap-4">
                    <span className="font-mono text-xs text-[#F26B1F]">{String(index + 1).padStart(2, '0')}</span>
                    {artwork && (
                      <span
                        className="grid h-16 w-16 shrink-0 place-items-center rounded-[46%_54%_48%_52%/52%_44%_56%_48%]"
                        style={{ backgroundColor: VISION_BLOB_COLOUR[card.category] ?? '#E4DDD4' }}
                        aria-hidden="true"
                      >
                        <img src={artwork} alt="" className="h-[72px] w-[72px] max-w-none object-contain" />
                      </span>
                    )}
                  </div>
                  <h3 className="mt-5 min-h-14 font-serif text-2xl leading-tight">{card.label}</h3>
                  <label className="mt-5 block text-[10px] font-bold uppercase tracking-[0.18em] text-[#968B81]" htmlFor={`direction-${item.id}`}>Where it sits</label>
                  <select id={`direction-${item.id}`} value={item.state} onChange={event => updateState(item.id, event.target.value as DirectionItemState)} className="mt-2 w-full rounded-xl border-[1.5px] border-[#CFC8BF] bg-[#FAF8F4] px-3 py-2.5 text-sm font-semibold outline-none focus:border-[#292929] dark:bg-zinc-800 dark:border-zinc-600">
                    {STATES.map(state => <option key={state.id} value={state.id}>{state.label}</option>)}
                  </select>
                </article>
              );
            })}
          </div>
        </section>

        <section className="mt-14 border-t border-[#DED9D2] pt-9 dark:border-zinc-800">
          <p className="text-[11px] font-bold uppercase tracking-[0.2em] text-[#968B81]">Next moves</p>
          <div className="mt-5 grid gap-4 md:grid-cols-2">
            <button onClick={onOpenFutureFinder} className="group flex items-center gap-4 rounded-[22px] border-2 border-[#292929] bg-white p-5 text-left shadow-[4px_4px_0_#292929] transition-transform hover:-translate-y-0.5 dark:bg-zinc-900 dark:border-zinc-600 dark:shadow-[4px_4px_0_#52525b]">
              <Search size={22} /><span className="flex-1"><strong className="block">Explore fitting routes</strong><small className="mt-1 block text-[#756D66] dark:text-zinc-400">Turn interests into courses and pathways.</small></span><ArrowRight size={19} />
            </button>
            <button onClick={onOpenPointsPassport} className="group flex items-center gap-4 rounded-[22px] border-2 border-[#292929] bg-[#F26B1F] p-5 text-left text-white shadow-[4px_4px_0_#292929] transition-transform hover:-translate-y-0.5 dark:border-zinc-600 dark:shadow-[4px_4px_0_#52525b]">
              <Check size={22} /><span className="flex-1"><strong className="block">Check what is within reach</strong><small className="mt-1 block text-orange-100">Connect targets to your projected points.</small></span><ArrowRight size={19} />
            </button>
          </div>
        </section>
      </div>
    </main>
  );
};

export default MyDirection;
