/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { WifiOff, Wifi } from 'lucide-react';
import { useOnlineStatus } from '../hooks/useOnlineStatus';

const OfflineBanner: React.FC = () => {
  const isOnline = useOnlineStatus();
  const [showReconnected, setShowReconnected] = useState(false);
  const wasOfflineRef = useRef(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!isOnline) {
      wasOfflineRef.current = true;
      setShowReconnected(false);
      if (timerRef.current) clearTimeout(timerRef.current);
    } else if (wasOfflineRef.current) {
      // Just came back online
      setShowReconnected(true);
      timerRef.current = setTimeout(() => {
        setShowReconnected(false);
        wasOfflineRef.current = false;
      }, 3000);
    }
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [isOnline]);

  const showBanner = !isOnline || showReconnected;

  return (
    <AnimatePresence>
      {showBanner && (
        <MotionDiv
          initial={{ y: -40, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -40, opacity: 0 }}
          transition={{ duration: 0.3, ease: [0.25, 1, 0.5, 1] }}
          className="fixed top-0 left-0 right-0 z-[200] flex items-center justify-center gap-2 py-2 px-4 text-xs font-medium"
          style={{
            // COLORS.success (#3A8D5F) carries white at only 4.07:1, and the
            // offline amber at 2.84:1. Darkening the green clears it with white;
            // the amber stays as authored — it is the recognisable warning
            // colour — and takes dark ink instead, which gives 6.13:1.
            backgroundColor: isOnline ? '#2F7A50' : '#D4891C',
            color: isOnline ? '#fff' : 'var(--ink-on-accent)',
          }}
        >
          {isOnline ? (
            <>
              <Wifi size={13} />
              <span>Back online — syncing your changes</span>
            </>
          ) : (
            <>
              <WifiOff size={13} />
              <span>You're offline — changes will sync when you reconnect</span>
            </>
          )}
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

export default OfflineBanner;
