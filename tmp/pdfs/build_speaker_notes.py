"""Speaker notes for the Nurturing Potential workshop deck (51 slides).

One A4 page per slide: thumbnail, the point, what to say, ask/do moments.
Run after build_deck_v3.py (it uses the rendered slide PNGs).
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path('/Users/alexlinehan/Documents/Nextstepuni-Launch-')
RENDER = Path('/private/tmp/claude-501/-Users-alexlinehan/'
              '4004560a-734a-4dd1-9436-c07c76c91ddb/scratchpad/v3_render')
OUT = ROOT / 'output' / 'pdf' / 'Nurturing_Potential_Speaker_Notes.pdf'

PW, PH = A4          # 595 x 842
MX = 48
CW = PW - 2 * MX

CANVAS = HexColor('#FAFBF6')
INK = HexColor('#1A1A1A')
MUTED = HexColor('#5F5A55')
LABEL = HexColor('#8A8178')
ORANGE = HexColor('#F26B1F')
TEAL = HexColor('#2F6F6D')
LINE = HexColor('#D8D3CD')
PALE_ORANGE = HexColor('#F9D8C4')
PALE_BLUE = HexColor('#D9E7EE')

SER, SERB, SERI = 'Serif', 'SerifB', 'SerifI'
SANS, SANSB = 'Helvetica', 'Helvetica-Bold'


def register_fonts():
    base = Path('/System/Library/Fonts/Supplemental')
    for name, fn in ((SER, 'Georgia.ttf'), (SERB, 'Georgia Bold.ttf'),
                     (SERI, 'Georgia Italic.ttf')):
        pdfmetrics.registerFont(TTFont(name, str(base / fn)))


def sw(t, f, s):
    return pdfmetrics.stringWidth(t, f, s)


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        trial = (cur + ' ' + w_).strip()
        if sw(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(c, text, x, y_top, width, font=SANS, size=10.5, leading=15.5,
          color=INK):
    y = y_top - size * 0.85
    c.setFillColor(color)
    for para in text.split('\n'):
        c.setFont(font, size)
        for ln in wrap(para, font, size, width):
            c.drawString(x, y, ln)
            y -= leading
        y -= 4
    return y + 4


def kicker(c, text, x, y, color=LABEL, size=8):
    tx = c.beginText(x, y)
    tx.setFont(SANSB, size)
    tx.setFillColor(color)
    tx.setCharSpace(1.6)
    tx.textOut(text.upper())
    tx.setCharSpace(0)
    c.drawText(tx)


# =====================================================================
# (title, minutes, point, say, ask_or_do)   ask_or_do may be ''
NOTES = [
 ("Keep the door open.", "1",
  "Set warmth and stakes before any content appears.",
  "Welcome them properly — colleagues gave you an evening. Then one sentence "
  "of framing: tonight is about a single question — what decides whether a "
  "capable child in a school like ours walks through the door to a good adult "
  "life, and what we can do deliberately to hold that door open.\n"
  "Say plainly: nothing tonight is about blame. Every statistic coming is "
  "about leverage, not guilt. The people in this room are the lever.", ""),

 ("Before the data, a person.", "3",
  "Your story is the emotional foundation — the data only lands after a face.",
  "This slide stays almost empty on purpose: you are the slide. Tell your own "
  "route through the system as a DEIS student. Keep it concrete and small: "
  "what was assumed about kids like you, the specific adult who saw more, the "
  "specific thing they kept doing, what opened because of it.\n"
  "Land on a line like: I wasn't the exception because the odds were fair — "
  "I was the exception because someone held the door. Then stop. Let the "
  "silence do a job before you advance.", ""),

 ("Who changed your odds?", "3",
  "Move the room from listening to owning — everyone has a door-holder.",
  "Turn your story into their story. Almost everyone in education can name "
  "the adult who changed their odds. The three cards give the shape: who "
  "noticed, what repeated, what opened.",
  "ASK — 60 seconds of private thinking: who changed your odds? Then invite "
  "two volunteers to share the PRACTICE, not the person: what did that adult "
  "actually do? Keep shares under a minute; thank the specifics. You are "
  "harvesting a list of behaviours the whole workshop will formalise."),

 ("One in seven.", "2",
  "Deprivation is the floor some children stand on before school begins.",
  "13.8 per cent of children — enforced deprivation, meaning the household "
  "could not afford essentials, not chose to go without. In any mixed class "
  "that is three or four children before you call the roll.\n"
  "The orange card is the sharpest line: 54.2 per cent where no adult works, "
  "3.7 where two do. That contrast is about household circumstances — money, "
  "work, luck — never about love and never about the child's capacity. Say "
  "that guard-rail out loud; the room needs to hear you set it.", ""),

 ("Absence compounds quietly.", "2",
  "The attendance gap is a poverty signal, not a discipline signal.",
  "Twenty-plus days is roughly a month of school gone. In DEIS schools that "
  "is 28.3 per cent of students — more than one in four — against 18.6 "
  "elsewhere. Name what actually sits under the bars: transport, caring "
  "duties, anxiety, money for the bus, a bad week at home.\n"
  "Point at the blue card: the threshold is where REPORTING starts, not "
  "where caring starts. The pattern — Mondays, single classes, a slow drift "
  "— is visible weeks before day twenty.", ""),

 ("Picture one classroom.", "2",
  "Convert national rates into faces in one room.",
  "This is the same data with the abstraction removed. A class of 24: about "
  "five will miss a month of school this year; about two will not finish. "
  "And the categories overlap — it is often the same child carrying all of "
  "it.\n"
  "Then the quiet punch: you already know their names. That is not fatalism "
  "— it is a targeting list for care. Every practical tool tonight is aimed "
  "at those specific seats.", ""),

 ("Now make it a DEIS classroom.", "2",
  "Same promise needed — twice the weight on it.",
  "Same room, DEIS intake: seven missing a month instead of five, four not "
  "finishing instead of two. The promise a school must make is identical; "
  "the weight on the promise doubles.\n"
  "Draw the implication for staffing and systems: a DEIS school cannot run "
  "on structures designed for schools that do not carry this weight. The "
  "supports have to be engineered for the load — which is exactly what the "
  "five promises later tonight are.", ""),

 ("Same exam. Three different trajectories.", "3",
  "The system is not one system — and the difference is not talent.",
  "Read the bars left to right: 62 — 80 — 99.7. Fee-charging schools educate "
  "roughly one student in fifteen and send effectively everyone on. Then the "
  "white card: even among those who progress, destination splits by postcode "
  "— three quarters from Dublin 4 to a university, fewer than one in five "
  "from Dublin 10.",
  "ASK the room: what do the 99.7 per cent schools have that money buys — "
  "and which of those things can we replicate without money? Draw out the "
  "real answers: expectation as the default, navigation knowledge, routine, "
  "networks, an assumption of progression. That question IS this workshop — "
  "everything after tonight is replication engineering."),

 ("Background shifts the odds. It does not write the outcome.", "2",
  "Hold both truths: the dice are loaded, and they are not thrown.",
  "Seventy-four PISA points between the most and least advantaged quarters — "
  "real and heavy. But hold the second card up with equal weight: twelve per "
  "cent of disadvantaged students score in the top quarter anyway. And "
  "Ireland's gap is smaller than the OECD average, and narrowing.\n"
  "The framing sentence: background loads the dice; it does not throw them. "
  "Adults in schools are part of the throw.", ""),

 ("The route into higher education is uneven.", "2",
  "Read the bars as navigation load, not as league tables.",
  "Disadvantaged students who reach higher education get there by more "
  "varied routes — FET awards, mature entry, HEAR. The direct CAO route is "
  "one application; the alternatives demand knowledge, paperwork, timing, "
  "and an adult who knows the system.\n"
  "Two lines matter: different routes are not lesser — say it explicitly. "
  "And: every route only works for students whose school makes it visible. "
  "That lands again on slide 27.", ""),

 ("The price of a closed door.", "2",
  "Why this fight is worth having — the cost of leaving early is lifelong.",
  "Three times more likely to be unemployed at 18 to 24. Employment of 43.8 "
  "per cent against 74 for peers who finished. This is what the door costs "
  "when it closes.\n"
  "Then the red card, slowly: 6,406 students from one entry cohort did not "
  "finish — and most slipped away during senior cycle. Not before school. "
  "Not at sixteen. On our watch, in fifth year. Keeping the door open is an "
  "economic intervention, not only a kindness.", ""),

 ("Not one wall. Four quiet doors.", "2",
  "Synthesis: the barriers compound — and each one has adults beside it.",
  "Pull the last fifteen minutes into one picture. Four doors, each slightly "
  "narrower: growing up, showing up, finishing, progressing. No single wall "
  "— a corridor of doors, each taking a few more children out of the walk.\n"
  "Then the turn that earns the pivot: nobody in this room built these "
  "doors. But everyone in this room stands beside at least one of them. The "
  "rest of tonight is about how we hold them open.", ""),

 ("Data can sharpen action — or harden a stereotype.", "2",
  "Give the room permission to use the data without becoming it.",
  "Name the danger of the last ten minutes directly: statistics become "
  "expectations if we let them. The left column is what unexamined data does "
  "to a staffroom. The right column is the professional discipline — the "
  "question that asks what makes it harder, not what is wrong with them.\n"
  "This slide is the hinge of tone: from here on, curiosity replaces "
  "diagnosis. If a colleague bristled during the stats, this is where they "
  "come back on board.", ""),

 ("Progress is real. The remaining gap is real.", "2",
  "Proof the system moves — effort is not naive.",
  "Decode the wedge for them: the shape IS the gap. On the left, 2001 — "
  "seventeen points of retention gap between DEIS and non-DEIS. On the "
  "right, today — 7.7. The gap has more than halved in seventeen years.\n"
  "That did not happen by weather. It happened because schools did "
  "deliberate, boring, repeated things. The wedge is the argument that "
  "effort works; the 7.7 that remains is the argument for tonight.", ""),

 ("In the door is not up the stairs.", "2",
  "The caveat: access won is not success won — the gap moves upstream.",
  "Guard against the comfortable conclusion that retention solved it. "
  "Twenty-three per cent of disadvantaged entrants do not get past first "
  "year in college — nearly double the affluent rate. High-points courses "
  "skew heavily affluent. Postgraduate study, 14 against 24.\n"
  "The message: our job does not end at the CAO form. Points, course "
  "choice, and preparation for independent study are part of keeping the "
  "door open — the door has a staircase behind it.", ""),

 ("The adult is the variable.", "2",
  "The thesis of the entire workshop — read the finding slowly.",
  "Read the quoted finding almost verbatim, slowly: students who grew up "
  "economically vulnerable needed positive teacher relationships in early "
  "secondary school to reach the same attainment as better-off peers — even "
  "when their parents held high expectations.\n"
  "Then the black pill: the relationship is not the soft part of the job — "
  "it is the mechanism. Frame it as power, not pressure: you are not "
  "bystanders to the statistics from the first half. You are the variable "
  "in them.", ""),

 ("Five promises that change the odds.", "1",
  "The organising frame for everything practical — five hooks.",
  "Keep it crisp: not five programmes, not five budgets — five experiences "
  "a student can COUNT on. Known. Taught. Present. Partnered. Future-ready. "
  "Everything for the rest of the evening hangs on these five hooks, in "
  "order.\n"
  "Tell them to test every idea tonight against one question: does this "
  "make one of the five more dependable for the kids from slide six?", ""),

 ("Relationships are learning infrastructure.", "2",
  "Being known is a system, not a personality trait.",
  "Belonging is not the fluffy bit — it is infrastructure, like the "
  "timetable. Four verbs make it a system: Name — every student can name an "
  "adult who would notice. Notice — absence, withdrawal and change trigger "
  "contact, not paperwork. Repair — conflict has a dignified route back; "
  "that route is what keeps a wobbling student in the building. Record — "
  "files start with strengths, because the file follows the child.",
  "ASK, rhetorically: could every student in our school name their adult? "
  "If we are not sure, that is the first 90-day project."),

 ("Care without lowering the ceiling.", "2",
  "Trauma-aware practice that keeps expectations intact.",
  "Decode the picture: the black line is the ceiling — expectations — and "
  "it does not drop. The five green pillars HOLD it up: predictability, "
  "choice within boundaries, regulate before reasoning, a dignified return, "
  "referral through the proper system.\n"
  "The red strip is professional discipline: no ACE scores, no amateur "
  "diagnosis, no demanded disclosure, no dropped accountability, no playing "
  "specialist. Close with the line that reconciles both halves: care that "
  "lowers expectations is abandonment with a kind face.", ""),

 ("High expectations need high support.", "2",
  "Locate your school's default under pressure — then design out of it.",
  "Walk the quadrant: sink-or-swim keeps the demand but hides the route; "
  "the kind ceiling keeps the warmth but shrinks the challenge — and it is "
  "where good schools drift under pressure, because it feels like care. "
  "Ambitious access keeps the demand AND builds the ramp.",
  "ASK: where does our school drift when a student is struggling — be "
  "honest? Most rooms answer 'kind ceiling'. That admission, said aloud, is "
  "worth twenty minutes of policy."),

 ("Teach the route, not only the destination.", "2",
  "Metacognition works inside subjects — the free move is thinking aloud.",
  "Six steps, nothing exotic: activate, model, guide, check, respond, "
  "transfer. The step schools skip is MODEL — students almost never see an "
  "expert actually thinking: choosing an approach, hitting confusion, "
  "resolving it.\n"
  "The move that costs nothing and transfers most: think aloud while you "
  "work a problem. Show them expert confusion and its repair — that is the "
  "route made visible.", ""),

 ("Studying is not the same as learning.", "2",
  "The familiarity trap — recognition masquerades as knowledge.",
  "The pink card is what most struggling students call study: read again, "
  "copy again, watch again. It produces familiarity — 'I recognise it' — "
  "which FEELS like knowing and is not.\n"
  "The orange card is the test any student can run alone tonight: close the "
  "page, produce. The green loop is what production makes possible: "
  "retrieve, check, repair, return. Blunt version for the staffroom: if "
  "your revision advice does not involve producing, it is entertainment.", ""),

 ("A study session needs an ending, not just a timer.", "1",
  "Structure beats duration — give sessions a shape.",
  "Quick slide: forty-five minutes with a shape — target, retrieve, check, "
  "repair, schedule. The times can flex; the sequence cannot. Five minutes "
  "choosing a target beats forty minutes of drift.\n"
  "This is the shape the app's study sessions enforce later — plant that "
  "seed now.", ""),

 ("Do not make success depend on a quiet bedroom.", "2",
  "The equity test for every method and every homework.",
  "Read the test on the white card: could the student run this without "
  "private tuition, their own device, or an expert adult at home? If not, "
  "the gap is access — and access is part of pedagogy, not an excuse.\n"
  "The five rows are what school can make dependable: a supervised slot, "
  "devices and schemes, a modelled routine, a low-noise place, rapid "
  "feedback. Closing line: homework that requires a quiet bedroom grades "
  "the bedroom, not the child.", ""),

 ("20 days is a reporting threshold. Support starts sooner.", "2",
  "Attendance is a care loop, not a compliance loop.",
  "Five verbs: notice the pattern early — Mondays, single subjects, the "
  "slow fade. Ask before interpreting. Map the barrier with student and "
  "family. Act small and specific — a bus arrangement, a morning check-in. "
  "Review: did ACCESS improve, not just the number.\n"
  "Practical detail that changes conversations: use days, not percentages. "
  "'Eighteen days' lands with a parent; 'ten per cent' does not.", ""),

 ("Partnership is designed before it is declared.", "2",
  "Families reach back when contact is designed to be reachable.",
  "Five habits: specific, curious, strength-first, accessible, reliable. "
  "Then read Sam's script on the right ALOUD — it demonstrates all five in "
  "four sentences: precise days, a named strength, a curious list of "
  "possible barriers, and one small agreed step with a check-in date.",
  "ASK: what proportion of our first contacts home carry a strength? If "
  "every call is a withdrawal, the account is empty when you need it."),

 ("A pathway is only real when a student can navigate it.", "2",
  "Aspiration without navigation is a wish.",
  "One aspiration, three routes: CAO, further education and tertiary, "
  "apprenticeship and work-plus-training. All legitimate; say so plainly.\n"
  "The black pill is the audit: every route needs entry requirements, "
  "deadlines, cost and funding, a named adult, a next action. A fifth-year "
  "who learns about HEAR and SUSI in time writes a different CAO list. "
  "Navigation is teachable — so timetable it.", ""),

 ("Leah is capable. School is becoming harder to reach.", "4",
  "Case lab — practise the promises on a composite student.",
  "Read Leah's card aloud once, warmly. She is fictional but assembled from "
  "the national data the room has just seen: strong orally, inconsistent on "
  "paper, sixteen days gone by February, caring duties, and a quiet 'courses "
  "like that are for people with money'.",
  "DO — groups of three or four, three minutes, the four questions on the "
  "right. WATCH for diagnosis creep ('she probably has…') and steer to "
  "observables and next steps. Push every group to finish the sentence: "
  "what changes for Leah on Monday?"),

 ("Coordinate the supports around the student.", "3",
  "One plausible response — the five promises as five handles.",
  "Walk the five cards as ONE sequenced plan with owners and a review date "
  "— not five separate worries. Known: a named check-in. Taught: model the "
  "written answers her oral ability proves she can reach. Present: map the "
  "morning barrier. Partnered: strength-first call home. Future-ready: the "
  "physio route with funding attached.",
  "ASK groups to compare against their own plans — what did they have that "
  "this misses? The meta-point to land: five promises give five handles, "
  "where one meeting of general worry gives none."),

 ("Six strategies that survive contact with an exam.", "2",
  "The evidence-based toolkit — none require talent, all require design.",
  "Frame the section: everything on this slide survives contact with a real "
  "exam because each one produces evidence, not familiarity. None require "
  "talent; all require design — which means every one is teachable in an "
  "ordinary classroom, tomorrow, without budget.\n"
  "Tell the room the next six slides are one minute each: what it is, and "
  "how a student actually runs it. (Short on time? Deep-dive retrieval and "
  "examiner-marking; name the rest.)", ""),

 ("Ask yourself before the notes open.", "1.5",
  "Retrieval practice — the single biggest upgrade to how students study.",
  "The flow on the left is the whole discipline: ask first, answer from "
  "memory — the notes stay closed — and only then check, keeping or "
  "repairing by name. The right card is the student routine: three "
  "questions after class, answered closed-book the next day.\n"
  "The counterintuitive bit to say out loud: retrieval feels WORSE than "
  "rereading. The difficulty is the signal it is working — students who "
  "are not warned will retreat to comfortable rereading.", ""),

 ("Four short visits beat one long night.", "1",
  "Spacing — same minutes, radically different memory.",
  "Point at the timeline: today, two days, a week, a month — ten minutes "
  "each. Then the crossed-out cram: same total minutes, weaker memory. "
  "The forgetting curve is not a moral failing; it is physics — schedule "
  "around it.\n"
  "Bridge to practice: the app's Spaced Repetition Timetable books the "
  "returns automatically, so the discipline survives a busy week.", ""),

 ("Mix the questions — choosing is the skill.", "1",
  "Interleaving — because the exam never announces the topic.",
  "Two tile rows: blocked practice feels smooth and fades; interleaved "
  "feels harder and sticks. The line under them is the mechanism: every "
  "switch forces the question — which method fits here? That decision IS "
  "the exam skill.\n"
  "If practice never makes a student choose, the exam is the first time "
  "they ever choose.", ""),

 ("Study the route before walking it alone.", "1",
  "Worked examples — scaffold, then fade it deliberately.",
  "Read the three rows as a fade: full example, every step shown; gap-fill, "
  "the student supplies the middle; solo, all theirs, then checked against "
  "the scheme. Novices learn routes from maps, not from being lost.\n"
  "And the pill: confusion at step two is information, not failure — it "
  "tells you exactly where the scaffold goes back in.", ""),

 ("Answer the verb, not the topic.", "1",
  "Command words — marks are awarded to the verb.",
  "Four verbs, four different answers: define wants the exact meaning, "
  "explain wants the how and why, contrast wants differences that matter, "
  "evaluate wants a judgement backed by evidence. A student who knows the "
  "topic but answers the wrong verb scores like a student who knows "
  "nothing.\n"
  "The routine: circle the command word before writing a single sentence.", ""),

 ("Find the marks. Name what is missing.", "1.5",
  "Marking like an examiner — converts hoping into knowing.",
  "Walk the two cards: a real answer marked against the real scheme, point "
  "by point — two ticks, one miss, two out of three. The repair is one "
  "written line: what earns the missing mark next time.\n"
  "This is the single habit that separates students who improve from "
  "students who just practise. And it is exactly what Mark Bank automates — "
  "which is the bridge to the next section.", ""),

 ("The app should strengthen a human support system.", "2",
  "Position the app honestly: it makes the promises dependable — humans stay central.",
  "Say the title sentence and mean it: nothing in the app replaces a "
  "teacher; it makes the five promises dependable in a student's pocket at "
  "9pm when no adult is available. Map the rows: each promise has a "
  "surface.\n"
  "Note the honesty of what they are seeing: live captures from the demo "
  "account, taken this week — not mock-ups.", ""),

 ("Teach the method before asking for independence.", "1.5",
  "The Modules are the taught curriculum of learning itself.",
  "Fifty-three modules across five worlds — active recall, spacing, the "
  "exam-craft from the strategy section — each one taught, not assumed. "
  "The right rows are the adult's sequence: explain, model, choose, fade.\n"
  "The caution on the pill: completion starts transfer; it does not prove "
  "it. The classroom conversation stays essential.", ""),

 ("Produce first. Then the real scheme decides.", "2",
  "Mark Bank in two screens — retrieval plus examiner-marking, frictionless.",
  "Two screens, one discipline: attempt a real 2025 Leaving Cert question "
  "from memory; then the real SEC scheme appears and the student marks "
  "point by point — missed it, shaky, got it — and the shaky ones schedule "
  "their own return.\n"
  "Connect it back: this is strategies one and six from the toolkit, made "
  "frictionless. 552 real questions, real schemes.", ""),

 ("One place to understand, practise, plan and track.", "1",
  "The Launchpad — assign a tool for a need, not 'use the app'.",
  "One screen, filtered by purpose: understand, practise, plan, track. The "
  "adult move is on the pill: choose FOR the need — a student drowning in "
  "material gets the spaced timetable, not a tour of nineteen tools.\n"
  "Specific beats general: 'open War Room tonight' lands; 'use the app "
  "more' does not.", ""),

 ("The next step stays visible without shrinking ambition.", "1",
  "Learning Paths — sequence the support, never hide the summit.",
  "Four routes — foundation, exam, mindset, learning — each a sequence "
  "where the next step is always visible. For an overwhelmed student the "
  "path answers the only question that matters tonight: what do I do "
  "NEXT?\n"
  "Design principle worth quoting: sequence support; never hide the "
  "prerequisites.", ""),

 ("A dashboard should start a conversation — not a verdict.", "1.5",
  "Progress data as conversation fuel — the four questions.",
  "The Five Climbs view: each programme a mountain, progress as ascent. "
  "Then the four questions on the right — what changed, what helped, where "
  "is it stuck, what happens next. That is a two-minute check-in script "
  "any tutor can run.\n"
  "And the pill is the ethic: patterns guide support; they do not predict "
  "worth.", ""),

 ("Let progress become a place the student can shape.", "1",
  "My Journey — belonging and authorship without league tables.",
  "Effort becomes an island the student shapes: earned points, real "
  "choices, no public ranking — deliberately. For students who have never "
  "owned an academic identity, watching one accumulate is quietly "
  "powerful.\n"
  "The rule on the footer matters: never compare islands or spending "
  "publicly.", ""),

 ("A tool in the routine — never a referee of worth.", "1.5",
  "The adult's three moves — and the closing ethic of the app section.",
  "Three verbs close the section: choose for need — one surface for this "
  "week's barrier; agree the output — a session, an attempt, a plan; "
  "review the next move — look at the pattern together, agree one action "
  "with one owner.\n"
  "Repeat the pill slowly — patterns guide support, they do not predict "
  "worth — and move on. The app section should end feeling like ethics, "
  "not sales.", ""),

 ("How dependable are the five promises?", "4",
  "Self-assessment — rate the SYSTEM, never the people.",
  "Bring it home. Five promises, four-point scale: rarely to dependable. "
  "The honest question is not 'do we care?' — everyone cares. It is: how "
  "DEPENDABLE is each promise for the students from slide six?",
  "DO — two minutes solo scoring, then compare with a neighbour. Then the "
  "harder question: where would our STUDENTS score us lower — and our "
  "families? A low score is a planning signal, not a verdict; no naming of "
  "staff or students."),

 ("One 90-day test beats a 30-page aspiration.", "3",
  "Turn the lowest score into one small, reviewable experiment.",
  "Take the weakest promise from the rating and shrink it: which student "
  "experience becomes more dependable, for whom exactly, what adults do "
  "differently and how often, who owns it, what early signal should move, "
  "and the review date — booked before you leave tonight.\n"
  "The standard: small enough to implement, important enough to matter, "
  "specific enough to learn from. And measure support and access — never "
  "a student's private history.", ""),

 ("Five moves by Friday.", "2",
  "Momentum — one move each before the weekend.",
  "Read the five fast: name the students at the edge and their adult; one "
  "strength-first family contact; audit one task for hidden assumptions; "
  "map A-B-C routes with one student; book the 90-day review.",
  "ASK each person to pick exactly ONE, now, and write it down. Not five — "
  "one. Momentum is a design choice; Friday is the deadline because "
  "intention decays over a weekend."),

 ("Stop. Start. Protect.", "3",
  "Private commitment — the quiet minute of the night.",
  "Drop your voice with the dark slide. Three prompts: one routine or "
  "phrase that quietly closes a door — stop it. One action to test for 90 "
  "days — start it. One strength this school already has — protect it, "
  "name it, resource it.",
  "DO — two minutes of private writing, phones away. Then invite two or "
  "three to share an ACTION, never a confession. If the room stays silent, "
  "let it — silence here is working."),

 ("Be the school that keeps the door open.", "2",
  "Close the loop — end on the student, not the programme.",
  "Return to your opening story in one or two sentences — the adult who "
  "held YOUR door. Then the two lines on the slide, slowly: not every "
  "barrier begins in school — but school decides whether a barrier becomes "
  "a ceiling.\n"
  "Final sentence, then stop talking: be the school that keeps the door "
  "open. Do not add a slide of thanks after it; end on the student.", ""),

 ("Sources — national statistics and policy.", "—",
  "Leave visible during questions.",
  "Leave this on screen for Q&A. Every number tonight traces to a public "
  "source — CSO, Tusla, Department of Education, OECD, HEA, ESRI. If "
  "someone challenges a figure, welcome it: the culture being modelled is "
  "that claims about children deserve verification.", ""),

 ("Sources — teaching, attendance, trauma, pathways.", "—",
  "The practice evidence base.",
  "Second half of the evidence base: NEPS, EEF, IES, the trauma reviews, "
  "the pathways bodies. Offer the workbook and these two pages as the "
  "take-home reference; the deck travels with the sources attached.", ""),
]

# =====================================================================
# Per-slide stat decode: slide index -> [(figure, explanation), ...]
NUM = {
 4: [("13.8%", "Children under 16 in child-specific enforced deprivation, 2024 — the "
      "household could not AFFORD at least 3 of 17 child essentials (a warm coat, a "
      "hobby, a school trip, a friend over). 'Enforced' is the key word: could not, "
      "not chose not to. Source: CSO SILC Module on Child Deprivation 2024. "
      "One in seven is the honest rounding of 13.8%."),
     ("54.2% vs 3.7%", "Same measure, split by household work status: deprivation hits "
      "54.2% of children where no adult in the home is in work, versus 3.7% where two "
      "adults work — roughly a fifteen-fold difference. Same CSO release. If asked "
      "'what drives it?': work intensity, not family structure or effort.")],
 5: [("18.6% / 28.3%", "Share of post-primary students absent 20 OR MORE days in "
      "2023/24 — non-DEIS vs DEIS. Source: Tusla, Analysis of School Attendance Data "
      "2023/24. Coverage caveat if challenged: 541 of 722 post-primary schools "
      "returned data; it is the national dataset that exists."),
     ("9.7pp", "The gap between those two rates in percentage points — say 'points', "
      "not 'per cent', or someone will correct you. It means: for every hundred "
      "students, ten more DEIS students cross the 20-day line."),
     ("20+ days", "Twenty school days is roughly FOUR school weeks — a month of "
      "teaching, relationships and momentum. It is also the statutory threshold at "
      "which schools must report to Tusla — which is why the slide argues support "
      "must start before the number does.")],
 6: [("≈5 of 24", "24 students × ~21% national post-primary 20+day absence rate ≈ 5. "
      "The 21% is the enrolment-weighted blend of DEIS (28.3%) and non-DEIS (18.6%) "
      "rates — roughly one post-primary student in four or five nationally."),
     ("≈2 of 24", "24 × 10% ≈ 2.4: the flip side of the 90% national retention rate "
      "(2018 entry cohort, DoE July 2026 report). Two of every 24 who started first "
      "year together are not there for the Leaving Cert."),
     ("≈3 of 24", "24 × 13.8% deprivation ≈ 3.3 children."),
     ("Caveat", "Say it as the footnote does: illustrative arithmetic — national "
      "rates applied to one class of 24, and the categories OVERLAP; the child in "
      "deprivation is disproportionately also the child missing the days.")],
 7: [("≈7 of 24", "24 × 28.3% (the DEIS 20+day rate) ≈ 6.8. Two more empty-chair "
      "children than the national classroom on the previous slide."),
     ("≈4 of 24", "24 × 15.9% ≈ 3.8 — from DEIS retention of 84.1% (2018 entry "
      "cohort). Double the national classroom's non-finishers."),
     ("The point of the pair", "Nothing about the children changed between the two "
      "slides — only the concentration of pressure. That is the argument for "
      "DEIS-weighted staffing, systems and energy.")],
 8: [("62%", "Share of DEIS-school Leaving Cert students progressing to third level "
      "— Irish Times feeder-schools analysis of the 2021 CAO cycle."),
     ("80%", "Same measure, non-fee-charging schools overall — effectively the "
      "national average."),
     ("99.7%", "Fee-charging schools: essentially every student progresses. They "
      "educate roughly 1 in 15 second-level students (6–7% of enrolment, DoE)."),
     ("≈1 in 4", "About a quarter of post-primary students attend DEIS schools "
      "(OECD resourcing review). So the 62% bar is a quarter of the country's "
      "children."),
     ("75.6% vs 17.6%", "Of students who DID progress, the share going to a "
      "traditional university: Dublin 4 vs Dublin 10 — 2025 feeder data. The door "
      "opens into different corridors by postcode."),
     ("If challenged", "Feeder data counts CAO entrants against Leaving Cert "
      "candidates, so a school can exceed 100% (repeat students, deferred entry); "
      "years differ across the two analyses. Direction and scale are robust; "
      "decimals are not the point.")],
 9: [("74 points", "PISA 2022 maths gap between Ireland's most and least "
      "socio-economically advantaged quarters (ESCS index). Rule of thumb: ~20 "
      "points ≈ a year of learning, so 74 points ≈ three-plus years between the "
      "quarters at age 15."),
     ("93 points", "The OECD-average version of the same gap — Ireland's is "
      "meaningfully smaller, and it NARROWED between 2012 and 2022 while the OECD "
      "average stood still. Genuine good news; use it."),
     ("12%", "Share of disadvantaged Irish students who are 'academically "
      "resilient' — bottom quarter of advantage, top quarter of maths performance. "
      "One in eight beats the odds already, with no system designed around them."),
     ("If challenged", "OECD flags Ireland's response-rate caveat for PISA 2022; "
      "the country note carries the numbers as published.")],
 10: [("61% vs 78%", "Route into higher education via second-level exams (the "
       "direct CAO route): disadvantaged vs affluent undergraduate new entrants, "
       "HEA socio-economic profiles 2021/22–2023/24."),
      ("9% vs 4%", "Entry via a further-education (FET/QQI) award — twice as "
       "common for disadvantaged entrants."),
      ("19% vs 4%", "Entry as mature students or through HEAR combined — nearly "
       "five times more common for disadvantaged entrants."),
      ("How to read it", "Not a deficit chart: it says disadvantaged students who "
       "get there navigate LONGER, more paperwork-heavy routes. Each alternative "
       "route needs an adult who knows it exists. Percentages are within-group "
       "shares and do not sum to 100 (other routes exist).")],
 11: [("3×", "Early school leavers aged 18–24 are roughly three times more likely "
       "to be unemployed than peers who finished — CSO analyses of early leavers."),
      ("43.8% vs 74%", "In-employment rates for the same comparison (CSO, 2019 "
       "release). A thirty-point employment gap that persists through the "
       "twenties."),
      ("6,406", "Students from the 2018 entry cohort who did not complete the "
       "Leaving Cert (DoE retention report, July 2026). Most left during senior "
       "cycle — between fifth and sixth year, on the school's watch."),
      ("Framing", "This is the cost side of the ledger: everything later in the "
       "deck is cheaper than this.")],
 12: [("The four doors", "All four figures already shown, gathered: 13.8% growing "
       "up in deprivation (CSO 2024) · +9.7pp DEIS absence gap (Tusla 2023/24) · "
       "−7.7pp DEIS retention gap (DoE, 2018 cohort) · 61% vs 78% direct-route "
       "entry to HE (HEA). Four separate measures, four separate sources, one "
       "direction of travel — that is what makes it a corridor, not a "
       "coincidence.")],
 14: [("≈17pp → 7.7pp", "The DEIS/non-DEIS Leaving Cert retention gap: about 17 "
       "points for the 2001 entry cohort, 7.7 points for 2018 (latest published, "
       "July 2026). The wedge drawing is literally this gap, to scale — it has "
       "MORE than halved in seventeen years."),
      ("84.1% / 91.8%", "The two retention rates behind today's 7.7pp: DEIS vs "
       "non-DEIS students staying from entry to the Leaving Cert, 2018 cohort."),
      ("PISA echo", "Ireland's socio-economic maths gap also narrowed 2012–2022 "
       "(OECD). Two independent datasets, same direction: deliberate school-level "
       "work moves these numbers.")],
 15: [("23% vs 12%", "First-year non-progression in higher education: "
       "disadvantaged vs affluent entrants (HEA, Exploring Student Progression, "
       "2024). Nearly one in four disadvantaged entrants does not make second "
       "year — almost double the affluent rate."),
      ("High-points courses", "HEA socio-economic profiling: medicine, "
       "engineering and finance-type courses are dominated by entrants from "
       "affluent backgrounds. Qualitative but consistent across releases."),
      ("14% vs 24%", "Progression to postgraduate study, disadvantaged vs "
       "affluent graduates; and graduate unemployment runs 9% vs 6% (HEA Graduate "
       "Outcomes and Socio-Economic Status, 2023)."),
      ("The chain", "Deprivation → attendance → retention → entry → completion → "
       "outcomes: the same gradient at every link. Access is one link, not the "
       "chain.")],
 16: [("The study", "Growing Up in Ireland '98 cohort — ~8,500 young people "
       "followed from age 9 to 20; analysis by Dempsey & McCoy (ESRI), published "
       "2025 in the British Journal of Educational Psychology."),
      ("The finding", "For economically vulnerable students, positive "
       "teacher–student relationships in EARLY secondary school predicted "
       "reaching the same attainment (a degree by 20) as better-off peers — and "
       "parental expectations alone, without that relationship, were not enough. "
       "That is why 'the adult is the variable' is a finding, not a slogan.")],
 25: [("20 days", "The statutory threshold: schools must report students absent "
       "20+ days to Tusla's education welfare services. The slide's argument: "
       "day 20 is an administrative fact — day 6 is a pattern; act on patterns."),
      ("Days, not %", "'Eighteen days' is a month a parent can picture; '10%' is "
       "an abstraction. Always translate.")],
 30: [("Evidence base", "All six strategies trace to the IES/What Works "
       "Clearinghouse practice guide (Organizing Instruction and Study) and EEF "
       "guidance on metacognition — the two most-cited practice syntheses in the "
       "field. Nothing on this slide is proprietary; the app just packages it.")],
 39: [("552", "Real Leaving Certificate questions from the 2021–2025 papers in "
       "Mark Bank, each carrying its actual SEC marking scheme. If asked about "
       "rights: marking points are quoted with attribution to the State "
       "Examinations Commission.")],
 45: [("The scale", "1 = rarely true for our students · 4 = dependable for "
       "every student. The unit being rated is the SYSTEM'S promise, never a "
       "person's effort — say that before anyone scores.")],
 46: [("90 days", "Long enough for a routine to bite, short enough to stay "
       "honest. The review date is the design feature: a plan with no learning "
       "date is an aspiration."),
      ("Early signal", "Pick something that should move in WEEKS (contact rate, "
       "study-slot attendance, one student's mornings) — not exam results, which "
       "arrive too late to steer.")],
}

SECTIONS = [
    (1, 3, 'Open — a person before the data', '7'),
    (4, 13, 'Act I — the wall (Irish context)', '21'),
    (14, 16, 'Act II — the turn', '6'),
    (17, 27, 'Act III — five promises', '20'),
    (28, 29, 'Case lab — Leah', '7'),
    (30, 36, 'The strategy toolkit', '8'),
    (37, 44, 'The app — promises made dependable', '11'),
    (45, 48, 'Whole school — plan and commit', '12'),
    (49, 51, 'Close', '2'),
]

OVERARCH = (
    "The single message: the gap between what disadvantaged students could do "
    "and what they currently get to do is not made of talent — it is made of "
    "ordinary, repairable moments. Being known by name. Being taught how, not "
    "just what. Being noticed at day six, not day twenty. Having a family that "
    "can reach a person, not a portal. Seeing a navigable route to a future. "
    "Schools cannot abolish poverty — but a school that makes those five "
    "experiences DEPENDABLE changes the odds a child carries for life. The "
    "deck walks the room from honest grief about the gaps, through proof the "
    "system moves, to five promises, a toolkit, and one 90-day commitment. "
    "Your job as speaker: keep it about leverage, never blame; keep it about "
    "the system, never individual heroics; and end every section on what "
    "changes Monday."
)


def cover(c):
    c.setFillColor(CANVAS)
    c.rect(0, 0, PW, PH, stroke=0, fill=1)
    kicker(c, 'Nurturing Potential · Facilitator document', MX, PH - 70,
           color=ORANGE, size=9)
    c.setFont(SER, 30)
    c.setFillColor(INK)
    c.drawString(MX, PH - 112, 'Speaker notes.')
    c.setFont(SANS, 11)
    c.setFillColor(MUTED)
    c.drawString(MX, PH - 134, '51 slides · ~90 minutes with activities · '
                               'flexible 60–120')
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2.5)
    c.line(MX, PH - 152, MX + 150, PH - 152)
    kicker(c, 'The overarching message', MX, PH - 182, color=TEAL)
    y = block(c, OVERARCH, MX, PH - 196, CW, font=SER, size=11, leading=17,
              color=INK)
    kicker(c, 'Running order and timing', MX, y - 24, color=TEAL)
    yy = y - 44
    for a, b, name, mins in SECTIONS:
        c.setFont(SANSB, 9.5)
        c.setFillColor(ORANGE)
        c.drawString(MX, yy, f'{a:02d}–{b:02d}')
        c.setFont(SANS, 10.5)
        c.setFillColor(INK)
        c.drawString(MX + 56, yy, name)
        c.setFont(SANSB, 10)
        c.setFillColor(MUTED)
        c.drawRightString(MX + CW, yy, f'≈{mins} min')
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(MX, yy - 7, MX + CW, yy - 7)
        yy -= 24
    block(c, 'Flexing the runtime: for 60 minutes, compress the strategy '
             'toolkit to slides 30, 31 and 36 and shorten both activities to '
             'three minutes. For 120, give Leah ten minutes and add a second '
             'round of sharing after Stop–Start–Protect.\n'
             'The notes format on each page: THE POINT is why the slide '
             'exists; SAY is spoken-voice guidance, not a script; ASK / DO '
             'marks the interaction moments.',
          MX, yy - 10, CW, size=9.5, leading=14, color=MUTED)
    c.showPage()


def page(c, idx, title, mins, point, say, askdo, nums=None):
    c.setFillColor(CANVAS)
    c.rect(0, 0, PW, PH, stroke=0, fill=1)
    kicker(c, f'Slide {idx:02d}', MX, PH - 56, color=ORANGE, size=9)
    if mins != '—':
        c.setFont(SANSB, 9.5)
        c.setFillColor(MUTED)
        c.drawRightString(MX + CW, PH - 56, f'≈{mins} min')
    c.setFont(SER, 16)
    c.setFillColor(INK)
    # title may need wrapping
    tl = wrap(title, SER, 16, CW)
    ty = PH - 80
    for ln in tl:
        c.drawString(MX, ty, ln)
        ty -= 20
    # thumbnail
    img = RENDER / f'v3-{idx:02d}.png'
    tw = 300
    th = tw * 540 / 960
    tx0 = MX
    ty0 = ty - 8 - th
    c.setFillColor(HexColor('#1A1A1A'))
    c.roundRect(tx0 + 3, ty0 - 3, tw, th, 8, stroke=0, fill=1)
    c.drawImage(ImageReader(str(img)), tx0, ty0, tw, th)
    c.setStrokeColor(HexColor('#383838'))
    c.setLineWidth(1)
    c.roundRect(tx0, ty0, tw, th, 8, stroke=1, fill=0)
    # THE POINT beside thumbnail
    px = tx0 + tw + 16
    pw_ = MX + CW - px
    kicker(c, 'The point', px, ty - 22, color=TEAL)
    block(c, point, px, ty - 36, pw_, font=SERI, size=10.5, leading=15,
          color=INK)
    # SAY
    y = ty0 - 26
    kicker(c, 'Say', MX, y, color=ORANGE)
    y = block(c, say, MX, y - 14, CW, font=SANS, size=10.5, leading=15.5,
              color=INK)
    if nums:
        kicker(c, 'The numbers — decoded', MX, y - 4, color=TEAL)
        y -= 20
        for fig, expl in nums:
            c.setFont(SANSB, 10)
            c.setFillColor(ORANGE)
            for j, ln in enumerate(wrap(fig, SANSB, 10, 92)):
                c.drawString(MX, y - 9 - j * 12, ln)
            ny = block(c, expl, MX + 100, y, CW - 100, size=9.3, leading=13,
                       color=INK)
            y = min(ny, y - 24) - 7
        y -= 4
    if askdo:
        label = 'Do' if askdo.startswith('DO') else 'Ask'
        body = askdo.split('—', 1)[1].strip() if '—' in askdo[:6] else askdo
        # strip leading ASK/DO token
        for tok in ('ASK —', 'DO —', 'ASK', 'DO'):
            if askdo.startswith(tok):
                body = askdo[len(tok):].lstrip(' —')
                break
        bh = len(wrap(body, SANS, 10, CW - 44)) * 14.5 + 34
        c.setFillColor(PALE_BLUE)
        c.roundRect(MX, y - bh - 8, CW, bh, 10, stroke=0, fill=1)
        kicker(c, label, MX + 16, y - 28, color=TEAL)
        block(c, body, MX + 16, y - 42, CW - 44, size=10, leading=14.5,
              color=INK)
    c.setFont(SANS, 7.5)
    c.setFillColor(LABEL)
    c.drawString(MX, 30, 'Nurturing Potential · speaker notes')
    c.drawRightString(MX + CW, 30, f'{idx:02d} / 51')
    c.showPage()


def build():
    register_fonts()
    assert len(NOTES) == 51, f'expected 51 notes, got {len(NOTES)}'
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle('Nurturing Potential — Speaker Notes')
    cover(c)
    for i, (title, mins, point, say, askdo) in enumerate(NOTES, 1):
        page(c, i, title, mins, point, say, askdo, NUM.get(i))
    c.save()
    print(f'notes: {OUT} ({len(NOTES)} slides + cover)')


if __name__ == '__main__':
    build()
