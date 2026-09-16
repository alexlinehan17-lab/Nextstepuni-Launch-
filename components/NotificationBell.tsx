/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useCallback, useId } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv, useReducedMotion } from './Motion';
import { X, ArrowUpRight } from 'lucide-react';
import { getNotifications, markNotificationRead, markAllRead, STAFF_ORIGINATED, type AppNotification, type NotificationType } from './gc/gcNotifications';
import { staffMessageText } from '../data/staffEncouragement';
import { NOTIFICATION_PANEL_TOGGLE_EVENT } from '../utils/notificationPanel';
import { DEMO_STUDENT_UID } from '../data/devStudent';

import './student-header.css';

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
  variant?: 'icon' | 'menu';
}

const NotificationBell: React.FC<NotificationBellProps> = ({ uid, onUnreadCountChange, variant = 'icon' }) => {
  const isDemo = uid === DEMO_STUDENT_UID;
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<AppNotification[]>([]);
  const panelRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const reducedMotion = useReducedMotion();
  const panelId = useId();

  useEffect(() => {
    if (!isOpen) { setSelectedId(null); return; }
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
        triggerRef.current?.focus();
      }
    };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [isOpen]);

  const loadNotifications = useCallback(async () => {
    if (isDemo) {
      setNotifications([]);
      onUnreadCountChange?.(0);
      return;
    }
    const items = await getNotifications(uid);
    setNotifications(items);
    const unread = items.filter(n => !n.read).length;
    onUnreadCountChange?.(unread);
  }, [uid, isDemo, onUnreadCountChange]);

  // Initial load + polling every 60s
  useEffect(() => {
    loadNotifications();
    if (isDemo) return;
    const interval = setInterval(loadNotifications, 60000);
    return () => clearInterval(interval);
  }, [isDemo, loadNotifications]);

  // Sidebar and header controls share this one state transition. Keeping the
  // panel state here avoids delayed synthetic clicks that can close and then
  // immediately reopen the panel.
  useEffect(() => {
    const handleToggle = () => setIsOpen(open => !open);
    window.addEventListener(NOTIFICATION_PANEL_TOGGLE_EVENT, handleToggle);
    return () => window.removeEventListener(NOTIFICATION_PANEL_TOGGLE_EVENT, handleToggle);
  }, []);

  // Click outside to close
  useEffect(() => {
    if (!isOpen) return;
    const handler = (e: MouseEvent) => {
      const target = e.target instanceof Element ? e.target : null;
      // An external sidebar toggle is part of the notification control. Let
      // its click perform the single close transition instead of treating its
      // preceding mousedown as an outside dismissal too.
      if (target?.closest('[data-notification-toggle]')) return;
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

  // Mark-read updates the UI first. Awaiting the write meant a tap did nothing
  // visible offline — the badge stayed lit until a reload.
  const handleMarkRead = (id: string) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
    onUnreadCountChange?.(Math.max(0, unreadCount - 1));
    if (!isDemo) void markNotificationRead(uid, id);
  };

  const handleMarkAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    onUnreadCountChange?.(0);
    if (!isDemo) void markAllRead(uid);
  };

  const selected = notifications.find(item => item.id === selectedId);
  const openItem = (item: AppNotification) => {
    if (!item.read) handleMarkRead(item.id);
    setSelectedId(item.id);
  };

  return (
    <div className={`nsu-post ${variant === 'menu' ? 'nsu-post-menu' : ''}`} ref={panelRef}>
      <button
        ref={triggerRef}
        data-notification-bell
        data-notification-toggle
        type="button"
        aria-label={isOpen ? 'Close notifications' : 'Open notifications'}
        aria-expanded={isOpen}
        aria-controls={isOpen ? panelId : undefined}
        title={unreadCount > 0 ? `${unreadCount} unread notifications` : 'Notifications'}
        onClick={() => setIsOpen(!isOpen)}
        className={`nsu-post-toggle ${isOpen ? 'is-open' : ''}`}
      >
        <span className="nsu-post-symbol" aria-hidden="true">
          <span className="nsu-folded-note"><i /><i /></span>
          {unreadCount > 0 && <span className="nsu-post-count">{unreadCount > 99 ? '99+' : unreadCount}</span>}
        </span>
        {variant === 'menu' && <span>Notifications</span>}
      </button>

      <AnimatePresence>
        {isOpen && (
          <MotionDiv
            id={panelId}
            role="region"
            aria-label="Notifications"
            initial={reducedMotion ? false : { opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={reducedMotion ? { opacity: 0 } : { opacity: 0, y: -8 }}
            transition={{ duration: reducedMotion ? 0 : 0.2 }}
            className="nsu-post-panel"
          >
            <div className="nsu-post-heading">
              <div><p className="nsu-post-eyebrow">YOUR UPDATES</p><h3>You’ve got post.</h3></div>
              <img src="/assets/star-crew/companions/listener-transparent.png" alt="" width="77" height="77" />
              <button type="button" className="nsu-post-close" aria-label="Close updates" onClick={() => { setIsOpen(false); triggerRef.current?.focus(); }}><X size={17} /></button>
            </div>
            <div className="nsu-post-body">
              {selected ? (
                <div className="nsu-post-detail">
                  <button type="button" className="nsu-post-back" onClick={() => setSelectedId(null)}>← All updates</button>
                  <p className="nsu-post-eyebrow">{STAFF_ORIGINATED.has(selected.type) ? 'FROM YOUR SCHOOL' : 'FROM NEXTSTEPUNI'}</p>
                  <h4>{displayTitle(selected)}</h4>
                  <p className="nsu-post-message">{displayBody(selected)}</p>
                  <p className="nsu-post-time">{relativeTime(selected.timestamp)} · Read</p>
                </div>
              ) : notifications.length === 0 ? (
                <div className="nsu-post-empty"><strong>All quiet for now.</strong><p>Messages from your school and updates on your progress will arrive here.</p></div>
              ) : (
                <>
                  {newItems.length > 0 && <section aria-label="New updates"><p className="nsu-post-section">New</p>{newItems.map(item => <NotificationItem key={item.id} item={item} onOpen={openItem} />)}</section>}
                  {earlierItems.length > 0 && <section aria-label="Earlier updates"><p className="nsu-post-section">Earlier</p>{earlierItems.map(item => <NotificationItem key={item.id} item={item} onOpen={openItem} />)}</section>}
                </>
              )}
            </div>
            {!selected && unreadCount > 0 && <div className="nsu-post-footer"><button type="button" onClick={handleMarkAllRead}>Mark all as read</button></div>}
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

  /**
 * Text to show a student for a notification.
 *
 * Anything written by a human at their school renders from the preset table by
 * `messageId` — never from the stored `body`. Staff send an id, not prose
 * (owner decision 2026-08-17, data/staffEncouragement.ts), so free text cannot
 * reach a minor even if a document were written directly through the SDK,
 * bypassing the dashboard UI. Legacy free-text notifications sent before
 * presets existed fall back to the neutral line rather than being displayed.
 *
 * App-generated notifications (streaks, comebacks, study insights) keep using
 * `body`: that copy comes from this codebase, not from a person.
 */
function displayBody(item: AppNotification): string {
  if (!STAFF_ORIGINATED.has(item.type)) return item.body;
  return staffMessageText(item.messageId);
}

/**
 * Titles for staff-originated notifications come from here, never from the
 * document.
 *
 * `title` used to be rendered raw for every type — so even a well-formed
 * gc-kudos item carried an unbounded free-text field to a student, in the
 * bolder of the two lines (security review 2026-08-17). Staff writes are now
 * denied by firestore.rules and composed server-side, which closes the write
 * path; this closes the READ path for the documents already in the database
 * from before that change.
 */
const STAFF_TITLES: Partial<Record<NotificationType, string>> = {
  'gc-kudos': 'Words of encouragement',
  'gc-recommendation': 'A tool your school suggests',
  'gc-broadcast': 'Message from your school',
};

function displayTitle(item: AppNotification): string {
  return STAFF_ORIGINATED.has(item.type)
    ? (STAFF_TITLES[item.type] ?? 'Message from your school')
    : item.title;
}

const NotificationItem: React.FC<{ item: AppNotification; onOpen: (item: AppNotification) => void }> = ({ item, onOpen }) => (
  <button type="button" onClick={() => onOpen(item)} className={`nsu-post-item ${item.read ? 'is-read' : ''}`}>
    <span className="nsu-post-dot" aria-hidden="true" />
    <span className="nsu-post-item-copy">
      <span className="nsu-post-eyebrow">{STAFF_ORIGINATED.has(item.type) ? 'From your school' : 'Nextstepuni'}</span>
      <strong>{displayTitle(item)}</strong>
      <span className="nsu-post-excerpt">{displayBody(item)}</span>
      <span className="nsu-post-time">{relativeTime(item.timestamp)}{!item.read && <span className="sr-only"> · Unread</span>}</span>
    </span>
    <ArrowUpRight size={17} aria-hidden="true" />
  </button>
);

export default NotificationBell;
