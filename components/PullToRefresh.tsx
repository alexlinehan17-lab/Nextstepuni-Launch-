/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useRef, useState } from 'react';
import { Capacitor } from '@capacitor/core';

const TRIGGER_DISTANCE = 70;
const MAX_PULL = 120;
const DRAG_RATIO = 0.5;
const PAGE_RATIO = 0.35;
const BADGE_SIZE = 40;
const ARC_RADIUS = 9;
const ARC_CIRCUMFERENCE = 2 * Math.PI * ARC_RADIUS;

interface PullToRefreshProps {
  children: React.ReactNode;
}

const PullToRefresh: React.FC<PullToRefreshProps> = ({ children }) => {
  const native = Capacitor.isNativePlatform();
  const [pull, setPull] = useState(0);
  const [refreshing, setRefreshing] = useState(false);
  // `transformActive` controls whether the wrapper has a CSS transform applied.
  // We only apply it while actively pulling / refreshing / snapping back,
  // because a transform on the wrapper creates a containing block for fixed-
  // positioned descendants — which breaks every modal/overlay (profile sheet,
  // settings, toasts, etc.) that uses position: fixed. At rest, no transform
  // is applied so position: fixed resolves against the viewport as expected.
  const [transformActive, setTransformActive] = useState(false);
  const startY = useRef<number | null>(null);
  const tracking = useRef(false);

  useEffect(() => {
    if (!native) return;

    const onTouchStart = (e: TouchEvent) => {
      if (window.scrollY > 0) return;
      startY.current = e.touches[0].clientY;
      tracking.current = true;
    };

    const onTouchMove = (e: TouchEvent) => {
      if (!tracking.current || startY.current === null) return;
      const delta = e.touches[0].clientY - startY.current;
      if (delta <= 0) {
        setPull(0);
        return;
      }
      const dampened = Math.min(delta * DRAG_RATIO, MAX_PULL);
      setPull(dampened);
      setTransformActive(true);
    };

    const onTouchEnd = () => {
      if (!tracking.current) return;
      tracking.current = false;
      startY.current = null;
      setPull(prev => {
        if (prev >= TRIGGER_DISTANCE && !refreshing) {
          setRefreshing(true);
          window.location.reload();
          return TRIGGER_DISTANCE;
        }
        return 0;
      });
    };

    window.addEventListener('touchstart', onTouchStart, { passive: true });
    window.addEventListener('touchmove', onTouchMove, { passive: true });
    window.addEventListener('touchend', onTouchEnd, { passive: true });
    window.addEventListener('touchcancel', onTouchEnd, { passive: true });

    return () => {
      window.removeEventListener('touchstart', onTouchStart);
      window.removeEventListener('touchmove', onTouchMove);
      window.removeEventListener('touchend', onTouchEnd);
      window.removeEventListener('touchcancel', onTouchEnd);
    };
  }, [native, refreshing]);

  if (!native) return <>{children}</>;

  const progress = Math.min(pull / TRIGGER_DISTANCE, 1);
  // Badge slides in from above (-BADGE_SIZE) and settles into view as the pull grows.
  // It eases toward a final resting point a little below the safe-area top.
  const badgeY = -BADGE_SIZE + Math.min(pull * 0.9, BADGE_SIZE + 20);
  const badgeScale = 0.6 + 0.4 * progress;
  const badgeOpacity = Math.min(pull / 18, 1);
  // Arc fills clockwise from 12 o'clock. Use stroke-dashoffset for smooth progress.
  const arcOffset = ARC_CIRCUMFERENCE * (1 - progress);
  // While the finger is moving, no transition — feels 1:1 with touch.
  // On release (pull === 0) or while refreshing, transitions kick in for the snap.
  const isResting = pull === 0 || refreshing;
  const pageTransform = `translate3d(0, ${pull * PAGE_RATIO}px, 0)`;

  return (
    <>
      <div
        style={transformActive ? {
          transform: pageTransform,
          transition: isResting ? 'transform 0.32s cubic-bezier(0.22, 1, 0.36, 1)' : 'none',
          willChange: 'transform',
        } : undefined}
        // When the snap-back animation finishes (pull is 0, not refreshing),
        // drop the transform so position: fixed descendants are no longer
        // re-anchored to this wrapper.
        onTransitionEnd={() => {
          if (pull === 0 && !refreshing) setTransformActive(false);
        }}
      >
        {children}
      </div>
      <div
        aria-hidden
        style={{
          position: 'fixed',
          top: 'calc(env(safe-area-inset-top, 0px) + 8px)',
          left: '50%',
          marginLeft: `-${BADGE_SIZE / 2}px`,
          width: `${BADGE_SIZE}px`,
          height: `${BADGE_SIZE}px`,
          borderRadius: '50%',
          background: '#ffffff',
          boxShadow: '0 2px 10px rgba(0,0,0,0.12), 0 1px 3px rgba(0,0,0,0.06)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          pointerEvents: 'none',
          zIndex: 9999,
          opacity: badgeOpacity,
          transform: `translate3d(0, ${badgeY}px, 0) scale(${badgeScale})`,
          transition: isResting ? 'transform 0.32s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.2s ease-out' : 'none',
          willChange: 'transform, opacity',
        }}
      >
        <svg
          width="22"
          height="22"
          viewBox="0 0 22 22"
          style={{
            animation: refreshing ? 'ptr-spin 0.9s linear infinite' : undefined,
            transform: refreshing ? undefined : `rotate(-90deg)`,
            transformOrigin: 'center',
          }}
        >
          {/* Track */}
          <circle
            cx="11"
            cy="11"
            r={ARC_RADIUS}
            fill="none"
            stroke="rgba(242,107,31,0.12)"
            strokeWidth="2"
          />
          {/* Progress arc */}
          <circle
            cx="11"
            cy="11"
            r={ARC_RADIUS}
            fill="none"
            stroke="#F26B1F"
            strokeWidth="2"
            strokeLinecap="round"
            strokeDasharray={ARC_CIRCUMFERENCE}
            strokeDashoffset={refreshing ? ARC_CIRCUMFERENCE * 0.75 : arcOffset}
            style={{
              transition: isResting && !refreshing ? 'stroke-dashoffset 0.25s ease-out' : 'none',
            }}
          />
        </svg>
        <style>{`@keyframes ptr-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
      </div>
    </>
  );
};

export default PullToRefresh;
