/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useCallback, useEffect, useRef, Suspense } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, Mountain, Users, Heart, Gift, X } from 'lucide-react';
import { SessionUser } from '../Auth';
import { NorthStar, UserProgress } from '../../types';
import { MilestoneReward } from '../../islandShopData';
import { db } from '../../firebase';
import { collection, query, where, getDocs, doc, getDoc } from 'firebase/firestore';

const FlareSystem = React.lazy(() => import('../flares/FlareSystem'));
import { useIslandShop, EnrichedShopItem } from '../../hooks/useIslandShop';
import JourneyCanvas from './JourneyCanvas';
import JourneyProgressPill from './JourneyProgressPill';
import IslandShopDrawer from './IslandShopDrawer';
import PurchaseCelebrationModal from './PurchaseCelebrationModal';
import MilestoneRewardModal from './MilestoneRewardModal';
import PeerIslandsList from './PeerIslandsList';
import KudosButton from './KudosButton';
import GiftButton from './GiftButton';
import { usePeerIslands, PeerIsland } from '../../hooks/usePeerIslands';
import { useKudos } from '../../hooks/useKudos';
import { useGifts } from '../../hooks/useGifts';
import { KUDOS_MESSAGES } from '../../kudosData';
import { STARTER_PACKS } from '../../islandShopData';
import { getAvatarUrl } from '../Auth';

interface CourseInfo {
  id: string;
  sectionsCount: number;
}

interface JourneyViewProps {
  onBack: () => void;
  user: SessionUser;
  northStar: NorthStar | null;
  onOpenNorthStar: () => void;
  pointsBalance: number;
  onPointsReload: () => void;
  userProgress?: UserProgress;
  allCourses?: CourseInfo[];
  subjects?: string[];
  flaresEnabled?: boolean;
}

const JourneyView: React.FC<JourneyViewProps> = ({
  onBack, user, northStar, onOpenNorthStar, pointsBalance, onPointsReload,
  userProgress, allCourses, subjects, flaresEnabled,
}) => {
  // Compute completed module count
  const completedCount = (allCourses ?? []).filter(c => {
    const p = userProgress?.[c.id];
    return p && p.unlockedSection >= c.sectionsCount;
  }).length;

  const {
    islandState,
    isLoading,
    availableItems,
    waterColor,
    stats,
    purchaseItem,
    placeGiftItem,
    hasItem,
    milestoneRewards,
    claimReward,
  } = useIslandShop(user.uid, northStar, completedCount);

  const [sheetOpen, setSheetOpen] = useState(false);
  const [celebrationActive, setCelebrationActive] = useState(false);
  const [purchasedItemName, setPurchasedItemName] = useState<string | null>(null);
  const [rewardModalItem, setRewardModalItem] = useState<string | null>(null);
  const [rewardModalModules, setRewardModalModules] = useState(0);

  // Peer Islands state
  type PeerViewMode = 'own' | 'peer-list' | 'peer-island';
  const [peerViewMode, setPeerViewMode] = useState<PeerViewMode>('own');
  const [selectedPeer, setSelectedPeer] = useState<PeerIsland | null>(null);
  const { peers, isLoading: peersLoading } = usePeerIslands(user.uid, user.school);
  const { kudosCount, recentKudos, canSendKudosTo, sendKudos, getMessageText } = useKudos(user.uid);
  const { pendingGifts, canSendGiftToday, sendGift, markGiftPlaced } = useGifts(user.uid);

  const [kudosModalOpen, setKudosModalOpen] = useState(false);
  const [giftsModalOpen, setGiftsModalOpen] = useState(false);

  // Flare system state
  const [flareSystemOpen, setFlareSystemOpen] = useState(false);
  const [flareInitialView, setFlareInitialView] = useState<'launcher' | 'feed'>('launcher');
  const [activeFlareCount, setActiveFlareCount] = useState(0);
  const [rescueCount, setRescueCount] = useState(0);

  // Fetch active flare count + rescue count
  useEffect(() => {
    if (!user?.uid || !user?.school || !subjects?.length || flaresEnabled === false) return;
    let cancelled = false;
    const fetchFlareData = async () => {
      try {
        // Fetch active flares count
        const q = query(
          collection(db, 'flares'),
          where('school', '==', user.school),
          where('status', '==', 'active'),
        );
        const snap = await getDocs(q);
        if (cancelled) return;
        const now = new Date();
        const count = snap.docs.filter(d => {
          const data = d.data();
          return data.senderUid !== user.uid
            && subjects?.includes(data.subject)
            && data.expiresAt?.toDate() > now;
        }).length;
        setActiveFlareCount(count);

        // Fetch rescue count from user doc
        try {
          const userDoc = await getDoc(doc(db, 'users', user.uid));
          if (!cancelled && userDoc.exists()) {
            setRescueCount(userDoc.data()?.rescueCount ?? 0);
          }
        } catch (_) {
          // Non-critical
        }
      } catch (e) {
        console.error('Failed to fetch flare count:', e);
      }
    };
    fetchFlareData();
    return () => { cancelled = true; };
  }, [user?.uid, user?.school, subjects, flaresEnabled]);

  const isViewingPeer = peerViewMode === 'peer-island' && selectedPeer !== null;

  const handleSelectPeer = useCallback((peer: PeerIsland) => {
    setSelectedPeer(peer);
    setPeerViewMode('peer-island');
  }, []);

  const handleBackFromPeer = useCallback(() => {
    if (peerViewMode === 'peer-island') {
      setPeerViewMode('peer-list');
      setSelectedPeer(null);
    } else {
      setPeerViewMode('own');
    }
  }, [peerViewMode]);

  // Track which rewards we've already auto-notified about
  const lastNotifiedCountRef = useRef(0);

  // DEV override: infinite points for testing
  const DEV_INFINITE_POINTS = false;
  const effectivePoints = DEV_INFINITE_POINTS ? 999999 : pointsBalance;

  const handlePurchase = useCallback(async (item: EnrichedShopItem) => {
    const success = await purchaseItem(item, effectivePoints);
    if (success) {
      onPointsReload();
      setCelebrationActive(true);
      setTimeout(() => setCelebrationActive(false), 2500);
      setPurchasedItemName(item.name);
    }
  }, [purchaseItem, effectivePoints, onPointsReload]);

  const handleClaimReward = useCallback(async (reward: MilestoneReward) => {
    const success = await claimReward(reward);
    if (success) {
      setCelebrationActive(true);
      setTimeout(() => setCelebrationActive(false), 2500);
      setRewardModalItem(reward.item.name);
      setRewardModalModules(completedCount);
    }
  }, [claimReward, completedCount]);

  // Auto-open milestone reward modal when new rewards become claimable
  useEffect(() => {
    const claimableRewards = milestoneRewards.filter(r => r.status === 'claimable');
    if (claimableRewards.length > lastNotifiedCountRef.current && lastNotifiedCountRef.current >= 0) {
      // Only auto-notify if this isn't the first render
      if (lastNotifiedCountRef.current > 0 || claimableRewards.length > 0) {
        // Don't auto-claim, just let the Rewards tab badge notify the user
      }
    }
    lastNotifiedCountRef.current = claimableRewards.length;
  }, [milestoneRewards]);

  // No North Star set
  if (!northStar) {
    return (
      <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col items-center justify-center px-6 text-center">
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-md"
        >
          <div className="w-20 h-20 rounded-2xl bg-[rgba(var(--accent),0.15)] text-[var(--accent-hex)] flex items-center justify-center mx-auto mb-6">
            <Mountain size={40} />
          </div>
          <h2 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white mb-3">Set Your North Star</h2>
          <p className="text-zinc-500 dark:text-zinc-400 text-sm leading-relaxed mb-8">
            Your North Star defines what you're working towards. Set it to unlock your personal journey and start building towards your goals.
          </p>
          <button
            onClick={onOpenNorthStar}
            className="px-6 py-3 rounded-xl bg-[var(--accent-hex)] text-white font-semibold text-sm hover:opacity-90 transition-opacity"
          >
            Choose My North Star
          </button>
          <button
            onClick={onBack}
            className="block mx-auto mt-4 text-sm text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300"
          >
            Go Back
          </button>
        </MotionDiv>
      </div>
    );
  }

  if (isLoading || !islandState) {
    return (
      <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-[var(--accent-hex)] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-zinc-950 z-[70] flex flex-col">
      <div className="flex-1 flex flex-col min-h-0 relative">
        {/* 3D Canvas area */}
        <div className="relative flex-1 min-w-0">
          <JourneyCanvas
            placements={isViewingPeer ? selectedPeer.islandState.placements : islandState.placements}
            waterColor={isViewingPeer ? (STARTER_PACKS[selectedPeer.northStarCategory]?.waterColor ?? waterColor) : waterColor}
            celebrationActive={isViewingPeer ? false : celebrationActive}
            northStarStatement={peerViewMode !== 'own' || sheetOpen || kudosModalOpen || giftsModalOpen ? undefined : northStar.statement}
          />

          {/* Top overlay */}
          <div className="absolute top-0 left-0 right-0 z-[75] flex items-center justify-between px-4 py-4 md:px-6">
            <button
              onClick={isViewingPeer ? handleBackFromPeer : onBack}
              className="p-2.5 rounded-xl bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 hover:bg-white dark:hover:bg-zinc-800 transition-colors"
            >
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </button>

            {isViewingPeer ? (
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800">
                  <img
                    src={getAvatarUrl(selectedPeer.avatar)}
                    alt={selectedPeer.name}
                    className="w-6 h-6 rounded-full"
                  />
                  <p className="text-xs font-medium text-zinc-600 dark:text-zinc-300 max-w-[120px] truncate">
                    {selectedPeer.name}'s Island
                  </p>
                </div>
                <KudosButton
                  senderUid={user.uid}
                  senderName={user.name}
                  targetUid={selectedPeer.uid}
                  school={user.school || ''}
                  canSendKudosTo={canSendKudosTo}
                  sendKudos={sendKudos}
                />
                <GiftButton
                  senderUid={user.uid}
                  senderName={user.name}
                  targetUid={selectedPeer.uid}
                  targetName={selectedPeer.name}
                  school={user.school || ''}
                  pointsBalance={effectivePoints}
                  canSendGiftToday={canSendGiftToday}
                  sendGift={sendGift}
                  onPointsReload={onPointsReload}
                />
              </div>
            ) : (
              <div />
            )}

            {/* Right side: kudos, gifts, peer islands buttons */}
            {!isViewingPeer && user.school ? (
              <div className="flex items-center gap-2">
                {kudosCount > 0 && (
                  <button
                    onClick={() => setKudosModalOpen(true)}
                    className="relative p-2.5 rounded-xl bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 hover:bg-white dark:hover:bg-zinc-800 transition-colors"
                  >
                    <Heart size={18} className="text-pink-500" fill="currentColor" />
                    <span className="absolute -top-1.5 -right-1.5 min-w-[18px] h-[18px] rounded-full bg-pink-500 text-white text-[9px] font-bold flex items-center justify-center px-1">
                      {kudosCount}
                    </span>
                  </button>
                )}
                {pendingGifts.length > 0 && (
                  <button
                    onClick={() => setGiftsModalOpen(true)}
                    className="relative p-2.5 rounded-xl bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 hover:bg-white dark:hover:bg-zinc-800 transition-colors"
                  >
                    <Gift size={18} className="text-amber-500" />
                    <span className="absolute -top-1.5 -right-1.5 min-w-[18px] h-[18px] rounded-full bg-amber-500 text-white text-[9px] font-bold flex items-center justify-center px-1">
                      {pendingGifts.length}
                    </span>
                  </button>
                )}
                <button
                  onClick={() => setPeerViewMode('peer-list')}
                  className="p-2.5 rounded-xl bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 hover:bg-white dark:hover:bg-zinc-800 transition-colors"
                >
                  <Users size={18} className="text-zinc-900 dark:text-white" />
                </button>
                {/* SOS Flare button */}
                {flaresEnabled !== false && (
                  <MotionDiv
                    animate={{ scale: [1, 1.08, 1] }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                  >
                    <button
                      onClick={() => { setFlareInitialView('launcher'); setFlareSystemOpen(true); }}
                      className="p-2.5 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 backdrop-blur-sm border border-amber-400/50 hover:from-amber-400 hover:to-orange-500 transition-all shadow-lg shadow-amber-500/30"
                      title="SOS Flare"
                    >
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" className="text-white">
                        <path d="M12 2L8 10h8L12 2z" fill="currentColor" />
                        <path d="M12 10v8" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
                        <circle cx="12" cy="21" r="1.5" fill="currentColor" opacity="0.6" />
                        <path d="M5 5l2 2M19 5l-2 2M3 12h3M18 12h3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.5" />
                      </svg>
                    </button>
                  </MotionDiv>
                )}
              </div>
            ) : (
              <div className="w-[42px]" />
            )}
          </div>

          {/* Horizon Glow — shown when active flares exist */}
          <AnimatePresence>
            {activeFlareCount > 0 && flaresEnabled !== false && !isViewingPeer && (
              <MotionDiv
                initial={{ opacity: 0 }}
                animate={{ opacity: [0.3, 0.6, 0.3] }}
                exit={{ opacity: 0 }}
                transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                onClick={() => { setFlareInitialView('feed'); setFlareSystemOpen(true); }}
                className="fixed top-20 left-1/2 -translate-x-1/2 z-[72] cursor-pointer flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-amber-500/80 to-orange-500/80 backdrop-blur-sm shadow-lg shadow-amber-500/20"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="text-white">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" />
                </svg>
                <span className="text-xs font-bold text-white">{activeFlareCount} active</span>
              </MotionDiv>
            )}
          </AnimatePresence>

          {/* Lighthouse Visual — based on rescue count */}
          {!isViewingPeer && flaresEnabled !== false && rescueCount >= 5 && (
            <div className="absolute bottom-28 right-6 z-[71] pointer-events-none flex flex-col items-center">
              {rescueCount >= 30 ? (
                /* Beacon tower — 30+ rescues */
                <MotionDiv
                  animate={{ opacity: [0.7, 1, 0.7] }}
                  transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                  className="flex flex-col items-center"
                >
                  <div className="w-3 h-3 rounded-full bg-amber-400 shadow-lg shadow-amber-400/60 mb-1" />
                  <svg width="24" height="40" viewBox="0 0 24 40" fill="none" className="text-amber-300">
                    <rect x="8" y="8" width="8" height="28" rx="2" fill="currentColor" opacity="0.9" />
                    <rect x="6" y="32" width="12" height="4" rx="1" fill="currentColor" opacity="0.7" />
                    <rect x="9" y="2" width="6" height="8" rx="3" fill="currentColor" />
                  </svg>
                  <p className="text-[9px] font-bold text-amber-400/80 mt-1">{rescueCount} rescues</p>
                </MotionDiv>
              ) : rescueCount >= 15 ? (
                /* Lighthouse — 15-29 rescues */
                <div className="flex flex-col items-center">
                  <svg width="20" height="32" viewBox="0 0 20 32" fill="none" className="text-amber-300">
                    <rect x="7" y="6" width="6" height="22" rx="1.5" fill="currentColor" opacity="0.8" />
                    <rect x="5" y="24" width="10" height="4" rx="1" fill="currentColor" opacity="0.6" />
                    <circle cx="10" cy="4" r="3" fill="currentColor" opacity="0.9" />
                  </svg>
                  <p className="text-[9px] font-bold text-amber-300/70 mt-1">{rescueCount} rescues</p>
                </div>
              ) : (
                /* Small lantern — 5-14 rescues */
                <div className="flex flex-col items-center">
                  <svg width="16" height="20" viewBox="0 0 16 20" fill="none" className="text-yellow-400">
                    <rect x="5" y="6" width="6" height="10" rx="1" fill="currentColor" opacity="0.7" />
                    <circle cx="8" cy="4" r="2.5" fill="currentColor" opacity="0.8" />
                    <rect x="4" y="14" width="8" height="3" rx="1" fill="currentColor" opacity="0.5" />
                  </svg>
                  <p className="text-[9px] font-bold text-yellow-400/60 mt-1">{rescueCount} rescues</p>
                </div>
              )}
            </div>
          )}

          {/* Progress Pill — shown when drawer is closed and viewing own island */}
          <AnimatePresence>
            {!sheetOpen && !isViewingPeer && (
              <JourneyProgressPill
                tileCount={stats.tileCount}
                decoCount={stats.decoCount}
                pointsBalance={effectivePoints}
                onTap={() => setSheetOpen(true)}
              />
            )}
          </AnimatePresence>
        </div>

        {/* Island Shop Drawer — hidden when viewing peer */}
        {!isViewingPeer && (
          <IslandShopDrawer
            isOpen={sheetOpen}
            onClose={() => setSheetOpen(false)}
            items={availableItems}
            pointsBalance={effectivePoints}
            onBuy={handlePurchase}
            hasItem={hasItem}
            milestoneRewards={milestoneRewards}
            onClaimReward={handleClaimReward}
          />
        )}
      </div>

      {/* Purchase Celebration Modal — hidden when viewing peer */}
      {!isViewingPeer && (
        <PurchaseCelebrationModal
          isOpen={purchasedItemName !== null}
          onClose={() => setPurchasedItemName(null)}
          itemName={purchasedItemName}
        />
      )}

      {/* Milestone Reward Celebration Modal — hidden when viewing peer */}
      {!isViewingPeer && (
        <MilestoneRewardModal
          isOpen={rewardModalItem !== null}
          onClose={() => setRewardModalItem(null)}
          itemName={rewardModalItem}
          modulesCompleted={rewardModalModules}
        />
      )}

      {/* Kudos Received Modal */}
      <AnimatePresence>
        {kudosModalOpen && (
          <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[90] bg-black/60 backdrop-blur-sm flex items-center justify-center px-6"
            onClick={() => setKudosModalOpen(false)}
          >
            <MotionDiv
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="bg-white dark:bg-zinc-900 rounded-2xl p-5 w-full max-w-sm shadow-2xl"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold text-zinc-900 dark:text-white">Kudos Received</h3>
                <button onClick={() => setKudosModalOpen(false)} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800">
                  <X size={16} className="text-zinc-400" />
                </button>
              </div>
              {recentKudos.length === 0 ? (
                <p className="text-sm text-zinc-400 text-center py-6">No kudos yet</p>
              ) : (
                <div className="flex flex-col gap-2 max-h-[50vh] overflow-y-auto" style={{ scrollbarWidth: 'none' }}>
                  {recentKudos.map((k, i) => {
                    const msg = getMessageText(k.messageId);
                    const emoji = KUDOS_MESSAGES.find(m => m.id === k.messageId)?.emoji ?? '💬';
                    return (
                      <div key={i} className="flex items-center gap-3 p-3 rounded-xl border border-zinc-200 dark:border-zinc-800">
                        <span className="text-xl">{emoji}</span>
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-medium text-zinc-800 dark:text-zinc-200">{msg}</p>
                          <p className="text-[10px] text-zinc-400 mt-0.5">from {k.fromName}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </MotionDiv>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Pending Gifts Modal */}
      <AnimatePresence>
        {giftsModalOpen && (
          <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[90] bg-black/60 backdrop-blur-sm flex items-center justify-center px-6"
            onClick={() => setGiftsModalOpen(false)}
          >
            <MotionDiv
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="bg-white dark:bg-zinc-900 rounded-2xl p-5 w-full max-w-sm shadow-2xl"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold text-zinc-900 dark:text-white">Pending Gifts</h3>
                <button onClick={() => setGiftsModalOpen(false)} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800">
                  <X size={16} className="text-zinc-400" />
                </button>
              </div>
              {pendingGifts.length === 0 ? (
                <p className="text-sm text-zinc-400 text-center py-6">No pending gifts</p>
              ) : (
                <div className="flex flex-col gap-2 max-h-[50vh] overflow-y-auto" style={{ scrollbarWidth: 'none' }}>
                  {pendingGifts.map(g => (
                    <div key={g.id} className="flex items-center gap-3 p-3 rounded-xl border border-zinc-200 dark:border-zinc-800">
                      <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center shrink-0">
                        <Gift size={18} className="text-amber-600 dark:text-amber-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-medium text-zinc-800 dark:text-zinc-200">{g.itemName}</p>
                        <p className="text-[10px] text-zinc-400 mt-0.5">from {g.fromName}</p>
                      </div>
                      <button
                        onClick={async () => {
                          await placeGiftItem(g.itemId);
                          await markGiftPlaced(g.id);
                          if (pendingGifts.length <= 1) setGiftsModalOpen(false);
                        }}
                        className="shrink-0 px-3 py-1.5 rounded-lg text-[10px] font-bold bg-amber-500 text-white hover:bg-amber-600 transition-colors"
                      >
                        Place on Island
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </MotionDiv>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Peer Islands List Overlay */}
      <PeerIslandsList
        isOpen={peerViewMode === 'peer-list'}
        onClose={() => setPeerViewMode('own')}
        onSelectPeer={handleSelectPeer}
        peers={peers}
        isLoading={peersLoading}
        currentUserIsland={{
          uid: user.uid,
          name: user.name,
          avatar: user.avatar || '',
          islandState,
        }}
      />

      {/* SOS Flare System Modal */}
      <AnimatePresence>
        {flareSystemOpen && (
          <Suspense fallback={null}>
            <FlareSystem
              isOpen={flareSystemOpen}
              onClose={() => {
                setFlareSystemOpen(false);
                // Re-fetch flare count on close
                if (user?.uid && user?.school && subjects?.length && flaresEnabled !== false) {
                  const q = query(
                    collection(db, 'flares'),
                    where('school', '==', user.school),
                    where('status', '==', 'active'),
                  );
                  getDocs(q).then(snap => {
                    const now = new Date();
                    const count = snap.docs.filter(d => {
                      const data = d.data();
                      return data.senderUid !== user.uid
                        && subjects?.includes(data.subject)
                        && data.expiresAt?.toDate() > now;
                    }).length;
                    setActiveFlareCount(count);
                  }).catch(() => {});
                  // Also re-fetch rescue count
                  getDoc(doc(db, 'users', user.uid)).then(userDoc => {
                    if (userDoc.exists()) {
                      setRescueCount(userDoc.data()?.rescueCount ?? 0);
                    }
                  }).catch(() => {});
                }
              }}
              initialView={flareInitialView}
              uid={user.uid}
              school={user.school || ''}
              subjects={subjects || []}
            />
          </Suspense>
        )}
      </AnimatePresence>
    </div>
  );
};

export default JourneyView;
