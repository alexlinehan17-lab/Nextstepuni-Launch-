/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Compass, Trophy, LayoutGrid } from 'lucide-react';
import { PeerIsland } from '../../hooks/usePeerIslands';
import { IslandState } from '../../types';
import { getAvatarUrl } from '../Auth';

const MotionDiv = motion.div as any;

function computeIslandScore(state: IslandState): number {
  const placementCount = state.placements.filter(p => !p.isStarter).length;
  const uniqueItems = new Set(state.purchaseHistory).size;
  return (placementCount * 2) + (uniqueItems * 3);
}

const MEDAL_COLORS = ['text-amber-400', 'text-zinc-300', 'text-amber-700'];

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

  // Compute leaderboard entries (peers + current user), sorted by score
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
          transition={{ duration: 0.2 }}
          className="fixed inset-0 z-[80] bg-zinc-950/95 backdrop-blur-sm flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800">
            <h2 className="text-lg font-semibold text-white">Peer Islands</h2>
            <button
              onClick={onClose}
              className="p-2 rounded-xl hover:bg-zinc-800 transition-colors"
            >
              <X size={20} className="text-zinc-400" />
            </button>
          </div>

          {/* Tab toggle */}
          <div className="flex gap-1 px-5 pt-3 pb-2">
            <button
              onClick={() => setTab('islands')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                tab === 'islands'
                  ? 'bg-white/10 text-white'
                  : 'text-zinc-500 hover:text-zinc-300'
              }`}
            >
              <LayoutGrid size={14} />
              Islands
            </button>
            <button
              onClick={() => setTab('leaderboard')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                tab === 'leaderboard'
                  ? 'bg-white/10 text-white'
                  : 'text-zinc-500 hover:text-zinc-300'
              }`}
            >
              <Trophy size={14} />
              Leaderboard
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto px-5 py-3">
            {isLoading ? (
              <div className="flex items-center justify-center h-40">
                <div className="w-8 h-8 border-2 border-[var(--accent-hex)] border-t-transparent rounded-full animate-spin" />
              </div>
            ) : peers.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-40 text-center">
                <Compass size={32} className="text-zinc-600 mb-3" />
                <p className="text-zinc-400 text-sm">
                  No peers from your school have built an island yet.
                </p>
              </div>
            ) : tab === 'islands' ? (
              /* ── Islands grid ── */
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {peers.map((peer) => {
                  const placementCount = peer.islandState.placements.length;
                  return (
                    <MotionDiv
                      key={peer.uid}
                      whileTap={{ scale: 0.97 }}
                      onClick={() => onSelectPeer(peer)}
                      className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 cursor-pointer hover:border-zinc-600 transition-colors flex flex-col items-center gap-2"
                    >
                      <img
                        src={getAvatarUrl(peer.avatar)}
                        alt={peer.name}
                        className="w-14 h-14 rounded-full bg-zinc-800"
                      />
                      <p className="text-sm font-medium text-white truncate max-w-full">
                        {peer.name}
                      </p>
                      <p className="text-xs text-zinc-500">
                        {placementCount} {placementCount === 1 ? 'piece' : 'pieces'}
                      </p>
                    </MotionDiv>
                  );
                })}
              </div>
            ) : (
              /* ── Leaderboard ── */
              <div className="flex flex-col gap-2">
                {leaderboard.map((entry, idx) => (
                  <MotionDiv
                    key={entry.uid}
                    whileTap={entry.isCurrentUser ? undefined : { scale: 0.98 }}
                    onClick={() => !entry.isCurrentUser && onSelectPeer(entry.peer)}
                    className={`flex items-center gap-3 p-3 rounded-xl border transition-colors ${
                      entry.isCurrentUser
                        ? 'border-[var(--accent-hex)]/30 bg-[rgba(var(--accent),0.08)]'
                        : 'border-zinc-800 bg-zinc-900 cursor-pointer hover:border-zinc-600'
                    }`}
                  >
                    {/* Rank */}
                    <div className="w-8 shrink-0 text-center">
                      {idx < 3 ? (
                        <Trophy size={18} className={MEDAL_COLORS[idx]} fill="currentColor" />
                      ) : (
                        <span className="text-sm font-bold text-zinc-500">{idx + 1}</span>
                      )}
                    </div>

                    {/* Avatar */}
                    <img
                      src={getAvatarUrl(entry.avatar)}
                      alt={entry.name}
                      className="w-9 h-9 rounded-full bg-zinc-800 shrink-0"
                    />

                    {/* Name + pieces */}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white truncate">
                        {entry.name} {entry.isCurrentUser && <span className="text-zinc-500 text-xs">(you)</span>}
                      </p>
                      <p className="text-[10px] text-zinc-500">
                        {entry.placements} {entry.placements === 1 ? 'piece' : 'pieces'} built
                      </p>
                    </div>

                    {/* Score */}
                    <div className="shrink-0 text-right">
                      <p className="text-sm font-bold text-[var(--accent-hex)]">{entry.score}</p>
                      <p className="text-[10px] text-zinc-500">score</p>
                    </div>
                  </MotionDiv>
                ))}
              </div>
            )}
          </div>
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

export default PeerIslandsList;
