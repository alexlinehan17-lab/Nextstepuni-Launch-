/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from '../Motion';
import { Heart, X } from 'lucide-react';
import { KUDOS_MESSAGES } from '../../kudosData';

interface KudosButtonProps {
  senderUid: string;
  senderName: string;
  targetUid: string;
  school: string;
  canSendKudosTo: (uid: string) => Promise<boolean>;
  sendKudos: (toUid: string, school: string, messageId: string, fromName: string) => Promise<boolean>;
}

const KudosButton: React.FC<KudosButtonProps> = ({
  senderUid, senderName, targetUid, school,
  canSendKudosTo, sendKudos,
}) => {
  const [pickerOpen, setPickerOpen] = useState(false);
  const [canSend, setCanSend] = useState(true);
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);
  const sentTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (sentTimerRef.current) clearTimeout(sentTimerRef.current);
    };
  }, []);

  useEffect(() => {
    canSendKudosTo(targetUid).then(setCanSend);
  }, [targetUid, canSendKudosTo]);

  const handleSend = async (messageId: string) => {
    if (sending) return;
    setSending(true);
    const success = await sendKudos(targetUid, school, messageId, senderName);
    setSending(false);
    if (success) {
      setSent(true);
      setCanSend(false);
      sentTimerRef.current = setTimeout(() => { setPickerOpen(false); setSent(false); }, 1200);
    }
  };

  return (
    <>
      <button
        onClick={() => canSend && setPickerOpen(true)}
        disabled={!canSend}
        className={`p-2.5 rounded-xl backdrop-blur-sm border transition-colors ${
          canSend
            ? 'bg-white/90 dark:bg-zinc-900/90 border-zinc-200 dark:border-zinc-800 hover:bg-white dark:hover:bg-zinc-800'
            : 'bg-white/50 dark:bg-zinc-900/50 border-zinc-200/50 dark:border-zinc-800/50 opacity-50'
        }`}
        title={canSend ? 'Send kudos' : 'Already sent kudos today'}
      >
        <Heart size={18} className={canSend ? 'text-pink-500' : 'text-zinc-400'} fill={canSend ? 'none' : 'currentColor'} />
      </button>

      {/* Kudos picker modal */}
      <AnimatePresence>
        {pickerOpen && (
          <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center px-6"
            onClick={() => !sending && setPickerOpen(false)}
          >
            <MotionDiv
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="bg-white dark:bg-zinc-900 rounded-2xl p-5 w-full max-w-sm shadow-2xl"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              {sent ? (
                <div className="flex flex-col items-center py-8">
                  <MotionDiv
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', damping: 10, stiffness: 200 }}
                  >
                    <Heart size={48} className="text-pink-500" fill="currentColor" />
                  </MotionDiv>
                  <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300 mt-3">Kudos sent!</p>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-semibold text-zinc-900 dark:text-white">Send Kudos</h3>
                    <button onClick={() => setPickerOpen(false)} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800">
                      <X size={16} className="text-zinc-400" />
                    </button>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    {KUDOS_MESSAGES.map(msg => (
                      <MotionButton
                        key={msg.id}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => handleSend(msg.id)}
                        disabled={sending}
                        className="flex items-center gap-2 px-3 py-2.5 rounded-xl border border-zinc-200 dark:border-zinc-700 hover:border-pink-300 dark:hover:border-pink-700 hover:bg-pink-50 dark:hover:bg-pink-950/20 transition-colors text-left"
                      >
                        <span className="text-base">{msg.emoji}</span>
                        <span className="text-xs font-medium text-zinc-700 dark:text-zinc-300 leading-tight">{msg.text}</span>
                      </MotionButton>
                    ))}
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

export default KudosButton;
