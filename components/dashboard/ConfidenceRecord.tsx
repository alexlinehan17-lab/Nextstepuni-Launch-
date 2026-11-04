import React from 'react';
import { averageConfidence, CONFIDENCE_LABELS, type ConfidenceObservation } from './dashboardAnalytics';

/** Every subject stays visible; each average opens into its recorded evidence. */
export default function ConfidenceRecord({ observations, subjects }: {
  observations: ConfidenceObservation[]; subjects: string[];
}) {
  const average = averageConfidence(observations);
  const names = [...new Set([...subjects, ...observations.map(item => item.subject)])];
  return <div className="confidence-record">
    <div className="confidence-record-summary">
      <strong>{average === null ? '—' : average.toFixed(1)}<span> / 5</span></strong>
      <p>{observations.length} reflection{observations.length === 1 ? '' : 's'} in this period{observations.length === 1 ? ' · one observation, not a trend' : ''}.</p>
      <p>How you felt after study. Not a grade prediction.</p>
    </div>
    {names.map(subject => {
      const records = observations.filter(item => item.subject === subject).sort((a, b) => b.timestamp - a.timestamp);
      const score = averageConfidence(records);
      return <details key={subject} className="dashboard-disclosure confidence-subject">
        <summary><div>{subject}<small>{records.length ? `${records.length} reflection${records.length === 1 ? '' : 's'}` : 'No reflections in this period'}</small></div><b>{score === null ? '—' : score.toFixed(1)}</b><span aria-hidden="true">+</span></summary>
        {records.length ? <ul>{records.map(record => <li key={record.id}><time dateTime={new Date(record.timestamp).toISOString()}>{new Date(record.timestamp).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })}</time><span>{CONFIDENCE_LABELS[record.score - 1]} · {record.score}/5</span></li>)}</ul> : <p className="dashboard-disclosure-detail">Add a reflection after a study session to begin your record.</p>}
      </details>;
    })}
  </div>;
}
