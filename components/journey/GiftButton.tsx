/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Gift, X, Check } from 'lucide-react';
import { ShopItem } from '../../types';
import { GIFTABLE_ITEMS } from '../../hooks/useGifts';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

interface GiftButtonProps {
  senderUid: string;
  senderName: string;
  targetUid: string;
  targetName: string;
  school: string;
  pointsBalance: number;
  canSendGiftToday: () => Promise<boolean>;
  sendGift: (toUid: string, school: string, item: ShopItem, fromName: string) => Promise<boolean>;
  onPointsReload: () => void;
}

const GiftButton: React.FC<GiftButtonProps> = ({
  senderUid, senderName, targetUid, targetName, school,
  pointsBalance, canSendGiftToday, sendGift, onPointsReload,
}) => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [canSend, setCanSend] = useState(true);
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);
  const [sentItemName, setSentItemName] = useState('');
  const sentTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (sentTimerRef.current) clearTimeout(sentTimerRef.current);
    };
  }, []);

  useEffect(() => {
    canSendGiftToday().then(setCanSend);
  }, [canSendGiftToday]);

  const handleSend = async (item: ShopItem) => {
    if (sending || pointsBalance < item.price) return;
    setSending(true);
    const success = await sendGift(targetUid, school, item, senderName);
    setSending(false);
    if (success) {
      setSent(true);
      setSentItemName(item.name);
      setCanSend(false);
      onPointsReload();
      sentTimerRef.current = setTimeout(() => { setDrawerOpen(false); setSent(false); }, 1500);
    }
  };

  return (
    <>
      <button
        onClick={() => canSend && setDrawerOpen(true)}
        disabled={!canSend}
        className={`p-2.5 rounded-xl backdrop-blur-sm border transition-colors ${
          canSend
            ? 'bg-white/90 dark:bg-zinc-900/90 border-zinc-200 dark:border-zinc-800 hover:bg-white dark:hover:bg-zinc-800'
            : 'bg-white/50 dark:bg-zinc-900/50 border-zinc-200/50 dark:border-zinc-800/50 opacity-50'
        }`}
        title={canSend ? 'Send a gift' : 'Already sent a gift today'}
      >
        <Gift size={18} className={canSend ? 'text-amber-500' : 'text-zinc-400'} />
      </button>

      <AnimatePresence>
        {drawerOpen && (
          <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-end md:items-center justify-center"
            onClick={() => !sending && setDrawerOpen(false)}
          >
            <MotionDiv
              initial={{ y: 100, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 100, opacity: 0 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="bg-white dark:bg-zinc-900 rounded-t-2xl md:rounded-2xl p-5 w-full max-w-md shadow-2xl max-h-[70vh] flex flex-col"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              {sent ? (
                <div className="flex flex-col items-center py-8">
                  <MotionDiv
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', damping: 10, stiffness: 200 }}
                  >
                    <Gift size={48} className="text-amber-500" />
                  </MotionDiv>
                  <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300 mt-3">
                    {sentItemName} sent to {targetName}!
                  </p>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="text-sm font-semibold text-zinc-900 dark:text-white">Send a Gift to {targetName}</h3>
                    <button onClick={() => setDrawerOpen(false)} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800">
                      <X size={16} className="text-zinc-400" />
                    </button>
                  </div>
                  <p className="text-[10px] text-zinc-400 mb-3">Pick a decoration to send. Costs come from your points.</p>

                  <div className="overflow-y-auto flex-1" style={{ scrollbarWidth: 'none' }}>
                    <div className="grid grid-cols-2 gap-2">
                      {GIFTABLE_ITEMS.map(item => {
                        const canAfford = pointsBalance >= item.price;
                        return (
                          <MotionButton
                            key={item.id}
                            whileTap={{ scale: 0.97 }}
                            onClick={() => handleSend(item)}
                            disabled={!canAfford || sending}
                            className={`text-left p-3 rounded-xl border transition-colors ${
                              canAfford
                                ? 'border-zinc-200 dark:border-zinc-700 hover:border-amber-300 dark:hover:border-amber-700 hover:bg-amber-50 dark:hover:bg-amber-950/20'
                                : 'border-zinc-200 dark:border-zinc-800 opacity-40 cursor-not-allowed'
                            }`}
                          >
                            <p className="text-xs font-semibold text-zinc-800 dark:text-zinc-200">{item.name}</p>
                            <p className="text-[10px] text-zinc-500 dark:text-zinc-400 mt-0.5 line-clamp-1">{item.description}</p>
                            <p className="text-[10px] font-bold text-amber-600 dark:text-amber-400 mt-1">{item.price} pts</p>
                          </MotionButton>
                        );
                      })}
                    </div>
                  </div>
                </>
              )}
            </MotionDiv>
          </MotionDiv>
        )}
      </AnimatePresence>
    </>
  );
};

export default GiftButton;
