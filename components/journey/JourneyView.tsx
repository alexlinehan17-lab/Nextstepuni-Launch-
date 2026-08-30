/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useCallback, useRef, useEffect, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, Mountain, Users, Heart, Gift, X, Hammer, RotateCw, Check, PackageOpen } from 'lucide-react';
import { type SessionUser } from '../../utils/authUtils';
import { type IslandPlacement, type NorthStar, type ShopItem, type UserProgress } from '../../types';
import { type MilestoneReward } from '../../islandShopData';

import { useIslandShop, type EnrichedShopItem } from '../../hooks/useIslandShop';
import JourneyCanvas from './JourneyCanvas';
import JourneyProgressPill from './JourneyProgressPill';
import IslandShopDrawer from './IslandShopDrawer';
import PurchaseCelebrationModal from './PurchaseCelebrationModal';
import MilestoneRewardModal from './MilestoneRewardModal';
import PeerIslandsList from './PeerIslandsList';
import KudosButton from './KudosButton';
import GiftButton from './GiftButton';
import { usePeerIslands, type PeerIsland } from '../../hooks/usePeerIslands';
import { useKudos } from '../../hooks/useKudos';
import { useGifts } from '../../hooks/useGifts';
import { KUDOS_MESSAGES } from '../../kudosData';
import { STARTER_PACKS } from '../../islandShopData';
import { getAvatarUrl } from '../../utils/authUtils';
import { getBuildCells, type BuildCell } from './build/islandBuildModel';
import { getPlacementRules } from '../../services/islandStateMigration';
import { getJourneyProgress } from '../../journeyProgression';

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
}

const JourneyView: React.FC<JourneyViewProps> = ({
  onBack, user, northStar, onOpenNorthStar, pointsBalance, onPointsReload,
  userProgress, allCourses,
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
    purchaseItemAt,
    updatePlacement,
    storePlacement,
    placeInventoryItem,
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
  const [buildMode, setBuildMode] = useState(false);
  const [pendingItem, setPendingItem] = useState<EnrichedShopItem | null>(null);
  const [pendingInventoryId, setPendingInventoryId] = useState<string | null>(null);
  const [selectedCell, setSelectedCell] = useState<BuildCell | null>(null);
  const [selectedPlacement, setSelectedPlacement] = useState<IslandPlacement | null>(null);
  const [buildRotation, setBuildRotation] = useState(0);
  const [buildMessage, setBuildMessage] = useState<string | null>(null);

  // Peer Islands state
  type PeerViewMode = 'own' | 'peer-list' | 'peer-island';
  const [peerViewMode, setPeerViewMode] = useState<PeerViewMode>('own');
  const [selectedPeer, setSelectedPeer] = useState<PeerIsland | null>(null);
  const { peers, isLoading: peersLoading } = usePeerIslands(user.uid, user.school);
  const { kudosCount, recentKudos, canSendKudosTo, sendKudos, getMessageText } = useKudos(user.uid);
  const { pendingGifts, canSendGiftToday, sendGift, markGiftPlaced } = useGifts(user.uid);

  const [kudosModalOpen, setKudosModalOpen] = useState(false);
  const [giftsModalOpen, setGiftsModalOpen] = useState(false);

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
  const journeyProgression = useMemo(() => getJourneyProgress({
    completedModules: completedCount,
    nonStarterPlacements: islandState?.placements.filter(placement => !placement.isStarter).length ?? 0,
    claimedRewards: islandState?.claimedRewards?.length ?? 0,
    inventoryItems: islandState?.inventory?.length ?? 0,
  }), [completedCount, islandState?.placements, islandState?.claimedRewards, islandState?.inventory]);

  const beginPlacement = useCallback((item: EnrichedShopItem, inventoryId?: string) => {
    setPendingItem(item);
    setPendingInventoryId(inventoryId ?? null);
    setSelectedPlacement(null);
    setSelectedCell(null);
    setBuildRotation(0);
    setBuildMessage('Choose a highlighted tile');
    setSheetOpen(false);
    setBuildMode(true);
  }, []);

  const handlePurchase = useCallback((item: EnrichedShopItem) => {
    beginPlacement(item);
  }, [beginPlacement]);

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

  const selectedPlacementItem = useMemo<ShopItem | null>(() => {
    if (!selectedPlacement) return null;
    return availableItems.find(item => item.id === selectedPlacement.itemId)
      ?? milestoneRewards.map(entry => entry.reward.item).find(item => item.id === selectedPlacement.itemId)
      ?? null;
  }, [selectedPlacement, availableItems, milestoneRewards]);

  const activeBuildItem = pendingItem ?? selectedPlacementItem;
  const placementState = useMemo(() => {
    if (!selectedPlacement || !islandState) return islandState;
    return {
      ...islandState,
      placements: islandState.placements.filter(p => p.placementId !== selectedPlacement.placementId),
    };
  }, [islandState, selectedPlacement]);
  const buildCells = useMemo(() => {
    if (!buildMode || !placementState || !activeBuildItem) return [];
    return getBuildCells(placementState, activeBuildItem);
  }, [buildMode, placementState, activeBuildItem]);

  const previewPlacement = useMemo<IslandPlacement | null>(() => {
    if (!activeBuildItem || !selectedCell?.valid) return null;
    return {
      placementId: 'build-preview',
      itemId: activeBuildItem.id,
      model: activeBuildItem.model,
      type: activeBuildItem.type,
      layer: getPlacementRules(activeBuildItem).layer,
      q: selectedCell.q,
      r: selectedCell.r,
      rotation: buildRotation,
      ...(activeBuildItem.type === 'decoration' ? { scale: activeBuildItem.defaultScale ?? 0.5 } : {}),
    };
  }, [activeBuildItem, selectedCell, buildRotation]);

  const exitBuildMode = useCallback(() => {
    setBuildMode(false);
    setPendingItem(null);
    setPendingInventoryId(null);
    setSelectedPlacement(null);
    setSelectedCell(null);
    setBuildMessage(null);
    setBuildRotation(0);
  }, []);

  const handleSelectBuildCell = useCallback((cell: BuildCell) => {
    setBuildMessage(cell.valid
      ? cell.recommended
        ? 'Great fit — rotate it or confirm'
        : 'This works here — rotate it or confirm'
      : (cell.reason ?? 'This tile is unavailable'));
    if (cell.valid) setSelectedCell(cell);
  }, []);

  const handleSelectOwnedPlacement = useCallback((placement: IslandPlacement) => {
    if (!buildMode || placement.isStarter || placement.layer === 'terrain') return;
    const item = availableItems.find(entry => entry.id === placement.itemId)
      ?? milestoneRewards.map(entry => entry.reward.item).find(entry => entry.id === placement.itemId);
    if (!item) {
      setBuildMessage('This legacy object cannot be moved yet');
      return;
    }
    setPendingItem(null);
    setPendingInventoryId(null);
    setSelectedPlacement(placement);
    setSelectedCell({ q: placement.q, r: placement.r, valid: true, terrain: 'unknown' });
    setBuildRotation(placement.rotation ?? 0);
    setBuildMessage('Move, rotate or put this object away');
  }, [buildMode, availableItems, milestoneRewards]);

  const confirmBuildPlacement = useCallback(async () => {
    if (!selectedCell?.valid || !activeBuildItem) return;
    let success = false;
    if (selectedPlacement?.placementId) {
      success = await updatePlacement(selectedPlacement.placementId, {
        q: selectedCell.q,
        r: selectedCell.r,
        rotation: buildRotation,
      });
    } else if (pendingInventoryId) {
      success = await placeInventoryItem(pendingInventoryId, selectedCell.q, selectedCell.r, buildRotation);
    } else if (pendingItem) {
      success = await purchaseItemAt(pendingItem, effectivePoints, selectedCell.q, selectedCell.r, buildRotation);
      if (success) onPointsReload();
    }
    if (!success) {
      setBuildMessage('That placement could not be saved. Try another tile.');
      return;
    }
    setCelebrationActive(true);
    setTimeout(() => setCelebrationActive(false), 1800);
    if (pendingItem && !pendingInventoryId) setPurchasedItemName(pendingItem.name);
    setPendingItem(null);
    setPendingInventoryId(null);
    setSelectedPlacement(null);
    setSelectedCell(null);
    setBuildMessage('Placed. Choose another object or finish building.');
  }, [selectedCell, activeBuildItem, selectedPlacement, pendingInventoryId, pendingItem, updatePlacement, placeInventoryItem, purchaseItemAt, effectivePoints, onPointsReload]);

  // No North Star set
  if (!northStar) {
    return (
      <div className="min-h-screen bg-[#FAFBF6] px-5 pb-28 pt-5 text-left dark:bg-zinc-950 sm:px-8 sm:pt-8">
        <button
          type="button"
          onClick={onBack}
          aria-label="Back to home"
          className="inline-flex h-11 w-11 items-center justify-center rounded-xl border-[1.5px] border-[#383838] bg-white text-[#1A1A1A] shadow-[2px_2px_0_0_#383838] dark:border-zinc-600 dark:bg-zinc-900 dark:text-white"
        >
          <ArrowLeft size={18} aria-hidden="true" />
        </button>
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mx-auto mt-8 grid max-w-5xl items-center gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:gap-16"
        >
          <div className="overflow-hidden rounded-[24px] border-[1.5px] border-[#383838] bg-white p-2 shadow-[5px_5px_0_0_#383838] dark:border-zinc-600 dark:bg-zinc-900">
            <img
              src="/assets/guide/journey.jpg"
              alt="My Journey island preview from the app"
              className="aspect-[16/10] w-full rounded-[18px] object-cover object-top"
            />
          </div>
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#B94712] dark:text-orange-300">My Journey</p>
            <h1 className="mt-3 max-w-xl font-serif text-4xl font-semibold leading-[1.05] tracking-tight text-[#1A1A1A] dark:text-white sm:text-5xl">Build a world around what matters to you.</h1>
            <p className="mt-5 max-w-lg text-base leading-relaxed text-zinc-600 dark:text-zinc-400">Choose a North Star—the reason you want to keep going—and your progress will begin shaping an island of your own.</p>
            <ul className="mt-6 space-y-3 text-sm text-zinc-700 dark:text-zinc-300">
              {['Turn study and module progress into Journey Points.', 'Unlock details that make the island feel like yours.', 'Keep your goal visible when motivation dips.'].map(item => (
                <li key={item} className="flex items-start gap-3"><Check size={17} className="mt-0.5 shrink-0 text-[#F26B1F]" aria-hidden="true" />{item}</li>
              ))}
            </ul>
            <div className="mt-8 flex flex-wrap gap-3">
              <button
                onClick={onOpenNorthStar}
                className="inline-flex min-h-12 items-center gap-2 rounded-xl border-[1.5px] border-[#1A1A1A] bg-[#F26B1F] px-6 text-sm font-semibold text-white shadow-[3px_3px_0_0_#1A1A1A] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none"
              >
                Choose my North Star
                <Mountain size={16} aria-hidden="true" />
              </button>
              <button onClick={onBack} className="min-h-12 rounded-xl px-5 text-sm font-semibold text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-900">Back to home</button>
            </div>
          </div>
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
            placements={isViewingPeer
              ? selectedPeer.islandState.placements
              : selectedPlacement?.placementId
                ? islandState.placements.filter(p => p.placementId !== selectedPlacement.placementId)
                : islandState.placements}
            waterColor={isViewingPeer ? (STARTER_PACKS[selectedPeer.northStarCategory]?.waterColor ?? waterColor) : waterColor}
            celebrationActive={isViewingPeer ? false : celebrationActive}
            northStarStatement={peerViewMode !== 'own' || sheetOpen || kudosModalOpen || giftsModalOpen ? undefined : northStar.statement}
            buildMode={buildMode && !isViewingPeer}
            buildCells={buildCells}
            selectedCell={selectedCell}
            previewPlacement={previewPlacement}
            selectedPlacementId={selectedPlacement?.placementId}
            onSelectCell={handleSelectBuildCell}
            onSelectPlacement={handleSelectOwnedPlacement}
          />

          {peerViewMode === 'own' && !sheetOpen && !kudosModalOpen && !giftsModalOpen && (
            <div className="pointer-events-none absolute left-1/2 top-[76px] z-[74] w-[calc(100%-32px)] max-w-sm -translate-x-1/2 rounded-2xl border border-white/20 bg-[#171824]/72 px-4 py-3 text-center text-white shadow-lg backdrop-blur-md sm:hidden">
              <p className="text-[9px] font-bold uppercase tracking-[0.18em] text-orange-200">My Journey · {journeyProgression.stage.name}</p>
              <p className="mt-1 line-clamp-2 font-serif text-sm font-semibold leading-snug">{northStar.statement}</p>
            </div>
          )}

          {/* Top overlay */}
          <div
            className="absolute top-0 left-0 right-0 z-[75] flex items-center justify-between gap-4 py-4 md:px-6"
            style={{
              paddingLeft: 'calc(20px + var(--sal, 0px))',
              paddingRight: 'calc(20px + var(--sar, 0px))',
            }}
          >
            <button
              type="button"
              onClick={isViewingPeer ? handleBackFromPeer : onBack}
              aria-label={isViewingPeer ? 'Back to my island' : 'Back to home'}
              className="flex h-11 w-11 items-center justify-center rounded-xl border border-zinc-200 bg-white/90 backdrop-blur-sm transition-colors hover:bg-white dark:border-zinc-800 dark:bg-zinc-900/90 dark:hover:bg-zinc-800"
            >
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </button>

            {isViewingPeer ? (
              <div className="flex min-w-0 items-center gap-2">
                <div className="hidden min-w-0 items-center gap-2 px-3 py-1.5 rounded-full bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 sm:flex">
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
            {!isViewingPeer ? (
              <div className="flex shrink-0 items-center gap-2 sm:gap-3">
                <button
                  type="button"
                  onClick={() => buildMode ? exitBuildMode() : setBuildMode(true)}
                  aria-label={buildMode ? 'Finish building' : 'Build island'}
                  className={`flex h-11 min-w-11 items-center justify-center gap-2 rounded-xl border px-3 backdrop-blur-sm transition-colors ${
                    buildMode
                      ? 'bg-[#F26B1F] border-[#F26B1F] text-white'
                      : 'bg-white/90 dark:bg-zinc-900/90 border-zinc-200 dark:border-zinc-800 text-zinc-900 dark:text-white'
                  }`}
                >
                  <Hammer size={17} />
                  <span className="hidden sm:inline text-xs font-bold">{buildMode ? 'Finish' : 'Build'}</span>
                </button>
                {user.school && <>
                {kudosCount > 0 && (
                  <button
                    type="button"
                    onClick={() => setKudosModalOpen(true)}
                    aria-label={`Open ${kudosCount} kudos`}
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
                    type="button"
                    onClick={() => setGiftsModalOpen(true)}
                    aria-label={`Open ${pendingGifts.length} pending gifts`}
                    className="relative p-2.5 rounded-xl bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 hover:bg-white dark:hover:bg-zinc-800 transition-colors"
                  >
                    <Gift size={18} className="text-amber-500" />
                    <span className="absolute -top-1.5 -right-1.5 min-w-[18px] h-[18px] rounded-full bg-amber-500 text-white text-[9px] font-bold flex items-center justify-center px-1">
                      {pendingGifts.length}
                    </span>
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => setPeerViewMode('peer-list')}
                  aria-label="View classmates' islands"
                  className="p-2.5 rounded-xl bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200 dark:border-zinc-800 hover:bg-white dark:hover:bg-zinc-800 transition-colors"
                >
                  <Users size={18} className="text-zinc-900 dark:text-white" />
                </button>
                </>}
              </div>
            ) : (
              <div className="w-[42px]" />
            )}
          </div>

          <AnimatePresence>
            {buildMode && !isViewingPeer && (
              <MotionDiv
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 18 }}
                transition={{ type: 'spring', stiffness: 280, damping: 28 }}
                className="absolute z-[80] left-4 right-4 bottom-5 mx-auto max-w-2xl rounded-[22px] border-2 border-[#343230] bg-[#FFFDF8]/95 px-4 py-3 shadow-[0_7px_0_#343230] backdrop-blur-md dark:bg-[#201F1D]/95"
              >
                <div className="flex flex-wrap items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-[#FDE8DB] text-[#C94F10] flex items-center justify-center shrink-0 dark:bg-[#4A291D] dark:text-[#FF9A62]">
                    {activeBuildItem ? <Hammer size={19} /> : <PackageOpen size={19} />}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-bold text-[#242220] dark:text-[#F5F1E8] truncate">
                      {activeBuildItem?.name ?? 'Build Mode'}
                    </p>
                    <p className="text-xs text-[#756F69] dark:text-[#B8B1A8] truncate">
                      {buildMessage ?? 'Open the shop or select an object to arrange your island'}
                    </p>
                  </div>
                  <div className="ml-auto flex shrink-0 items-center gap-2">
                  {activeBuildItem && (
                    <button
                      onClick={() => setBuildRotation(rotation => (rotation + 1) % 6)}
                      className="p-2.5 rounded-xl border border-[#D8D1C8] text-[#343230] hover:bg-[#F4EFE8] dark:border-[#57524C] dark:text-[#F5F1E8] dark:hover:bg-[#302E2B]"
                      aria-label="Rotate object"
                    >
                      <RotateCw size={18} />
                    </button>
                  )}
                  {selectedPlacement && !selectedPlacement.isStarter && (
                    <button
                      onClick={async () => {
                        if (!selectedPlacement.placementId) return;
                        const success = await storePlacement(selectedPlacement.placementId);
                        if (success) {
                          setSelectedPlacement(null);
                          setSelectedCell(null);
                          setBuildMessage('Object moved to your unplaced items');
                        }
                      }}
                      className="px-3 py-2.5 rounded-xl border border-[#D8D1C8] text-xs font-bold text-[#343230] dark:border-[#57524C] dark:text-[#F5F1E8]"
                    >
                      Put away
                    </button>
                  )}
                  {previewPlacement && (
                    <button
                      onClick={confirmBuildPlacement}
                      className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-[#F26B1F] text-white text-xs font-bold border-2 border-[#343230] shadow-[0_3px_0_#343230] active:translate-y-[2px] active:shadow-[0_1px_0_#343230]"
                    >
                      <Check size={16} /> Confirm
                    </button>
                  )}
                  {!activeBuildItem && (
                    <button
                      onClick={() => setSheetOpen(true)}
                      className="px-4 py-2.5 rounded-xl bg-[#F26B1F] text-white text-xs font-bold border-2 border-[#343230] shadow-[0_3px_0_#343230]"
                    >
                      Open shop
                    </button>
                  )}
                  {activeBuildItem && (
                    <button
                      onClick={() => {
                        setPendingItem(null);
                        setPendingInventoryId(null);
                        setSelectedPlacement(null);
                        setSelectedCell(null);
                        setBuildMessage('Selection cancelled');
                      }}
                      className="p-2 text-[#756F69] dark:text-[#B8B1A8]"
                      aria-label="Cancel placement"
                    >
                      <X size={18} />
                    </button>
                  )}
                  </div>
                </div>
                {(islandState.inventory?.length ?? 0) > 0 && !activeBuildItem && (
                  <div className="mt-3 pt-3 border-t border-[#E5DED5] dark:border-[#403D39] flex gap-2 overflow-x-auto">
                    {islandState.inventory!.map(entry => {
                      const item = availableItems.find(candidate => candidate.id === entry.itemId)
                        ?? milestoneRewards.map(candidate => candidate.reward.item).find(candidate => candidate.id === entry.itemId);
                      if (!item) return null;
                      return (
                        <button
                          key={entry.inventoryId}
                          onClick={() => beginPlacement(item as EnrichedShopItem, entry.inventoryId)}
                          className="shrink-0 px-3 py-2 rounded-xl border border-[#D8D1C8] bg-white text-xs font-semibold text-[#343230] dark:bg-[#2A2825] dark:border-[#57524C] dark:text-[#F5F1E8]"
                        >
                          {item.name}
                        </button>
                      );
                    })}
                  </div>
                )}
              </MotionDiv>
            )}
          </AnimatePresence>

          {/* Progress Pill — shown when drawer is closed and viewing own island */}
          <AnimatePresence>
            {!sheetOpen && !isViewingPeer && !buildMode && (
              <JourneyProgressPill
                tileCount={stats.tileCount}
                decoCount={stats.decoCount}
                pointsBalance={effectivePoints}
                stageName={journeyProgression.stage.name}
                stageProgress={journeyProgression.progress}
                nextStageName={journeyProgression.nextStage?.name}
                modulesToNext={journeyProgression.modulesToNext}
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
            progression={journeyProgression}
            onOpenBuildMode={() => {
              setSheetOpen(false);
              setBuildMode(true);
              setBuildMessage('Choose an item from your Build Tray');
            }}
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
          onClose={() => {
            setRewardModalItem(null);
            setSheetOpen(false);
            setBuildMode(true);
            setBuildMessage('Your reward is waiting in the Build Tray');
          }}
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
                        Add to Build Tray
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

    </div>
  );
};

export default JourneyView;
