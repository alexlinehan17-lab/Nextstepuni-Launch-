/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { WifiOff, AlertCircle, CheckCircle, X, Info, type LucideIcon } from 'lucide-react';
import { SAVE_ERROR_EVENT, type SaveErrorDetail } from '../utils/logError';

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
  icon: LucideIcon;
  bg: string;
  text: string;
  iconColor: string;
}> = {
  error: {
    icon: AlertCircle,
    bg: 'bg-red-50 dark:bg-red-950/80',
    text: 'text-[#7F1D1D] dark:text-red-200',
    iconColor: 'text-red-500 dark:text-red-400',
  },
  success: {
    icon: CheckCircle,
    bg: 'bg-emerald-50 dark:bg-emerald-950/80',
    text: 'text-[#14532D] dark:text-emerald-200',
    iconColor: 'text-emerald-500 dark:text-emerald-400',
  },
  warning: {
    icon: WifiOff,
    bg: 'bg-amber-50 dark:bg-amber-950/80',
    text: 'text-[#78350F] dark:text-amber-200',
    iconColor: 'text-amber-500 dark:text-amber-400',
  },
  info: {
    icon: Info,
    bg: 'bg-zinc-50 dark:bg-zinc-900/90',
    text: 'text-[#383838] dark:text-zinc-200',
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

  // Bridge: the data layer (hooks, contexts, plain async fns) reports save
  // failures via a window event (see utils/logError.ts → reportSaveError) so it
  // can surface a toast without holding this context. The dedupe in showToast
  // keeps a burst of failures to a single visible toast.
  useEffect(() => {
    const onSaveError = (e: Event) => {
      const detail = (e as CustomEvent<SaveErrorDetail>).detail;
      showToast(detail?.message ?? "Couldn't save — check your connection", 'error');
    };
    window.addEventListener(SAVE_ERROR_EVENT, onSaveError);
    return () => window.removeEventListener(SAVE_ERROR_EVENT, onSaveError);
  }, [showToast]);

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
            className="fixed left-1/2 top-3 z-[9999] flex w-[calc(100%-1.5rem)] max-w-lg -translate-x-1/2 items-center justify-center gap-2 rounded-xl border-[1.5px] border-[#383838] bg-[#FFF8E5] px-4 py-3 shadow-[3px_3px_0_0_#383838] dark:border-zinc-600 dark:bg-amber-950"
          >
            <WifiOff size={14} className="text-amber-500 dark:text-amber-400 shrink-0" />
            <span className="text-xs font-semibold text-amber-700 dark:text-amber-300">
              You're offline — some features may not work
            </span>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Toast stack */}
      <div className="fixed bottom-[calc(1rem+var(--sab,0px))] left-1/2 z-[9998] flex w-[calc(100%-1.5rem)] max-w-md -translate-x-1/2 flex-col-reverse gap-3 pointer-events-none sm:bottom-6">
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
                role={toast.type === 'error' ? 'alert' : 'status'}
                className={`pointer-events-auto flex min-h-14 items-center gap-3 rounded-xl border-[1.5px] border-[#383838] px-4 py-3 shadow-[4px_4px_0_0_#383838] dark:border-zinc-600 ${config.bg}`}
              >
                <Icon size={16} className={`${config.iconColor} shrink-0`} />
                <span className={`text-xs font-medium flex-1 ${config.text}`}>{toast.message}</span>
                <button
                  onClick={() => dismissToast(toast.id)}
                  aria-label="Dismiss message"
                  className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-zinc-500 transition-colors hover:bg-black/5 hover:text-zinc-800 dark:hover:bg-white/10 dark:hover:text-white"
                >
                  <X size={14} />
                </button>
              </MotionDiv>
            );
          })}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
};
