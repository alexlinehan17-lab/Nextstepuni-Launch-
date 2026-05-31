/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * MoneySorter — sorts the four kinds of money students conflate (means-based,
 * merit, automatic, admission route) and flags the costly AUTOMATIC-vs-APPLY
 * distinction. Tap an item to reveal the detail + official source.
 */
import React, { useState } from 'react';
import { ChevronDown, ExternalLink } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import { MONEY_ITEMS, MONEY_BUCKETS, type MoneyBucket } from '../../collegeCompassData';

const BUCKET_ORDER: MoneyBucket[] = ['means', 'automatic', 'merit', 'admission'];

const MoneySorter: React.FC = () => {
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-5">
      <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500 mb-1">
        Sort the money
      </p>
      <h4 className="font-serif text-lg font-bold text-[#1A1A1A] dark:text-white mb-4">
        Four kinds of money — which is which?
      </h4>

      <div className="space-y-5">
        {BUCKET_ORDER.map(bucket => {
          const items = MONEY_ITEMS.filter(m => m.bucket === bucket);
          if (items.length === 0) return null;
          const meta = MONEY_BUCKETS[bucket];
          return (
            <div key={bucket}>
              <p className="text-sm font-bold text-[#1A1A1A] dark:text-white">{meta.label}</p>
              <p className="text-xs text-[#7a7068] mb-2">{meta.blurb}</p>
              <div className="space-y-2">
                {items.map(item => {
                  const open = openId === item.id;
                  return (
                    <div
                      key={item.id}
                      className="rounded-xl border-2 overflow-hidden"
                      style={{ borderColor: COLORS.border, backgroundColor: '#FFFFFF' }}
                    >
                      <button
                        type="button"
                        onClick={() => setOpenId(open ? null : item.id)}
                        className="w-full flex items-center gap-2 px-3 py-2.5 text-left"
                      >
                        <span className="text-sm font-semibold text-[#1A1A1A] flex-1 min-w-0">{item.name}</span>
                        <span
                          className="text-[9px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full shrink-0"
                          style={
                            item.isAutomatic
                              ? { backgroundColor: COLORS.successTint, color: COLORS.successDarkText }
                              : { backgroundColor: COLORS.accentTint, color: COLORS.accentDarkText }
                          }
                        >
                          {item.isAutomatic ? 'Automatic' : 'Apply'}
                        </span>
                        <ChevronDown
                          size={15}
                          className="text-zinc-400 shrink-0 transition-transform"
                          style={{ transform: open ? 'rotate(180deg)' : 'rotate(0deg)' }}
                        />
                      </button>
                      {open && (
                        <div className="px-3 pb-3 pt-0">
                          <p className="text-xs text-[#7a7068] leading-relaxed mb-1.5">{item.note}</p>
                          <p className="text-[11px] font-semibold text-[#1A1A1A] mb-2">When: {item.deadlineWindow}</p>
                          <a
                            href={item.sourceUrl}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 text-[11px] font-semibold underline"
                            style={{ color: COLORS.accentDarkText }}
                          >
                            Official source <ExternalLink size={11} />
                          </a>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Verify callout */}
      <div className="mt-4 pl-3 py-1" style={{ borderLeft: `3px solid ${COLORS.accent}` }}>
        <p className="text-xs italic leading-relaxed" style={{ color: COLORS.accentDarkText }}>
          Amounts, thresholds and dates change every year — and SUSI is a grant, not a scholarship. Always confirm on the official source before you rely on a figure.
        </p>
      </div>
    </div>
  );
};

export default MoneySorter;
