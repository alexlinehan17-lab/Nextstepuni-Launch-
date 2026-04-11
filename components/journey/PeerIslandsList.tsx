/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { X, Compass, Trophy, LayoutGrid, Crown } from 'lucide-react';
import { PeerIsland } from '../../hooks/usePeerIslands';
import { IslandState } from '../../types';
import { getAvatarUrl } from '../Auth';

function computeIslandScore(state: IslandState): number {
  const placementCount = state.placements.filter(p => !p.isStarter).length;
  const uniqueItems = new Set(state.purchaseHistory).size;
  return (placementCount * 2) + (uniqueItems * 3);
}

// Bold, saturated Headspace-inspired palette — not pastel
const CARD_PALETTES = [
  { bg: '#F59E0B', light: 'rgba(245,158,11,0.12)', text: '#92400E' },   // amber
  { bg: '#2A7D6F', light: 'rgba(42,125,111,0.12)', text: '#134E45' },   // teal
  { bg: '#6366F1', light: 'rgba(99,102,241,0.12)', text: '#3730A3' },   // indigo
  { bg: '#EC4899', light: 'rgba(236,72,153,0.12)', text: '#9D174D' },   // pink
  { bg: '#F97316', light: 'rgba(249,115,22,0.12)', text: '#9A3412' },   // orange
  { bg: '#8B5CF6', light: 'rgba(139,92,246,0.12)', text: '#5B21B6' },   // purple
  { bg: '#10B981', light: 'rgba(16,185,129,0.12)', text: '#065F46' },   // emerald
  { bg: '#3B82F6', light: 'rgba(59,130,246,0.12)', text: '#1E3A8A' },   // blue
  { bg: '#EF4444', light: 'rgba(239,68,68,0.12)', text: '#991B1B' },    // red
  { bg: '#14B8A6', light: 'rgba(20,184,166,0.12)', text: '#0F766E' },   // teal-light
];

function getCardPalette(name: string) {
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return CARD_PALETTES[Math.abs(hash) % CARD_PALETTES.length];
}

// Podium config
const PODIUM = [
  { label: '1st', bg: '#F59E0B', light: 'rgba(245,158,11,0.10)', border: 'rgba(245,158,11,0.25)', text: '#92400E' },
  { label: '2nd', bg: '#94A3B8', light: 'rgba(148,163,184,0.10)', border: 'rgba(148,163,184,0.25)', text: '#475569' },
  { label: '3rd', bg: '#CD7F32', light: 'rgba(205,127,50,0.10)', border: 'rgba(205,127,50,0.25)', text: '#78350F' },
];

interface PeerIslandsListProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectPeer: (peer: PeerIsland) => void;
  peers: PeerIsland[];
  isLoading: boolean;
  currentUserIsland?: {
    uid: string;
    name: string;
    avatar: string;
    islandState: IslandState;
  };
}

const PeerIslandsList: React.FC<PeerIslandsListProps> = ({
  isOpen, onClose, onSelectPeer, peers, isLoading, currentUserIsland,
}) => {
  const [tab, setTab] = useState<'islands' | 'leaderboard'>('islands');

  const leaderboard = useMemo(() => {
    const entries = peers.map(p => ({
      uid: p.uid,
      name: p.name,
      avatar: p.avatar,
      score: computeIslandScore(p.islandState),
      placements: p.islandState.placements.filter(pl => !pl.isStarter).length,
      isCurrentUser: false,
      peer: p,
    }));
    if (currentUserIsland) {
      entries.push({
        uid: currentUserIsland.uid,
        name: currentUserIsland.name,
        avatar: currentUserIsland.avatar,
        score: computeIslandScore(currentUserIsland.islandState),
        placements: currentUserIsland.islandState.placements.filter(pl => !pl.isStarter).length,
        isCurrentUser: true,
        peer: null as any,
      });
    }
    return entries.sort((a, b) => b.score - a.score);
  }, [peers, currentUserIsland]);

  return (
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.25 }}
          className="fixed inset-0 z-[80] flex flex-col overflow-hidden bg-[#FAF7F4] dark:bg-zinc-900"
        >
          {/* Header */}
          <div className="flex items-center justify-between px-5 pt-5 pb-2">
            <h2 className="text-xl font-serif font-bold text-[#1A1A1A] dark:text-white">
              Peer Islands
            </h2>
            <button
              onClick={onClose}
              className="w-9 h-9 flex items-center justify-center rounded-full transition-colors text-[#78716C] dark:text-zinc-400"
              style={{ backgroundColor: 'rgba(0,0,0,0.05)' }}
            >
              <X size={18} strokeWidth={2} />
            </button>
          </div>

          {/* Tab toggle */}
          <div className="flex gap-1 px-5 pb-4 pt-1">
            {(['islands', 'leaderboard'] as const).map(t => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`flex items-center gap-1.5 px-4 py-2 text-xs font-semibold transition-all ${tab === t ? '' : 'text-[#A8A29E] dark:text-zinc-500'}`}
                style={{
                  borderRadius: 10,
                  backgroundColor: tab === t ? '#2A7D6F' : 'transparent',
                  color: tab === t ? '#FFFFFF' : undefined,
                }}
              >
                {t === 'islands' ? <LayoutGrid size={14} /> : <Trophy size={14} />}
                {t === 'islands' ? 'Islands' : 'Leaderboard'}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto px-5 pb-10">
            {isLoading ? (
              <div className="flex items-center justify-center h-40">
                <div className="w-8 h-8 border-2 border-[#2A7D6F] border-t-transparent rounded-full animate-spin" />
              </div>
            ) : peers.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-40 text-center">
                <div
                  className="w-14 h-14 rounded-full flex items-center justify-center mb-3"
                  style={{ backgroundColor: 'rgba(42,125,111,0.08)' }}
                >
                  <Compass size={28} style={{ color: '#2A7D6F' }} />
                </div>
                <p className="text-sm text-[#78716C] dark:text-zinc-400">
                  No peers from your school have built an island yet.
                </p>
              </div>
            ) : tab === 'islands' ? (
              /* ═══ ISLANDS GRID ═══ */
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {peers.map((peer, i) => {
                  const placementCount = peer.islandState.placements.length;
                  const palette = getCardPalette(peer.name);
                  return (
                    <MotionDiv
                      key={peer.uid}
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.04, duration: 0.4, ease: [0.25, 1, 0.5, 1] }}
                      whileTap={{ scale: 0.97 }}
                      onClick={() => onSelectPeer(peer)}
                      className="cursor-pointer relative overflow-hidden"
                      style={{
                        borderRadius: 18,
                        backgroundColor: palette.bg,
                        boxShadow: `0 4px 16px ${palette.bg}25`,
                        transition: 'box-shadow 0.3s, transform 0.3s',
                      }}
                      onMouseEnter={(e: React.MouseEvent<HTMLDivElement>) => {
                        e.currentTarget.style.boxShadow = `0 8px 28px ${palette.bg}35`;
                        e.currentTarget.style.transform = 'translateY(-2px)';
                      }}
                      onMouseLeave={(e: React.MouseEvent<HTMLDivElement>) => {
                        e.currentTarget.style.boxShadow = `0 4px 16px ${palette.bg}25`;
                        e.currentTarget.style.transform = 'translateY(0)';
                      }}
                    >
                      {/* Decorative blobs */}
                      <div
                        className="absolute pointer-events-none"
                        style={{
                          top: -30, right: -20,
                          width: 100, height: 100,
                          borderRadius: '50%',
                          background: 'rgba(255,255,255,0.12)',
                        }}
                      />
                      <div
                        className="absolute pointer-events-none"
                        style={{
                          bottom: -20, left: -15,
                          width: 70, height: 70,
                          borderRadius: '50%',
                          background: 'rgba(0,0,0,0.06)',
                        }}
                      />
                      <div
                        className="absolute pointer-events-none"
                        style={{
                          top: 20, right: 30,
                          width: 35, height: 35,
                          borderRadius: '50%',
                          background: 'rgba(255,255,255,0.08)',
                        }}
                      />

                      {/* Card content */}
                      <div className="relative z-10 px-5 pt-5 pb-4 flex flex-col items-center">
                        {/* Avatar — prominent, overlapping slightly */}
                        <div
                          className="w-[68px] h-[68px] rounded-full flex items-center justify-center mb-3"
                          style={{
                            backgroundColor: 'rgba(255,255,255,0.25)',
                            border: '2.5px solid rgba(255,255,255,0.4)',
                          }}
                        >
                          <img
                            src={getAvatarUrl(peer.avatar)}
                            alt={peer.name}
                            className="w-14 h-14 rounded-full"
                          />
                        </div>

                        <p className="text-[15px] font-bold text-white truncate max-w-full mb-1">
                          {peer.name}
                        </p>

                        {/* Pieces pill */}
                        <span
                          className="inline-flex items-center px-2.5 py-0.5 text-[11px] font-semibold"
                          style={{
                            borderRadius: 8,
                            backgroundColor: 'rgba(255,255,255,0.2)',
                            color: 'rgba(255,255,255,0.85)',
                          }}
                        >
                          {placementCount} {placementCount === 1 ? 'piece' : 'pieces'}
                        </span>
                      </div>
                    </MotionDiv>
                  );
                })}
              </div>
            ) : (
              /* ═══ LEADERBOARD ═══ */
              <div>
                {/* Top 3 — podium cards */}
                {leaderboard.length >= 3 && (
                  <div className="flex gap-3 mb-5 items-end">
                    {/* 2nd place — left */}
                    {(() => {
                      const entry = leaderboard[1];
                      const p = PODIUM[1];
                      return (
                        <MotionDiv
                          key={entry.uid}
                          initial={{ opacity: 0, y: 15 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.1, duration: 0.4, ease: [0.25, 1, 0.5, 1] }}
                          onClick={() => !entry.isCurrentUser && onSelectPeer(entry.peer)}
                          className="flex-1 relative overflow-hidden text-center"
                          style={{
                            borderRadius: 16,
                            backgroundColor: p.light,
                            border: `1.5px solid ${p.border}`,
                            cursor: entry.isCurrentUser ? 'default' : 'pointer',
                            paddingTop: 20, paddingBottom: 16,
                          }}
                        >
                          <div className="absolute pointer-events-none" style={{ top: -15, right: -10, width: 50, height: 50, borderRadius: '50%', background: p.border }} />
                          <span className="text-[11px] font-bold" style={{ color: p.bg }}>2nd</span>
                          <div className="w-12 h-12 rounded-full mx-auto mt-2 mb-1.5 flex items-center justify-center" style={{ backgroundColor: `${p.bg}20`, border: `2px solid ${p.bg}40` }}>
                            <img src={getAvatarUrl(entry.avatar)} alt={entry.name} className="w-9 h-9 rounded-full" />
                          </div>
                          <p className="text-xs font-bold truncate px-2 text-[#1A1A1A] dark:text-white">{entry.name}</p>
                          <span className="inline-flex items-center px-2 py-0.5 mt-1 text-[10px] font-bold" style={{ borderRadius: 6, backgroundColor: `${p.bg}15`, color: p.bg }}>{entry.score}</span>
                        </MotionDiv>
                      );
                    })()}

                    {/* 1st place — center, taller */}
                    {(() => {
                      const entry = leaderboard[0];
                      const p = PODIUM[0];
                      return (
                        <MotionDiv
                          key={entry.uid}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.05, duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
                          onClick={() => !entry.isCurrentUser && onSelectPeer(entry.peer)}
                          className="flex-1 relative overflow-hidden text-center"
                          style={{
                            borderRadius: 18,
                            backgroundColor: p.bg,
                            boxShadow: `0 6px 24px ${p.bg}30`,
                            cursor: entry.isCurrentUser ? 'default' : 'pointer',
                            paddingTop: 18, paddingBottom: 18,
                            marginBottom: -8,
                          }}
                        >
                          {/* Blobs */}
                          <div className="absolute pointer-events-none" style={{ top: -20, right: -15, width: 70, height: 70, borderRadius: '50%', background: 'rgba(255,255,255,0.12)' }} />
                          <div className="absolute pointer-events-none" style={{ bottom: -10, left: -10, width: 50, height: 50, borderRadius: '50%', background: 'rgba(0,0,0,0.06)' }} />

                          <div className="relative z-10">
                            <Crown size={18} style={{ color: 'rgba(255,255,255,0.7)' }} className="mx-auto mb-1" />
                            <div className="w-16 h-16 rounded-full mx-auto mb-2 flex items-center justify-center" style={{ backgroundColor: 'rgba(255,255,255,0.25)', border: '2.5px solid rgba(255,255,255,0.4)' }}>
                              <img src={getAvatarUrl(entry.avatar)} alt={entry.name} className="w-12 h-12 rounded-full" />
                            </div>
                            <p className="text-sm font-bold text-white truncate px-2">{entry.name}</p>
                            <span className="inline-flex items-center px-3 py-0.5 mt-1.5 text-xs font-bold" style={{ borderRadius: 8, backgroundColor: 'rgba(255,255,255,0.2)', color: '#fff' }}>{entry.score}</span>
                          </div>
                        </MotionDiv>
                      );
                    })()}

                    {/* 3rd place — right */}
                    {(() => {
                      const entry = leaderboard[2];
                      const p = PODIUM[2];
                      return (
                        <MotionDiv
                          key={entry.uid}
                          initial={{ opacity: 0, y: 15 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.15, duration: 0.4, ease: [0.25, 1, 0.5, 1] }}
                          onClick={() => !entry.isCurrentUser && onSelectPeer(entry.peer)}
                          className="flex-1 relative overflow-hidden text-center"
                          style={{
                            borderRadius: 16,
                            backgroundColor: p.light,
                            border: `1.5px solid ${p.border}`,
                            cursor: entry.isCurrentUser ? 'default' : 'pointer',
                            paddingTop: 20, paddingBottom: 16,
                          }}
                        >
                          <div className="absolute pointer-events-none" style={{ top: -12, left: -8, width: 45, height: 45, borderRadius: '50%', background: p.border }} />
                          <span className="text-[11px] font-bold" style={{ color: p.bg }}>3rd</span>
                          <div className="w-12 h-12 rounded-full mx-auto mt-2 mb-1.5 flex items-center justify-center" style={{ backgroundColor: `${p.bg}20`, border: `2px solid ${p.bg}40` }}>
                            <img src={getAvatarUrl(entry.avatar)} alt={entry.name} className="w-9 h-9 rounded-full" />
                          </div>
                          <p className="text-xs font-bold truncate px-2 text-[#1A1A1A] dark:text-white">{entry.name}</p>
                          <span className="inline-flex items-center px-2 py-0.5 mt-1 text-[10px] font-bold" style={{ borderRadius: 6, backgroundColor: `${p.bg}15`, color: p.bg }}>{entry.score}</span>
                        </MotionDiv>
                      );
                    })()}
                  </div>
                )}

                {/* Remaining positions (4+) */}
                <div className="flex flex-col gap-2">
                  {leaderboard.slice(3).map((entry, i) => {
                    const idx = i + 3;
                    const palette = getCardPalette(entry.name);
                    const isYou = entry.isCurrentUser;
                    return (
                      <MotionDiv
                        key={entry.uid}
                        initial={{ opacity: 0, x: -6 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 + i * 0.03, duration: 0.3, ease: [0.25, 1, 0.5, 1] }}
                        whileTap={isYou ? undefined : { scale: 0.98 }}
                        onClick={() => !isYou && onSelectPeer(entry.peer)}
                        className={`flex items-center gap-3 px-4 py-3 ${isYou ? '' : 'bg-[#FAF7F4] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800'}`}
                        style={{
                          borderRadius: 14,
                          ...(isYou ? {
                            backgroundColor: 'rgba(42,125,111,0.08)',
                            border: '2px solid rgba(42,125,111,0.25)',
                            borderLeft: '4px solid #2A7D6F',
                            boxShadow: '0 2px 8px rgba(42,125,111,0.08)',
                          } : {
                            boxShadow: '0 1px 3px rgba(28,25,23,0.03)',
                          }),
                          cursor: isYou ? 'default' : 'pointer',
                        }}
                      >
                        <span className="w-7 text-center text-[13px] font-semibold shrink-0" style={{ color: '#C4C0BC' }}>{idx + 1}</span>

                        <div
                          className="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
                          style={{ backgroundColor: palette.light, border: `1.5px solid ${palette.bg}30` }}
                        >
                          <img src={getAvatarUrl(entry.avatar)} alt={entry.name} className="w-8 h-8 rounded-full" />
                        </div>

                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold truncate text-[#1A1A1A] dark:text-white">
                            {entry.name}
                            {isYou && <span className="text-[11px] font-bold ml-1.5" style={{ color: '#2A7D6F' }}>you</span>}
                          </p>
                          <p className="text-[11px] text-[#A8A29E] dark:text-zinc-500">
                            {entry.placements} {entry.placements === 1 ? 'piece' : 'pieces'} built
                          </p>
                        </div>

                        <span
                          className="shrink-0 px-2.5 py-1 text-sm font-bold"
                          style={{
                            borderRadius: 8,
                            backgroundColor: isYou ? 'rgba(42,125,111,0.1)' : palette.light,
                            color: isYou ? '#2A7D6F' : palette.text,
                          }}
                        >
                          {entry.score}
                        </span>
                      </MotionDiv>
                    );
                  })}

                  {/* If current user is in top 3, show them highlighted below the podium too */}
                  {leaderboard.slice(0, 3).some(e => e.isCurrentUser) && (
                    (() => {
                      const you = leaderboard.find(e => e.isCurrentUser);
                      if (!you) return null;
                      const yourIdx = leaderboard.indexOf(you);
                      return (
                        <MotionDiv
                          key="you-highlight"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.3, duration: 0.3 }}
                          className="flex items-center gap-3 px-4 py-3 mt-1"
                          style={{
                            borderRadius: 14,
                            backgroundColor: 'rgba(42,125,111,0.08)',
                            border: '2px solid rgba(42,125,111,0.25)',
                            borderLeft: '4px solid #2A7D6F',
                          }}
                        >
                          <span className="w-7 text-center text-[13px] font-bold shrink-0" style={{ color: '#2A7D6F' }}>{yourIdx + 1}</span>
                          <div className="w-10 h-10 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(42,125,111,0.12)' }}>
                            <img src={getAvatarUrl(you.avatar)} alt={you.name} className="w-8 h-8 rounded-full" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-semibold text-[#1A1A1A] dark:text-white">
                              {you.name} <span className="text-[11px] font-bold" style={{ color: '#2A7D6F' }}>you</span>
                            </p>
                            <p className="text-[11px] text-[#A8A29E] dark:text-zinc-500">{you.placements} pieces built</p>
                          </div>
                          <span className="px-2.5 py-1 text-sm font-bold" style={{ borderRadius: 8, backgroundColor: 'rgba(42,125,111,0.1)', color: '#2A7D6F' }}>{you.score}</span>
                        </MotionDiv>
                      );
                    })()
                  )}
                </div>
              </div>
            )}
          </div>
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

export default PeerIslandsList;
