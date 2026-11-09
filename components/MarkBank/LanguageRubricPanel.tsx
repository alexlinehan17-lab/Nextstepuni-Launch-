import React from 'react';
import type { LanguageWritingRubric, LanguageWritingCriterion, LanguagePointsRubric, SecRubricCard } from '../../types/markBank';
import { ClaimRow, MarkStrip } from './ClaimRows';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageCriterionLimits, languageCriterionValue, languageOtherLanguageId, type LanguageScoreId, type LanguageScores } from './languageScoring';
import './language-rubric.css';

export default function LanguageRubricPanel({ card, scores, onScore }: {
  card: SecRubricCard & { rubric: LanguageWritingRubric | LanguagePointsRubric };
  scores: LanguageScores;
  onScore: (id: LanguageScoreId, marks: number) => void;
}) {
  const { rubric } = card;
  const writingRubric: LanguageWritingRubric = { ...rubric, system: 'language-writing', criteria: rubric.criteria ?? [] };
  const conditions = writingRubric.criteria.flatMap(criterion => (criterion.limits ?? []).flatMap(limit => limit.when.any));
  const lengths = [...new Set(conditions.flatMap(condition => 'length' in condition ? [condition.length] : []))];
  const flags = [...new Map(conditions.flatMap(condition => 'flag' in condition ? [[condition.flag, condition] as const] : [])).values()];
  const selectedGroups = rubric.system === 'language-points' ? rubric.groups.filter(group => scores[languageGroupId(group.id)] === 1).length : 0;
  const claimedDetails = rubric.system === 'language-points' ? rubric.groups
    .filter(group => scores[languageGroupId(group.id)] === 1)
    .reduce((sum, group) => sum + group.rows.filter(row => (scores[languageRowId(group.id, row.id)] ?? 0) > 0).length, 0) : 0;
  const renderCriterion = (criterion: LanguageWritingCriterion, criterionRubric: LanguageWritingRubric, disabled = false) => {
      const limits = languageCriterionLimits(criterionRubric, criterion, scores, [criterion.id]);
      const cap = Math.min(criterion.maxMarks, ...limits.map(limit => limit.maxMarks));
      const selected = Math.min(scores[languageScoreId(criterion.id)] ?? 0, cap);
      const bands = ([...limits].sort((a, b) => a.maxMarks - b.maxMarks).find(limit => limit.bands)?.bands ?? criterion.bands)
        ?.filter(band => Math.max(...band.marks) <= cap);
      const permitted = criterion.permittedMarks.filter(mark => mark <= cap);
      return <section className="mb-language-criterion" key={criterion.id}>
        <div className="mb-language-heading"><h4>{criterion.label}</h4><span>{criterion.kind === 'deduction' ? 'Deduction' : `Up to ${cap} marks`}</span></div>
        {criterion.guidance.map((text, index) => <p key={index}>{text}</p>)}
        {limits.flatMap(limit => limit.guidance).map((text, index) => <p className="mb-language-rule" key={index}>{text}</p>)}
        {bands?.map(band => <div className="mb-language-band" key={band.label}>
          <strong>{band.marks[0]}–{band.marks.at(-1)} marks · {band.label}</strong>
          <ul>{band.guidance.map((text, index) => <li key={index}>{text}</li>)}</ul>
        </div>)}
        <MarkStrip disabled={disabled} label={criterion.label} marks={permitted} selected={selected} onSelect={mark => onScore(languageScoreId(criterion.id), mark)} />
        {criterion.kind !== 'deduction' && languageCriterionValue(criterionRubric, criterion.id, scores) !== selected && <p>After published deductions: {languageCriterionValue(criterionRubric, criterion.id, scores)} marks.</p>}
      </section>;
  };
  const otherLanguageControl = (target: string, label: string, disabled = false) => card.answerLanguageRule && <label className="mb-language-flag">
    <input type="checkbox" disabled={disabled || (target !== 'response' && scores[languageOtherLanguageId('response')] === 1)} aria-label={`${label} answered in another language`}
      checked={scores[languageOtherLanguageId(target)] === 1}
      onChange={event => onScore(languageOtherLanguageId(target), event.currentTarget.checked ? 1 : 0)} />
    <span>{target === 'response' && rubric.system === 'language-points' ? 'All answers use' : 'This answer uses'} a language other than specified · {card.answerLanguageRule.otherLanguageMultiplier === 0 ? 'no credit' : 'half credit'}</span>
  </label>;
  return <div className="mb-language-rubric">
    <h3>Assess your response</h3>
    <ul>{rubric.taskRequirements.map((text, index) => <li key={index}>{text}</li>)}</ul>
    {lengths.map(unit => <label className="mb-language-length" key={unit}>
      Response length ({unit})
      <input type="number" min="0" step="1" value={(scores[languageLengthId(unit)] ?? -1) < 0 ? '' : scores[languageLengthId(unit)]}
        onChange={event => onScore(languageLengthId(unit), event.currentTarget.value === '' ? -1 : Math.max(0, Math.floor(Number(event.currentTarget.value))))} />
      <span>Enter the length to apply the scheme’s expression scale.</span>
    </label>)}
    {flags.map(condition => <label className="mb-language-flag" key={condition.flag}>
      <input type="checkbox" checked={scores[languageFlagId(condition.flag)] === 1}
        onChange={event => onScore(languageFlagId(condition.flag), event.currentTarget.checked ? 1 : 0)} />
      <span>{condition.prompt}</span>
    </label>)}
    {writingRubric.criteria.map(criterion => renderCriterion(criterion, writingRubric))}
    {rubric.system === 'language-writing' && otherLanguageControl('response', 'Response')}
    {rubric.system === 'language-points' && <>
      {otherLanguageControl('response', 'All answers')}
      <p>{rubric.allocationCap?.answerCount
        ? `Select up to ${rubric.count} groups, then claim up to ${rubric.allocationCap.answerCount} details in total.`
        : `Select the ${rubric.count} items you answered, then claim each component.`}</p>
      {rubric.allocationCap && <>
        <p>These answers earn up to {rubric.allocationCap.maxMarks} marks altogether.</p>
        <p>{rubric.allocationCap.sourceText}</p>
      </>}
      {rubric.groups.map(group => {
        const selected = scores[languageGroupId(group.id)] === 1;
        const claimed = group.rows.filter(row => (scores[languageRowId(group.id, row.id)] ?? 0) > 0).length;
        return <section className="mb-language-criterion" key={group.id}>
          <button type="button" className="mb-language-choice" aria-pressed={selected}
            disabled={!selected && selectedGroups >= rubric.count}
            onClick={() => onScore(languageGroupId(group.id), selected ? 0 : 1)}>{group.label}</button>
          {group.rows.map(row => {
            const value = scores[languageRowId(group.id, row.id)] ?? 0;
            const quotaReached = claimed >= (group.answerCount ?? group.rows.length)
              || claimedDetails >= (rubric.allocationCap?.answerCount ?? Infinity);
            return <React.Fragment key={row.id}><ClaimRow text={row.text} marks={row.marks} steps={row.steps} claimed={value > 0} value={value} disabled={!selected || (value === 0 && quotaReached)}
              onToggle={() => onScore(languageRowId(group.id, row.id), value ? 0 : 1)}
              onStep={mark => onScore(languageRowId(group.id, row.id), value === mark ? 0 : mark)} />
              {otherLanguageControl(`row:${group.id}:${row.id}`, row.text, !selected)}
            </React.Fragment>;
          })}
          {group.criteria?.map(criterion => renderCriterion(criterion, { ...writingRubric, criteria: group.criteria! }, !selected))}
          {!!group.criteria?.length && otherLanguageControl(`group:${group.id}`, group.label, !selected)}
        </section>;
      })}
    </>}
    <div className="mb-language-total"><span>Your placement</span><strong>{languageMarks(card, scores)} / {card.totalMarks}</strong></div>
    <p>{rubric.markingGuideNote}</p>
    {card.answerLanguageRule && <p>{card.answerLanguageRule.sourceText}</p>}
  </div>;
}
