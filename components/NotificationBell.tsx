/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, MessageSquare, Flame, TrendingUp, BookOpen, AlertTriangle, Megaphone, Heart, CheckCheck } from 'lucide-react';
import { getNotifications, markNotificationRead, markAllRead, type AppNotification, type NotificationType } from './gc/gcNotifications';

const MotionDiv = motion.div as any;

const ICON_MAP: Record<NotificationType, React.ElementType> = {
  'gc-recommendation': BookOpen,
  'gc-kudos': Heart,
  'comeback': Flame,
  'streak-milestone': TrendingUp,
  'study-insight': MessageSquare,
  'subject-neglect': AlertTriangle,
  'gc-broadcast': Megaphone,
};

const ICON_COLOR_MAP: Record<NotificationType, string> = {
  'gc-recommendation': 'text-indigo-500 bg-indigo-100 dark:bg-indigo-900/30',
  'gc-kudos': 'text-emerald-500 bg-emerald-100 dark:bg-emerald-900/30',
  'comeback': 'text-orange-500 bg-orange-100 dark:bg-orange-900/30',
  'streak-milestone': 'text-amber-500 bg-amber-100 dark:bg-amber-900/30',
  'study-insight': 'text-teal-500 bg-teal-100 dark:bg-teal-900/30',
  'subject-neglect': 'text-rose-500 bg-rose-100 dark:bg-rose-900/30',
  'gc-broadcast': 'text-purple-500 bg-purple-100 dark:bg-purple-900/30',
};

function relativeTime(ts: number): string {
  const diff = Math.floor((Date.now() - ts) / 1000);
  if (diff < 60) return 'just now';
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
  return new Date(ts).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });
}

interface NotificationBellProps {
  uid: string;
  onUnreadCountChange?: (count: number) => void;
}

const NotificationBell: React.FC<NotificationBellProps> = ({ uid, onUnreadCountChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<AppNotification[]>([]);
  const panelRef = useRef<HTMLDivElement>(null);

  const loadNotifications = useCallback(async () => {
    const items = await getNotifications(uid);
    setNotifications(items);
    const unread = items.filter(n => !n.read).length;
    onUnreadCountChange?.(unread);
  }, [uid, onUnreadCountChange]);

  // Initial load + polling every 60s
  useEffect(() => {
    loadNotifications();
    const interval = setInterval(loadNotifications, 60000);
    return () => clearInterval(interval);
  }, [loadNotifications]);

  // Click outside to close
  useEffect(() => {
    if (!isOpen) return;
    const handler = (e: MouseEvent) => {
      if (panelRef.current && !panelRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [isOpen]);

  const unreadCount = notifications.filter(n => !n.read).length;
  const newItems = notifications.filter(n => !n.read);
  const earlierItems = notifications.filter(n => n.read).slice(0, 20);

  const handleMarkRead = async (id: string) => {
    await markNotificationRead(uid, id);
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
    onUnreadCountChange?.(Math.max(0, unreadCount - 1));
  };

  const handleMarkAllRead = async () => {
    await markAllRead(uid);
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    onUnreadCountChange?.(0);
  };

  return (
    <div className="relative" ref={panelRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2.5 rounded-xl bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm border border-zinc-200/60 dark:border-zinc-800/60 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]"
      >
        <Bell size={18} className="text-zinc-600 dark:text-zinc-300" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] flex items-center justify-center rounded-full bg-rose-500 text-white text-[10px] font-bold px-1">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      <AnimatePresence>
        {isOpen && (
          <MotionDiv
            initial={{ opacity: 0, y: -8, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="absolute top-full right-0 mt-2 w-80 sm:w-96 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-xl overflow-hidden z-50"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-100 dark:border-zinc-800">
              <h3 className="text-sm font-semibold text-zinc-800 dark:text-white">Notifications</h3>
              {unreadCount > 0 && (
                <button
                  onClick={handleMarkAllRead}
                  className="flex items-center gap-1 text-[11px] font-medium text-[var(--accent-hex)] hover:opacity-80 transition-opacity"
                >
                  <CheckCheck size={12} /> Mark all read
                </button>
              )}
            </div>

            {/* Body */}
            <div className="max-h-[400px] overflow-y-auto">
              {notifications.length === 0 ? (
                <div className="py-10 text-center">
                  <Bell size={24} className="mx-auto text-zinc-300 dark:text-zinc-600 mb-2" />
                  <p className="text-sm text-zinc-400 dark:text-zinc-500">No notifications yet</p>
                </div>
              ) : (
                <>
                  {newItems.length > 0 && (
                    <div>
                      <p className="px-4 pt-3 pb-1 text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">New</p>
                      {newItems.map(item => (
                        <NotificationItem key={item.id} item={item} onMarkRead={handleMarkRead} />
                      ))}
                    </div>
                  )}
                  {earlierItems.length > 0 && (
                    <div>
                      <p className="px-4 pt-3 pb-1 text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Earlier</p>
                      {earlierItems.map(item => (
                        <NotificationItem key={item.id} item={item} onMarkRead={handleMarkRead} />
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

const NotificationItem: React.FC<{ item: AppNotification; onMarkRead: (id: string) => void }> = ({ item, onMarkRead }) => {
  const IconComp = ICON_MAP[item.type] || Bell;
  const colorClasses = ICON_COLOR_MAP[item.type] || 'text-zinc-500 bg-zinc-100 dark:bg-zinc-800';

  return (
    <button
      onClick={() => !item.read && onMarkRead(item.id)}
      className={`w-full flex items-start gap-3 px-4 py-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors ${!item.read ? 'bg-[rgba(var(--accent),0.03)]' : ''}`}
    >
      <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${colorClasses}`}>
        <IconComp size={14} />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <p className={`text-sm leading-tight ${!item.read ? 'font-semibold text-zinc-800 dark:text-white' : 'font-medium text-zinc-600 dark:text-zinc-300'}`}>
            {item.title}
          </p>
          {!item.read && <div className="w-2 h-2 rounded-full bg-[var(--accent-hex)] shrink-0 mt-1.5" />}
        </div>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5 line-clamp-2">{item.body}</p>
        <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1">{relativeTime(item.timestamp)}</p>
      </div>
    </button>
  );
};

export default NotificationBell;
