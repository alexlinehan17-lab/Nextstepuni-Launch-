export const meta = {
  name: 'construction-figures',
  description: 'Extract + adversarially verify real SEC figures (scheme exemplar drawings / paper diagrams) for Construction Studies cards',
  phases: [
    { title: 'Extract', detail: 'locate → render → view → crop → save PNG' },
    { title: 'Verify', detail: 'view each crop, check it matches the spec' },
  ],
}

// args = [cardId, ...]  — each agent reads its full spec from SPECS_FILE.
const CARD_IDS = Array.isArray(args) ? args : (typeof args === 'string' ? JSON.parse(args) : [])
const SPECS_FILE = '/tmp/cons_figs.json'
const TOOL = 'python3 tools/extract_exam_figure.py'
const DIR = '/Users/alexlinehan/Nextstepuni-Launch-'

const EXTRACT_SCHEMA = {
  type: 'object', required: ['cardId', 'found', 'page', 'cropBox', 'alt'],
  properties: {
    cardId: { type: 'string' },
    found: { type: 'boolean' },
    page: { type: 'integer' },
    cropBox: { type: 'string', description: 'the x0 y0 x1 y1 fractions used' },
    alt: { type: 'string', description: 'alt text describing the saved figure' },
    note: { type: 'string' },
  },
}

phase('Extract')
const extracted = await parallel(CARD_IDS.map((cardId) => () =>
  agent(
    `You extract ONE real SEC figure for a Construction Studies card and save it as a PNG asset. Work in ${DIR}.\n\n` +
    `YOUR CARD ID: ${cardId}\n` +
    `FIRST: read ${SPECS_FILE} (a JSON array) and find the object whose "cardId" === "${cardId}". It gives you:\n` +
    `  pdf (the SEC PDF to crop from), txt (extracted text with ===PAGE n=== markers), questionRef, describes (the exact\n` +
    `  drawing to crop), outPng (where to save). Use THOSE values below.\n\n` +
    `STEPS (use Bash + Read):\n` +
    `1. LOCATE THE PAGE: grep the txt file for the question (e.g. "grep -n 'Question' <txt>" then the part letter, or grep the topic words from describes). Count the "===PAGE n===" markers at/before the match for the 1-based PDF page. A marking-scheme exemplar DRAWING is often 1-3 pages AFTER the question heading; a paper diagram is on/just after the question.\n` +
    `2. RENDER: ${TOOL} page <pdf> <page> /tmp/fig_${cardId}_p<page>.png 150 — render the candidate page (and a neighbour if unsure).\n` +
    `3. VIEW: Read the rendered PNG(s). Find the labelled construction drawing/section/detail matching describes. If not there, render adjacent pages until you find it.\n` +
    `4. CROP: choose a TIGHT box (fractions x0 y0 x1 y1, each 0..1) around JUST that drawing incl. its labels/dimensions. Run: ${TOOL} crop <pdf> <page> <x0> <y0> <x1> <y1> <outPng> 150\n` +
    `5. VERIFY YOUR OWN CROP: Read <outPng>. Confirm it shows the COMPLETE labelled drawing (nothing key cut off, legible, not a wrong/blank/text region). If bad, re-crop. Re-render at dpi 200 if labels are illegible.\n` +
    `6. Return { cardId:"${cardId}", found:true, page, cropBox:'x0 y0 x1 y1', alt:(a precise one-line alt describing the saved drawing) }. If you truly cannot find it after trying neighbouring pages, return found:false with a note.\n\n` +
    `Save ONLY the PNG (an asset). Do NOT edit any .ts file. Crop coords are FRACTIONS of the page (top-left origin).`,
    { label: `extract:${cardId}`, phase: 'Extract', schema: EXTRACT_SCHEMA },
  ),
))

const ok = extracted.filter(Boolean).filter((e) => e.found)
log(`Extracted ${ok.length}/${CARD_IDS.length} figures`)

phase('Verify')
const VERIFY_SCHEMA = {
  type: 'object', required: ['cardId', 'pass', 'reason'],
  properties: {
    cardId: { type: 'string' },
    pass: { type: 'boolean', description: 'true if the saved crop is a correct, complete, legible match for the spec' },
    reason: { type: 'string' },
    altFix: { type: 'string', description: 'an improved alt text if the original is weak; omit if fine' },
  },
}

const verified = await parallel(ok.map((e) => () =>
  agent(
    `Adversarially verify ONE extracted SEC figure. Default FAIL if off.\n\n` +
    `YOUR CARD ID: ${e.cardId}\n` +
    `Read ${SPECS_FILE}, find the object with cardId === "${e.cardId}" → it has outPng (the saved PNG), describes (what it should show), questionRef.\n\n` +
    `Read the saved PNG (outPng). PASS only if: (a) it is the CORRECT drawing/detail the describes calls for (not a wrong figure, not a block of text, not a blank/margin region), (b) the drawing is COMPLETE (key parts + labels not cut off), (c) it is LEGIBLE at this size. ` +
    `If it fails any of these, pass:false with the specific reason. If the alt text could be sharper, give altFix.\n` +
    `Return { cardId:"${e.cardId}", pass, reason, altFix? }.`,
    { label: `verify:${e.cardId}`, phase: 'Verify', schema: VERIFY_SCHEMA },
  )
))

const results = ok.map((e) => {
  const v = verified.filter(Boolean).find((x) => x.cardId === e.cardId)
  return { cardId: e.cardId, page: e.page, cropBox: e.cropBox, alt: (v && v.altFix) || e.alt, pass: v ? v.pass : false, reason: v && v.reason }
})
const passed = results.filter((r) => r.pass)
const failed = results.filter((r) => !r.pass)
const notFound = CARD_IDS.filter((id) => !ok.find((e) => e.cardId === id))
log(`Verify: ${passed.length} passed, ${failed.length} failed, ${notFound.length} not found`)
return { passed, failed, notFound, results }
