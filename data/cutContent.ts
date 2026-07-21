/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Cut Content Log ────────────────────────────────────────────────────────
//
// Tracked record of module content that was REMOVED or REFRAMED during the
// pre-accreditation review (ahead of the meeting with Brian MacCraith / DCU).
//
// Governing rule (agreed 2026-06): we only state or advise something the
// peer-reviewed literature actually supports. Any claim that could not be
// verified against a real, locatable source is reframed to non-prescriptive
// language or cut outright — a citation is NEVER invented to keep it.
//
// Every cut or reframe is logged here so there is a transparent audit trail of
// exactly what changed and why. This list is surfaced in-app via the
// "Cut Content" page (home sidebar, admin/owner reference — not student-facing
// guidance).
//
// When cutting or reframing content, append an entry below. Keep `original`
// as the verbatim text that was removed so it can be reviewed in context.

export type CutAction = 'removed' | 'reframed' | 'corrected';

export interface CutContentEntry {
  /** Stable unique id (e.g. `${moduleId}-001`). */
  id: string;
  /** Human-readable module/course this came from (title preferred). */
  module: string;
  /** The lesson / section / sub-module the content was cut from. */
  section: string;
  /** Whether the content was removed entirely or reframed to non-prescriptive. */
  action: CutAction;
  /** Verbatim original text that was removed. */
  original: string;
  /** If reframed, the replacement text now shown to students. */
  reframedTo?: string;
  /** Why it was cut — e.g. "No peer-reviewed source supports this advice." */
  reason: string;
  /** ISO date the cut was made. */
  date: string;
  /**
   * True when this was only reframed because a primary source is paywalled /
   * unconfirmable — the original wording can be RESTORED verbatim once the PDF
   * is supplied. These surface in their own "Awaiting references" section.
   */
  awaitingSource?: boolean;
  /** The specific paper to dig out to restore the original (shown in the awaiting section). */
  neededSource?: string;
}

export const CUT_CONTENT: CutContentEntry[] = [
  {
    id: 'mastering-active-recall-001',
    module: 'Mastering Active Recall',
    section: "Step 3 — The 'I Know This' Trap",
    action: 'reframed',
    original:
      'Students who stopped testing themselves after one correct answer could only remember about 35% of the material a week later. Students who kept testing themselves on everything remembered about 80% — more than double.',
    reframedTo:
      'In a well-known study, students who kept testing themselves on material remembered far more a week later than students who stopped as soon as they got it right once — even though both groups felt just as sure they knew it.',
    reason:
      'The specific figures (35% / 80%) come from Karpicke & Roediger (2008, Science), which is paywalled with no open-access copy, so the exact numbers could not be verified against the primary source. Reframed to the qualitative finding, which the abstract fully supports. Citation retained (doi:10.1126/science.1152408). Exact figures can be restored if the PDF is supplied.',
    date: '2026-06-23',
    awaitingSource: true,
    neededSource: 'Karpicke, J. D., & Roediger, H. L. (2008). The critical importance of retrieval for learning. Science. doi:10.1126/science.1152408',
  },
  {
    id: 'mastering-active-recall-002',
    module: 'Mastering Active Recall',
    section: 'Step 5 — The Anxiety Myth',
    action: 'reframed',
    original:
      'An incredible 92% of students said it helped them learn, and 72% said it made them less nervous for big exams.',
    reframedTo:
      'The large majority said it helped them learn, and most said it actually made them less nervous for big exams.',
    reason:
      'The 92%/72% figures trace to Agarwal et al. (2014, JARMAC), which is paywalled and not indexed in open databases. The percentages are corroborated by multiple secondary sources but could not be confirmed against the primary full text, so they were reframed to a qualitative claim the paper supports. Citation retained (doi:10.1016/j.jarmac.2014.07.002).',
    date: '2026-06-23',
    awaitingSource: true,
    neededSource: "Agarwal, P. K., D'Antonio, L., Roediger, H. L., McDermott, K. B., & McDaniel, M. A. (2014). Classroom-based programs of retrieval practice reduce middle school and high school students' test anxiety. Journal of Applied Research in Memory and Cognition. doi:10.1016/j.jarmac.2014.07.002",
  },
  {
    id: 'mastering-active-recall-003',
    module: 'Mastering Active Recall',
    section: 'Step 6 — Your Recall Toolkit (micro-commitment)',
    action: 'reframed',
    original:
      'For your next study session, try the 20/80 rule. Spend 20% of your time consuming information (reading, watching) and 80% of your time actively recalling it (self-quizzing, explaining it out loud).',
    reframedTo:
      'For your next study session, flip the balance: spend most of your time actively recalling (self-quizzing, explaining out loud) rather than re-reading or watching.',
    reason:
      'The specific 20/80 ratio is a popularisation with no peer-reviewed empirical basis. The underlying principle (weight study time toward retrieval over restudy) is well supported (Roediger & Karpicke 2006; Karpicke & Roediger 2008), so the advice was reframed to drop the false-precision ratio.',
    date: '2026-06-23',
  },
  {
    id: 'mastering-active-recall-004',
    module: 'Mastering Active Recall',
    section: 'Step 6 — Your Recall Toolkit (Rule 1 card)',
    action: 'reframed',
    original:
      "If It Feels Hard, It's Working — That feeling of struggle when you're trying to remember something? That IS learning happening. If it feels easy, it's probably not doing much.",
    reframedTo:
      "A Bit of Struggle Is the Point — When recalling something takes real effort, but you can still manage it, that effort is what builds lasting memory ('desirable difficulties'). If it feels completely effortless, it's probably not doing much.",
    reason:
      "The original overstated the science — not all difficulty aids learning, only 'desirable difficulties' (effortful but ultimately successful retrieval). Reframed to the precise concept, supported by Soderstrom & Bjork (2015, doi:10.1177/1745691615569000).",
    date: '2026-06-23',
  },
  {
    id: 'spaced-repetition-001',
    module: 'Spaced Repetition',
    section: 'Step 1 — The Forgetting Curve',
    action: 'reframed',
    original:
      'Without reviewing, you can lose over 50% of new information within an hour, and up to 80% within a day.',
    reframedTo:
      'Without reviewing, a large share of new information slips away within the first day or two — classic studies of the forgetting curve, since replicated, show memory dropping sharply soon after learning.',
    reason:
      "The specific figures overstate the evidence — the replicated Ebbinghaus forgetting curve (Murre & Dros 2015, doi:10.1371/journal.pone.0120644) shows a sharp early drop but not ~80% loss within 24 hours. Reframed to a defensible qualitative claim citing the replication.",
    date: '2026-06-23',
  },
  {
    id: 'spaced-repetition-002',
    module: 'Spaced Repetition',
    section: 'Step 2 — The Cramming Paradox',
    action: 'reframed',
    original: 'Spaced Practice can triple how long you remember something.',
    reframedTo: 'Spaced Practice can dramatically increase how long you remember something.',
    reason:
      'The "triple" multiplier is not supported as a general figure. The spacing effect itself is robustly evidenced (Cepeda et al. 2006, doi:10.1037/0033-2909.132.3.354), but effect sizes vary widely by interval, so the specific number was reframed to a qualitative claim.',
    date: '2026-06-23',
  },
  {
    id: 'how-memory-works-001',
    module: 'How Your Memory Works',
    section: 'Step 6 — Your Action Plan (micro-commitment)',
    action: 'reframed',
    original:
      "This single act of 'sleep hygiene' has a bigger impact on your memory than an extra hour of cramming.",
    reframedTo:
      "This single act of 'sleep hygiene' protects the deep sleep your memory relies on to lock in what you studied.",
    reason:
      'The original made a direct quantitative comparison ("bigger impact than an extra hour of cramming") that is not established by any specific study. The underlying point — sleep is essential for memory consolidation — is well supported (Diekelmann & Born 2010, doi:10.1038/nrn2762), so the claim was reframed to drop the unsupported comparison.',
    date: '2026-06-23',
  },
  {
    id: 'elaborative-interrogation-001',
    module: 'Elaborative Interrogation',
    section: 'Step 1 — The "Why" Engine',
    action: 'reframed',
    original:
      'Students who asked "Why?" remembered 72% of material. Passive readers remembered only 37%. … the "Why?" group remembered almost double what the passive readers did (72% vs 37%).',
    reframedTo:
      'In classic experiments, students who asked "Why?" remembered far more than passive readers — one simple question can come close to doubling how much sticks.',
    reason:
      'The specific 72%/37% figures could not be tied to a verifiable primary source. The elaborative-interrogation effect (the "why" question roughly doubling retention vs passive reading) is well evidenced (Stein & Bransford 1979, doi:10.1016/s0022-5371(79)90481-x; Pressley et al. 1987, doi:10.1037/0278-7393.13.2.291; reviewed in Dunlosky et al. 2013), so the claim was reframed to the supported qualitative version. The on-screen demo bars are illustrative only (no numbers shown).',
    date: '2026-06-23',
  },
  {
    id: 'cognitive-endurance-001',
    module: 'Cognitive Endurance',
    section: 'Step 3 — Fueling the Engine',
    action: 'reframed',
    original:
      'Swishing a sports drink around your mouth for 10 seconds tricks your brain into thinking fuel is on the way. This can give you a real mental boost in the final, gruelling hour of a long exam.',
    reframedTo:
      'Swishing a sports drink around your mouth for about 10 seconds activates reward areas in your brain. In endurance exercise this reliably lowers how hard the effort feels; it may give a similar lift in the final, gruelling hour of a long exam, though the evidence for mental tasks is less settled.',
    reason:
      'The carbohydrate mouth-rinse effect is established for endurance/physical performance and perceived effort (Chambers, Bridge & Jones 2009, doi:10.1113/jphysiol.2008.164285), but its benefit for sustained cognitive/exam performance is not well established. Reframed to state the evidenced mechanism and flag the uncertainty for mental tasks rather than promising "a real mental boost".',
    date: '2026-06-23',
  },
  {
    id: 'cognitive-endurance-002',
    module: 'Cognitive Endurance',
    section: 'Step 6 — The Recovery Protocol',
    action: 'reframed',
    original:
      'In the crucial break between two exams on the same day, a 20-minute NSDR session is the single most effective way to recharge for the afternoon paper.',
    reframedTo:
      'In the crucial break between two exams on the same day, a 20-minute NSDR session is one of the best ways to recharge for the afternoon paper.',
    reason:
      'The "single most effective" superlative is not supported — the peer-reviewed evidence base for NSDR / yoga nidra as a recovery tool is still limited. Reframed to a non-superlative recommendation. (Brief structured breathing has stronger support: Balban et al. 2023, doi:10.1016/j.xcrm.2022.100895.)',
    date: '2026-06-23',
  },
  {
    id: 'digital-distraction-001',
    module: 'Creating Barriers for Digital Distractions',
    section: 'Step 1 — Why Your Phone Wins (+ Attention Deficit Calculator)',
    action: 'reframed',
    original:
      'Every phone check costs you 23 minutes of focus recovery. That means 3 checks per hour leaves almost zero deep work time. … [calculator] Every phone check triggers a ~23 minute attention recovery. How much of your study hour survives?',
    reframedTo:
      'After an interruption, research found it can take around 23 minutes to fully refocus — so frequent phone checks can quietly wreck a whole study session. … [calculator] After an interruption it can take a while to fully refocus. This is a simplified illustration of how quickly those costs add up.',
    reason:
      'The ~23-minute figure is real (Mark, Gudith & Klocke 2008, doi:10.1145/1357054.1357072 — average time to return to an interrupted task), but the original linearly stacked it (e.g. "3 checks = over an hour lost"), which the study does not support (recovery periods overlap and vary). Reframed to cite the figure accurately and to label the interactive calculator as a simplified illustration rather than a precise measure.',
    date: '2026-06-23',
  },
  {
    id: 'learning-radar-001',
    module: 'The Learning Radar',
    section: "Step 1 — You Don't Know What You Don't Know",
    action: 'reframed',
    original:
      'Students predicted they would remember 70% of what they studied. They actually remembered 37%. … across over 100 studies, researchers found that the link between how well students think they\'ll do and how they actually do is shockingly weak. Barely better than chance.',
    reframedTo:
      'Students routinely predict they\'ll remember far more than they actually do. … across many studies, researchers found that people\'s self-assessments line up only modestly with how they actually perform.',
    reason:
      'The specific 70%/37% word-pair figures could not be tied to a verifiable primary source, and "barely better than chance" overstates the evidence — the large metasynthesis of self-insight (Zell & Krizan 2014, doi:10.1177/1745691613518075) finds self-assessments correlate *modestly* (not near-zero) with performance. Reframed to the supported qualitative claim.',
    date: '2026-06-23',
  },
  {
    id: 'learning-radar-002',
    module: 'The Learning Radar',
    section: 'Step 2 — Why the Least Prepared Feel Most Confident (Confidence vs Reality curve)',
    action: 'reframed',
    original:
      'The "Confidence vs. Reality Curve" interactive presented the popular rollercoaster Dunning-Kruger shape (Peak of Overconfidence → Valley of Doubt → Steady Improvement → Realistic Confidence) as how confidence tracks competence.',
    reframedTo:
      'Subtitle relabelled: "A simplified illustration of how confidence and real ability can drift apart — not a literal graph of any single study." Prose reflects the actual Kruger & Dunning (1999) finding.',
    reason:
      'The popular "valley of despair" rollercoaster curve is an internet meme, not the data from Kruger & Dunning (1999, doi:10.1037/0022-3514.77.6.1121), whose actual finding is that low performers overestimate and top performers slightly underestimate (no valley). The prose was corrected to the real finding and the interactive is now explicitly labelled an illustration rather than the empirical curve.',
    date: '2026-06-23',
  },
  {
    id: 'learning-radar-003',
    module: 'The Learning Radar',
    section: 'Step 6 — The Prediction Game',
    action: 'reframed',
    original:
      'Students who did this improved their prediction accuracy by 50% over a year. This skill transfers across subjects too. … Students who practised predicting in one subject showed better self-awareness in completely unrelated subjects. This isn\'t a trick that only works for one topic — it\'s a general skill.',
    reframedTo:
      'Students who do this get noticeably better at predicting their performance over time. The habit tends to carry over to other subjects too. … It behaves less like a one-topic trick and more like a general habit.',
    reason:
      'The specific "50% more accurate over a year" figure could not be verified, and the strong cross-subject "transfer" claim overstates a contested area (metacognitive transfer across domains is not firmly established). Reframed to the supported qualitative claim that prediction practice improves calibration and tends to generalise.',
    date: '2026-06-23',
  },
  {
    id: 'note-taking-paradox-001',
    module: 'The Note-Taking Paradox',
    section: 'Step 1 — The Transcription Trap',
    action: 'reframed',
    original:
      'A famous study compared students who typed their notes on laptops with students who wrote by hand. … when they were tested on questions that needed real understanding, the handwriters crushed it.',
    reframedTo:
      'A well-known study compared laptop vs handwritten note-takers … On questions that needed real understanding, the handwriters came out ahead. (Later replications suggest the handwriting-versus-laptop part is less clear-cut than first reported — what matters is whether you copy verbatim or process ideas into your own words, not the device.)',
    reason:
      'The original overstated Mueller & Oppenheimer (2014, doi:10.1177/0956797614524581). That study is real, but large replications (e.g. Morehead et al. 2019; Urry et al. 2021) failed to reproduce the conceptual-understanding advantage of longhand. Reframed to emphasise the robust mechanism (verbatim copying vs generative processing) and to flag the replication uncertainty around handwriting vs laptop specifically.',
    date: '2026-06-23',
  },
  {
    id: 'note-taking-paradox-002',
    module: 'The Note-Taking Paradox',
    section: 'Step 2 — Notes That Actually Work',
    action: 'reframed',
    original:
      'Students who paraphrase, summarise, and make connections in their notes consistently outperform word-for-word note-takers by 30-40% on the kinds of questions that actually matter.',
    reframedTo:
      'Students who paraphrase, summarise, and make connections in their notes tend to outperform word-for-word note-takers on the kinds of questions that actually matter.',
    reason:
      'The specific "30-40%" figure could not be tied to a verifiable source. The underlying generative/encoding benefit of note-taking is well supported (Kiewra 1989, doi:10.1007/bf01326640; depth-of-processing, Craik & Lockhart 1972), so the claim was reframed to the supported qualitative version.',
    date: '2026-06-23',
  },
  {
    id: 'cognitive-load-001',
    module: 'Cognitive Load',
    section: 'Step 3 — Why Separate Diagrams Kill Learning',
    action: 'reframed',
    original:
      'Students who studied with combined materials performed 30 to 50% better than those who studied the same content with the text and images apart.',
    reframedTo:
      'Students who studied with combined materials learned substantially better than those who studied the same content with the text and images apart.',
    reason:
      'The split-attention effect is well established (Chandler & Sweller 1992, doi:10.1111/j.2044-8279.1992.tb01017.x), but the specific "30-50%" range is not a single verifiable figure (effect sizes vary by study and material). Reframed to the supported qualitative claim.',
    date: '2026-06-23',
  },
  {
    id: 'context-effect-001',
    module: 'The Context Effect',
    section: 'Steps 1 & 2 — Context-dependent memory',
    action: 'reframed',
    original:
      'People tested in the same place they studied recalled 40% more. … students who studied in two different rooms recalled 40% more than those who stayed in one room.',
    reframedTo:
      'People tested in the same place they studied tend to recall noticeably more. … students who studied in two different rooms recalled more than those who stayed in one room.',
    reason:
      'The "40%" figures overstate the effect. The underlying studies are real (Godden & Baddeley 1975, doi:10.1111/j.2044-8295.1975.tb01468.x; Smith, Glenberg & Bjork 1978, doi:10.3758/bf03197465), but the meta-analysis (Smith & Vela 2001, doi:10.3758/bf03196157) shows environmental context-dependent memory is real but modest and does not always replicate. Reframed to qualitative, and §4 now states the effect is "modest".',
    date: '2026-06-23',
  },
  {
    id: 'myelin-manual-001',
    module: 'The Myelin Manual',
    section: 'Step 2 — The Signal of Struggle',
    action: 'reframed',
    original:
      'That feeling of struggle is not failure. It is your brain placing the order for a faster connection. No struggle means no upgrade. … It\'s the physical sensation of your brain placing the order for a faster, better connection.',
    reframedTo:
      "That feeling of effortful struggle is a sign you're practising at the right level — the focused, effortful practice that drives these changes. Coasting through easy material does much less.",
    reason:
      'Activity-dependent (adaptive) myelination is genuinely supported (Gibson et al. 2014, doi:10.1126/science.1252304; McKenzie et al. 2014, doi:10.1126/science.1254960) — neural activity drives myelination, and effortful practice produces that activity. But the popularised gloss that the *subjective feeling of struggle* is literally "the brain placing the order for myelin" (and "no struggle, no upgrade") overstates the science. Reframed to tie the change to effortful/focused practice (deliberate practice, desirable difficulty) rather than to the sensation of struggle itself.',
    date: '2026-06-23',
  },
  {
    id: 'myelin-manual-002',
    module: 'The Myelin Manual',
    section: 'Step 5 — The Rules of Myelination',
    action: 'reframed',
    original:
      "It's permanent but slow. Once a skill gets wrapped in myelin, it sticks with you for good.",
    reframedTo:
      "It's durable but slow. A skill built through proper practice lasts far longer than anything you cram… but brain changes aren't frozen forever: stop practising completely and they gradually fade.",
    reason:
      'Claiming skills are "permanent" / "stick for good" contradicts the use-it-or-lose-it evidence in the very previous module (the juggling study, Draganski et al. 2004, showed training-induced brain changes reverse when practice stops). Reframed to "durable but reversible if abandoned" for consistency with the evidence.',
    date: '2026-06-23',
  },
  {
    id: 'praise-protocol-001',
    module: 'The Power of Praise',
    section: 'Step 2 — The Praise Experiment',
    action: 'reframed',
    original:
      'They picked harder challenges, actually enjoyed the struggle, bounced back after failing, and were three times more honest about their scores.',
    reframedTo:
      'They picked harder challenges, actually enjoyed the struggle, bounced back after failing, and were far more honest about their scores.',
    reason:
      'The underlying study (Mueller & Dweck 1998) reports that nearly 40% of ability-praised children misrepresented their scores — that specific figure is kept and cited. But the precise "three times more honest" ratio is a derived comparison not stated as such in the paper, so the precision was softened to "far more honest" to avoid quoting a number we cannot point to in the source.',
    date: '2026-06-23',
  },
  {
    id: 'praise-protocol-002',
    module: 'The Power of Praise',
    section: 'Step 3 — The Brain on Praise',
    action: 'reframed',
    original:
      "When you get praised, your brain releases dopamine — the feel-good chemical. Process praise connects that feeling to the work you put in, so your brain starts craving effort. Person praise connects it to who you are, so any failure feels like a personal attack and your motivation crashes.",
    reframedTo:
      "Praise feels good — but person praise attaches that feeling to who you are, so any failure can land like a personal attack and motivation crashes. Process praise attaches it to the work you put in — something you can always do again — so setbacks feel less threatening.",
    reason:
      'The specific neurochemical mechanism — that dopamine from praise gets "wired" to effort vs. identity, making the brain "crave effort" — is a popularised just-so story not established in the praise literature. Reframed to the behavioural claim that is supported (person praise is associated with more helpless responses to failure; Mueller & Dweck 1998) without asserting an unverified dopamine pathway. The error-signal claim that follows is kept and cited to Moser et al. 2011.',
    date: '2026-06-23',
  },
  {
    id: 'effective-struggle-001',
    module: 'Effective Struggle',
    section: 'Step 1 — The Fallacy of Ease (and "The Great Deception" chart)',
    action: 'reframed',
    original:
      'Students who re-read predicted 90% recall but scored 40%. Self-testers predicted 40% but scored 61%. (Chart: "What students predicted" = 90% re-reading vs 40% self-testing.)',
    reframedTo:
      'Students who re-read felt more confident but recalled 40% a week later; self-testers felt less sure yet recalled 61%. The chart now shows only the verified one-week retention (40% vs 61%) and notes the re-reading group\'s higher confidence qualitatively.',
    reason:
      'The one-week retention figures (40% re-study vs 61% self-testing) are the verified headline result of Roediger & Karpicke (2006, Exp 2) and are kept and cited. But the precise prediction percentages (90% vs 40%) are not the predictions that study reported — its participants\' predicted recall hovered around half, and the paper supports only the qualitative point that re-reading "increased students\' confidence." The fabricated prediction numbers were removed from both the prose and the interactive chart; the confidence/calibration point is retained qualitatively.',
    date: '2026-06-23',
  },
  {
    id: 'science-of-mistakes-001',
    module: 'The Science of Mistakes',
    section: 'Step 4 — The High-Stakes Hijack',
    action: 'reframed',
    original:
      'When that happens, two things go wrong at once. First, the logical, problem-solving part of your brain gets weaker… Second, that important Pe signal gets squashed.',
    reframedTo:
      'Acute stress weakens the prefrontal cortex (the logical, problem-solving part of the brain), making it much harder to analyse a mistake calmly in the moment.',
    reason:
      'The claim that exam stress specifically "squashes the Pe signal" is not established — the anxiety/error-monitoring literature is mixed (anxiety often *increases* the earlier ERN), and there is no clean finding that acute exam stress reduces Pe amplitude. The supported mechanism — acute stress impairing prefrontal-cortex function (Arnsten 2009) — is kept and cited; the specific unsupported Pe-under-stress claim was removed.',
    date: '2026-06-23',
  },
  {
    id: 'power-of-yet-001',
    module: 'The Power of "Yet"',
    section: 'Step 2 — The Software Patch',
    action: 'reframed',
    original:
      'A school in Chicago actually replaced "Fail" grades with "Not Yet" on report cards, and students started trying harder and finishing more work.',
    reframedTo:
      'Some schools have even swapped "Fail" grades for "Not Yet" on report cards to send that exact message — a failed test isn\'t a verdict, it\'s just a checkpoint you haven\'t passed yet.',
    reason:
      'The "Chicago school" example comes from Carol Dweck\'s 2014 TED talk, not a peer-reviewed study, and the specific causal outcome — that students "started trying harder and finishing more work" — has no verifiable source. The "Not Yet" grading practice is kept as an illustration of the concept, but the unverifiable achievement/effort outcome was removed.',
    date: '2026-06-23',
  },
  {
    id: 'controllable-variables-001',
    module: 'Using Controllable Variables to Grow',
    section: 'Step 2 — Sleep',
    action: 'reframed',
    original:
      'After just one week of 5-hour nights, your working memory drops by about 17% — that\'s enough to drop you from an A to a C.',
    reframedTo:
      'After just a week of 5-hour nights, your working memory takes a real hit — chronic short sleep builds up a cognitive deficit that keeps growing the longer it drags on.',
    reason:
      'The directional claim — chronic sleep restriction progressively impairs working memory / neurobehavioral function — is well established (Van Dongen et al. 2003) and is kept and cited. But the precise "17%" figure and the "A to a C" grade equivalence could not be traced to a specific, locatable paper reporting exactly that, so both were reframed to the supported qualitative claim.',
    date: '2026-06-23',
  },
  {
    id: 'controllable-variables-002',
    module: 'Using Controllable Variables to Grow',
    section: 'Step 2/3 — Sleep simulator & Nutrition',
    action: 'reframed',
    original:
      'Simulator milestones "Working memory reduced by 30%" and "You are now LEGALLY DRUNK in terms of cognitive function"; nutrition text "even mild dehydration (losing just 1% of your body weight in water) is enough to mess with your working memory."',
    reframedTo:
      'Simulator now reads "Working memory is now clearly impaired" and "Your impairment now rivals being over the drink-drive limit"; nutrition text reads "even mild dehydration is enough to make it harder to concentrate."',
    reason:
      'The "30%" working-memory figure and the precise "1% body-weight dehydration impairs working memory" claim could not be tied to a specific verifiable source, and "legally drunk" is a jurisdiction-specific legal claim. The supported core — prolonged wakefulness produces alcohol-equivalent impairment (Dawson & Reid 1997, who found ~17 h awake ≈ BAC 0.05%) — is kept and cited; the unverifiable precise figures were softened to qualitative statements.',
    date: '2026-06-23',
  },
  {
    id: 'teaching-effect-001',
    module: 'The Teaching Effect',
    section: 'Step 3 — You Don\'t Need an Audience',
    action: 'reframed',
    original:
      'In one study with physics students, those who paused after each worked example to explain to themselves why each step was taken solved 82% of new problems on a test. The students who just read through the examples? Only 46%.',
    reframedTo:
      'In classic studies with physics students, those who paused after each worked example to explain to themselves why each step was taken went on to solve far more new problems than the students who just read through the examples.',
    reason:
      'The self-explanation effect is robust and is kept and cited (Chi et al. 1989). But the "82% vs 46%" figures were framed as an explain-vs-read experimental manipulation, whereas Chi et al. (1989) was a correlational study comparing students who spontaneously self-explained more ("good" solvers) with those who did not ("poor" solvers) — so that causal framing and those precise percentages misrepresent the study\'s design. Reframed to the qualitative, accurately-attributed self-explanation effect.',
    date: '2026-06-23',
  },
  {
    id: 'hope-protocol-001',
    module: 'The Science of Hope',
    section: 'Step 3 — The Science of Willpower',
    action: 'reframed',
    original:
      'Your brain uses Dopamine to create motivation. You can trigger it on demand. … That vivid image fires up your brain\'s reward system and gives you a real motivational boost. (Micro-commitment: "giving your brain a small, upfront hit of dopamine.")',
    reframedTo:
      'Your brain\'s reward system drives motivation — and you can switch it on deliberately. … Vividly imagining future success makes that reward feel real now, which boosts your motivation to start. (Micro-commitment: "giving your motivation a small, upfront boost.")',
    reason:
      'Episodic future thinking is supported and cited (Peters & Büchel 2010), but that study showed EFT reduces delay discounting via prefrontal-mediotemporal interactions — it did not demonstrate an on-demand "dopamine hit." The specific dopamine-release mechanism was an over-attribution, so the claims were reframed to the supported effect (EFT makes future rewards feel closer and more motivating now) without asserting the unverified neurochemical specifics.',
    date: '2026-06-23',
  },
  {
    id: 'leaving-cert-strategy-001',
    module: 'The Points Playbook (Leaving Cert Strategy)',
    section: 'Step 5 — Command Word Decoder',
    action: 'reframed',
    original:
      'Misinterpreting this word is the #1 cause of losing marks.',
    reframedTo:
      'Misreading what this word is asking for is one of the most common ways students lose marks.',
    reason:
      'SEC Chief Examiner reports repeatedly identify "not answering the question asked / misreading the question" as a leading source of lost marks (verified in the in-repo Business 2015 Chief Examiner report), which supports the general claim. But the specific superlative "#1 cause" ranks it above all other error types, which no single report establishes across subjects — so the ranking was softened to "one of the most common" while keeping the cited examiner-report point.',
    date: '2026-06-24',
  },
  {
    id: 'exam-crisis-management-001',
    module: 'Exam Crisis Management',
    section: 'Step 5 — Food and Focus',
    action: 'reframed',
    original:
      'Quick-burn foods (sweets, white bread, energy drinks) cause a crash that will hit you right in the middle of your exam.',
    reframedTo:
      'Quick-burn foods (sweets, white bread, energy drinks) can leave your energy dipping partway through, just when you need it most. A slower-release breakfast is linked to steadier concentration in students through the morning.',
    reason:
      'The RCT evidence (Micha, Rogers & Nelson 2011, Br J Nutr) supports that a lower-GI breakfast yields better cognitive function and mood in school children through the morning. It does not establish a guaranteed mid-exam "crash" caused by quick-burn foods in healthy students, so the deterministic causal claim was softened to a probabilistic "can leave your energy dipping" plus the cited low-GI benefit.',
    date: '2026-06-24',
  },
  {
    id: 'exam-crisis-management-002',
    module: 'Exam Crisis Management',
    section: 'Step 5 — Food and Focus',
    action: 'reframed',
    original:
      'If tea is more your thing, even better -- it has a natural ingredient that gives you calm focus without the jitters.',
    reframedTo:
      'If tea is more your thing, many people find it a gentler lift than coffee.',
    reason:
      'The implied L-theanine "calm focus" mechanism has supportive but mixed RCT evidence and was not being cited; rather than attach a borderline mechanistic claim or a new source for an aside, it was reframed to a non-prescriptive experiential statement.',
    date: '2026-06-24',
  },
  {
    id: 'game-day-001',
    module: 'Game Day: Peak Performance',
    section: 'Step 3 — The Final Week',
    action: 'reframed',
    original:
      'Cutting your study hours by 40-60% in the final days actually improves your performance because you go in fresh instead of burnt out.',
    reframedTo:
      'Cutting your study hours by 40-60% in the final days helps you go in fresh instead of burnt out.',
    reason:
      'The athletic taper improving competition performance is established in sport science, but transferring it to a precise "cutting study 40-60% improves exam performance" claim is an extrapolation with no direct study in students. The avoid-burnout rationale is kept; the asserted performance gain was removed so the sentence no longer claims a quantified improvement no source establishes.',
    date: '2026-06-24',
  },
  {
    id: 'points-optimization-001',
    module: 'The 625 Blueprint (Points Optimization)',
    section: 'Step 7 — Your 625 Blueprint',
    action: 'reframed',
    original:
      'marking standards are tightening. The generous adjustments from 2022-2024 are being phased out. You should prepare for tougher marking.',
    reframedTo:
      'the post-pandemic grade adjustments are being phased out, so the very high recent H1 rates are expected to ease back toward pre-2020 levels. It is sensible to prepare for tougher marking.',
    reason:
      'The verifiable SEC/Department of Education policy is the gradual unwinding of the post-2020 grade adjustments toward pre-2020 grade profiles; the original "marking standards are tightening / generous adjustments from 2022-2024" framing was tightened to that documented policy (cited to SEC examination statistics) rather than an unsourced claim about marker behaviour.',
    date: '2026-06-24',
  },
  {
    id: 'marking-scheme-decoder-001',
    module: 'The Marking Scheme Decoder',
    section: 'Step 3 — Reading a Real Marking Scheme',
    action: 'reframed',
    original:
      'PCLM — Partial Credit Level Marks. You get marks for each correct step in your answer independently.',
    reframedTo:
      'partial credit — on-the-right-track work earns part-marks. SEC schemes (especially Maths) award graduated partial credit (low, mid, or high) for the right approach, so each correct step earns its own credit.',
    reason:
      'SEC Mathematics marking schemes award graduated partial credit via "scales" with low/mid/high partial-credit descriptors; they do not use the acronym "PCLM (Partial Credit Level Marks)". The underlying concept (credit for correct steps even with a wrong final answer) is genuine and verifiable in the schemes, so the glossary item was reframed to the documented partial-credit mechanism and the coined acronym dropped.',
    date: '2026-06-24',
  },
  {
    id: 'answer-engineering-001',
    module: 'Answer Engineering',
    section: 'Step 1 — The Structure Gap',
    action: 'reframed',
    original:
      'Examiners read 400+ scripts. They spend 2-3 minutes per answer.',
    reframedTo:
      'Examiners work through large volumes of scripts under real time pressure during marking conferences. They give limited time to each answer.',
    reason:
      'The qualitative point (examiners mark at volume under time pressure, so findable structure matters) is well-supported and emphasised in Chief Examiner reports, but the specific figures "400+ scripts" and "2-3 minutes per answer" could not be verified against a locatable SEC source. The unverifiable precise numbers were removed and the verifiable qualitative claim kept.',
    date: '2026-06-24',
  },
  {
    id: 'subject-business-001',
    module: 'Mastering Business (subject)',
    section: 'Section 1 / Section 3 — exam structure',
    action: 'corrected',
    original:
      'Section 1 ... You answer 10 out of 15 questions, each worth 8 marks. ... Ten questions at 8 marks each.',
    reframedTo:
      'Section 1 ... You answer 8 short questions, each worth 10 marks. ... Eight questions at 10 marks each.',
    reason:
      'Factual error. The in-repo SEC Business HL 2025 marking scheme states Section 1 is "Answer 8 questions. Each question carries 10 marks." The original question count (10) and per-question marks (8) were both wrong; corrected against the marking scheme.',
    date: '2026-06-26',
  },
  {
    id: 'subject-business-002',
    module: 'Mastering Business (subject)',
    section: 'Sections 1, 3, 5, 6 — ABQ units',
    action: 'corrected',
    original:
      'The ABQ draws from Units 3, 4, and 5 of the syllabus: Management Activities, Managing People (HR), and Enterprise and Marketing.',
    reframedTo:
      'The 2025 ABQ drew from Units 2, 3, and 4 of the syllabus: Enterprise, Management, and Human Resources.',
    reason:
      'Factual error. The 2025 marking scheme labels the Applied Business Question "Units 2, 3 & 4", and the 2025 ABQ covered enterprise skills, management control, and HRM (no marketing). The unit numbers and topic set were corrected to the marking scheme, and the unit set is now stated as the 2025 set rather than implied to be fixed.',
    date: '2026-06-26',
  },
  {
    id: 'subject-business-003',
    module: 'Mastering Business (subject)',
    section: 'Section 1 — Section 3 selection',
    action: 'corrected',
    original:
      'You choose 4 from 7 questions, each worth 60 marks.',
    reframedTo:
      'You answer 4 questions, each worth 60 marks — at least one from Part 1 (People in Business / Business Environment) and one from Part 2.',
    reason:
      'The "4 questions x 60 marks = 240" was correct, but the selection rule was incomplete. The 2025 marking scheme specifies one question from each Part plus two further questions; the Part-selection constraint was added.',
    date: '2026-06-26',
  },
  {
    id: 'subject-business-004',
    module: 'Mastering Business (subject)',
    section: 'Section 2 — sub-part marks / depth',
    action: 'reframed',
    original:
      'Part (a) might be a definition or list worth 10-15 marks, part (b) asks for explanation worth 20-25 marks, and part (c) demands evaluation worth 20-25 marks. ... three well-developed points score higher than six shallow ones.',
    reframedTo:
      'Part (a) might be a definition or list, part (b) asks for explanation, and part (c) demands evaluation or application. ... fully developed points score higher than a longer list of one-word or undeveloped ones.',
    reason:
      'The specific per-part mark figures and the precise "three vs six points" ratio were invented (Section 3 part allocations vary by question in the scheme). Reframed to the verifiable developed-vs-undeveloped principle from the 2015 Chief Examiner report.',
    date: '2026-06-26',
  },
  {
    id: 'subject-mathematics-001',
    module: 'Mastering Mathematics (subject)',
    section: 'Section 1 — paper marks',
    action: 'corrected',
    original:
      'Higher Level Maths is split across two papers, each worth 150 marks ... That gives you a total of 300 marks across five hours.',
    reframedTo:
      'Higher Level Maths is split across two papers, each worth 300 marks ... a total of 600 marks across five hours.',
    reason:
      'Factual error. The in-repo 2015 Maths Chief Examiner\'s Report states each paper "is marked out of 300 marks." Each HL Maths paper is 300 marks (600 total), not 150 (300 total). Corrected, with the section bullets updated to match.',
    date: '2026-06-26',
  },
  {
    id: 'subject-mathematics-002',
    module: 'Mastering Mathematics (subject)',
    section: 'Section 1 — paper format',
    action: 'corrected',
    original:
      'Both papers have the same format: six questions, and you must answer all of them.',
    reframedTo:
      'Both papers have the same format: each is split into two sections — Section A (Concepts and Skills, 6 questions at 25 marks) and Section B (Contexts and Applications, usually 3 questions) — and you must answer all questions.',
    reason:
      'Factual error. Each paper is not "six questions"; the report describes Section A (6 questions at 25 marks each) plus Section B (Contexts and Applications, three questions in 2015). Corrected to the report\'s two-section structure.',
    date: '2026-06-26',
  },
  {
    id: 'subject-mathematics-003',
    module: 'Mastering Mathematics (subject)',
    section: 'Section 2 — scale marks',
    action: 'reframed',
    original:
      'A "5A" or "5B" scale means 5 marks are available, and partial credit is given for partially correct work.',
    reframedTo:
      'each part is graded on a numbered scale (for example out of 5 or out of 10), with partial credit built in at each level for partially correct work.',
    reason:
      'The scale letters in SEC Maths schemes indicate the number of credit gradations, not "marks available", so the original implied an inaccurate meaning. Reframed to the accurate numbered-scale-with-partial-credit description, which the Chief Examiner report supports.',
    date: '2026-06-26',
  },
  {
    id: 'subject-mathematics-004',
    module: 'Mastering Mathematics (subject)',
    section: 'Section 4 — time management',
    action: 'corrected',
    original:
      'With 6 compulsory questions in 150 minutes, you have roughly 25 minutes per question.',
    reframedTo:
      'Each paper is 300 marks in 150 minutes, so a useful rule of thumb is about a minute for every two marks — roughly 12-13 minutes on a 25-mark Section A question and around 25 minutes on a 50-mark Section B one.',
    reason:
      'Follow-on from the structure correction: there are ~9 questions across Section A and Section B, not 6, so "25 minutes per question" was wrong. Replaced with a marks-based pace derived from the verified 300-marks-in-150-minutes structure.',
    date: '2026-06-26',
  },

  // ─── Independent verification pass (2026-06-26) — upheld citation issues ─────
  {
    id: 'spaced-repetition-001',
    module: 'Mastering Spaced Repetition',
    section: '§4 The Best Review Schedule',
    action: 'reframed',
    original:
      'Your review gap should be roughly 5-20% of the time until the test … longer retention intervals call for proportionally longer gaps.',
    reframedTo:
      'A fraction of the time until the test — about 20-40% of the interval for a test a week away, shrinking to ~5-10% for a year away; the absolute gap grows, the proportion shrinks.',
    reason:
      'Verification pass: Cepeda et al. (2008) report the optimal gap as a PROPORTION of the test delay DECLINES (≈20-40% at 1 week → ≈5-10% at 1 year). The original both truncated the short-delay band (5-20%) and stated the proportion direction backwards ("proportionally longer gaps").',
    date: '2026-06-26',
  },
  {
    id: 'answer-engineering-002',
    module: 'Answer Engineering',
    section: '§3 The Science Answer Stack',
    action: 'reframed',
    original:
      'In a 25-mark question, the answer is worth only 4-5 marks … most science and maths questions … only 4-5 out of 25 marks … skipping 80% of the available marks.',
    reframedTo:
      'The final answer earns only a small share of the marks; the majority are for showing your method and working.',
    reason:
      'Verification pass: the generic SEC marking-scheme archive (the cited source) does not establish a fixed 4-5/25 split — schemes use question-specific partial-credit scales. The specific "4-5 of 25" and "80%" figures were dropped; only the supported qualitative claim (most marks are for method) is kept.',
    date: '2026-06-26',
  },
  {
    id: 'exam-hall-strategies-001',
    module: 'Exam Hall Strategies',
    section: '§4 Order of Attack',
    action: 'reframed',
    original:
      'Your brain keeps working on it in the background, so the answer often clicks when you come back to it later.',
    reframedTo:
      'Stepping away can sometimes help: taking a break before you return to a stubborn question may let the answer come more easily.',
    reason:
      'Verification pass: Sio & Ormerod (2009) find incubation helps most for divergent tasks and least when the break is filled with other high-demand work — the exam case. The prescriptive/causal "often clicks when you come back" was softened to non-prescriptive "can sometimes help."',
    date: '2026-06-26',
  },
  {
    id: 'exam-hall-strategies-002',
    module: 'Exam Hall Strategies',
    section: '§6 Staying Calm Under Pressure',
    action: 'reframed',
    original:
      'The fastest trick is Box Breathing … It physically calms your nervous system down in under a minute.',
    reframedTo:
      'One reliable tool is slow, structured breathing — like Box Breathing — to settle your nervous system.',
    reason:
      'Verification pass: Balban et al. (2023) show arousal reduction for structured breathwork broadly (especially cyclic sighing) over daily practice, not a box-breathing-specific or acute "under a minute" effect. The technique-specific and acute claims were dropped.',
    date: '2026-06-26',
  },
  {
    id: 'reverse-engineering-001',
    module: 'Reverse Engineering the Exam',
    section: '§2 Why backwards works (Future Thinking)',
    action: 'reframed',
    original:
      'Picturing exam day makes each step feel necessary and keeps you motivated. … It is a motivation boost.',
    reframedTo:
      'Picturing exam day makes the future feel real and weigh more in today\'s choices, so it is easier to follow through on each step.',
    reason:
      'Verification pass: Peters & Büchel (2010) measure episodic future thinking reducing delay discounting (intertemporal choice), not "motivation". Reframed to the delay-discounting mechanism the study establishes.',
    date: '2026-06-26',
  },
  {
    id: 'teaching-effect-002',
    module: 'The Teaching Effect',
    section: '§3 / §4 self-explanation',
    action: 'reframed',
    original:
      'students who paused to explain each step to themselves solved far more new problems than those who just read … Actively creating explanations beats passive reading every time.',
    reframedTo:
      'the students who spontaneously explained each step to themselves went on to solve far more new problems … actively creating explanations is linked to deeper learning than passively reading.',
    reason:
      'Verification pass: Chi et al. (1989) is correlational (good vs poor solvers; explanation measured, not manipulated; no passive-reading control). The "than those who just read" / "beats passive reading every time" causal head-to-head was softened to the association the study supports.',
    date: '2026-06-26',
  },
  {
    id: 'points-optimization-002',
    module: 'The 625 Blueprint (Points Optimization)',
    section: '§3 H1 Probability Map + dashboard',
    action: 'corrected',
    original:
      'Physics and Chemistry sit around 18-22%. English … historically sits at just 3-5% (rising to 7-11%). [dashboard: Physics 20, Chemistry 19]',
    reframedTo:
      'Qualitative tiers (sciences relatively high; English/Geography among the lowest, only a few percent); dashboard Physics 20→11, Chemistry 19→12; footnote relabelled "illustrative relative estimates, not official published figures".',
    reason:
      'Verification pass: the specific bands were contradicted by publicly reported SEC figures (Physics/Chemistry ~7-13% not 18-22%; English ~6-7% not 3-5%). Unverifiable/incorrect precise figures removed; only the robust directional claim is asserted.',
    date: '2026-06-26',
  },
  {
    id: 'points-optimization-003',
    module: 'The 625 Blueprint (Points Optimization)',
    section: '§7 Your 625 Blueprint',
    action: 'reframed',
    original:
      'the very high recent H1 rates are expected to ease back toward pre-2020 levels.',
    reframedTo:
      'recent H1 rates have been unusually high by historical standards, and the temporary post-pandemic grade adjustments are being wound down — so today\'s rates may not hold.',
    reason:
      'Verification pass: a backward-looking SEC statistics source cannot support a forward-looking forecast. Reframed to the verifiable historical observation plus the separately-announced phase-out, with no forecast asserted.',
    date: '2026-06-26',
  },
  {
    id: 'examiners-chair-spanish-001',
    module: "The Examiner's Chair — Spanish",
    section: 'Session Sp4',
    action: 'reframed',
    original:
      'Don’t hedge the aural list — a listening item asks for one detail; the candidate writes two (one right, one wrong). In the aural vocabulary-list items, a wrong extra answer cancels a correct one. Cited to p.5 ("aural: wrong extra cancels a correct answer").',
    reframedTo:
      'Copy the phrase exactly — a finding-a-phrase transcription item requires the exact words from the text; padding a correct phrase with extra words voids the item ("No marks awarded if extra words are added. Exact transcription required", p.5). Recast from an aural lesson to the genuine written transcription rule.',
    reason:
      'Second-year verification (2023/2024/2025): the cited "aural wrong-extra-cancels" rule does not exist in the Spanish aural section in any of the three years, and p.5 is a written Section A rule. Retargeted the session to the real, verifiable exact-transcription rule that p.5 actually states.',
    date: '2026-07-06',
  },
  {
    id: 'examiners-chair-economics-001',
    module: "The Examiner's Chair — Economics",
    section: 'Subject coverage note',
    action: 'corrected',
    original:
      'two-point questions are front-loaded (1st @ 8 / 2nd @ 4), and there is no omission-of-% deduction at OL. Verified against the 2025 OL scheme.',
    reframedTo:
      'two-point questions are front-loaded (1st @ 8 / 2nd @ 4), so the first point banks the most marks. Verified against the 2025 and 2023 OL schemes.',
    reason:
      'Second-year verification (2023): the 2023 OL scheme DOES apply an omission-of-% deduction ("Deduct 1 mark for omission of % sign"), so the "no omission-of-% deduction at OL" claim was year-specific and inaccurate as a general statement. Dropped the unstable clause; kept the stable front-loading difference.',
    date: '2026-07-06',
  },
  {
    id: 'examiners-chair-italian-001',
    module: "The Examiner's Chair — Italian",
    section: 'Session IT2',
    action: 'reframed',
    original:
      'The scheme applies a 50% deduction for answering in the wrong language. … answering in Italian where English is required halves your marks.',
    reframedTo:
      'The 2025 scheme applies a 50% deduction for answering in the wrong language. The English-answer requirement is standing across years, but the explicit −50% figure is stated in the 2025 scheme (not reproduced in 2023/2024) — so the magnitude is pinned to 2025.',
    reason:
      'Second-year verification (2023/2024): the English-answer requirement for the opinion question is stable across years, but the explicit "−50% of marks gained" clause appears only in the 2025 scheme. Pinned the magnitude to 2025 rather than implying a timeless standing rule (the in-app cite was already stamped 2025, so this is a precision fix).',
    date: '2026-07-06',
  },
  {
    id: 'examiners-chair-accounting-001',
    module: "The Examiner's Chair — Accounting",
    section: 'Session AC2',
    action: 'reframed',
    original:
      'A Balance Sheet carries a discrete mark for both totals agreeing (marked with a *). … scale name "Both totals correct *".',
    reframedTo:
      'A Balance Sheet carries a discrete mark for both totals agreeing — a presentation mark separate from the line figures. (Dropped the literal "*" wording: the 2024 scheme flags the mark with a * annotation, the 2023 scheme with an examiner arrow — the mark itself is the standing convention.)',
    reason:
      'Second-year verification (2023): the concept (a discrete agreeing-totals mark) is stable, but the literal "Both totals correct *" asterisk string is a 2024 presentation choice absent from the 2023 scheme. Made the wording year-neutral so it does not imply the asterisk notation is universal.',
    date: '2026-07-06',
  },
  {
    id: 'examiners-chair-engineering-001',
    module: "The Examiner's Chair — Engineering",
    section: 'Session EN1',
    action: 'corrected',
    original:
      'In "Any N @…" parts only the first N answers count — extras score nothing and can push your best material outside the counted set… Only the first three answers are marked… if your strongest points come fourth and fifth they fall outside the counted three and score nothing.',
    reframedTo:
      'In "Any N @…" parts only N answers are credited — extra answers earn nothing, so over-answering only costs you time. And each mark is earned by proper discussion, not a bare mention. Pick your strongest N and develop them. (Recast the whole session: fewer developed points beat more thin ones.)',
    reason:
      'Second-year verification (2024/2025): the scheme states the "Any N" cap but is SILENT on which excess answers are read; the "only the first N count / best material wasted" claim is unsupported and contradicts the repo\'s own 2025 insights ("only the best N are read"). Recast EN1 onto the accurate, load-bearing lesson (N-credited cap + proper-discussion requirement) so it no longer teaches order-dependence the scheme does not apply.',
    date: '2026-07-06',
  },
  {
    id: 'examiners-chair-religiouseducation-001',
    module: "The Examiner's Chair — Religious Education",
    section: 'Session RE3 (OL)',
    action: 'corrected',
    original:
      'There is no HL-style "you didn\'t evaluate" cap — the OL scheme uses "Max" zero times. / OL commands are lower-order: Outline, Describe, Give an account.',
    reframedTo:
      'There is no HL-style descriptive cap at OL: a description is not ceilinged at Fair for "not evaluating." Where an OL note applies a "Max", it caps a partial answer that omits a required element — not a description. / OL centres on lower-order skills … but even where an OL question uses a higher-order stem, the scheme does not cap a description at Fair.',
    reason:
      'Second-year verification (2024): the "OL uses Max zero times" count is true for 2025 but FALSE for 2024 OL (which uses "max" twice, as partial-answer caps), and "OL commands are exclusively lower-order" is overstated (2024 OL uses Discuss/Profile/Explore). Reframed to the underlying year-stable principle (no descriptive Fair-cap at OL; the OL "Max" caps that exist are partial-answer caps) and dropped the brittle count.',
    date: '2026-07-06',
  },
  {
    id: 'examiners-chair-classical-001',
    module: "The Examiner's Chair — Classical Studies",
    section: 'Sessions CL2 & CL3',
    action: 'reframed',
    original:
      'CL2 one-part ceiling stated as "~57/80"; CL3 Overall-Quality band edges shown as Low (1–12) / Good (13–17) / High (18–20).',
    reframedTo:
      'CL2 ceiling reframed to "the mid-50s/80"; CL3 band labels reduced to Low/Good/High with the numeric edges removed. The load-bearing rules — the units-of-development structure and the verbatim Low-band descriptor "relies mostly on narrative" — are unchanged (both CONFIRMED stable across 2024 and 2025).',
    reason:
      'Second-year verification (2024): the Overall-Quality band edges are year-specific (2024 = 1–10/11–15/16–20 vs 2025 = 1–12/13–17/18–20), and the "57" ceiling is the 2025 value (2024 = 55). Removed the year-specific numbers from the student-facing scale while keeping the stable structure and the confirmed "relies mostly on narrative" descriptor.',
    date: '2026-07-06',
  },
  {
    id: 'subject-english-001',
    module: 'Mastering English',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Section I has two comprehension texts (Question A, worth 50 marks each — you do both)',
    reframedTo:
      'Section I — Comprehending (100 marks), which presents three texts on a shared theme — you answer a Question A (50 marks, comprehension) on one text and a Question B (50 marks, a functional writing task) on a different text (you may not answer both on the same text)',
    reason:
      'Paper 1 Section I is Question A on one text + Question B on a different text, not two Question A\'s. Confirmed examiner-reports/english/2025-marking-scheme.md lines 143-144. The old text omitted Question B (a 50-mark / 12.5% functional-writing task).',
    date: '2026-07-21',
  },
  {
    id: 'subject-english-002',
    module: 'Mastering English',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'and [[Unseen Poetry]] (a poem you have never seen before, followed by a comparison with a second poem — 70 marks). [Highlight: \'a guided question on it (20 marks), then get a second poem and compare both (30 marks for the comparison, 20 marks for the second poem individually). Total: 70 marks.\']',
    reframedTo:
      'and [[Poetry]] (70 marks total, in two parts: an Unseen Poem — 20 marks — and Prescribed Poetry, an essay on one of your studied poets — 50 marks). [Highlight rewritten to Unseen 20 + Prescribed 50.]',
    reason:
      'The 70-mark two-poem unseen comparison does not exist. The real Paper 2 Section III is Unseen Poem 20 + Prescribed Poetry 50. Confirmed examiner-reports/english/2024-marking-scheme.md lines 1801-1857. Prescribed Poetry (50 marks, the studied poets) had been omitted entirely.',
    date: '2026-07-21',
  },
  {
    id: 'subject-english-003',
    module: 'Mastering English',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Each criterion carries roughly equal weight, and together they define the difference between an H5 and an H1.',
    reframedTo:
      'The published split is Purpose 30%, Coherence 30%, Language 30%, Mechanics 10% — so the first three criteria dominate, and Purpose has primacy (the marks for Coherence or Language can never exceed the marks awarded for Purpose).',
    reason:
      'PCLM is not equally weighted: Mechanics is 10%. Confirmed examiner-reports/english/2025-marking-scheme.md lines 66-69 and the Purpose-primacy rule at lines 85-86.',
    date: '2026-07-21',
  },
  {
    id: 'subject-irish-001',
    module: 'Mastering Irish',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'the [[Scrúdú Béil (Oral Exam)]] worth 240 marks (40%), Paper 1 worth 120 marks (20%), Paper 2 worth 160 marks (approximately 27%), and the [[Scrúdú Cluastuisceana (Aural Exam)]] worth 80 marks (approximately 13%). At Ordinary Level, the oral is worth 240 marks out of 500, making it an even larger proportion — 48%.',
    reframedTo:
      'the [[Scrúdú Béil (Oral Exam)]] worth 240 marks (40%), Paper 1 worth 160 marks (approximately 27%), and Paper 2 worth 200 marks (approximately 33%). Paper 1 contains the [[Scrúdú Cluastuisceana (Aural Exam)]], An Chluastuiscint, worth 60 marks (10% of your grade), alongside the composition. The oral is a common paper at both levels — 240 marks out of 600, 40%.',
    reason:
      'SEC HL breakdown is Oral 240 / Paper 1 160 (Cluastuiscint 60 + Ceapadóireacht 100) / Paper 2 200; total 600. Confirmed examiner-reports/irish/2026-assessment-arrangements-oral.md pp.39-40. The old 120/160/80 split and the OL 240/500=48% claim were wrong.',
    date: '2026-07-21',
  },
  {
    id: 'subject-irish-002',
    module: 'Mastering Irish',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The essay is typically worth 50 marks or more.',
    reframedTo:
      'worth 100 marks at Higher Level. You choose one piece from a range of formats (essay, story, debate/speech, or discussion), so you can play to your strengths.',
    reason:
      'The HL Ceapadóireacht is 100 marks, not \'50 or more\'. Confirmed examiner-reports/irish/2026-assessment-arrangements-oral.md (\'An Cheapadóireacht (100 marc)\') and 2025-insights.md line 29.',
    date: '2026-07-21',
  },
  {
    id: 'subject-irish-003',
    module: 'Mastering Irish',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'It runs for 2 hours 50 minutes. ... It runs for 3 hours 20 minutes.',
    reframedTo:
      '[duration specifics removed; papers described by component instead]',
    reason:
      'These were the English Paper 1/2 durations copy-carried into Irish. No Irish paper duration is confirmable from examiner-reports or subjectTiming.ts (which gives Irish P2=165min, conflicting with the audit\'s 3h05, and no P1 figure) — so the unverified specifics were dropped per the HARD RULE rather than replaced with a guess.',
    date: '2026-07-21',
  },
  {
    id: 'subject-french-001',
    module: 'Mastering French',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'the [[Aural Exam (Listening)]] worth 100 marks (25%), and the [[Written Exam]] worth 200 marks (50%) ... the oral and aural together account for 50% of your total. ... The written exam is a 2 hour 50 minute paper worth 200 marks ... reading and writing sections are each worth approximately 100 marks.',
    reframedTo:
      'the [[Aural Exam (Listening)]] worth 80 marks (20%), and the [[Written Exam]] worth 220 marks (55%) ... oral and aural together account for 45%. ... a 2 hour 30 minute paper worth 220 marks ... Reading Comprehension (120 marks) and Written Expression (100 marks).',
    reason:
      'The 25/25/50 split is the OL allocation; HL is Oral 25 / Aural 20 / Reading 30 / Writing 25. Confirmed examiner-reports/french/2025-marking-scheme.md (Section A 120, Section B 100, Listening 80) + lc-french-syllabus.md HL table. Duration 150 min per subjectTiming.ts \'mfl\'.',
    date: '2026-07-21',
  },
  {
    id: 'subject-german-001',
    module: 'Mastering German',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '[[Aural Exam]] worth 100 marks (25%), and the [[Written Exam]] worth 200 marks (50%) ... determine half your grade ... written paper runs for 2 hours 50 minutes ... Reading Comprehension (approximately 100 marks) and Written Production (approximately 100 marks).',
    reframedTo:
      '[[Aural Exam]] worth 80 marks (20%), and the [[Written Exam]] worth 220 marks (55%) ... determine 45% of your grade ... 2 hours 30 minutes ... Reading Comprehension (120 marks) and Written Production (100 marks).',
    reason:
      'HL split is Oral 25 / Aural 20 / Reading 30 / Writing 25. Confirmed examiner-reports/german/2025-marking-scheme.md line 922 (Listening 80) + german-syllabus.md lines 800-805. Duration 150 min per subjectTiming.ts.',
    date: '2026-07-21',
  },
  {
    id: 'subject-german-002',
    module: 'Mastering German',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Students who invest in oral preparation often score 15 to 20 marks higher than their written paper performance would predict.',
    reframedTo:
      'Because so much of the oral is within your control, students who invest in it reliably outperform what their written paper alone would predict.',
    reason:
      'Uncited invented statistic; no SEC or peer-reviewed source. Reframed qualitatively per the accreditation cut-log rule.',
    date: '2026-07-21',
  },
  {
    id: 'subject-spanish-001',
    module: 'Mastering Spanish',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'the [[Aural Exam]] is worth 100 marks (25%), and the [[Written Exam]] is worth 200 marks (50%) ... 50% of your grade is determined by your speaking and listening ... covering: your prepared topic (tema preparado) ... and discussion of visual or situational stimuli. ... 2 hours 50 minutes ... Reading Comprehension (approximately 100 marks) and Written Expression (approximately 100 marks).',
    reframedTo:
      'the [[Aural Exam]] is worth 80 marks (20%), and the [[Written Exam]] is worth 220 marks (55%) ... 45% ... (a) a general conversation (optional literary-work discussion) and (b) a role-play situation, 15 minutes ... 2 hours 30 minutes ... three sections; reading ~120 + written production ~100 incl. the 50-mark Linked Question.',
    reason:
      'Marks corrected against examiner-reports/spanish/2025-insights.md (aural 80, written 220, Sections A/B/C, 50-mark Linked Question). The \'tema preparado\' component does not exist — the LC Spanish oral is general conversation + role-play (spanish-syllabus.md \'Oral Assessment\'). Duration 150 min per subjectTiming.ts.',
    date: '2026-07-21',
  },
  {
    id: 'subject-italian-001',
    module: 'Mastering Italian',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '[[Aural Exam]] worth 100 marks (25%), and the [[Written Exam]] worth 200 marks (50%). The structure is identical to French, German, and Spanish ... 2 hours 50 minutes ... Reading Comprehension (approximately 100 marks) and Written Production (approximately 100 marks).',
    reframedTo:
      '[[Aural Exam]] worth 80 marks (20%), and the [[Written Exam]] worth 220 marks (55%). Italian shares the same broad shape ... but has a distinctive prescribed-literature strand ... 2 hours 30 minutes ... Reading Comprehension (120 marks: Section A journalistic 60 + Section B literary 60) and Written Production (Section C, 100 marks).',
    reason:
      'Marks corrected against examiner-reports/italian/2025-marking-scheme.md lines 142-150 (Listening 80/Reading 120/Writing 100) + italian-syllabus.md HL table. The \'identical structure\' claim is refuted by the prescribed-literature strand (2025-insights.md lines 100-104), now added. Duration 150 min per subjectTiming.ts.',
    date: '2026-07-21',
  },
  {
    id: 'subject-japanese-001',
    module: 'Mastering Japanese',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'follows the same three-component structure as the European languages ... The [[Oral Exam]] is worth 100 marks (25%), the [[Aural Exam]] is worth 100 marks (25%), and the [[Written Exam]] is worth 200 marks (50%) ... approximately 40 minutes ... 2 hours 50 minutes ... reading section is worth approximately 100 marks and the writing section approximately 100 marks. ... Kanji written with incorrect stroke order often look \'off\' to the examiner [and] may not be accepted.',
    reframedTo:
      'assesses the same core skills ... through an Oral, Aural and Written Exam. Confirm the exact mark allocation and weighting for your year from the SEC paper and your teacher ... [all durations/marks removed] ... a Kanji the examiner cannot read clearly cannot earn its marks; practising correct stroke order is the reliable route to clean, legible characters.',
    reason:
      'No in-repo source (no examiner-reports/japanese, not in subjectTiming.ts) and SEC/NCCA/curriculumonline pages were unreachable (403/404), so none of the Japanese weightings, durations, or the 25/25/50 split (internally inconsistent with the HL 25/20/55 pattern it claimed to match) could be grounded. All specifics reframed per the HARD RULE; the stroke-order marking-consequence claim softened to legibility.',
    date: '2026-07-21',
  },
  {
    id: 'subject-mathematics-001',
    module: 'Mastering Mathematics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Both papers have the same format: each is split into [[two sections]] — Section A and Section B — and you must answer **all** questions. There is no choice -- every question counts.{{cite:1}}',
    reframedTo:
      'Both papers have the same format: each is split into [[two sections]] — Section A (Concepts and Skills) and Section B (Contexts and Applications) — and there **is** some choice within each section, so you do not have to answer every question. Always check the instructions box on the front of the current year\'s paper for the exact number to answer.',
    reason:
      'Stale/false: the 2025 SEC HL Maths papers (P1 & P2) rubric reads \'Answer any five questions from Section A\' and \'any three from Section B\' — there IS choice. The old claim described the pre-reform no-choice paper and was mis-cited to the 2015 Chief Examiner report; cite removed because that source does not ground the current structure.',
    date: '2026-07-21',
  },
  {
    id: 'subject-mathematics-002',
    module: 'Mastering Mathematics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '**Section A (Concepts and Skills)** is 6 questions at 25 marks each (150 marks); **Section B (Contexts and Applications)** is typically 3 longer questions making up the other 150 marks.{{cite:1}}',
    reframedTo:
      'On the recent papers, **Section A (Concepts and Skills)** presents 6 questions worth 150 marks and asks you to answer **any five** of them; **Section B (Contexts and Applications)** presents 4 questions worth 150 marks and asks you to answer **any three**. ... Because the exact number of questions and the choice can be adjusted from year to year, read the instructions on the front of your paper first.',
    reason:
      'Wrong figures: Section A questions are 30 marks each (150 / any 5 of 6), not 25; Section B is 4 questions (answer any 3), not \'typically 3\'. Grounded in SEC 2025 HL Maths P1/P2 front-page Instructions. Cite:1 (2015 report) removed as it does not support the current structure.',
    date: '2026-07-21',
  },
  {
    id: 'subject-applied-maths-001',
    module: 'Mastering Applied Maths',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Applied Maths consists of a **single exam paper** lasting **2 hours and 30 minutes**. The paper contains **10 questions**, and you must answer **6 of them**. Each question is worth **50 marks**, giving a total of **300 marks**. ... There is no coursework, no practical component, and no oral or aural. It is purely an exam-based subject.',
    reframedTo:
      'Under the current specification (first examined 2023), Applied Maths is assessed in **two components**: a **written paper worth 400 marks (80% of your grade)** lasting **2 hours and 30 minutes**, and a separate **Mathematical Modelling Project worth 100 marks (20%)**. ... On the written paper there are **10 questions, each worth 50 marks, and you answer any 8 of them**.',
    reason:
      'The entry described the discontinued pre-2023 syllabus. SEC 2025 HL Applied Maths paper: 400 marks, \'Answer any eight questions\' of ten at 50 marks each; examiner-reports/applied-maths/2024-insights.md confirms a separate 100-mark (20%) Mathematical Modelling Project. The 300-marks / answer-6 / no-coursework claims are all false for current students.',
    date: '2026-07-21',
  },
  {
    id: 'subject-applied-maths-002',
    module: 'Mastering Applied Maths',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The 10 questions map directly onto 10 topics from the syllabus: [[Linear Motion]], [[Projectiles]], [[Newton\'s Laws]], [[Connected Particles]], [[Moments and Equilibrium]], [[Statics]] (including inclined planes), [[Collisions]] (including oblique impacts), [[Circular Motion]], [[Simple Harmonic Motion]] (SHM), and [[Differential Equations]]. Each topic gets exactly one question every year, so the paper is highly predictable.',
    reframedTo:
      'The questions are drawn from across the current strands: [[Mathematical Modelling]], [[Kinematics and Dynamics]] (linear motion, projectiles, connected particles, collisions, circular and relative motion, friction), [[Difference Equations]], [[Networks and Graph Theory]], and [[Algorithms]]. Recent papers mix these throughout ...',
    reason:
      'Old-syllabus topic list. SHM, conical pendulums, oblique impacts and statics/ladders are not the current standalone topics; the revised spec (first examined 2023) introduced networks/graph theory, difference equations and algorithms. Topics verified from the 2025 SEC HL Applied Maths paper and examiner-reports/applied-maths/2024-marking-scheme.md (Prim\'s/Kruskal\'s/Dijkstra\'s algorithms, adjacency matrices, difference-equation models).',
    date: '2026-07-21',
  },
  {
    id: 'subject-applied-maths-003',
    module: 'Mastering Applied Maths',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The marking scheme uses a **cumulative approach** -- if you make an error early in a solution but then solve correctly from that point, you can still earn [[follow-through marks]] for all subsequent correct work. ... Drawing a correct [[free-body diagram]] ... can be worth **10-15 marks** before you even start solving.',
    reframedTo:
      'The marking scheme runs on a **penalty model**: examiners start from the full mark for a step and deduct for classified errors -- a method error (\'blunder\') costs 3 marks, while a minor arithmetic or transcription **slip costs only 1 mark**. ... a slip that *oversimplifies* the problem is re-priced as a 3-mark blunder. (Setup paragraph reframed to remove the \'10-15 marks\' specific.)',
    reason:
      'The scheme is subtractive (blunder -3, slip -1), not an additive \'cumulative/follow-through\' model, per examiner-reports/applied-maths/2024-insights.md and 2024-marking-scheme.md instruction 4-5. The \'10-15 marks before you start\' figure is unverifiable and was removed per the HARD RULE.',
    date: '2026-07-21',
  },
  {
    id: 'subject-applied-maths-004',
    module: 'Mastering Applied Maths',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Most students can master both topics with 4-5 hours of focused practice. ... you can solve nearly every collision problem that has appeared in the last 15 years. ... You only need 6 ... Pick your 6 best topics ... approximately 25 minutes per question.',
    reframedTo:
      'You answer 8 of the 10 written-paper questions, so the biggest strategic move is breadth ... (effort/\'15 years\' claims removed; timing corrected to ~18-19 minutes per question, 8 questions in 150 minutes).',
    reason:
      'The whole \'pick 6, ignore the rest\' strategy is unsafe: current students answer any 8 of 10 and must also do the 20% project. The \'4-5 hours\', \'last 15 years\' and 25-min-per-question specifics are unverifiable/wrong and were removed or corrected against the SEC 2025 paper.',
    date: '2026-07-21',
  },
  {
    id: 'subject-chemistry-001',
    module: 'Mastering Chemistry',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '[[Section A]] is worth **120 marks** and typically contains around **5 experiment-based questions** -- you must answer **3 of them**. Each is worth **40 marks**. ... [[Section B]] is worth **280 marks** and contains **8 questions** -- you must answer **5 of them**. Each question is worth **56 marks**.',
    reframedTo:
      'Across the whole paper there are **11 questions**, every one worth **50 marks**, and you answer **8 of them** -- 400 marks. [[Section A]] is the experiment section: **3 questions (Q1-Q3)**, answer **at least two**, 50 marks each. [[Section B]] is the theory section: **8 questions (Q4-Q11)**, each 50 marks.',
    reason:
      'These were the Leaving Cert PHYSICS figures (the text even said \'Like Physics\'). Real SEC Chemistry structure per examiner-reports/chemistry/2024-insights.md: 11 questions, all 50 marks, answer 8 = 400 marks; Q1-Q3 experiments (answer at least two), Q4-Q11 theory.',
    date: '2026-07-21',
  },
  {
    id: 'subject-chemistry-002',
    module: 'Mastering Chemistry',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'A student who thoroughly prepares all the experiments can realistically score **100-120 marks** in Section A. ... On exam day, allocate roughly 45 minutes for Section A and 2 hours 15 minutes for Section B.',
    reframedTo:
      'You must answer at least two of the three experiment questions, each worth 50 marks ... can realistically bank **100-150 marks** here. ... if you answer two experiment questions from Section A and six from Section B, that works out at about 45 minutes on Section A and 2 hours 15 minutes on Section B.',
    reason:
      'Section A ceiling recomputed for the real 50-marks-per-question paper (2 x 50 = 100 up to 3 x 50 = 150), not the false 120. Timing re-tied to the real answer pattern (2 from A + 6 from B); the 45/135 split is consistent with data/knowledge/subjectTiming.ts.',
    date: '2026-07-21',
  },
  {
    id: 'subject-computer-science-001',
    module: 'Mastering Computer Science',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The [[written exam]] is a **2-hour paper** worth **70%** of your grade. ... The [[Applied Learning Task]] (ALT) ... submitted as a portfolio including your code, documentation, and a reflective journal.',
    reframedTo:
      'The [[end-of-course exam]] is worth **70%** of your grade and is delivered as a **computer-based examination** -- you sit it at a computer ... there are **practical questions that require you to use a programming language at the computer** (writing, running, testing, and debugging code in the exam environment). ... The [[coursework project]] ... develop, and document a computational artefact ... submitted with a report.',
    reason:
      'LCCS is a computer-based exam, not a conventional written paper (a defining feature that changes prep). Official curriculumonline.ie specification: exam is \'Written and computer-based\', with \'Practical questions requiring the use of a programming language\'; the 30% component is \'One computational artefact with report\', not the formative ALTs. Unverifiable \'2-hour\' duration removed rather than replaced (no source-1/2/3 confirmation).',
    date: '2026-07-21',
  },
  {
    id: 'subject-ag-science-001',
    module: 'Mastering Agricultural Science',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The assessment consists of a **written exam paper** ... and [[Classroom-Based Assessments]] (CBAs) completed during the course. ... While the CBAs themselves do not carry a direct percentage of the final exam mark in the same way as the CS ALT ... The written paper is divided into three sections. [[Section A]] ... [[Section B]] ... [[Section C]] ...',
    reframedTo:
      'Agricultural Science is assessed in **two components**: a **written exam paper** worth **75%** (300 marks) and the [[Individual Investigative Study]] (IIS) coursework worth **25%** (100 marks), for a total of **400 marks**. ... The written paper is divided into two sections. [[Section A]] ... **any 10 questions at 10 marks each** (100 marks) ... [[Section B]] ... **any 4 questions at 50 marks each** (200 marks).',
    reason:
      'LC Ag Science has NO CBAs (a Junior Cycle construct). The practical component is the Individual Investigative Study, worth 25% (written paper 75%) — not a component with \'no direct percentage\'. The paper has two sections (A short / B long), not three A/B/C. All grounded in examiner-reports/agricultural-science/2024-insights.md and 2024-marking-scheme.md.',
    date: '2026-07-21',
  },
  {
    id: 'subject-accounting-001',
    module: 'Mastering Accounting',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The paper is split into [[three sections]]. **Section 1** contains short questions worth **120 marks** in total — you answer **four** out of six questions, each carrying 30 marks. These are designed to be completed relatively quickly and test breadth across the syllabus. **Section 2** has three compulsory long questions worth **60 marks each** (180 marks total). **Section 3** is one extended question worth **100 marks** — this is the big one, typically a full set of final accounts.',
    reframedTo:
      'The paper is split into [[three sections]]. **Section 1 — Financial Accounting** is worth **120 marks**: you either answer the single **120-mark Q1** (a full set of final accounts — the sole trader, company, or manufacturing account) **or** answer **any two of Q2–Q4 at 60 marks each**. **Section 2 — Financial Accounting** is worth **200 marks**: you answer **two of Q5–Q7, each worth 100 marks** (areas like interpretation of accounts, cash flow, published accounts, or correction of errors). **Section 3 — Management Accounting** is worth **80 marks**: you answer **one of Q8–Q9** (budgeting, costing, or flexible budgets).',
    reason:
      'The described structure is fabricated and contradicts the SEC paper. Per examiner-reports/accounting/2024-insights.md (verified against the 2024 SEC marking scheme) and data/knowledge/subjectTiming.ts: Section 1 = Financial Accounting 120 marks (Q1 alone or two of Q2–Q4 at 60); Section 2 = Financial Accounting 200 marks (two of Q5–Q7 at 100); Section 3 = Management Accounting 80 marks (one of Q8–Q9). Final accounts are Section 1 Q1, not a 100-mark Section 3.',
    date: '2026-07-21',
  },
  {
    id: 'subject-accounting-002',
    module: 'Mastering Accounting',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The **Section 3 question** is worth **100 marks** — that is **25% of the entire paper** in a single question. It almost always involves preparing a full set of [[final accounts]] … Here is the strategic point most students miss: **Section 1 and Section 3 together account for 220 of 400 marks** — over half the paper.',
    reframedTo:
      'The single biggest question on the paper is **Section 1 Q1**, worth **120 marks** — that is **30% of the entire paper** in one question. It almost always involves preparing a full set of [[final accounts]] … Here is the strategic point most students miss: **Section 1 (120 marks) and Section 2 (200 marks) together account for 320 of 400 marks** — four-fifths of the paper.',
    reason:
      'Every downstream strategic claim inherited the fabricated structure. Final accounts are Section 1 Q1 (120 marks = 30%), not Section 3 (which is Management Accounting, 80 marks). The \'220 of 400\' figure was built on the wrong section sizes; corrected to the verified Section 1 (120) + Section 2 (200) = 320. Source: examiner-reports/accounting/2024-insights.md.',
    date: '2026-07-21',
  },
  {
    id: 'subject-accounting-003',
    module: 'Mastering Accounting',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'You must allocate time proportionally: roughly 25 minutes for Section 1, 75 minutes for Section 2 (25 each), and 45 minutes for Section 3, with a few minutes for review.',
    reframedTo:
      'Allocate time in proportion to the marks — roughly **0.45 minutes per mark**: about **54 minutes for the 120-mark Section 1 Q1**, about **90 minutes for Section 2** (roughly 45 minutes for each 100-mark question), and about **36 minutes for the 80-mark Section 3**, with a few minutes left for review.',
    reason:
      'Timing computed from the wrong structure would starve the highest-value question. Recomputed at the verified 0.45 min/mark on the real 120/200/80 split. Source: examiner-reports/accounting/2024-insights.md (\'≈ 0.45 min/mark, so the 120-mark Q1 warrants ~54 minutes\'); subjectTiming.ts lines 83-85 (54/90/36).',
    date: '2026-07-21',
  },
  {
    id: 'subject-economics-001',
    module: 'Mastering Economics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The Leaving Certificate Economics Higher Level exam is a **single paper** lasting **2 hours and 30 minutes**, worth a total of **400 marks**. It is divided into [[two sections]] … **Section A** contains short questions worth **100 marks (25%)**. You answer **5 out of 9** questions, each worth **20 marks** … **Section B** … It contains long questions worth **300 marks (75%)**. You choose **4 from 7** questions, each worth **75 marks** … With 150 minutes for 400 marks, you have about **22 seconds per mark** … roughly **28-30 minutes per long question**.',
    reframedTo:
      'Leaving Certificate Economics has **two assessment components**: a **written examination worth 80%** … and a **Student Research Project (SRP) worth 20%** … The written paper lasts **two and a half hours** … **Section A** is worth **75 marks**. It is a set of short questions built around stimulus material … **Section B** is the extended-response section — six themed long questions (**Q11–Q16**) … This is where most of the written-paper marks sit, so disciplined pacing across the two and a half hours is essential.',
    reason:
      'The module described the pre-2019 Economics exam, retired after 2020. The current specification (curriculumonline.ie LCEconomics_0219_EN.pdf) is 80% written + 20% research study, two-and-a-half-hour paper; the 2025 SEC marking scheme confirms Section A = 75 marks and Section B = Q11–Q16 six themed questions. Total paper marks, Section A/B choice and per-question marks are not stated in any grounded source, so those specifics were reframed out per the accreditation HARD RULE rather than guessed.',
    date: '2026-07-21',
  },
  {
    id: 'subject-economics-002',
    module: 'Mastering Economics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Here is the strategic insight: **if you score 90 in Section A and average 60 out of 75 on your four long questions, that gives you 330 out of 400 — a comfortable H1.** The path to a top grade is not about knowing everything; it is about being excellent at the high-frequency topics and disciplined on time.',
    reframedTo:
      'Here is the strategic insight: because the written paper is **80% of your grade** and the Student Research Project is the other **20%**, the top grades come from being strong on **both** components — excellent on the high-frequency Section B topics, efficient in Section A, and deliberate about the SRP rather than treating it as an afterthought. The path to a top grade is not about knowing everything; it is about depth on the topics that recur and discipline across both components.',
    reason:
      'The worked example rested on the retired 400-mark structure AND was arithmetically wrong: 330/400 = 82.5%, which is a H2, not a H1 (H1 requires 90%+). Reframed to the verified 80/20 component split with no fabricated mark total. Source: 2019 specification (80% written + 20% SRP); examiner-reports/economics/2025-insights.md gives no paper total to substitute.',
    date: '2026-07-21',
  },
  {
    id: 'subject-economics-003',
    module: 'Mastering Economics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Next, master your [[diagram library]]. You need to be able to draw, from memory, approximately 15-20 key diagrams: basic supply and demand, shifts in supply and demand, price ceiling and floor, individual firm under perfect competition (short-run and long-run), monopoly profit maximisation, kinked demand curve, cost curves (MC, AC, AVC), the circular flow of income, and the Keynesian Cross.',
    reframedTo:
      'Next, master your [[diagram library]]. You need to be able to draw, from memory, the key diagrams the paper keeps returning to: basic supply and demand and shifts in supply and demand, individual firm under perfect competition (short-run and long-run), monopoly profit maximisation, the minimum-wage / price-control labour-market diagram, the kinked-demand curve, cost curves (MC, AC, AVC), and the long-run average cost (LRAC) construction. Practise each one until you can draw it quickly with **every curve, axis, and equilibrium point fully labelled** — because the labels are separately marked.',
    reason:
      '\'Keynesian Cross\' and \'circular flow of income\' could not be grounded in the current-spec source (examiner-reports/economics/2025-insights.md), so they were dropped per HARD RULE and replaced with diagrams the 2025 scheme verifies as examined (minimum-wage labour market, monopoly, kinked-demand, LRAC construction), plus the verified point that labelling is separately marked.',
    date: '2026-07-21',
  },
  {
    id: 'subject-economics-004',
    module: 'Mastering Economics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'For Section B preparation, use **past papers aggressively**. Work through every question from the last 10 years by topic. … Begin this week by downloading the last 10 years of Economics HL papers and marking schemes. Create a [[topic frequency table]] … You will find that about 8-10 core topics cover the vast majority of questions.',
    reframedTo:
      'For Section B preparation, use **past papers aggressively** — but note the syllabus change. The current Economics specification … has been examined only from **2021 onward**, so work through the papers from **2021 to the present** by topic. … Begin this week by downloading the Economics HL papers and marking schemes **from 2021 onward** … (Older papers use a different paper structure, so building a frequency table from them would mislead your priorities.)',
    reason:
      'Only 2021–2025 papers exist under the current specification (repo holds economics-2021 through 2025). A 10-year table would be built mostly from old-syllabus papers with a different structure, misleading topic prioritisation. Scoped to 2021+ with an explicit note on the syllabus change. Source: examiner-reports/economics/2025-insights.md; 2019 specification.',
    date: '2026-07-21',
  },
  {
    id: 'subject-history-001',
    module: 'Mastering History',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The Leaving Certificate History Higher Level exam is a single paper lasting **2 hours and 50 minutes**, worth a total of **400 marks**. There is no second paper and no coursework component — everything rides on this one sitting. That makes understanding the layout absolutely critical.',
    reframedTo:
      'Leaving Certificate History Higher Level has two components. The **Research Study Report (RSR)** is a project you complete and submit *before* the exam — it is worth **100 marks (20% of your overall grade)**. The **written paper** lasts **2 hours and 50 minutes** and is worth the other **400 marks**. Together they total **500 marks**. Getting your RSR done well banks a fifth of your grade before you sit down for the written exam, so it is not something to leave until the last minute.',
    reason:
      'False: LC History HL/OL both include the pre-submitted Research Study Report worth 20% (100 of 500 marks). Grounded in examiner-reports/history/2025-insights.md (RSR 100 marks, pp.4–6) and data/knowledge/subjectTiming.ts (history totalMarks: 500).',
    date: '2026-07-21',
  },
  {
    id: 'subject-history-002',
    module: 'Mastering History',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'In essays, the key scoring unit is the [[SIP]] — a Significant Individual Point. Each SIP is a distinct historical point that is explained and, ideally, supported with evidence. A strong essay will contain **5 to 7 well-developed SIPs** in the body paragraphs. Examiners allocate marks per SIP, so more developed points means more marks.',
    reframedTo:
      'In essays, the marking scheme splits every long answer into two headings that always sum to 100% of the question: the [[Cumulative Mark]] (CM, max 60) for accurate, relevant historical content, and the [[Overall Evaluation]] (OE, max 40) for how well the whole answer addresses the question set — a fixed 60/40 ratio. The CM is built up **paragraph by paragraph**, each paragraph graded on a band, so a well-developed answer of roughly **5 to 6 strong paragraphs** reaches the CM ceiling. Writing more paragraphs than that earns nothing extra — the marks come from developing each point, not from piling on more of them.',
    reason:
      '\'SIP\' is not SEC terminology and essays are not marked by tallying marks per point. Real model is CM (cumulative, by paragraph) + OE, 60/40, per examiner-reports/history/2025-insights.md and 2024-verification.md.',
    date: '2026-07-21',
  },
  {
    id: 'subject-history-003',
    module: 'Mastering History',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Within the Document Question, the **contextualisation** sub-question (typically worth 20 marks) asks you to write a short paragraph setting the documents in their historical context.',
    reframedTo:
      'Within the Document Question, the **contextualisation** sub-question (worth **40 marks** — the largest single part of the DBQ) asks you to write a mini-essay setting the documents in their historical context.',
    reason:
      'Contextualisation is 40 marks (Max CM 24 + Max OE 16), the largest DBQ sub-question, per examiner-reports/history/2025-insights.md p.11–12; the \'20 marks\' understatement misweighted student effort.',
    date: '2026-07-21',
  },
  {
    id: 'subject-geography-001',
    module: 'Mastering Geography',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '[[Physical Geography]] (including your elective — Geoecology or the Atmosphere), [[Regional Geography]] ... and [[Human and Economic Geography]] along with an option topic.',
    reframedTo:
      'one from **[[Physical Geography]]** (core), one from **[[Regional Geography]]** (core ...), one from your **[[Elective]]** (you choose Economic Activities *or* the Human Environment), and — at Higher Level only — one from the **[[Options]]** (a specialised topic such as Global Interdependence, Geoecology, Culture and Identity, or the Atmosphere-Ocean Environment).',
    reason:
      'Conflated the LC Geography electives with the HL Options. Electives are Economic Activities vs Human Environment; Geoecology and Atmosphere-Ocean are HL-only Options, not part of Physical Geography core. Grounded in examiner-reports/geography/2025-insights.md paper structure (Sections 3 Electives Q7–12; Section 4 Options Q13–24).',
    date: '2026-07-21',
  },
  {
    id: 'subject-politics-and-society-001',
    module: 'Mastering Politics & Society',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '[[Section A]] consists of **short-answer questions** worth a total of **80 marks**.',
    reframedTo:
      '[[Section A]] is a **short-answer question** worth **50 marks**: you answer **any 10 of 15** short items at 5 marks each.',
    reason:
      'Section A is 50 marks (10 x 5, best 10 of 15), not 80. Grounded in examiner-reports/politics-society/2025-insights.md \'Section A — Question 1, 50 marks\'.',
    date: '2026-07-21',
  },
  {
    id: 'subject-religious-education-001',
    module: 'Mastering Religious Education',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '[[Section C]] is the extended essay section, worth **200 marks** — a full **half of the exam paper**. You write longer, essay-style answers on major topics from the syllabus.',
    reframedTo:
      '**[[Unit Two]]** is worth **160 marks — the largest part of the paper**. You answer **two of three sections**: Christianity (Origins and Contemporary Expressions), World Religions, and Moral Decision-Making. These are *content areas*, not a stimulus format — each section you choose is worth 80 marks from its parts.',
    reason:
      'Invented exam anatomy. The RE written paper is 320 marks built from Unit One (80) / Unit Two (160) / Unit Three (80); there is no 200-mark essay section. Grounded in examiner-reports/religious-education/2025-insights.md \'the written paper is 320 marks\'.',
    date: '2026-07-21',
  },
  {
    id: 'subject-religious-education-002',
    module: 'Mastering Religious Education',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The examiner uses [[cumulative marking]] — each relevant, well-explained point adds to your total, so more developed points means more marks.',
    reframedTo:
      'RE answers are graded [[holistically, band by band]] — not by counting points. The examiner reads your whole answer and places it in one of six bands (Excellent, Very Good, Good, Fair, Weak, Poor) against that question\'s Marking Criteria ... if a question uses a higher-order command word (Assess, Compare, Evaluate) and you only *describe* ... your answer is **capped at the Fair band**.',
    reason:
      'Opposite of how LC RE is marked. RE is holistic band-by-band with a descriptive-answer Fair cap; there is no adding-up of points. Grounded in examiner-reports/religious-education/2025-insights.md marking-system section and the implicit-reference cap (p.5, p.18).',
    date: '2026-07-21',
  },
  {
    id: 'subject-religious-education-003',
    module: 'Mastering Religious Education',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '[[Coursework Journal]] ... A reflective journal completed during the course, covering your engagement with religious education topics.',
    reframedTo:
      '[[Coursework]] — a written report on one prescribed title (chosen from the SEC list), completed during the course ... marked on research/summary-of-findings/skills/personal-reflection grids.',
    reason:
      'Mischaracterised the 20% coursework. It is a Coursework Booklet on ONE prescribed title (Section E or H) marked on Part A/Part B descriptor grids, not a reflective journal with per-topic entries. Grounded in examiner-reports/religious-education/2025-insights.md coursework section (pp.33–36).',
    date: '2026-07-21',
  },
  {
    id: 'subject-home-economics-001',
    module: 'Mastering Home Economics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The [[Food Practical Exam]] is the timed cooking test, typically held in April or early May in your school\'s home ec room. It is worth roughly **35% of your total mark**. You receive a brief with a set of dishes to prepare, and you are assessed on planning, execution, presentation, and hygiene. This is the single biggest block of marks outside the written paper.',
    reframedTo:
      'In [[Section C]] you answer **one** option: one of the three electives — Home Design and Management, Textiles Fashion and Design, or Social Studies — or the Section C core question. Note that Food Studies is NOT an elective; it is the compulsory core of the course, examined in Section B. There is **no timed food practical exam** in Leaving Certificate Home Economics — the timed cooking test you may have done in Junior Cycle does not carry over to the Leaving Cert.',
    reason:
      'There is no timed food practical exam in LC Home Economics; the 35% figure is invented. The subject is assessed by written paper (320/400, 80%) + Food Studies coursework journal (80/400, 20%). The described timed cooking exam is a Junior Cycle component. Confirmed by examiner-reports/home-economics/2025-marking-scheme.md (paper is Sections A/B/C only) and curriculumonline.ie SCSEC21 Home Economics syllabus (written 80% / practical coursework journal 20%).',
    date: '2026-07-21',
  },
  {
    id: 'subject-home-economics-002',
    module: 'Mastering Home Economics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      '{ term: \'Food Practical Exam\', description: \'A timed cooking examination, usually 2.5–3 hours, where you prepare a number of dishes under exam conditions. Marked on planning, skill, presentation, and food safety.\' }',
    reframedTo:
      '{ term: \'Section C\', description: \'The elective/core section, worth up to 80 marks. You answer one option: Home Design and Management, Textiles Fashion and Design, Social Studies, or the Section C core question.\' }',
    reason:
      'The Food Practical Exam highlight tooltip described a non-existent LC component. Replaced with the real Section C structure per examiner-reports/home-economics/2025-insights.md.',
    date: '2026-07-21',
  },
  {
    id: 'subject-home-economics-003',
    module: 'Mastering Home Economics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'You choose one of two electives: [[Elective 1 — Food Studies]] or [[Elective 2 — Social Studies]]. Most students take Elective 1. ... { term: \'Elective 1 — Food Studies\', description: \'The most popular elective, covering food science, nutrition, food technology, and cookery. Taken by the vast majority of HL students.\' }',
    reframedTo:
      'In [[Section C]] you answer **one** option: one of the three electives — Home Design and Management, Textiles Fashion and Design, or Social Studies — or the Section C core question. Note that Food Studies is NOT an elective; it is the compulsory core of the course, examined in Section B.',
    reason:
      'Food Studies is the compulsory core (Section B), not an elective. The real electives are Home Design & Management, Textiles Fashion & Design, and Social Studies, examined in Section C. Confirmed by examiner-reports/home-economics/2025-insights.md Section C options list.',
    date: '2026-07-21',
  },
  {
    id: 'subject-home-economics-004',
    module: 'Mastering Home Economics',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'For the Food Practical, there is no substitute for **cooking practice at home**. Aim to practise your core dishes at least 3–4 times each before the exam. Time yourself. Get feedback from family. Practise your planning sheet alongside the cooking — write it out as if it were the real exam. The goal is that by the day of the practical, every dish feels automatic and your time plan is second nature.',
    reframedTo:
      'For the long questions, **practise structuring your answers as distinct, developed points**. Because the marking scheme distributes a fixed number of points across named headings, take a past question, write out the separate points it deserves, and develop each one. Rehearsing the shape of a full 80-mark or 50-mark answer is as important as knowing the content, because it is how the marks are actually awarded.',
    reason:
      'Study advice for a non-existent timed food practical. Replaced with advice grounded in the real points-based marking grammar documented in examiner-reports/home-economics/2025-insights.md.',
    date: '2026-07-21',
  },
  {
    id: 'subject-construction-studies-001',
    module: 'Mastering Construction Studies',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Construction Studies is split almost perfectly down the middle: **roughly 50% for the written exam and 50% for the practical project**. ... The [[written paper]] is a **3-hour exam worth 400 marks**.',
    reframedTo:
      'Construction Studies is assessed across **three components**: the **written exam (50%)**, a **practical skills test (25%)**, and a **project (25%)**. ... The [[written paper]] is a **3-hour exam worth 300 marks (50% of your total grade)**.',
    reason:
      'The written paper is 300 marks (not 400), and the assessment is three components (written 50% / practical skills test 25% / project 25% of 600), not a 50/50 written-vs-project split. The practical skills examination — a whole component worth 25% — was omitted entirely. Confirmed by examiner-reports/construction-studies/2025-insights.md (Theory HL 300 marks; Practical Test 150; Practical Coursework 150) and WebSearch.',
    date: '2026-07-21',
  },
  {
    id: 'subject-engineering-001',
    module: 'Mastering Engineering',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The assessment is split roughly **50/50 between the written exam and the practical project**. ... The project is half your grade — it deserves your best effort.',
    reframedTo:
      'The assessment has **three components**: the **written exam (roughly 50%)**, the **practical project (roughly 25%)**, and a separate **day practical examination (roughly 25%)**. ... The project and the day practical examination together are half your grade — the workshop deserves your best effort.',
    reason:
      'LC Engineering HL has THREE components: 300-mark written paper (~50%), project (~25%), and a separate SEC Day Practical Examination (~25%), documented in examiner-reports/engineering/2025-insights.md as the \'Day 2 Practical Examination\' marked out of 100. The project alone is ~25%, not half the grade. The day practical exam was never mentioned. Confirmed by the insights file and WebSearch.',
    date: '2026-07-21',
  },
  {
    id: 'subject-art-001',
    module: 'Mastering Art',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Together the practical exam accounts for roughly **62.5%** of your total mark — that is **250 out of 400 marks**.',
    reframedTo:
      'Artefact A is worth **250 marks — 50% of your total**, so half your grade is decided in the studio, not the exam hall. This is the single biggest mark zone in the whole subject. [and] This invigilated exam runs for around **five hours** and is worth **100 marks — 20% of your total**.',
    reason:
      'Described the discontinued pre-2021 400-mark syllabus. Current spec is 500 marks (Artefact A 250/50%, Artefact B 100/20%, Visual Studies 150/30%). Source: syllabusMeta.ts lines 531-538; examiner-reports/art/2023-verification.md lines 20-23.',
    date: '2026-07-21',
  },
  {
    id: 'subject-art-002',
    module: 'Mastering Art',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'Later the same day (or on a separate scheduled sitting), you complete a [[Life Drawing]] session, typically lasting one and a half hours, working from a live model.',
    reframedTo:
      'The second practical component is the [[Invigilated Practical Examination]] — Artefact B. On a single scheduled exam day you produce a further piece of practical work, developed from the same SEC brief and stimulus as your coursework.',
    reason:
      'Life Drawing was abolished under the revised specification; there is no separate live-model session. Replaced with the current Artefact B invigilated exam. Source: syllabusMeta.ts lines 534-547 (no Life Drawing component; Artefact A/B + Visual Studies).',
    date: '2026-07-21',
  },
  {
    id: 'subject-art-003',
    module: 'Mastering Art',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The second component is the [[Art History and Appreciation]] written paper ... This paper is worth **150 marks — 37.5% of your total**. It covers Irish art, European art from the Renaissance to the present, and appreciation of art and design.',
    reframedTo:
      'The third component is the [[Visual Studies]] written paper ... This paper is worth **150 marks — 30% of your total** and runs for **two and a half hours**. It has three sections: Section A "Today\'s World", Section B "Europe and the wider world", and Section C "Ireland and its place in the wider world".',
    reason:
      'The \'Art History and Appreciation\' paper (37.5% of 400) is the old syllabus. Current paper is \'Visual Studies\', 150 marks = 30% of 500, with named Sections A/B/C. Source: syllabusMeta.ts line 536 + strands art-4/art-5/art-6; examiner-reports/art/2023-verification.md lines 20-23.',
    date: '2026-07-21',
  },
  {
    id: 'subject-art-004',
    module: 'Mastering Art',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The single biggest mark zone in Leaving Cert Art is your [[Craftwork or Imaginative Composition]] — the five-hour practical. It carries the heaviest weighting within the 250-mark practical component ...',
    reframedTo:
      'The single biggest mark zone in Leaving Cert Art is your [[Practical Coursework]] — Artefact A and its workbook, worth **250 marks (50%)**. This is half your entire grade, and it is decided over a coursework period rather than in one high-pressure sitting, which means it is also the most controllable.',
    reason:
      'Named the 5-hour exam piece as the biggest zone and never mentioned coursework — actively harmful, since coursework/Artefact A is 50% (the true largest component). Source: syllabusMeta.ts line 538 keyAdvice + strand art-1 markWeight 45.',
    date: '2026-07-21',
  },
  {
    id: 'subject-music-001',
    module: 'Mastering Music',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The [[Listening Paper]] is the written exam, sat in June, and it is worth **200 marks — 50% of your total**. It runs for approximately **two and a half hours** ...',
    reframedTo:
      'The [[Listening Paper]] is a written exam, sat in June. As a core activity it is worth **100 marks — 25% of your total** and runs for approximately **one and a half hours** ...',
    reason:
      'Marks, weighting and duration all wrong. Listening core = 100 marks (25%), ~1.5 hrs. Source: syllabusMeta.ts line 554 + line 557 keyAdvice.',
    date: '2026-07-21',
  },
  {
    id: 'subject-music-002',
    module: 'Mastering Music',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The [[Composing]] component is also worth **100 marks — 25%**. You submit a portfolio of compositions as coursework, usually including a melody composition and a harmony exercise or arrangement task as well as an original composition. The portfolio is prepared throughout the year and submitted before a set deadline.',
    reframedTo:
      'The [[Composing]] component is also worth **100 marks — 25%** as a core activity. This is a **written exam of about one and a half hours**, not submitted coursework: you answer melody-writing questions and a harmony question under timed conditions in June. (A large-scale original composition exists only for the minority of students who choose the Composing elective.)',
    reason:
      'Composing core is a timed written exam (melody + harmony), not a submitted portfolio; portfolio applies only to the minority Composing elective. Source: syllabusMeta.ts line 553 + strand music-1 line 560; examiner-reports/music/2022-insights.md lines 15-30.',
    date: '2026-07-21',
  },
  {
    id: 'subject-music-003',
    module: 'Mastering Music',
    section: 'Exam structure & assessment',
    action: 'corrected',
    original:
      'The [[Listening Paper]] is the single largest mark zone at **200 marks (50%)**. ... The [[Composing]] portfolio (100 marks) is often the most overlooked area ... your composition portfolio is coursework — you can draft, revise, get feedback, and refine before you submit.',
    reframedTo:
      'For most Higher Level students, the largest mark zone is [[Performing]]. Because the great majority take the Performing elective, Performing is typically worth **50%** ... The [[Composing]] paper (100 marks / 25% as a core activity) is a timed written exam of melody and harmony ...',
    reason:
      'Inverted the real weighting (Listening is not 50%) and misdescribed Composing as revisable coursework. With the common Performing elective, Performing is typically 50%; Composing is a timed written paper. Source: syllabusMeta.ts line 555-560 keyAdvice + strands music-0/music-1.',
    date: '2026-07-21',
  },
];
