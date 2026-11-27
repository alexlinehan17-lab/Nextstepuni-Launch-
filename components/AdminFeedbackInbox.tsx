/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { RefreshCw } from 'lucide-react';
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
import { Button, TextButton } from './ui/Button';
import { Menu } from './ui/Menu';
import { EmptyState, LoadingShape } from './ui/States';

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

  const refresh = () => {
    if (isLoading) return;
    lastDocument.current = null;
    void Promise.all([loadFeedback(), loadCounts()]);
  };

  return (
    <section aria-labelledby="feedback-inbox-title" className="adm-feedback">
      <header className="gc8-head adm-head">
        <p className="gc8-label">Anonymous student voice</p>
        <h1 id="feedback-inbox-title" className="gc8-name">Feedback inbox</h1>
        <p className="gc8-sub">
          Account details are not automatically attached. A message may still contain details a student typed themselves.
        </p>
        {/* The five statuses in one menu that says which is showing and how many (they ran off the edge as chips). */}
        <div className="adm-asof">
          <Menu
            label="Feedback status"
            value={statusFilter}
            onChange={value => setStatusFilter(value as FeedbackStatus)}
            options={FEEDBACK_STATUSES.map(status => ({ value: status, label: `${FEEDBACK_STATUS_LABELS[status]} · ${statusCounts[status]}` }))}
          />
          <TextButton tone="quiet" className="gc8-ib" aria-disabled={isLoading || undefined} onClick={refresh}>
            <RefreshCw className={`ui-icon${isLoading ? ' adm-spin' : ''}`} width={16} height={16} strokeWidth={2} aria-hidden="true" />Refresh
          </TextButton>
        </div>
      </header>

      {error && <p className="adm-alert" role="alert">{error}</p>}

      {isLoading ? (
        <LoadingShape rows={4} label="Loading feedback…" />
      ) : entries.length === 0 ? (
        <EmptyState className="adm-empty" title="Nothing here yet." line="New submissions will appear here after students send them." />
      ) : (
        <div className="adm-msgs">
          {entries.map(entry => (
            <article key={entry.id} className="adm-msg">
              <p className="gc8-label">{FEEDBACK_CATEGORY_LABELS[entry.category] || 'Feedback'}</p>
              <p className="adm-msgtext">{entry.message}</p>
              <div className="adm-msgfoot">
                <span className="adm-msgmeta">
                  <span className="gc8-meta">{formatDate(entry.createdAt)} · {entry.context?.moduleTitle || entry.context?.surface || 'Context not included'}</span>
                  <span className="gc8-meta"><span>{entry.platform}</span> · <span>Version {entry.appVersion}</span></span>
                </span>
                <Menu
                  label="Status"
                  value={entry.status}
                  onChange={next => updateStatus(entry.id, next as FeedbackStatus)}
                  options={FEEDBACK_STATUSES.map(status => ({ value: status, label: FEEDBACK_STATUS_LABELS[status] }))}
                />
              </div>
            </article>
          ))}
          {hasMore && (
            <div className="adm-more">
              <Button aria-disabled={isLoadingMore || undefined} onClick={() => { if (!isLoadingMore) void loadFeedback(true); }}>
                {isLoadingMore ? 'Loading…' : 'Load more'}
              </Button>
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default AdminFeedbackInbox;
