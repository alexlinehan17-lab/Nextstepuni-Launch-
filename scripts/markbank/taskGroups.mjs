/** Select a complete marking method without retaining another method's row scopes. */
export function assessmentVariant(card, variant) {
  const rows = variant.rows;
  const ids = new Set(rows.map(r => r.id));
  return { ...card, answerVariants: undefined, rows,
    taskGroups: variant.taskGroups ?? card.taskGroups,
    calculationCaps: card.calculationCaps?.map(cap => {
      const limits = cap.rowLimits?.filter(limit => ids.has(limit.rowId));
      return { ...cap, rowLimits: limits?.length ? limits : undefined };
    }),
  };
}

/** Complete assessment routes retain short, separately marked task groups.
 * Every row belongs to exactly one contiguous group; each group keeps the
 * five-row fixed limit or sixteen-row shared-response limit, with a separately
 * reconciled published maximum.
 */
export function taskGroupsFault(card) {
  const caps = card.calculationCaps;
  if (caps && (!Array.isArray(caps) || !caps.length || card.tariffModel?.kind !== 'fixed'
    || new Set(caps.map(c => c.id)).size !== caps.length
    || new Set(caps.map(c => JSON.stringify([c.sourceCardId, c.verbatim?.trim()]))).size !== caps.length
    || caps.some(c => !c.id || card.rows.some(r => r.id === c.id)
      || card.answerVariants?.some(v => v.rows.some(r => r.id === c.id))
      || card.calculationDeductions?.some(d => d.id === c.id)
      || c.id === card.questionBonus?.id || !c.label?.trim() || !c.verbatim?.trim() || !c.contextNote?.trim()
      || !Number.isInteger(c.maxMarks) || c.maxMarks < 0
      || c.maxMarks >= (card.taskGroups?.find(g => g.sourceCardId === c.sourceCardId)?.marks ?? card.totalMarks)
      || (card.taskGroups ? !card.taskGroups.some(g => g.sourceCardId === c.sourceCardId) : !!c.sourceCardId)))) return 'invalid calculation score ceiling';
  if (caps?.some(cap => cap.rowLimits && (!Array.isArray(cap.rowLimits) || !cap.rowLimits.length
    || new Set(cap.rowLimits.map(limit => limit.rowId)).size !== cap.rowLimits.length
    || cap.rowLimits.some(limit => {
      const methods = [{ rows: card.rows, taskGroups: card.taskGroups }, ...(card.answerVariants ?? []).map(v => ({ rows: v.rows, taskGroups: v.taskGroups ?? card.taskGroups }))];
      const matches = methods.flatMap(method => method.rows.filter(row => row.id === limit.rowId)
        .map(row => ({ row, group: method.taskGroups?.find(g => g.sourceCardId === cap.sourceCardId) })));
      return !limit.rowId || !Number.isInteger(limit.maxMarks) || limit.maxMarks < 0 || !matches.length
        || matches.some(({row,group}) => !Number.isFinite(row.marks) || limit.maxMarks >= row.marks
          || (card.taskGroups && !group?.rowIds.includes(limit.rowId)));
    })))) return 'invalid calculation stage ceiling';
  const deductions = card.calculationDeductions;
  if (deductions && (!Array.isArray(deductions) || !deductions.length || card.tariffModel?.kind !== 'fixed'
    || new Set(deductions.map(d => d.id)).size !== deductions.length
    || new Set(deductions.map(d => JSON.stringify([d.sourceCardId, d.verbatim?.trim()]))).size !== deductions.length
    || deductions.some(d => !d.id || card.rows.some(r => r.id === d.id)
      || card.answerVariants?.some(v => v.rows.some(r => r.id === d.id))
      || d.id === card.questionBonus?.id || !d.label?.trim() || !d.verbatim?.trim() || !d.contextNote?.trim()
      || (d.maxMarks !== undefined && (!Number.isInteger(d.maxMarks) || d.maxMarks < 1 || d.maxMarks > card.totalMarks))
      || (card.taskGroups ? !card.taskGroups.some(g => g.sourceCardId === d.sourceCardId) : !!d.sourceCardId)))) return 'invalid calculation deduction scope';
  const bonus = card.questionBonus;
  if (bonus && (card.tariffModel?.kind !== 'fixed' || !card.taskGroups?.length
    || !bonus.id || card.rows.some(row => row.id === bonus.id)
    || bonus.kind !== 'criterion' || !bonus.verbatim?.trim() || !bonus.contextNote?.trim()
    || !Number.isFinite(bonus.marks) || bonus.marks <= 0
    || !Array.isArray(bonus.permittedMarks) || bonus.permittedMarks.length < 2
    || bonus.permittedMarks[0] !== 0 || bonus.permittedMarks.at(-1) !== bonus.marks
    || bonus.permittedMarks.some((mark, index, steps) => !Number.isFinite(mark)
      || mark < 0 || (index > 0 && mark <= steps[index - 1])))) return 'invalid whole-question bonus';
  if (card.taskGroups === undefined) return null;
  const ordered = card.tariffModel?.kind === 'orderedSplit';
  if ((!ordered && card.tariffModel?.kind !== 'fixed')
      || !Array.isArray(card.taskGroups) || card.taskGroups.length < 2
      || card.taskGroups.length > 24) return 'invalid complete-route task groups';
  if (card.answerVariants?.some(variant => {
    const groups = variant.taskGroups ?? card.taskGroups;
    return JSON.stringify(groups.map(g => [g.sourceCardId,g.label,g.marks])) !== JSON.stringify(card.taskGroups.map(g => [g.sourceCardId,g.label,g.marks]))
      || taskGroupsFault(assessmentVariant(card,variant));
  })) return 'invalid complete-route answer variant';
  const ids = new Set();
  const rowIds = [];
  let total = 0;
  for (const group of card.taskGroups) {
    if (!group.sourceCardId || ids.has(group.sourceCardId) || !group.label?.trim()
      || !Array.isArray(group.rowIds) || !group.rowIds.length || group.rowIds.length > (ordered ? 16 : 5)
      || !Number.isFinite(group.marks) || group.marks <= 0) return 'invalid route task boundary';
    ids.add(group.sourceCardId);
    const rows = group.rowIds.map(id => card.rows.find(row => row.id === id));
    if (rows.some(row => !row || row.route || (row.dependsOn && !group.rowIds.includes(row.dependsOn)))) {
      return 'route task has missing rows or cross-task scoring dependencies';
    }
    if (ordered) {
      const terms = group.tariffModel?.notation?.replace(/\s/g, '').split('+');
      if (group.tariffModel?.kind !== 'orderedSplit' || !terms?.length
        || terms.some(term => !/^\d+(?:\(\d+\))?$/.test(term))) return 'invalid independent response tariff';
      const awards = terms.flatMap(term => {
        const match = term.match(/^(\d+)\((\d+)\)$/);
        return match ? Array(Number(match[1])).fill(Number(match[2])) : [Number(term)];
      });
      if (!Array.isArray(group.responseCounts) || group.responseCounts.length !== rows.length
        || group.responseCounts.some(n => !Number.isInteger(n) || n < 1)
        || group.responseCounts.reduce((sum, n) => sum + n, 0) !== awards.length
        || awards.some((n, i) => n <= 0 || (i > 0 && n > awards[i - 1]))
        || awards.reduce((sum, n) => sum + n, 0) !== group.marks
        || rows.some(row => row.marks !== null || row.group)
        || rows.some((row, i) => row.kind !== 'anyN' && group.responseCounts[i] !== 1)) {
        return 'independent response tariff does not reconcile';
      }
    } else {
      if (group.tariffModel || group.responseCounts) return 'fixed task cannot contain a shared response tariff';
      const worth = row => row.group
        ? row.group.perOptionSteps?.reduce((sum, mark) => sum + mark, 0) ?? row.group.claimMax * row.group.perOption
        : row.marks;
      if (rows.some(row => !Number.isFinite(worth(row)))
        || rows.reduce((sum, row) => sum + worth(row), 0) !== group.marks) return 'route task marks do not reconcile';
    }
    rowIds.push(...group.rowIds);
    total += group.marks;
  }
  if (new Set(rowIds).size !== rowIds.length || JSON.stringify(rowIds) !== JSON.stringify(card.rows.map(row => row.id))) {
    return 'route rows must form a complete ordered partition';
  }
  return total + (bonus?.marks ?? 0) === card.totalMarks ? null : 'complete route marks do not reconcile';
}
