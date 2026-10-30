/** Validate both the modern credit scales and older step/deduction rules. */
export function validReviewedMathematicsMarking(card, paper) {
  const validBand = (code, marks, total) => /^[0-9]+[ABCDE]$/.test(code)
    && Array.isArray(marks) && marks.length === 'ABCDE'.indexOf(code.at(-1)) + 2
    && Number.parseInt(code, 10) === total && marks[0] === 0 && marks.at(-1) === total
    && marks.every((mark, index) => Number.isInteger(mark) && (index === 0 || mark > marks[index - 1]));
  const valid = card.methods
    ? card.scale === undefined && card.permittedMarks === undefined && card.components === undefined
      && !(card.fullCreditMinusOne ?? paper.fullCreditMinusOne) && card.methods.length > 0
      && new Set(card.methods.map(method => method.id)).size === card.methods.length
      && card.methods.every(method => /^[a-z][a-z0-9-]*$/.test(method.id)
        && typeof method.label === 'string' && method.label.trim().length > 0
        && Array.isArray(method.components) && method.components.length > 0
        && new Set(method.components.map(component => component.id)).size === method.components.length
        && method.components.every(component => /^[a-z][a-z0-9-]*$/.test(component.id)
          && typeof component.label === 'string' && component.label.trim().length > 0
          && Number.isInteger(component.maximum) && component.maximum > 0
          && Number.isInteger(component.attempt) && component.attempt >= 0 && component.attempt < component.maximum
          && (component.permittedMarks === undefined || (Array.isArray(component.permittedMarks)
            && component.permittedMarks[0] === 0 && component.permittedMarks.at(-1) === component.maximum
            && component.permittedMarks.includes(component.attempt)
            && component.permittedMarks.every((mark, index, marks) => Number.isInteger(mark)
              && (index === 0 || (mark >= component.attempt && mark > marks[index - 1]))))))
        && method.components.reduce((sum, component) => sum + component.maximum, 0) === card.totalMarks)
    : card.components
    ? card.scale === undefined && card.permittedMarks === undefined
      && card.components.length > 1
      && new Set(card.components.map(c => c.id)).size === card.components.length
      && card.components.every(c => /^[a-z][a-z0-9-]*$/.test(c.id) && c.id !== 'deduction'
        && typeof c.label === 'string' && c.label.trim().length
        && (c.fullCreditMinusOne === undefined || typeof c.fullCreditMinusOne === 'boolean')
        && validBand(c.code, c.marks, Number.parseInt(c.code, 10)))
      && !((card.fullCreditMinusOne ?? paper.fullCreditMinusOne) && card.components.some(c => c.fullCreditMinusOne))
      && card.components.reduce((sum, c) => sum + Number.parseInt(c.code, 10), 0) === card.totalMarks
    : validBand(card.scale, card.permittedMarks, card.totalMarks);
  return valid && (card.fullCreditMinusOne === undefined || typeof card.fullCreditMinusOne === 'boolean')
    && typeof paper.fullCreditMinusOne === 'boolean'
    && !!paper.generalNotesPages?.length && !!card.schemePages?.length
    && (card.generalNotesPages === undefined || (Array.isArray(card.generalNotesPages)
      && card.generalNotesPages.length > 0
      && new Set(card.generalNotesPages).size === card.generalNotesPages.length
      && card.generalNotesPages.every(page => Number.isInteger(page) && page > 0
        && paper.generalNotesPages.includes(page))));
}
