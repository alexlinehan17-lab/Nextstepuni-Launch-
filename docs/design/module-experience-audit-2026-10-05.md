# NextStepUni modules audit

The Modules feature has a substantial, distinctive library. Its biggest opportunity is to help a student leave each visit knowing what to do next, with useful work saved and advice that matches their own examination. I would prioritise curriculum accuracy, navigation eligibility, saving and accessibility before expanding the catalogue or adding more decoration.

Reviewed on 5 October 2026 in the local Kobra sidebar worktree. This report proposes changes; it does not implement them or publish anything.

## Scope and evidence

The rendered inventory covers all 83 registered modules: 54 general modules and 29 subject guides. It includes 505 sections in full mode and 488 in Essentials mode, or 993 rendered section states. The extracted lesson text contains approximately 100,377 words in full mode and 76,275 in Essentials. These are DOM word counts, including some activity copy, rather than editorial manuscript counts.

I inspected the actual desktop and mobile preview, the shared reader, discovery screens, curated paths, progress and reward logic, response storage, notes, subject filtering, sources, and representative interactive exercises. The inventory used a 390 × 844 viewport; task walkthroughs also used a 1440 × 1000 desktop viewport. The mobile browsing preview explicitly enabled the app's mobile layout. I verified selected examination claims against current primary sources.

The inventory found no page errors or document-level horizontal overflow in the captured initial section states. That does not certify every expanded activity, popover, keyboard state or assistive technology. This is an expert review with reproducible browser and code findings. It is not a student usability study, a production analytics review, a complete scientific fact check, or an on-device iOS/VoiceOver assessment.

[The structured inventory](module-experience-inventory-2026-10-05.json) records coverage, section lengths, mode differences and task checks. The older July content audit helped identify areas to revisit, but its findings were not assumed to remain current. For example, the old Maths H6/H3 arithmetic error and the subject English paper breakdown have been corrected; support signposting now exists in the anxiety-related modules.

## What I would preserve

Keep the five worlds as a recognisable browsing system, the serif headings, the hand-drawn artwork, the paper and charcoal surfaces, and the optional activities. The current dark reader is much more coherent than the previous implementation. Definitions, sources, contents, reading comfort and notes are useful foundations.

The library already contains practical ingredients: triage drills, marking-scheme examples, if-then plans, WOOP, worked subject strategies and links to relevant tools. The app also has a strategy mastery system and programme measurement. Improvements should connect those pieces more effectively rather than introduce a second progress system or another isolated planning tool.

## Recommended priorities

Priority reflects student consequences, not just visual prominence. Effort is a relative estimate for planning, not a delivery commitment.

| Priority | Change | Student benefit | Relative effort |
| --- | --- | --- | --- |
| First | Resolve examination facts by specification, year and level | Avoids preparing for the wrong assessment | Large editorial task with existing technical foundation |
| First | Reconcile paths, subject visibility and Junior Cycle eligibility | Removes dead ends and inappropriate entry routes | Small to medium |
| First | Preserve meaningful exercise drafts and clarify notes storage | Protects work and trust | Medium |
| First | Repair keyboard controls, labels and section focus | Makes activities usable for more students | Medium across the library |
| Next | Add direct resume and routes based on a student's problem | Gets students to useful help quickly | Medium |
| Next | Give each lesson a real practice task and useful saved outcome | Connects reading to studying | Medium per pilot module |
| Next | Make completion actions specific to the lesson | Reduces the gap between intention and action | Medium |
| Next | Unify short and detailed content around the same facts | Preserves accuracy while reducing effort | Medium to large |
| Next | Simplify mobile reader chrome and activity presentation | Improves orientation and focus | Medium |
| Next | Calibrate tone, scientific claims and sensitive exercises | Makes advice credible and humane | Medium editorial task |
| Later | Add gentle follow-up, bookmarks and searchable takeaways | Helps useful ideas survive the first visit | Medium |
| Later | Validate offline recovery and performance on real devices | Supports interrupted and limited-connectivity study | Depends on measured findings |

## Students and the jobs they need to accomplish

These are design scenarios, not claims about interviewed students.

| Situation | What the student needs | What success should look like |
| --- | --- | --- |
| A tired student has ten minutes after school | A manageable next action | They practise one useful technique and can stop without losing work |
| A student cannot begin revision | A way to start with their actual subject | They create one small if-then plan and begin a real task |
| A student has an exam tomorrow | Immediate help with a specific problem | They can open triage, timing or a calm exam plan directly |
| A student reads slowly or uses assistive technology | Clear language and operable controls | They can understand and complete the same meaningful task without a speed penalty |
| A student is aiming to pass or improve one grade | Relevant examples and achievable progress | Their goal feels as legitimate as a 625-point target |
| A returning student changes devices | Their saved work and exact context | They resume the right lesson and can find their own plan |
| A Junior Cycle student follows a curated path | Content that is available and appropriate | Every suggested module opens correctly and path progress remains attainable |

## Accuracy and eligibility

### Examination guidance must use the curriculum registry

**Confirmed.** Subject guides render static content without resolving the student's specification, examination year or subject level. The app already has the canonical registry required to do this.

There are consequential examples in the current material:

- The Essentials branch of Mastering English states that Theme or Issue is not a Higher Level comparative mode. For 2027, Theme or Issue is one of the prescribed HL modes. The same module foregrounds Macbeth as its single-text example; the 2027 single-text list includes Othello, while Macbeth is on the comparative list. A worked Macbeth example can remain useful when explicitly scoped, but cannot serve as unqualified current guidance. [Official 2027 prescribed material](https://www.curriculumonline.ie/getmedia/ee4aa8b9-06c6-4091-974b-ea444dbae0af/Prescribed-Material-for-the-Leaving-Certificate-English-Examination-2027.pdf).
- The subject Business guide describes the older three-section paper and organises preparation around the ABQ. The specification introduced in September 2025 includes a Business Alive Investigative Study worth 40% and a written examination worth 60%. Those assessment components already appear in `business:2027` in the local registry, but the guide does not use them. [Official Business specification](https://www.curriculumonline.ie/getmedia/e81ccca9-fdf5-42e9-a291-52e9549820c9/SC-Business-Spec-ENG.pdf).
- The subject Biology guide describes the older single-paper assessment. The new specification includes a Biology in Practice Investigation worth 40% and a written examination worth 60%. [Official Biology specification](https://www.curriculumonline.ie/getmedia/04e86311-7225-4cf3-a723-675e33154daf/SC-BIOLOGY-Spec-ENG.pdf).
- The simplified Maths strategy says that writing a formula and substituting one value gets three marks. That should be shown as a worked example tied to a specific question and marking scheme, rather than an automatic award across questions.

**Recommendation.** Resolve assessment facts through `curriculumRegistry.ts` using canonical subject, specification, examination year and level. Keep historical worked examples, clearly labelled with their original year. When a new examination structure has not been officially established, teach supported specification content and say what remains unconfirmed; do not infer a future paper layout from an old one.

Show a short context line such as “Leaving Certificate · Higher Level · 2027” on relevant guides. Use the student's existing profile, with an accessible way to correct it. Do not ask them to choose their year on every lesson.

**Acceptance.** A 2027 Business student sees the correct assessment components. English modes match the selected year. Full, Essentials, tooltips, charts, metadata and action plans all agree. Ordinary Level students receive appropriate structures. Existing canonical IDs, historical material and Mark Bank card IDs remain intact.

Evidence: [SubjectModule.tsx](../../components/SubjectModule.tsx), [subjectContentBusiness.ts](../../subjectContentBusiness.ts), [subjectContentStem.ts](../../subjectContentStem.ts), [MasteringEnglishModule.tsx](../../components/MasteringEnglishModule.tsx) around lines 310–348, [LearningMathModule.tsx](../../components/LearningMathModule.tsx) around lines 394–411, and [curriculumRegistry.ts](../../curriculumRegistry.ts) around lines 874–981.

### Paths and module availability must agree

**Confirmed.** `LearningPathsView` iterates the raw module IDs in each path. A missing course is treated as incomplete, its raw ID can become its display title, and it can become the target of Continue.

With a Junior Cycle catalogue, Getting Started points first to the unavailable `agency-protocol`. Exam Prep Sprint includes unavailable Leaving Cert points modules. The router correctly rejects a module outside the student's catalogue, so these suggestions lead away from the path instead of delivering the promised lesson. The denominator also includes unavailable modules, preventing genuine completion.

There is a separate visibility problem for senior students. Choosing subjects removes eight general subject-strategy modules because the subject filter only maps subject names to `subject-...` guides. In the English, Mathematics and Biology profile check, this hid Mastering English, Mastering Maths and Mastering the Sciences along with the other general strategy guides. This behaviour is documented as a pre-existing quirk in `courseVisibility.ts`.

**Source risk requiring a route test.** The Junior Cycle coming-soon interception exists in `App.tsx`, but `AppRouter` defines its own selection handler that navigates directly. Its module route checks catalogue membership but not `jcStatus`. A visible coming-soon guide could therefore reach senior content through some routes. This was identified in source, not verified with a signed-in Junior Cycle account.

**Recommendation.** Create one eligibility resolver used by cards, paths, search, deep links and the router. Provide age-appropriate path variants; derive path totals and next steps from eligible modules. Distinguish an unavailable module from an unfinished one. Map general subject strategies to relevant subject families rather than requiring them to be the single guide mapped to a subject name.

**Acceptance.** Every suggested path entry opens an available lesson. Coming-soon lessons never open senior material for Junior Cycle students. No raw ID appears as a title. A student can finish every path they are offered. Subject selection retains relevant general strategies.

Evidence: [LearningPathsView.tsx](../../components/LearningPathsView.tsx) around lines 79–110, [learningPaths.ts](../../learningPaths.ts), [courseVisibility.ts](../../utils/courseVisibility.ts), [AppRouter.tsx](../../components/AppRouter.tsx) around lines 318 and 816, and [App.tsx](../../App.tsx) around line 427.

## Saving and student trust

### Meaningful work needs reliable persistence

**Confirmed in the browser.** I entered text in Your Personal Crisis Plan, moved to another section and returned. The draft was empty. The WRAP builder stores its text and selections in component state. The Thought Record also uses local component state.

Seven module components use the shared cloud response hook. This is useful, but it provides no visible save confirmation or retry state; failures are logged to the console. Some fields write on every keystroke. The hook also needs careful handling of initial loading, user changes and late responses so older data cannot replace a newly typed draft.

**Recommendation.** Classify activity data by purpose. Disposable demonstration choices can reset. Personal plans, written explanations, commitments and reflections should have a deliberate save policy. Introduce a shared response mechanism with stable module/activity IDs, draft restoration, debounced writes and visible “Saving”, “Saved” or “Could not save” states. Preserve drafts before navigation or offer a clear recovery action.

Sensitive exercises need an explicit choice about retention. Offer a private account save or a clearly explained device-only option where appropriate. Do not silently save personal worries merely because another activity saves ordinary study choices.

**Acceptance.** A student can leave mid-plan and return to their work. A failed or delayed write never looks like a successful save. Slow loading does not overwrite edits. The student can clear their response and knows where it is stored.

Evidence: [ExamCrisisManagementModule.tsx](../../components/ExamCrisisManagementModule.tsx) around lines 682–715, [CatastrophicThinkingModule.tsx](../../components/CatastrophicThinkingModule.tsx) around line 26, and [useModuleResponses.ts](../../hooks/useModuleResponses.ts).

### Notes need a clear lifetime and a useful destination

**Confirmed in source.** Reader notes are saved in localStorage and correctly say they are saved on this device. They do not sync between devices. The logout cleanup clears localStorage, which also removes these notes. That cleanup protects shared devices, but the notes dialog does not explain this lifetime or offer export.

**Recommendation.** Provide private account notes for ordinary learning material, plus a clearly labelled device-only choice where justified. Keep shared-device cleanup. Until account notes exist, explain that logging out clears local notes and offer a simple copy/export action before they are lost.

Attach notes to the section or technique where they were written. Add “Save this method” and a small searchable collection of saved takeaways. A student should not need to remember which of 83 modules contains their useful sentence.

The response rules currently restrict module response reads and writes to the account owner. Preserve that boundary. Teacher-visible completion is a separate thing from private reflections.

Evidence: [ReaderNotes.tsx](../../components/learning/ReaderNotes.tsx), [sessionPrivacy.ts](../../utils/sessionPrivacy.ts), and [firestore.rules](../../firestore.rules) around lines 179 and 262.

## Accessibility and control

### Every activity must work without a pointer

**Confirmed in the browser.** The Attribution Reframe Drill uses clickable DIV elements without button semantics or a keyboard handler. Enter did not change a card; a pointer click did. This is a functional barrier, not a visual preference.

The initial full-mode inventory found 113 form controls, of which 106 lacked an associated HTML label or `aria-label` under the inventory's limited check. This is a triage signal, not a formal count of accessibility failures: it does not resolve `aria-labelledby`, title-based names or all dynamically revealed controls. Examples in source include labels placed next to fields without `htmlFor`, and sliders without useful accessible names.

**Recommendation.** Use actual buttons for flip/reveal interactions, associated labels for fields, announced selection and feedback states, and keyboard alternatives to reordering or dragging. Give sliders a meaningful label and value explanation. Test the complete task with a keyboard and VoiceOver, including dialogs and expanded feedback.

### Section transitions should orient the student

**Confirmed in the browser.** After keyboard activation of Continue, the new section appeared and the viewport moved up, but focus stayed on the footer's Continue button. The new heading already has `tabIndex=-1`; the transition does not focus it.

**Recommendation.** Move focus to the new section heading on deliberate navigation, without stealing focus during background saves. Announce completion succinctly. Keep a predictable return focus when a dialog closes. W3C's focus-order guidance explains why sequential navigation must preserve meaning and operation. [W3C focus order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html).

### Reading preferences should cover the entire task

Reading comfort already enlarges prose, and its UI works. Some activity paragraphs, controls, chart labels and inline font sizes are independently fixed, so prose enlargement alone is not sufficient evidence that the full activity scales well.

**Recommendation.** Check all activities at 200% text enlargement and narrow layouts. Provide readable text summaries for charts and avoid essential information in tiny SVG labels. Prefer sufficiently large touch controls, generous spacing and robust focus styles. The 120% convenience control does not itself prove a WCAG failure; browser and platform scaling must also be tested. [W3C text resizing](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html).

The timed triage and dump-sheet exercises are useful optional exam practice, but I would add an untimed training mode, pause/restart where appropriate, and a clear timer choice. Timed practice should not be the only way to learn a technique.

Evidence: [AgencyArchitectureModule.tsx](../../components/AgencyArchitectureModule.tsx) around line 239, [ModuleLayout.tsx](../../components/ModuleLayout.tsx) around lines 128 and 179, [ExamHallStrategiesModule.tsx](../../components/ExamHallStrategiesModule.tsx), and [reader.css](../../components/learning/reader.css).

## Finding the right help

### Put the student's immediate problem above the catalogue

**Confirmed.** The worlds organise content by subject matter. Their next-up selection mainly follows partial progress or catalogue order. The mobile overview asks students to pick a world; its Continue label does not directly resume a module. Mobile category lists retain catalogue order, so completed modules can fill the first screen while the unfinished lesson sits further down.

**Recommendation.** Place a direct “Continue [lesson] · [section]” action at the top on both desktop and mobile. Under it, offer a few plain routes such as “I can't get started”, “I forget what I revise”, “I need to improve my answers” and “My exam is close”. Keep the worlds below for exploration.

These routes should use existing lessons and profile context. Do not insert a mandatory diagnostic questionnaire before helping. Explain recommendations with one useful reason, let the student change them, and avoid inferring a mental state from browsing behaviour.

**Proposed success measure.** In a student task test, the student can find suitable help and begin a useful activity within roughly a minute. That is a target to validate, not a measured result from this audit.

Evidence: [ModulesView.tsx](../../components/ModulesView.tsx) around lines 179–218 and 550–645, [ModuleShowcase.tsx](../../components/ModuleShowcase.tsx) around lines 195–258.

### Search should match student language

**Confirmed.** The mobile category search matches titles and descriptions within that category. The reader search matches section metadata, and future sections remain disabled. Neither offers a general search across lesson content from the Modules overview.

**Recommendation.** Add one search across eligible modules and section headings, with reviewed synonyms for student needs. “Keep forgetting” should find active recall and spacing; “can't start” should find procrastination and implementation. Show the matching section and a plain explanation. Keep a browsable list with In progress, Saved and Finished filters. These should supplement the worlds, not create another competing taxonomy.

Show an honest time range and the practical outcome before opening a lesson: reading time and activity time are different. The existing metadata does not provide estimated duration or an explicit outcome. Pilot estimates with students before presenting precise promises.

### Make opening and returning predictable

Desktop world cards and module cards can promote a preview before opening, while the mobile flow opens list items directly. Distinguish “Preview” from “Open” if both remain. A student should not have to discover that the first click changes the card instead of entering the lesson.

Twelve catalogue titles differ from their reader titles in the inventory. Most are harmless shortened labels, but Focused vs Diffuse Mode becoming The Bimodal Brain is a notable change in terminology. Keep a consistent primary name and store the metaphor as a subtitle or search alias.

Preserve the entry context when returning from a module: a curated path, search result, category filter or assigned lesson. The current back handler restores category or Modules, with a special case for Journey; it does not restore a Learning Paths origin.

## Learning design

### Distinguish finishing pages from learning a skill

**Confirmed.** Continue advances the unlocked section and can complete a module without activity participation. The reader calls those sections “read”. Rewards and weekly section goals follow that progression. Essentials versions with fewer sections report the full section count at the end so existing completion logic agrees.

Optional practice and the absence of a forced pass mark are good. The problem is what the status implies. “Finished the short lesson” is credible; “mastered this technique” needs different evidence.

The app already has strategy tiers—learned, practiced, applied and habitual—but their calculation uses completed modules and sessions where a strategy was shown. A shown prompt is evidence of exposure, not proof that the technique was used successfully.

**Recommendation.** Keep reading completion lightweight. Show it separately from a practice attempt, a student's chosen action and later use. Extend the existing strategy system rather than duplicate it. Record meaningful task events or voluntary confirmation of use, and describe their limits accurately. Completing Essentials must not imply that omitted full-version pages were read.

Avoid compulsory quizzes, minimum dwell times or extra locks as a way to manufacture engagement. Reward useful attempts and returns without turning every exercise into a points transaction.

Evidence: [ModuleLayout.tsx](../../components/ModuleLayout.tsx) around lines 136–159, [ReadingProgress.tsx](../../components/learning/ReadingProgress.tsx), [App.tsx](../../App.tsx) around lines 335–408, [useStrategyMastery.ts](../../hooks/useStrategyMastery.ts) and [useStudySession.ts](../../hooks/useStudySession.ts) around line 336.

### Unlock useful sections while offering a suggested route

**Confirmed.** Future contents entries are disabled, including the final toolkit. A student looking for a practical method must progress through preceding pages first.

**Recommendation.** Let students open any appropriate section. Offer “Start from the beginning”, “Try the exercise” and “Use this now” as clear alternatives. Preserve a recommended order for novices, with a short explanation when a prerequisite genuinely matters. Use age and curriculum eligibility for access; do not equate reading order with eligibility.

A worried student should be able to reach relevant help and support without unlocking several lessons first.

### Teach techniques through the student's own work

The Active Recall lesson explains retrieval and includes a method auditor and memory-strength illustration. Those help understanding, but they do not themselves ask the student to recall content from their actual subject. Other modules have stronger practice opportunities, so this is a recommendation for a common standard rather than a claim that the library contains no practice.

**Recommendation.** Give each lesson one observable outcome and a compact cycle: a concrete example, the student's attempt, useful feedback, and application to their next real task. Offer further explanation when needed.

For active recall, let the student choose a topic, close the explanation, retrieve three points, compare with a trustworthy answer and select what to revisit. For spacing, build a small review plan from the same topic. For procrastination, write an if-then plan and launch one manageable task.

Retrieval practice has primary experimental support for improved delayed retention compared with repeated study in the tested prose tasks. Using it in this product is a design inference; the exact NextStepUni activity still needs validation. [Roediger and Karpicke 2006](https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x).

### Make activity effort proportionate to its value

Some interactions mostly reveal an illustration or classify a prewritten statement. They can remain useful demonstrations, but should not be presented as evidence of personal skill improvement. Each activity should earn its place by helping the student understand, practise, diagnose a specific mistake or create something useful.

Use a small set of accessible interaction patterns: a worked comparison, a retrieval attempt, an answer with criteria, a saved plan, a decision scenario and an explanation in the student's own words. Keep custom simulations where their interaction explains something the simpler pattern cannot.

Feedback should explain the reasoning and next action. An incorrect choice should not produce a psychological verdict about the student. Test answer checking against reasonable alternate wording rather than exact keywords alone.

### Make subject guides teach an actual task

**Confirmed.** All 29 subject guides use a shared renderer of paragraphs, bullets and commitments. Their rendered content is identical when Essentials is toggled. They provide strategic guidance, but do not contain an embedded attempt-and-feedback activity in this renderer.

**Recommendation.** For each subject, add at least one carefully selected worked task and one student attempt tied to the correct year, level, specification and marking criteria. Show what earns credit, what an incomplete answer misses and how to improve it. Use the existing Paper Trail or Mark Bank corpus rather than copying a second question bank into Modules.

For writing subjects, compare plausible student answers and explain the difference. For calculation subjects, allow workings and partial progress. For coursework subjects, teach planning, evidence and review with the current assessment component in view. Avoid implying that keyword matching alone can grade a full essay or establish understanding.

## Moving from a lesson into study

### Replace the generic completion action with the lesson's next action

**Confirmed.** Every module's completion screen sends “Put it into practice” to the generic study session. Several modules already contain specific tool links; retain these and make their handoff richer.

**Recommendation.** Show the student's own saved takeaway or plan at completion, with one relevant action and a calm option to leave. Carry subject, topic, specification and relevant selections into the destination. Returning to the lesson should restore context.

| Lesson | Proposed action | Useful handoff |
| --- | --- | --- |
| Active recall | Practise a selected topic | Topic and a small set of suitable recall tasks |
| Spaced repetition | Schedule the first reviews | Topic, first review and editable future dates |
| Marking Scheme Decoder | Inspect and attempt a real question | Correct paper, question and scheme criteria |
| Answer Engineering | Improve one answer | Student draft and reviewed criteria |
| Reverse Engineering | Put the next week into Planner | Existing subject choices and manageable blocks |
| Procrastination or Implementation | Start the student's small task | Their if-then plan and chosen activity |
| Exam Hall Strategies | Try a relevant paper drill | Subject, paper structure and optional timing |
| Future Goals | Continue a chosen direction | Their stated interest, with permission to revise it |

Do not scatter the student into unfamiliar tools with only a generic Open button. The handoff should explain what will happen and deliver the promised starting point.

### Return later to the useful idea

**Proposed improvement.** Offer a short follow-up based on the student's saved action: “Did you try this?” or a brief retrieval prompt. Let them skip, reschedule or turn it off. Follow-up should respond to actual use and the examination context, not enforce an arbitrary daily module streak.

Save a small takeaway that a student can find before studying. Make follow-up a continuation of work they chose, rather than another notification demanding attention.

## Content depth and tone

### Essentials should share facts with the detailed version

**Confirmed.** Many general modules have separate full and simplified branches, and seven reduce the number of sections. All 29 subject guides ignore the mode. The English and Maths examples show that separate prose can also diverge in certainty and accuracy.

**Recommendation.** Store each core fact, source and outcome once, with a concise explanation and optional detail. Let students adjust reading depth within age-appropriate material. Junior students can receive a simpler default without being denied a reviewed deeper explanation. Do not expose unrevised senior material simply by enabling a switch.

Prefer literal, familiar language before introducing a metaphor or technical name. W3C's cognitive accessibility guidance recommends clear words, short sentences and manageable chunks; this is supplemental guidance, not a claim that a particular sentence fails a conformance criterion. [W3C clear content guidance](https://www.w3.org/WAI/WCAG2/supplemental/objectives/o3-clear-content/).

### Reduce competing concepts and repeated lessons

The library repeatedly covers growth, failure, self-talk, brain change, motivation and control through several metaphors. Depth can be valuable, but a newcomer does not need the entire theoretical landscape before starting effective revision.

**Recommendation.** Introduce a short recommended core, then offer extensions with a clear distinction. For example, Learning to learn could begin with retrieval, spacing and feedback; the student can open memory theory when it helps answer a question. Explain how a related module adds something new.

Preserve specialised material and stable IDs. Improve sequencing and relationships before considering merges. Where overlap is real, share the underlying explanation and refer back rather than repeat it with a new OS, engine or shield metaphor.

### Calibrate science and achievement claims

**Confirmed examples.** The active-recall strength meter uses illustrative fixed values. Some copy describes a technique as the only route to a kind of learning, predicts what a student's brain will do, or suggests that one writing technique moves an H4 essay into H1 territory. The crisis quiz infers a panic response from choices in hypothetical scenarios.

**Recommendation.** Distinguish an illustration, a group-level research result and a measurement of this student. Label illustrative charts where needed. Replace guaranteed grades and automatic brain outcomes with accurate, useful explanations of what the technique can help the student do.

Keep sources close to important claims, but audit whether the claim is stronger than the study supports. Scientific mechanisms and memorable metaphors should not become personalised diagnoses. Verify the provenance of named stories; retain genuine founder experiences, and identify composites or teaching examples if that is what they are.

Do not replace confidence with timid prose. Concrete instructions can be confident while their promised outcomes remain honest.

### Make ambition feel available to different students

**Design hypothesis to test.** Repeated H1, peak-performance and 625 framing may motivate some students while making others feel the library is not for them. The app already has personal goals; bring those into examples and suggested actions.

Include improving one grade, passing a difficult subject, keeping options open, apprenticeships and further education. Show ordinary as well as higher-level examples. Let a student choose a small goal without treating it as lesser ambition.

Acknowledging constraints matters. Recommendations should work with limited quiet space, shared devices, work, care responsibilities and changing energy. Agency can include asking for help or changing a plan. Avoid implying that all setbacks are within a student's control or that disadvantage is automatically an advantage.

## Sensitive exercises

### Keep exam support optional and humane

**Confirmed.** Support signposts now exist, which is an improvement. They appear late in the relevant modules. The Thought Record begins with an intensity of 90, models Panic, asks for negative thoughts and later treats a lower rating as proof that the reframe is working. Those responses are not a validated clinical measure.

**Recommendation.** Offer an everyday example before asking for a personal worry. Leave emotion ratings unselected until the student chooses one. Let them skip, stop or use an example throughout. Explain that feeling unchanged is possible and is not failure. Place existing support options close to the relevant exercise and make them reachable directly.

Review these exercises with an appropriate youth professional before expanding their use. Keep exam preparation distinct from a personal clinical crisis plan, especially for Junior Cycle students. Do not infer panic, resilience or mental health from a quiz score. Retention and sharing should be explicit and private by default.

Example feedback change: replace “Your brain defaulted to panic” with “This choice may cost time. Try moving to a question you can answer, then return to this one.” The feedback addresses the scenario rather than judging the student.

## Visual design and mobile reading

### Give the lesson more room and clearer orientation

**Confirmed in the phone preview.** The module title is hidden from the running breadcrumb at narrow widths, leaving a module number. Controls and the repeated description occupy substantial space before the lesson heading. Some activities introduce several coloured explanatory cards before the student reaches the input.

**Recommendation.** Keep a recognisable module title and section position visible. Use a compact toolbar with clear Text and display controls rather than relying on a palette icon. Make the full module description available on demand instead of repeating it at every section. Bring the practical outcome and activity into view sooner.

Keep comfortable line length and body size. Do not squeeze typography to fit more content. Where an activity is long, give it its own clear space and save state rather than shrinking everything into the reader card.

### Use one activity design language

The dark palette has improved, but the activities still have different border weights, radii, button treatments, status colours and small labels. The WRAP introduction's four saturated cards are a concrete example of visual information competing with the task.

**Recommendation.** Use white or charcoal for primary surfaces, consistent ink outlines, serif activity headings and restrained brand accents. Reserve semantic colour for a meaningful state. A four-step explanation can be a simple ordered sequence rather than four separately styled panels.

Retain the dimensional card effect where it suits an interactive object. Use a quieter treatment for extended reading. Motion should reveal a relationship or communicate a state, with reduced-motion support; sound should follow the student's setting and remain easy to mute during study.

This should be a shared component pass, including selected, incorrect, completed, disabled, loading and error states. A good initial-state screenshot alone does not establish visual quality for the whole activity.

### Make sources useful without interrupting every sentence

Source bubbles and definitions are useful. On narrow screens, several inline bubbles can break the reading rhythm. Some official references link to a general archive rather than the exact document.

**Recommendation.** Keep an accessible claim-to-source connection, but use a quiet, compact reference treatment and a readable sources drawer. Link directly to the relevant paper, scheme or specification where possible, including year and level. Offer a plain explanation of how the source supports the claim when useful. Do not remove citations merely to make the page cleaner.

## Recommendations for each world

| World | Current scope | Main recommendation |
| --- | --- | --- |
| Mind | 13 modules | Build one manageable action, preserve personal work and calibrate emotional language |
| Growth | 10 modules | Reduce repeated brain and failure metaphors; pair effort with strategy, feedback, rest and support |
| Learn | 15 modules | Make retrieval, spacing and feedback a practical core using the student's real subjects |
| Decode | 37 modules including 29 subject guides | Resolve cohort facts and level first, then add worked tasks with genuine marking criteria |
| Exam | 8 modules | Provide direct access to useful drills and a saved exam plan, with optional timing and compassionate feedback |

## Reliability and measurement

### Test interrupted study as a normal journey

The app has service-worker caching for web assets and deliberately uses a memory-only Firestore cache to protect shared devices. Native packaging follows a different path. I did not test production offline behaviour, so this report does not claim that offline lessons are broken.

**Recommendation.** Test opening and resuming a lesson offline on the installed app and web, changing network state mid-save, closing the app during a queued write and returning on a second device. Show which work is saved, waiting to sync or recoverable. Never substitute a broad durable cache of student records merely to make an offline indicator look successful.

Provide a readable recovery screen for a failed module load, preserving draft context. Measure low-end mobile performance before adding more animations or assets. Retain lazy loading; prefetch a likely next destination only when measurement justifies it.

### Measure useful study outcomes

The current app already tracks module starts/completions and practice activity through a structured, privacy-conscious event vocabulary. No live results were reviewed here.

**Recommendation.** Extend that foundation to distinguish opening, resuming, attempting a relevant task, saving an action and using it later. Keep route provenance so the team can compare paths, search and recommendations. Module completion alone cannot show improved learning, and sessions where a strategy was shown cannot establish mastery.

Useful product measures include time to suitable help, successful draft restoration, lesson-to-real-practice conversion, return to a saved method and performance on a relevant delayed task. Treat confidence as a self-report, not ability. Keep private answers, worry text and notes out of analytics.

## Proposed lesson experience

This is a candidate design to prototype and test, not a specification already accepted by students.

1. A student selects “I forget what I revise”. They can see why Active Recall is suggested and choose another option.
2. The lesson states one outcome: practise remembering a small part of their chosen subject without looking.
3. A brief worked example demonstrates the technique. Further explanation is available.
4. The student chooses an eligible topic and makes a low-pressure attempt.
5. Feedback compares the attempt with trustworthy criteria and identifies one next step.
6. Their chosen takeaway and response are saved with a clear status.
7. Completion offers “Practise this topic” with the topic already selected, plus an easy way to leave.
8. On a later visit, they can retrieve the idea again or open the saved method before studying.

Someone who only wants the explanation can still read it. Someone with an urgent need can open the practical section directly. The learning route should support both.

## Implementation sequence and validation

First correct cohort-dependent facts and reconcile eligibility across every entry route. In the same reliability pass, preserve useful drafts, explain notes lifetime and fix demonstrated keyboard barriers. These changes should precede a broad cosmetic rollout.

Then prototype the improved learning cycle in Active Recall, Spaced Repetition and Procrastination, plus one subject guide with a current specification. Use existing tools and stable IDs. Apply shared reader, accessibility and saving improvements across the catalogue; expand bespoke learning activities after the pilot is understood.

Run a small qualitative study with approximately 8–12 students across Junior and Senior Cycle, different reading needs, ordinary/higher levels and different goals. That sample can reveal usability problems; it cannot prove educational efficacy. Ask them to find help from a problem statement, use an activity, pause and resume, explain their takeaway and start a real study task. Include a keyboard or assistive-technology walkthrough and an interrupted-network test.

Check delayed understanding with a relevant follow-up task where feasible. Set success criteria before evaluating the prototype and avoid interpreting more clicks, longer sessions or higher completion as learning by themselves.

Future implementation checks should include:

- Year and level permutations, all path targets, coming-soon routes and direct links.
- All meaningful response fields across navigation, mode changes, slow loading and failed saves.
- Keyboard operation, focus order, labels, announcements, touch targets and enlarged text.
- Initial and interactive states in light and dark mode, including narrow devices.
- Subject-specific question and scheme verification, with the repository's required curriculum and Mark Bank preservation tests for any changes in that area.
- Private response boundaries, notes deletion/export, shared-device logout and analytics content limits.

The highest-value change is to make each visit produce a trustworthy next step that fits the student's situation. The existing library has enough material to support that; the next investment should make it easier to find, use and remember.
