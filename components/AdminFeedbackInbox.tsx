/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Inbox, RefreshCw } from 'lucide-react';
import {
  collection,
  doc,
  getCountFromServer,
  getDocs,
  limit,
  orderBy,
  query,
  serverTimestamp,
  startAfter,
  updateDoc,
  where,
  type DocumentData,
  type QueryConstraint,
  type QueryDocumentSnapshot,
  type Timestamp,
} from 'firebase/firestore';
import { db } from '../firebase';
import { saveInBackground } from '../utils/firestoreWrite';
import {
  FEEDBACK_CATEGORY_LABELS,
  FEEDBACK_STATUSES,
  FEEDBACK_STATUS_LABELS,
  type FeedbackCategory,
  type FeedbackPlatform,
  type FeedbackStatus,
} from '../utils/anonymousFeedback';

interface FeedbackEntry {
  id: string;
  category: FeedbackCategory;
  message: string;
  context: { surface: string; moduleId?: string; moduleTitle?: string } | null;
  platform: FeedbackPlatform;
  appVersion: string;
  status: FeedbackStatus;
  createdAt?: Timestamp;
}

const PAGE_SIZE = 50;

function formatDate(createdAt?: Timestamp): string {
  if (!createdAt?.toDate) return 'Just now';
  return new Intl.DateTimeFormat('en-IE', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(createdAt.toDate());
}

const AdminFeedbackInbox: React.FC = () => {
  const [entries, setEntries] = useState<FeedbackEntry[]>([]);
  const [statusFilter, setStatusFilter] = useState<FeedbackStatus>('new');
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(false);
  const [statusCounts, setStatusCounts] = useState<Record<FeedbackStatus, number>>({
    new: 0,
    reviewing: 0,
    planned: 0,
    fixed: 0,
    archived: 0,
  });
  const [error, setError] = useState('');
  const lastDocument = useRef<QueryDocumentSnapshot<DocumentData> | null>(null);

  const loadCounts = useCallback(async () => {
    const feedbackCollection = collection(db, 'anonymousFeedback');
    const counts = await Promise.all(FEEDBACK_STATUSES.map(async status => {
      const snapshot = await getCountFromServer(query(feedbackCollection, where('status', '==', status)));
      return [status, snapshot.data().count] as const;
    }));
    setStatusCounts(Object.fromEntries(counts) as Record<FeedbackStatus, number>);
  }, []);

  const loadFeedback = useCallback(async (append = false) => {
    if (append) setIsLoadingMore(true);
    else setIsLoading(true);
    setError('');
    try {
      const constraints: QueryConstraint[] = [
        where('status', '==', statusFilter),
        orderBy('createdAt', 'desc'),
        limit(PAGE_SIZE),
      ];
      if (append && lastDocument.current) constraints.splice(2, 0, startAfter(lastDocument.current));
      const snapshot = await getDocs(query(
        collection(db, 'anonymousFeedback'),
        ...constraints,
      ));
      const nextEntries = snapshot.docs.map(feedbackDoc => ({
        id: feedbackDoc.id,
        ...feedbackDoc.data(),
      })) as FeedbackEntry[];
      setEntries(current => append ? [...current, ...nextEntries] : nextEntries);
      lastDocument.current = snapshot.docs.at(-1) || null;
      setHasMore(snapshot.docs.length === PAGE_SIZE);
    } catch (loadError) {
      console.error('Error loading anonymous feedback:', loadError);
      setError('Feedback could not be loaded. Confirm the latest Firestore rules are deployed.');
    } finally {
      setIsLoading(false);
      setIsLoadingMore(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    lastDocument.current = null;
    setEntries([]);
    void loadFeedback();
  }, [loadFeedback]);

  useEffect(() => {
    void loadCounts().catch(countError => {
      console.error('Error loading feedback counts:', countError);
      setError('Feedback counts could not be loaded.');
    });
  }, [loadCounts]);

  const updateStatus = (entryId: string, status: FeedbackStatus) => {
    const previousStatus = entries.find(entry => entry.id === entryId)?.status;
    if (!previousStatus || previousStatus === status) return;
    const previousEntry = entries.find(entry => entry.id === entryId);
    setError('');
    setEntries(current => current.filter(entry => entry.id !== entryId));
    setStatusCounts(current => ({
      ...current,
      [previousStatus]: Math.max(0, current[previousStatus] - 1),
      [status]: current[status] + 1,
    }));
    saveInBackground(
      updateDoc(doc(db, 'anonymousFeedback', entryId), {
        status,
        reviewedAt: serverTimestamp(),
      }),
      'AdminFeedbackInbox.updateStatus',
      () => {
        if (previousEntry) setEntries(current => [previousEntry, ...current]);
        setStatusCounts(current => ({
          ...current,
          [previousStatus]: current[previousStatus] + 1,
          [status]: Math.max(0, current[status] - 1),
        }));
        setError('That status change did not save. Please try again.');
      },
    );
  };

  return (
    <section aria-labelledby="feedback-inbox-title">
      <div className="mb-6 flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="mb-1 text-[11px] font-bold uppercase tracking-[0.18em] text-[#9E9186]">Anonymous student voice</p>
          <h2 id="feedback-inbox-title" className="font-serif text-3xl font-semibold text-[#1A1A1A] dark:text-white">Feedback inbox</h2>
          <p className="mt-1 max-w-2xl text-sm text-[#706A64] dark:text-zinc-400">
            Account details are not automatically attached. A message may still contain details a student typed themselves.
          </p>
        </div>
        <button
          type="button"
          onClick={() => {
            lastDocument.current = null;
            void Promise.all([loadFeedback(), loadCounts()]);
          }}
          disabled={isLoading}
          className="flex items-center justify-center gap-2 self-start rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-sm font-bold text-[#1A1A1A] disabled:opacity-50 md:self-auto"
        >
          <RefreshCw size={15} className={isLoading ? 'animate-spin' : ''} />
          Refresh
        </button>
      </div>

      <div className="mb-6 flex gap-2 overflow-x-auto pb-2" role="tablist" aria-label="Feedback status">
        {FEEDBACK_STATUSES.map(status => {
          const selected = statusFilter === status;
          return (
            <button
              key={status}
              type="button"
              role="tab"
              aria-selected={selected}
              onClick={() => setStatusFilter(status)}
              className="flex shrink-0 items-center gap-2 rounded-full border-2 px-4 py-2 text-sm font-bold transition-colors"
              style={{
                borderColor: selected ? '#F26B1F' : '#1A1A1A',
                backgroundColor: selected ? '#F26B1F' : '#FFFFFF',
                color: selected ? '#FFFFFF' : '#1A1A1A',
              }}
            >
              {FEEDBACK_STATUS_LABELS[status]}
              <span
                className="rounded-full px-2 py-0.5 text-[11px]"
                style={{
                  backgroundColor: selected ? '#FFFFFF' : '#F0F0F0',
                  color: selected ? '#9A3B0E' : '#3A3530',
                }}
              >
                {statusCounts[status]}
              </span>
            </button>
          );
        })}
      </div>

      {error && <p className="mb-5 text-sm font-semibold text-red-700" role="alert">{error}</p>}

      {isLoading ? (
        <p className="py-14 text-center text-[#706A64]">Loading feedback…</p>
      ) : entries.length === 0 ? (
        <div className="border-t-2 border-[#1A1A1A] py-16 text-center">
          <Inbox size={30} className="mx-auto mb-3 text-[#9E9186]" />
          <p className="font-serif text-xl font-semibold text-[#1A1A1A] dark:text-white">Nothing here yet.</p>
          <p className="mt-1 text-sm text-[#706A64]">New submissions will appear here after students send them.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {entries.map(entry => (
            <article key={entry.id} className="rounded-2xl border-2 border-[#1A1A1A] bg-white p-5 sm:p-6">
              <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
                <div className="min-w-0">
                  <p className="text-[11px] font-bold uppercase tracking-[0.15em] text-[#9A3B0E]">
                    {FEEDBACK_CATEGORY_LABELS[entry.category] || 'Feedback'}
                  </p>
                  <p className="mt-3 whitespace-pre-wrap text-[15px] leading-relaxed text-[#3A3530]">{entry.message}</p>
                </div>
                <label className="shrink-0 text-[10px] font-bold uppercase tracking-[0.14em] text-[#9E9186]">
                  Status
                  <select
                    value={entry.status}
                    onChange={event => updateStatus(entry.id, event.target.value as FeedbackStatus)}
                    className="mt-1 block min-w-32 rounded-lg border-2 border-[#1A1A1A] bg-white px-3 py-2 text-sm font-semibold normal-case tracking-normal text-[#1A1A1A]"
                  >
                    {FEEDBACK_STATUSES.map(status => (
                      <option key={status} value={status}>{FEEDBACK_STATUS_LABELS[status]}</option>
                    ))}
                  </select>
                </label>
              </div>
              <div className="mt-5 flex flex-wrap gap-x-4 gap-y-1 border-t border-[#DDD8D2] pt-3 text-xs text-[#7A7068]">
                <span>{formatDate(entry.createdAt)}</span>
                <span>{entry.context?.moduleTitle || entry.context?.surface || 'Context not included'}</span>
                <span>{entry.platform}</span>
                <span>Version {entry.appVersion}</span>
              </div>
            </article>
          ))}
          {hasMore && (
            <div className="pt-3 text-center">
              <button
                type="button"
                onClick={() => void loadFeedback(true)}
                disabled={isLoadingMore}
                className="rounded-full border-2 border-[#1A1A1A] bg-white px-5 py-2.5 text-sm font-bold text-[#1A1A1A] disabled:opacity-50"
              >
                {isLoadingMore ? 'Loading…' : 'Load more'}
              </button>
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default AdminFeedbackInbox;
