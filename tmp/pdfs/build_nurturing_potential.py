from __future__ import annotations

import os
import math
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path('/Users/alexlinehan/Documents/Nextstepuni-Launch-')
TMP = ROOT / 'tmp' / 'pdfs'
OUT = ROOT / 'output' / 'pdf'
TMP.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

DECK_PATH = OUT / 'Nurturing_Potential_Irish_Post_Primary_Workshop_Deck.pdf'
GUIDE_PATH = OUT / 'Nurturing_Potential_Facilitator_Guide.pdf'
WORKBOOK_PATH = OUT / 'Nurturing_Potential_Participant_Workbook.pdf'

DECK_W, DECK_H = 960, 540

CANVAS = HexColor('#FAFBF6')
PAPER = HexColor('#FFFFFF')
SOFT = HexColor('#F6F2EC')
INK = HexColor('#1A1A1A')
MUTED = HexColor('#5F5A55')
LABEL = HexColor('#8A8178')
ORANGE = HexColor('#F26B1F')
TEAL = HexColor('#2F6F6D')
OCHRE = HexColor('#B27A2D')
PURPLE = HexColor('#735D9D')
RED = HexColor('#B75353')
GREEN = HexColor('#4D7969')
OUTLINE = HexColor('#383838')
LINE = HexColor('#D8D3CD')
PALE_ORANGE = HexColor('#F9D8C4')
PALE_GREEN = HexColor('#D6E8DC')
PALE_BLUE = HexColor('#D9E7EE')
PALE_PURPLE = HexColor('#E2DCF0')
PALE_RED = HexColor('#EFD9D7')


SOURCES = {
    'cso_child': 'https://www.cso.ie/en/releasesandpublications/ep/p-silccd/silcmoduleonchilddeprivation2024/keyfindings/',
    'cso_poverty': 'https://www.cso.ie/en/releasesandpublications/ep/p-silc/surveyonincomeandlivingconditionssilc2024/poverty/',
    'tusla_attendance': 'https://www.tusla.ie/uploads/content/Analysis_of_School_Attendance_Data_2023-24.pdf',
    'tusla_reporting': 'https://www.tusla.ie/tess/tess-ews/reporting-absenteeism/',
    'tusla_ews': 'https://www.tusla.ie/services/educational-welfare-services/ews/',
    'retention': 'https://www.gov.ie/en/department-of-education/press-releases/minister-mcentee-launches-national-campaign-on-school-attendance/',
    'deis_strategy': 'https://www.gov.ie/en/department-of-education/publications/deis-strategy-to-2035/',
    'deis_plus': 'https://www.gov.ie/en/department-of-education/press-releases/minister-naughton-announces-48-million-investment-in-new-deis-strategy-and-deis-plus-scheme/',
    'pisa': 'https://www.oecd.org/en/publications/pisa-2022-results-volume-i-and-ii-country-notes_ed6fbcc5-en/ireland_01173012-en.html',
    'hea_profile': 'https://hea.ie/statistics/data-for-download-and-visualisations/students/widening-participation-for-equity-of-access/socio-economic-profiles-2021-22-2023-24/student-profile/',
    'hea_match': 'https://hea.ie/statistics/data-for-download-and-visualisations/students/student-course-match-analysis-2021/',
    'esri_relationships': 'https://www.esri.ie/publications/how-are-childrens-academic-self-concepts-their-parents-expectations-and-their',
    'esri_reengagement': 'https://www.esri.ie/publications/we-respect-them-and-they-respect-us-the-value-of-interpersonal-relationships-in',
    'esri_wellbeing': 'https://www.esri.ie/news/new-esri-research-highlights-importance-of-school-culture-relationships-and-belonging-in',
    'oecd_disadvantage': 'https://www.oecd.org/en/publications/oecd-review-of-resourcing-schools-to-address-educational-disadvantage-in-ireland_3433784c-en.html',
    'neps_service': 'https://www.gov.ie/en/department-of-education/services/national-educational-psychological-service-neps/',
    'neps_resources': 'https://www.gov.ie/en/department-of-education/collections/national-educational-psychological-service-neps-resources-and-publications/',
    'neps_wellbeing': 'https://www.gov.ie/en/department-of-education/publications/guidance-to-support-the-wellbeing-of-school-communities/',
    'student_support': 'https://www.gov.ie/en/department-of-education/publications/resources-for-student-support-teams/',
    'ace_caution': 'https://www.gov.uk/government/publications/trauma-informed-practice-learning-from-experience/trauma-informed-practice-learning-from-experience-of-violence-reduction-unit-delivery-2021-to-2023-accessible',
    'trauma_review': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8356508/',
    'eef_meta': 'https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/metacognition-and-self-regulation',
    'eef_feedback': 'https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/feedback',
    'eef_attendance': 'https://educationendowmentfoundation.org.uk/education-evidence/leadership-and-planning/supporting-attendance/summary-of-evidence',
    'ies_study': 'https://ies.ed.gov/ncee/wwc/PracticeGuide/1',
    'gov_study': 'https://www.gov.ie/en/department-of-education/publications/how-to-create-study-routines-for-the-leaving-certificate-during-the-covid-19-pandemic/',
    'pathways': 'https://www.gov.ie/en/department-of-further-and-higher-education-research-innovation-and-science/press-releases/ministers-lawless-and-harkin-urge-all-learners-to-explore-the-unprecedented-number-of-education-pathways-now-available/',
    'hear': 'https://accesscollege.ie/hear/how-do-i-apply/eligibility-criteria/',
    'susi': 'https://www.susi.ie/eligibility-reckoner-app-irish/index.html',
    'apprenticeship': 'https://www.gov.ie/en/department-of-further-and-higher-education-research-innovation-and-science/services/become-an-apprentice/',
}


def register_fonts():
    font_paths = {
        'BrandSerif': '/System/Library/Fonts/Supplemental/Georgia.ttf',
        'BrandSerifBold': '/System/Library/Fonts/Supplemental/Georgia Bold.ttf',
        'BrandSerifItalic': '/System/Library/Fonts/Supplemental/Georgia Italic.ttf',
        'BrandSerifBoldItalic': '/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf',
    }
    for name, path in font_paths.items():
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily(
        'BrandSerif',
        normal='BrandSerif',
        bold='BrandSerifBold',
        italic='BrandSerifItalic',
        boldItalic='BrandSerifBoldItalic',
    )


register_fonts()


def pstyle(name='Body', font='Helvetica', size=16, leading=None, color=INK,
           align=TA_LEFT, space_after=0, allow_widows=0):
    return ParagraphStyle(
        name=name,
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.28,
        textColor=color,
        alignment=align,
        spaceAfter=space_after,
        allowWidows=allow_widows,
        allowOrphans=0,
    )


def para(c, text, x, y_top, width, height, style, debug=False):
    story = Paragraph(text, style)
    w, h = story.wrap(width, height)
    story.drawOn(c, x, y_top - h)
    if debug:
        c.setStrokeColor(colors.magenta)
        c.rect(x, y_top - h, w, h, stroke=1, fill=0)
    return h


def draw_label(c, text, x, y, color=LABEL, size=9, tracking=1.9):
    c.saveState()
    c.setFillColor(color)
    t = c.beginText(x, y)
    t.setFont('Helvetica-Bold', size)
    t.setFillColor(color)
    t.setCharSpace(tracking)
    t.textLine(text.upper())
    c.drawText(t)
    c.restoreState()


def draw_title(c, text, x=52, y_top=460, width=850, size=32, color=INK, max_h=88):
    return para(c, text, x, y_top, width, max_h,
                pstyle('Title', 'BrandSerif', size, size * 1.08, color))


def draw_rule(c, x1, y, x2, color=LINE, width=1):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)
    c.restoreState()


def round_box(c, x, y, w, h, fill=PAPER, stroke=OUTLINE, radius=16, line_width=1.4, shadow=False):
    c.saveState()
    if shadow:
        c.setFillColor(INK)
        c.roundRect(x + 6, y - 7, w, h, radius, fill=1, stroke=0)
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(line_width)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    c.restoreState()


def blob(c, cx, cy, rx, ry, fill, rotation=0):
    c.saveState()
    c.translate(cx, cy)
    c.rotate(rotation)
    p = c.beginPath()
    p.moveTo(-0.95 * rx, 0.05 * ry)
    p.curveTo(-0.90 * rx, 0.75 * ry, -0.32 * rx, 1.05 * ry, 0.14 * rx, 0.88 * ry)
    p.curveTo(0.78 * rx, 0.67 * ry, 1.04 * rx, 0.25 * ry, 0.88 * rx, -0.20 * ry)
    p.curveTo(0.71 * rx, -0.76 * ry, 0.15 * rx, -1.02 * ry, -0.30 * rx, -0.89 * ry)
    p.curveTo(-0.81 * rx, -0.74 * ry, -1.08 * rx, -0.40 * ry, -0.95 * rx, 0.05 * ry)
    p.close()
    c.setFillColor(fill)
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def draw_icon(c, path, x, y, w, h, blob_fill=None, blob_pad=10):
    path = Path(path)
    if blob_fill is not None:
        blob(c, x + w / 2, y + h / 2, w / 2 + blob_pad, h / 2 + blob_pad, blob_fill, -7)
    if path.exists():
        c.drawImage(ImageReader(str(path)), x, y, width=w, height=h,
                    preserveAspectRatio=True, mask='auto', anchor='c')


def draw_screen(c, path, x, y, w, h, pad=10, shadow=True, radius=18):
    """Frame an authentic app capture without stretching or cropping it."""
    path = Path(path)
    round_box(c, x, y, w, h, PAPER, OUTLINE, radius, 1.3, shadow)
    if not path.exists():
        return
    reader = ImageReader(str(path))
    img_w, img_h = reader.getSize()
    avail_w, avail_h = w - pad * 2, h - pad * 2
    scale = min(avail_w / img_w, avail_h / img_h)
    draw_w, draw_h = img_w * scale, img_h * scale
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2
    c.drawImage(reader, draw_x, draw_y, width=draw_w, height=draw_h,
                preserveAspectRatio=True, mask='auto')


def draw_screen_crop(c, path, x, y, w, h, crop=(0, 0, 1, 1), pad=8,
                     shadow=True, radius=18):
    """Frame a live capture and zoom to a normalised top-left crop region."""
    path = Path(path)
    round_box(c, x, y, w, h, PAPER, OUTLINE, radius, 1.3, shadow)
    if not path.exists():
        return
    reader = ImageReader(str(path))
    img_w, img_h = reader.getSize()
    left, top, right, bottom = crop
    left = max(0, min(1, left)); right = max(left + 0.001, min(1, right))
    top = max(0, min(1, top)); bottom = max(top + 0.001, min(1, bottom))
    crop_w = (right - left) * img_w
    crop_h = (bottom - top) * img_h
    inner_x, inner_y = x + pad, y + pad
    inner_w, inner_h = w - pad * 2, h - pad * 2
    scale = max(inner_w / crop_w, inner_h / crop_h)
    crop_cx = ((left + right) / 2) * img_w
    crop_cy_from_bottom = (1 - (top + bottom) / 2) * img_h
    draw_x = inner_x + inner_w / 2 - crop_cx * scale
    draw_y = inner_y + inner_h / 2 - crop_cy_from_bottom * scale
    c.saveState()
    clip = c.beginPath()
    clip.rect(inner_x, inner_y, inner_w, inner_h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(reader, draw_x, draw_y, width=img_w * scale, height=img_h * scale,
                preserveAspectRatio=True, mask='auto')
    c.restoreState()


def number_dot(c, n, cx, cy, fill=ORANGE, r=16, text_color=PAPER):
    c.setFillColor(fill)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(cx, cy - 3.5, str(n).zfill(2))


def tool_tile(c, x, y, w, h, number, title, reason, fill, accent, icon_path=None):
    """A roomy Launchpad tile that keeps product names and rationale legible."""
    round_box(c, x, y, w, h, fill, OUTLINE, 17, 1.0, True)
    c.setFillColor(accent)
    c.circle(x + 27, y + h - 28, 14, fill=1, stroke=0)
    c.setFillColor(PAPER)
    c.setFont('Helvetica-Bold', 7)
    c.drawCentredString(x + 27, y + h - 30.5, str(number).zfill(2))
    if icon_path and Path(icon_path).exists():
        blob(c, x + w - 43, y + h - 34, 27, 24, PAPER, -6)
        draw_icon(c, icon_path, x + w - 70, y + h - 62, 57, 57)
    title_w = w - (115 if icon_path and Path(icon_path).exists() else 65)
    para(c, title, x + 51, y + h - 18, title_w, 39,
         pstyle(f'ToolTitle{number}{x}{y}', 'BrandSerif', 13.7 if w > 300 else 12.2,
                16.5 if w > 300 else 15, INK))
    para(c, reason, x + 21, y + h - 68, w - 42, h - 70,
         pstyle(f'ToolReason{number}{x}{y}', 'Helvetica', 9.1 if w > 300 else 8.6,
                12.8 if w > 300 else 12, MUTED))


def begin_slide(c, eyebrow, title, dark=False, slide_no=None):
    bg = INK if dark else CANVAS
    ink = PAPER if dark else INK
    muted = HexColor('#D6D0C9') if dark else MUTED
    c.setFillColor(bg)
    c.rect(0, 0, DECK_W, DECK_H, fill=1, stroke=0)
    draw_label(c, eyebrow, 52, 500, ORANGE if dark else LABEL, 8.5, 1.8)
    if title:
        draw_title(c, title, 52, 466, 850, 31, ink)
    if slide_no is not None:
        c.setFillColor(muted)
        c.setFont('Helvetica', 7.5)
        c.drawRightString(910, 24, f'{slide_no:02d}')
    return ink, muted


def source_footer(c, text, dark=False):
    c.saveState()
    c.setFont('Helvetica', 6.4)
    c.setFillColor(HexColor('#B7B0A9') if dark else LABEL)
    c.drawString(52, 22, text)
    c.restoreState()


def rich_lines(c, items, x, y_top, width, size=15, leading=22, color=INK,
               bullet_color=ORANGE, gap=9, bullet='•'):
    y = y_top
    for item in items:
        c.setFillColor(bullet_color)
        c.setFont('Helvetica-Bold', size)
        c.drawString(x, y - 1, bullet)
        h = para(c, item, x + 23, y + 4, width - 23, 80,
                 pstyle('List', 'Helvetica', size, leading, color))
        y -= max(leading, h) + gap
    return y


def stat(c, value, label, x, y, color=ORANGE, value_size=56, label_w=240):
    c.setFillColor(color)
    c.setFont('BrandSerif', value_size)
    c.drawString(x, y, value)
    para(c, label, x, y - 12, label_w, 100,
         pstyle('StatLabel', 'Helvetica', 13, 18, MUTED))


SLIDES = []


def add_meta(title, timing, purpose, say, ask='', watch='', route='', sources=None):
    SLIDES.append({
        'title': title,
        'timing': timing,
        'purpose': purpose,
        'say': say,
        'ask': ask,
        'watch': watch,
        'route': route,
        'sources': sources or [],
    })


def build_deck():
    c = canvas.Canvas(str(DECK_PATH), pagesize=(DECK_W, DECK_H), pageCompression=1)
    assets = ROOT / 'public' / 'assets'
    screens = TMP / 'app_screens'
    live = screens / 'live_demo'

    # 01 - title
    c.setFillColor(CANVAS); c.rect(0, 0, DECK_W, DECK_H, fill=1, stroke=0)
    draw_label(c, 'Nurturing potential', 54, 493, LABEL, 9, 2.2)
    para(c, 'Keep the door<br/>open.', 54, 441, 520, 210,
         pstyle('Cover', 'BrandSerif', 56, 58, INK))
    para(c, 'Helping every young person succeed in second-level education and navigate a future beyond it.',
         58, 268, 520, 100, pstyle('CoverSub', 'Helvetica', 18, 26, MUTED))
    draw_rule(c, 58, 170, 438, OUTLINE, 1.3)
    para(c, 'An Irish post-primary workshop for teachers, year heads and school leaders',
         58, 150, 440, 60, pstyle('CoverMeta', 'Helvetica-Bold', 11, 16, INK))
    blob(c, 758, 285, 130, 130, PALE_ORANGE, -8)
    draw_icon(c, assets / 'section-icons' / 'my-journey.png', 632, 158, 250, 250)
    c.setFillColor(ORANGE); c.circle(880, 466, 9, fill=1, stroke=0)
    c.showPage()
    add_meta(
        'Keep the door open.', '2 min',
        'Set a hopeful, demanding frame: this is about changing conditions, not rescuing or labelling children.',
        'Welcome the room. Name the destination: stronger expectations, better learning support, and a small whole-school plan people can actually carry back.',
        ask='None yet. Let the first minute feel intentional.',
        watch='Avoid framing staff as the problem or students as damaged.',
        route='Core in every version.', sources=[])

    # 02 - story
    n = len(SLIDES) + 1
    begin_slide(c, 'Start here', 'Before the data, a person.', slide_no=n)
    c.setStrokeColor(LINE); c.setLineWidth(3); c.line(145, 249, 815, 249)
    story_cards = [
        (70, PALE_BLUE, TEAL, '01', 'What was assumed.', 'The label, expectation or limit placed on me.'),
        (357, PALE_ORANGE, ORANGE, '02', 'What changed.', 'The adult action, opportunity or standard that shifted the path.'),
        (644, PALE_GREEN, GREEN, '03', 'What opened.', 'The choice, confidence or future that became possible.'),
    ]
    for x, fill, accent, num, head, body in story_cards:
        round_box(c, x, 112, 245, 270, fill, OUTLINE, 20, 1.2, True)
        c.setFillColor(accent); c.circle(x + 38, 344, 19, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 10); c.drawCentredString(x + 38, 340, num)
        para(c, head, x + 25, 300, 195, 58, pstyle(f'StoryHead{num}', 'BrandSerif', 22, 27, INK))
        draw_rule(c, x + 25, 240, x + 220, accent, 2.2)
        para(c, body, x + 25, 214, 195, 95, pstyle(f'StoryBody{num}', 'Helvetica', 13, 19, MUTED))
    source_footer(c, 'Tell the story in three beats. Your lived experience leads; the evidence follows.')
    c.showPage()
    add_meta(
        'Before the data, a person.', '6-8 min',
        'Give the evidence a human anchor and establish the presenter’s credibility without turning the story into a universal template.',
        'Tell your own DEIS journey in three beats: what was assumed about you; the adult, practice or opportunity that altered your trajectory; what still depended on your own agency. End on what became possible.',
        ask='You can step into the audience here. Ask listeners to hold one student in mind, without naming them.',
        watch='Do not imply that grit alone overcame structural barriers. Name both support and agency.',
        route='60 min: 5 minutes. 90/120 min: allow 7-8 minutes.', sources=[])

    # 03 - audience reflection
    n = len(SLIDES) + 1
    begin_slide(c, 'A quiet question', 'Who changed your odds?', slide_no=n)
    c.setStrokeColor(LINE); c.setLineWidth(3); c.line(142, 246, 818, 246)
    reflection_cards = [
        (72, 151, 246, 238, PALE_BLUE, TEAL, '01', 'Who noticed?', 'Who saw more than the label, result or difficult week?'),
        (356, 124, 246, 266, PALE_ORANGE, ORANGE, '02', 'What repeated?', 'What did they keep doing - quietly, reliably, more than once?'),
        (640, 151, 246, 238, PALE_GREEN, GREEN, '03', 'What opened?', 'Which choice, confidence or future became easier to imagine?'),
    ]
    for x, y, w, h, fill, accent, num, head, body in reflection_cards:
        round_box(c, x, y, w, h, fill, OUTLINE, 20, 1.2, True)
        c.setFillColor(accent); c.circle(x + 33, y + h - 35, 16, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 8); c.drawCentredString(x + 33, y + h - 38, num)
        para(c, head, x + 24, y + h - 78, w - 48, 52,
             pstyle(f'ReflectHead{num}', 'BrandSerif', 22, 27, INK))
        para(c, body, x + 24, y + h - 118, w - 48, 82,
             pstyle(f'ReflectBody{num}', 'Helvetica', 12, 18, MUTED))
    c.setFillColor(INK); c.roundRect(221, 69, 518, 39, 12, fill=1, stroke=0)
    para(c, '<b>Think privately.</b> If invited, share the practice - not the person.', 243, 94, 474, 22,
         pstyle('ReflectionBoundary', 'Helvetica', 10.5, 14, PAPER, TA_CENTER))
    source_footer(c, 'No one is required to disclose a personal experience.')
    c.showPage()
    add_meta(
        'Who changed your odds?', '3 min',
        'Prime the room to notice repeatable adult behaviours rather than heroic one-off gestures.',
        'Give 30 seconds of silence. Invite two or three responses. Translate each answer into a routine: “checked in” becomes “noticed absence quickly”; “believed in me” becomes “kept the level of challenge high and made the next step visible.”',
        ask='“What did they do repeatedly?”',
        watch='Do not force personal disclosure. People may have no positive school adult to name.',
        route='Core in 90/120. In 60, take one response only.', sources=[])

    # 04 - deprivation
    n = len(SLIDES) + 1
    begin_slide(c, 'The Irish starting line', 'One in seven.', slide_no=n)
    stat(c, '13.8%', 'of children lived in households experiencing child-specific enforced deprivation in 2024.', 76, 285, ORANGE, 74, 330)
    c.setFillColor(LINE); c.rect(478, 118, 1, 260, fill=1, stroke=0)
    para(c, 'This measure means a household could not afford at least three of 17 child-specific essentials or activities.',
         535, 348, 330, 110, pstyle('Explain', 'BrandSerif', 21, 29, INK))
    para(c, 'It is a description of conditions around childhood - not a description of a child’s capacity.',
         535, 222, 330, 80, pstyle('Explain2', 'Helvetica-Bold', 14, 21, TEAL))
    source_footer(c, 'Source: CSO, SILC Module on Child Deprivation 2024.')
    c.showPage()
    add_meta(
        'One in seven.', '4 min',
        'Make material disadvantage concrete while separating circumstances from ability.',
        'Define the statistic before interpreting it. Examples in the measure include adequate clothing, leisure, celebrations and school-related participation. Then state the central distinction: conditions can constrain learning opportunities; they do not measure intelligence or potential.',
        ask='“Where might these conditions quietly show up in school routines or expectations?” Take two answers.',
        watch='Do not invite staff to identify “which children” in the room or school.',
        route='Core in every version.', sources=[SOURCES['cso_child']])

    # 05 - attendance chart
    n = len(SLIDES) + 1
    begin_slide(c, 'Where inequality accumulates', 'Absence compounds quietly.', slide_no=n)
    vals = [('Non-DEIS', 18.6, TEAL), ('DEIS', 28.3, ORANGE)]
    for i, (lab, val, col) in enumerate(vals):
        x = 86 + i * 222
        track_x, track_y, track_w, track_h = x, 133, 176, 244
        c.setFillColor(HexColor('#E8E4DF'))
        c.roundRect(track_x, track_y, track_w, track_h, 20, fill=1, stroke=0)
        # Keep the original open vertical-bar composition, but place the value
        # deliberately inside the quiet headroom instead of letting it collide
        # with the bar or slide edge.
        c.setFillColor(col); c.setFont('BrandSerif', 43)
        c.drawCentredString(track_x + track_w / 2, track_y + track_h - 70, f'{val:.1f}%')
        fill_h = 160 * val / 32
        c.setFillColor(col)
        c.roundRect(track_x, track_y, track_w, fill_h, 20, fill=1, stroke=0)
        c.setFillColor(MUTED); c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(track_x + track_w / 2, 102, lab)

    round_box(c, 558, 244, 330, 133, PAPER, OUTLINE, 18, 1.2, True)
    draw_label(c, 'The reported gap', 584, 345, ORANGE, 7.8, 1.35)
    c.setFillColor(ORANGE); c.setFont('BrandSerif', 45); c.drawString(584, 285, '9.7')
    para(c, '<b>percentage points</b><br/>separate the two rates.', 690, 311, 170, 62,
         pstyle('AttendanceDelta', 'Helvetica', 12.5, 18, INK))

    round_box(c, 558, 133, 330, 88, PALE_BLUE, OUTLINE, 16, 1.0, True)
    c.setFillColor(TEAL); c.setFont('BrandSerif', 22); c.drawString(584, 176, '20+ days')
    para(c, 'is about four school weeks. Support should begin when the pattern emerges.', 704, 190, 158, 58,
         pstyle('AttendanceAction', 'Helvetica-Bold', 10.3, 14.5, INK))
    source_footer(c, 'Source: Tusla Analysis of School Attendance Data 2023/24. Post-primary response coverage: 541 of 722 schools.')
    c.showPage()
    add_meta(
        'Absence compounds quietly.', '5 min',
        'Show the size of the attendance gap without treating absence as a character flaw.',
        'Explain that 28.3% of students in responding DEIS post-primary schools and 18.6% in non-DEIS schools missed 20 or more days. The report covered 541 of 722 post-primary schools, so avoid presenting it as a census of every student.',
        ask='“What do we currently notice at day 3, day 5 or day 10 - before a statutory threshold?”',
        watch='Avoid saying absence automatically causes every later outcome. Frame it as lost access to teaching and a signal to investigate barriers.',
        route='Core. In 60, move straight to the next slide after the question.', sources=[SOURCES['tusla_attendance']])

    # 06 - retention
    n = len(SLIDES) + 1
    begin_slide(c, 'A system can move', 'Progress is real. The remaining gap is real.', slide_no=n)
    # timeline
    c.setStrokeColor(OUTLINE); c.setLineWidth(2); c.line(120, 272, 840, 272)
    points = [(170, '2006', '68.2%', 'DEIS retention'), (595, '2017 cohort', '83.4%', 'DEIS retention'), (790, '2017 cohort', '92.1%', 'non-DEIS')]
    for idx, (x, year, val, lab) in enumerate(points):
        col = ORANGE if idx < 2 else TEAL
        c.setFillColor(col); c.circle(x, 272, 11, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont('BrandSerif', 31); c.drawCentredString(x, 321 if idx != 1 else 192, val)
        c.setFillColor(MUTED); c.setFont('Helvetica-Bold', 10); c.drawCentredString(x, 304 if idx != 1 else 174, year)
        c.setFont('Helvetica', 9); c.drawCentredString(x, 291 if idx != 1 else 160, lab)
    para(c, 'The DEIS/non-DEIS retention gap narrowed from <b>16.8</b> to <b>8.7 percentage points</b>.',
         260, 112, 450, 50, pstyle('Retention', 'Helvetica', 14, 21, MUTED, TA_CENTER))
    source_footer(c, 'Source: Department of Education; Leaving Certificate retention for the 2017 first-year entry cohort.')
    c.showPage()
    add_meta(
        'Progress is real. The remaining gap is real.', '4 min',
        'Prevent fatalism: policy, resourcing and school practice have already shifted retention.',
        'DEIS retention improved from 68.2% in 2006 to 83.4% for the 2017 entry cohort. The gap narrowed, yet 83.4% still sat below 92.1% in non-DEIS schools. Use both truths together: improvement is possible and unfinished.',
        ask='“Which improvement in your own school proves that trajectories can change?”',
        watch='Be precise that these are retention-to-Leaving-Certificate rates, not third-level progression rates.',
        route='Core in 90/120; optional in 60.', sources=[SOURCES['retention'], SOURCES['deis_strategy']])

    # 07 - PISA inequality and resilience
    n = len(SLIDES) + 1
    begin_slide(c, 'The same dataset holds two truths', 'Background shifts the odds. It does not write the outcome.', slide_no=n)
    round_box(c, 70, 125, 365, 250, PAPER, OUTLINE, 22, 1.4, True)
    stat(c, '74', 'maths points separated Ireland’s most and least socio-economically advantaged quarters in PISA 2022.', 103, 262, RED, 68, 285)
    round_box(c, 530, 125, 365, 250, PAPER, OUTLINE, 22, 1.4, True)
    stat(c, '12%', 'of disadvantaged students were academically resilient - scoring in Ireland’s top quarter.', 565, 262, TEAL, 68, 285)
    source_footer(c, 'Source: OECD PISA 2022 Ireland country note. Interpret with the OECD’s response-rate caveat for Ireland.')
    c.showPage()
    add_meta(
        'Background shifts the odds. It does not write the outcome.', '5 min',
        'Hold inequality and agency together, avoiding both blame and determinism.',
        'The 74-point gap signals unequal odds. The 12% resilience figure shows that disadvantage is not destiny. Neither number licenses a prediction about an individual student. Note that OECD flagged Ireland’s response rate and estimated mean scores may be somewhat high; the slide uses the within-country gap and resilience rate cautiously.',
        ask='“What changes when we treat data as a prompt for support rather than a forecast of a child?”',
        watch='Do not call resilient students “exceptions” in a way that blames peers who face different barriers.',
        route='Core in every version.', sources=[SOURCES['pisa']])

    # 08 - HE routes
    n = len(SLIDES) + 1
    begin_slide(c, 'Opportunity includes navigation', 'The route into higher education is uneven.', slide_no=n)
    categories = [('Second-level exams', 61, 78), ('FET award', 9, 4), ('Mature + HEAR', 19, 4)]
    # Keep the chart labels in their own lane between the narrative card and
    # the bars. Long labels must never tuck underneath the card.
    x0, y0, chart_w = 420, 350, 406
    for i, (lab, dis, aff) in enumerate(categories):
        y = y0 - i * 105
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 10.5); c.drawString(320, y + 8, lab)
        for j, (v, col, label) in enumerate([(dis, ORANGE, 'Disadvantaged'), (aff, TEAL, 'Affluent')]):
            yy = y - j * 30
            c.setFillColor(HexColor('#EAE6E1')); c.roundRect(x0, yy, chart_w, 18, 9, fill=1, stroke=0)
            bar_w = chart_w * v / 82
            c.setFillColor(col); c.roundRect(x0, yy, bar_w, 18, 9, fill=1, stroke=0)
            # Percentage labels sit in a centred pill at the bar end rather
            # than floating above or below the visual measure.
            pill_x = min(x0 + chart_w - 36, max(x0 + 6, x0 + bar_w - 10))
            c.setFillColor(PAPER); c.roundRect(pill_x, yy + 1, 34, 16, 8, fill=1, stroke=0)
            c.setFillColor(INK); c.setFont('Helvetica-Bold', 9)
            c.drawCentredString(pill_x + 17, yy + 5, f'{v}%')
    c.setFillColor(ORANGE); c.circle(435, 88, 5, fill=1, stroke=0); c.setFillColor(MUTED); c.setFont('Helvetica', 10); c.drawString(446, 84, 'Disadvantaged entrants')
    c.setFillColor(TEAL); c.circle(620, 88, 5, fill=1, stroke=0); c.setFillColor(MUTED); c.drawString(631, 84, 'Affluent entrants')
    # Give the route callout its own generous editorial lane. The three routes
    # read as a sequence, not as labels squeezed beneath a headline.
    c.setFillColor(HexColor('#FFF8F2'))
    c.roundRect(52, 120, 254, 267, 24, fill=1, stroke=0)
    draw_label(c, 'The navigation gap', 78, 354, ORANGE, 7.7, 1.3)
    para(c, 'Routes need<br/><b>equal visibility.</b>', 78, 316, 202, 70,
         pstyle('RouteCallout', 'BrandSerif', 22, 27, INK))
    route_chips = [
        ('01', 'Points / CAO', PALE_ORANGE, ORANGE),
        ('02', 'FET / PLC', PALE_GREEN, GREEN),
        ('03', 'Mature / HEAR', PALE_BLUE, TEAL),
    ]
    chip_y = 220
    for num, label, fill, accent in route_chips:
        c.setFillColor(fill); c.roundRect(76, chip_y, 206, 39, 12, fill=1, stroke=0)
        c.setFillColor(accent); c.circle(96, chip_y + 19.5, 11, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 6.4); c.drawCentredString(96, chip_y + 17, num)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 10.2); c.drawString(116, chip_y + 15, label)
        chip_y -= 50
    para(c, '<b>Different routes are not lesser.</b>', 65, 103, 228, 24,
         pstyle('RouteEquity', 'Helvetica', 10.2, 14, TEAL, TA_CENTER))
    source_footer(c, 'Source: HEA socioeconomic student profile, undergraduate entrants 2021/22-2023/24. Categories shown do not exhaust all entry routes.')
    c.showPage()
    add_meta(
        'The route into higher education is uneven.', '5 min',
        'Show that progression depends partly on navigation and access routes, not only points.',
        'Among undergraduate entrants in the HEA profile, 61% of disadvantaged entrants came via second-level exams compared with 78% of affluent entrants; FET and mature/HEAR routes were more prominent for disadvantaged entrants. The categories on screen are selected routes and do not sum to 100%.',
        ask='“Are we giving parallel routes equal time, status and practical support?”',
        watch='Do not imply every disadvantaged learner should pursue higher education. The purpose is informed choice across routes.',
        route='Core in 90/120; optional data detail in 60.', sources=[SOURCES['hea_profile']])

    # 09 - assumptions
    n = len(SLIDES) + 1
    begin_slide(c, 'The danger in the story we tell', 'Data can sharpen action - or harden a stereotype.', slide_no=n)
    draw_label(c, 'The quick conclusion', 65, 355, RED, 8, 1.4)
    draw_label(c, 'The useful question', 520, 355, TEAL, 8, 1.4)
    pairs = [
        ('“They do not value school.”', '“What makes attendance harder here?”'),
        ('“The family will not engage.”', '“How accessible and trustworthy is our contact?”'),
        ('“Not college material.”', '“Which routes and supports are still invisible?”'),
        ('“Trauma explains the behaviour.”', '“What supports regulation and a return to learning?”'),
    ]
    y = 308
    for left, right in pairs:
        para(c, left, 65, y, 370, 48, pstyle('Assumption', 'BrandSerifItalic', 16, 21, MUTED))
        para(c, right, 520, y, 370, 48, pstyle('Question', 'Helvetica-Bold', 13, 19, INK))
        draw_rule(c, 65, y - 37, 892, LINE, 0.8)
        y -= 66
    source_footer(c, 'Principle: ask about barriers without lowering expectations or removing accountability.')
    c.showPage()
    add_meta(
        'Data can sharpen action - or harden a stereotype.', '6 min',
        'Challenge deficit thinking while keeping professional accountability and behavioural boundaries intact.',
        'Read one or two pairs aloud. Emphasise that a barrier question is not an excuse; it is a better route to an effective response. Expectations remain high, while support becomes more accurate.',
        ask='Invite pairs to rewrite one phrase they hear in their own context. Do not collect identifiable examples.',
        watch='Keep the tone challenging but non-shaming. Staff need enough psychological safety to examine practice honestly.',
        route='Core. In 120, allow 5 minutes in pairs; in 60, model one rewrite.', sources=[SOURCES['oecd_disadvantage']])

    # 10 - pivot
    n = len(SLIDES) + 1
    begin_slide(c, 'The pivot', 'Five promises that change the odds.', dark=True, slide_no=n)
    promises = [('Known', PALE_BLUE), ('Taught', PALE_ORANGE), ('Present', PALE_GREEN), ('Partnered', PALE_PURPLE), ('Future-ready', PALE_RED)]
    x_positions = [108, 287, 466, 645, 824]
    c.setStrokeColor(HexColor('#6F6963')); c.setLineWidth(2); c.line(108, 250, 824, 250)
    for i, ((lab, col), x) in enumerate(zip(promises, x_positions), start=1):
        c.setFillColor(col); c.circle(x, 250, 34, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 12); c.drawCentredString(x, 246, str(i).zfill(2))
        c.setFillColor(PAPER); c.setFont('BrandSerif', 18); c.drawCentredString(x, 185, lab)
    para(c, 'Not five programmes. Five dependable experiences of school.', 210, 120, 540, 45,
         pstyle('PivotLine', 'Helvetica', 15, 21, HexColor('#D6D0C9'), TA_CENTER))
    source_footer(c, 'A practical synthesis aligned with DEIS planning, NEPS Continuum of Support and Irish evidence.', True)
    c.showPage()
    add_meta(
        'Five promises that change the odds.', '3 min',
        'Give the workshop a memorable whole-school architecture.',
        'Introduce the five promises: every student is known; taught ambitiously; supported to attend; partnered with through family and community; and future-ready with navigable pathways. They are experiences to make dependable, not five new initiatives.',
        ask='Ask people to note which promise is currently strongest and which is least dependable.',
        watch='Do not let the language imply a guarantee of outcomes. The guarantee is the quality and consistency of provision.',
        route='Core in every version.', sources=[SOURCES['deis_strategy'], SOURCES['neps_service'], SOURCES['oecd_disadvantage']])

    # 11 - known
    n = len(SLIDES) + 1
    begin_slide(c, 'Promise 01 · Known', 'Relationships are learning infrastructure.', slide_no=n)
    round_box(c, 54, 118, 390, 266, PAPER, OUTLINE, 20, 1.3, True)
    draw_label(c, 'What the evidence points to', 80, 351, ORANGE, 7.7, 1.25)
    para(c, 'Positive teacher-student relationships at age 13 were especially important in the later attainment of economically vulnerable young people.',
         80, 315, 338, 130, pstyle('KnownEvidence', 'BrandSerif', 18.5, 25, INK))
    draw_rule(c, 80, 190, 418, ORANGE, 2.3)
    para(c, 'School cannot remove every external pressure.<br/><b>It can make sure no student becomes invisible.</b>',
         80, 170, 338, 58, pstyle('KnownSynthesis', 'Helvetica', 10.5, 15, MUTED))

    moves = [
        ('01', 'Name', 'One reliable adult the student can identify.', PALE_BLUE, TEAL),
        ('02', 'Notice', 'Absence, withdrawal and change trigger contact.', PALE_ORANGE, ORANGE),
        ('03', 'Repair', 'Conflict has a dignified route back to learning.', PALE_GREEN, GREEN),
        ('04', 'Record', 'Support begins with strengths and what works.', PALE_PURPLE, PURPLE),
    ]
    for idx, (num, head, body, fill, accent) in enumerate(moves):
        col = idx % 2
        row = idx // 2
        x = 485 + col * 205
        y = 256 - row * 137
        round_box(c, x, y, 180, 112, fill, OUTLINE, 16, 1.1, True)
        c.setFillColor(accent); c.circle(x + 25, y + 84, 14, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 7.5); c.drawCentredString(x + 25, y + 81, num)
        c.setFillColor(INK); c.setFont('BrandSerif', 16); c.drawString(x + 48, y + 78, head)
        para(c, body, x + 18, y + 58, 144, 50,
             pstyle(f'KnownMove{idx}', 'Helvetica', 9.5, 13.2, INK))
    c.setFillColor(TEAL); c.roundRect(102, 65, 756, 35, 12, fill=1, stroke=0)
    para(c, '<b>Belonging is not an extra programme.</b> It is how learning stays reachable.', 125, 89, 710, 22,
         pstyle('KnownBanner', 'Helvetica', 10.5, 14, PAPER, TA_CENTER))
    source_footer(c, 'Source: ESRI / Growing Up in Ireland research on self-concept, expectations and teacher-student relationships.')
    c.showPage()
    add_meta(
        'Relationships are learning infrastructure.', '6 min',
        'Move relationships out of the “nice extra” category and into the school’s learning design.',
        'Summarise the ESRI finding carefully as longitudinal association/model evidence, not proof that one relationship alone determines attainment. Then make the practice concrete: named adult, fast noticing, repair, and strength-based information.',
        ask='Private prompt: “Can the student you held in mind name their adult?”',
        watch='A named adult must have a routine and capacity; a spreadsheet assignment alone is not a relationship.',
        route='Core. In 120, invite examples of effective repair after conflict.', sources=[SOURCES['esri_relationships'], SOURCES['esri_reengagement']])

    # 12 - high expectations matrix
    n = len(SLIDES) + 1
    begin_slide(c, 'Promise 02 · Taught', 'High expectations need high support.', slide_no=n)
    x0, y0, size = 260, 95, 300
    # quadrants
    quad = [
        (x0, y0 + size/2, PALE_RED, 'A kind ceiling', 'Warm support; shrinking challenge'),
        (x0 + size/2, y0 + size/2, PALE_GREEN, 'Ambitious access', 'Challenge made reachable'),
        (x0, y0, SOFT, 'Abandonment', 'Low challenge; low support'),
        (x0 + size/2, y0, PALE_ORANGE, 'Sink or swim', 'High demand; hidden route'),
    ]
    for x, y, fill, head, body in quad:
        c.setFillColor(fill); c.setStrokeColor(PAPER); c.setLineWidth(4); c.rect(x, y, size/2, size/2, fill=1, stroke=1)
        para(c, f'<b>{head}</b><br/>{body}', x + 14, y + 100, size/2 - 28, 80,
             pstyle('Quad', 'Helvetica', 11, 16, INK, TA_CENTER))
    c.saveState(); c.translate(206, 230); c.rotate(90); c.setFillColor(MUTED); c.setFont('Helvetica-Bold', 10); c.drawCentredString(0, 0, 'SUPPORT >'); c.restoreState()
    c.setFillColor(MUTED); c.setFont('Helvetica-Bold', 10); c.drawCentredString(410, 72, 'EXPECTATION >')
    para(c, 'The goal is not “be tougher.”<br/>The goal is to make ambitious work <b>legible, scaffolded and attainable</b>.',
         635, 326, 255, 130, pstyle('MatrixCallout', 'BrandSerif', 20, 28, INK))
    source_footer(c, 'Workshop framework: distinguish demand from access, and care from lowered ceilings.')
    c.showPage()
    add_meta(
        'High expectations need high support.', '7 min',
        'Replace the false choice between compassion and academic ambition.',
        'Walk through the four quadrants. “Ambitious access” means preserving the intellectual goal while making the route visible: worked examples, vocabulary, guided practice, feedback, time and re-entry after absence. High expectation without access becomes sink-or-swim; support without challenge becomes a kind ceiling.',
        ask='“Where can a well-intended support accidentally reduce future options - subject level, task demand, timetable, or pathway advice?”',
        watch='Do not criticise individual accommodations. The issue is whether support preserves access to meaningful learning and choice.',
        route='Core. In 120, let departments map one current practice onto the matrix.', sources=[SOURCES['oecd_disadvantage']])

    # 13 - teaching cycle
    n = len(SLIDES) + 1
    begin_slide(c, 'Make success visible', 'Teach the route, not only the destination.', slide_no=n)
    steps = [
        ('01', 'Activate', 'What do we already know?'),
        ('02', 'Model', 'Think aloud; show a worked example.'),
        ('03', 'Guide', 'Practise together; fade support.'),
        ('04', 'Check', 'Hear from everyone, not only volunteers.'),
        ('05', 'Respond', 'Feedback changes the next attempt.'),
        ('06', 'Transfer', 'Plan, retrieve, monitor, evaluate.'),
    ]
    y = 342
    for i, (num, head, body) in enumerate(steps):
        x = 58 + i * 147
        c.setFillColor(ORANGE if i in (1, 4) else OUTLINE); c.circle(x + 48, y, 24, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 9); c.drawCentredString(x + 48, y - 3, num)
        if i < len(steps)-1:
            c.setStrokeColor(LINE); c.setLineWidth(2); c.line(x + 74, y, x + 145, y)
        c.setFillColor(INK); c.setFont('BrandSerif', 17); c.drawCentredString(x + 48, 280, head)
        para(c, body, x, 246, 96, 88, pstyle('CycleBody', 'Helvetica', 10.5, 15, MUTED, TA_CENTER))
    para(c, 'Metacognition works best inside subject teaching: model how an expert plans, monitors and evaluates a real task.',
         165, 123, 630, 55, pstyle('CycleEvidence', 'Helvetica-Bold', 13, 20, TEAL, TA_CENTER))
    source_footer(c, 'Sources: Education Endowment Foundation guidance on metacognition/self-regulation and feedback.')
    c.showPage()
    add_meta(
        'Teach the route, not only the destination.', '6 min',
        'Translate high support into classroom moves with a strong evidence base.',
        'Keep this subject-specific. Model how to plan an essay, decode a source, set out a calculation or test an answer. Use checks that sample the whole class. Feedback should create a next action, and scaffolds should fade toward independence.',
        ask='“Which step is most likely to remain hidden for students who have less academic help outside school?”',
        watch='Avoid presenting the sequence as a rigid lesson script. It is a planning lens.',
        route='90/120 core. In 60, combine verbally with the expectations matrix.', sources=[SOURCES['eef_meta'], SOURCES['eef_feedback']])

    # 14 - studying versus looking busy
    n = len(SLIDES) + 1
    begin_slide(c, 'Study correctly · 01', 'Studying is not the same as learning.', slide_no=n)
    # One coherent transformation: recognition on the left, a deliberate
    # closed-page test in the centre, and evidence on the right.
    c.setFillColor(PALE_RED); c.roundRect(58, 128, 292, 244, 28, fill=1, stroke=0)
    draw_label(c, 'Familiarity', 84, 341, RED, 8, 1.35)
    para(c, '“I recognise it.”', 84, 300, 240, 55,
         pstyle('FamiliarityQuote', 'BrandSerifItalic', 25, 31, INK))
    para(c, 'Useful for orientation.<br/><b>Not yet proof of recall.</b>', 84, 245, 232, 58,
         pstyle('FamiliarityCopy', 'Helvetica', 12, 18, MUTED))
    familiar_actions = [('READ', 'again'), ('COPY', 'again'), ('WATCH', 'again')]
    for i, (verb, tail) in enumerate(familiar_actions):
        x = 84 + i * 78
        c.setFillColor(PAPER); c.roundRect(x, 155, 65, 48, 12, fill=1, stroke=0)
        c.setFillColor(RED); c.setFont('Helvetica-Bold', 8.3); c.drawCentredString(x + 32.5, 181, verb)
        c.setFillColor(MUTED); c.setFont('Helvetica', 7.4); c.drawCentredString(x + 32.5, 168, tail)

    c.setStrokeColor(OUTLINE); c.setLineWidth(2.2); c.line(350, 248, 390, 248)
    c.setFillColor(INK); c.roundRect(390, 194, 180, 108, 24, fill=1, stroke=0)
    draw_label(c, 'The test', 448, 274, ORANGE, 7.2, 1.15)
    para(c, 'Close the page.<br/><b>Produce.</b>', 412, 251, 136, 60,
         pstyle('CloseBook', 'BrandSerif', 18, 23, PAPER, TA_CENTER))
    c.setStrokeColor(OUTLINE); c.line(570, 248, 610, 248)

    c.setFillColor(PALE_GREEN); c.roundRect(610, 128, 292, 244, 28, fill=1, stroke=0)
    draw_label(c, 'Evidence', 636, 341, TEAL, 8, 1.35)
    para(c, '“I can produce it.”', 636, 300, 240, 55,
         pstyle('EvidenceQuote', 'BrandSerifItalic', 25, 31, INK))
    evidence_steps = [
        ('01', 'Retrieve', 'without notes', TEAL),
        ('02', 'Check', 'against a source', ORANGE),
        ('03', 'Repair', 'name the error', GREEN),
        ('04', 'Return', 'after a gap', PURPLE),
    ]
    c.setStrokeColor(HexColor('#AFC8BC')); c.setLineWidth(2.2); c.line(651, 184, 861, 184)
    for i, (num, head, body, accent) in enumerate(evidence_steps):
        cx = 650 + i * 70
        c.setFillColor(accent); c.circle(cx, 184, 12, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 6.1); c.drawCentredString(cx, 181.5, num)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 8); c.drawCentredString(cx, 154, head)
        para(c, body, cx - 31, 143, 62, 30,
             pstyle(f'EvidenceStep{i}', 'Helvetica', 6.8, 9.2, MUTED, TA_CENTER))
    para(c, '<b>Input can orient.</b> Evidence shows what survived when the page disappeared.',
         190, 91, 580, 28, pstyle('StudyTest', 'Helvetica', 11, 15, TEAL, TA_CENTER))
    source_footer(c, 'Evidence base: IES practice guide on retrieval, spacing and worked examples; EEF metacognition guidance.')
    c.showPage()
    add_meta(
        'Studying is not the same as learning.', '6 min',
        'Give staff and students a usable distinction between study activity and evidence of learning.',
        'Rereading, copying and watching may support orientation, but they do not by themselves test whether knowledge can be produced later. Teach a repeatable cycle: retrieve without notes, check accurately, repair the error, and revisit after a gap.',
        ask='“Which study behaviours do we praise because they look diligent, even when they produce little evidence of learning?”',
        watch='Do not tell students that all rereading or note-making is useless. The distinction is between input and proof of recall or application.',
        route='Core in 90/120. In 60, use the contrast and the closing sentence.', sources=[SOURCES['ies_study'], SOURCES['eef_meta']])

    # 15 - a complete study loop
    n = len(SLIDES) + 1
    begin_slide(c, 'Study correctly · 02', 'A study session needs an ending, not just a timer.', slide_no=n)
    draw_label(c, 'One practical shape', 72, 365, ORANGE, 7.8, 1.35)
    c.setFillColor(ORANGE); c.setFont('BrandSerif', 82); c.drawString(68, 255, '45')
    draw_label(c, 'Minutes', 78, 224, INK, 8.2, 1.5)
    para(c, 'The time can flex.<br/><b>The sequence cannot.</b>', 72, 190, 200, 65,
         pstyle('LoopAnchor', 'BrandSerif', 18, 23, INK))
    segments = [
        ('01', 'Target', 5, 'One clear thing to produce.', PALE_BLUE, TEAL),
        ('02', 'Retrieve', 15, 'Answer, solve or explain.', PALE_ORANGE, ORANGE),
        ('03', 'Check', 10, 'Use the model or scheme.', PALE_GREEN, GREEN),
        ('04', 'Repair', 10, 'Correct and name the error.', PALE_PURPLE, PURPLE),
        ('05', 'Schedule', 5, 'Choose what returns.', PALE_RED, RED),
    ]
    for i, (num, head, mins, body, fill, accent) in enumerate(segments):
        y = 326 - i * 52
        c.setFillColor(fill); c.roundRect(320, y, 570, 42, 13, fill=1, stroke=0)
        c.setFillColor(accent); c.circle(344, y + 21, 12, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 6.3); c.drawCentredString(344, y + 18.5, num)
        c.setFillColor(accent); c.setFont('Helvetica-Bold', 8.5); c.drawString(371, y + 24, f'{mins:02d} MIN')
        c.setFillColor(INK); c.setFont('BrandSerif', 15); c.drawString(445, y + 20, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 9.2); c.drawString(590, y + 18, body)
    para(c, 'Target → retrieve → check → repair → return.', 78, 91, 812, 30,
         pstyle('LoopNote', 'Helvetica-Bold', 11.5, 16, TEAL, TA_CENTER))
    source_footer(c, 'Practical template informed by IES retrieval/spacing guidance and Irish Department of Education study-routine guidance.')
    c.showPage()
    add_meta(
        'A study session needs an ending, not just a timer.', '7 min',
        'Turn “study more” into a teachable, observable routine.',
        'Present the timings as a flexible 45-minute template, not a validated dose. The important architecture is that every session starts with a target and ends with corrected evidence plus a scheduled revisit. A timer supports attention; it does not prove learning.',
        ask='Ask departments to replace the generic instruction “revise this topic” with a target, retrieval task, checking source and revisit date.',
        watch='Adapt duration and breaks for age, need and context. Preserve the learning cycle even when the block is shorter.',
        route='Core in 90/120; optional detail in 60.', sources=[SOURCES['ies_study'], SOURCES['gov_study']])

    # 16 - subject-specific study
    n = len(SLIDES) + 1
    begin_slide(c, 'Study correctly · 03', 'Good study changes with the subject.', slide_no=n)
    subject_cards = [
        ('Maths', 'Solve an unseen problem.', 'Proof: explain each step and repair the first wrong move.', PALE_BLUE, TEAL),
        ('Essay subjects', 'Retrieve the argument and evidence.', 'Proof: plan or write a paragraph without copying.', PALE_ORANGE, ORANGE),
        ('Languages', 'Produce words and sentences.', 'Proof: speak or write, then correct accurately.', PALE_PURPLE, PURPLE),
        ('Science', 'Explain a process and apply it.', 'Proof: draw from memory or answer an exam item.', PALE_GREEN, GREEN),
    ]
    positions = [(76, 250), (650, 250), (76, 116), (650, 116)]
    # Connect the disciplines to one central standard before drawing the
    # nodes, so the page reads as one system rather than four unrelated cards.
    c.setStrokeColor(LINE); c.setLineWidth(2.4)
    for x, y in positions:
        edge_x = x + 218 if x < 480 else x
        c.line(480, 244, edge_x, y + 61)
    round_box(c, 330, 185, 300, 120, PAPER, OUTLINE, 26, 1.4, True)
    draw_label(c, 'The shared standard', 390, 270, ORANGE, 7.4, 1.2)
    para(c, '<b>Can the student perform<br/>without the notes?</b>', 350, 244, 260, 62,
         pstyle('SubjectHub', 'BrandSerif', 17.5, 22, INK, TA_CENTER))
    for i, ((head, do, proof, fill, accent), (x, y)) in enumerate(zip(subject_cards, positions)):
        round_box(c, x, y, 218, 122, fill, OUTLINE, 18, 1.1, True)
        c.setFillColor(accent); c.circle(x + 28, y + 94, 14, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 7.2); c.drawCentredString(x + 28, y + 91.5, str(i + 1).zfill(2))
        c.setFillColor(INK); c.setFont('BrandSerif', 17); c.drawString(x + 51, y + 88, head)
        para(c, f'<b>{do}</b>', x + 20, y + 62, 178, 36,
             pstyle(f'SubjectDo{i}', 'Helvetica', 9.5, 13, INK))
        para(c, proof, x + 20, y + 32, 178, 34,
             pstyle(f'SubjectProof{i}', 'Helvetica', 8.5, 11.5, MUTED))
    c.setFillColor(TEAL); c.roundRect(217, 63, 526, 33, 11, fill=1, stroke=0)
    para(c, '<b>The method must meet the material.</b> Model it on real subject tasks.', 239, 86, 482, 20,
         pstyle('SubjectStudyLine', 'Helvetica', 10.1, 14, PAPER, TA_CENTER))
    source_footer(c, 'Practice synthesis: retrieval, worked examples, feedback and metacognitive modelling should remain subject-specific.')
    c.showPage()
    add_meta(
        'Good study changes with the subject.', '7 min',
        'Prevent generic study-skills advice from becoming detached from the actual demands of subjects.',
        'Students need teachers to demonstrate what retrieval, checking and repair look like in their discipline. Use real tasks, real criteria and real examples. The same cycle applies across subjects, but the evidence of learning differs.',
        ask='Invite each department to write one “proof of learning” task students can do without notes.',
        watch='Avoid turning study skills into another standalone booklet students must decode alone.',
        route='90/120 core; optional in 60.', sources=[SOURCES['ies_study'], SOURCES['eef_meta'], SOURCES['eef_feedback']])

    # 17 - equitable study conditions
    n = len(SLIDES) + 1
    begin_slide(c, 'Study correctly · 04', 'Do not make success depend on a quiet bedroom.', slide_no=n)
    blob(c, 212, 250, 157, 129, PALE_ORANGE, -4)
    draw_label(c, 'The equity test', 78, 361, ORANGE, 7.8, 1.3)
    para(c, 'Could the student use this method <b>without</b> private tuition, their own device or an expert adult at home?',
         88, 321, 245, 148, pstyle('EquityStudy', 'BrandSerif', 19.5, 27, INK))
    draw_icon(c, assets / 'study' / 'study-session.png', 284, 302, 92, 92)
    c.setFillColor(TEAL); c.roundRect(90, 117, 240, 37, 12, fill=1, stroke=0)
    para(c, '<b>Access is part of pedagogy.</b>', 108, 141, 204, 22,
         pstyle('AccessPedagogy', 'Helvetica', 10.1, 14, PAPER, TA_CENTER))

    draw_label(c, 'What school can make dependable', 430, 380, TEAL, 7.8, 1.3)
    supports = [
        ('01', 'A predictable, supervised study slot', PALE_BLUE, TEAL),
        ('02', 'Device, print, books and mark-scheme access', PALE_ORANGE, ORANGE),
        ('03', 'A modelled routine using real subject work', PALE_GREEN, GREEN),
        ('04', 'A low-noise place to retrieve and practise', PALE_PURPLE, PURPLE),
        ('05', 'Rapid feedback and one visible next step', PALE_RED, RED),
    ]
    support_positions = [(430, 268, 218, 87), (668, 268, 218, 87),
                         (430, 167, 218, 87), (668, 167, 218, 87),
                         (430, 92, 456, 58)]
    for (num, text_item, fill, accent), (x, y, w, h) in zip(supports, support_positions):
        round_box(c, x, y, w, h, fill, OUTLINE, 15, 1.0, True)
        c.setFillColor(accent); c.circle(x + 28, y + h - 26, 13, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 6.8); c.drawCentredString(x + 28, y + h - 28.5, num)
        para(c, text_item, x + 51, y + h - 19, w - 69, h - 24,
             pstyle(f'EquitySupport{num}', 'Helvetica-Bold', 9.4 if h > 60 else 10.3,
                    13.1 if h > 60 else 14, INK))
    source_footer(c, 'Equity principle: teach and resource the routine in school; do not assume ideal study conditions at home.')
    c.showPage()
    add_meta(
        'Do not make success depend on a quiet bedroom.', '6 min',
        'Connect effective study practice to equitable access and whole-school provision.',
        'Students cannot consistently use a method they have never seen modelled, cannot resource or cannot find a place to practise. Schools cannot remove every home constraint, but they can reduce how much successful study depends on resources and expert help outside school.',
        ask='“Which part of our current study advice silently assumes money, space, technology or an academically confident adult at home?”',
        watch='Do not stereotype home environments. Audit the demands created by school routines rather than guessing about individual families.',
        route='Core in every version.', sources=[SOURCES['gov_study'], SOURCES['oecd_disadvantage']])

    # 18 - trauma-aware boundaries
    n = len(SLIDES) + 1
    begin_slide(c, 'Trauma-aware, role-clear', 'Care without lowering the ceiling.', slide_no=n)
    para(c, 'Respond to what is observable. Refer what is not ours to assess.', 120, 395, 720, 32,
         pstyle('TraumaPosition', 'BrandSerifItalic', 18, 23, INK, TA_CENTER))

    c.setFillColor(PALE_GREEN); c.roundRect(55, 105, 408, 262, 26, fill=1, stroke=0)
    draw_label(c, 'Stability we can design', 82, 337, TEAL, 7.8, 1.22)
    para(c, '<b>Dignity and challenge,<br/>held together.</b>', 82, 304, 330, 58,
         pstyle('DesignStability', 'BrandSerif', 20, 25, INK))
    good = [
        ('Predictability', 'routines and transitions'),
        ('Choice', 'within clear boundaries'),
        ('Regulate', 'before reasoning'),
        ('Return', 'a dignified route back'),
        ('Refer', 'through the support system'),
    ]
    for i, (head, body) in enumerate(good):
        y = 238 - i * 30
        c.setFillColor(TEAL); c.circle(86, y + 9, 8, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 5.4); c.drawCentredString(86, y + 7, str(i + 1).zfill(2))
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 9.6); c.drawString(104, y + 6, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 8.8); c.drawString(202, y + 6, body)

    c.setFillColor(PALE_RED); c.roundRect(497, 105, 408, 262, 26, fill=1, stroke=0)
    draw_label(c, 'Lines we do not cross', 524, 337, RED, 7.8, 1.22)
    para(c, 'Support the behaviour.<br/><b>Do not invent the history.</b>', 524, 304, 330, 58,
         pstyle('TraumaBoundaryLead', 'BrandSerif', 20, 25, INK))
    boundary_rows = [
        ('ACE scores', 'do not collect or display'),
        ('Diagnosis', 'do not infer from behaviour'),
        ('Disclosure', 'do not demand a private story'),
        ('Boundaries', 'do not remove accountability'),
        ('Specialist care', 'do not attempt to replace it'),
    ]
    for i, (head, body) in enumerate(boundary_rows):
        y = 238 - i * 30
        c.setStrokeColor(RED); c.setLineWidth(2.4); c.line(528, y + 9, 542, y + 9)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 9.4); c.drawString(556, y + 6, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 8.5); c.drawString(650, y + 6, body)
    para(c, '<b>Notice → support → refer.</b> Keep the student’s privacy, dignity and future options intact.',
         160, 83, 640, 25, pstyle('TraumaSequence', 'Helvetica', 10.5, 15, TEAL, TA_CENTER))
    source_footer(c, 'Sources: NEPS trauma resources and Continuum of Support; systematic review evidence; UK government caution on ACE screening.')
    c.showPage()
    add_meta(
        'Care without lowering the ceiling.', '8 min',
        'Give staff a safe, evidence-calibrated role in trauma-sensitive schooling.',
        'Say directly: teachers should be trauma-aware, not trauma-detectives. NEPS focuses on stress, resilience and a continuum of universal, targeted and individual support. School-wide trauma-informed evidence remains emergent and variable; use sensible practices without making inflated claims. ACE questionnaires are population research tools and should not substitute for comprehensive assessment or gate access to support.',
        ask='“Which routine can increase predictability tomorrow without asking any student to disclose?”',
        watch='Remind staff to follow safeguarding procedures for disclosures and immediate risks; do not investigate in the room.',
        route='Core in every version. In 120, give 3 minutes to identify one predictable routine and one referral boundary.', sources=[SOURCES['neps_resources'], SOURCES['neps_service'], SOURCES['trauma_review'], SOURCES['ace_caution']])

    # 15 - attendance response
    n = len(SLIDES) + 1
    begin_slide(c, 'Promise 03 · Present', '20 days is a reporting threshold. Support starts sooner.', slide_no=n)
    steps = [('Notice', 'Pattern, change, context'), ('Ask', 'Student + family voice'), ('Map', 'Barrier, strength, support'), ('Act', 'Small, specific response'), ('Review', 'Did access improve?')]
    for i, (head, body) in enumerate(steps):
        x = 70 + i * 178
        if i < len(steps)-1:
            c.setStrokeColor(LINE); c.setLineWidth(4); c.line(x + 55, 280, x + 176, 280)
        c.setFillColor([PALE_BLUE, PALE_ORANGE, PALE_GREEN, PALE_PURPLE, PALE_RED][i]); c.circle(x + 40, 280, 39, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 10); c.drawCentredString(x + 40, 276, str(i+1).zfill(2))
        c.setFillColor(INK); c.setFont('BrandSerif', 18); c.drawCentredString(x + 40, 210, head)
        para(c, body, x - 18, 183, 116, 64, pstyle('AttendStep', 'Helvetica', 10.5, 15, MUTED, TA_CENTER))
    para(c, 'Use days missed, not only percentages. Be specific. Stay curious about the cause.', 145, 105, 670, 40,
         pstyle('AttendLine', 'Helvetica-Bold', 13, 20, TEAL, TA_CENTER))
    source_footer(c, 'Sources: Tusla absenteeism guidance and Educational Welfare Services; EEF attendance evidence review.')
    c.showPage()
    add_meta(
        '20 days is a reporting threshold. Support starts sooner.', '7 min',
        'Shift attendance from late-stage compliance to early, barrier-responsive support.',
        'Clarify the distinction: Irish schools report students absent 20 days or more, but Tusla also stresses early response. Start with a pattern, seek the student and family perspective, identify the barrier, agree a small response, and review. Escalate through the school’s support structures and TESS when in-school efforts are insufficient.',
        ask='“At what point does a human conversation happen in our current process?”',
        watch='Exclude bereavement, long-term illness and known sensitive circumstances from automated or shaming messages.',
        route='Core. In 120, teams map their current attendance response against the five steps.', sources=[SOURCES['tusla_reporting'], SOURCES['tusla_ews'], SOURCES['eef_attendance']])

    # 16 - family partnership
    n = len(SLIDES) + 1
    begin_slide(c, 'Promise 04 · Partnered', 'Partnership is designed before it is declared.', slide_no=n)
    habits = [('Specific', 'days · patterns · next step'), ('Curious', 'ask before interpreting'), ('Strength-first', 'name what the child can do'), ('Accessible', 'person · language · channel · time'), ('Reliable', 'do what was agreed · report back')]
    habit_fills = [PALE_BLUE, PALE_ORANGE, HexColor('#F2E2C6'), PALE_PURPLE, PALE_RED]
    habit_accents = [TEAL, ORANGE, OCHRE, PURPLE, RED]
    for i, ((head, body), fill, accent) in enumerate(zip(habits, habit_fills, habit_accents)):
        x = 58 + i * 23
        y = 327 - i * 51
        w = 360 - i * 18
        round_box(c, x, y, w, 47, fill, OUTLINE, 13, 0.9, True)
        c.setFillColor(accent); c.circle(x + 24, y + 23.5, 12, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 6.6); c.drawCentredString(x + 24, y + 21, str(i + 1).zfill(2))
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 11.1); c.drawString(x + 46, y + 27, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 8.7); c.drawString(x + 46, y + 12, body)
    draw_label(c, 'Five habits that make contact reachable', 59, 386, TEAL, 7.5, 1.1)
    round_box(c, 520, 103, 375, 285, PAPER, OUTLINE, 20, 1.4, True)
    draw_label(c, 'A stronger first contact', 548, 344, ORANGE, 8, 1.2)
    para(c, '“We have missed Sam on seven mornings. Sam’s oral answers in Science are strong. Is transport, sleep, caring, anxiety - or something else - making mornings harder?”',
         548, 309, 320, 130, pstyle('FamilyQuote', 'BrandSerifItalic', 17, 24, INK))
    para(c, '“Can we agree one step and check in on Friday?”', 548, 172, 320, 45,
         pstyle('FamilyNext', 'Helvetica-Bold', 12.5, 18, TEAL))
    source_footer(c, 'Practice synthesis informed by attendance evidence, HSCL/DEIS principles and responsive family engagement.')
    c.showPage()
    add_meta(
        'Partnership is designed before it is declared.', '6 min',
        'Make family engagement concrete and reduce deficit assumptions about non-response.',
        'Contrast generic warnings with specific, strength-based, curious contact. Make the next step small and mutual. Accessibility includes channel, timing, literacy, language, previous school experiences and whether the family can reach a real person.',
        ask='Invite participants to rewrite one common message using the five habits.',
        watch='Do not promise confidentiality beyond safeguarding duties or supports the school cannot deliver.',
        route='90/120 core. In 60, show the example and move on.', sources=[SOURCES['oecd_disadvantage'], SOURCES['eef_attendance']])

    # 17 - futures
    n = len(SLIDES) + 1
    begin_slide(c, 'Promise 05 · Future-ready', 'A pathway is only real when a student can navigate it.', slide_no=n)
    # branching lines first
    c.setStrokeColor(OUTLINE); c.setLineWidth(2.2)
    c.line(197, 280, 337, 280); c.line(337, 280, 424, 356); c.line(337, 280, 424, 280); c.line(337, 280, 424, 204)
    blob(c, 197, 280, 62, 60, PALE_ORANGE, 4)
    c.setFillColor(INK); c.setFont('BrandSerif', 18); c.drawCentredString(197, 276, 'Aspiration')
    routes = [
        (444, 326, PALE_BLUE, 'Route A', 'CAO / higher education'),
        (444, 250, PALE_GREEN, 'Route B', 'FET, PLC, tertiary, access'),
        (444, 174, PALE_PURPLE, 'Route C', 'Apprenticeship or work + training'),
    ]
    for x, y, fill, tag, body in routes:
        c.setFillColor(fill); c.setStrokeColor(OUTLINE); c.setLineWidth(1.2); c.roundRect(x, y, 330, 62, 16, fill=1, stroke=1)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 10); c.drawString(x+18, y+38, tag)
        body_size = 14.5 if tag == 'Route C' else 16
        c.setFont('BrandSerif', body_size); c.drawString(x+18, y+16, body)
    c.setFillColor(INK); c.roundRect(118, 82, 724, 45, 14, fill=1, stroke=0)
    para(c, '<b>Each route needs</b>  ·  entry requirements  ·  deadlines  ·  cost/funding  ·  a named adult  ·  family understanding  ·  a next action',
         143, 111, 674, 28, pstyle('RouteNeeds', 'Helvetica', 9.7, 14, PAPER, TA_CENTER))
    source_footer(c, 'Sources: DFHERIS pathways overview; HEAR; SUSI; Government of Ireland apprenticeship information.')
    c.showPage()
    add_meta(
        'A pathway is only real when a student can navigate it.', '8 min',
        'Give every route status and convert aspiration into practical navigation.',
        'The CAO points route is one route among many. FET/PLC, tertiary programmes, access/foundation routes, apprenticeships and work-plus-training can lead to meaningful qualifications and careers. Apprenticeships span more than 80 types and NFQ Levels 5-10; at least half the learning is on the job. HEAR, DARE where relevant, and SUSI require early, accurate support and deadlines.',
        ask='“Does every fifth-year student have a plausible A, B and C - and know the next action on each?”',
        watch='Do not create a hierarchy where Route B or C is quietly presented as a fallback for “weaker” students.',
        route='Core. In 120, participants map routes for the student they held in mind.', sources=[SOURCES['pathways'], SOURCES['hear'], SOURCES['susi'], SOURCES['apprenticeship']])

    # 18 - case workshop
    n = len(SLIDES) + 1
    begin_slide(c, 'Case lab · composite scenario', 'Leah is capable. School is becoming harder to reach.', slide_no=n)
    round_box(c, 58, 102, 405, 285, PAPER, OUTLINE, 18, 1.4, True)
    draw_label(c, 'Leah · Fifth Year', 84, 353, ORANGE, 8, 1.2)
    case = ('Strong oral contributions. Written work is inconsistent. Sixteen days absent by February and often late. '
            'She helps care for younger siblings. She says she wants physiotherapy, then adds: “Courses like that are for people with money.”')
    para(c, case, 84, 319, 350, 180, pstyle('CaseText', 'BrandSerif', 17.5, 25, INK))
    draw_label(c, 'In groups', 508, 383, TEAL, 8, 1.2)
    prompts = [
        ('What might the school wrongly infer?', PALE_BLUE, TEAL),
        ('What do we need to learn from Leah and home?', PALE_ORANGE, ORANGE),
        ('What changes tomorrow, this term and this year?', PALE_GREEN, GREEN),
        ('Who owns each next step?', PALE_PURPLE, PURPLE),
    ]
    prompt_positions = [(508, 245), (711, 245), (508, 112), (711, 112)]
    for i, ((item, fill, accent), (x, y)) in enumerate(zip(prompts, prompt_positions)):
        round_box(c, x, y, 178, 111, fill, OUTLINE, 16, 1.0, True)
        c.setFillColor(accent); c.circle(x + 27, y + 82, 14, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 7); c.drawCentredString(x + 27, y + 79.5, str(i + 1).zfill(2))
        para(c, item, x + 20, y + 65, 138, 58,
             pstyle(f'CasePrompt{i}', 'Helvetica-Bold', 10.1, 14.1, INK))
    source_footer(c, 'Fictional composite for discussion. Do not diagnose, and do not share identifiable student cases.')
    c.showPage()
    add_meta(
        'Leah is capable. School is becoming harder to reach.', '10-15 min',
        'Let participants apply the five promises to a complex, non-diagnostic scenario.',
        'State clearly that Leah is a fictional composite. Groups should separate what is known from what is assumed; identify questions for Leah and family; plan immediate, term and progression actions; and name ownership. Ask them to preserve both dignity and academic ambition.',
        ask='Use the four on-screen prompts. Ask for one action per promise, not a long list.',
        watch='Do not let the group diagnose anxiety, trauma, neglect or a learning difficulty. Caring responsibility is context, not a complete explanation.',
        route='90 min: 8 minutes work + 4 debrief. 120: 15 + 8. 60: omit and use the next slide as a worked example.', sources=[])

    # 19 - case debrief
    n = len(SLIDES) + 1
    begin_slide(c, 'One plausible response - not a prescription', 'Coordinate the supports around the student.', slide_no=n)
    responses = [
        ('Known', 'Named check-in; ask Leah what is changing and what helps.'),
        ('Taught', 'Model written responses; prioritised catch-up after absence.'),
        ('Present', 'Map caring/morning barriers; agree a small plan; review weekly.'),
        ('Partnered', 'Strength-first family conversation; practical constraints first.'),
        ('Future-ready', 'Physio Route A; related FET/tertiary Route B; funding + HEAR check.'),
    ]
    fills = [PALE_BLUE, PALE_ORANGE, PALE_GREEN, PALE_PURPLE, PALE_RED]
    accents = [TEAL, ORANGE, GREEN, PURPLE, RED]
    positions = [
        (54, 258, 402, 120),
        (504, 258, 402, 120),
        (54, 119, 264, 111),
        (348, 119, 264, 111),
        (642, 119, 264, 111),
    ]
    for i, ((head, body), fill, accent, (x, y, w, h)) in enumerate(zip(responses, fills, accents, positions)):
        round_box(c, x, y, w, h, fill, OUTLINE, 17, 1.1, True)
        c.setFillColor(accent); c.circle(x + 28, y + h - 29, 14, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 7.3); c.drawCentredString(x + 28, y + h - 31.5, str(i + 1).zfill(2))
        c.setFillColor(INK); c.setFont('BrandSerif', 17 if i < 2 else 15.5); c.drawString(x + 53, y + h - 35, head)
        para(c, body, x + 22, y + h - 58, w - 44, h - 62,
             pstyle(f'CaseAnswer{i}', 'Helvetica', 10.3 if i < 2 else 9.3, 14.5 if i < 2 else 13.2, INK))
    c.setFillColor(TEAL); c.roundRect(128, 63, 704, 34, 11, fill=1, stroke=0)
    para(c, '<b>Shared · sequenced · reviewed.</b> One owner, one next step, one date to learn.',
         150, 86, 660, 20, pstyle('Coordination', 'Helvetica', 10.4, 14, PAPER, TA_CENTER))
    c.showPage()
    add_meta(
        'Coordinate the supports around the student.', '5 min',
        'Model a coherent response and show that no single role should carry the whole case.',
        'Present this as one plausible response after listening, not a checklist to impose. The key is sequence and ownership: immediate relationship and learning access; barrier-responsive attendance; family partnership; longer-term route planning; and review through the student support structure.',
        ask='“What would Leah experience differently by next Monday?”',
        watch='Avoid over-promising access to a specific course or support before checking eligibility and current requirements.',
        route='Core after case. In 60, use this slide to explain the case in 3 minutes.', sources=[SOURCES['student_support'], SOURCES['hear'], SOURCES['susi']])

    # 20 - diagnostic
    n = len(SLIDES) + 1
    begin_slide(c, 'Whole-school reality check', 'How dependable are the five promises?', slide_no=n)
    questions = [
        ('Known', 'Can every student name an adult who will notice?'),
        ('Taught', 'Does support preserve challenge and future options?'),
        ('Present', 'Are patterns acted on before 20 days?'),
        ('Partnered', 'Can families reach a person, not only a portal?'),
        ('Future-ready', 'Does every student have A, B and C routes?'),
    ]
    fills = [PALE_BLUE, PALE_ORANGE, PALE_GREEN, PALE_PURPLE, PALE_RED]
    accents = [TEAL, ORANGE, GREEN, PURPLE, RED]
    for i, ((head, q), fill, accent) in enumerate(zip(questions, fills, accents)):
        x = 54 + i * 176
        round_box(c, x, 117, 160, 263, fill, OUTLINE, 18, 1.1, True)
        c.setFillColor(accent); c.circle(x + 28, 345, 15, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 7.2); c.drawCentredString(x + 28, 342.5, str(i + 1).zfill(2))
        c.setFillColor(INK); c.setFont('BrandSerif', 16.5 if head != 'Future-ready' else 14.3); c.drawString(x + 21, 302, head)
        para(c, q, x + 21, 273, 118, 105,
             pstyle(f'DiagnosticQ{i}', 'Helvetica', 10.1, 14.3, INK))
        c.setStrokeColor(PAPER); c.setLineWidth(2)
        c.line(x + 24, 183, x + 136, 183)
        c.setStrokeColor(accent); c.setLineWidth(1.1)
        for j in range(4):
            c.circle(x + 31 + j * 32, 151, 9, fill=0, stroke=1)
        c.setFillColor(MUTED); c.setFont('Helvetica', 6.5); c.drawString(x + 21, 128, '1 · rarely')
        c.drawRightString(x + 139, 128, '4 · dependable')
    c.setFillColor(INK); c.roundRect(225, 63, 510, 34, 11, fill=1, stroke=0)
    para(c, '<b>Rate the system.</b> Then listen for where students and families would score it differently.', 246, 86, 468, 20,
         pstyle('RateSystem', 'Helvetica', 10.3, 14, PAPER, TA_CENTER))
    source_footer(c, 'A low score is a planning signal, not a verdict. Do not rank individual staff or students.')
    c.showPage()
    add_meta(
        'How dependable are the five promises?', '6 min',
        'Turn broad values into an honest baseline for whole-school planning.',
        'Participants rate each promise from 1 (person-dependent or inconsistent) to 4 (systematic, visible and reviewed). Ask them to rate the student experience, not the existence of a policy. Their lowest score is not automatically the priority; they should consider urgency, reach and feasibility.',
        ask='Silent rating first, then compare at tables. Ask: “Where would students and families rate us differently?”',
        watch='Avoid public ranking of departments or individual staff.',
        route='Core in 90/120. In 60, complete silently and select one promise.', sources=[SOURCES['deis_strategy'], SOURCES['oecd_disadvantage']])

    # 21 - action plan
    n = len(SLIDES) + 1
    begin_slide(c, 'From intention to implementation', 'One 90-day test beats a 30-page aspiration.', slide_no=n)
    fields = [
        ('Promise', 'Which student experience will become more dependable?'),
        ('Focus', 'For whom, where and when is the gap most visible?'),
        ('Routine', 'What will adults do differently and how often?'),
        ('Owner', 'Who coordinates, supports and follows through?'),
        ('Early signal', 'What should move before outcomes move?'),
        ('Review', 'What date will the team learn and adapt?'),
    ]
    y = 360
    for i, (head, prompt) in enumerate(fields):
        c.setFillColor(ORANGE if i in (0,5) else LABEL); c.setFont('Helvetica-Bold', 10); c.drawString(74, y, head.upper())
        c.setFillColor(INK); c.setFont('BrandSerif', 15); c.drawString(200, y-1, prompt)
        draw_rule(c, 200, y-14, 882, LINE, 1)
        y -= 51
    para(c, 'Small enough to implement. Important enough to matter. Specific enough to learn from.',
         170, 65, 620, 35, pstyle('PlanLine', 'Helvetica-Bold', 12, 18, TEAL, TA_CENTER))
    source_footer(c, 'Planning structure aligned with implementation guidance and DEIS whole-school planning.')
    c.showPage()
    add_meta(
        'One 90-day test beats a 30-page aspiration.', '12-20 min',
        'Produce a concrete whole-school output before participants leave.',
        'Teams select one promise and define a focused 90-day test: target experience, student group/context, adult routine, owner, early indicator and review date. Encourage a practice change people can observe, not a slogan or a new form.',
        ask='Ask each team to read its plan aloud in one sentence: “For [group/context], we will [routine], led by [owner], and by [date] we expect [early signal].”',
        watch='Prevent plans that depend entirely on one enthusiastic person, collect sensitive trauma data, or wait a year to learn whether implementation happened.',
        route='60: 8 min individual draft. 90: 15 min teams. 120: 25 min with peer critique.', sources=[SOURCES['deis_strategy'], SOURCES['oecd_disadvantage']])

    # 22 - measures
    n = len(SLIDES) + 1
    begin_slide(c, 'Measure the change you can see early', 'Track access before outcomes arrive.', slide_no=n)
    lead = ['students with a named adult', 'timely check-ins after emerging absence', 'family contacts that end with an agreed step', 'students with three mapped pathways', 'staff using the agreed teaching routine']
    lag = ['attendance and punctuality', 'engagement and belonging', 'attainment and subject-level access', 'retention to Leaving Certificate', 'progression to HE, FET, apprenticeship or work']
    draw_label(c, 'What we can see in weeks', 72, 389, ORANGE, 8, 1.2)
    draw_label(c, 'What we hope to shift over time', 558, 389, TEAL, 8, 1.2)
    c.setFillColor(SOFT); c.roundRect(420, 360, 120, 27, 10, fill=1, stroke=0)
    c.setFillColor(MUTED); c.setFont('Helvetica-Bold', 6.6); c.drawCentredString(480, 370, 'CAN INFLUENCE')
    row_accents = [TEAL, ORANGE, GREEN, PURPLE, RED]
    for i, (early, later, accent) in enumerate(zip(lead, lag, row_accents)):
        y = 320 - i * 50
        if i:
            draw_rule(c, 72, y + 43, 888, LINE, .65)
        c.setFillColor(accent); c.circle(84, y + 19, 10, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 6.1); c.drawCentredString(84, y + 16.6, str(i + 1).zfill(2))
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 9.5); c.drawString(106, y + 15.5, early)
        c.setStrokeColor(accent); c.setLineWidth(1.4); c.line(414, y + 19, 516, y + 19)
        c.setFillColor(accent); c.setFont('Helvetica-Bold', 10); c.drawString(510, y + 15, '›')
        c.setFillColor(accent); c.circle(548, y + 19, 5, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont('Helvetica', 9.6); c.drawString(568, y + 15.5, later)
    c.setFillColor(PALE_RED); c.roundRect(213, 53, 534, 35, 11, fill=1, stroke=0)
    para(c, '<b>Privacy boundary:</b> measure support and access - never a student’s private trauma history.', 234, 80, 492, 20,
         pstyle('MeasureBoundary', 'Helvetica', 10, 14, RED, TA_CENTER))
    source_footer(c, 'Pair early implementation signals with longer-term outcomes. Review for learning, not surveillance.')
    c.showPage()
    add_meta(
        'Track access before outcomes arrive.', '5 min',
        'Give leaders useful implementation indicators and a privacy boundary.',
        'Lagging outcomes matter, but they move slowly and reflect many factors. Pair them with leading signals that show whether the promised experience is becoming dependable. Data should support learning and coordination, not surveillance or labelling.',
        ask='“Which early signal would tell us within four weeks that the routine is actually happening?”',
        watch='Do not collect ACE counts, diagnostic guesses or identifiable narratives for programme measurement.',
        route='Core in 90/120; optional in 60 if time is tight.', sources=[SOURCES['deis_strategy'], SOURCES['neps_service']])

    # 23 - stop start protect
    n = len(SLIDES) + 1
    begin_slide(c, 'A disciplined commitment', 'Stop. Start. Protect.', dark=True, slide_no=n)
    cols = [
        ('STOP', 'One routine or phrase that quietly closes a door.', RED),
        ('START', 'One action the school will test for 90 days.', ORANGE),
        ('PROTECT', 'One strength already changing students’ odds.', TEAL),
    ]
    for i, (head, body, col) in enumerate(cols):
        x = 58 + i*300
        c.setFillColor(col); c.rect(x, 364, 220, 7, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('BrandSerif', 26); c.drawString(x, 316, head)
        para(c, body, x, 270, 220, 95, pstyle('CommitBody', 'Helvetica', 13, 20, HexColor('#D6D0C9')))
        c.setStrokeColor(HexColor('#6F6963')); c.setLineWidth(1); c.line(x, 138, x+220, 138)
        c.line(x, 108, x+220, 108)
    source_footer(c, 'Write privately first. Share the action, not a confession.', True)
    c.showPage()
    add_meta(
        'Stop. Start. Protect.', '6 min',
        'End planning with focus: remove harm, add one practice, and retain what already works.',
        'Give two quiet minutes. Invite table-level sharing, then ask leaders to collect only actions people are comfortable making public. “Protect” matters because reform that ignores existing strengths can damage trust and capacity.',
        ask='Ask for one sentence from each group, prioritising “Start” and “Protect.”',
        watch='Do not turn “Stop” into public blame or a list of individual failings.',
        route='Core in 90/120. In 60, use as the closing commitment.', sources=[])

    # 24 - by Friday
    n = len(SLIDES) + 1
    begin_slide(c, 'Take it back Monday', 'Five moves by Friday.', slide_no=n)
    moves = [
        ('01', 'Name', 'the students at the edge - and the adult who will notice.'),
        ('02', 'Contact', 'one family with a strength before the concern.'),
        ('03', 'Audit', 'one task for hidden vocabulary, steps or assumed support.'),
        ('04', 'Map', 'A, B and C routes with one student.'),
        ('05', 'Schedule', 'the 90-day review before momentum fades.'),
    ]
    y = 370
    for num, verb, body in moves:
        c.setFillColor(ORANGE); c.setFont('Helvetica-Bold', 10); c.drawString(70, y, num)
        c.setFillColor(INK); c.setFont('BrandSerif', 18); c.drawString(116, y-3, verb)
        c.setFillColor(MUTED); c.setFont('Helvetica', 13); c.drawString(250, y-2, body)
        draw_rule(c, 70, y-18, 888, LINE, 0.8)
        y -= 59
    para(c, 'Momentum is a design choice.', 330, 58, 300, 30,
         pstyle('Momentum', 'BrandSerifItalic', 16, 21, TEAL, TA_CENTER))
    c.showPage()
    add_meta(
        'Five moves by Friday.', '3 min',
        'Convert workshop energy into immediate action without adding a new programme.',
        'Read the five moves. Ask participants to circle one in the workbook and name when it will happen. The actions deliberately span relationship, family, teaching, progression and implementation.',
        ask='“Which one will be visible in your calendar before you leave?”',
        watch='Encourage one completed action, not five vague intentions.',
        route='Core in every version.', sources=[])

    # App implementation - every screen below is a live Demo Account capture.
    n = len(SLIDES) + 1
    begin_slide(c, 'From workshop to student routine', 'The app should strengthen a human support system.', slide_no=n)
    draw_screen(c, live / '01-home.png', 48, 68, 520, 320, 8, True, 20)
    round_box(c, 602, 68, 308, 320, PAPER, OUTLINE, 20, 1.2, True)
    draw_label(c, 'Five dependable experiences', 626, 358, ORANGE, 7.2, 1.1)
    ecosystem = [
        ('Modules', 'TEACH', 'make methods explicit', PALE_GREEN, GREEN),
        ('Launchpad', 'CHOOSE', 'match tool to need', PALE_ORANGE, ORANGE),
        ('My Progress', 'NOTICE', 'see patterns over time', PALE_BLUE, TEAL),
        ('Learning Paths', 'SEQUENCE', 'make the next step clear', PALE_PURPLE, PURPLE),
        ('My Journey', 'BELONG', 'turn growth into a place', PALE_RED, RED),
    ]
    for i, (head, verb, body, fill, accent) in enumerate(ecosystem):
        y = 301 - i * 46
        c.setFillColor(fill); c.roundRect(624, y, 264, 39, 11, fill=1, stroke=0)
        c.setFillColor(accent); c.roundRect(635, y + 8, 55, 23, 8, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 6.4); c.drawCentredString(662.5, y + 16.5, verb)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 9.1); c.drawString(704, y + 22, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 7.5); c.drawString(704, y + 9, body)
    source_footer(c, 'Live Demo Account capture · Home · 16 August 2026. The app supports the routine; relationships, teaching and judgement remain human.')
    c.showPage()
    add_meta(
        'The app should strengthen a human support system.', '4 min',
        'Show the real student home and connect each destination to a dependable school experience.',
        'The home screen gives one coherent route into teaching, tool choice, progress review, guided sequencing and belonging. Use it to reinforce routines that already involve adults; do not position the product as a substitute for a trusted relationship.',
        ask='“Where could one of these experiences strengthen an adult conversation already happening in school?”',
        watch='Do not hand a vulnerable student a menu and call that support. Pair access with orientation and follow-up.',
        route='Use near the close in 90/120. In 60, show this overview plus the progress slide.', sources=[])

    n = len(SLIDES) + 1
    begin_slide(c, 'Facilitate growth · Teach', 'Teach the method before asking for independence.', slide_no=n)
    draw_screen_crop(c, live / '02-modules.png', 48, 76, 564, 312, (0, 0, 1, .76), 8, True, 20)
    round_box(c, 646, 76, 264, 312, PAPER, OUTLINE, 20, 1.2, True)
    draw_label(c, 'Transfer needs adult action', 670, 358, GREEN, 7.1, 1.05)
    module_moves = [
        ('01', 'Explain', 'teach one strategy explicitly', PALE_BLUE, TEAL),
        ('02', 'Model', 'use real subject content', PALE_ORANGE, ORANGE),
        ('03', 'Choose', 'name when and why it fits', PALE_GREEN, GREEN),
        ('04', 'Fade', 'revisit until support can reduce', PALE_PURPLE, PURPLE),
    ]
    for i, (num, head, body, fill, accent) in enumerate(module_moves):
        y = 291 - i * 52
        c.setFillColor(fill); c.roundRect(668, y, 220, 43, 12, fill=1, stroke=0)
        c.setFillColor(accent); c.circle(687, y + 21.5, 9, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 5.6); c.drawCentredString(687, y + 19, num)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 9.1); c.drawString(706, y + 24, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 7.5); c.drawString(706, y + 10, body)
    c.setFillColor(INK); c.roundRect(668, 88, 220, 31, 10, fill=1, stroke=0)
    para(c, '<b>Completion starts transfer;</b> it does not prove it.', 684, 109, 188, 18,
         pstyle('ModuleLiveBoundary', 'Helvetica', 8.3, 11.5, PAPER, TA_CENTER))
    source_footer(c, 'Live Demo Account capture · Modules · 16 August 2026. Facilitation sequence grounded in metacognitive modelling.')
    c.showPage()
    add_meta(
        'Teach the method before asking for independence.', '4 min',
        'Position the learning modules as a common language that adults actively teach and revisit.',
        'The live Modules view shows the five-world programme and a clear continuation point. Teachers make the content usable by modelling it on actual subject work, naming when it applies, checking use and fading support gradually.',
        ask='“Which module could become part of an existing tutor, SPHE or subject routine rather than an optional extra?”',
        watch='Do not treat module completion as proof that a strategy transferred into independent study.',
        route='90/120. Optional in 60.', sources=[SOURCES['eef_meta']])

    n = len(SLIDES) + 1
    begin_slide(c, 'Facilitate growth · Sequence', 'A pathway makes the next step visible without shrinking ambition.', slide_no=n)
    draw_screen_crop(c, live / '19-learning-paths.png', 48, 76, 530, 312, (0, 0, 1, .73), 8, True, 20)
    round_box(c, 610, 76, 300, 312, PAPER, OUTLINE, 20, 1.2, True)
    draw_label(c, 'Four live routes', 634, 358, PURPLE, 7.3, 1.15)
    path_rows = [
        ('Foundation', 'stabilise habits and core strategies', PALE_BLUE, TEAL),
        ('Exam', 'make tactical preparation explicit', PALE_ORANGE, ORANGE),
        ('Mindset', 'develop resilience and self-knowledge', PALE_PURPLE, PURPLE),
        ('Learning', 'sequence evidence-based study methods', PALE_GREEN, GREEN),
    ]
    for i, (head, body, fill, accent) in enumerate(path_rows):
        y = 291 - i * 52
        c.setFillColor(fill); c.roundRect(632, y, 256, 43, 12, fill=1, stroke=0)
        c.setFillColor(accent); c.setFont('Helvetica-Bold', 8.2); c.drawString(647, y + 25, head.upper())
        c.setFillColor(MUTED); c.setFont('Helvetica', 7.7); c.drawString(647, y + 10, body)
    c.setFillColor(INK); c.roundRect(632, 88, 256, 31, 10, fill=1, stroke=0)
    para(c, '<b>Sequence support.</b> Never hide prerequisites.', 648, 109, 224, 18,
         pstyle('PathBoundaryLive', 'Helvetica', 8.8, 12, PAPER, TA_CENTER))
    source_footer(c, 'Live Demo Account capture · Learning Paths · 16 August 2026.')
    c.showPage()
    add_meta(
        'A pathway makes the next step visible without shrinking ambition.', '4 min',
        'Show how curated routes reduce decision load while preserving challenge and future options.',
        'Learning Paths organise modules into a visible sequence. Adults can use them to make prerequisites explicit, choose a sensible starting point and review progress without making the student navigate the entire programme alone.',
        ask='“Where is a student currently expected to infer the sequence for themselves?”',
        watch='A route should remain revisable. Do not turn a suggested path into a ceiling.',
        route='90/120. Optional in 60.', sources=[SOURCES['eef_meta']])

    n = len(SLIDES) + 1
    begin_slide(c, 'Facilitate growth · Practice', 'Make the next study session easy to begin.', slide_no=n)
    draw_screen(c, live / '03-study-session-mathematics.png', 48, 70, 546, 322, 8, True, 20)
    round_box(c, 626, 70, 284, 322, PAPER, OUTLINE, 20, 1.2, True)
    draw_label(c, 'Before the timer', 650, 362, TEAL, 7.2, 1.05)
    focus_moves = [
        ('Target', 'What will be produced?', PALE_BLUE, TEAL),
        ('Method', 'Retrieve, solve or explain.', PALE_ORANGE, ORANGE),
        ('Check', 'What proves accuracy?', PALE_GREEN, GREEN),
        ('Return', 'What comes back, when?', PALE_PURPLE, PURPLE),
    ]
    for i, (head, body, fill, accent) in enumerate(focus_moves):
        y = 284 - i * 52
        c.setFillColor(fill); c.roundRect(648, y, 240, 43, 11, fill=1, stroke=0)
        c.setFillColor(accent); c.setFont('Helvetica-Bold', 7.4); c.drawString(664, y + 25, head.upper())
        c.setFillColor(INK); c.setFont('Helvetica', 8.2); c.drawString(664, y + 10, body)
    para(c, '<b>Time protects attention.</b> The task creates evidence.', 650, 91, 236, 22,
         pstyle('StudyLiveBoundary', 'Helvetica', 9, 12.5, TEAL, TA_CENTER))
    source_footer(c, 'Live Demo Account capture · Mathematics Practice session · 16 August 2026.')
    c.showPage()
    add_meta(
        'Make the next study session easy to begin.', '4 min',
        'Show how an in-subject study session can reduce initiation friction while preserving an evidence-based learning routine.',
        'The live Mathematics session keeps the subject, purpose, time and an elaboration prompt visible. Agree the product, method, accuracy check and return point before the timer starts.',
        ask='“Could a supervised study period begin with this four-part prompt?”',
        watch='Do not reward minutes without examining the task and the evidence produced.',
        route='90/120. Optional in 60.', sources=[SOURCES['ies_study'], SOURCES['gov_study']])

    launchpad_groups = [
        ('Understand', 'Make demanding material and possible futures easier to enter.',
         '05-launchpad-understand.png', (0, 0, 1, .68),
         [
             ('Future Finder', 'widen career possibilities'),
             ('Paper Trail', 'open real SEC papers'),
             ('Command-Word Reflex', 'decode the demanded action'),
             ('How They Did It', 'make pathways relatable'),
             ('Your Possible Life', 'test real career trade-offs'),
         ], TEAL, PALE_BLUE,
         'Which unfamiliar task could we make more legible without making it less ambitious?'),
        ('Practice', 'Turn effort into feedback, repair and another attempt.',
         '06-launchpad-practise.png', (0, 0, 1, .68),
         [('Mark Bank', 'attempt, compare, self-mark and revisit')], ORANGE, PALE_ORANGE,
         'Where does practice currently stop before feedback changes the next attempt?'),
        ('Plan', 'Protect continuity when time, confidence or attendance slips.',
         '07-launchpad-plan.png', (0, 0, 1, .68),
         [
             ('Spaced Repetition Timetable', 'schedule useful returns'),
             ('War Room', 'choose priorities'),
             ('Comeback Engine', 'plan a dignified recovery'),
             ('College Compass', 'keep routes and deadlines visible'),
             ('Catch-Up Lane', 'replace backlog with one next step'),
         ], GREEN, PALE_GREEN,
         'Which tool could turn “catch up” into one visible next step?'),
        ('Track', 'Make choices, routes and progress discussable.',
         '08-launchpad-track.png', (0, 0, 1, .68),
         [
             ('Academic Journey Simulator', 'rehearse choices safely'),
             ('Points Passport', 'see trends and possible gains'),
         ], PURPLE, PALE_PURPLE,
         'Which student needs a route made visible rather than chosen for them?'),
    ]
    row_fills = [PALE_BLUE, PALE_ORANGE, PALE_GREEN, PALE_PURPLE, PALE_RED, SOFT]
    row_accents = [TEAL, ORANGE, GREEN, PURPLE, RED, OCHRE]
    for group_idx, (group, title, filename, crop, tools, category_accent, category_fill, question) in enumerate(launchpad_groups):
        n = len(SLIDES) + 1
        begin_slide(c, f'Launchpad · {group}', title, slide_no=n)
        draw_screen_crop(c, live / filename, 48, 98, 570, 270, crop, 8, True, 20)
        c.setFillColor(SOFT); c.roundRect(650, 98, 260, 270, 22, fill=1, stroke=0)
        if group == 'Practice':
            draw_label(c, 'The repair loop', 674, 340, category_accent, 7.1, 1.05)
            para(c, 'Mark Bank', 674, 313, 205, 42,
                 pstyle('PracticeToolTitle', 'BrandSerif', 22, 27, INK))
            practice_loop = [
                ('01', 'Attempt', 'without notes', PALE_BLUE, TEAL),
                ('02', 'Compare', 'with the scheme', PALE_ORANGE, ORANGE),
                ('03', 'Repair', 'the first error', PALE_GREEN, GREEN),
                ('04', 'Return', 'after a gap', PALE_PURPLE, PURPLE),
            ]
            for i, (num, head, reason, fill, accent) in enumerate(practice_loop):
                y = 252 - i * 43
                c.setFillColor(fill); c.roundRect(672, y, 216, 35, 11, fill=1, stroke=0)
                c.setFillColor(accent); c.circle(690, y + 17.5, 8.5, fill=1, stroke=0)
                c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 5.2); c.drawCentredString(690, y + 15, num)
                c.setFillColor(INK); c.setFont('Helvetica-Bold', 8.8); c.drawString(708, y + 19, head)
                c.setFillColor(MUTED); c.setFont('Helvetica', 7.4); c.drawString(776, y + 18.5, reason)
        elif group == 'Plan':
            draw_label(c, 'A continuity map', 674, 340, category_accent, 7.1, 1.05)
            c.setStrokeColor(HexColor('#A9C1B6')); c.setLineWidth(2); c.line(687, 132, 687, 313)
            for i, (tool_name, reason) in enumerate(tools):
                y = 300 - i * 42
                accent = row_accents[i % len(row_accents)]
                c.setFillColor(accent); c.circle(687, y, 8.5, fill=1, stroke=0)
                c.setFillColor(INK); c.setFont('Helvetica-Bold', 8.3); c.drawString(708, y + 3, tool_name)
                c.setFillColor(MUTED); c.setFont('Helvetica', 7.2); c.drawString(708, y - 9, reason)
        else:
            draw_label(c, f'Live tools · {group}', 674, 340, category_accent, 7.1, 1.05)
            count = len(tools)
            if count == 2:
                for i, (tool_name, reason) in enumerate(tools):
                    y = 235 - i * 95
                    fill = row_fills[i]
                    accent = row_accents[i]
                    c.setFillColor(fill); c.roundRect(672, y, 216, 76, 16, fill=1, stroke=0)
                    c.setFillColor(accent); c.circle(691, y + 52, 9, fill=1, stroke=0)
                    c.setFillColor(INK); c.setFont('Helvetica-Bold', 9.2); c.drawString(711, y + 49, tool_name)
                    para(c, reason, 711, y + 35, 158, 28,
                         pstyle(f'LiveToolReason{group_idx}{i}', 'Helvetica', 7.8, 10.5, MUTED))
            else:
                c.setStrokeColor(LINE); c.setLineWidth(1.2); c.line(687, 132, 687, 313)
                for i, (tool_name, reason) in enumerate(tools):
                    y = 300 - i * 41
                    accent = row_accents[i % len(row_accents)]
                    c.setFillColor(accent); c.circle(687, y, 8, fill=1, stroke=0)
                    c.setFillColor(INK); c.setFont('Helvetica-Bold', 8.1); c.drawString(706, y + 3, tool_name)
                    c.setFillColor(MUTED); c.setFont('Helvetica', 7); c.drawString(706, y - 9, reason)
        c.setFillColor(category_fill); c.roundRect(130, 49, 700, 34, 12, fill=1, stroke=0)
        para(c, '<b>Adult role:</b> choose for need · agree the output · review the next move.', 158, 72, 644, 20,
             pstyle(f'LaunchpadAdult{group_idx}', 'Helvetica', 9.5, 13, category_accent, TA_CENTER))
        source_footer(c, f'Live Demo Account capture · Launchpad {group} filter · 16 August 2026.')
        c.showPage()
        add_meta(
            title, '4-5 min',
            'Present the real Launchpad tools as a menu organised by student need.',
            'The live filtered view keeps the choice understandable. An adult helps the student select a tool, agrees what successful use will produce and reviews whether it changed the next action.',
            ask=question,
            watch='Avoid prescribing a tool from a label or treating tool use as evidence of learning by itself.',
            route='90/120. In 60, show the two Launchpad groups most relevant to the school.', sources=[])

    n = len(SLIDES) + 1
    begin_slide(c, 'Facilitate growth · Feedback', 'Practice must end with feedback and a next move.', slide_no=n)
    draw_screen_crop(c, live / '15-mark-bank-session.png', 48, 82, 646, 306, (0, .03, 1, .80), 8, True, 20)
    round_box(c, 726, 82, 184, 306, PAPER, OUTLINE, 20, 1.2, True)
    draw_label(c, 'The learning loop', 746, 358, ORANGE, 7.2, 1.05)
    feedback_steps = [
        ('01', 'Attempt', 'without notes', PALE_BLUE, TEAL),
        ('02', 'Compare', 'against the scheme', PALE_ORANGE, ORANGE),
        ('03', 'Decide', 'missed · shaky · got it', PALE_GREEN, GREEN),
        ('04', 'Repair', 'before moving on', PALE_PURPLE, PURPLE),
    ]
    for i, (num, head, body, fill, accent) in enumerate(feedback_steps):
        y = 286 - i * 49
        c.setFillColor(fill); c.roundRect(744, y, 148, 41, 10, fill=1, stroke=0)
        c.setFillColor(accent); c.circle(760, y + 20.5, 8.5, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 5.3); c.drawCentredString(760, y + 18, num)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 8.5); c.drawString(776, y + 23, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 7); c.drawString(776, y + 10, body)
    c.setFillColor(INK); c.roundRect(744, 94, 148, 29, 10, fill=1, stroke=0)
    para(c, '<b>Repair changes the next attempt.</b>', 755, 114, 126, 18,
         pstyle('MarkBankLiveBoundary', 'Helvetica', 7.4, 10, PAPER, TA_CENTER))
    source_footer(c, 'Live Demo Account capture · Biology Mark Bank · real SEC question and scheme · 16 August 2026.')
    c.showPage()
    add_meta(
        'Practice must end with feedback and a next move.', '5 min',
        'Connect exam practice, marking guidance, self-assessment and error repair.',
        'The live Biology session shows one of five cards, a real question, its SEC-aligned scheme and the Missed it/Shaky/Got it decision. Use that decision to schedule repair and later retrieval.',
        ask='“What would make “shaky” a useful next-action category rather than a label?”',
        watch='Self-rating is fallible. Calibrate it with worked examples, teacher feedback and later retrieval.',
        route='Core in 90/120; show briefly in 60.', sources=[SOURCES['ies_study'], SOURCES['eef_feedback']])

    n = len(SLIDES) + 1
    begin_slide(c, 'Facilitate growth · Review', 'A dashboard should start a conversation - not issue a verdict.', slide_no=n)
    draw_screen_crop(c, live / '15-dashboard-overview.png', 48, 68, 570, 320, (0, 0, 1, .85), 8, True, 20)
    round_box(c, 650, 68, 260, 320, PAPER, OUTLINE, 20, 1.2, True)
    draw_label(c, 'Use the filters, then ask', 672, 358, TEAL, 7.1, 1.0)
    dashboard_prompts = [
        ('01', 'What changed?', 'Compare week, month and year.', PALE_BLUE, TEAL),
        ('02', 'What helped?', 'Connect rhythm to method and access.', PALE_GREEN, GREEN),
        ('03', 'Where is it stuck?', 'Look for a barrier, not a defect.', PALE_ORANGE, ORANGE),
        ('04', 'What happens next?', 'Name an action and an adult.', PALE_PURPLE, PURPLE),
    ]
    for i, (num, head, body, fill, accent) in enumerate(dashboard_prompts):
        y = 279 - i * 51
        c.setFillColor(fill); c.roundRect(671, y, 218, 44, 11, fill=1, stroke=0)
        c.setFillColor(accent); c.circle(687, y + 22, 8.5, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 5.4); c.drawCentredString(687, y + 19.5, num)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 8.6); c.drawString(703, y + 25, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 7.2); c.drawString(703, y + 10, body)
    c.setFillColor(INK); c.roundRect(671, 80, 218, 28, 10, fill=1, stroke=0)
    para(c, '<b>Patterns guide support.</b> They do not predict worth.', 687, 100, 186, 18,
         pstyle('DashLiveBoundary', 'Helvetica', 8.1, 11, PAPER, TA_CENTER))
    source_footer(c, 'Live Demo Account capture · My Progress Overview · 16 August 2026. Sessions/minutes and week/month/year filters are live.')
    c.showPage()
    add_meta(
        'A dashboard should start a conversation - not issue a verdict.', '5 min',
        'Use live product data as a prompt for reflection, recognition and targeted support.',
        'The live Overview connects study rhythm, focused minutes, confidence, subject allocation, Five Climbs, techniques and mock evidence. Change the timeframe, then ask what changed, what helped and what support comes next.',
        ask='“Who reviews this with the student, and how often, so that the data changes a next action?”',
        watch='Avoid rankings, deterministic predictions and surveillance. Sparse data may reflect access barriers as well as motivation or skill.',
        route='Core in every version.', sources=[SOURCES['eef_feedback'], SOURCES['eef_meta']])

    n = len(SLIDES) + 1
    begin_slide(c, 'My Progress · Three lenses', 'Rhythm, confidence and practice stay connected.', slide_no=n)
    dashboard_views = [
        ('Study', '16-dashboard-study.png', PALE_BLUE, TEAL, 'Is effort becoming a dependable rhythm?'),
        ('Confidence', '17-dashboard-confidence.png', PALE_GREEN, GREEN, 'What is the student noticing about readiness?'),
        ('Practice', '18-dashboard-practice.png', PALE_ORANGE, ORANGE, 'Is work producing exam evidence and repair?'),
    ]
    for i, (label, filename, fill, accent, prompt) in enumerate(dashboard_views):
        x = 38 + i * 302
        draw_screen(c, live / filename, x, 154, 282, 230, 7, True, 17)
        c.setFillColor(fill); c.roundRect(x + 12, 71, 258, 60, 14, fill=1, stroke=0)
        c.setFillColor(accent); c.setFont('Helvetica-Bold', 7.2); c.drawString(x + 28, 108, label.upper())
        para(c, prompt, x + 28, 95, 222, 34,
             pstyle(f'DashLens{i}', 'Helvetica', 8.2, 11.2, INK))
    source_footer(c, 'Live Demo Account captures · Study, Confidence and Practice tabs · 16 August 2026. Five Climbs remains visible in the Confidence view.')
    c.showPage()
    add_meta(
        'Rhythm, confidence and practice stay connected.', '5 min',
        'Show the current Study, Confidence and Practice views without collapsing progress into one number.',
        'Study shows consistency and technique use; Confidence shows reflections and the Five Climbs programme landscape; Practice shows mock trajectory, readiness and method use. Review the lenses together so one chart does not become a judgement.',
        ask='“Which lens would help this student name a useful next step?”',
        watch='Confidence is a reflection signal, not a measure of ability. Practice evidence also needs context.',
        route='Core in 90/120; optional detail in 60.', sources=[SOURCES['eef_feedback'], SOURCES['eef_meta']])

    n = len(SLIDES) + 1
    begin_slide(c, 'Facilitate growth · Belong', 'Let progress become a place the student can shape.', slide_no=n)
    draw_label(c, 'Journey mode', 49, 419, TEAL, 7.5, 1.15)
    draw_label(c, 'Build mode', 503, 419, ORANGE, 7.5, 1.15)
    draw_screen(c, live / '10-journey-mode.png', 48, 132, 410, 273, 7, True, 18)
    draw_screen(c, live / '13-build-terrain.png', 502, 132, 410, 273, 7, True, 18)
    c.setFillColor(PALE_BLUE); c.roundRect(72, 72, 362, 42, 12, fill=1, stroke=0)
    para(c, '<b>Journey:</b> accumulated effort becomes a place and a story.', 92, 100, 322, 24,
         pstyle('JourneyLiveReason', 'Helvetica', 9, 12, TEAL, TA_CENTER))
    c.setFillColor(PALE_ORANGE); c.roundRect(526, 72, 362, 42, 12, fill=1, stroke=0)
    para(c, '<b>Build:</b> meaningful choice adds authorship without public ranking.', 546, 100, 322, 25,
         pstyle('BuildLiveReason', 'Helvetica', 9, 12, ORANGE, TA_CENTER))
    source_footer(c, 'Live Demo Account captures · Journey and Build modes · 16 August 2026. Compare neither islands nor spending publicly.')
    c.showPage()
    add_meta(
        'Let progress become a place the student can shape.', '4 min',
        'Explain how the live Journey and Build modes can support continuity, ownership and belonging when used carefully.',
        'Journey mode makes accumulated effort visible as a place rather than only a score. Build mode adds meaningful choice over what the student places and changes. Use the space as a reflection prompt: what does this represent, what changed and what does the student want to build next?',
        ask='“How could an adult notice the story behind the build rather than praise only the amount completed?”',
        watch='Do not compare islands publicly or make decorative rewards the primary reason to learn.',
        route='90/120. Optional in 60.', sources=[])

    # close - light, with large illustrations visibly extending beyond their
    # blobs instead of the small icon-in-circle treatment the user rejected.
    n = len(SLIDES) + 1
    begin_slide(c, 'The invitation', 'Be the school that keeps the door open.', slide_no=n)
    para(c, 'Not every barrier begins in school.<br/><br/><b>But school can decide whether a barrier becomes a ceiling.</b>',
         70, 344, 450, 190, pstyle('Close', 'BrandSerif', 27, 36, INK))
    c.setStrokeColor(ORANGE); c.setLineWidth(3); c.line(70, 136, 255, 136)
    blob(c, 738, 272, 98, 85, PALE_ORANGE, -7)
    draw_icon(c, assets / 'section-icons' / 'my-journey.png', 610, 151, 250, 250)
    blob(c, 629, 163, 54, 47, PALE_BLUE, 8)
    draw_icon(c, assets / 'section-icons' / 'my-progress-mountain.png', 552, 92, 152, 152)
    blob(c, 835, 149, 56, 48, PALE_PURPLE, -5)
    draw_icon(c, assets / 'learning-paths' / 'getting-started.png', 760, 78, 155, 155)
    source_footer(c, 'Return to your story. End with the student, not the programme.')
    c.showPage()
    add_meta(
        'Be the school that keeps the door open.', '3-5 min',
        'Return to the opening story and close with responsibility, hope and collective agency.',
        'Return briefly to the student you were and the adult action that changed what was possible. Avoid claiming school can solve poverty or trauma. Land on the distinction: schools cannot control every starting condition, but they can protect access, challenge, belonging and navigation.',
        ask='Optional final line to the room: “Whose door will be more open because of what we do next?”',
        watch='Finish cleanly. Do not add a new content section after this slide.',
        route='Core in every version.', sources=[])

    # 26 - references Ireland
    n = len(SLIDES) + 1
    begin_slide(c, 'Evidence base · Ireland', 'National statistics and policy sources.', slide_no=n)
    refs = [
        ('CSO', 'SILC Module on Child Deprivation 2024', SOURCES['cso_child']),
        ('Tusla', 'Analysis of School Attendance Data 2023/24', SOURCES['tusla_attendance']),
        ('Department of Education', 'DEIS Strategy to 2035; retention and attendance material', SOURCES['deis_strategy']),
        ('OECD', 'PISA 2022 Results - Ireland country note', SOURCES['pisa']),
        ('HEA', 'Socio-economic profiles of students, 2021/22-2023/24', SOURCES['hea_profile']),
        ('ESRI / GUI', 'Self-concept, expectations and teacher-student relationships', SOURCES['esri_relationships']),
        ('OECD', 'Review of Resourcing Schools to Address Educational Disadvantage in Ireland', SOURCES['oecd_disadvantage']),
    ]
    y = 370
    for org, title, url in refs:
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 9.5); c.drawString(65, y, org)
        para(c, title, 205, y+3, 290, 30, pstyle('RefTitle', 'Helvetica', 9.5, 12, MUTED))
        para(c, url, 515, y+3, 375, 34, pstyle('RefUrl', 'Helvetica', 6.3, 8.2, LABEL))
        draw_rule(c, 65, y-13, 890, LINE, 0.6)
        y -= 46
    c.showPage()
    add_meta(
        'National statistics and policy sources.', 'Reference',
        'Make the evidence traceable.',
        'This slide is not normally presented line by line. Leave it available for questions and circulate the facilitator guide/workbook references.',
        ask='', watch='Check figures against the dated source before reusing the deck in a future year.',
        route='Appendix/reference.', sources=[u for _,_,u in refs])

    # 27 - references practice
    n = len(SLIDES) + 1
    begin_slide(c, 'Evidence base · practice', 'Teaching, attendance, trauma and pathways.', slide_no=n)
    refs2 = [
        ('NEPS', 'Service, Continuum of Support and trauma resources', SOURCES['neps_resources']),
        ('EEF', 'Metacognition and self-regulation; feedback', SOURCES['eef_meta']),
        ('IES / WWC', 'Organizing Instruction and Study to Improve Student Learning', SOURCES['ies_study']),
        ('Department of Education', 'How to create study routines for the Leaving Certificate', SOURCES['gov_study']),
        ('EEF', 'Attendance interventions evidence summary', SOURCES['eef_attendance']),
        ('Campbell systematic review', 'Effects of trauma-informed approaches in schools', SOURCES['trauma_review']),
        ('UK Government', 'Caution on use of ACE screening tools', SOURCES['ace_caution']),
        ('DFHERIS', 'Education pathways in Ireland', SOURCES['pathways']),
        ('Access College / SUSI', 'HEAR and student grant information', SOURCES['hear']),
    ]
    y = 370
    for org, title, url in refs2:
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 8.7); c.drawString(65, y, org)
        para(c, title, 205, y+3, 290, 27, pstyle('Ref2Title', 'Helvetica', 8.7, 10.8, MUTED))
        para(c, url, 515, y+3, 375, 29, pstyle('Ref2Url', 'Helvetica', 5.7, 7.2, LABEL))
        draw_rule(c, 65, y-11, 890, LINE, 0.6)
        y -= 39
    c.showPage()
    add_meta(
        'Teaching, attendance, trauma and pathways.', 'Reference',
        'Make the practical guidance and its limits traceable.',
        'Use this slide for questions about evidence quality. Be especially transparent that school-wide trauma-informed evidence is still developing; the workshop prioritises low-risk, role-clear practices aligned with NEPS.',
        ask='', watch='HEAR, SUSI, apprenticeship and course details change. Recheck annually.',
        route='Appendix/reference.', sources=[u for _,_,u in refs2])

    c.save()


def render_deck_pages():
    import pypdfium2 as pdfium
    deck_dir = TMP / 'deck_pages'
    deck_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(DECK_PATH))
    paths = []
    for i in range(len(pdf)):
        page = pdf[i]
        img = page.render(scale=1.5).to_pil()
        path = deck_dir / f'slide-{i+1:02d}.png'
        img.save(path)
        paths.append(path)
    return paths


def build_facilitator_guide(slide_images):
    w, h = A4
    c = canvas.Canvas(str(GUIDE_PATH), pagesize=A4, pageCompression=1)
    # cover
    c.setFillColor(CANVAS); c.rect(0, 0, w, h, fill=1, stroke=0)
    draw_label(c, 'Facilitator guide', 46, h-62, LABEL, 9, 1.9)
    para(c, 'Nurturing<br/>potential.', 46, h-112, 340, 165, pstyle('FGCover', 'BrandSerif', 42, 45, INK))
    para(c, 'A flexible 60 / 90 / 120-minute route for Irish post-primary staff.', 48, h-280, 330, 80,
         pstyle('FGSub', 'Helvetica', 16, 23, MUTED))
    blob(c, w-130, 185, 88, 85, PALE_ORANGE, -5)
    draw_icon(c, ROOT / 'public' / 'assets' / 'section-icons' / 'my-journey.png', w-220, 95, 180, 180)
    draw_rule(c, 48, 205, 300, OUTLINE, 1.2)
    para(c, '<b>Core communication job</b><br/>Disadvantage changes the obstacles around learning, not the ceiling on a child’s potential. Consistent adult and whole-school practices can change the odds.',
         48, 184, 305, 135, pstyle('FGJob', 'Helvetica', 10.5, 16, INK))
    c.showPage()

    # route map
    c.setFillColor(CANVAS); c.rect(0,0,w,h,fill=1,stroke=0)
    draw_label(c, 'How to use this guide', 46, h-55, LABEL, 8.5, 1.7)
    para(c, 'Choose the route; keep the spine.', 46, h-87, 500, 65, pstyle('FGTitle', 'BrandSerif', 26, 31, INK))
    routes = [
        ('60 minutes', 'Keep slides 1-5, 7, 9-12, 14-15, 17, 19-21, 23-25. Use the worked case rather than group case time.'),
        ('90 minutes', 'Use the full core deck. Allow 12 minutes for the case and 15 minutes for the 90-day plan.'),
        ('120 minutes', 'Use the full deck. Extend expectation audit, case work and peer critique of school plans.'),
    ]
    y = h-175
    for i,(head, body) in enumerate(routes):
        number_dot(c, i+1, 64, y, [TEAL, ORANGE, PURPLE][i], 15)
        c.setFillColor(INK); c.setFont('BrandSerif', 16); c.drawString(92, y-5, head)
        para(c, body, 92, y-26, 440, 70, pstyle('FGRoute', 'Helvetica', 10.5, 15, MUTED))
        y -= 115
    round_box(c, 46, 105, w-92, 150, PAPER, OUTLINE, 16, 1.2, False)
    draw_label(c, 'Safeguarding boundary', 68, 225, RED, 8, 1.2)
    para(c, 'Do not invite public disclosure of trauma, poverty, family circumstances or named student cases. If a participant raises an immediate safeguarding concern, pause the activity and follow the school’s established procedures.',
         68, 198, w-136, 78, pstyle('FGBoundary', 'Helvetica-Bold', 10.5, 16, INK))
    c.showPage()

    for idx, (meta, img_path) in enumerate(zip(SLIDES, slide_images), start=1):
        c.setFillColor(CANVAS); c.rect(0,0,w,h,fill=1,stroke=0)
        draw_label(c, f'Slide {idx:02d} · {meta["timing"]}', 42, h-42, LABEL, 7.5, 1.2)
        para(c, meta['title'], 42, h-65, 510, 45, pstyle('FGSlideTitle', 'BrandSerif', 20, 24, INK))
        # thumbnail
        c.drawImage(ImageReader(str(img_path)), 42, h-350, width=w-84, height=230,
                    preserveAspectRatio=True, mask='auto', anchor='c')
        y = h-372
        blocks = [('PURPOSE', meta['purpose'], ORANGE), ('SAY', meta['say'], TEAL)]
        if meta['ask']:
            blocks.append(('ASK / DO', meta['ask'], PURPLE))
        if meta['watch']:
            blocks.append(('WATCH FOR', meta['watch'], RED))
        if meta['route']:
            blocks.append(('ROUTE', meta['route'], OCHRE))
        for head, body, col in blocks:
            draw_label(c, head, 42, y, col, 6.8, 1.1)
            h_used = para(c, body, 118, y+3, w-160, 85, pstyle('FGBlock', 'Helvetica', 8.6, 12.1, INK))
            y -= max(23, h_used + 7)
        if meta['sources']:
            draw_label(c, 'Sources', 42, y, LABEL, 6.8, 1.1)
            source_text = '<br/>'.join(meta['sources'])
            para(c, source_text, 118, y+3, w-160, 72, pstyle('FGSources', 'Helvetica', 5.8, 7.2, LABEL))
        c.setFillColor(LABEL); c.setFont('Helvetica', 7); c.drawRightString(w-42, 24, str(idx))
        c.showPage()
    c.save()


def wb_header(c, page_no, eyebrow, title, subtitle=None):
    w, h = A4
    c.setFillColor(CANVAS); c.rect(0,0,w,h,fill=1,stroke=0)
    draw_label(c, eyebrow, 42, h-44, LABEL, 7.8, 1.5)
    para(c, title, 42, h-70, w-84, 80, pstyle('WBTitle', 'BrandSerif', 26, 31, INK))
    y = h-128
    if subtitle:
        para(c, subtitle, 42, y, w-84, 55, pstyle('WBSub', 'Helvetica', 10.5, 15.5, MUTED))
        y -= 48
    c.setFillColor(LABEL); c.setFont('Helvetica', 7); c.drawRightString(w-42, 24, str(page_no))
    return y


def writing_lines(c, x, y_top, w, count, gap=24, color=LINE):
    c.setStrokeColor(color); c.setLineWidth(0.8)
    for i in range(count):
        y = y_top - i*gap
        c.line(x, y, x+w, y)


def checkbox(c, x, y, label, checked=False, size=11, color=INK):
    c.setStrokeColor(OUTLINE); c.setLineWidth(1); c.rect(x, y-2, 11, 11, fill=0, stroke=1)
    if checked:
        c.setStrokeColor(ORANGE); c.setLineWidth(1.8); c.line(x+2,y+3,x+5,y); c.line(x+5,y,x+10,y+8)
    c.setFillColor(color); c.setFont('Helvetica', size); c.drawString(x+18, y-1, label)


def build_workbook():
    w, h = A4
    c = canvas.Canvas(str(WORKBOOK_PATH), pagesize=A4, pageCompression=1)
    assets = ROOT / 'public' / 'assets'

    # Cover
    c.setFillColor(CANVAS); c.rect(0,0,w,h,fill=1,stroke=0)
    draw_label(c, 'Participant workbook + practical toolkit', 42, h-55, LABEL, 8, 1.5)
    para(c, 'Nurturing<br/>potential.', 42, h-104, 350, 150, pstyle('WBCover', 'BrandSerif', 42, 44, INK))
    para(c, 'Helping every young person succeed in second-level education and navigate a future beyond it.',
         44, h-270, 350, 80, pstyle('WBCoverSub', 'Helvetica', 14, 21, MUTED))
    blob(c, w-130, 195, 88, 84, PALE_ORANGE, -5)
    draw_icon(c, assets / 'section-icons' / 'my-progress-mountain.png', w-220, 95, 180, 180)
    draw_rule(c, 44, 235, 330, OUTLINE, 1.2)
    para(c, '<b>Name / team</b>  ___________________________________________<br/><br/><b>Date</b>  ____________________',
         44, 215, 360, 80, pstyle('WBName', 'Helvetica', 10.5, 18, INK))
    c.showPage()

    # 2 opening reflection
    y = wb_header(c, 2, 'Start with experience', 'Who changed your odds?', 'Think of a repeatable adult practice, not a heroic one-off gesture.')
    prompts = [
        'What did that adult do repeatedly?',
        'What did their behaviour communicate about your ability or future?',
        'Which student in your school may not experience that reliably yet?',
    ]
    for i,p in enumerate(prompts, start=1):
        number_dot(c, i, 57, y-6, [TEAL, ORANGE, PURPLE][i-1], 12)
        para(c, p, 82, y+3, w-124, 50, pstyle('WBPrompt', 'BrandSerif', 14, 20, INK))
        writing_lines(c, 82, y-43, w-124, 3, 22)
        y -= 137
    round_box(c, 42, 85, w-84, 92, PAPER, OUTLINE, 14, 1.1)
    para(c, '<b>Boundary:</b> keep the student private. Work with patterns and practices; do not write trauma histories or identifying details.',
         62, 146, w-124, 52, pstyle('WBBound', 'Helvetica', 9.5, 14, RED))
    c.showPage()

    # 3 evidence snapshot
    y = wb_header(c, 3, 'Ireland · evidence snapshot', 'Hold two truths together.', 'Inequality is measurable. Individual outcomes are not predetermined.')
    stats = [
        ('13.8%', 'children in child-specific enforced deprivation, 2024', ORANGE),
        ('28.3%', 'DEIS post-primary students missing 20+ days in responding schools, 2023/24', RED),
        ('83.4%', 'DEIS retention to Leaving Certificate for the 2017 entry cohort', TEAL),
        ('12%', 'disadvantaged students academically resilient in PISA 2022', PURPLE),
    ]
    for i,(v,l,col) in enumerate(stats):
        x = 42 + (i%2)*258
        yy = y - (i//2)*150
        round_box(c, x, yy-115, 232, 118, PAPER, LINE, 14, 1, False)
        c.setFillColor(col); c.setFont('BrandSerif', 30); c.drawString(x+18, yy-42, v)
        para(c, l, x+18, yy-58, 196, 54, pstyle('WBStat', 'Helvetica', 8.7, 12.5, MUTED))
    para(c, '<b>What does this data make you notice?</b>', 42, 287, w-84, 30, pstyle('WBDataQ', 'Helvetica-Bold', 10.5, 15, INK))
    writing_lines(c, 42, 254, w-84, 3, 23)
    para(c, '<b>What must it never make us assume about an individual student?</b>', 42, 162, w-84, 30, pstyle('WBDataQ2', 'Helvetica-Bold', 10.5, 15, INK))
    writing_lines(c, 42, 131, w-84, 3, 23)
    c.showPage()

    # 4 diagnostic
    y = wb_header(c, 4, 'The five promises', 'Rate the student experience, not the policy.', '1 = person-dependent or inconsistent · 4 = systematic, visible and reviewed')
    rows = [
        ('Known', 'Every student can name an adult who will notice.'),
        ('Taught', 'Support preserves challenge, subject access and future options.'),
        ('Present', 'Attendance patterns trigger timely, barrier-responsive support.'),
        ('Partnered', 'Families can reach a person and leave with a clear next step.'),
        ('Future-ready', 'Every student can name three plausible routes and next actions.'),
    ]
    y -= 5
    for i,(head, desc) in enumerate(rows, start=1):
        number_dot(c, i, 58, y-4, [TEAL, ORANGE, GREEN, PURPLE, RED][i-1], 12)
        c.setFillColor(INK); c.setFont('BrandSerif', 14); c.drawString(82, y-8, head)
        para(c, desc, 185, y+2, 275, 42, pstyle('WBDiag', 'Helvetica', 8.8, 12.5, MUTED))
        for j in range(4):
            c.setStrokeColor(LINE); c.circle(488+j*23, y-4, 7, fill=0, stroke=1)
            c.setFillColor(LABEL); c.setFont('Helvetica', 6.5); c.drawCentredString(488+j*23, y-7, str(j+1))
        y -= 74
    para(c, '<b>Strongest promise:</b> _______________________________', 42, 225, w-84, 24, pstyle('WBDiag2', 'Helvetica', 10, 15, INK))
    para(c, '<b>Least dependable:</b> _________________________________', 42, 188, w-84, 24, pstyle('WBDiag3', 'Helvetica', 10, 15, INK))
    para(c, '<b>Where might student or family ratings differ from ours?</b>', 42, 145, w-84, 25, pstyle('WBDiag4', 'Helvetica-Bold', 10, 15, INK))
    writing_lines(c, 42, 116, w-84, 3, 22)
    c.showPage()

    # 5 expectation audit
    y = wb_header(c, 5, 'Expectation audit', 'Turn a verdict into a useful question.', 'Barrier-aware language preserves both accountability and possibility.')
    examples = [
        ('“They do not value school.”', 'What makes attendance harder here?'),
        ('“The family will not engage.”', 'How accessible and trustworthy is our contact?'),
        ('“Not college material.”', 'Which routes and supports remain invisible?'),
        ('“Trauma explains it.”', 'What supports regulation and a return to learning?'),
    ]
    draw_label(c, 'Verdict', 42, y, RED, 7, 1.1); draw_label(c, 'Better question', 294, y, TEAL, 7, 1.1)
    y -= 28
    for left,right in examples:
        para(c, left, 42, y, 220, 44, pstyle('WBVerdict', 'BrandSerifItalic', 11, 16, MUTED))
        para(c, right, 294, y, 255, 44, pstyle('WBQuestion', 'Helvetica-Bold', 9.5, 14, INK))
        draw_rule(c, 42, y-37, w-42, LINE, 0.7)
        y -= 62
    para(c, '<b>A phrase or assumption we need to examine:</b>', 42, 274, w-84, 28, pstyle('WBRewrite', 'Helvetica-Bold', 10, 15, INK))
    writing_lines(c, 42, 242, w-84, 2, 23)
    para(c, '<b>Our more useful question:</b>', 42, 174, w-84, 28, pstyle('WBRewrite2', 'Helvetica-Bold', 10, 15, INK))
    writing_lines(c, 42, 142, w-84, 3, 23)
    c.showPage()

    # 6 known + taught
    y = wb_header(c, 6, 'Promise tools', 'Known + taught ambitiously.', 'Choose routines that make belonging and success less dependent on luck.')
    draw_label(c, 'Known', 42, y, TEAL, 8, 1.2)
    known = ['Named adult with a real check-in routine', 'Fast noticing after absence, withdrawal or change', 'Repair after conflict', 'Strength recorded and carried into support meetings']
    yy = y-30
    for item in known:
        checkbox(c, 48, yy, item, size=9.5); yy -= 30
    draw_label(c, 'Taught', 42, yy-2, ORANGE, 8, 1.2)
    yy -= 32
    taught = ['Model expert thinking aloud', 'Use worked examples and guided practice', 'Check understanding beyond volunteers', 'Feedback creates a next attempt', 'Fade scaffolds toward independent retrieval and planning']
    for item in taught:
        checkbox(c, 48, yy, item, size=9.5); yy -= 30
    round_box(c, 42, 105, w-84, 135, PAPER, OUTLINE, 14, 1.1)
    draw_label(c, 'One routine to make dependable', 62, 210, PURPLE, 7, 1.1)
    para(c, '<b>Routine:</b> _______________________________________________<br/><br/><b>Where / when:</b> __________________________________________<br/><br/><b>How we know it happened:</b> _______________________________',
         62, 186, w-124, 95, pstyle('WBRoutine', 'Helvetica', 9.5, 16, INK))
    c.showPage()

    # 7 trauma-aware
    y = wb_header(c, 7, 'Role clarity', 'Trauma-aware without becoming trauma-detectives.', 'Universal safety and predictable practice; targeted support through established systems.')
    c.setFillColor(PALE_GREEN); c.roundRect(42, 415, 245, 245, 16, fill=1, stroke=0)
    draw_label(c, 'Do', 62, 632, TEAL, 8, 1.2)
    do = ['make routines predictable', 'offer choice within boundaries', 'regulate before reasoning', 'provide a dignified route back', 'refer and review through the support team']
    yy = 600
    for item in do:
        checkbox(c, 62, yy, item, size=9); yy -= 32
    c.setFillColor(PALE_RED); c.roundRect(308, 415, 245, 245, 16, fill=1, stroke=0)
    draw_label(c, 'Do not', 328, 632, RED, 8, 1.2)
    dont = ['collect ACE scores', 'diagnose from behaviour', 'demand disclosure', 'remove all limits', 'replace specialist care']
    yy = 600
    for item in dont:
        checkbox(c, 328, yy, item, size=9); yy -= 32
    para(c, '<b>One predictable routine we can strengthen:</b>', 42, 372, w-84, 25, pstyle('WBTraumaQ', 'Helvetica-Bold', 10, 15, INK))
    writing_lines(c, 42, 340, w-84, 3, 23)
    para(c, '<b>Our route for consultation / referral:</b>', 42, 246, w-84, 25, pstyle('WBTraumaQ2', 'Helvetica-Bold', 10, 15, INK))
    writing_lines(c, 42, 214, w-84, 3, 23)
    round_box(c, 42, 80, w-84, 86, PAPER, OUTLINE, 12, 1)
    para(c, '<b>Safeguarding:</b> follow school procedures for disclosures or immediate risk. Do not investigate in a classroom or workshop activity.',
         60, 140, w-120, 50, pstyle('WBSafe', 'Helvetica-Bold', 9.2, 14, RED))
    c.showPage()

    # 8 attendance map
    y = wb_header(c, 8, 'Attendance', 'Notice > ask > map > act > review.', 'Twenty days is a reporting threshold; support should begin when a meaningful pattern emerges.')
    steps = [('NOTICE', 'What changed? When? Which pattern?'), ('ASK', 'What does the student say? The family?'), ('MAP', 'Barrier, strength, resource, risk'), ('ACT', 'One specific response and owner'), ('REVIEW', 'Date, evidence, adapt / escalate')]
    y -= 5
    for i,(head,desc) in enumerate(steps, start=1):
        number_dot(c, i, 58, y-7, [TEAL, ORANGE, OCHRE, PURPLE, RED][i-1], 12)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 9); c.drawString(83, y-10, head)
        c.setFillColor(MUTED); c.setFont('Helvetica', 9); c.drawString(150, y-10, desc)
        writing_lines(c, 83, y-34, 468, 2, 20)
        y -= 92
    c.showPage()

    # 9 family conversation
    y = wb_header(c, 9, 'Family partnership', 'Plan the first contact.', 'Specific · curious · strength-first · accessible · reliable')
    fields = [
        ('STRENGTH', 'What can we truthfully name first?'),
        ('PATTERN', 'What specific days, changes or work have we noticed?'),
        ('QUESTION', 'How will we ask what may be getting in the way?'),
        ('NEXT STEP', 'What small action can school and home agree?'),
        ('FOLLOW-THROUGH', 'Who will report back, through which channel, and when?'),
    ]
    for head,prompt in fields:
        draw_label(c, head, 42, y, ORANGE if head in ('STRENGTH','NEXT STEP') else LABEL, 7, 1.1)
        para(c, prompt, 145, y+3, 400, 28, pstyle('WBFamilyField', 'Helvetica', 9.3, 13, MUTED))
        writing_lines(c, 42, y-27, w-84, 2, 21)
        y -= 90
    c.showPage()

    # 10 pathway map
    y = wb_header(c, 10, 'Future-ready', 'Build three routes, not one prediction.', 'Each route needs requirements, deadlines, costs/funding, a named adult and a next action.')
    routes = [('ROUTE A', 'Aspiration / CAO / higher education', PALE_BLUE), ('ROUTE B', 'FET / PLC / tertiary / access / foundation', PALE_GREEN), ('ROUTE C', 'Apprenticeship / work + training', PALE_PURPLE)]
    y -= 5
    for head,desc,fill in routes:
        c.setFillColor(fill); c.roundRect(42, y-125, w-84, 122, 15, fill=1, stroke=0)
        draw_label(c, head, 62, y-25, INK, 7.5, 1.1)
        c.setFillColor(INK); c.setFont('BrandSerif', 13); c.drawString(145, y-28, desc)
        c.setFillColor(MUTED); c.setFont('Helvetica', 8.5)
        c.drawString(62, y-58, 'Course / role:'); c.line(128, y-60, 310, y-60)
        c.drawString(330, y-58, 'Next action:'); c.line(395, y-60, 535, y-60)
        c.drawString(62, y-89, 'Funding / access:'); c.line(148, y-91, 310, y-91)
        c.drawString(330, y-89, 'Adult / date:'); c.line(395, y-91, 535, y-91)
        y -= 145
    check_y = 165
    checkbox(c, 42, check_y, 'HEAR / DARE checked where relevant', size=9)
    checkbox(c, 305, check_y, 'SUSI / costs discussed', size=9)
    checkbox(c, 42, check_y-28, 'Entry requirements verified', size=9)
    checkbox(c, 305, check_y-28, 'Family understands the routes', size=9)
    c.showPage()

    # 11 case lab
    y = wb_header(c, 11, 'Case lab · fictional composite', 'Leah: separate what is known from what is assumed.', 'Strong orally · inconsistent written work · 16 absences by February · caring responsibilities · physiotherapy aspiration')
    columns = [('KNOWN', 'Only the information actually given.'), ('ASSUMED', 'What might we be adding to the story?')]
    for i,(head,desc) in enumerate(columns):
        x = 42 + i*267
        draw_label(c, head, x, y, [TEAL, RED][i], 7.5, 1.1)
        para(c, desc, x, y-22, 240, 35, pstyle('WBCaseCol', 'Helvetica', 8.5, 12, MUTED))
        writing_lines(c, x, y-65, 240, 5, 22)
    draw_rule(c, 42, 382, w-42, OUTLINE, 1.2)
    prompts = [('What do we need to learn from Leah and home?', TEAL), ('What changes tomorrow?', ORANGE), ('What changes this term?', PURPLE), ('Who owns each next step?', RED)]
    yy = 350
    for prompt,col in prompts:
        c.setFillColor(col); c.setFont('Helvetica-Bold', 9.5); c.drawString(42, yy, prompt)
        writing_lines(c, 42, yy-25, w-84, 2, 20)
        yy -= 78
    c.showPage()

    # 12 90-day plan
    y = wb_header(c, 12, 'Whole-school action', 'Design one 90-day test.', 'Small enough to implement · important enough to matter · specific enough to learn from')
    fields = [
        ('PROMISE', 'Which experience will become more dependable?'),
        ('FOCUS', 'For whom, where and when is the gap most visible?'),
        ('ROUTINE', 'What will adults do differently, and how often?'),
        ('OWNER + SUPPORT', 'Who coordinates? What capacity or training is needed?'),
        ('EARLY SIGNAL', 'What should move within four weeks?'),
        ('LAGGING OUTCOME', 'Which attendance, learning, retention or progression measure matters?'),
        ('REVIEW DATE', 'When will the team learn, adapt or stop?'),
    ]
    for head,prompt in fields:
        draw_label(c, head, 42, y, ORANGE if head in ('PROMISE','REVIEW DATE') else LABEL, 6.8, 1.0)
        para(c, prompt, 150, y+2, 395, 25, pstyle('WBPlanPrompt', 'Helvetica', 8.7, 12, MUTED))
        writing_lines(c, 42, y-25, w-84, 2, 20)
        y -= 76
    c.showPage()

    # 13 implementation and privacy
    y = wb_header(c, 13, 'Implementation check', 'Will the plan survive Monday?', 'Use this before the team commits.')
    checks = [
        'The change is a visible adult routine, not only a value statement.',
        'The owner has authority, time and support.',
        'The plan fits existing DEIS / SSE / student-support structures.',
        'Students and families can shape or test the approach.',
        'We know what we will stop or simplify to create capacity.',
        'We can see implementation within four weeks.',
        'No sensitive trauma history or diagnostic guess is collected.',
        'There is a review date and permission to adapt or stop.',
    ]
    yy = y-8
    for item in checks:
        checkbox(c, 48, yy, item, size=9.5); yy -= 38
    round_box(c, 42, 128, w-84, 135, PAPER, OUTLINE, 14, 1.1)
    draw_label(c, 'One sentence plan', 62, 235, TEAL, 7, 1.1)
    para(c, 'For ____________________, we will ________________________________, led by ____________________, and by ______________ we expect ________________________________.',
         62, 208, w-124, 90, pstyle('WBSentence', 'BrandSerif', 12.5, 21, INK))
    c.showPage()

    # 14 tear-out toolkit
    y = wb_header(c, 14, 'One-page toolkit', 'The open-door standard.', 'Keep this page. Use it in year-head, subject-department, student-support and leadership meetings.')
    promises = [
        ('KNOWN', TEAL, ['Name the adult.', 'Notice change quickly.', 'Repair after conflict.']),
        ('TAUGHT', ORANGE, ['Keep the ceiling high.', 'Model the hidden steps.', 'Feedback creates another attempt.']),
        ('PRESENT', GREEN, ['Act before 20 days.', 'Ask before assuming.', 'Review the small plan.']),
        ('PARTNERED', PURPLE, ['Strength before concern.', 'Make contact accessible.', 'End with one agreed step.']),
        ('FUTURE-READY', RED, ['Map A, B and C.', 'Check funding and access.', 'Name the adult and deadline.']),
    ]
    y -= 2
    for i,(head,col,items) in enumerate(promises):
        c.setFillColor(col); c.roundRect(42, y-88, 116, 82, 12, fill=1, stroke=0)
        c.setFillColor(PAPER); c.setFont('Helvetica-Bold', 8); c.drawCentredString(100, y-31, head)
        c.setFont('BrandSerif', 22); c.drawCentredString(100, y-62, str(i+1).zfill(2))
        yy = y-20
        for item in items:
            c.setFillColor(INK); c.setFont('Helvetica', 9.2); c.drawString(185, yy, '•  '+item)
            yy -= 23
        draw_rule(c, 185, y-82, w-42, LINE, 0.7)
        y -= 98
    round_box(c, 42, 86, w-84, 90, PAPER, OUTLINE, 12, 1)
    para(c, '<b>Monday:</b> ____________________________________   <b>Owner:</b> ____________________<br/><br/><b>Review date:</b> _________________________________',
         60, 150, w-120, 58, pstyle('WBMonday', 'Helvetica', 9.5, 16, INK))
    c.showPage()

    # 15 references
    y = wb_header(c, 15, 'Sources + live information', 'Recheck pathways and statistics before reuse.', 'Figures and eligibility rules change. The links below are the primary starting points.')
    refs = [
        ('CSO child deprivation', SOURCES['cso_child']),
        ('Tusla attendance 2023/24', SOURCES['tusla_attendance']),
        ('DEIS Strategy to 2035', SOURCES['deis_strategy']),
        ('OECD PISA Ireland 2022', SOURCES['pisa']),
        ('HEA socioeconomic profiles', SOURCES['hea_profile']),
        ('ESRI teacher relationships', SOURCES['esri_relationships']),
        ('NEPS resources', SOURCES['neps_resources']),
        ('HEAR', SOURCES['hear']),
        ('SUSI', SOURCES['susi']),
        ('Apprenticeships', SOURCES['apprenticeship']),
    ]
    for head,url in refs:
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 8); c.drawString(42, y, head)
        para(c, url, 170, y+2, w-212, 30, pstyle('WBRefUrl', 'Helvetica', 5.7, 7.5, LABEL))
        draw_rule(c, 42, y-11, w-42, LINE, 0.5)
        y -= 45
    round_box(c, 42, 78, w-84, 80, PAPER, OUTLINE, 12, 1)
    para(c, '<b>Evidence note:</b> trauma-informed school evidence is still developing. This toolkit prioritises role-clear, low-risk practices aligned with NEPS and does not support ACE screening or diagnosis by school staff.',
         58, 135, w-116, 52, pstyle('WBEvidenceNote', 'Helvetica', 8.5, 13, RED))
    c.showPage()
    c.save()


def inspect_outputs():
    from pypdf import PdfReader
    result = {}
    for path in (DECK_PATH, GUIDE_PATH, WORKBOOK_PATH):
        reader = PdfReader(str(path))
        text_chars = sum(len((p.extract_text() or '')) for p in reader.pages)
        result[path.name] = {'pages': len(reader.pages), 'text_chars': text_chars, 'bytes': path.stat().st_size}
    return result


if __name__ == '__main__':
    build_deck()
    slide_images = render_deck_pages()
    build_facilitator_guide(slide_images)
    build_workbook()
    print(inspect_outputs())
