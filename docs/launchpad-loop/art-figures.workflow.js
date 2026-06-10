export const meta = {
  name: 'art-figures',
  description: 'Extract + adversarially verify artwork figures from the SEC Art plates booklets for Art Visual Studies cards',
  phases: [
    { title: 'Extract', detail: 'locate artwork on plates → render → view → crop → save PNG' },
    { title: 'Verify', detail: 'view each crop, check it is the right complete artwork' },
  ],
}

// args = [cardId, ...]  — each agent reads its full spec from SPECS_FILE.
const CARD_IDS = Array.isArray(args) ? args : (typeof args === 'string' ? JSON.parse(args) : [])
const SPECS_FILE = '/tmp/art_figs.json'
const TOOL = 'python3 tools/extract_exam_figure.py'
const DIR = '/Users/alexlinehan/Nextstepuni-Launch-'

const EXTRACT_SCHEMA = {
  type: 'object', required: ['cardId', 'found', 'page', 'cropBox', 'alt'],
  properties: {
    cardId: { type: 'string' }, found: { type: 'boolean' }, page: { type: 'integer' },
    cropBox: { type: 'string' }, alt: { type: 'string' }, note: { type: 'string' },
  },
}

phase('Extract')
const extracted = await parallel(CARD_IDS.map((cardId) => () =>
  agent(
    `You extract ONE artwork image from an SEC Art plates booklet and save it as a PNG asset. Work in ${DIR}.\n\n` +
    `YOUR CARD ID: ${cardId}\n` +
    `FIRST: read ${SPECS_FILE} (a JSON array), find the object whose "cardId" === "${cardId}". It gives: pdf (the plates\n` +
    `booklet), txt (its extracted text with ===PAGE n=== markers — captions only), artwork (the ARTIST + TITLE to find),\n` +
    `describes, outPng (where to save). Use THOSE values.\n\n` +
    `STEPS (use Bash + Read):\n` +
    `1. LOCATE: the plates booklet shows the Section A artworks, each captioned with the artist + title. grep the txt for a\n` +
    `   distinctive word from the artwork title/artist (e.g. "grep -in 'meenagrauv\\|quinn' <txt>") to find the ===PAGE n===\n` +
    `   it is on. If the caption text is sparse, render pages and look.\n` +
    `2. LIST/RENDER: try "${TOOL} list <pdf> <page>" to see embedded images, and "${TOOL} page <pdf> <page> /tmp/art_${cardId}_p<page>.png 150" to render.\n` +
    `3. VIEW: Read the rendered page. Confirm it shows the named artwork (match the caption to the artist+title).\n` +
    `4. CROP: choose a TIGHT box (fractions x0 y0 x1 y1, 0..1) around JUST the artwork image itself (you MAY include its\n` +
    `   printed caption strip if adjacent, but exclude other artworks and page margins). Run: ${TOOL} crop <pdf> <page> <x0> <y0> <x1> <y1> <outPng> 150\n` +
    `5. VERIFY YOUR OWN CROP: Read <outPng>. Confirm it is the COMPLETE artwork (not cropped through the image, not a\n` +
    `   different artwork, legible). Re-crop if needed; re-render at dpi 200 if low quality.\n` +
    `6. Return { cardId:"${cardId}", found:true, page, cropBox:'x0 y0 x1 y1', alt:(a precise one-line alt: artist, title, medium + what it depicts) }. If you cannot find the artwork after checking pages, found:false + note.\n\n` +
    `Save ONLY the PNG (an asset). Do NOT edit any .ts file. Crop coords are FRACTIONS of the page (top-left origin).`,
    { label: `extract:${cardId}`, phase: 'Extract', schema: EXTRACT_SCHEMA },
  ),
))

const ok = extracted.filter(Boolean).filter((e) => e.found)
log(`Extracted ${ok.length}/${CARD_IDS.length} artworks`)

phase('Verify')
const VERIFY_SCHEMA = {
  type: 'object', required: ['cardId', 'pass', 'reason'],
  properties: { cardId: { type: 'string' }, pass: { type: 'boolean' }, reason: { type: 'string' }, altFix: { type: 'string' } },
}

const verified = await parallel(ok.map((e) => () =>
  agent(
    `Adversarially verify ONE extracted artwork crop. Default FAIL if off.\n\n` +
    `YOUR CARD ID: ${e.cardId}\nRead ${SPECS_FILE}, find cardId === "${e.cardId}" → outPng (saved PNG), artwork (artist+title it should be), describes.\n\n` +
    `Read the saved PNG. PASS only if: (a) it is the CORRECT artwork named (artist+title), (b) the whole artwork is in frame (not cropped through the image, no big chunks of a neighbouring artwork or page margin), (c) it is legible. ` +
    `If off, pass:false + the specific reason. If the alt could be sharper, give altFix.\n` +
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
