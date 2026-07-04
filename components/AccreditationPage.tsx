/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, Printer, ShieldCheck, BadgeCheck, AlertTriangle } from 'lucide-react';
import { ACCREDITATION } from '../data/accreditation';
import { REF } from '../data/references/library';
import { type Reference } from '../data/references/types';
import { CUT_CONTENT } from '../data/cutContent';

interface AccreditationPageProps {
  onBack: () => void;
}

const SERIF = "'Source Serif 4', serif";
const SANS = "'DM Sans', sans-serif";

// Mercury / data-dense palette
const INK = '#1a1a1a';
const HAIRLINE = '#EDEBE8';
const PAGE = '#f0f0f0';
const PANEL = '#FAF7F4';
const BODY = '#5a5550';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const ACCENT = '#F26B1F';
const ACCENT_TINT = '#FDEEDF';
const ACCENT_DARK_TEXT = '#8C3A0E';
const SUCCESS = '#3A8D5F';
const SUCCESS_TINT = '#E8F2EC';
const SUCCESS_DARK_TEXT = '#1F5F3E';
const FAINT = '#b0a898';

const MicroLabel: React.FC<{ children: React.ReactNode; color?: string; className?: string }> = ({
  children,
  color = LABEL,
  className = '',
}) => (
  <p className={`text-[10px] font-bold uppercase tracking-[0.14em] ${className}`} style={{ color, fontFamily: SANS }}>
    {children}
  </p>
);

const Stat: React.FC<{ value: number | string; label: string; accent?: boolean }> = ({ value, label, accent }) => (
  <div className="flex flex-col gap-1">
    <span className="text-4xl md:text-5xl font-semibold leading-none" style={{ fontFamily: SERIF, color: accent ? ACCENT : INK }}>
      {value}
    </span>
    <MicroLabel>{label}</MicroLabel>
  </div>
);

const SectionHeading: React.FC<{ eyebrow: string; title: string }> = ({ eyebrow, title }) => (
  <div className="mb-4">
    <MicroLabel color={ACCENT}>{eyebrow}</MicroLabel>
    <h2 className="text-[19px] md:text-[21px] font-semibold mt-1" style={{ fontFamily: SERIF, color: INK }}>
      {title}
    </h2>
  </div>
);

const isOfficial = (r: Reference) => r.kind === 'official';

// One row in the full reference list: the citation + a kind tag + a resolvable link.
const RefRow: React.FC<{ r: Reference; n: number }> = ({ r, n }) => {
  const official = isOfficial(r);
  const link = r.doi
    ? { href: `https://doi.org/${r.doi}`, label: `doi:${r.doi}` }
    : r.url
    ? { href: r.url, label: r.url.replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, '') }
    : null;
  return (
    <div className="flex gap-3 py-3" style={{ borderTop: `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}>
      <span className="shrink-0 w-7 text-right text-[12px] font-semibold tabular-nums pt-0.5" style={{ color: FAINT, fontFamily: SANS }}>
        {n}
      </span>
      <div className="min-w-0">
        <p className="text-[13.5px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>
          {r.authors} ({r.year}). {r.title}. <span className="italic">{r.source}</span>.
        </p>
        <div className="flex flex-wrap items-center gap-x-2.5 gap-y-1 mt-1">
          <span
            className="inline-flex items-center px-2 py-0.5 rounded-full text-[9.5px] font-bold uppercase tracking-[0.08em]"
            style={
              official
                ? { backgroundColor: ACCENT_TINT, color: ACCENT_DARK_TEXT, border: `1px solid rgba(242,107,31,0.25)` }
                : { backgroundColor: SUCCESS_TINT, color: SUCCESS_DARK_TEXT, border: `1px solid rgba(58,141,95,0.3)` }
            }
          >
            {official ? 'Official source' : 'Peer-reviewed'}
          </span>
          {link && (
            <a
              href={link.href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[11.5px] underline decoration-dotted underline-offset-2 break-all"
              style={{ color: MUTED, fontFamily: SANS }}
            >
              {link.label}
            </a>
          )}
          {r.repoPath && (
            <span className="text-[11px]" style={{ color: FAINT, fontFamily: SANS }}>
              · in repo: {r.repoPath}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

const AccreditationPage: React.FC<AccreditationPageProps> = ({ onBack }) => {
  const a = ACCREDITATION;

  const accredited = a.coverage.reduce((s, g) => s + g.accredited, 0);
  const sources = Object.keys(REF).length;
  const changes = CUT_CONTENT.length;
  const subjectGroup = a.coverage.find(g => g.name.toLowerCase().includes('subject'));
  const subjectsPending = subjectGroup ? subjectGroup.total - subjectGroup.accredited : 0;
  const v = a.verification;
  const verificationReady = v.claimsChecked > 0;

  const [tab, setTab] = useState<'overview' | 'references'>('overview');
  const [refFilter, setRefFilter] = useState<'all' | 'paper' | 'official'>('all');

  // Every source on the site, alphabetised — the full bibliography.
  const allRefs = useMemo(
    () => Object.values(REF).slice().sort((x, y) => x.authors.localeCompare(y.authors)),
    []
  );
  const officialCount = useMemo(() => allRefs.filter(isOfficial).length, [allRefs]);
  const paperCount = allRefs.length - officialCount;
  const refChips: { key: 'all' | 'paper' | 'official'; label: string; count: number }[] = [
    { key: 'all', label: 'All', count: allRefs.length },
    { key: 'paper', label: 'Peer-reviewed', count: paperCount },
    { key: 'official', label: 'Official (SEC / CAO)', count: officialCount },
  ];
  const refMatches = (r: Reference) =>
    refFilter === 'all' || (refFilter === 'official' ? isOfficial(r) : !isOfficial(r));

  const overviewCls = tab === 'overview' ? '' : 'hidden print:block';
  const referencesCls = tab === 'references' ? '' : 'hidden print:block';

  return (
    <div className="min-h-screen print:bg-white" style={{ backgroundColor: PAGE }}>
      {/* Masthead */}
      <header
        className="sticky top-0 z-30 px-4 md:px-10 bg-[#f0f0f0]/90 backdrop-blur-sm border-b print:static print:bg-white print:backdrop-blur-none"
        style={{ borderColor: HAIRLINE, paddingTop: 'calc(16px + var(--sat, 0px))', paddingBottom: '16px' }}
      >
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-4 min-w-0">
            <button
              onClick={onBack}
              className="p-2.5 rounded-xl transition-colors hover:bg-white print:hidden shrink-0"
              style={{ border: '1px solid rgba(0,0,0,0.08)', backgroundColor: 'white' }}
              aria-label="Back"
            >
              <ArrowLeft size={18} style={{ color: INK }} />
            </button>
            <div className="min-w-0">
              <MicroLabel color={ACCENT}>Pre-accreditation review · DCU</MicroLabel>
              <h1 className="text-lg md:text-xl font-semibold leading-tight mt-0.5" style={{ fontFamily: SERIF, color: INK }}>
                Accreditation Dossier
              </h1>
            </div>
          </div>
          <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-[13px] font-semibold transition-colors hover:bg-white print:hidden shrink-0"
            style={{ border: '1px solid rgba(0,0,0,0.1)', backgroundColor: 'white', color: MUTED, fontFamily: SANS }}
          >
            <Printer size={15} />
            <span className="hidden sm:inline">Export / Print</span>
          </button>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 md:px-10 py-6 md:py-9">
        {/* Lede */}
        <p className="text-[15px] md:text-[16px] leading-relaxed mb-6" style={{ color: BODY, fontFamily: SANS, maxWidth: '52ch' }}>
          A record of how every claim in the Learning Lab was checked against the evidence before review — what is
          backed, how it was verified, and what is honestly still in progress.
        </p>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 p-1 rounded-xl print:hidden" style={{ backgroundColor: 'white', border: `1px solid ${HAIRLINE}`, width: 'fit-content' }}>
          {([
            { key: 'overview' as const, label: 'Overview' },
            { key: 'references' as const, label: `Full reference list (${allRefs.length})` },
          ]).map(t => {
            const active = tab === t.key;
            return (
              <button
                key={t.key}
                onClick={() => setTab(t.key)}
                className="px-4 py-2 rounded-lg text-[13px] font-semibold transition-colors"
                style={{
                  fontFamily: SANS,
                  backgroundColor: active ? ACCENT : 'transparent',
                  color: active ? 'white' : MUTED,
                }}
              >
                {t.label}
              </button>
            );
          })}
        </div>

        {/* ── OVERVIEW TAB ─────────────────────────────────────────────── */}
        <div className={overviewCls}>

        {/* Summary band */}
        <section
          className="rounded-2xl px-5 md:px-8 py-6 md:py-7 mb-5"
          style={{ backgroundColor: 'white', border: `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}
        >
          <div className="grid grid-cols-2 md:grid-cols-4 gap-y-6 gap-x-4 md:gap-x-8">
            <Stat value={accredited} label="Modules accredited" />
            <Stat value={sources} label="Verified sources" />
            <Stat value={changes} label="Audit-trail changes" />
            <Stat value={subjectsPending} label="Subjects in progress" accent />
          </div>
        </section>

        {/* Governing standard */}
        <section
          className="rounded-2xl px-5 md:px-8 py-7 mb-7"
          style={{ backgroundColor: PANEL, border: `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}
        >
          <div className="flex items-center gap-2 mb-3">
            <ShieldCheck size={16} style={{ color: ACCENT }} />
            <MicroLabel color={ACCENT_DARK_TEXT}>The standard every claim is held to</MicroLabel>
          </div>
          <p className="text-[16px] md:text-[18px] leading-relaxed" style={{ fontFamily: SERIF, color: INK }}>
            {a.governingRule}
          </p>
        </section>

        {/* Methodology */}
        <section className="mb-8" style={{ breakInside: 'avoid' }}>
          <SectionHeading eyebrow="Methodology" title="How the evidence was verified" />
          <ol className="space-y-2.5">
            {a.methodology.map((m, i) => (
              <li key={i} className="flex gap-3">
                <span
                  className="shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-[11px] font-bold mt-0.5"
                  style={{ backgroundColor: ACCENT_TINT, color: ACCENT_DARK_TEXT, fontFamily: SANS }}
                >
                  {i + 1}
                </span>
                <p className="text-[14px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>
                  {m}
                </p>
              </li>
            ))}
          </ol>
        </section>

        {/* Coverage */}
        <section className="mb-8" style={{ breakInside: 'avoid' }}>
          <SectionHeading eyebrow="Coverage" title="What has been accredited" />
          <div className="rounded-2xl overflow-hidden" style={{ border: `1px solid ${HAIRLINE}` }}>
            {a.coverage.map((g, i) => {
              const complete = g.accredited >= g.total;
              const pct = Math.round((g.accredited / g.total) * 100);
              const barColor = complete ? SUCCESS : ACCENT;
              return (
                <div
                  key={g.name}
                  className="px-5 md:px-6 py-4 flex flex-col md:flex-row md:items-center gap-3 md:gap-6"
                  style={{ backgroundColor: 'white', borderTop: i === 0 ? 'none' : `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}
                >
                  <div className="md:w-64 shrink-0">
                    <div className="flex items-center gap-2">
                      {complete ? (
                        <BadgeCheck size={15} style={{ color: SUCCESS }} />
                      ) : (
                        <span className="w-[15px] h-[15px] rounded-full" style={{ border: `2px solid ${ACCENT}` }} />
                      )}
                      <span className="text-[14px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
                        {g.name}
                      </span>
                    </div>
                    <p className="text-[11.5px] mt-0.5 ml-[23px]" style={{ color: LABEL, fontFamily: SANS }}>
                      {g.basis}
                    </p>
                  </div>
                  <div className="flex-1 flex items-center gap-3">
                    <div className="flex-1 h-2 rounded-full overflow-hidden" style={{ backgroundColor: '#EDEBE8' }}>
                      <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: barColor }} />
                    </div>
                    <span className="text-[13px] font-semibold tabular-nums shrink-0" style={{ color: complete ? SUCCESS_DARK_TEXT : ACCENT_DARK_TEXT, fontFamily: SANS }}>
                      {g.accredited}/{g.total}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Exam-preparation engine */}
        <section className="mb-8" style={{ breakInside: 'avoid' }}>
          <SectionHeading eyebrow="Exam preparation engine" title="Every SEC paper, made teachable" />
          <div className="rounded-2xl px-5 md:px-8 py-6 md:py-7 mb-4" style={{ backgroundColor: 'white', border: `1px solid ${HAIRLINE}` }}>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-y-6 gap-x-4 md:gap-x-8 mb-5">
              {a.examEngine.stats.map((s, i) => (
                <Stat key={i} value={s.value} label={s.label} accent={s.value.includes('%')} />
              ))}
            </div>
            <p className="text-[13.5px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>
              {a.examEngine.provenance}
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-3">
            {a.examEngine.capabilities.map((c, i) => (
              <div key={i} className="rounded-xl px-4 md:px-5 py-4" style={{ backgroundColor: PANEL, border: `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}>
                <p className="text-[14px] font-semibold mb-1" style={{ fontFamily: SERIF, color: INK }}>{c.title}</p>
                <p className="text-[13px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>{c.detail}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Independent verification */}
        <section className="mb-8" style={{ breakInside: 'avoid' }}>
          <SectionHeading eyebrow="Independent re-verification" title="A second, adversarial check" />
          <div className="rounded-2xl px-5 md:px-8 py-6" style={{ backgroundColor: 'white', border: `1px solid ${HAIRLINE}` }}>
            {verificationReady ? (
              <>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-y-5 gap-x-4 md:gap-x-8 mb-5">
                  <Stat value={v.modulesAudited} label="Modules re-audited" />
                  <Stat value={v.claimsChecked} label="Claims re-checked" />
                  <Stat value={v.modulesClean} label="Modules fully clean" />
                  <Stat value={`${v.issuesUpheld}→0`} label="Issues found & fixed" accent={v.issuesUpheld > 0} />
                </div>
                <p className="text-[13.5px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>
                  {v.method}
                </p>
              </>
            ) : (
              <p className="text-[13.5px] leading-relaxed" style={{ color: MUTED, fontFamily: SANS }}>
                An independent reviewer per module is re-checking that each citation supports its specific claim, with
                every issue re-tested before being upheld. Results are added here on completion.
              </p>
            )}
          </div>
        </section>

        {/* Known limitations */}
        <section className="mb-8" style={{ breakInside: 'avoid' }}>
          <SectionHeading eyebrow="In the open" title="Known limitations" />
          <div className="space-y-3">
            {a.limitations.map((l, i) => (
              <div
                key={i}
                className="rounded-xl px-4 md:px-5 py-3.5 flex gap-3"
                style={{ backgroundColor: PANEL, border: `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}
              >
                <AlertTriangle size={15} style={{ color: ACCENT }} className="mt-0.5 shrink-0" />
                <div>
                  <p className="text-[14px] font-semibold mb-0.5" style={{ fontFamily: SERIF, color: INK }}>
                    {l.title}
                  </p>
                  <p className="text-[13px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>
                    {l.detail}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Footer note */}
        <p className="text-[12.5px] leading-relaxed" style={{ color: LABEL, fontFamily: SANS }}>
          The full change-by-change audit trail is on the <strong style={{ color: MUTED }}>Cut Content</strong> page;
          each module also carries a claim-by-claim evidence dossier in the project repository.
        </p>

        </div>{/* ── end OVERVIEW TAB ── */}

        {/* ── REFERENCES TAB ───────────────────────────────────────────── */}
        <div className={referencesCls}>
          <SectionHeading eyebrow="Bibliography" title={`Every source on the site (${allRefs.length})`} />
          <p className="text-[14px] leading-relaxed mb-5" style={{ color: BODY, fontFamily: SANS, maxWidth: '60ch' }}>
            The complete reference set behind the Learning Lab — {paperCount} peer-reviewed papers (each DOI verified on
            CrossRef) and {officialCount} official sources (State Examinations Commission and CAO documents). Every entry
            resolves to a real, locatable record.
          </p>

          {/* Filter chips */}
          <div className="flex flex-wrap gap-2 mb-2 print:hidden">
            {refChips.map(chip => {
              const active = refFilter === chip.key;
              return (
                <button
                  key={chip.key}
                  onClick={() => setRefFilter(chip.key)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-[12.5px] font-semibold transition-colors"
                  style={{
                    fontFamily: SANS,
                    backgroundColor: active ? ACCENT : 'white',
                    color: active ? 'white' : MUTED,
                    border: `1px solid ${active ? ACCENT : HAIRLINE}`,
                  }}
                >
                  {chip.label}
                  <span
                    className="text-[10.5px] font-bold px-1.5 rounded-full"
                    style={{ backgroundColor: active ? 'rgba(255,255,255,0.22)' : '#f0eeec', color: active ? 'white' : FAINT }}
                  >
                    {chip.count}
                  </span>
                </button>
              );
            })}
          </div>

          {/* The list */}
          <div role="list" className="rounded-2xl px-4 md:px-6 py-1" style={{ backgroundColor: 'white', border: `1px solid ${HAIRLINE}` }}>
            {allRefs.map((r, i) => (
              <div role="listitem" key={r.id} className={refMatches(r) ? '' : 'hidden print:block'}>
                <RefRow r={r} n={i + 1} />
              </div>
            ))}
          </div>
          <p className="text-[11.5px] mt-3" style={{ color: LABEL, fontFamily: SANS }}>
            Numbering here is a stable index for the whole site; within each module the inline citations are numbered
            locally in order of appearance.
          </p>
        </div>{/* ── end REFERENCES TAB ── */}

        {/* Print footer */}
        <div className="hidden print:block mt-8 pt-4 text-[10px]" style={{ borderTop: `1px solid ${HAIRLINE}`, color: LABEL, fontFamily: SANS }}>
          Nextstepuni — Accreditation Dossier · Pre-accreditation review (DCU / Brian MacCraith) · as of {a.asOf}
        </div>
      </div>
    </div>
  );
};

export default AccreditationPage;
