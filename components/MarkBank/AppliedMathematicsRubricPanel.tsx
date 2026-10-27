import React, { useEffect, useState } from 'react';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import type { AppliedMathematicsRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import CropView from '../PaperTrail/CropView';
import { paperStoragePath, paperUrl } from '../PaperTrail/storage';
import { vaultPdf } from '../PaperTrail/vaultDocs';
import { resolveSubjectId } from '../../curriculumRegistry';

export type AppliedMathematicsScoreId = `applied:${string}:${'credit' | 'errors' | 'slips'}`;
export type AppliedMathematicsScores = Partial<Record<AppliedMathematicsScoreId, number>>;

export function appliedMathematicsMarks(card: SecRubricCard, scores: AppliedMathematicsScores): number {
  if (card.rubric.system !== 'applied-mathematics') return 0;
  return card.rubric.allocations.reduce((total, item) => {
    const credit = scores[`applied:${item.id}:credit`] ?? 0;
    if (!item.credit.includes(credit)) return total;
    const count = (type: 'errors' | 'slips') => {
      const value = scores[`applied:${item.id}:${type}`] ?? 0;
      return Number.isFinite(value) ? Math.max(0, Math.floor(value)) : 0;
    };
    return total + Math.max(0, credit - 3 * count('errors') - count('slips'));
  }, 0);
}

/** The scheme document the card's steps are cut from, loaded once for every step's crop. */
function useSchemePdf(card: SecRubricCard & { rubric: AppliedMathematicsRubric }, wanted: boolean) {
  const [pdf, setPdf] = useState<PDFDocumentProxy | null>(null);
  const [failed, setFailed] = useState(false);
  const source = card.rubric.solution;
  const fileid = (source.sourceFileid ?? card.paperFileid ?? '').replace(/(\.pdf)?$/i, '.pdf');
  const url = paperUrl(paperStoragePath('lc', resolveSubjectId(card.subjectId) ?? card.subjectId, source.sourceYear ?? card.year, 'scheme', fileid));
  useEffect(() => {
    if (!wanted) return;
    let cancelled = false;
    setFailed(false);
    vaultPdf(url).then(doc => { if (!cancelled) setPdf(doc); }).catch(() => { if (!cancelled) setFailed(true); });
    return () => { cancelled = true; };
  }, [url, wanted]);
  return { pdf, failed };
}

/** The lines a published step prices, cut from the scheme page (reviewed.json allocation.region, am_steps.py):
 * the step's content shown, since the equation-editor text layer cannot be read as words. */
const StepCrop: React.FC<{ label: string; region: { p: number; r: [number, number, number, number] }; pdf: PDFDocumentProxy | null; failed: boolean }> =
  ({ label, region, pdf, failed }) => (
    <div className="mb-applied-step" aria-label={`${label}: the lines it prices`}>
      {pdf ? (
        <CropView pdf={pdf} region={[{ p: region.p, r: region.r }]} trim maxWidth={720}
          ariaLabel={() => `${label}, the scheme's own lines for this step — © State Examinations Commission`}
          failText="This step could not be rendered. Open the worked solution above." />
      ) : failed ? <p className="mb-source-reader-failed">This step could not be loaded. Open the worked solution above.</p>
        : <p aria-busy="true">Loading the step…</p>}
    </div>
  );

const AppliedMathematicsRubricPanel: React.FC<{
  card: SecRubricCard & { rubric: AppliedMathematicsRubric };
  scores: AppliedMathematicsScores;
  onScore: (id: AppliedMathematicsScoreId, marks: number) => void;
}> = ({ card, scores, onScore }) => {
  const cut = card.rubric.allocations.some(item => item.region);
  const { pdf, failed } = useSchemePdf(card, cut);
  return (
    <div className="mb-applied-scheme">
      <p>{cut ? 'Each step shows the scheme\u2019s own lines for it; place your credit on each.' : 'Compare your working with the official solution, including any diagrams.'}</p>
      <SourceMaterialReader
        source={card.rubric.solution}
        subjectId={card.subjectId}
        year={card.year}
        paperFileid={card.rubric.solution.sourceFileid ?? card.paperFileid!}
      />
      <p>{card.rubric.markingGuideNote}</p>
      {card.rubric.allocations.map(item => (
        <fieldset key={item.id}>
          <legend>{item.label} · {Math.max(...item.credit)} marks</legend>
          {item.region && <StepCrop label={item.label} region={item.region} pdf={pdf} failed={failed} />}
          {item.guidance && <p>{item.guidance}</p>}
          <div className="mb-applied-credit" aria-label={`${item.label} credit`}>
            {item.credit.map(mark => (
              <button
                type="button" key={mark}
                aria-label={`Set ${item.label} to ${mark} marks`}
                aria-pressed={(scores[`applied:${item.id}:credit`] ?? 0) === mark}
                onClick={() => onScore(`applied:${item.id}:credit`, mark)}
              >{mark}</button>
            ))}
          </div>
          <div className="mb-applied-deductions">
            {(['errors', 'slips'] as const).map(type => (
              <label key={type}>
                {type === 'errors' ? 'Mathematical errors (−3 each)' : 'Slips or minor misreadings (−1 each)'}
                <input type="number" min={0} step={1}
                  aria-label={`${item.label} ${type}`}
                  value={scores[`applied:${item.id}:${type}`] ?? 0}
                  onChange={event => onScore(`applied:${item.id}:${type}`, Math.max(0, Math.floor(Number(event.target.value) || 0)))}
                />
              </label>
            ))}
          </div>
        </fieldset>
      ))}
      <p aria-live="polite"><strong>Your mark: {appliedMathematicsMarks(card, scores)} / {card.totalMarks}</strong></p>
    </div>
  );
};

export default AppliedMathematicsRubricPanel;
