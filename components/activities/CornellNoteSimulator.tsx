import React, { useId, useState } from 'react';

export default function CornellNoteSimulator() {
  const fieldId = useId();
  const [mainNotes, setMainNotes] = useState('');
  const [cueQuestions, setCueQuestions] = useState('');
  const [summary, setSummary] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);

  const originalConcept = 'Osmosis is the movement of water molecules from a region of high water concentration to a region of low water concentration through a semi-permeable membrane. This is a passive process — it requires no energy. The membrane allows water to pass but blocks larger solute molecules.';

  const getFeedback = () => {
    const issues: { type: 'warning' | 'success'; message: string }[] = [];

    // Main notes checks
    if (mainNotes.trim().length === 0) {
      issues.push({ type: 'warning', message: 'Main notes are empty. Try paraphrasing the concept in your own words.' });
    } else if (mainNotes.trim().length < 20) {
      issues.push({ type: 'warning', message: 'Main notes are very brief. Try to capture the key idea in a full sentence.' });
    } else {
      issues.push({ type: 'success', message: 'Main notes added. Check that they explain the concept in your own words.' });
    }

    // Cue questions checks
    const cueLines = cueQuestions.trim().split('\n').filter((l) => l.trim().length > 0);
    if (cueLines.length === 0) {
      issues.push({ type: 'warning', message: 'No cue questions added. Try writing 2-3 questions you could use to test yourself.' });
    } else if (cueLines.length < 2) {
      issues.push({ type: 'warning', message: 'Only one cue question. Aim for at least 2-3 for effective self-testing.' });
    } else {
      const hasYesNo = cueLines.some((q) => {
        const lower = q.toLowerCase().trim();
        return lower.startsWith('is ') || lower.startsWith('does ') || lower.startsWith('can ') || lower.startsWith('are ') || lower.startsWith('was ') || lower.startsWith('do ');
      });
      if (hasYesNo) {
        issues.push({ type: 'warning', message: 'Some cue questions look like yes/no questions. Open-ended questions (What, How, Why, Explain) force deeper retrieval.' });
      } else {
        issues.push({ type: 'success', message: `${cueLines.length} cue questions — great for self-testing!` });
      }
    }

    // Summary checks
    const summaryWords = summary.trim().split(/\s+/).filter((w) => w.length > 0).length;
    if (summaryWords === 0) {
      issues.push({ type: 'warning', message: 'Summary is empty. Write the core idea in one concise sentence.' });
    } else if (summaryWords > 25) {
      issues.push({ type: 'warning', message: `Summary is ${summaryWords} words. Aim for no more than 25 words — the constraint forces deeper compression.` });
    } else {
      issues.push({ type: 'success', message: `Summary is ${summaryWords} words — within the 25-word limit.` });
    }

    return issues;
  };

  const handleCheck = () => {
    setShowFeedback(true);
  };

  const handleReset = () => {
    setMainNotes('');
    setCueQuestions('');
    setSummary('');
    setShowFeedback(false);
  };

  const feedback = showFeedback ? getFeedback() : [];
  const allSuccess = feedback.length > 0 && feedback.every((f) => f.type === 'success');

  const fieldClass = "mt-3 min-h-36 w-full resize-y rounded-lg border border-zinc-300 bg-white p-3 text-base leading-relaxed text-zinc-900 placeholder:text-zinc-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#B54D14] dark:border-zinc-600 dark:bg-zinc-950 dark:text-white";
  return <section className="my-10 font-sans text-zinc-900 dark:text-zinc-100" aria-labelledby={`${fieldId}-title`}>
    <p className="mb-2 text-xs font-bold uppercase tracking-widest text-[#B54D14] dark:text-orange-400">Try it · Put notes to work</p>
    <h4 id={`${fieldId}-title`} className="font-serif text-3xl font-semibold">Cornell Note Simulator</h4>
    <p className="mt-2 mb-6 text-base leading-relaxed text-zinc-600 dark:text-zinc-300">Practice the Cornell Method on a real concept. Paraphrase, question, summarise.</p>
    <div className="mb-6 border-y border-zinc-300 py-5 dark:border-zinc-700">
      <h5 className="mb-3 text-xs font-bold uppercase tracking-widest text-zinc-600 dark:text-zinc-400">Original concept</h5>
      <p className="font-serif text-lg leading-relaxed">{originalConcept}</p>
    </div>
    <div className="grid grid-cols-1 gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)]">
      <div className="min-w-0 rounded-xl border border-zinc-300 p-4 dark:border-zinc-700 md:col-start-2 md:row-start-1">
        <label htmlFor={`${fieldId}-notes`} className="block text-base font-bold">1. Main notes</label>
        <p id={`${fieldId}-notes-help`} className="mt-1 text-sm leading-relaxed text-zinc-600 dark:text-zinc-300">Explain the concept in your own words.</p>
        <textarea id={`${fieldId}-notes`} rows={5} aria-describedby={`${fieldId}-notes-help`} value={mainNotes} onChange={e => { setMainNotes(e.target.value); setShowFeedback(false); }} placeholder="Water moves from…" className={fieldClass} />
      </div>
      <div className="min-w-0 rounded-xl border border-zinc-300 p-4 dark:border-zinc-700 md:col-start-1 md:row-start-1">
        <label htmlFor={`${fieldId}-cues`} className="block text-base font-bold">2. Cue questions</label>
        <p id={`${fieldId}-cues-help`} className="mt-1 text-sm leading-relaxed text-zinc-600 dark:text-zinc-300">Write 2–3 questions, one per line.</p>
        <textarea id={`${fieldId}-cues`} rows={5} aria-describedby={`${fieldId}-cues-help`} value={cueQuestions} onChange={e => { setCueQuestions(e.target.value); setShowFeedback(false); }} placeholder={"What is osmosis?\nWhy is no energy needed?"} className={fieldClass} />
      </div>
      <div className="min-w-0 rounded-xl border border-zinc-300 p-4 dark:border-zinc-700 md:col-span-2">
        <label htmlFor={`${fieldId}-summary`} className="block text-base font-bold">3. Summary</label>
        <p id={`${fieldId}-summary-help`} className="mt-1 text-sm leading-relaxed text-zinc-600 dark:text-zinc-300">Capture the core idea in one sentence, up to 25 words.</p>
        <textarea id={`${fieldId}-summary`} rows={3} aria-describedby={`${fieldId}-summary-help`} value={summary} onChange={e => { setSummary(e.target.value); setShowFeedback(false); }} placeholder="The key idea is…" className={fieldClass.replace('min-h-36', 'min-h-24')} />
      </div>
    </div>
    <div className="my-5 flex flex-wrap gap-3">
      <button onClick={handleCheck} className="min-h-12 flex-1 rounded-xl bg-[#F26B1F] px-5 py-3 text-base font-bold text-[#1A1A1A]">Check my notes</button>
      <button onClick={handleReset} className="min-h-12 rounded-xl border border-zinc-300 px-5 py-3 text-base font-semibold dark:border-zinc-700">Reset</button>
    </div>
    {showFeedback && <div role="status" className="border-t border-zinc-300 pt-4 dark:border-zinc-700">
      <h5 className="font-serif text-xl font-semibold">{allSuccess ? 'Ready to practise recall' : 'Review your notes'}</h5>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-300">This checks the structure of your notes. Compare the meaning with the original concept yourself.</p>
      <ul className="mt-3 space-y-3">{feedback.map((item, index) => <li key={index} className="text-base leading-relaxed"><span className="mr-2 font-bold text-[#B54D14] dark:text-orange-400" aria-hidden="true">{item.type === 'success' ? '✓' : '→'}</span>{item.message}</li>)}</ul>
      {allSuccess && <p className="mt-5 border-t border-zinc-200 pt-4 font-semibold leading-relaxed dark:border-zinc-700">Hide your main notes and summary, then test yourself using only your cue questions.</p>}
    </div>}
  </section>;
}
