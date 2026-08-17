"""Nurturing Potential workshop deck — ground-up rebuild (v2).

Design system: cream canvas, Georgia serif display, Helvetica text,
orange accent, five promise pastels. One layout engine, every slide
composed from the same primitives on a fixed grid.

Run:  python3 tmp/pdfs/build_deck_v2.py          (build + render QA pages)
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path('/Users/alexlinehan/Documents/Nextstepuni-Launch-')
TMP = ROOT / 'tmp' / 'pdfs'
OUT = ROOT / 'output' / 'pdf'
SHOTS = TMP / 'app_screens' / 'live_demo'
WORK = TMP / 'v2_screens'
ASSETS = ROOT / 'public' / 'assets'
DECK_PATH = OUT / 'Nurturing_Potential_Irish_Post_Primary_Workshop_Deck.pdf'
for d in (OUT, WORK):
    d.mkdir(parents=True, exist_ok=True)

W, H = 960, 540
MX = 52                      # side margin
CW = W - 2 * MX              # content width

# ---------------------------------------------------------------- palette
CANVAS = HexColor('#FAFBF6')
PAPER = HexColor('#FFFFFF')
INK = HexColor('#1A1A1A')
DARK_BG = HexColor('#181715')
MUTED = HexColor('#5F5A55')
LABEL = HexColor('#8A8178')
ORANGE = HexColor('#F26B1F')
TEAL = HexColor('#2F6F6D')
GREEN = HexColor('#4D7969')
PURPLE = HexColor('#735D9D')
RED = HexColor('#B75353')
OCHRE = HexColor('#B27A2D')
OUTLINE = HexColor('#383838')
LINE = HexColor('#D8D3CD')
TRACK = HexColor('#EAE5DC')
PALE_ORANGE = HexColor('#F9D8C4')
PALE_GREEN = HexColor('#D6E8DC')
PALE_BLUE = HexColor('#D9E7EE')
PALE_PURPLE = HexColor('#E2DCF0')
PALE_RED = HexColor('#EFD9D7')
BLOB_PEACH = HexColor('#F7DBC6')

# promise palette: (pale fill, accent) — Known, Taught, Present, Partnered, Future-ready
PROMISES = [(PALE_BLUE, TEAL), (PALE_ORANGE, ORANGE), (PALE_GREEN, GREEN),
            (PALE_PURPLE, PURPLE), (PALE_RED, RED)]

SER, SERB, SERI, SERBI = 'Serif', 'SerifB', 'SerifI', 'SerifBI'
SANS, SANSB = 'Helvetica', 'Helvetica-Bold'
SANSO = 'Helvetica-Oblique'


def register_fonts():
    base = Path('/System/Library/Fonts/Supplemental')
    for name, fn in ((SER, 'Georgia.ttf'), (SERB, 'Georgia Bold.ttf'),
                     (SERI, 'Georgia Italic.ttf'), (SERBI, 'Georgia Bold Italic.ttf')):
        pdfmetrics.registerFont(TTFont(name, str(base / fn)))
    pdfmetrics.registerFontFamily(SER, normal=SER, bold=SERB, italic=SERI, boldItalic=SERBI)


# ---------------------------------------------------------------- text utils
def sw(text, font, size):
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text, font, size, width):
    """Greedy word wrap → list of lines."""
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


def text_block(c, text, x, y_top, width, font=SANS, size=13, leading=None,
               color=INK, align='left', max_lines=None):
    """Draw wrapped text from its top edge. Returns height used."""
    leading = leading or size * 1.42
    lines = wrap(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    c.setFont(font, size)
    c.setFillColor(color)
    y = y_top - size * 0.85
    for ln in lines:
        if align == 'center':
            c.drawCentredString(x + width / 2, y, ln)
        elif align == 'right':
            c.drawRightString(x + width, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= leading
    return len(lines) * leading


def rich_block(c, runs, x, y_top, width, size=13, leading=None, align='left'):
    """runs: list of (text, font, color). Wraps across runs. Returns height."""
    leading = leading or size * 1.45
    words = []
    for text, font, color in runs:
        for w_ in text.split():
            words.append((w_, font, color))
    lines, cur, cur_w = [], [], 0.0
    space = sw(' ', SANS, size)
    for w_, font, color in words:
        ww = sw(w_, font, size)
        if cur and cur_w + space + ww > width:
            lines.append(cur)
            cur, cur_w = [], 0.0
        cur_w += (space if cur else 0) + ww
        cur.append((w_, font, color))
    if cur:
        lines.append(cur)
    y = y_top - size * 0.85
    for line in lines:
        total = sum(sw(t, f, size) for t, f, _ in line) + space * (len(line) - 1)
        if align == 'center':
            cx = x + (width - total) / 2
        elif align == 'right':
            cx = x + width - total
        else:
            cx = x
        for t, f, col in line:
            c.setFont(f, size)
            c.setFillColor(col)
            c.drawString(cx, y, t)
            cx += sw(t, f, size) + space
        y -= leading
    return len(lines) * leading


def kicker_width(text, size=9, tracking=1.9):
    t = text.upper()
    return sw(t, SANSB, size) + tracking * max(len(t) - 1, 0)


def kicker(c, text, x=MX, y=H - 42, color=LABEL, size=9):
    tx = c.beginText(x, y)
    tx.setFont(SANSB, size)
    tx.setFillColor(color)
    tx.setCharSpace(1.9)
    tx.textOut(text.upper())
    tx.setCharSpace(0)   # Tc persists across BT/ET in the content stream — reset inside
    c.drawText(tx)


def headline(c, text, x=MX, y_top=H - 62, width=CW, size=31, color=INK):
    """Serif display title from top. Returns y of baseline area bottom."""
    lines = wrap(text, SER, size, width)
    c.setFont(SER, size)
    c.setFillColor(color)
    y = y_top - size * 0.9
    for ln in lines:
        c.drawString(x, y, ln)
        y -= size * 1.18
    return y + size * 1.18 - 10   # bottom edge of title block


def footer(c, source, page_no, dark=False):
    col = HexColor('#8A867E') if not dark else HexColor('#8F8B84')
    if source:
        c.setFont(SANS, 7.5)
        c.setFillColor(col)
        c.drawString(MX, 22, source)
    if page_no:
        c.setFont(SANS, 8)
        c.setFillColor(col)
        c.drawRightString(W - MX, 22, f'{page_no:02d}')


# ---------------------------------------------------------------- shapes
def round_box(c, x, y, w, h, fill=PAPER, stroke=OUTLINE, radius=14,
              line_width=1.4, shadow=True):
    if shadow:
        c.setFillColor(HexColor('#1A1A1A'))
        c.roundRect(x + 3, y - 3, w, h, radius, stroke=0, fill=1)
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(line_width)
        c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    else:
        c.roundRect(x, y, w, h, radius, stroke=0, fill=1)


def soft_box(c, x, y, w, h, fill, radius=14):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, radius, stroke=0, fill=1)


def pill(c, cx_center, y, text_runs, size=12, pad_x=22, pad_y=11, fill=INK,
         max_w=CW):
    total = sum(sw(t, f, size) for t, f, _ in text_runs)
    w = min(total + 2 * pad_x, max_w)
    h = size + 2 * pad_y
    x = cx_center - w / 2
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, h / 2, stroke=0, fill=1)
    tx = x + (w - total) / 2
    for t, f, col in text_runs:
        c.setFont(f, size)
        c.setFillColor(col)
        c.drawString(tx, y + pad_y + size * 0.12, t)
        tx += sw(t, f, size)
    return h


def chip(c, x, y, text, fill, color, size=8.5, pad=8):
    w = sw(text, SANSB, size) + 2 * pad
    h = size + 11
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, h / 2, stroke=0, fill=1)
    c.setFont(SANSB, size)
    c.setFillColor(color)
    c.drawString(x + pad, y + 5.5, text)
    return w


def number_dot(c, n, cx, cy, fill=ORANGE, r=13, text_color=PAPER, size=9.5):
    c.setFillColor(fill)
    c.circle(cx, cy, r, stroke=0, fill=1)
    c.setFont(SANSB, size)
    c.setFillColor(text_color)
    c.drawCentredString(cx, cy - size * 0.36, f'{n:02d}')


def blob(c, cx, cy, rx, ry, fill):
    c.saveState()
    c.setFillColor(fill)
    c.translate(cx, cy)
    p = c.beginPath()
    p.moveTo(-rx, 0)
    p.curveTo(-rx, ry * 0.62, -rx * 0.55, ry, 0.05 * rx, ry * 0.94)
    p.curveTo(rx * 0.68, ry * 0.86, rx, ry * 0.42, rx * 0.94, -0.12 * ry)
    p.curveTo(rx * 0.86, -ry * 0.72, rx * 0.38, -ry, -0.1 * rx, -ry * 0.92)
    p.curveTo(-rx * 0.62, -ry * 0.82, -rx, -ry * 0.5, -rx, 0)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def draw_icon(c, path, x, y, w, h):
    c.drawImage(ImageReader(str(path)), x, y, w, h, mask='auto',
                preserveAspectRatio=True, anchor='c')


def device(c, key, x, y, w, h=None, radius=12, border=True):
    """Draw prepped screenshot scaled to width w (or fit box w×h), rounded."""
    img_path = WORK / f'{key}.png'
    with Image.open(img_path) as im:
        iw, ih = im.size
    scale = w / iw
    dh = ih * scale
    if h and dh > h:
        scale = h / ih
        dh = h
        dw = iw * scale
        x = x + (w - dw) / 2
        w = dw
    # chunky shadow
    c.setFillColor(HexColor('#1A1A1A'))
    c.roundRect(x + 4, y - 4, w, dh, radius, stroke=0, fill=1)
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, dh, radius)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(PAPER)
    c.rect(x, y, w, dh, stroke=0, fill=1)
    c.drawImage(ImageReader(str(img_path)), x, y, w, dh, mask='auto')
    c.restoreState()
    if border:
        c.setStrokeColor(OUTLINE)
        c.setLineWidth(1.6)
        c.roundRect(x, y, w, dh, radius, stroke=1, fill=0)
    return dh


# ---------------------------------------------------------------- screenshots
SCREEN_SPECS = {
    # key: (file, crop L,U,R,Low  or None, [patch rects (l,u,r,low, fill|sample xy)])
    'home':        ('01-home.png', (0, 0, 1126, 690), []),
    'modules':     ('02-modules.png', None, [((331, 394, 360, 432), (382, 412))]),
    'study':       ('03-study-session-mathematics.png', None,
                    [((733, 418, 782, 460), (860, 430))]),
    'launchpad':   ('04-launchpad-all.png', (0, 0, 1126, 760),
                    [((833, 334, 878, 378), (912, 352))]),
    'dash_hero':   ('09-dashboard-overview.png', (0, 0, 1126, 480), []),
    'climbs':      ('09-dashboard-overview.png', (36, 1460, 1090, 2168), []),
    'journey':     ('10-journey-mode.png', (300, 250, 860, 710), []),
    'shop':        ('12-build-shop.png', (360, 0, 1126, 763), []),
    'markbank':    ('14-mark-bank-index.png', (0, 0, 1126, 545), []),
    'marksession': ('15-mark-bank-session.png', (0, 0, 1126, 760), []),
    'paths':       ('19-learning-paths.png', (0, 0, 1126, 510),
                    [((834, 412, 880, 454), '#FFFFFF')]),
}


def prep_screens():
    for key, (fn, crop, patches) in SCREEN_SPECS.items():
        im = Image.open(SHOTS / fn).convert('RGB')
        for rect, fill in patches:
            if isinstance(fill, tuple):
                fill = im.getpixel(fill)
            else:
                fill = tuple(int(fill[i:i + 2], 16) for i in (1, 3, 5))
            im.paste(Image.new('RGB', (rect[2] - rect[0], rect[3] - rect[1]), fill),
                     (rect[0], rect[1]))
        if crop:
            im = im.crop(crop)
        im.save(WORK / f'{key}.png')


# ---------------------------------------------------------------- slide shell
PAGE = {'n': 0}


def begin(c, kick, title=None, dark=False, title_size=31, no_number=False):
    PAGE['n'] += 1
    c.setFillColor(DARK_BG if dark else CANVAS)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    if kick:
        kicker(c, kick, color=ORANGE if dark else LABEL)
    bottom = H - 62
    if title:
        bottom = headline(c, title, size=title_size,
                          color=PAPER if dark else INK)
    return bottom  # y under the title block


# =================================================================== slides
def s01_title(c):
    begin(c, 'Nurturing Potential', None, no_number=True)
    # right illustration
    blob(c, 730, 300, 150, 138, BLOB_PEACH)
    draw_icon(c, ASSETS / 'section-icons' / 'my-journey.png', 620, 195, 220, 220)
    # left text
    c.setFont(SER, 52)
    c.setFillColor(INK)
    c.drawString(MX, 372, 'Keep the door')
    c.drawString(MX, 314, 'open.')
    text_block(c, 'Helping every young person succeed in second-level '
                  'education and navigate a future beyond it.',
               MX, 248, 400, font=SANS, size=15, leading=23, color=MUTED)
    c.setStrokeColor(INK)
    c.setLineWidth(1.2)
    c.line(MX, 168, MX + 340, 168)
    c.setFont(SANSB, 11)
    c.setFillColor(INK)
    c.drawString(MX, 144, 'An Irish post-primary workshop for teachers,')
    c.drawString(MX, 128, 'year heads and school leaders')
    footer(c, '', None)


def s02_person(c):
    begin(c, '', None)
    kicker(c, 'Start here', x=W / 2 - kicker_width('Start here') / 2, y=352)
    c.setFont(SER, 40)
    c.setFillColor(INK)
    c.drawCentredString(W / 2, 282, 'Before the data, a person.')
    c.setFont(SERI, 15)
    c.setFillColor(MUTED)
    c.drawCentredString(W / 2, 236, 'A story from inside the system.')
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2.4)
    c.line(W / 2 - 36, 208, W / 2 + 36, 208)
    footer(c, 'Your lived experience leads; the evidence follows.', PAGE['n'])


def s03_question(c):
    top = begin(c, 'A quiet question', 'Who changed your odds?')
    cards = [('Who noticed?', 'Who saw more than the label, the result or the difficult week?'),
             ('What repeated?', 'What did they keep doing — quietly, reliably, more than once?'),
             ('What opened?', 'Which choice, confidence or future became easier to imagine?')]
    cw_, gut = (CW - 2 * 24) / 3, 24
    ch, cy = 240, 132
    for i, (t, d) in enumerate(cards):
        x = MX + i * (cw_ + gut)
        fill, accent = PROMISES[i if i < 2 else 2]
        round_box(c, x, cy, cw_, ch, fill=fill, stroke=OUTLINE)
        number_dot(c, i + 1, x + 30, cy + ch - 32, fill=accent)
        c.setFont(SER, 21)
        c.setFillColor(INK)
        c.drawString(x + 20, cy + ch - 82, t)
        c.setStrokeColor(accent)
        c.setLineWidth(2)
        c.line(x + 20, cy + ch - 98, x + cw_ - 20, cy + ch - 98)
        text_block(c, d, x + 20, cy + ch - 116, cw_ - 40, size=12.5,
                   leading=19, color=MUTED)
    pill(c, W / 2, 66, [('Think privately. ', SANSB, PAPER),
                        ('If invited, share the practice — not the person.', SANS, PAPER)])
    footer(c, 'No one is required to disclose a personal experience.', PAGE['n'])


def s04_deprivation(c):
    begin(c, 'The starting line', 'One in seven.')
    # left: hero stat
    c.setFont(SER, 92)
    c.setFillColor(ORANGE)
    c.drawString(MX, 260, '13.8%')
    text_block(c, 'of children lived in households experiencing child-specific '
                  'enforced deprivation in 2024.',
               MX, 238, 330, size=13.5, leading=20, color=MUTED)
    # secondary contrast
    soft_box(c, MX, 92, 372, 74, PALE_ORANGE, radius=12)
    rich_block(c, [('54.2% ', SERB, INK), ('where no adult in the home works — ',
                                           SANS, HexColor('#7A4A24')),
                   ('3.7% ', SERB, INK), ('where two do.', SANS, HexColor('#7A4A24'))],
               MX + 18, 152, 336, size=12.5, leading=19)
    # divider
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.line(492, 96, 492, 356)
    # right: definition
    text_block(c, 'The measure: a household could not afford at least three of '
                  '17 child-specific essentials or activities.',
               524, 350, 372, font=SER, size=19, leading=28, color=INK)
    text_block(c, 'It describes the conditions around a childhood — never a '
                  'child’s capacity.',
               524, 240, 360, font=SANSB, size=13, leading=20, color=TEAL)
    footer(c, 'Source: CSO, SILC Module on Child Deprivation 2024.', PAGE['n'])


def s05_absence(c):
    begin(c, 'Where inequality accumulates', 'Absence compounds quietly.')
    # two bars
    base_y, max_h, bw = 108, 240, 150
    for i, (pct, col, lab) in enumerate((('18.6', TEAL, 'Non-DEIS'),
                                         ('28.3', ORANGE, 'DEIS'))):
        x = MX + 48 + i * (bw + 60)
        c.setFillColor(TRACK)
        c.roundRect(x, base_y, bw, max_h, 16, stroke=0, fill=1)
        fh = max_h * float(pct) / 40.0
        c.setFillColor(col)
        c.roundRect(x, base_y, bw, fh, 16, stroke=0, fill=1)
        c.setFont(SER, 34)
        c.setFillColor(col)
        c.drawCentredString(x + bw / 2, base_y + max_h + 18, pct + '%')
        c.setFont(SANSB, 13)
        c.setFillColor(INK)
        c.drawCentredString(x + bw / 2, base_y - 26, lab)
    c.setFont(SANS, 10.5)
    c.setFillColor(MUTED)
    c.drawCentredString(MX + 48 + bw + 30, 66,
                        'Students missing 20+ days, post-primary, 2023/24')
    # right cards
    rx, rw = 588, 320
    round_box(c, rx, 258, rw, 108, fill=PAPER)
    kicker(c, 'The reported gap', x=rx + 22, y=336, color=ORANGE)
    c.setFont(SER, 40)
    c.setFillColor(ORANGE)
    c.drawString(rx + 22, 282, '9.7')
    rich_block(c, [('percentage points ', SANSB, INK),
                   ('separate the two rates.', SANS, MUTED)],
               rx + 108, 312, rw - 130, size=12.5, leading=18)
    round_box(c, rx, 118, rw, 114, fill=PALE_BLUE)
    c.setFont(SER, 22)
    c.setFillColor(TEAL)
    c.drawString(rx + 22, 196, '20+ days ≈ four school weeks.')
    text_block(c, 'Support should begin when the pattern emerges — not at the '
                  'threshold.',
               rx + 22, 182, rw - 44, size=11.5, leading=16.5, color=INK)
    footer(c, 'Source: Tusla, Analysis of School Attendance Data 2023/24. '
              'Post-primary response coverage: 541 of 722 schools.', PAGE['n'])


def s06_pisa(c):
    begin(c, 'The same dataset holds two truths',
          'Background shifts the odds. It does not write the outcome.')
    cw_, gut, ch, cy = (CW - 40) / 2, 40, 210, 140
    x = MX
    round_box(c, x, cy, cw_, ch, fill=PAPER)
    c.setFont(SER, 58)
    c.setFillColor(RED)
    c.drawString(x + 28, cy + ch - 84, '74')
    text_block(c, 'maths points separated Ireland’s most and least '
                  'socio-economically advantaged quarters in PISA 2022.',
               x + 28, cy + ch - 108, cw_ - 56, size=13, leading=19, color=MUTED)
    x = MX + cw_ + gut
    round_box(c, x, cy, cw_, ch, fill=PAPER)
    c.setFont(SER, 58)
    c.setFillColor(TEAL)
    c.drawString(x + 28, cy + ch - 84, '12%')
    text_block(c, 'of disadvantaged students were academically resilient — '
                  'scoring in Ireland’s top quarter.',
               x + 28, cy + ch - 108, cw_ - 56, size=13, leading=19, color=MUTED)
    rich_block(c, [('Ireland’s gap is smaller than the OECD average (93 points) — ',
                    SANS, MUTED),
                   ('and it narrowed between 2012 and 2022.', SANSB, TEAL)],
               MX, 104, CW, size=13, leading=19, align='center')
    footer(c, 'Source: OECD, PISA 2022 Results — Ireland country note. Interpret with '
              'the OECD’s response-rate caveat for Ireland.', PAGE['n'])


def s07_routes(c):
    begin(c, 'Opportunity includes navigation',
          'The route into higher education is uneven.')
    # left insight card
    lw = 268
    soft_box(c, MX, 96, lw, 268, HexColor('#FBEFE3'), radius=18)
    kicker(c, 'The navigation gap', x=MX + 22, y=332, color=ORANGE)
    c.setFont(SER, 24)
    c.setFillColor(INK)
    c.drawString(MX + 22, 288, 'Routes need')
    c.setFont(SERB, 24)
    c.drawString(MX + 22, 258, 'equal visibility.')
    rows = [('Points / CAO', PALE_ORANGE, ORANGE), ('FET / PLC', PALE_GREEN, GREEN),
            ('Mature / HEAR', PALE_BLUE, TEAL)]
    ry = 206
    for i, (t, fill, accent) in enumerate(rows):
        soft_box(c, MX + 22, ry - i * 46, lw - 44, 36, fill, radius=18)
        number_dot(c, i + 1, MX + 44, ry - i * 46 + 18, fill=accent, r=10, size=8)
        c.setFont(SANSB, 11.5)
        c.setFillColor(INK)
        c.drawString(MX + 62, ry - i * 46 + 13, t)
    c.setFont(SANSB, 12)
    c.setFillColor(GREEN)
    c.drawCentredString(MX + lw / 2, 74, 'Different routes are not lesser.')
    # right: grouped bars
    bx, bw_full = 392, 470
    groups = [('Second-level exams', 61, 78), ('FET award', 9, 4),
              ('Mature + HEAR', 19, 4)]
    gy = 330
    for label, dis, aff in groups:
        c.setFont(SANSB, 12)
        c.setFillColor(INK)
        c.drawString(bx, gy + 6, label)
        for j, (v, col) in enumerate(((dis, ORANGE), (aff, TEAL))):
            yy = gy - 12 - j * 24
            c.setFillColor(TRACK)
            c.roundRect(bx, yy, bw_full, 15, 7.5, stroke=0, fill=1)
            fw = max(bw_full * v / 100.0, 20)
            c.setFillColor(col)
            c.roundRect(bx, yy, fw, 15, 7.5, stroke=0, fill=1)
            c.setFillColor(PAPER)
            c.circle(bx + fw, yy + 7.5, 12, stroke=0, fill=1)
            c.setStrokeColor(LINE)
            c.setLineWidth(0.8)
            c.circle(bx + fw, yy + 7.5, 12, stroke=1, fill=0)
            c.setFont(SANSB, 9.5)
            c.setFillColor(INK)
            c.drawCentredString(bx + fw, yy + 4.2, f'{v}%')
        gy -= 86
    # legend
    ly = 78
    c.setFillColor(ORANGE)
    c.circle(bx + 10, ly, 5, stroke=0, fill=1)
    c.setFont(SANS, 10.5)
    c.setFillColor(MUTED)
    c.drawString(bx + 22, ly - 3.5, 'Disadvantaged entrants')
    c.setFillColor(TEAL)
    c.circle(bx + 190, ly, 5, stroke=0, fill=1)
    c.drawString(bx + 202, ly - 3.5, 'Affluent entrants')
    footer(c, 'Source: HEA socio-economic student profile, undergraduate new entrants '
              '2021/22–2023/24. Categories shown do not exhaust all entry routes.',
           PAGE['n'])


def s08_doors(c):
    begin(c, 'The pattern', 'Not one wall. Four quiet doors.')
    doors = [('13.8%', 'GROWING UP', 'of children in enforced deprivation', PALE_BLUE, TEAL, 300),
             ('9.7pp', 'SHOWING UP', 'wider 20+ day absence rate in DEIS schools', PALE_ORANGE, ORANGE, 268),
             ('7.7pp', 'FINISHING', 'retention gap to the Leaving Certificate', PALE_GREEN, GREEN, 236),
             ('61v78', 'PROGRESSING', 'direct-route entry, disadvantaged vs affluent', PALE_RED, RED, 204)]
    dw, gut = 176, 28
    x0 = MX + (CW - (4 * dw + 3 * gut)) / 2
    floor = 120
    def arch(px, py, pw, ph, r, fill_col, stroke_col=None, lw=1.4):
        p = c.beginPath()
        p.moveTo(px, py)
        p.lineTo(px, py + ph - r)
        p.curveTo(px, py + ph - r * 0.45, px + r * 0.45, py + ph, px + r, py + ph)
        p.lineTo(px + pw - r, py + ph)
        p.curveTo(px + pw - r * 0.45, py + ph, px + pw, py + ph - r * 0.45,
                  px + pw, py + ph - r)
        p.lineTo(px + pw, py)
        p.close()
        c.setFillColor(fill_col)
        if stroke_col:
            c.setStrokeColor(stroke_col)
            c.setLineWidth(lw)
            c.drawPath(p, stroke=1, fill=1)
        else:
            c.drawPath(p, stroke=0, fill=1)

    for i, (num, lab, desc, fill, accent, dh) in enumerate(doors):
        x = x0 + i * (dw + gut)
        arch(x + 3, floor - 3, dw, dh, 42, HexColor('#1A1A1A'))
        arch(x, floor, dw, dh, 42, fill, OUTLINE)
        kicker(c, lab, x=x + 18, y=floor + dh - 34, color=accent, size=8)
        if num == '61v78':
            c.setFont(SER, 27)
            c.setFillColor(INK)
            c.drawString(x + 18, floor + dh - 74, '61%')
            c.setFont(SANS, 13)
            c.setFillColor(MUTED)
            c.drawString(x + 72, floor + dh - 74, 'vs')
            c.setFont(SER, 27)
            c.setFillColor(INK)
            c.drawString(x + 92, floor + dh - 74, '78%')
        else:
            c.setFont(SER, 33)
            c.setFillColor(INK)
            c.drawString(x + 18, floor + dh - 78, num)
        text_block(c, desc, x + 18, floor + dh - 96, dw - 34, size=10.5,
                   leading=15, color=MUTED)
    # floor line
    c.setStrokeColor(OUTLINE)
    c.setLineWidth(1.6)
    c.line(x0 - 24, floor, x0 + 4 * dw + 3 * gut + 24, floor)
    rich_block(c, [('Four separate national measures. One direction of travel. ',
                    SANSB, INK),
                   ('Each door can be held open — that is the rest of this workshop.',
                    SANS, TEAL)],
               MX, 84, CW, size=13, leading=19, align='center')
    footer(c, 'Synthesis of the preceding measures: CSO 2024 · Tusla 2023/24 · '
              'DoE retention, 2018 entry cohort · HEA 2021/22–2023/24.', PAGE['n'])


def s09_stereotype(c):
    begin(c, 'The danger in the story we tell',
          'Data can sharpen action — or harden a stereotype.')
    rows = [('“They do not value school.”', '“What makes attendance harder here?”'),
            ('“The family will not engage.”', '“How accessible and trustworthy is our contact?”'),
            ('“Not college material.”', '“Which routes and supports are still invisible?”'),
            ('“Trauma explains the behaviour.”', '“What supports regulation and a return to learning?”')]
    col2 = MX + 420
    kicker(c, 'The quick conclusion', x=MX, y=372, color=RED)
    kicker(c, 'The useful question', x=col2, y=372, color=TEAL)
    y = 330
    for a, b in rows:
        c.setFont(SERI, 15.5)
        c.setFillColor(MUTED)
        c.drawString(MX, y, a)
        c.setFont(SANSB, 13.5)
        c.setFillColor(INK)
        c.drawString(col2, y, b)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.line(MX, y - 22, W - MX, y - 22)
        y -= 64
    footer(c, 'Principle: ask about barriers without lowering expectations or removing '
              'accountability.', PAGE['n'])


def s10_progress(c):
    begin(c, 'A system can move', 'Progress is real. The remaining gap is real.')
    # gap timeline
    ty = 300
    c.setStrokeColor(OUTLINE)
    c.setLineWidth(2)
    c.line(MX + 40, ty, W - MX - 40, ty)
    pts = [(MX + 90, '≈17pp', '2001 entry cohort', 'retention gap', ORANGE, 15),
           (W - MX - 130, '7.7pp', '2018 entry cohort', 'retention gap', TEAL, 15)]
    for px, big, l1, l2, col, r in pts:
        c.setFillColor(col)
        c.circle(px, ty, r, stroke=0, fill=1)
        c.setFont(SER, 40)
        c.setFillColor(col)
        c.drawCentredString(px, ty + 42, big)
        c.setFont(SANSB, 11)
        c.setFillColor(INK)
        c.drawCentredString(px, ty - 40, l1)
        c.setFont(SANS, 10.5)
        c.setFillColor(MUTED)
        c.drawCentredString(px, ty - 55, l2)
    # halving arrow annotation
    c.setFont(SERI, 15)
    c.setFillColor(MUTED)
    c.drawCentredString(W / 2, ty + 26, 'the DEIS / non-DEIS gap has more than halved')
    # latest cohort dots
    rich_block(c, [('2018 entry cohort:  ', SANSB, INK),
                   ('DEIS 84.1%', SERB, ORANGE), ('   ·   ', SANS, MUTED),
                   ('non-DEIS 91.8%', SERB, TEAL),
                   ('   stayed to the Leaving Certificate.', SANS, MUTED)],
               MX, 178, CW, size=15, leading=22, align='center')
    rich_block(c, [('PISA tells the same story: ', SANS, MUTED),
                   ('Ireland’s socio-economic gap in maths narrowed between '
                    '2012 and 2022.', SANSB, TEAL)],
               MX, 120, CW, size=12.5, leading=18, align='center')
    footer(c, 'Sources: Department of Education, retention of the 2018 entry cohort '
              '(July 2026); gap halved since the 2001 cohort. OECD PISA 2022.', PAGE['n'])


def s11_adult(c):
    begin(c, 'The turn', 'The adult is the variable.')
    round_box(c, MX, 148, CW, 202, fill=PAPER)
    kicker(c, 'What the Irish evidence points to', x=MX + 30, y=316, color=ORANGE)
    text_block(c, 'Students who grew up economically vulnerable needed positive '
                  'teacher relationships in early secondary school to reach the '
                  'same attainment as better-off peers — even when their '
                  'parents held high expectations.',
               MX + 30, 296, CW - 60, font=SER, size=19.5, leading=29, color=INK)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2.4)
    c.line(MX + 30, 182, MX + 330, 182)
    c.setFont(SANS, 11)
    c.setFillColor(MUTED)
    c.drawString(MX + 30, 162, 'Growing Up in Ireland ’98 cohort, ~8,500 young people '
                               'followed from age 9 to 20.')
    pill(c, W / 2, 84, [('The relationship is not the soft part of the job. ', SANSB, PAPER),
                        ('It is the mechanism.', SANS, PAPER)], size=12.5)
    footer(c, 'Source: Dempsey & McCoy (2025), ESRI / Growing Up in Ireland; British '
              'Journal of Educational Psychology.', PAGE['n'])


def s12_pivot(c):
    begin(c, 'The pivot', 'Five promises that change the odds.', dark=True)
    names = ['Known', 'Taught', 'Present', 'Partnered', 'Future-ready']
    n = 5
    cx0, cxn = MX + 70, W - MX - 70
    step = (cxn - cx0) / (n - 1)
    cy = 268
    c.setStrokeColor(HexColor('#4A463F'))
    c.setLineWidth(2)
    c.line(cx0, cy, cxn, cy)
    for i, name in enumerate(names):
        fill, accent = PROMISES[i]
        cx = cx0 + i * step
        c.setFillColor(fill)
        c.circle(cx, cy, 40, stroke=0, fill=1)
        c.setFont(SANSB, 12)
        c.setFillColor(INK)
        c.drawCentredString(cx, cy - 4.5, f'0{i + 1}')
        c.setFont(SER, 20)
        c.setFillColor(PAPER)
        c.drawCentredString(cx, cy - 82, name)
    c.setFont(SANS, 14.5)
    c.setFillColor(HexColor('#C9C4BC'))
    c.drawCentredString(W / 2, 112, 'Not five programmes. Five dependable experiences of school.')
    footer(c, 'A practical synthesis aligned with DEIS planning, the NEPS Continuum of '
              'Support and Irish evidence.', PAGE['n'], dark=True)


def s13_known(c):
    begin(c, 'Promise 01 · Known', 'Relationships are learning infrastructure.')
    # left summary card
    lw = 330
    round_box(c, MX, 96, lw, 268, fill=PAPER)
    kicker(c, 'The promise', x=MX + 24, y=332, color=TEAL)
    text_block(c, 'Every student is known by name, noticed early and met with '
                  'strengths first.',
               MX + 24, 312, lw - 48, font=SER, size=18, leading=26, color=INK)
    c.setStrokeColor(TEAL)
    c.setLineWidth(2.2)
    c.line(MX + 24, 210, MX + 220, 210)
    rich_block(c, [('School cannot remove every external pressure. ', SANS, MUTED),
                   ('It can make sure no student becomes invisible.', SANSB, INK)],
               MX + 24, 192, lw - 48, size=12.5, leading=18.5)
    # right 2×2
    items = [('Name', 'One reliable adult the student can identify.'),
             ('Notice', 'Absence, withdrawal and change trigger contact.'),
             ('Repair', 'Conflict has a dignified route back to learning.'),
             ('Record', 'Support begins with strengths and what works.')]
    gx, gy, gw = MX + lw + 28, 96, CW - lw - 28
    cw_, ch_ = (gw - 20) / 2, 124
    for i, (t, d) in enumerate(items):
        x = gx + (i % 2) * (cw_ + 20)
        y = gy + (1 - i // 2) * (ch_ + 20)
        fill, accent = PROMISES[i % 4 if i < 2 else (i + 1) % 4]
        fill, accent = [(PALE_BLUE, TEAL), (PALE_ORANGE, ORANGE),
                        (PALE_GREEN, GREEN), (PALE_PURPLE, PURPLE)][i]
        round_box(c, x, y, cw_, ch_, fill=fill)
        number_dot(c, i + 1, x + 26, y + ch_ - 28, fill=accent, r=11, size=8.5)
        c.setFont(SER, 18)
        c.setFillColor(INK)
        c.drawString(x + 44, y + ch_ - 34, t)
        text_block(c, d, x + 18, y + ch_ - 56, cw_ - 36, size=11.5,
                   leading=16.5, color=MUTED)
    footer(c, 'Source: ESRI / Growing Up in Ireland research on relationships, '
              'self-concept and attainment.', PAGE['n'])


def s14_trauma(c):
    begin(c, 'Promise 01 · Known', 'Care without lowering the ceiling.')
    c.setFont(SERI, 15.5)
    c.setFillColor(MUTED)
    c.drawCentredString(W / 2, 372, 'Respond to what is observable. Refer what is not ours to assess.')
    pw = (CW - 28) / 2
    py, ph = 96, 250
    # left green
    soft_box(c, MX, py, pw, ph, PALE_GREEN, radius=18)
    kicker(c, 'Stability we can design', x=MX + 24, y=py + ph - 28, color=GREEN)
    rows = [('Predictability', 'routines and transitions'),
            ('Choice', 'within clear boundaries'),
            ('Regulate', 'before reasoning'),
            ('Return', 'a dignified route back'),
            ('Refer', 'through the support system')]
    y = py + ph - 62
    for i, (t, d) in enumerate(rows):
        number_dot(c, i + 1, MX + 36, y + 5, fill=GREEN, r=9.5, size=7.5)
        c.setFont(SANSB, 12.5)
        c.setFillColor(INK)
        c.drawString(MX + 54, y, t)
        c.setFont(SANS, 11)
        c.setFillColor(MUTED)
        c.drawString(MX + 176, y, d)
        y -= 38
    # right red
    rx = MX + pw + 28
    soft_box(c, rx, py, pw, ph, PALE_RED, radius=18)
    kicker(c, 'Lines we do not cross', x=rx + 24, y=py + ph - 28, color=RED)
    rows = [('ACE scores', 'do not collect or display'),
            ('Diagnosis', 'do not infer from behaviour'),
            ('Disclosure', 'do not demand a private story'),
            ('Boundaries', 'do not remove accountability'),
            ('Specialist care', 'do not attempt to replace it')]
    y = py + ph - 62
    for t, d in rows:
        c.setStrokeColor(RED)
        c.setLineWidth(3)
        c.line(rx + 28, y + 4, rx + 44, y + 4)
        c.setFont(SANSB, 12.5)
        c.setFillColor(INK)
        c.drawString(rx + 56, y, t)
        c.setFont(SANS, 11)
        c.setFillColor(MUTED)
        c.drawString(rx + 178, y, d)
        y -= 38
    rich_block(c, [('Notice → support → refer. ', SANSB, TEAL),
                   ('Keep the student’s privacy, dignity and future options intact.',
                    SANS, MUTED)],
               MX, 74, CW, size=12.5, leading=18, align='center')
    footer(c, 'Sources: NEPS trauma resources and Continuum of Support; Campbell '
              'systematic review; UK government caution on ACE screening.', PAGE['n'])


def s15_quadrant(c):
    begin(c, 'Promise 02 · Taught', 'High expectations need high support.')
    # quadrant left-centred
    qs = 250
    qx, qy = MX + 68, 96
    cells = [('A kind ceiling', 'Warm support; shrinking challenge', PALE_RED, 0, 1),
             ('Ambitious access', 'Challenge made reachable', PALE_GREEN, 1, 1),
             ('Abandonment', 'Low challenge; low support', HexColor('#F2EEE8'), 0, 0),
             ('Sink or swim', 'High demand; hidden route', PALE_ORANGE, 1, 0)]
    round_box(c, qx - 8, qy - 8, qs * 2 + 16, qs + 16 + qs * 0, fill=PAPER,
              shadow=True) if False else None
    for t, d, fill, ix, iy in cells:
        x, y = qx + ix * (qs + 4) / 1, qy + iy * (qs / 2 + 4)
        w_, h_ = qs, qs / 2
        x = qx + ix * (w_ + 4)
        soft_box(c, x, y, w_, h_, fill, radius=10)
        c.setFont(SANSB, 13.5)
        c.setFillColor(INK)
        c.drawCentredString(x + w_ / 2, y + h_ - 44, t)
        text_block(c, d, x + 24, y + h_ - 60, w_ - 48, size=11, leading=15,
                   color=MUTED, align='center')
    # axes
    c.setFont(SANSB, 10)
    c.setFillColor(LABEL)
    c.drawCentredString(qx + qs + 2, qy - 24, 'EXPECTATION  →')
    c.saveState()
    c.translate(qx - 26, qy + qs / 2 + 2)
    c.rotate(90)
    c.drawCentredString(0, 0, 'SUPPORT  →')
    c.restoreState()
    # right takeaway
    tx = qx + 2 * qs + 56
    tw = W - MX - tx
    rich_block(c, [('The goal is not “be tougher.” ', SER, INK),
                   ('The goal is to make ambitious work ', SER, INK),
                   ('legible, scaffolded and attainable.', SERB, INK)],
               tx, 320, tw, size=19, leading=28)
    footer(c, 'Workshop framework: distinguish demand from access, and care from '
              'lowered ceilings.', PAGE['n'])


def s16_route(c):
    begin(c, 'Promise 02 · Taught', 'Teach the route, not only the destination.')
    steps = [('Activate', 'What do we already know?'),
             ('Model', 'Think aloud; show a worked example.'),
             ('Guide', 'Practise together; fade support.'),
             ('Check', 'Hear from everyone, not only volunteers.'),
             ('Respond', 'Feedback changes the next attempt.'),
             ('Transfer', 'Plan, retrieve, monitor, evaluate.')]
    n = len(steps)
    cx0, cxn = MX + 52, W - MX - 52
    stepw = (cxn - cx0) / (n - 1)
    cy = 288
    c.setStrokeColor(LINE)
    c.setLineWidth(2)
    c.line(cx0, cy, cxn, cy)
    for i, (t, d) in enumerate(steps):
        cx = cx0 + i * stepw
        c.setFillColor(ORANGE if i % 2 else INK)
        c.circle(cx, cy, 26, stroke=0, fill=1)
        c.setFont(SANSB, 11)
        c.setFillColor(PAPER)
        c.drawCentredString(cx, cy - 4, f'0{i + 1}')
        c.setFont(SER, 17)
        c.setFillColor(INK)
        c.drawCentredString(cx, cy - 62, t)
        text_block(c, d, cx - stepw / 2 + 10, cy - 84, stepw - 20, size=10.5,
                   leading=15, color=MUTED, align='center')
    rich_block(c, [('Metacognition works best inside subject teaching: ', SANSB, TEAL),
                   ('model how an expert plans, monitors and evaluates a real task.',
                    SANS, TEAL)],
               MX + 60, 106, CW - 120, size=13, leading=19, align='center')
    footer(c, 'Sources: Education Endowment Foundation guidance on metacognition, '
              'self-regulation and feedback.', PAGE['n'])


def s17_produce(c):
    begin(c, 'Study Lab · optional depth', 'Studying is not the same as learning.')
    pw, ph, py = 320, 240, 104
    # left familiarity
    soft_box(c, MX, py, pw, ph, PALE_RED, radius=18)
    kicker(c, 'Familiarity', x=MX + 24, y=py + ph - 30, color=RED)
    c.setFont(SERI, 25)
    c.setFillColor(INK)
    c.drawString(MX + 24, py + ph - 74, '“I recognise it.”')
    rich_block(c, [('Useful for orientation. ', SANS, MUTED),
                   ('Not yet proof of recall.', SANSB, INK)],
               MX + 24, py + ph - 96, pw - 48, size=12, leading=17)
    for i, t in enumerate(('READ', 'COPY', 'WATCH')):
        bx = MX + 24 + i * 94
        round_box(c, bx, py + 22, 82, 52, fill=PAPER, stroke=None, shadow=False)
        c.setFont(SANSB, 11)
        c.setFillColor(RED)
        c.drawCentredString(bx + 41, py + 50, t)
        c.setFont(SANS, 10)
        c.setFillColor(MUTED)
        c.drawCentredString(bx + 41, py + 34, 'again')
    # middle test
    mw = 168
    mx_ = MX + pw + 24
    round_box(c, mx_, py + 52, mw, 136, fill=INK, stroke=None)
    kicker(c, 'The test', x=mx_ + 40, y=py + 156, color=ORANGE)
    c.setFont(SER, 18)
    c.setFillColor(PAPER)
    c.drawCentredString(mx_ + mw / 2, py + 116, 'Close the page.')
    c.setFont(SERB, 20)
    c.drawCentredString(mx_ + mw / 2, py + 88, 'Produce.')
    # right evidence
    rx = mx_ + mw + 24
    rw = W - MX - rx
    soft_box(c, rx, py, rw, ph, PALE_GREEN, radius=18)
    kicker(c, 'Evidence', x=rx + 24, y=py + ph - 30, color=GREEN)
    c.setFont(SERI, 25)
    c.setFillColor(INK)
    c.drawString(rx + 24, py + ph - 74, '“I can produce it.”')
    loop = [('Retrieve', 'without notes'), ('Check', 'against a source'),
            ('Repair', 'name the error'), ('Return', 'after a gap')]
    lx0 = rx + 40
    stepw = (rw - 80) / 3
    ly = py + 74
    c.setStrokeColor(HexColor('#B9CDБF'.replace('Б', 'B')))
    c.setStrokeColor(HexColor('#B9CDBF'))
    c.setLineWidth(1.6)
    c.line(lx0, ly, lx0 + 3 * stepw, ly)
    for i, (t, d) in enumerate(loop):
        cx = lx0 + i * stepw
        c.setFillColor([TEAL, ORANGE, GREEN, PURPLE][i])
        c.circle(cx, ly, 13, stroke=0, fill=1)
        c.setFont(SANSB, 8)
        c.setFillColor(PAPER)
        c.drawCentredString(cx, ly - 3, f'0{i + 1}')
        c.setFont(SANSB, 10.5)
        c.setFillColor(INK)
        c.drawCentredString(cx, ly - 32, t)
        c.setFont(SANS, 9)
        c.setFillColor(MUTED)
        c.drawCentredString(cx, ly - 46, d)
    rich_block(c, [('Input can orient. ', SANSB, INK),
                   ('Evidence shows what survived when the page disappeared.',
                    SANS, MUTED)],
               MX, 76, CW, size=12.5, leading=18, align='center')
    footer(c, 'Evidence base: IES practice guide on retrieval, spacing and worked '
              'examples; EEF metacognition guidance.', PAGE['n'])


def s18_session(c):
    begin(c, 'Study Lab · optional depth', 'A study session needs an ending, not just a timer.')
    # left stat
    kicker(c, 'One practical shape', x=MX, y=352, color=ORANGE)
    c.setFont(SER, 84)
    c.setFillColor(ORANGE)
    c.drawString(MX, 252, '45')
    kicker(c, 'Minutes', x=MX + 4, y=228, color=INK)
    rich_block(c, [('The time can flex. ', SER, INK), ('The sequence cannot.', SERB, INK)],
               MX, 190, 240, size=17, leading=24)
    # right rows
    rows = [('05 MIN', 'Target', 'One clear thing to produce.'),
            ('15 MIN', 'Retrieve', 'Answer, solve or explain.'),
            ('10 MIN', 'Check', 'Use the model or scheme.'),
            ('10 MIN', 'Repair', 'Correct and name the error.'),
            ('05 MIN', 'Schedule', 'Choose what returns.')]
    rx, rw = 356, W - MX - 356
    ry, rh, gap = 336, 47, 10
    for i, (mins, t, d) in enumerate(rows):
        fill, accent = PROMISES[i]
        y = ry - i * (rh + gap)
        soft_box(c, rx, y - rh, rw, rh, fill, radius=rh / 2)
        number_dot(c, i + 1, rx + 26, y - rh / 2, fill=accent, r=11, size=8.5)
        c.setFont(SANSB, 10)
        c.setFillColor(accent)
        c.drawString(rx + 48, y - rh / 2 - 3.5, mins)
        c.setFont(SER, 17)
        c.setFillColor(INK)
        c.drawString(rx + 118, y - rh / 2 - 5.5, t)
        c.setFont(SANS, 11.5)
        c.setFillColor(MUTED)
        c.drawString(rx + 240, y - rh / 2 - 4, d)
    c.setFont(SANSB, 12.5)
    c.setFillColor(TEAL)
    c.drawCentredString(rx + rw / 2, 42 + 6,
                        'Target → retrieve → check → repair → return.')
    footer(c, 'Practical template informed by IES retrieval/spacing guidance and Irish '
              'Department of Education study-routine guidance.', PAGE['n'])


def s19_bedroom(c):
    begin(c, 'Promise 02 · Taught', 'Do not make success depend on a quiet bedroom.')
    # left blob question
    blob(c, MX + 150, 240, 158, 128, BLOB_PEACH)
    kicker(c, 'The equity test', x=MX + 30, y=330, color=ORANGE)
    rich_block(c, [('Could the student use this method ', SER, INK),
                   ('without ', SERB, INK),
                   ('private tuition, their own device or an expert adult at home?',
                    SER, INK)],
               MX + 34, 300, 250, size=16.5, leading=24)
    pill(c, MX + 150, 92, [('Access is part of pedagogy.', SANSB, PAPER)],
         size=12, fill=TEAL)
    # right dependables
    rx = 420
    rw = W - MX - rx
    kicker(c, 'What school can make dependable', x=rx, y=356, color=TEAL)
    items = [('A predictable, supervised study slot', PALE_BLUE, TEAL),
             ('Device, print, books and mark-scheme access', PALE_ORANGE, ORANGE),
             ('A modelled routine using real subject work', PALE_GREEN, GREEN),
             ('A low-noise place to retrieve and practise', PALE_PURPLE, PURPLE),
             ('Rapid feedback and one visible next step', PALE_RED, RED)]
    cw_ = (rw - 18) / 2
    ch_, gy = 84, 250
    for i, (t, fill, accent) in enumerate(items[:4]):
        x = rx + (i % 2) * (cw_ + 18)
        y = gy - (i // 2) * (ch_ + 16)
        soft_box(c, x, y, cw_, ch_, fill, radius=14)
        number_dot(c, i + 1, x + 24, y + ch_ - 24, fill=accent, r=10, size=8)
        text_block(c, t, x + 40, y + ch_ - 14, cw_ - 56, font=SANSB, size=11.5,
                   leading=16, color=INK)
    y = gy - 2 * (ch_ + 16) + ch_ - 58
    soft_box(c, rx, y, rw, 58, PALE_RED, radius=14)
    number_dot(c, 5, rx + 24, y + 29, fill=RED, r=10, size=8)
    c.setFont(SANSB, 11.5)
    c.setFillColor(INK)
    c.drawString(rx + 42, y + 24.5, items[4][0])
    footer(c, 'Equity principle: teach and resource the routine in school; do not assume '
              'ideal study conditions at home.', PAGE['n'])


def s20_present(c):
    begin(c, 'Promise 03 · Present', '20 days is a reporting threshold. Support starts sooner.')
    steps = [('Notice', 'Pattern, change, context'), ('Ask', 'Student + family voice'),
             ('Map', 'Barrier, strength, support'), ('Act', 'Small, specific response'),
             ('Review', 'Did access improve?')]
    n = len(steps)
    cx0, cxn = MX + 70, W - MX - 70
    stepw = (cxn - cx0) / (n - 1)
    cy = 268
    c.setStrokeColor(LINE)
    c.setLineWidth(2.4)
    c.line(cx0, cy, cxn, cy)
    for i, (t, d) in enumerate(steps):
        fill, accent = PROMISES[i]
        cx = cx0 + i * stepw
        c.setFillColor(fill)
        c.circle(cx, cy, 38, stroke=0, fill=1)
        c.setStrokeColor(accent)
        c.setLineWidth(1.8)
        c.circle(cx, cy, 38, stroke=1, fill=0)
        c.setFont(SANSB, 11.5)
        c.setFillColor(accent)
        c.drawCentredString(cx, cy - 4, f'0{i + 1}')
        c.setFont(SER, 19)
        c.setFillColor(INK)
        c.drawCentredString(cx, cy - 74, t)
        text_block(c, d, cx - stepw / 2 + 8, cy - 96, stepw - 16, size=10.5,
                   leading=15, color=MUTED, align='center')
    c.setFont(SANSB, 13)
    c.setFillColor(TEAL)
    c.drawCentredString(W / 2, 104, 'Use days missed, not only percentages. Be specific. '
                                    'Stay curious about the cause.')
    footer(c, 'Sources: Tusla absenteeism guidance and Educational Welfare Services; '
              'EEF attendance evidence review.', PAGE['n'])


def s21_partnered(c):
    begin(c, 'Promise 04 · Partnered', 'Partnership is designed before it is declared.')
    kicker(c, 'Five habits that make contact reachable', x=MX, y=362, color=TEAL)
    rows = [('Specific', 'days · patterns · next step'),
            ('Curious', 'ask before interpreting'),
            ('Strength-first', 'name what the child can do'),
            ('Accessible', 'person · language · channel · time'),
            ('Reliable', 'do what was agreed · report back')]
    lw = 380
    ry, rh, gap = 344, 50, 9
    for i, (t, d) in enumerate(rows):
        fill, accent = PROMISES[i]
        y = ry - i * (rh + gap)
        soft_box(c, MX, y - rh, lw, rh, fill, radius=rh / 2)
        number_dot(c, i + 1, MX + 26, y - rh / 2, fill=accent, r=11, size=8.5)
        c.setFont(SANSB, 13)
        c.setFillColor(INK)
        c.drawString(MX + 46, y - rh / 2 - 4.5, t)
        c.setFont(SANS, 10.5)
        c.setFillColor(MUTED)
        c.drawString(MX + 158, y - rh / 2 - 4, d)
    # right script card
    rx = MX + lw + 30
    rw = W - MX - rx
    round_box(c, rx, 62, rw, 300, fill=PAPER)
    kicker(c, 'A stronger first contact', x=rx + 26, y=326, color=ORANGE)
    text_block(c, '“We have missed Sam on seven mornings. Sam’s oral answers '
                  'in Science are strong. Is transport, sleep, caring, anxiety — '
                  'or something else — making mornings harder?”',
               rx + 26, 306, rw - 52, font=SERI, size=15.5, leading=23, color=INK)
    c.setFont(SANSB, 12.5)
    c.setFillColor(TEAL)
    c.drawString(rx + 26, 96, '“Can we agree one step and check in on Friday?”')
    footer(c, 'Practice synthesis informed by attendance evidence, HSCL/DEIS principles '
              'and responsive family engagement.', PAGE['n'])


def s22_pathway(c):
    begin(c, 'Promise 05 · Future-ready', 'A pathway is only real when a student can navigate it.')
    # aspiration blob
    blob(c, MX + 118, 235, 96, 82, BLOB_PEACH)
    c.setFont(SER, 21)
    c.setFillColor(INK)
    c.drawCentredString(MX + 118, 228, 'Aspiration')
    routes = [('Route A', 'CAO / higher education', PALE_BLUE),
              ('Route B', 'FET, PLC, tertiary, access', PALE_GREEN),
              ('Route C', 'Apprenticeship or work + training', PALE_PURPLE)]
    rx, rw, rh = 470, 380, 74
    ys = [312, 224, 136]
    # connectors
    c.setStrokeColor(OUTLINE)
    c.setLineWidth(1.8)
    for y in ys:
        c.line(MX + 214, 235, rx - 18, y + rh / 2 - 37 + 37)
    for (t, d, fill), y in zip(routes, ys):
        round_box(c, rx, y - 37, rw, rh, fill=fill)
        c.setFont(SANSB, 10.5)
        c.setFillColor(MUTED)
        c.drawString(rx + 24, y + 10, t.upper())
        c.setFont(SER, 18)
        c.setFillColor(INK)
        c.drawString(rx + 24, y - 14, d)
    pill(c, W / 2, 56, [('Each route needs ', SANSB, PAPER),
                        (' entry requirements · deadlines · cost and funding · a named '
                         'adult · a next action', SANS, PAPER)], size=11.5)
    footer(c, 'Sources: DFHERIS pathways overview; HEAR; SUSI; Government of Ireland '
              'apprenticeship information.', PAGE['n'])


def s23_leah(c):
    begin(c, 'Case lab · composite scenario', 'Leah is capable. School is becoming harder to reach.')
    lw = 400
    round_box(c, MX, 84, lw, 286, fill=PAPER)
    kicker(c, 'Leah · fifth year', x=MX + 26, y=336, color=ORANGE)
    text_block(c, 'Strong oral contributions. Written work is inconsistent. Sixteen '
                  'days absent by February and often late. She helps care for younger '
                  'siblings. She says she wants physiotherapy, then adds: “Courses '
                  'like that are for people with money.”',
               MX + 26, 314, lw - 52, font=SER, size=15.5, leading=24, color=INK)
    # right group questions
    rx = MX + lw + 28
    rw = W - MX - rx
    kicker(c, 'In groups', x=rx, y=356, color=TEAL)
    qs = [('What might the school wrongly infer?', PALE_BLUE, TEAL),
          ('What do we need to learn from Leah and home?', PALE_ORANGE, ORANGE),
          ('What changes tomorrow, this term, this year?', PALE_GREEN, GREEN),
          ('Who owns each next step?', PALE_PURPLE, PURPLE)]
    cw_, ch_ = (rw - 18) / 2, 126
    for i, (q, fill, accent) in enumerate(qs):
        x = rx + (i % 2) * (cw_ + 18)
        y = 214 - (i // 2) * (ch_ + 16) + (0 if i < 2 else 0)
        y = 218 if i < 2 else 78
        y = 218 - (i // 2) * (ch_ + 14)
        soft_box(c, x, y, cw_, ch_, fill, radius=16)
        number_dot(c, i + 1, x + 26, y + ch_ - 28, fill=accent, r=11, size=8.5)
        text_block(c, q, x + 18, y + ch_ - 48, cw_ - 36, font=SANSB, size=12,
                   leading=17, color=INK)
    footer(c, 'Fictional composite for discussion. Do not diagnose, and do not share '
              'identifiable student cases.', PAGE['n'])


def s24_coordinate(c):
    begin(c, 'One plausible response — not a prescription',
          'Coordinate the supports around the student.')
    cards = [('Known', 'Named check-in; ask Leah what is changing and what helps.'),
             ('Taught', 'Model written responses; prioritised catch-up after absence.'),
             ('Present', 'Map caring/morning barriers; agree a small plan; review weekly.'),
             ('Partnered', 'Strength-first family conversation; practical constraints first.'),
             ('Future-ready', 'Physio Route A; related FET/tertiary Route B; funding + HEAR check.')]
    # top row 2, bottom row 3
    top_w = (CW - 24) / 2
    y1, h1 = 248, 108
    for i in range(2):
        fill, accent = PROMISES[i]
        x = MX + i * (top_w + 24)
        round_box(c, x, y1, top_w, h1, fill=fill)
        number_dot(c, i + 1, x + 28, y1 + h1 - 28, fill=accent, r=12, size=9)
        c.setFont(SER, 19)
        c.setFillColor(INK)
        c.drawString(x + 48, y1 + h1 - 34, cards[i][0])
        text_block(c, cards[i][1], x + 20, y1 + h1 - 56, top_w - 40, size=11.5,
                   leading=16.5, color=INK)
    bot_w = (CW - 48) / 3
    y2, h2 = 116, 112
    for i in range(3):
        fill, accent = PROMISES[i + 2]
        x = MX + i * (bot_w + 24)
        round_box(c, x, y2, bot_w, h2, fill=fill)
        number_dot(c, i + 3, x + 26, y2 + h2 - 26, fill=accent, r=11, size=8.5)
        c.setFont(SER, 17)
        c.setFillColor(INK)
        c.drawString(x + 44, y2 + h2 - 31, cards[i + 2][0])
        text_block(c, cards[i + 2][1], x + 18, y2 + h2 - 50, bot_w - 36, size=11,
                   leading=15.5, color=INK)
    pill(c, W / 2, 56, [('Shared · sequenced · reviewed. ', SANSB, PAPER),
                        ('One owner, one next step, one date to learn.', SANS, PAPER)],
         size=12, fill=TEAL)
    footer(c, '', PAGE['n'])


# ------------------------------------------------ app section (8 slides)
def s25_app_open(c):
    begin(c, 'From workshop to student routine',
          'The app should strengthen a human support system.')
    dh = device(c, 'home', MX + 60, 128, 480)
    # right mapping card
    rx = MX + 60 + 480 + 36
    rw = W - MX - rx + 10
    kicker(c, 'Five promises · five surfaces', x=rx, y=352, color=ORANGE)
    rows = [('KNOWN', 'Home', 'one place, one next step', TEAL, PALE_BLUE),
            ('TAUGHT', 'Modules', 'methods made explicit', ORANGE, PALE_ORANGE),
            ('PRESENT', 'My Progress', 'patterns you can discuss', GREEN, PALE_GREEN),
            ('PARTNERED', 'Launchpad', 'tools chosen for need', PURPLE, PALE_PURPLE),
            ('FUTURE-READY', 'My Journey', 'growth becomes a place', RED, PALE_RED)]
    ry, rh, gap = 340, 48, 9
    for i, (tag, t, d, accent, fill) in enumerate(rows):
        y = ry - i * (rh + gap)
        soft_box(c, rx, y - rh, rw, rh, fill, radius=11)
        chip(c, rx + 12, y - rh / 2 - 10, tag, accent, PAPER, size=7.5, pad=7)
        c.setFont(SANSB, 12)
        c.setFillColor(INK)
        c.drawString(rx + 118, y - rh / 2 + 3, t)
        c.setFont(SANS, 9.5)
        c.setFillColor(MUTED)
        c.drawString(rx + 118, y - rh / 2 - 12, d)
    footer(c, 'Live demo account capture · Home · 16 August 2026. The app supports the '
              'routine; relationships, teaching and judgement remain human.', PAGE['n'])


def s26_modules(c):
    begin(c, 'Facilitate growth · teach', 'Teach the method before asking for independence.')
    device(c, 'modules', MX, 96, 520, h=272)
    rx = MX + 520 + 34
    rw = W - MX - rx
    kicker(c, 'Transfer needs adult action', x=rx, y=356, color=TEAL)
    rows = [('Explain', 'teach one strategy explicitly'),
            ('Model', 'use real subject content'),
            ('Choose', 'name when and why it fits'),
            ('Fade', 'revisit until support can reduce')]
    ry, rh, gap = 338, 50, 10
    for i, (t, d) in enumerate(rows):
        fill, accent = PROMISES[i]
        y = ry - i * (rh + gap)
        soft_box(c, rx, y - rh, rw, rh, fill, radius=12)
        number_dot(c, i + 1, rx + 24, y - rh / 2, fill=accent, r=10.5, size=8)
        c.setFont(SANSB, 12)
        c.setFillColor(INK)
        c.drawString(rx + 42, y - rh / 2 + 3, t)
        c.setFont(SANS, 10)
        c.setFillColor(MUTED)
        c.drawString(rx + 42, y - rh / 2 - 12, d)
    pill(c, rx + rw / 2, 72, [('Completion starts transfer; ', SANSB, PAPER),
                              ('it does not prove it.', SANS, PAPER)], size=10.5,
         max_w=rw + 20)
    footer(c, 'Live demo account capture · Modules · 16 August 2026. Facilitation '
              'sequence grounded in metacognitive modelling.', PAGE['n'])


def s27_session_app(c):
    begin(c, 'Facilitate growth · practise', 'Make the next study session easy to begin.')
    device(c, 'study', MX, 118, 520)
    rx = MX + 520 + 34
    rw = W - MX - rx
    kicker(c, 'Before the timer', x=rx, y=356, color=TEAL)
    rows = [('Target', 'What will be produced?'), ('Method', 'Retrieve, solve or explain.'),
            ('Check', 'What proves accuracy?'), ('Return', 'What comes back, when?')]
    ry, rh, gap = 338, 50, 10
    for i, (t, d) in enumerate(rows):
        fill, accent = PROMISES[i]
        y = ry - i * (rh + gap)
        soft_box(c, rx, y - rh, rw, rh, fill, radius=12)
        c.setFont(SANSB, 10)
        c.setFillColor(accent)
        c.drawString(rx + 18, y - rh / 2 + 4, t.upper())
        c.setFont(SANS, 10.5)
        c.setFillColor(INK)
        c.drawString(rx + 18, y - rh / 2 - 11, d)
    rich_block(c, [('Time protects attention. ', SANSB, TEAL),
                   ('The task creates evidence.', SANS, TEAL)],
               rx, 92, rw, size=11.5, leading=16, align='center')
    footer(c, 'Live demo account capture · Mathematics practice session · '
              '16 August 2026.', PAGE['n'])


def s28_markbank(c):
    begin(c, 'Facilitate growth · feedback', 'Real papers. Real schemes. Real repair.')
    device(c, 'markbank', MX, 176, 416)
    device(c, 'marksession', MX + 444, 96, 416)
    # caption chips under left
    soft_box(c, MX, 96, 416, 62, PALE_ORANGE, radius=12)
    text_block(c, '552 questions from the 2021–2025 Leaving Certificate papers, '
                  'each marked against the real SEC scheme.',
               MX + 16, 148, 384, font=SANSB, size=11, leading=16,
               color=HexColor('#7A4A24'))
    pill(c, W / 2, 46, [('Attempt → compare → decide → repair. ', SANSB, PAPER),
                        ('Feedback changes the next attempt.', SANS, PAPER)],
         size=11)
    footer(c, 'Live demo account capture · Biology Mark Bank · real SEC question and '
              'scheme · 16 August 2026.', PAGE['n'])


def s29_launchpad(c):
    begin(c, 'Explore · Launchpad', 'One place to understand, practise, plan and track.')
    device(c, 'launchpad', MX, 90, 500)
    rx = MX + 500 + 32
    rw = W - MX - rx
    rows = [('UNDERSTAND', 'Future Finder · Paper Trail · Command-Word Reflex', TEAL, PALE_BLUE),
            ('PRACTISE', 'Mark Bank · study sessions · exam reps', ORANGE, PALE_ORANGE),
            ('PLAN', 'Spaced timetable · War Room · Comeback Engine', GREEN, PALE_GREEN),
            ('TRACK', 'Journey Simulator · Points Passport · College Compass', PURPLE, PALE_PURPLE)]
    ry, rh, gap = 352, 56, 10
    for i, (t, d, accent, fill) in enumerate(rows):
        y = ry - i * (rh + gap)
        soft_box(c, rx, y - rh, rw, rh, fill, radius=13)
        kicker(c, t, x=rx + 18, y=y - 20, color=accent, size=8.5)
        text_block(c, d, rx + 18, y - 30, rw - 36, size=10.5, leading=14.5,
                   color=INK)
    pill(c, rx + rw / 2, 52, [('Adult role: ', SANSB, PAPER),
                              ('choose for need · agree the output · review the next '
                               'move.', SANS, PAPER)], size=10, max_w=rw + 30)
    footer(c, 'Live demo account capture · Launchpad · 16 August 2026. One screen, '
              'filtered by purpose — not four different tours.', PAGE['n'])


def s30_paths(c):
    begin(c, 'Guided · learning paths', 'The next step stays visible without shrinking ambition.')
    device(c, 'paths', MX, 106, 520)
    rx = MX + 520 + 34
    rw = W - MX - rx
    kicker(c, 'Four live routes', x=rx, y=356, color=PURPLE)
    rows = [('Foundation', 'stabilise habits and core strategies', PALE_BLUE),
            ('Exam', 'make tactical preparation explicit', PALE_ORANGE),
            ('Mindset', 'develop resilience and self-knowledge', PALE_PURPLE),
            ('Learning', 'sequence evidence-based study methods', PALE_GREEN)]
    ry, rh, gap = 338, 50, 10
    for i, (t, d) in enumerate([(a, b) for a, b, _ in rows]):
        fill = rows[i][2]
        y = ry - i * (rh + gap)
        soft_box(c, rx, y - rh, rw, rh, fill, radius=12)
        c.setFont(SANSB, 11.5)
        c.setFillColor(INK)
        c.drawString(rx + 18, y - rh / 2 + 4, t.upper())
        c.setFont(SANS, 10)
        c.setFillColor(MUTED)
        c.drawString(rx + 18, y - rh / 2 - 11, d)
    pill(c, rx + rw / 2, 68, [('Sequence support. ', SANSB, PAPER),
                              ('Never hide prerequisites.', SANS, PAPER)],
         size=10.5, max_w=rw + 20)
    footer(c, 'Live demo account capture · Learning Paths · 16 August 2026.', PAGE['n'])


def s31_dashboard(c):
    begin(c, 'Review together', 'A dashboard should start a conversation — not a verdict.')
    device(c, 'climbs', MX, 92, 464)
    rx = MX + 540 + 32
    rw = W - MX - rx
    kicker(c, 'Use the filters, then ask', x=rx, y=356, color=TEAL)
    rows = [('What changed?', 'Compare week, month and year.'),
            ('What helped?', 'Connect rhythm to method and access.'),
            ('Where is it stuck?', 'Look for a barrier, not a defect.'),
            ('What happens next?', 'Name an action and an adult.')]
    ry, rh, gap = 338, 52, 10
    for i, (t, d) in enumerate(rows):
        fill, accent = PROMISES[i]
        y = ry - i * (rh + gap)
        soft_box(c, rx, y - rh, rw, rh, fill, radius=12)
        number_dot(c, i + 1, rx + 22, y - rh / 2, fill=accent, r=10, size=8)
        c.setFont(SANSB, 11.5)
        c.setFillColor(INK)
        c.drawString(rx + 40, y - rh / 2 + 4, t)
        c.setFont(SANS, 9.5)
        c.setFillColor(MUTED)
        c.drawString(rx + 40, y - rh / 2 - 11, d)
    pill(c, rx + rw / 2, 64, [('Patterns guide support. ', SANSB, PAPER),
                              ('They do not predict worth.', SANS, PAPER)],
         size=10.5, max_w=rw + 20)
    footer(c, 'Live demo account capture · My Progress, programme view · '
              '16 August 2026.', PAGE['n'])


def s32_journey(c):
    begin(c, 'Facilitate growth · belong', 'Let progress become a place the student can shape.')
    kicker(c, 'Journey mode', x=MX + 35, y=394, color=TEAL)
    device(c, 'journey', MX + 35, 122, 322)
    kicker(c, 'Build mode', x=MX + 546, y=394, color=ORANGE)
    device(c, 'shop', MX + 436, 122, 420, h=264)
    soft_box(c, MX, 62, 400, 44, PALE_BLUE, radius=12)
    rich_block(c, [('Journey: ', SANSB, TEAL),
                   ('accumulated effort becomes a place and a story.', SANS, INK)],
               MX + 14, 96, 372, size=10.5, leading=14)
    soft_box(c, MX + 436, 62, 420, 44, PALE_ORANGE, radius=12)
    rich_block(c, [('Build: ', SANSB, ORANGE),
                   ('meaningful choice adds authorship — without public ranking.',
                    SANS, INK)],
               MX + 450, 96, 392, size=10.5, leading=14)
    footer(c, 'Live demo account captures · Journey and Build modes · 16 August 2026. '
              'Compare neither islands nor spending publicly.', PAGE['n'])


def s33_adult_role(c):
    begin(c, 'The adult stays in the loop', 'A tool in the routine — never a referee of worth.')
    cols = [('Choose', 'for need', 'Pick the surface that matches the barrier this '
             'week — not the whole app at once.', PALE_BLUE, TEAL),
            ('Agree', 'the output', 'Name what the student will produce and show — '
             'a session, an attempt, a plan.', PALE_ORANGE, ORANGE),
            ('Review', 'the next move', 'Look at the pattern together and agree one '
             'action with one owner.', PALE_GREEN, GREEN)]
    cw_ = (CW - 48) / 3
    cy, ch_ = 138, 216
    for i, (t, sub, d, fill, accent) in enumerate(cols):
        x = MX + i * (cw_ + 24)
        round_box(c, x, cy, cw_, ch_, fill=fill)
        number_dot(c, i + 1, x + 28, cy + ch_ - 32, fill=accent, r=12, size=9)
        c.setFont(SER, 21)
        c.setFillColor(INK)
        c.drawString(x + 48, cy + ch_ - 38, t)
        c.setFont(SERI, 13)
        c.setFillColor(MUTED)
        c.drawString(x + 48, cy + ch_ - 56, sub)
        c.setStrokeColor(accent)
        c.setLineWidth(2)
        c.line(x + 22, cy + ch_ - 72, x + cw_ - 22, cy + ch_ - 72)
        text_block(c, d, x + 22, cy + ch_ - 88, cw_ - 44, size=11.5, leading=17,
                   color=INK)
    pill(c, W / 2, 74, [('Patterns guide support. They do not predict worth.',
                         SANSB, PAPER)], size=12)
    footer(c, 'The app extends the five promises; the relationship carries them.',
           PAGE['n'])


# ------------------------------------------------ whole school + close
def s34_reality(c):
    begin(c, 'Whole-school reality check', 'How dependable are the five promises?')
    qs = [('Known', 'Can every student name an adult who will notice?'),
          ('Taught', 'Does support preserve challenge and future options?'),
          ('Present', 'Are patterns acted on before 20 days?'),
          ('Partnered', 'Can families reach a person, not only a portal?'),
          ('Future-ready', 'Does every student have A, B and C routes?')]
    cw_ = (CW - 4 * 18) / 5
    cy, ch_ = 118, 240
    for i, (t, q) in enumerate(qs):
        fill, accent = PROMISES[i]
        x = MX + i * (cw_ + 18)
        round_box(c, x, cy, cw_, ch_, fill=fill)
        number_dot(c, i + 1, x + 24, cy + ch_ - 28, fill=accent, r=11, size=8.5)
        c.setFont(SER, 16)
        c.setFillColor(INK)
        c.drawString(x + 16, cy + ch_ - 62, t)
        text_block(c, q, x + 16, cy + ch_ - 82, cw_ - 32, size=10.5, leading=15,
                   color=INK)
        # rating circles
        c.setStrokeColor(PAPER)
        c.setLineWidth(2)
        c.line(x + 16, cy + 58, x + cw_ - 16, cy + 58)
        for j in range(4):
            c.setStrokeColor(accent)
            c.setLineWidth(1.6)
            c.circle(x + 27 + j * ((cw_ - 54) / 3), cy + 38, 9, stroke=1, fill=0)
        c.setFont(SANS, 7.5)
        c.setFillColor(MUTED)
        c.drawString(x + 16, cy + 16, '1 · rarely')
        c.drawRightString(x + cw_ - 16, cy + 16, '4 · dependable')
    pill(c, W / 2, 62, [('Rate the system. ', SANSB, PAPER),
                        ('Then listen for where students and families would score it '
                         'differently.', SANS, PAPER)], size=11.5)
    footer(c, 'A low score is a planning signal, not a verdict. Do not rank individual '
              'staff or students.', PAGE['n'])


def s35_ninety(c):
    begin(c, 'From intention to implementation',
          'One 90-day test beats a 30-page aspiration.')
    rows = [('PROMISE', 'Which student experience will become more dependable?', ORANGE),
            ('FOCUS', 'For whom, where and when is the gap most visible?', LABEL),
            ('ROUTINE', 'What will adults do differently, and how often?', LABEL),
            ('OWNER', 'Who coordinates, supports and follows through?', LABEL),
            ('EARLY SIGNAL', 'What should move before outcomes move?', LABEL),
            ('REVIEW', 'What date will the team learn and adapt?', ORANGE)]
    y = 352
    for lab, q, col in rows:
        c.setFont(SANSB, 10.5)
        c.setFillColor(col)
        c.drawString(MX, y, lab)
        c.setFont(SER, 16.5)
        c.setFillColor(INK)
        c.drawString(MX + 150, y - 1, q)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.line(MX + 150, y - 14, W - MX, y - 14)
        y -= 46
    rich_block(c, [('Small enough to implement. Important enough to matter. Specific '
                    'enough to learn from. ', SANSB, TEAL),
                   ('Measure support and access — never a student’s private '
                    'history.', SANS, MUTED)],
               MX, 84, CW, size=12, leading=17.5, align='center')
    footer(c, 'Planning structure aligned with implementation guidance and DEIS '
              'whole-school planning.', PAGE['n'])


def s36_friday(c):
    begin(c, 'Take it back Monday', 'Five moves by Friday.')
    rows = [('Name', 'the students at the edge — and the adult who will notice.'),
            ('Contact', 'one family with a strength before the concern.'),
            ('Audit', 'one task for hidden vocabulary, steps or assumed support.'),
            ('Map', 'A, B and C routes with one student.'),
            ('Schedule', 'the 90-day review before momentum fades.')]
    y = 348
    for i, (t, d) in enumerate(rows):
        c.setFont(SANSB, 11)
        c.setFillColor(ORANGE)
        c.drawString(MX, y, f'0{i + 1}')
        c.setFont(SER, 21)
        c.setFillColor(INK)
        c.drawString(MX + 44, y - 2, t)
        c.setFont(SANS, 13)
        c.setFillColor(MUTED)
        c.drawString(MX + 190, y, d)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.line(MX, y - 16, W - MX, y - 16)
        y -= 52
    c.setFont(SERI, 16)
    c.setFillColor(TEAL)
    c.drawCentredString(W / 2, 62, 'Momentum is a design choice.')
    footer(c, '', PAGE['n'])


def s37_stop(c):
    begin(c, 'A disciplined commitment', 'Stop. Start. Protect.', dark=True)
    cols = [('STOP', 'One routine or phrase that quietly closes a door.', RED),
            ('START', 'One action the school will test for 90 days.', ORANGE),
            ('PROTECT', 'One strength already changing students’ odds.', TEAL)]
    cw_ = (CW - 2 * 44) / 3
    for i, (t, d, col) in enumerate(cols):
        x = MX + i * (cw_ + 44)
        c.setFillColor(col)
        c.rect(x, 356, cw_, 8, stroke=0, fill=1)
        c.setFont(SER, 30)
        c.setFillColor(PAPER)
        c.drawString(x, 306, t)
        text_block(c, d, x, 280, cw_ - 10, size=13, leading=19,
                   color=HexColor('#C9C4BC'))
        c.setStrokeColor(HexColor('#5A564F'))
        c.setLineWidth(1)
        c.line(x, 152, x + cw_, 152)
        c.line(x, 112, x + cw_, 112)
    c.setFont(SANS, 9)
    c.setFillColor(HexColor('#8F8B84'))
    footer(c, 'Write privately first. Share the action, not a confession.', PAGE['n'],
           dark=True)


def s38_invite(c):
    begin(c, 'The invitation', 'Be the school that keeps the door open.')
    text_block(c, 'Not every barrier begins in school.', MX, 316, 430,
               font=SER, size=23, leading=32, color=INK)
    rich_block(c, [('But school can decide whether a barrier becomes a ceiling.',
                    SERB, INK)],
               MX, 264, 430, size=23, leading=32)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(3)
    c.line(MX, 148, MX + 210, 148)
    # right: composed illustration
    blob(c, 700, 250, 160, 145, BLOB_PEACH)
    draw_icon(c, ASSETS / 'section-icons' / 'my-journey.png', 596, 160, 210, 210)
    blob(c, 560, 120, 70, 58, PALE_BLUE)
    draw_icon(c, ASSETS / 'section-icons' / 'my-progress-mountain.png', 512, 74, 98, 98)
    blob(c, 852, 120, 70, 58, PALE_PURPLE)
    draw_icon(c, ASSETS / 'learning-paths' / 'getting-started.png', 806, 72, 96, 96)
    footer(c, 'Return to your story. End with the student, not the programme.', PAGE['n'])


def _sources(c, kick, title, rows):
    begin(c, kick, title)
    y = 358
    for org, doc, url in rows:
        c.setFont(SANSB, 11)
        c.setFillColor(INK)
        c.drawString(MX, y, org)
        c.setFont(SANS, 11)
        c.setFillColor(MUTED)
        c.drawString(MX + 190, y, doc)
        c.setFont(SANS, 7)
        c.setFillColor(HexColor('#9A958D'))
        c.drawString(MX + 190, y - 12, url[:120])
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(MX, y - 20, W - MX, y - 20)
        y -= 40
    footer(c, '', PAGE['n'])


def s39_sources_a(c):
    _sources(c, 'Evidence base · Ireland', 'National statistics and policy sources.', [
        ('CSO', 'SILC Module on Child Deprivation 2024',
         'cso.ie/en/releasesandpublications/ep/p-silccd/silcmoduleonchilddeprivation2024/'),
        ('Tusla', 'Analysis of School Attendance Data 2023/24',
         'tusla.ie/uploads/content/Analysis_of_School_Attendance_Data_2023-24.pdf'),
        ('Dept. of Education', 'Retention of the 2018 entry cohort (July 2026); DEIS strategy',
         'gov.ie/en/department-of-education/ — retention reports and DEIS Strategy to 2035'),
        ('OECD', 'PISA 2022 Results — Ireland country note',
         'oecd.org/en/publications/pisa-2022-results-volume-i-and-ii-country-notes_ed6fbcc5-en/ireland_01173012-en.html'),
        ('HEA', 'Socio-economic profiles of students, 2021/22–2023/24',
         'hea.ie/statistics/ — widening participation, socio-economic profiles, student profile'),
        ('ESRI / GUI', 'Dempsey & McCoy (2025): self-concept, expectations and teacher relationships',
         'esri.ie/publications/how-are-childrens-academic-self-concepts-their-parents-expectations-and-their'),
        ('OECD', 'Review of Resourcing Schools to Address Educational Disadvantage in Ireland',
         'oecd.org/en/publications/oecd-review-of-resourcing-schools-to-address-educational-disadvantage-in-ireland_3433784c-en.html'),
    ])


def s40_sources_b(c):
    _sources(c, 'Evidence base · practice', 'Teaching, attendance, trauma and pathways.', [
        ('NEPS', 'Continuum of Support and trauma resources',
         'gov.ie/en/department-of-education/collections/national-educational-psychological-service-neps-resources-and-publications/'),
        ('EEF', 'Metacognition and self-regulation; attendance evidence summary',
         'educationendowmentfoundation.org.uk/education-evidence/'),
        ('IES / WWC', 'Organizing Instruction and Study to Improve Student Learning',
         'ies.ed.gov/ncee/wwc/PracticeGuide/1'),
        ('Dept. of Education', 'Study routines for the Leaving Certificate',
         'gov.ie/en/department-of-education/publications/how-to-create-study-routines-for-the-leaving-certificate-during-the-covid-19-pandemic/'),
        ('Campbell review', 'Effects of trauma-informed approaches in schools',
         'pmc.ncbi.nlm.nih.gov/articles/PMC8356508/'),
        ('UK Government', 'Caution on use of ACE screening tools',
         'gov.uk/government/publications/trauma-informed-practice-learning-from-experience/'),
        ('DFHERIS', 'Education pathways in Ireland',
         'gov.ie/en/department-of-further-and-higher-education-research-innovation-and-science/'),
        ('AccessCollege / SUSI', 'HEAR eligibility and student grant information',
         'accesscollege.ie/hear/how-do-i-apply/eligibility-criteria/'),
    ])


SLIDES = [s01_title, s02_person, s03_question, s04_deprivation, s05_absence,
          s06_pisa, s07_routes, s08_doors, s09_stereotype, s10_progress,
          s11_adult, s12_pivot, s13_known, s14_trauma, s15_quadrant, s16_route,
          s17_produce, s18_session, s19_bedroom, s20_present, s21_partnered,
          s22_pathway, s23_leah, s24_coordinate, s25_app_open, s26_modules,
          s27_session_app, s28_markbank, s29_launchpad, s30_paths,
          s31_dashboard, s32_journey, s33_adult_role, s34_reality, s35_ninety,
          s36_friday, s37_stop, s38_invite, s39_sources_a, s40_sources_b]


def build():
    register_fonts()
    prep_screens()
    PAGE['n'] = 0
    c = canvas.Canvas(str(DECK_PATH), pagesize=(W, H))
    c.setTitle('Nurturing Potential — Irish Post-Primary Workshop')
    for fn in SLIDES:
        fn(c)
        c.showPage()
    c.save()
    print(f'deck: {DECK_PATH} ({len(SLIDES)} slides)')


def render_qa(out_dir):
    import sys
    sys.path.insert(0, str(TMP / '_deps'))
    import fitz
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(DECK_PATH))
    for i, page in enumerate(doc, 1):
        page.get_pixmap(dpi=144).save(out / f'v2-{i:02d}.png')
    print(f'rendered {len(doc)} pages to {out}')


if __name__ == '__main__':
    build()
    render_qa('/private/tmp/claude-501/-Users-alexlinehan/4004560a-734a-4dd1-9436-c07c76c91ddb/scratchpad/v2_render')
