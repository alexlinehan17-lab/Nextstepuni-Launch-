/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { useModal } from '../hooks/useModal';
import { BookOpen, Timer, Trophy, Gem, MapPin, SkipForward, CalendarOff } from 'lucide-react';

interface PointsExplainerProps {
  isOpen: boolean;
  onDismiss: () => void;
}

const EARN_ITEMS = [
  { icon: Timer, label: 'Study session', value: '15', unit: 'pts / 10 min', accent: true },
  { icon: BookOpen, label: 'Module section', value: '10', unit: 'pts each', accent: false },
  { icon: Trophy, label: 'Complete a module', value: '+30', unit: 'bonus', accent: false },
  { icon: Gem, label: 'Quests & challenges', value: '25\u2013200', unit: 'pts', accent: false },
];

const SPEND_ITEMS = [
  { icon: MapPin, label: 'Island shop', cost: 'Varies', desc: 'Build your island' },
  { icon: SkipForward, label: 'Skip a block', cost: '20 pts', desc: 'Skip one study session' },
  { icon: CalendarOff, label: 'Rest day pass', cost: '60 pts', desc: 'Day off, streak safe' },
];

const PointsExplainer: React.FC<PointsExplainerProps> = ({ isOpen, onDismiss }) => {
  useModal(isOpen, onDismiss);

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 flex items-center justify-center z-[300] p-4"
          style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}
          onClick={onDismiss}
        >
          <MotionDiv
            initial={{ opacity: 0, y: 20, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.97 }}
            transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            className="w-full max-w-md overflow-hidden"
            style={{ borderRadius: '20px', boxShadow: '0 25px 60px rgba(0,0,0,0.15), 0 0 0 1px rgba(0,0,0,0.06)' }}
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Hero header */}
            <div style={{ background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2a 100%)', padding: '28px 24px 24px' }}>
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', fontWeight: 700, letterSpacing: '0.12em', color: 'rgba(255,255,255,0.4)', textTransform: 'uppercase', margin: 0, marginBottom: '8px' }}>
                YOUR POINTS
              </p>
              <h2 style={{ fontFamily: "'Source Serif 4', serif", fontSize: '26px', fontWeight: 700, color: '#ffffff', margin: 0, marginBottom: '6px' }}>
                Study more, earn more
              </h2>
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '14px', color: 'rgba(255,255,255,0.5)', margin: 0 }}>
                Every session builds your island
              </p>
            </div>

            {/* Content body */}
            <div style={{ background: '#ffffff', padding: '20px 24px 24px' }}>

              {/* Earn grid */}
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase', margin: '0 0 10px 0' }}>
                EARN
              </p>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '20px' }}>
                {EARN_ITEMS.map((item) => (
                  <div
                    key={item.label}
                    style={{
                      padding: '14px 12px',
                      borderRadius: '12px',
                      background: item.accent ? '#e8f5f2' : '#fafaf8',
                      border: item.accent ? '1.5px solid rgba(42,125,111,0.25)' : '1px solid rgba(0,0,0,0.05)',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                      <item.icon size={14} color={item.accent ? '#2A7D6F' : '#9e9186'} strokeWidth={2} />
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', fontWeight: 600, color: '#7a7068' }}>
                        {item.label}
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
                      <span style={{ fontFamily: "'Source Serif 4', serif", fontSize: '22px', fontWeight: 700, color: item.accent ? '#2A7D6F' : '#1a1a1a' }}>
                        {item.value}
                      </span>
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', color: '#9e9186' }}>
                        {item.unit}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Spend row */}
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase', margin: '0 0 10px 0' }}>
                SPEND
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '20px' }}>
                {SPEND_ITEMS.map((item) => (
                  <div
                    key={item.label}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '10px 12px',
                      borderRadius: '10px',
                      background: '#fafaf8',
                      border: '1px solid rgba(0,0,0,0.05)',
                    }}
                  >
                    <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: '#e8f5f2', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                      <item.icon size={16} color="#2A7D6F" strokeWidth={2} />
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '13px', fontWeight: 600, color: '#1a1a1a', margin: 0 }}>
                        {item.label}
                      </p>
                      <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', color: '#9e9186', margin: 0 }}>
                        {item.desc}
                      </p>
                    </div>
                    <span style={{ fontFamily: "'Source Serif 4', serif", fontSize: '13px', fontWeight: 700, color: '#2A7D6F', flexShrink: 0 }}>
                      {item.cost}
                    </span>
                  </div>
                ))}
              </div>

              {/* CTA */}
              <button
                onClick={onDismiss}
                className="w-full transition-all active:translate-y-[3px]"
                style={{
                  background: '#2A7D6F',
                  color: '#ffffff',
                  fontFamily: "'DM Sans', sans-serif",
                  fontSize: '15px',
                  fontWeight: 600,
                  border: 'none',
                  borderRadius: '100px',
                  borderBottom: '3px solid #1a5a4e',
                  boxShadow: '0 4px 0 #1a5a4e',
                  padding: '14px 28px',
                  cursor: 'pointer',
                }}
              >
                Let's go
              </button>
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default PointsExplainer;
