#!/usr/bin/env python3
"""
Generate the formal ~10-page evidence appendix PDF for Nextstepuni.

Academic sources backing each platform feature, Innovation Zone tool breakdowns,
and DEIS school challenges with how the platform addresses them.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether,
)
from reportlab.lib import colors
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'Nextstepuni_Evidence_Appendix.pdf')

# ── Colours ──────────────────────────────────────────────────────────────────
BRAND_DARK  = HexColor('#18181b')   # zinc-900
BRAND_BLUE  = HexColor('#3b82f6')   # blue-500
BRAND_INDIGO = HexColor('#6366f1')  # indigo-500
SECTION_BG  = HexColor('#f4f4f5')   # zinc-100
MUTED       = HexColor('#71717a')   # zinc-500

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    'DocTitle', parent=styles['Title'],
    fontSize=22, leading=28, textColor=BRAND_DARK,
    spaceAfter=6, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    'DocSubtitle', parent=styles['Normal'],
    fontSize=11, leading=14, textColor=MUTED,
    spaceAfter=20, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    'SectionHead', parent=styles['Heading1'],
    fontSize=15, leading=20, textColor=BRAND_BLUE,
    spaceBefore=18, spaceAfter=8,
))
styles.add(ParagraphStyle(
    'SubHead', parent=styles['Heading2'],
    fontSize=12, leading=16, textColor=BRAND_INDIGO,
    spaceBefore=12, spaceAfter=4,
))
styles.add(ParagraphStyle(
    'BodyJ', parent=styles['Normal'],
    fontSize=10, leading=14, alignment=TA_JUSTIFY,
    spaceAfter=6,
))
styles.add(ParagraphStyle(
    'Citation', parent=styles['Normal'],
    fontSize=8.5, leading=11, textColor=MUTED,
    leftIndent=12, spaceAfter=3,
))
styles.add(ParagraphStyle(
    'BulletBody', parent=styles['Normal'],
    fontSize=10, leading=14, leftIndent=18, bulletIndent=6,
    spaceAfter=3, alignment=TA_JUSTIFY,
))
styles.add(ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontSize=9, leading=12,
))
styles.add(ParagraphStyle(
    'TableHead', parent=styles['Normal'],
    fontSize=9, leading=12, textColor=colors.white,
))

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=MUTED, spaceAfter=8, spaceBefore=4)

def bullet(text):
    return Paragraph(f'• {text}', styles['BulletBody'])

def cite(text):
    return Paragraph(text, styles['Citation'])

def body(text):
    return Paragraph(text, styles['BodyJ'])

def section(text):
    return Paragraph(text, styles['SectionHead'])

def subsection(text):
    return Paragraph(text, styles['SubHead'])


# ── Build ────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title='Nextstepuni — Evidence Appendix',
        author='Nextstepuni',
    )

    story = []

    # ── Title page ───────────────────────────────────────────────────────
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph('Nextstepuni — Evidence Appendix', styles['DocTitle']))
    story.append(Paragraph(
        'Academic and Research Foundations for Platform Design',
        styles['DocSubtitle'],
    ))
    story.append(Spacer(1, 8*mm))
    story.append(body(
        'This document presents the scientific evidence underpinning Nextstepuni\'s '
        'Learning Lab platform. Each feature, module, and Innovation Zone tool is '
        'mapped to peer-reviewed research and published data from Irish educational '
        'bodies (HEA, ESRI, CSO, DES). Particular attention is given to the DEIS '
        'school context, where the platform is designed to have the greatest impact.'
    ))
    story.append(Spacer(1, 4*mm))
    story.append(body(
        '<i>Prepared for stakeholder review — March 2026</i>'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 1 — DEIS Context
    # ══════════════════════════════════════════════════════════════════════
    story.append(section('1. The DEIS School Context: Challenges and Gaps'))
    story.append(body(
        'The Delivering Equality of Opportunity in Schools (DEIS) programme, '
        'established by the Department of Education in 2005, targets schools '
        'serving the most socio-economically disadvantaged communities in Ireland. '
        'Despite significant investment, persistent gaps remain in student outcomes, '
        'particularly at senior cycle and in progression to third-level education.'
    ))
    story.append(Spacer(1, 2*mm))

    story.append(subsection('1.1 Lower Third-Level Progression'))
    story.append(body(
        'HEA data consistently shows that students from DEIS schools progress '
        'to higher education at significantly lower rates than the national average. '
        'The HEA\'s <i>Equal Access Survey</i> (2022) found that students from '
        'non-manual and semi/unskilled backgrounds — the groups concentrated in '
        'DEIS catchments — remain under-represented in universities, particularly '
        'in high-points courses. The ESRI report <i>"Leaving School in Ireland"</i> '
        '(McCoy et al., 2014) established that socio-economic background is the '
        'strongest predictor of Leaving Certificate performance and college entry, '
        'even after controlling for prior achievement.'
    ))
    story.append(cite(
        'HEA (2022). <i>National Access Plan Progress Review 2022–2028</i>. '
        'Higher Education Authority.'
    ))
    story.append(cite(
        'McCoy, S., Smyth, E., Watson, D. & Darmody, M. (2014). '
        '<i>Leaving School in Ireland: A Longitudinal Study of Post-School Transitions</i>. ESRI.'
    ))

    story.append(subsection('1.2 Lack of Self-Belief and Academic Self-Efficacy'))
    story.append(body(
        'Research by Smyth and McCoy (2009) at the ESRI demonstrated that '
        'students in disadvantaged schools report significantly lower academic '
        'self-concept and aspirations than peers in non-DEIS settings. Bandura\'s '
        'self-efficacy theory (1997) holds that belief in one\'s capability to '
        'succeed is among the strongest predictors of academic achievement. In '
        'DEIS contexts, repeated low performance and limited exposure to '
        'third-level role models erode this self-belief, creating a cycle where '
        'low expectations lead to low engagement and poor outcomes.'
    ))
    story.append(cite(
        'Smyth, E. & McCoy, S. (2009). "Investing in Education: Combating '
        'Educational Disadvantage." <i>ESRI Research Series No. 6</i>.'
    ))
    story.append(cite(
        'Bandura, A. (1997). <i>Self-Efficacy: The Exercise of Control</i>. '
        'W.H. Freeman.'
    ))

    story.append(subsection('1.3 No Clear Picture of Current Performance'))
    story.append(body(
        'Unlike students in fee-paying or grind-school environments who receive '
        'frequent, structured feedback on their performance trajectory, many DEIS '
        'students lack visibility into where they stand relative to their goals. '
        'Hattie\'s meta-analyses (2009, 2023) identify <b>feedback</b> (d = 0.70) '
        'and <b>self-assessment</b> (d = 0.54) as among the highest-impact '
        'interventions in education. Without structured self-monitoring tools, '
        'students cannot make informed decisions about where to direct study effort.'
    ))
    story.append(cite(
        'Hattie, J. (2009). <i>Visible Learning</i>. Routledge.'
    ))
    story.append(cite(
        'Hattie, J. (2023). <i>Visible Learning: The Sequel</i>. Routledge.'
    ))

    story.append(subsection('1.4 No Explicit Study Strategy Instruction'))
    story.append(body(
        'A core finding from Dunlosky et al.\'s landmark review (2013) of learning '
        'techniques is that the most effective strategies — retrieval practice, '
        'spaced repetition, interleaving — are rarely taught explicitly in schools. '
        'Instead, students default to ineffective methods like re-reading and '
        'highlighting. This problem is amplified in DEIS schools where access to '
        'supplementary tuition (grinds) that might compensate for this gap is '
        'limited. The ESRI\'s <i>Growing Up in Ireland</i> study (2019) found '
        'that children from disadvantaged backgrounds are substantially less '
        'likely to receive private tuition.'
    ))
    story.append(cite(
        'Dunlosky, J., Rawson, K.A., Marsh, E.J., Nathan, M.J. & Willingham, D.T. '
        '(2013). "Improving Students\' Learning With Effective Learning Techniques." '
        '<i>Psychological Science in the Public Interest</i>, 14(1), 4–58.'
    ))
    story.append(cite(
        'ESRI (2019). <i>Growing Up in Ireland: Key Findings Series</i>. '
        'Dept. of Children, Equality, Disability, Integration and Youth.'
    ))

    story.append(subsection('1.5 Guidance Counsellor Capacity'))
    story.append(body(
        'The Institute of Guidance Counsellors (IGC) has repeatedly noted that '
        'the student-to-counsellor ratio in many DEIS schools exceeds 500:1, '
        'far above recommended levels. The DES Circular 0009/2012 cut ex-quota '
        'guidance provision during the recession, and while partially restored, '
        'capacity in DEIS schools remains strained. Counsellors report spending '
        'disproportionate time on crisis support rather than proactive career '
        'and academic guidance (IGC, 2021). Technology-assisted tools that give '
        'counsellors a dashboard view of student progress and career direction '
        'can amplify their limited time.'
    ))
    story.append(cite(
        'Institute of Guidance Counsellors (2021). <i>Annual Survey of Guidance '
        'Counsellors</i>. IGC Ireland.'
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 2 — Core Learning Modules
    # ══════════════════════════════════════════════════════════════════════
    story.append(section('2. Core Learning Modules — Scientific Foundations'))
    story.append(body(
        'Nextstepuni\'s 43+ educational modules are organised into seven categories. '
        'Each module teaches a specific, evidence-based learning strategy through '
        'interactive content, micro-commitments, and personal reflection. Below are '
        'the key strategies and their research backing.'
    ))

    # 2.1 Spaced Repetition
    story.append(subsection('2.1 Spaced Repetition'))
    story.append(body(
        'The spacing effect — distributing study over time rather than massing it — '
        'is one of the most robust findings in cognitive psychology. Cepeda et al. '
        '(2006) conducted a meta-analysis of 254 studies and found that spaced '
        'practice consistently outperformed massed practice, with effect sizes '
        'often exceeding d = 0.50. Nextstepuni\'s <b>Mastering Spaced Repetition</b> '
        'module teaches students to build optimal review schedules and includes an '
        'interactive calculator that generates personalised spacing intervals.'
    ))
    story.append(cite(
        'Cepeda, N.J., Pashler, H., Vul, E., Wixted, J.T. & Rohrer, D. (2006). '
        '"Distributed Practice in Verbal Recall Tasks." <i>Review of Educational '
        'Research</i>, 76(3), 354–380.'
    ))

    # 2.2 Active Recall / Retrieval Practice
    story.append(subsection('2.2 Active Recall and Retrieval Practice'))
    story.append(body(
        'Roediger and Butler (2011) demonstrated that testing oneself on material — '
        'rather than passively re-reading — produces significantly stronger '
        'long-term retention (the "testing effect"). Karpicke and Blunt (2011) '
        'showed retrieval practice outperformed elaborative concept mapping for '
        'learning science texts. Multiple Nextstepuni modules teach students '
        'to replace passive review with active self-testing, and the platform\'s '
        'interactive quizzes within modules serve as in-built retrieval practice.'
    ))
    story.append(cite(
        'Roediger, H.L. & Butler, A.C. (2011). "The Critical Role of Retrieval '
        'Practice in Long-Term Retention." <i>Trends in Cognitive Sciences</i>, '
        '15(1), 20–27.'
    ))
    story.append(cite(
        'Karpicke, J.D. & Blunt, J.R. (2011). "Retrieval Practice Produces More '
        'Learning than Elaborative Studying with Concept Mapping." '
        '<i>Science</i>, 331(6018), 772–775.'
    ))

    # 2.3 Interleaving
    story.append(subsection('2.3 Interleaving'))
    story.append(body(
        'Rohrer and Taylor (2007) demonstrated that interleaving — mixing different '
        'problem types or topics during study — improves the ability to discriminate '
        'between solution strategies and enhances transfer. This is particularly '
        'relevant for Leaving Certificate mathematics and sciences, where students '
        'must choose the correct approach from a repertoire. The <b>Mastering '
        'Interleaving</b> module includes a Problem Type Spotter interactive that '
        'trains exactly this discrimination skill.'
    ))
    story.append(cite(
        'Rohrer, D. & Taylor, K. (2007). "The Shuffling of Mathematics Problems '
        'Improves Learning." <i>Instructional Science</i>, 35(6), 481–498.'
    ))

    # 2.4 Growth Mindset
    story.append(subsection('2.4 Growth Mindset'))
    story.append(body(
        'Dweck\'s (2006) research established that students who believe intelligence '
        'is malleable (growth mindset) outperform those with a fixed mindset, '
        'particularly when facing setbacks. Yeager et al. (2019), in a large-scale '
        'RCT across 65 US schools (N = 12,490), found that a brief growth mindset '
        'intervention improved grades among lower-achieving students by 0.1 GPA '
        'points — a meaningful effect when scaled. For DEIS students who may have '
        'internalised narratives of limited ability, reframing intelligence as '
        'developable is foundational.'
    ))
    story.append(cite(
        'Dweck, C.S. (2006). <i>Mindset: The New Psychology of Success</i>. '
        'Random House.'
    ))
    story.append(cite(
        'Yeager, D.S. et al. (2019). "A National Experiment Reveals Where a Growth '
        'Mindset Improves Achievement." <i>Nature</i>, 573, 364–369.'
    ))

    # 2.5 Metacognition
    story.append(subsection('2.5 Metacognition and Self-Regulated Learning'))
    story.append(body(
        'The Education Endowment Foundation (EEF) identifies metacognition and '
        'self-regulation as providing an average of +7 months of additional progress '
        'at very low cost — one of the highest-impact, lowest-cost interventions '
        'available. Zimmerman (2002) showed that self-regulated learners set goals, '
        'select strategies, monitor progress, and adapt — exactly the cycle that '
        'Nextstepuni\'s modules teach through structured reflection prompts and '
        'micro-commitments at the end of each section.'
    ))
    story.append(cite(
        'Education Endowment Foundation (2023). <i>Teaching and Learning Toolkit: '
        'Metacognition and Self-Regulation</i>. EEF.'
    ))
    story.append(cite(
        'Zimmerman, B.J. (2002). "Becoming a Self-Regulated Learner: An Overview." '
        '<i>Theory Into Practice</i>, 41(2), 64–70.'
    ))

    # 2.6 Neuroplasticity
    story.append(subsection('2.6 Neuroplasticity Awareness'))
    story.append(body(
        'Teaching students about neuroplasticity — the brain\'s ability to '
        'reorganise and strengthen neural pathways through practice — provides '
        'a scientific foundation for growth mindset beliefs. Blackwell, '
        'Trzesniewski, and Dweck (2007) found that a workshop teaching students '
        'that the brain grows with effort led to improved maths achievement. '
        'Nextstepuni\'s <b>Neuroplasticity Protocol</b> module uses visualisations '
        'of synapse strengthening and a "Study Method Grader" to make this '
        'neuroscience tangible and actionable.'
    ))
    story.append(cite(
        'Blackwell, L.S., Trzesniewski, K.H. & Dweck, C.S. (2007). "Implicit '
        'Theories of Intelligence Predict Achievement Across an Adolescent '
        'Transition." <i>Child Development</i>, 78(1), 246–263.'
    ))

    # 2.7 Cognitive Load
    story.append(subsection('2.7 Cognitive Architecture and Dual Coding'))
    story.append(body(
        'Sweller\'s Cognitive Load Theory (1988, 2019) informs the platform\'s '
        'progressive-disclosure design: content is divided into short sections '
        'with a single concept per screen, reducing extraneous cognitive load. '
        'Paivio\'s Dual Coding Theory (1986) — combining verbal and visual '
        'representations — is applied through the platform\'s interactive '
        'visualisations, SVG diagrams, and animated models alongside text '
        'explanations.'
    ))
    story.append(cite(
        'Sweller, J., van Merriënboer, J.J.G. & Paas, F. (2019). "Cognitive '
        'Architecture and Instructional Design: 20 Years Later." '
        '<i>Educational Psychology Review</i>, 31, 261–292.'
    ))
    story.append(cite(
        'Paivio, A. (1986). <i>Mental Representations: A Dual Coding Approach</i>. '
        'Oxford University Press.'
    ))

    # 2.8 Elaborative Interrogation
    story.append(subsection('2.8 Elaborative Interrogation and the Feynman Technique'))
    story.append(body(
        'Dunlosky et al. (2013) rated elaborative interrogation as a "moderate" '
        'utility strategy — effective across a range of learners and tasks. The '
        'Feynman Technique, which asks students to explain concepts in simple terms, '
        'leverages this mechanism. Nextstepuni\'s modules prompt students to '
        'explain ideas back in their own words and identify gaps in their '
        'understanding, embedding elaborative processing directly into the '
        'learning experience.'
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 3 — Innovation Zone Tools
    # ══════════════════════════════════════════════════════════════════════
    story.append(section('3. Innovation Zone — Tool-by-Tool Evidence Base'))
    story.append(body(
        'The Innovation Zone is a suite of interactive tools that go beyond '
        'content delivery. Each tool addresses a specific gap identified in '
        'DEIS student experience and is grounded in established research.'
    ))

    # 3.1 War Room
    story.append(subsection('3.1 War Room (Grade Tracking & Performance Visibility)'))
    story.append(body(
        '<b>What it does:</b> A four-tab dashboard where students track their '
        'grades by subject, monitor mock exam trajectories over time, view '
        'syllabus coverage via a visual checklist, and access a strategic '
        'briefing with personalised study advice.'
    ))
    story.append(body(
        '<b>Evidence:</b> Self-monitoring is a core component of self-regulated '
        'learning (Zimmerman, 2002). Hattie (2009) found that self-reported '
        'grades/student expectations have the highest effect size in his '
        'meta-analysis (d = 1.44), meaning that when students have clear '
        'visibility of their performance, they calibrate effort more effectively. '
        'The EEF\'s guidance report on metacognition (2018) specifically '
        'recommends that schools "explicitly teach pupils how to plan, monitor, '
        'and evaluate their learning," which is exactly what the War Room enables.'
    ))
    story.append(body(
        '<b>DEIS relevance:</b> Students in disadvantaged settings are less '
        'likely to receive structured progress feedback outside of formal '
        'report cards. The War Room provides continuous, student-owned '
        'visibility — replacing the opaque "I don\'t know where I stand" '
        'with a clear, data-driven picture of current performance and trend.'
    ))
    story.append(cite(
        'EEF (2018). <i>Metacognition and Self-Regulated Learning: Guidance Report</i>. '
        'Education Endowment Foundation.'
    ))

    # 3.2 Comeback Engine
    story.append(subsection('3.2 Comeback Engine (Goal-Setting & Points Targeting)'))
    story.append(body(
        '<b>What it does:</b> Students set a target CAO points total and the tool '
        'breaks it down into per-subject grade targets. It calculates the gap '
        'between current and target performance, and generates a structured '
        '"comeback plan" with subject-level actions.'
    ))
    story.append(body(
        '<b>Evidence:</b> Locke and Latham\'s Goal-Setting Theory (2002), '
        'supported by decades of research, demonstrates that specific, '
        'challenging goals lead to higher performance than vague intentions. '
        'The mechanism works through directing attention, increasing effort, '
        'and promoting persistence. Morisano et al. (2010) found that a '
        'structured goal-setting intervention improved GPA in struggling '
        'university students.'
    ))
    story.append(body(
        '<b>DEIS relevance:</b> Many DEIS students have never articulated a '
        'specific points target or mapped what grades they need per subject '
        'to achieve it. The Comeback Engine makes ambition concrete and '
        'actionable, directly countering the vague aspiration problem.'
    ))
    story.append(cite(
        'Locke, E.A. & Latham, G.P. (2002). "Building a Practically Useful Theory '
        'of Goal Setting and Task Motivation." <i>American Psychologist</i>, '
        '57(9), 705–717.'
    ))
    story.append(cite(
        'Morisano, D., Hirsh, J.B., Peterson, J.B., Pihl, R.O. & Shore, B.M. '
        '(2010). "Setting, Elaborating, and Reflecting on Personal Goals Improves '
        'Academic Performance." <i>Journal of Applied Psychology</i>, 95(2), 255–264.'
    ))

    # 3.3 Future Finder
    story.append(subsection('3.3 Future Finder (Career & Course Discovery)'))
    story.append(body(
        '<b>What it does:</b> A 12-question assessment that matches students to '
        'CAO courses based on interests, values, work-style preferences, '
        'geographic preference, and subject alignment — not just points. Each '
        'recommendation includes 2-3 "why" explanations.'
    ))
    story.append(body(
        '<b>Evidence:</b> Holland\'s (1997) Theory of Vocational Personalities '
        'demonstrates that career satisfaction and persistence are highest when '
        'there is congruence between a person\'s interests and their occupational '
        'environment. Savickas (2005) extended this with Career Construction '
        'Theory, arguing that helping adolescents articulate their interests and '
        'values builds "career adaptability." For DEIS students with limited '
        'exposure to diverse careers, structured exploration tools fill a critical '
        'information gap.'
    ))
    story.append(body(
        '<b>DEIS relevance:</b> Research consistently shows that parental '
        'education level — lower on average in DEIS catchments — is the strongest '
        'predictor of students\' career knowledge breadth (Schoon & Parsons, '
        '2002). The Future Finder compensates for narrower social networks by '
        'systematically exposing students to courses and careers they may never '
        'have encountered.'
    ))
    story.append(cite(
        'Holland, J.L. (1997). <i>Making Vocational Choices</i> (3rd ed.). '
        'Psychological Assessment Resources.'
    ))
    story.append(cite(
        'Savickas, M.L. (2005). "The Theory and Practice of Career Construction." '
        'In S.D. Brown & R.W. Lent (Eds.), <i>Career Development and Counseling</i>, 42–70.'
    ))

    # 3.4 Timetable
    story.append(subsection('3.4 Study Timetable Builder'))
    story.append(body(
        '<b>What it does:</b> An interactive weekly planner that helps students '
        'allocate study time across subjects, with built-in spacing principles '
        'and break scheduling.'
    ))
    story.append(body(
        '<b>Evidence:</b> Time management is a key dimension of self-regulated '
        'learning (Zimmerman & Kitsantas, 1997). Britton and Tesser (1991) found '
        'that time management skills in first-year university students predicted '
        'GPA better than SAT scores. For exam preparation specifically, structured '
        'scheduling that distributes practice across subjects applies the spacing '
        'effect (Cepeda et al., 2006) at the macro level.'
    ))
    story.append(body(
        '<b>DEIS relevance:</b> Students without study-oriented home environments '
        'or private tuition often lack external structure for study. The Timetable '
        'Builder provides scaffolding that more resourced students receive '
        'through grinds schools and parental oversight.'
    ))
    story.append(cite(
        'Britton, B.K. & Tesser, A. (1991). "Effects of Time-Management Practices '
        'on College Grades." <i>Journal of Educational Psychology</i>, 83(3), 405–410.'
    ))

    # 3.5 Study Debrief
    story.append(subsection('3.5 Study Debrief (Reflection Tool)'))
    story.append(body(
        '<b>What it does:</b> After a study session, students answer structured '
        'reflection prompts: what they studied, what worked, what was difficult, '
        'and what they\'ll change next time.'
    ))
    story.append(body(
        '<b>Evidence:</b> Reflective practice is the "evaluate" phase of the '
        'plan–monitor–evaluate metacognitive cycle (EEF, 2018). Chi et al. (1989) '
        'demonstrated that self-explanation — articulating what you learned and '
        'where gaps remain — significantly improves comprehension and transfer. '
        'The debrief format also applies Kolb\'s (1984) experiential learning '
        'cycle, which positions reflection as essential for translating experience '
        'into improved future action.'
    ))
    story.append(body(
        '<b>DEIS relevance:</b> Without prompting, weaker students rarely '
        'reflect on their study effectiveness (Zimmerman, 2002). The structured '
        'debrief habit teaches a skill that self-regulating learners use '
        'intuitively.'
    ))
    story.append(cite(
        'Chi, M.T.H., Bassok, M., Lewis, M.W., Reimann, P. & Glaser, R. (1989). '
        '"Self-Explanations: How Students Study and Use Examples in Learning to '
        'Solve Problems." <i>Cognitive Science</i>, 13(2), 145–182.'
    ))

    # 3.6 Peer Island / Study Sessions
    story.append(subsection('3.6 Peer Island & Study Sessions (Collaborative Learning)'))
    story.append(body(
        '<b>What it does:</b> Peer Island enables students to form study groups, '
        'share insights, and engage in collaborative problem-solving. Study '
        'Sessions provide a structured format for group revision.'
    ))
    story.append(body(
        '<b>Evidence:</b> Vygotsky\'s Zone of Proximal Development (1978) '
        'established that learners can achieve more with peer support than alone. '
        'Johnson and Johnson\'s (2009) meta-analysis of cooperative learning '
        'found effect sizes of d = 0.67 for achievement compared to individual '
        'study. Peer tutoring specifically — where explaining to others deepens '
        'one\'s own understanding — yields d = 0.55 in the EEF Toolkit (2023). '
        'Webb and Mastergeorge (2003) showed that the quality of help-seeking '
        'and help-giving in peer groups is critical; structured collaboration '
        'outperforms unstructured social study.'
    ))
    story.append(body(
        '<b>DEIS relevance:</b> Students in disadvantaged areas may have fewer '
        'academically-oriented peer networks. Providing a structured digital '
        'space for collaborative study normalises academic engagement and creates '
        'peer accountability.'
    ))
    story.append(cite(
        'Johnson, D.W. & Johnson, R.T. (2009). "An Educational Psychology '
        'Success Story: Social Interdependence Theory and Cooperative Learning." '
        '<i>Educational Researcher</i>, 38(5), 365–379.'
    ))

    # 3.7 North Star
    story.append(subsection('3.7 North Star Onboarding (Goal Articulation)'))
    story.append(body(
        '<b>What it does:</b> The onboarding flow asks students to articulate '
        'their "North Star" — a personal goal or aspiration that anchors their '
        'study motivation. This is stored and referenced throughout the platform.'
    ))
    story.append(body(
        '<b>Evidence:</b> Oyserman, Bybee, and Terry (2006) demonstrated that '
        '"possible selves" interventions — where disadvantaged students '
        'articulate a detailed future self and the steps to get there — improved '
        'school attendance, behaviour, and GPA over an 8-week period. Having a '
        'clear, personally meaningful goal activates identity-based motivation, '
        'where academic effort becomes part of "who I am going to be" rather '
        'than an external obligation.'
    ))
    story.append(body(
        '<b>DEIS relevance:</b> Students lacking third-level role models in their '
        'family or community may never have been asked "What do you want to '
        'achieve?" in a structured way. The North Star prompt makes aspiration '
        'explicit and revisitable.'
    ))
    story.append(cite(
        'Oyserman, D., Bybee, D. & Terry, K. (2006). "Possible Selves and '
        'Academic Outcomes: How and When Possible Selves Impel Action." '
        '<i>Journal of Personality and Social Psychology</i>, 91(1), 188–204.'
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 4 — Platform Design Principles
    # ══════════════════════════════════════════════════════════════════════
    story.append(section('4. Platform Design Principles — Evidence Base'))

    # 4.1 Progressive Unlock
    story.append(subsection('4.1 Progressive Unlock and Micro-Commitments'))
    story.append(body(
        'Content is revealed one section at a time, requiring engagement before '
        'advancing. Each section ends with a "micro-commitment" — a short '
        'action the student agrees to take. This design draws on Fogg\'s (2009) '
        'Behavior Model: by making the target behaviour small and immediate, '
        'the motivation threshold is lowered. Cialdini\'s (2007) commitment and '
        'consistency principle further suggests that small public commitments '
        'increase follow-through.'
    ))
    story.append(cite(
        'Fogg, B.J. (2009). "A Behavior Model for Persuasive Design." '
        '<i>Proceedings of Persuasive \'09</i>, ACM.'
    ))

    # 4.2 Gamification
    story.append(subsection('4.2 Gamification (Activity Rings, Progress Tracking)'))
    story.append(body(
        'The platform uses visual progress indicators (activity rings), '
        'category completion tracking, and progressive unlock as gamification '
        'elements. Hamari, Koivisto, and Sarsa\'s (2014) systematic review '
        'of gamification in education found positive effects on engagement and '
        'learning outcomes in the majority of studies, particularly when '
        'gamification provided clear progress feedback and achievable milestones. '
        'Importantly, the platform avoids extrinsic reward mechanisms (points, '
        'leaderboards) that can undermine intrinsic motivation per Deci and '
        'Ryan\'s Self-Determination Theory (1985).'
    ))
    story.append(cite(
        'Hamari, J., Koivisto, J. & Sarsa, H. (2014). "Does Gamification Work? '
        'A Literature Review of Empirical Studies on Gamification." '
        '<i>Proceedings of HICSS-47</i>.'
    ))
    story.append(cite(
        'Deci, E.L. & Ryan, R.M. (1985). <i>Intrinsic Motivation and Self-Determination '
        'in Human Behavior</i>. Plenum Press.'
    ))

    # 4.3 GC Dashboard
    story.append(subsection('4.3 Guidance Counsellor Dashboard'))
    story.append(body(
        '<b>What it does:</b> Gives counsellors a read-only view of student '
        'engagement, module progress, saved career goals (from Future Finder), '
        'and grade trajectories — enabling data-informed conversations in '
        'limited one-to-one time.'
    ))
    story.append(body(
        '<b>Evidence:</b> Marzano (2003) identified that teacher awareness of '
        'individual student progress is a key factor in effective intervention. '
        'In the Irish context, the DES\'s <i>Looking at Guidance</i> inspection '
        'framework (2020) emphasises that effective guidance requires knowledge '
        'of students\' academic standing and career aspirations. The dashboard '
        'replaces anecdotal knowledge with structured data, allowing counsellors '
        'to prioritise students most in need of support.'
    ))
    story.append(body(
        '<b>DEIS relevance:</b> With counsellor-to-student ratios often exceeding '
        '500:1 in DEIS schools, efficiency tools are essential. The dashboard '
        'ensures that the limited guidance time available is spent on '
        'intervention rather than information-gathering.'
    ))
    story.append(cite(
        'Marzano, R.J. (2003). <i>What Works in Schools: Translating Research '
        'Into Action</i>. ASCD.'
    ))

    # 4.4 Subject-Specific Modules
    story.append(subsection('4.4 Subject-Specific Study Strategies'))
    story.append(body(
        'Beyond generic study skills, Nextstepuni includes modules tailored to '
        'specific Leaving Certificate disciplines: Maths, Sciences, Humanities, '
        'Languages, Business, and Creatives. Pressley, Borkowski, and Schneider '
        '(1987) demonstrated that strategy instruction is most effective when '
        'contextualised to specific domains, as students learn not just what a '
        'strategy is but <i>when and how to deploy it</i>. The platform filters '
        'available modules based on each student\'s subject choices, ensuring '
        'relevance.'
    ))
    story.append(cite(
        'Pressley, M., Borkowski, J.G. & Schneider, W. (1987). "Cognitive '
        'Strategies: Good Strategy Users Coordinate Metacognition and Knowledge." '
        '<i>Annals of Child Development</i>, 4, 89–129.'
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 5 — Impact Model for DEIS
    # ══════════════════════════════════════════════════════════════════════
    story.append(section('5. Theory of Change: How Nextstepuni Addresses DEIS Gaps'))
    story.append(body(
        'The following table maps each identified DEIS gap to the platform '
        'features that address it, with the underlying evidence mechanism.'
    ))

    table_data = [
        [Paragraph('<b>DEIS Gap</b>', styles['TableHead']),
         Paragraph('<b>Platform Feature</b>', styles['TableHead']),
         Paragraph('<b>Evidence Mechanism</b>', styles['TableHead'])],

        [Paragraph('Low academic self-belief', styles['TableCell']),
         Paragraph('Growth Mindset modules, Neuroplasticity Protocol, North Star onboarding', styles['TableCell']),
         Paragraph('Self-efficacy theory (Bandura, 1997); possible selves (Oyserman et al., 2006); brain-as-muscle framing (Blackwell et al., 2007)', styles['TableCell'])],

        [Paragraph('No visibility of performance', styles['TableCell']),
         Paragraph('War Room (grade tracking, trajectory, syllabus coverage)', styles['TableCell']),
         Paragraph('Self-monitoring (Zimmerman, 2002); feedback (Hattie, d = 0.70); metacognitive cycle (EEF, 2018)', styles['TableCell'])],

        [Paragraph('No study strategies taught', styles['TableCell']),
         Paragraph('43 core modules covering spaced repetition, retrieval practice, interleaving, elaboration, etc.', styles['TableCell']),
         Paragraph('Dunlosky et al. (2013) top-rated techniques; domain-specific strategy instruction (Pressley et al., 1987)', styles['TableCell'])],

        [Paragraph('Vague or absent career goals', styles['TableCell']),
         Paragraph('Future Finder, Comeback Engine, North Star', styles['TableCell']),
         Paragraph('Goal-setting theory (Locke & Latham, 2002); career construction (Savickas, 2005); possible selves (Oyserman et al., 2006)', styles['TableCell'])],

        [Paragraph('Limited guidance counsellor time', styles['TableCell']),
         Paragraph('GC Dashboard, War Room data export', styles['TableCell']),
         Paragraph('Data-informed guidance (DES, 2020); teacher awareness (Marzano, 2003)', styles['TableCell'])],

        [Paragraph('Lack of structured study time', styles['TableCell']),
         Paragraph('Timetable Builder, progressive unlock design', styles['TableCell']),
         Paragraph('Time management and GPA (Britton & Tesser, 1991); spacing effect (Cepeda et al., 2006)', styles['TableCell'])],

        [Paragraph('Fewer academic peer networks', styles['TableCell']),
         Paragraph('Peer Island, Study Sessions', styles['TableCell']),
         Paragraph('Cooperative learning (Johnson & Johnson, 2009, d = 0.67); peer tutoring (EEF, d = 0.55)', styles['TableCell'])],

        [Paragraph('Lower third-level progression', styles['TableCell']),
         Paragraph('All of the above, working together', styles['TableCell']),
         Paragraph('Cumulative: addressing upstream causes (self-belief, strategy, goals, support) to improve downstream outcome (progression)', styles['TableCell'])],
    ]

    t = Table(table_data, colWidths=[3.8*cm, 4.5*cm, 7.7*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, SECTION_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 6 — References
    # ══════════════════════════════════════════════════════════════════════
    story.append(section('6. References'))

    refs = [
        'Bandura, A. (1997). <i>Self-Efficacy: The Exercise of Control</i>. W.H. Freeman.',
        'Blackwell, L.S., Trzesniewski, K.H. & Dweck, C.S. (2007). "Implicit Theories of Intelligence Predict Achievement Across an Adolescent Transition." <i>Child Development</i>, 78(1), 246–263.',
        'Britton, B.K. & Tesser, A. (1991). "Effects of Time-Management Practices on College Grades." <i>Journal of Educational Psychology</i>, 83(3), 405–410.',
        'Cepeda, N.J., Pashler, H., Vul, E., Wixted, J.T. & Rohrer, D. (2006). "Distributed Practice in Verbal Recall Tasks." <i>Review of Educational Research</i>, 76(3), 354–380.',
        'Chi, M.T.H., Bassok, M., Lewis, M.W., Reimann, P. & Glaser, R. (1989). "Self-Explanations: How Students Study and Use Examples." <i>Cognitive Science</i>, 13(2), 145–182.',
        'Cialdini, R.B. (2007). <i>Influence: The Psychology of Persuasion</i> (Rev. ed.). HarperBusiness.',
        'Deci, E.L. & Ryan, R.M. (1985). <i>Intrinsic Motivation and Self-Determination in Human Behavior</i>. Plenum Press.',
        'DES (2020). <i>Looking at Guidance: A Quality Framework for Post-Primary Schools</i>. Dept. of Education and Skills.',
        'Dunlosky, J., Rawson, K.A., Marsh, E.J., Nathan, M.J. & Willingham, D.T. (2013). "Improving Students\' Learning With Effective Learning Techniques." <i>Psychological Science in the Public Interest</i>, 14(1), 4–58.',
        'Dweck, C.S. (2006). <i>Mindset: The New Psychology of Success</i>. Random House.',
        'Education Endowment Foundation (2018). <i>Metacognition and Self-Regulated Learning: Guidance Report</i>. EEF.',
        'Education Endowment Foundation (2023). <i>Teaching and Learning Toolkit</i>. EEF.',
        'ESRI (2019). <i>Growing Up in Ireland: Key Findings Series</i>. Dept. of Children, Equality, Disability, Integration and Youth.',
        'Fogg, B.J. (2009). "A Behavior Model for Persuasive Design." <i>Proceedings of Persuasive \'09</i>, ACM.',
        'Hamari, J., Koivisto, J. & Sarsa, H. (2014). "Does Gamification Work?" <i>Proceedings of HICSS-47</i>.',
        'Hattie, J. (2009). <i>Visible Learning</i>. Routledge.',
        'Hattie, J. (2023). <i>Visible Learning: The Sequel</i>. Routledge.',
        'HEA (2022). <i>National Access Plan Progress Review 2022–2028</i>. Higher Education Authority.',
        'Holland, J.L. (1997). <i>Making Vocational Choices</i> (3rd ed.). Psychological Assessment Resources.',
        'Institute of Guidance Counsellors (2021). <i>Annual Survey of Guidance Counsellors</i>. IGC Ireland.',
        'Johnson, D.W. & Johnson, R.T. (2009). "An Educational Psychology Success Story." <i>Educational Researcher</i>, 38(5), 365–379.',
        'Karpicke, J.D. & Blunt, J.R. (2011). "Retrieval Practice Produces More Learning than Elaborative Studying." <i>Science</i>, 331(6018), 772–775.',
        'Kolb, D.A. (1984). <i>Experiential Learning</i>. Prentice Hall.',
        'Locke, E.A. & Latham, G.P. (2002). "Building a Practically Useful Theory of Goal Setting." <i>American Psychologist</i>, 57(9), 705–717.',
        'Marzano, R.J. (2003). <i>What Works in Schools</i>. ASCD.',
        'McCoy, S., Smyth, E., Watson, D. & Darmody, M. (2014). <i>Leaving School in Ireland</i>. ESRI.',
        'Morisano, D. et al. (2010). "Setting, Elaborating, and Reflecting on Personal Goals." <i>Journal of Applied Psychology</i>, 95(2), 255–264.',
        'Oyserman, D., Bybee, D. & Terry, K. (2006). "Possible Selves and Academic Outcomes." <i>Journal of Personality and Social Psychology</i>, 91(1), 188–204.',
        'Paivio, A. (1986). <i>Mental Representations: A Dual Coding Approach</i>. Oxford University Press.',
        'Pressley, M., Borkowski, J.G. & Schneider, W. (1987). "Cognitive Strategies." <i>Annals of Child Development</i>, 4, 89–129.',
        'Roediger, H.L. & Butler, A.C. (2011). "The Critical Role of Retrieval Practice." <i>Trends in Cognitive Sciences</i>, 15(1), 20–27.',
        'Rohrer, D. & Taylor, K. (2007). "The Shuffling of Mathematics Problems Improves Learning." <i>Instructional Science</i>, 35(6), 481–498.',
        'Savickas, M.L. (2005). "The Theory and Practice of Career Construction." In Brown & Lent (Eds.), <i>Career Development and Counseling</i>, 42–70.',
        'Schoon, I. & Parsons, S. (2002). "Teenage Aspirations for Future Careers and Occupational Outcomes." <i>Journal of Vocational Behavior</i>, 60(2), 262–288.',
        'Smyth, E. & McCoy, S. (2009). "Investing in Education." <i>ESRI Research Series No. 6</i>.',
        'Sweller, J., van Merriënboer, J.J.G. & Paas, F. (2019). "Cognitive Architecture and Instructional Design." <i>Educational Psychology Review</i>, 31, 261–292.',
        'Vygotsky, L.S. (1978). <i>Mind in Society</i>. Harvard University Press.',
        'Webb, N.M. & Mastergeorge, A.M. (2003). "The Development of Students\' Helping Behavior and Learning in Peer-Directed Small Groups." <i>Cognition and Instruction</i>, 21(4), 361–428.',
        'Yeager, D.S. et al. (2019). "A National Experiment Reveals Where a Growth Mindset Improves Achievement." <i>Nature</i>, 573, 364–369.',
        'Zimmerman, B.J. (2002). "Becoming a Self-Regulated Learner." <i>Theory Into Practice</i>, 41(2), 64–70.',
        'Zimmerman, B.J. & Kitsantas, A. (1997). "Developmental Phases in Self-Regulation." <i>Journal of Educational Psychology</i>, 89(1), 29–36.',
    ]

    for r in refs:
        story.append(Paragraph(r, styles['Citation']))

    # ── Build PDF ────────────────────────────────────────────────────────
    doc.build(story)
    print(f'✓ Appendix PDF written to {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    build()
