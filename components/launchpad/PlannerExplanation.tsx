import React, { useState } from 'react';
import { ArrowRight, ChevronDown } from 'lucide-react';
import ModalFrame from '../ui/ModalFrame';
import type { SubjectPriority, SessionAllocation } from '../timetableAlgorithm';
import { getSubjectFill } from '../../utils/subjectColors';
import './launchpad.css';

interface Props {
  open: boolean;
  onClose: () => void;
  priorities: SubjectPriority[];
  allocations: SessionAllocation[];
  totalSessions: number;
  totalMinutes: number;
  workloadExplanation: string;
}

/** Explains the scores supplied by the planner; it never recalculates allocation. */
export default function PlannerExplanation({ open, onClose, priorities, allocations, totalSessions, totalMinutes, workloadExplanation }: Props) {
  const [selected, setSelected] = useState('');
  const active = priorities.find(p => p.subjectName === selected) ?? priorities[0];
  const ranked = [...priorities].sort((a, b) => b.targetPoints - a.targetPoints);
  const bestSix = ranked.slice(0, 6);
  const outside = ranked.slice(6);
  const targetTotal = bestSix.reduce((sum, p) => sum + p.targetPoints, 0);
  const sessionsFor = (name: string) => allocations.find(a => a.subjectName === name)?.sessions ?? 0;
  const gain = active ? active.bestSixPointsGain ?? active.pointsGain : 0;
  return (
    <ModalFrame open={open} onClose={onClose} width="xl" eyebrow="The Planner · Behind your plan" title="A little more time where it counts." labelledBy="planner-explanation-title">
      <div className="lp-plan-explanation">
        <p className="lp-plan-intro">Your targets set the direction. Your topic confidence helps decide where to spend the time. Every subject keeps a place in the week.</p>
        {active && <div className="lp-plan-inspector">
          <nav className="lp-plan-subjects" aria-label="Inspect a subject’s allocation">
            <p className="lp-eyebrow">Your subjects <span>Blocks</span></p>
            {priorities.map(p => <button key={p.subjectName} type="button" aria-label={`Inspect ${p.subjectName} allocation`} aria-pressed={p.subjectName === active.subjectName} onClick={() => setSelected(p.subjectName)}>
              <i aria-hidden="true" style={{ background: getSubjectFill(p.subjectName) }} />
              <span>{p.subjectName}</span><b>{sessionsFor(p.subjectName)}</b>
            </button>)}
          </nav>
          <div className="lp-plan-mobile-picker">
            <label htmlFor="planner-inspect-subject">Look at a subject</label>
            <div><select id="planner-inspect-subject" value={active.subjectName} onChange={e => setSelected(e.target.value)}>{priorities.map(p => <option key={p.subjectName}>{p.subjectName}</option>)}</select><ChevronDown size={17} aria-hidden="true" /></div>
          </div>
          <section className="lp-plan-detail" aria-label={`${active.subjectName} allocation details`}>
            <div className="lp-plan-detail-heading">
              <div><p className="lp-eyebrow">A closer look</p><h3><i aria-hidden="true" style={{ background: getSubjectFill(active.subjectName) }} />{active.subjectName}</h3><p className="lp-plan-grades">{active.currentGrade} <ArrowRight size={15} aria-label="to" /> {active.targetGrade}<span>Your target</span></p></div>
              <p className="lp-plan-block-count"><strong>{sessionsFor(active.subjectName)}</strong><span>{sessionsFor(active.subjectName) === 1 ? 'block' : 'blocks'} this week</span></p>
            </div>
            <dl className="lp-plan-factors">
              <div><dt><span>01</span> Points to gain</dt><dd>+{gain}</dd><p>Added to your current best-six total if you reach this target{active.isMaths ? ', including any Higher Maths bonus' : ''}.</p></div>
              <div><dt><span>02</span> Grade steps</dt><dd>×{active.difficultyMultiplier.toFixed(2)}</dd><p>{(active.targetGradeSteps ?? 0) > 0 ? `${active.targetGradeSteps} grade ${(active.targetGradeSteps ?? 0) === 1 ? 'step' : 'steps'} to your target. Closer targets receive a larger weight.` : 'You are at or above your target. The plan keeps time for maintenance.'}</p></div>
              <div><dt><span>03</span> Topic confidence</dt><dd>×{active.coverageMultiplier.toFixed(2)}</dd><p>{active.coverageMultiplier > 1 ? 'A little extra weight for topics you marked shaky or not started.' : 'No extra weighting from your topic confidence at the moment.'}</p></div>
            </dl>
            <div className="lp-plan-score"><span>Priority score</span><span>{gain} × {active.difficultyMultiplier.toFixed(2)} × {active.coverageMultiplier.toFixed(2)} ≈ <strong>{active.priorityScore.toFixed(1)}</strong></span></div>
            <p className="lp-plan-footnote">{gain === 0 && active.pointsGain > 0 ? 'This grade improvement would not change your current best-six total. You still receive maintenance time.' : gain === 0 ? 'Your target is already met. Regular maintenance helps keep what you know.' : 'This score is weighed alongside your other subjects, then fitted into whole study blocks. Spaced review can also affect the allocation.'}</p>
          </section>
        </div>}
        <div className="lp-plan-outlook">
          <section className="lp-plan-target" aria-label="Projected CAO points">
            <p className="lp-eyebrow">If you reach every target</p><p className="lp-plan-total"><strong>{targetTotal}</strong><span>/ 625 points</span></p>
            <p>Your highest six subjects make up this total.</p>
            <ol>{bestSix.map(p => <li key={p.subjectName}><i aria-hidden="true" style={{ background: getSubjectFill(p.subjectName) }} /><span>{p.subjectName}</span><small>{p.targetGrade}</small><b>{p.targetPoints}</b></li>)}</ol>
            {outside.length > 0 && <p className="lp-plan-outside"><strong>Outside this projected six:</strong> {outside.map(p => `${p.subjectName} (${p.targetGrade}, ${p.targetPoints} pts)`).join('; ')}. These subjects still receive study time.</p>}
          </section>
          <section className="lp-plan-week"><p className="lp-eyebrow">Room for the whole week</p><h3>{totalSessions} focused blocks.<br />{Math.floor(totalMinutes / 60)}h{totalMinutes % 60 ? ` ${totalMinutes % 60}m` : ''} of study.</h3><p>{workloadExplanation}</p><p>Blocks are spread across your available days, with repeat sessions spaced apart. The plan keeps maintenance time for every subject.</p><p className="lp-plan-footnote">Change your grades, topic confidence or available days and the plan adjusts with you.</p></section>
        </div>
      </div>
    </ModalFrame>
  );
}
