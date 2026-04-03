/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { WifiOff, AlertCircle, CheckCircle, X, Info } from 'lucide-react';

// ── Types ──────────────────────────────────────────────────

type ToastType = 'error' | 'success' | 'warning' | 'info';

interface Toast {
  id: string;
  message: string;
  type: ToastType;
  duration: number;
}

interface ToastContextValue {
  showToast: (message: string, type?: ToastType, duration?: number) => void;
}

// ── Context ────────────────────────────────────────────────

const ToastContext = createContext<ToastContextValue>({
  showToast: () => {},
});

export const useToast = () => useContext(ToastContext);

// ── Icons & Styles ─────────────────────────────────────────

const TOAST_CONFIG: Record<ToastType, {
  icon: React.ElementType;
  bg: string;
  border: string;
  text: string;
  iconColor: string;
}> = {
  error: {
    icon: AlertCircle,
    bg: 'bg-red-50 dark:bg-red-950/80',
    border: 'border-red-200/60 dark:border-red-800/40',
    text: 'text-red-800 dark:text-red-200',
    iconColor: 'text-red-500 dark:text-red-400',
  },
  success: {
    icon: CheckCircle,
    bg: 'bg-emerald-50 dark:bg-emerald-950/80',
    border: 'border-emerald-200/60 dark:border-emerald-800/40',
    text: 'text-emerald-800 dark:text-emerald-200',
    iconColor: 'text-emerald-500 dark:text-emerald-400',
  },
  warning: {
    icon: WifiOff,
    bg: 'bg-amber-50 dark:bg-amber-950/80',
    border: 'border-amber-200/60 dark:border-amber-800/40',
    text: 'text-amber-800 dark:text-amber-200',
    iconColor: 'text-amber-500 dark:text-amber-400',
  },
  info: {
    icon: Info,
    bg: 'bg-zinc-50 dark:bg-zinc-900/90',
    border: 'border-zinc-200/60 dark:border-zinc-700/40',
    text: 'text-zinc-700 dark:text-zinc-300',
    iconColor: 'text-zinc-500 dark:text-zinc-400',
  },
};

// ── Provider ───────────────────────────────────────────────

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [isOffline, setIsOffline] = useState(!navigator.onLine);

  // Offline detection
  useEffect(() => {
    const goOffline = () => setIsOffline(true);
    const goOnline = () => setIsOffline(false);
    window.addEventListener('offline', goOffline);
    window.addEventListener('online', goOnline);
    return () => {
      window.removeEventListener('offline', goOffline);
      window.removeEventListener('online', goOnline);
    };
  }, []);

  const showToast = useCallback((message: string, type: ToastType = 'error', duration: number = 4000) => {
    const id = Math.random().toString(36).substring(2, 10);
    setToasts(prev => {
      // Deduplicate: don't show the same message if it's already visible
      if (prev.some(t => t.message === message)) return prev;
      return [...prev, { id, message, type, duration }];
    });
  }, []);

  const timerMapRef = useRef<Map<string, ReturnType<typeof setTimeout>>>(new Map());

  const dismissToast = useCallback((id: string) => {
    const timer = timerMapRef.current.get(id);
    if (timer) {
      clearTimeout(timer);
      timerMapRef.current.delete(id);
    }
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  // Auto-dismiss toasts — only create a timer once per toast ID
  useEffect(() => {
    toasts.forEach(toast => {
      if (!timerMapRef.current.has(toast.id)) {
        const timer = setTimeout(() => {
          timerMapRef.current.delete(toast.id);
          dismissToast(toast.id);
        }, toast.duration);
        timerMapRef.current.set(toast.id, timer);
      }
    });

    // Clean up stale entries for toasts that were removed externally
    const currentIds = new Set(toasts.map(t => t.id));
    timerMapRef.current.forEach((timer, id) => {
      if (!currentIds.has(id)) {
        clearTimeout(timer);
        timerMapRef.current.delete(id);
      }
    });
  }, [toasts, dismissToast]);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}

      {/* Offline banner */}
      <AnimatePresence>
        {isOffline && (
          <MotionDiv
            initial={{ y: -60, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -60, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed top-0 left-0 right-0 z-[9999] flex items-center justify-center gap-2 px-4 py-2.5 bg-amber-50 dark:bg-amber-950/90 border-b border-amber-200/60 dark:border-amber-800/40 backdrop-blur-xl"
          >
            <WifiOff size={14} className="text-amber-500 dark:text-amber-400 shrink-0" />
            <span className="text-xs font-semibold text-amber-700 dark:text-amber-300">
              You're offline — some features may not work
            </span>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Toast stack */}
      <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[9998] flex flex-col-reverse gap-2 w-[calc(100%-2rem)] max-w-sm pointer-events-none">
        <AnimatePresence>
          {toasts.map(toast => {
            const config = TOAST_CONFIG[toast.type];
            const Icon = config.icon;
            return (
              <MotionDiv
                key={toast.id}
                initial={{ y: 20, opacity: 0, scale: 0.95 }}
                animate={{ y: 0, opacity: 1, scale: 1 }}
                exit={{ y: 10, opacity: 0, scale: 0.95 }}
                transition={{ type: 'spring', damping: 25, stiffness: 350 }}
                className={`pointer-events-auto flex items-center gap-2.5 px-4 py-3 rounded-xl border shadow-lg backdrop-blur-xl ${config.bg} ${config.border}`}
              >
                <Icon size={16} className={`${config.iconColor} shrink-0`} />
                <span className={`text-xs font-medium flex-1 ${config.text}`}>{toast.message}</span>
                <button
                  onClick={() => dismissToast(toast.id)}
                  className="shrink-0 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                >
                  <X size={12} />
                </button>
              </MotionDiv>
            );
          })}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
};
