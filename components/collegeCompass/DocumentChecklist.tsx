/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * DocumentChecklist — turns the HEAR/DARE self-checks into a personalised list
 * of what to gather and post. Reacts live to the selections in HearMeter and
 * DareGate above it. Guide only — the live handbook is the source of truth.
 */
import React from 'react';
import { FileText, Mail, ShieldCheck, Laptop, Stethoscope } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import { buildDocumentPack, DOCUMENT_DEADLINE_NOTE } from '../../collegeCompassData';

interface DocumentChecklistProps {
  hearIndicators: string[];
  dareCategoryId?: string;
}

const PostRow: React.FC<{ icon: React.ElementType; tint: string; iconColor: string; text: string; muted?: boolean }> = ({ icon: Icon, tint, iconColor, text, muted }) => (
  <div className="flex items-start gap-2.5">
    <span className="inline-flex items-center justify-center w-6 h-6 rounded-lg shrink-0 mt-0.5" style={{ backgroundColor: tint }}>
      <Icon size={13} style={{ color: iconColor }} />
    </span>
    <p className={`text-xs leading-relaxed ${muted ? 'text-[#7a7068]' : 'text-[#1A1A1A] dark:text-zinc-200'}`}>{text}</p>
  </div>
);

const DocumentChecklist: React.FC<DocumentChecklistProps> = ({ hearIndicators, dareCategoryId }) => {
  const pack = buildDocumentPack(hearIndicators, dareCategoryId);
  const totalToPost = pack.hear.toPost.length + pack.dare.toPost.length;
  const nothing = !pack.hear.applying && !pack.dare.applying;

  return (
    <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-5">
      <div className="flex items-start gap-3 mb-3">
        <span className="inline-flex items-center justify-center w-9 h-9 rounded-xl shrink-0" style={{ backgroundColor: COLORS.accentTint }}>
          <FileText size={17} style={{ color: COLORS.accent }} />
        </span>
        <div className="min-w-0 flex-1">
          <h4 className="font-serif text-lg font-bold text-[#1A1A1A] dark:text-white leading-tight">Your document pack</h4>
          <p className="text-xs text-[#7a7068]">Built from your answers above</p>
        </div>
        {totalToPost > 0 && (
          <span className="text-[10px] font-bold uppercase tracking-wide px-2.5 py-1 rounded-full shrink-0" style={{ backgroundColor: COLORS.accentTint, color: COLORS.accentDarkText }}>
            {totalToPost} to post
          </span>
        )}
      </div>

      {nothing ? (
        <div className="rounded-xl px-4 py-6 text-center" style={{ backgroundColor: '#F9F9F7' }}>
          <p className="text-sm text-[#7a7068] leading-relaxed">
            Tick your situation in the HEAR and DARE checkers above — your exact list of what to gather and post builds itself here.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* HEAR */}
          {pack.hear.applying && (
            <div>
              <p className="text-[10px] font-bold uppercase tracking-[0.15em] mb-2" style={{ color: '#2A7D6F' }}>For HEAR</p>
              <div className="space-y-1.5">
                {pack.hear.toPost.map((t, i) => (
                  <PostRow key={`hp${i}`} icon={Mail} tint={COLORS.accentTint} iconColor={COLORS.accent} text={t} />
                ))}
                {pack.hear.autoVerified.map((t, i) => (
                  <PostRow key={`ha${i}`} icon={ShieldCheck} tint={COLORS.successTint} iconColor={COLORS.success} text={t} muted />
                ))}
              </div>
            </div>
          )}

          {/* DARE */}
          {pack.dare.applying && (
            <div>
              <p className="text-[10px] font-bold uppercase tracking-[0.15em] mb-2" style={{ color: '#2A7D6F' }}>For DARE</p>
              <div className="space-y-1.5">
                {pack.dare.online.map((t, i) => (
                  <PostRow key={`do${i}`} icon={Laptop} tint="#EAF1F8" iconColor="#2C4B6E" text={t} />
                ))}
                {pack.dare.toPost.map((t, i) => (
                  <PostRow key={`dp${i}`} icon={Mail} tint={COLORS.accentTint} iconColor={COLORS.accent} text={t} />
                ))}
              </div>
              {pack.dare.categoryReqs.length > 0 && (
                <div className="mt-2 rounded-xl p-3" style={{ backgroundColor: '#F9F9F7' }}>
                  {pack.dare.categoryReqs.map((t, i) => (
                    <PostRow key={`dc${i}`} icon={Stethoscope} tint="#FFFFFF" iconColor={COLORS.success} text={t} />
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Deadline note — sanctioned left-border callout */}
          <div className="pl-3 py-1" style={{ borderLeft: `3px solid ${COLORS.accent}` }}>
            <p className="text-xs leading-relaxed" style={{ color: COLORS.accentDarkText }}>{DOCUMENT_DEADLINE_NOTE}</p>
          </div>

          <p className="text-[11px] text-[#7a7068] leading-relaxed">
            A guide, not the official list. Confirm exactly what to send on{' '}
            <a href="https://accesscollege.ie" target="_blank" rel="noreferrer" className="underline font-semibold">accesscollege.ie</a>.
          </p>
        </div>
      )}
    </div>
  );
};

export default DocumentChecklist;
