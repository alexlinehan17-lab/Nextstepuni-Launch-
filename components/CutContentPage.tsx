/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { ArrowLeft, Scissors, FileText } from 'lucide-react';
import { CUT_CONTENT, type CutContentEntry } from '../data/cutContent';

interface CutContentPageProps {
  onBack: () => void;
}

const ActionTag: React.FC<{ action: CutContentEntry['action'] }> = ({ action }) => {
  const reframed = action === 'reframed';
  return (
    <span
      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-[0.06em]"
      style={
        reframed
          ? { backgroundColor: '#E8F2EC', color: '#1F5F3E', border: '1px solid rgba(58,141,95,0.3)' }
          : { backgroundColor: '#FDEEDF', color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.25)' }
      }
    >
      {reframed ? 'Reframed' : 'Removed'}
    </span>
  );
};

const CutEntryCard: React.FC<{ entry: CutContentEntry }> = ({ entry }) => (
  <div className="bg-white rounded-2xl p-5 md:p-6" style={{ border: '2px solid #1a1a1a' }}>
    <div className="flex items-start justify-between gap-3 mb-3">
      <div>
        <h3 className="text-base font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
          {entry.module}
        </h3>
        <p className="text-xs mt-0.5" style={{ color: '#9e9186' }}>
          Cut from: <span style={{ color: '#7a7068', fontWeight: 600 }}>{entry.section}</span>
        </p>
      </div>
      <div className="flex flex-col items-end gap-1.5 shrink-0">
        <ActionTag action={entry.action} />
        <span className="text-[11px]" style={{ color: '#b0a898' }}>{entry.date}</span>
      </div>
    </div>

    {/* Original (removed) text */}
    <div
      className="rounded-lg p-3 mb-3"
      style={{ backgroundColor: '#faf8f5', borderLeft: '3px solid #d0cdc8' }}
    >
      <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>
        Original
      </p>
      <p className="text-[13px] leading-relaxed" style={{ color: '#5a5550' }}>{entry.original}</p>
    </div>

    {/* Reframed replacement, if any */}
    {entry.reframedTo && (
      <div className="rounded-lg p-3 mb-3" style={{ backgroundColor: '#E8F2EC', borderLeft: '3px solid #3A8D5F' }}>
        <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#1F5F3E' }}>
          Reframed to
        </p>
        <p className="text-[13px] leading-relaxed italic" style={{ color: '#1F5F3E' }}>{entry.reframedTo}</p>
      </div>
    )}

    {/* Reason */}
    <div className="flex items-start gap-2">
      <span className="text-[10px] font-bold uppercase tracking-[0.12em] mt-0.5 shrink-0" style={{ color: '#9e9186' }}>
        Reason
      </span>
      <p className="text-[13px] leading-relaxed" style={{ color: '#7a7068' }}>{entry.reason}</p>
    </div>

    {/* Paper to dig out, for awaiting-source items */}
    {entry.neededSource && (
      <div className="mt-3 rounded-lg p-3" style={{ backgroundColor: '#FDEEDF', borderLeft: '3px solid #F26B1F' }}>
        <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#8C3A0E' }}>
          Find this paper to restore
        </p>
        <p className="text-[12px] leading-relaxed" style={{ color: '#8C3A0E' }}>{entry.neededSource}</p>
      </div>
    )}
  </div>
);

const CutContentPage: React.FC<CutContentPageProps> = ({ onBack }) => {
  const entries = CUT_CONTENT;
  const awaiting = entries.filter(e => e.awaitingSource);
  const resolved = entries.filter(e => !e.awaitingSource);

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#f0f0f0' }}>
      {/* Header */}
      <header
        className="sticky top-0 z-30 px-4 md:px-10 bg-[#f0f0f0]/90 backdrop-blur-sm border-b"
        style={{ borderColor: '#d0cdc8', paddingTop: 'calc(16px + var(--sat, 0px))', paddingBottom: '16px' }}
      >
        <div className="max-w-3xl mx-auto flex items-center gap-4">
          <button
            onClick={onBack}
            className="p-2.5 rounded-xl transition-colors hover:bg-white"
            style={{ border: '1px solid rgba(0,0,0,0.08)', backgroundColor: 'white' }}
            aria-label="Back"
          >
            <ArrowLeft size={18} style={{ color: '#1a1a1a' }} />
          </button>
          <div className="flex items-center gap-2.5">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center"
              style={{ backgroundColor: '#FDEEDF', border: '1.5px solid rgba(242,107,31,0.3)' }}
            >
              <Scissors size={18} style={{ color: '#F26B1F' }} />
            </div>
            <div>
              <h1 className="text-lg font-semibold leading-tight" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
                Cut Content
              </h1>
              <p className="text-[11px]" style={{ color: '#9e9186' }}>Pre-accreditation review log</p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-3xl mx-auto px-4 md:px-10 py-6 md:py-8">
        {/* Disclaimer */}
        <div
          className="rounded-xl p-4 mb-6"
          style={{ backgroundColor: '#FDEEDF', borderLeft: '3px solid #F26B1F' }}
        >
          <p className="text-[13px] leading-relaxed italic" style={{ color: '#8C3A0E' }}>
            This is a page of content cut because it couldn&apos;t be verified in advance of the meeting with
            Brian MacCraith. Each entry records the module and sub-module it came from, the original wording, and
            why it was removed or reframed.
          </p>
        </div>

        {/* Entries */}
        {entries.length === 0 ? (
          <div
            className="rounded-2xl p-10 text-center"
            style={{ backgroundColor: 'white', border: '2px dashed #d0cdc8' }}
          >
            <div className="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center" style={{ backgroundColor: '#f0f0f0' }}>
              <FileText size={22} style={{ color: '#b0a898' }} />
            </div>
            <p className="text-sm font-medium" style={{ color: '#7a7068' }}>Nothing cut yet</p>
            <p className="text-xs mt-1" style={{ color: '#9e9186' }}>
              As the module review proceeds, removed and reframed content will be logged here.
            </p>
          </div>
        ) : (
          <>
            {/* Awaiting references — reframed only because a primary source is
                paywalled; restorable once the PDF is supplied. */}
            {awaiting.length > 0 && (
              <section className="mb-8">
                <div className="rounded-xl p-4 mb-4" style={{ backgroundColor: 'white', border: '2px solid #F26B1F' }}>
                  <p className="text-xs font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#8C3A0E' }}>
                    Awaiting references · {awaiting.length}
                  </p>
                  <p className="text-[13px] leading-relaxed" style={{ color: '#7a7068' }}>
                    These statements were reframed <span style={{ fontWeight: 600 }}>only</span> because their source
                    paper is paywalled and the exact wording couldn&apos;t be verified against the primary source.
                    Dig out the paper noted on each card and the original can be restored verbatim.
                  </p>
                </div>
                <div className="space-y-4">
                  {awaiting.map(entry => (
                    <CutEntryCard key={entry.id} entry={entry} />
                  ))}
                </div>
              </section>
            )}

            {/* Reframed / removed for good */}
            {resolved.length > 0 && (
              <section>
                <p className="text-xs font-bold uppercase tracking-[0.12em] mb-3" style={{ color: '#9e9186' }}>
                  Reframed &amp; removed · {resolved.length}
                </p>
                <div className="space-y-4">
                  {resolved.map(entry => (
                    <CutEntryCard key={entry.id} entry={entry} />
                  ))}
                </div>
              </section>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default CutContentPage;
