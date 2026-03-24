#!/usr/bin/env python3
"""
Generate the punchy ~3-page evidence summary PDF for Nextstepuni.

A concise, business-style document summarising the scientific backing
for the platform, suitable for stakeholder meetings.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether,
)
from reportlab.lib import colors
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'Nextstepuni_Evidence_Summary.pdf')

# ── Colours ──────────────────────────────────────────────────────────────────
BRAND_DARK   = HexColor('#18181b')
BRAND_BLUE   = HexColor('#3b82f6')
BRAND_INDIGO = HexColor('#6366f1')
MUTED        = HexColor('#71717a')
ACCENT_BG    = HexColor('#eff6ff')  # blue-50

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    'DocTitle', parent=styles['Title'],
    fontSize=20, leading=26, textColor=BRAND_DARK,
    spaceAfter=4, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    'DocSubtitle', parent=styles['Normal'],
    fontSize=10, leading=13, textColor=MUTED,
    spaceAfter=14, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    'SectionHead', parent=styles['Heading1'],
    fontSize=13, leading=17, textColor=BRAND_BLUE,
    spaceBefore=14, spaceAfter=6,
))
styles.add(ParagraphStyle(
    'SubHead', parent=styles['Heading2'],
    fontSize=11, leading=14, textColor=BRAND_INDIGO,
    spaceBefore=10, spaceAfter=3,
))
styles.add(ParagraphStyle(
    'BodyJ', parent=styles['Normal'],
    fontSize=10, leading=14, alignment=TA_JUSTIFY,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    'BulletBody', parent=styles['Normal'],
    fontSize=10, leading=14, leftIndent=16, bulletIndent=4,
    spaceAfter=2, alignment=TA_JUSTIFY,
))
styles.add(ParagraphStyle(
    'Callout', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=BRAND_DARK,
    backColor=ACCENT_BG, borderPadding=8,
    leftIndent=6, rightIndent=6,
    spaceBefore=6, spaceAfter=6,
))
styles.add(ParagraphStyle(
    'SmallRef', parent=styles['Normal'],
    fontSize=7.5, leading=10, textColor=MUTED,
    spaceAfter=2,
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
    return HRFlowable(width='100%', thickness=0.5, color=MUTED, spaceAfter=6, spaceBefore=3)

def bullet(text):
    return Paragraph(f'• {text}', styles['BulletBody'])

def body(text):
    return Paragraph(text, styles['BodyJ'])


def build():
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title='Nextstepuni — Evidence Summary',
        author='Nextstepuni',
    )

    story = []

    # ── Header ───────────────────────────────────────────────────────────
    story.append(Paragraph('Nextstepuni — Evidence Summary', styles['DocTitle']))
    story.append(Paragraph(
        'Why This Platform Works: The Science Behind Every Feature',
        styles['DocSubtitle'],
    ))
    story.append(hr())

    # ── The Problem ──────────────────────────────────────────────────────
    story.append(Paragraph('The Problem', styles['SectionHead']))
    story.append(body(
        'Students in DEIS schools face a compounding set of challenges that '
        'conventional teaching alone cannot address:'
    ))
    story.append(bullet(
        '<b>Low self-belief:</b> Students in disadvantaged schools report '
        'significantly lower academic self-concept (Smyth & McCoy, 2009, ESRI). '
        'Without belief that effort leads to success, engagement drops.'
    ))
    story.append(bullet(
        '<b>No performance visibility:</b> Unlike students with private tutors '
        'or structured home support, DEIS students often have no clear picture '
        'of where they stand. Hattie (2009) rates feedback at d = 0.70 — one '
        'of the highest-impact interventions — yet these students receive the least of it.'
    ))
    story.append(bullet(
        '<b>No study strategies taught:</b> The most effective learning '
        'techniques (retrieval practice, spaced repetition, interleaving) are '
        'rarely taught in schools (Dunlosky et al., 2013). Students default to '
        're-reading and highlighting — methods rated as having "low utility."'
    ))
    story.append(bullet(
        '<b>Guidance counsellor overload:</b> DEIS school counsellor-to-student '
        'ratios often exceed 500:1 (IGC, 2021), leaving minimal time for '
        'proactive academic and career guidance.'
    ))
    story.append(bullet(
        '<b>Lower third-level progression:</b> The cumulative result — DEIS '
        'students progress to higher education at rates well below the national '
        'average (HEA, 2022).'
    ))
    story.append(Spacer(1, 2*mm))

    # ── The Solution ─────────────────────────────────────────────────────
    story.append(Paragraph('The Solution: Nextstepuni Learning Lab', styles['SectionHead']))
    story.append(body(
        'Nextstepuni is a web-based platform that teaches Leaving Certificate '
        'students <b>how to learn</b>, not just <b>what to learn</b>. Every '
        'feature is built on peer-reviewed research. Here\'s the evidence:'
    ))

    # ── Core Modules ─────────────────────────────────────────────────────
    story.append(Paragraph('Core Learning Modules', styles['SubHead']))

    table_data = [
        [Paragraph('<b>Strategy</b>', styles['TableHead']),
         Paragraph('<b>Key Evidence</b>', styles['TableHead']),
         Paragraph('<b>Impact</b>', styles['TableHead'])],

        [Paragraph('Spaced Repetition', styles['TableCell']),
         Paragraph('Cepeda et al. (2006) — meta-analysis of 254 studies', styles['TableCell']),
         Paragraph('d > 0.50 vs massed practice', styles['TableCell'])],

        [Paragraph('Retrieval Practice', styles['TableCell']),
         Paragraph('Roediger & Butler (2011); Karpicke & Blunt (2011, <i>Science</i>)', styles['TableCell']),
         Paragraph('Outperforms re-reading by 50%+', styles['TableCell'])],

        [Paragraph('Interleaving', styles['TableCell']),
         Paragraph('Rohrer & Taylor (2007)', styles['TableCell']),
         Paragraph('Improves problem discrimination', styles['TableCell'])],

        [Paragraph('Growth Mindset', styles['TableCell']),
         Paragraph('Yeager et al. (2019, <i>Nature</i>) — RCT, N = 12,490', styles['TableCell']),
         Paragraph('+0.1 GPA for lower achievers', styles['TableCell'])],

        [Paragraph('Metacognition', styles['TableCell']),
         Paragraph('EEF Toolkit (2023)', styles['TableCell']),
         Paragraph('+7 months progress, very low cost', styles['TableCell'])],

        [Paragraph('Neuroplasticity', styles['TableCell']),
         Paragraph('Blackwell, Trzesniewski & Dweck (2007)', styles['TableCell']),
         Paragraph('Improved maths achievement', styles['TableCell'])],
    ]

    t = Table(table_data, colWidths=[3.5*cm, 7*cm, 5.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f4f4f5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 3*mm))

    # ── Innovation Zone ──────────────────────────────────────────────────
    story.append(Paragraph('Innovation Zone Tools', styles['SubHead']))

    iz_data = [
        [Paragraph('<b>Tool</b>', styles['TableHead']),
         Paragraph('<b>What It Does</b>', styles['TableHead']),
         Paragraph('<b>Why It Works</b>', styles['TableHead'])],

        [Paragraph('<b>War Room</b>', styles['TableCell']),
         Paragraph('Track grades, mock trajectories, syllabus coverage', styles['TableCell']),
         Paragraph('Self-monitoring + feedback (Hattie, d = 0.70; Zimmerman, 2002)', styles['TableCell'])],

        [Paragraph('<b>Comeback Engine</b>', styles['TableCell']),
         Paragraph('Set target CAO points, break down into per-subject goals', styles['TableCell']),
         Paragraph('Goal-setting theory (Locke & Latham, 2002) — specific goals ↑ performance', styles['TableCell'])],

        [Paragraph('<b>Future Finder</b>', styles['TableCell']),
         Paragraph('12-question assessment → matched CAO course recommendations with "why" explanations', styles['TableCell']),
         Paragraph('Career congruence (Holland, 1997); possible selves (Oyserman et al., 2006)', styles['TableCell'])],

        [Paragraph('<b>Timetable</b>', styles['TableCell']),
         Paragraph('Weekly study planner with spacing built in', styles['TableCell']),
         Paragraph('Time management predicts GPA > SAT scores (Britton & Tesser, 1991)', styles['TableCell'])],

        [Paragraph('<b>Study Debrief</b>', styles['TableCell']),
         Paragraph('Post-session reflection prompts', styles['TableCell']),
         Paragraph('Self-explanation effect (Chi et al., 1989); metacognitive cycle (EEF, 2018)', styles['TableCell'])],

        [Paragraph('<b>Peer Island</b>', styles['TableCell']),
         Paragraph('Structured collaborative study groups', styles['TableCell']),
         Paragraph('Cooperative learning d = 0.67 (Johnson & Johnson, 2009)', styles['TableCell'])],

        [Paragraph('<b>North Star</b>', styles['TableCell']),
         Paragraph('Onboarding: articulate personal aspiration', styles['TableCell']),
         Paragraph('Identity-based motivation (Oyserman et al., 2006)', styles['TableCell'])],

        [Paragraph('<b>GC Dashboard</b>', styles['TableCell']),
         Paragraph('Counsellor view of student progress & goals', styles['TableCell']),
         Paragraph('Data-informed intervention (Marzano, 2003)', styles['TableCell'])],
    ]

    t2 = Table(iz_data, colWidths=[3*cm, 5.5*cm, 7.5*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_INDIGO),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f4f4f5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 3*mm))

    # ── Design principles ────────────────────────────────────────────────
    story.append(Paragraph('Platform Design', styles['SubHead']))
    story.append(bullet(
        '<b>Progressive unlock:</b> Content revealed one section at a time '
        'with micro-commitments — applying Fogg\'s Behavior Model (2009) to '
        'lower the motivation threshold for action.'
    ))
    story.append(bullet(
        '<b>Visual progress (activity rings):</b> Gamification that provides '
        'clear progress feedback without extrinsic rewards that undermine '
        'intrinsic motivation (Hamari et al., 2014; Deci & Ryan, 1985).'
    ))
    story.append(bullet(
        '<b>Subject-filtered content:</b> Modules are filtered to each '
        'student\'s Leaving Cert subjects — contextualised strategy instruction '
        'is more effective than generic advice (Pressley et al., 1987).'
    ))
    story.append(bullet(
        '<b>Interactive elements throughout:</b> Every module includes hands-on '
        'activities (simulators, graders, planners, drag-and-rank exercises). '
        'Active learning yields d = 0.36 higher exam performance than passive '
        'lectures (Freeman et al., 2014, <i>PNAS</i>).'
    ))
    story.append(Spacer(1, 4*mm))

    # ── DEIS-specific section ────────────────────────────────────────────
    story.append(Paragraph('Why This Matters for DEIS Schools', styles['SectionHead']))
    story.append(body(
        'DEIS students face a specific set of compounding disadvantages that '
        'Nextstepuni is designed to address directly:'
    ))
    story.append(Spacer(1, 2*mm))

    story.append(bullet(
        '<b>Self-belief gap → Growth Mindset + Neuroplasticity modules:</b> '
        'Students in disadvantaged schools report lower academic self-concept '
        '(Smyth & McCoy, 2009). Nextstepuni teaches that intelligence is '
        'malleable and backs it with neuroscience, rebuilding belief through '
        'evidence rather than empty encouragement.'
    ))
    story.append(bullet(
        '<b>Performance blindness → War Room:</b> Without grinds or structured '
        'home support, many DEIS students cannot answer "where do I stand?" '
        'The War Room provides continuous, student-owned visibility into '
        'grades, trajectories, and syllabus gaps — the kind of tracking that '
        'fee-paying school students receive as standard.'
    ))
    story.append(bullet(
        '<b>No strategy instruction → 43 core modules:</b> The most effective '
        'study techniques are almost never explicitly taught (Dunlosky et al., '
        '2013). Students in schools without grind culture are left using '
        'low-utility methods. Nextstepuni fills this gap with structured, '
        'interactive lessons on each high-impact technique.'
    ))
    story.append(bullet(
        '<b>Narrow career horizons → Future Finder + North Star:</b> '
        'First-generation students have fewer role models and narrower career '
        'awareness (Schoon & Parsons, 2002). These tools systematically expand '
        'horizons and make aspirations concrete.'
    ))
    story.append(bullet(
        '<b>Counsellor overload → GC Dashboard:</b> With ratios often '
        'exceeding 500:1, counsellors in DEIS schools need efficiency tools. '
        'The dashboard replaces information-gathering with data-informed '
        'intervention, maximising the impact of limited one-to-one time.'
    ))
    story.append(bullet(
        '<b>Lower third-level progression → cumulative effect:</b> Third-level '
        'progression is the downstream outcome. By addressing the upstream '
        'causes — self-belief, strategy, performance visibility, goal clarity, '
        'and guidance capacity — Nextstepuni targets the root of the problem, '
        'not just the symptom.'
    ))
    story.append(Spacer(1, 4*mm))

    # ── Callout ──────────────────────────────────────────────────────────
    story.append(Paragraph(
        '<b>The bottom line:</b> Every feature in Nextstepuni maps to at least '
        'one established research finding. This is not a content platform — it '
        'is a structured intervention that teaches students the skills, strategies, '
        'and self-awareness that the evidence says matter most, targeting the '
        'specific gaps that hold DEIS students back.',
        styles['Callout'],
    ))
    story.append(Spacer(1, 6*mm))

    # ── Key sources ──────────────────────────────────────────────────────
    story.append(Paragraph('Key Sources', styles['SubHead']))
    key_refs = [
        'Bandura, A. (1997). <i>Self-Efficacy: The Exercise of Control</i>. W.H. Freeman.',
        'Cepeda, N.J. et al. (2006). "Distributed Practice in Verbal Recall Tasks." <i>Review of Educational Research</i>, 76(3).',
        'Dunlosky, J. et al. (2013). "Improving Students\' Learning With Effective Learning Techniques." <i>Psych. Science in the Public Interest</i>, 14(1).',
        'EEF (2018). <i>Metacognition and Self-Regulated Learning: Guidance Report</i>.',
        'EEF (2023). <i>Teaching and Learning Toolkit</i>.',
        'Hattie, J. (2009). <i>Visible Learning</i>. Routledge.',
        'HEA (2022). <i>National Access Plan Progress Review 2022–2028</i>.',
        'Johnson, D.W. & Johnson, R.T. (2009). "Social Interdependence Theory and Cooperative Learning." <i>Ed. Researcher</i>, 38(5).',
        'Locke, E.A. & Latham, G.P. (2002). "Goal Setting and Task Motivation." <i>American Psychologist</i>, 57(9).',
        'McCoy, S., Smyth, E. et al. (2014). <i>Leaving School in Ireland</i>. ESRI.',
        'Oyserman, D. et al. (2006). "Possible Selves and Academic Outcomes." <i>JPSP</i>, 91(1).',
        'Roediger, H.L. & Butler, A.C. (2011). "The Critical Role of Retrieval Practice." <i>Trends in Cognitive Sciences</i>, 15(1).',
        'Smyth, E. & McCoy, S. (2009). "Investing in Education." <i>ESRI Research Series No. 6</i>.',
        'Yeager, D.S. et al. (2019). "Growth Mindset Improves Achievement." <i>Nature</i>, 573.',
        'Zimmerman, B.J. (2002). "Becoming a Self-Regulated Learner." <i>Theory Into Practice</i>, 41(2).',
    ]
    for r in key_refs:
        story.append(Paragraph(r, styles['SmallRef']))

    doc.build(story)
    print(f'✓ Summary PDF written to {os.path.abspath(OUTPUT_PATH)}')


if __name__ == '__main__':
    build()
