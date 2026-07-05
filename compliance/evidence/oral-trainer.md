# Evidence Dossier — Irish Oral Trainer (Launchpad)

**Tool:** `oral-trainer` (`components/OralExamTrainer.tsx`)
**Content data:** `data/oralExam/irish.ts` (`IRISH_ORAL`), typed by `data/oralExam/types.ts`
**Review date:** 2026-07-05
**Reviewer:** Pre-accreditation fact review (ahead of DCU / Brian MacCraith)
**Governing rule:** Every factual claim about the exam's structure, weighting and
prescribed material is stated only where a primary State Examinations Commission (SEC)
/ Department of Education source supports it. No figure or component is asserted unless
it traces to a resolvable official document. Where the exact wording of a rule was not
directly confirmable, the claim was reframed to the qualitative statement the source
supports and labelled as a teaching convention rather than an SEC-prescribed list.

Unlike the module dossiers, the sources here are **official SEC / Department of
Education exam documents**, not peer-reviewed literature — an exam's structure is an
administrative fact, not a research finding. Accordingly the verification below is
against government-published exam documentation rather than CrossRef/DOI records.

---

## Verified sources

| Key | Source | URL | Verification |
|-----|--------|-----|--------------|
| sec2026 | SEC — Assessment Arrangements for Leaving Certificate Examinations 2026 | https://assets.gov.ie/static/documents/2c504db1/Assessment_Doc_EN_2026.pdf | gov.ie / SEC published document for the 2026 sitting; confirms the oral is examined as a component of Leaving Certificate Irish and the current 40% weighting. |
| circ0026 | Department of Education Circular 0026/2024 — Prescribed Material for the Leaving Certificate 2026 | https://assets.gov.ie/288543/d803ad6c-6573-4026-91a6-9dc1d05197dd.pdf | Official prescribed-material circular for the 2026 examination; confirms the five prescribed poems and the 20-sequence *sraith pictiúr* set from which candidates prepare. |

Both are examiner/authority-published and citable. They are surfaced in-app as a
sources footnote at the foot of the tool's home view (links open in a new tab).

---

## Claim-by-claim record

### Overall weighting — "240 marks — 40% of Leaving Cert Irish"
- **Source:** sec2026.
- **Support:** Direct — the Irish oral currently carries 40% of the subject's marks at
  both levels. (Note: a redeveloped Irish specification will move the oral to a
  different weighting in a later cycle; the tool states the **current 2026** figure and
  is labelled "for 2026" so it does not misstate a future spec.)

### Common exam — "the same components and marks at Higher and Ordinary level"
- **Source:** sec2026.
- **Support:** Direct — the oral is a common examination; the components and their mark
  allocations are identical at Higher and Ordinary level. (Earlier scaffold wrongly
  assumed the levels differed — corrected before ship.)

### An Comhrá — general conversation, 120 marks
- **Source:** sec2026.
- **Support:** Direct on marks. The specific conversation *topics* listed in the tool
  (yourself, family, home area, school, pastimes, plans after the Leaving Cert) are the
  set students typically prepare — a **teaching convention**, not an SEC-prescribed
  checklist. The tool labels them as such in-copy ("These are the topics students
  usually prepare — the conversation is free-ranging, not an official SEC checklist").

### An tSraith Pictiúr — picture sequence, 80 marks
- **Source:** sec2026 (marks); circ0026 (the sequence set).
- **Support:** Direct — candidates prepare **10 of the 20** official picture sequences
  for 2026; in the exam the examiner selects one of the candidate's prepared sequences.
  The narration guidance (past tense, sequencing connectors *ar dtús / ansin / ina
  dhiaidh sin / ar deireadh*) is generic language-teaching guidance, not a scored rule,
  and is framed as advice ("usually in the past tense").

### Léamh na Filíochta — reading the poetry, 35 marks
- **Source:** sec2026 (marks); circ0026 (the five prescribed poems).
- **Support:** Direct. Critically, this component is **reading aloud**, not recitation
  from memory — the text is in front of the candidate. (Earlier scaffold wrongly called
  this "recitation"; corrected.) The five prescribed poems for 2026 per circ0026:
  *An Spailpín Fánach* (verses 1–3); *Géibheann* (Caitlín Maude); *An tEarrach Thiar*
  (Máirtín Ó Direáin); *Mo Ghrá-sa (idir lúibíní)* (Nuala Ní Dhomhnaill); *Colscaradh*
  (Pádraig Mac Suibhne).

### An Fáiltiú — the greeting, 5 marks
- **Source:** sec2026.
- **Support:** Direct — the opening greeting / roll-number confirmation carries 5 marks.

**Marks total:** 120 + 80 + 35 + 5 = **240**, consistent with the stated total.

---

## Reframed / corrected content (pre-ship)

| ID | Original scaffold | Reframed / corrected | Reason |
|----|-------------------|----------------------|--------|
| OT-001 | "Filíocht — recitation of a prescribed poem" | "Léamh na Filíochta — you read the poem aloud; it isn't recited from memory" | The component is reading aloud with the text present, not memorised recitation. |
| OT-002 | Implied Higher/Ordinary differ | "It's a common exam — the same components and marks at Higher and Ordinary level" | The oral is a common examination; components/marks are identical across levels. |
| OT-003 | Draft used 25% weighting | "240 marks — 40% of Leaving Cert Irish" | 25% is the *future* redeveloped specification; the current 2026 oral is 40%. |
| OT-004 | Conversation topics implied official | Labelled "the topics students usually prepare … not an official SEC checklist" | The comhrá is free-ranging; the topic list is a teaching convention, not prescribed. |

---

## Year-cycling note

Prescribed material (the poems and the *sraith pictiúr* set) is year-specific. The data
file and in-app copy are labelled **for 2026**. When the 2027 prescribed-material
circular publishes, update `data/oralExam/irish.ts` and this dossier together — the
dossier must never lag the app.

---

## Scope

MVP covers **Leaving Certificate Irish** only. If other language orals (French, German,
Spanish, etc.) are added, each gets its own verified `data/oralExam/<lang>.ts` and a
corresponding section here, grounded in that language's SEC documentation. No audio ever
leaves the device — recordings are in-memory only, never uploaded or persisted, so there
is no data-processing claim to substantiate.
