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
    section: '§1 Exam Structure / §3 High-Value Zones',
    action: 'corrected',
    original:
      'Section I has two comprehension texts (Question A, worth 50 marks each — you do both) … The comprehension section (Question A on Paper 1) delivers 100 marks across two texts.',
    reframedTo:
      'Section I — Comprehending — is worth 100 marks: a Question A (50 marks, reading comprehension on one text) and a Question B (50 marks, a short functional writing task) — and you may not answer A and B on the same text.',
    reason:
      'The 2025 HL marking scheme (p.4) defines Section I as Question A (50) on one text plus Question B (50) — a functional-writing task — on a different text, with an explicit rule that A and B may not be answered on the same text. There is no "two Question As" structure.',
    date: '2026-07-18',
  },
  {
    id: 'subject-english-002',
    module: 'Mastering English',
    section: '§1 Exam Structure / §3 High-Value Zones / §4 Common Pitfalls',
    action: 'corrected',
    original:
      'Unseen Poetry (a poem you have never seen before, followed by a comparison with a second poem — 70 marks) … You get a poem you have never seen and answer a guided question on it (20 marks), then get a second poem and compare both (30 marks for the comparison, 20 marks for the second poem individually). Total: 70 marks.',
    reframedTo:
      'Poetry (70 marks) — which is not all unseen: it pairs a short Unseen Poem question (20 marks) with Prescribed Poetry on your studied poets (50 marks), and both parts are compulsory.',
    reason:
      'The 2025 HL marking scheme (p.42) defines Paper 2 Section III — Poetry (70) as A: Unseen Poem (20 marks, either Q1 10+10 or Q2 20) plus B: Prescribed Poetry (50 marks), both compulsory. The described two-poem comparison structure does not exist, and calling the whole 70-mark section "Unseen Poetry" misstates where 50 of the marks are.',
    date: '2026-07-18',
  },
  {
    id: 'subject-english-003',
    module: 'Mastering English',
    section: '§2 Marking Criteria',
    action: 'corrected',
    original:
      'This stands for Purpose, Coherence of Delivery, Language, and Mechanics … Each criterion carries roughly equal weight, and together they define the difference between an H5 and an H1.',
    reframedTo:
      'Clarity of Purpose, Coherence of Delivery, Efficiency of Language Use, and Accuracy of Mechanics … The weighting for every task is 30% Purpose, 30% Coherence, 30% Language, and 10% Mechanics — and marks for Coherence or Language can never exceed the Purpose mark.',
    reason:
      'The 2025 HL marking scheme (p.3) weights the criteria 30/30/30/10 — Mechanics is not "roughly equal" — and states the primacy-of-P rule verbatim. Criterion names corrected to the scheme’s own terms. Weightings and primacy rule confirmed identical in the 2024 HL and 2025 OL schemes.',
    date: '2026-07-18',
  },
  {
    id: 'subject-english-004',
    module: 'Mastering English',
    section: '§1 highlight / §3 High-Value Zones',
    action: 'reframed',
    original:
      'The Comparative is highly formulaic. Once you learn the structure — linking your three texts through the mode of comparison, using clear comparative language ("Similarly", "In contrast", "While Text 1...") — you can consistently score well. It rewards preparation and technique more than inspiration. / Worth 70 marks and often the highest-scoring section when done well. / Highly structured and very learnable. Students who master the comparative framework (linking all three texts in every paragraph) consistently score well.',
    reframedTo:
      'The Chief Examiner’s Report found the Comparative was the section where candidates scored least well, and warns that formulaic approaches "can hinder candidates by inhibiting their engagement with the terms of the questions". What actually scores is engaging with the question asked and the quality of evidence cited.',
    reason:
      'The 2013 Chief Examiner’s Report directly contradicts the original advice: the Comparative was the weakest-scoring section at both levels (HL 60%, OL 58%, p.7), and the report explicitly identifies "a rigid and formulaic approach" as a cause of under-achievement (pp.8, 19–20). Teaching students to learn a formula here reproduces the exact failure mode the examiner flags.',
    date: '2026-07-18',
  },
  {
    id: 'subject-english-005',
    module: 'Mastering English',
    section: '§4 Common Pitfalls',
    action: 'reframed',
    original:
      'A five-paragraph essay will not score in the top bracket. Examiners want to see sustained, developed writing — think seven to nine substantial paragraphs for a personal essay. / Top-scoring compositions are sustained pieces of writing — 1,000+ words, rich in detail and developed thought.',
    reframedTo:
      'The Chief Examiner’s words: "it is difficult to sustain a response or develop a range of ideas necessary to acquire maximum marks if the answer is brief in the extreme" — and the strongest compositions showed real command of their chosen genre.',
    reason:
      'The paragraph counts and the 1,000+ word figure are invented — no SEC source specifies them. The report supports the qualitative principle (brevity prevents development, pp.15–16; genre control discriminates, p.16), so the claim was reframed to what the source actually says.',
    date: '2026-07-18',
  },
  {
    id: 'subject-english-006',
    module: 'Mastering English',
    section: '§5 Study Techniques',
    action: 'reframed',
    original:
      'For Unseen Poetry, practise the TPCASLT method: Title, Paraphrase, Connotation, Attitude, Shifts, Literary devices, Theme. Work through one unseen poem per week using this method. Within six weeks, you will approach any poem with confidence and a clear analytical framework.',
    reframedTo:
      'For the Unseen Poem, build a consistent reading routine: what is literally happening; the tone or attitude, and where it shifts; the imagery and sound of the language; and what the poem suggests rather than states — mirroring the scheme’s instruction to reward "the patterned nature of the language of poetry, its imagery, its sensuous qualities, and its suggestiveness".',
    reason:
      'The "TPCASLT method" is not locatable in any SEC source (it appears to be a variant of a US classroom mnemonic, TPCASTT). Replaced the branded method with a routine grounded in the 2025 marking scheme’s own unseen-poetry marking stance (p.42).',
    date: '2026-07-18',
  },
  {
    id: 'subject-english-007',
    module: 'Mastering English',
    section: '§2 Marking Criteria / §4 Common Pitfalls',
    action: 'reframed',
    original:
      'the most common reason students lose marks is writing a beautiful answer to a question that was not asked … Every year, the Chief Examiner’s Report says the same thing … The number one mark-killer in English is not answering the question. / The most common reason for mid-range marks across all of English.',
    reframedTo:
      'The biggest mark-killer in English is not answering the question … The Chief Examiner’s Report ties under-achievement to "a loss of focus in terms of the requirements of the task", and notes that prepared "banks of knowledge" earn marks only when shaped to the specific question asked.',
    reason:
      'The report supports task-focus as a leading, recurring cause of lost marks (pp.11, 18, 20) but provides no ranking that would verify "the most common reason", and "every year" overstates a single report (2013 is the most recent Chief Examiner’s Report for LC English). Softened the superlatives and attributed the claim to what the report states.',
    date: '2026-07-18',
  },
];
