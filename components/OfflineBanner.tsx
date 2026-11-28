/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { useOnlineStatus } from '../hooks/useOnlineStatus';
import { StandingMessage } from './ui/Message';

/** The one offline notice: the shared message's charcoal line at the foot of the screen (above the
 *  tab bar and the home indicator), never over a bar or the sidebar. Today's words. */
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

  const text = !isOnline
    ? 'You\'re offline — changes will sync when you reconnect'
    : showReconnected ? 'Back online — syncing your changes' : null;

  return <StandingMessage text={text} />;
};

export default OfflineBanner;
