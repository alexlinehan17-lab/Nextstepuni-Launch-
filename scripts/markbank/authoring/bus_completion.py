#!/usr/bin/env python3
"""Complete the Business paper-census gaps from the published schemes.

Business uses three different document layouts across 2016-2025.  This pass
keeps the paper as the denominator, groups only leaves which share a printed
parent tariff, and joins each paper prompt to the final scheme/support-notes
occurrence of that prompt.  Every proposed answer row is then checked by the
same provenance matcher used by build-deck.mjs.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_parts import parts as scheme_parts  # noqa: E402
from paper_census import (  # noqa: E402
    ROMANS, census_sections, census_subject, key_label, leaves_of,
)
from reconcile import reconcile_subject  # noqa: E402


DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
TARGETS_PATH = os.path.join(
    ROOT, 'scripts', 'markbank', 'authored', 'business-completion-targets.json')
VERIFY = os.path.join(DIR, 'verify-claims.mjs')
TOKEN = re.compile(r"[^\W_]+(?:['’][^\W_]+)?", re.UNICODE)
COMMAND = re.compile(
    r'\b(?:explain|outline|discuss|describe|name|state|identify|calculate|'
    r'evaluate|illustrate|list|write|distinguish|complete|indicate|choose|'
    r'circle|draft|read|using|what|how|why|fill|match)\b', re.I)
COMMAND_HEAD = re.compile(
    r'^(?:explain|outline|discuss|describe|name|state|identify|calculate|'
    r'evaluate|illustrate|list|write|distinguish|complete|indicate|choose|'
    r'circle|draft|read|using|what|how|why)\b', re.I)
NOISE = re.compile(
    r'^(?:## Page|Leaving Certificate|LC Business|Business (?:Higher|Ordinary)|'
    r'Question Possible|Possible Response|Max(?:imum)? Mark|Available Marks|'
    r'SECTION|PART \d|Note:|Accept\b|Other correct answers?|The expected '
    r'responses|Marks?$|Name, Explain|State, Explain|Source, Explain|'
    r'Question\s+\d+\s*$)', re.I)
TARIFF_ONLY = re.compile(
    r'^(?:[+@x×\d\s(),.:;m⟨⟩\-]+|\d+\s*marks?.*|'
    r'(?:first|second|third) correct.*)$', re.I)
ANGLE = re.compile(r'⟨[^⟩]*⟩')
MARK_TOKEN = re.compile(
    r'⟨[^⟩]*\d[^⟩]*⟩|\(?\b\d{1,3}\s*m(?:arks?)?\b\)?', re.I)
PAPER_MARKS = re.compile(r'\((\d{1,2})\s*(?:marks?)?\)', re.I)
SCHEME_TOTAL = re.compile(
    r'⟨\s*(\d{1,2})\s*m?(?:arks?)?\s*⟩|\b(\d{1,2})\s+marks?\b', re.I)
BROKEN_GLYPH = re.compile(r'[\u0100-\u1FFF\uE000-\uF8FF\uFB00-\uFB4F]')

# A small number of Business schemes put short-answer keys in diagrams,
# multi-column tables, or an appendix whose reading order cannot be joined to
# the paper prompt reliably. Keep those joins explicit. The rows remain
# verbatim SEC scheme text and still pass through traceable() below; this table
# is a locator, not a provenance bypass.
MANUAL_ROWS = {
    (2016, 'hl', '1', 3, None, None): [
        'FALSE TRUE TRUE FALSE FALSE',
    ],
    (2016, 'hl', '1', 4, None, None): [
        'C D F A B',
    ],
    (2016, 'hl', '1', 7, None, None): [
        '€70 €105 €35 deficit',
        '€90 €65 €25 surplus',
        '€80 €110 €30 deficit',
        'Invisible Exports refers to services sold to foreign countries and money flowing into the country/ Money flows into Ireland when Irish services are sold abroad.',
        'E.g. Italian tourists holidaying in Ireland; foreign students studying in Ireland/Irish internet providers selling their services to customers abroad.',
    ],
    (2016, 'ol', '2', 2, 'a', None): [
        'The secondary sector includes the manufacturing and construction industries.',
        'Primary sector or Tertiary/Services sector.',
    ],
    (2016, 'ol', '2', 5, 'c', None): [
        'Value Added Tax',
        'Corporation Tax',
    ],
    (2016, 'ol', '2', 5, 'd', None): [
        'A bank overdraft is a short term source of finance. It is an agreement which allows account holders to withdraw/spend more money than they have in their account.',
        'An overdraft must be paid back/cleared within one year.',
    ],
    (2016, 'ol', '2', 6, 'e', None): [
        'Website – on the company website',
        'Newspapers',
    ],
    (2017, 'hl', '1', 1, None, None): [
        'E A B C F',
    ],
    (2017, 'hl', '1', 5, None, None): [
        'A. 25,000',
        'B. (3,000)',
        'C. 11,000',
        'D. 5,000',
        'E. 16,000',
    ],
    (2017, 'hl', '1', 6, None, None): [
        'Set appropriate credit limits and credit periods: Draw up clear terms and conditions controlling the amount of credit and ensuring that payments are made on time.',
        'Offer incentives such as a cash discount for early or prompt payment.',
    ],
    (2017, 'hl', '1', 7, None, None): [
        'A global business sells all over the world/regards the world as a single market /using a standardised marketing mix /adapted marketing mix.',
        'Examples: Coca-Cola, Google, Facebook, Nike, Adidas, Amazon, VW, Ford etc.',
    ],
    (2017, 'hl', '1', 8, None, None): [
        'A FIXED COSTS B TOTAL REVENUE C TOTAL COSTS D BREAK EVEN POINT',
        '75,000 units – 50,000 units = 25,000 units',
        'How far forecasted sales/sales revenue can fall before the firm becomes lossmaking.',
    ],
    (2017, 'hl', '1', 10, None, None): [
        'Inflation rate is a (sustained) percentage increase in the general level of prices/cost of living over a period of time, normally 1 year/It is measured by the Consumer Price Index (CPI)/percentage increase in the price of goods.',
        'The price/cost/reward paid by a borrower to a lender for the use of money/the cost of borrowed money expressed as a % of amount borrowed/amount of money the borrower must pay the lender for the use of the lender’s funds expressed as a % of amount borrowed/set by the ECB.',
    ],
    (2017, 'hl', '3', 6, 'c', None): [
        'The Net Profit Margin (NPM) has decreased from 20.5% to 15.2%',
        'The Return on Investment (ROI) has decreased from 8% to 4%.',
        'The Current Ratio has decreased from 2:1 to 1.25:1',
        'The business should not expand as all key financial indicators are in decline.',
        'Assets may not be shown at their true value.',
        'Ratios are based on past figures and not on projected future figures.',
    ],
    (2017, 'ol', '1', 4, None, None): [
        'PRODUCT PRICE PROMOTION PLACE',
    ],
    (2018, 'hl', '1', 4, None, None): [
        'E D A B F',
    ],
    (2018, 'hl', '1', 5, None, None): [
        '(i) May',
        '(ii) August',
        'Import substitution refers to a trade policy which replaces imports with domestically produced goods/services.',
    ],
    (2018, 'hl', '1', 6, None, None): [
        'A. 360,000',
        'B. 400,000',
        'C. 760,000',
        'D. 600,000',
        'E. (360,000)',
    ],
    (2018, 'hl', '1', 9, None, None): [
        '1. False 2. False 3. False 4. True 5. True',
    ],
    (2018, 'hl', '3', 5, 'a', None): [
        'Economies of scale exist. There is strength in numbers.',
        'Control is lost over the day-to-day management of the franchise businesses.',
        'The reputation of the whole business could be affected by the actions of one franchisee /poor quality standards/staff',
    ],
    (2018, 'ol', '1', 1, None, None): [
        'DIRT Deposit Interest Retention Tax',
        'PIN Personal Identification Number',
        'PAYE Pay As You Earn',
    ],
    (2018, 'ol', '1', 2, None, None): [
        'Sony Intrapreneur',
        'Stanford Univ. Entrepreneur',
        'Facebook Intrapreneur',
        'Google Intrapreneur',
        'O’Connor Entrepreneur',
    ],
    (2018, 'ol', '1', 5, None, None): [
        '1. Strengths 2. Weaknesses 3. Opportunities 4. Threats',
    ],
    (2018, 'ol', '1', 6, None, None): [
        '(i) PRSI €2,800 (70,000 x 4 / 100)',
        '(ii) USC €2,100 (70,000 x 3 / 100)',
        '(iii) Total Deductions €21,790',
        '(iv) Take Home Pay €48, 210',
    ],
    (2018, 'ol', '1', 11, None, None): [
        'An agenda is a list of the items to be discussed at a meeting. It gives the order of business for a meeting. An agenda gives a meeting structure.',
        'The minutes of a meeting are a written record of what happened at a meeting.',
    ],
    (2018, 'ol', '1', 12, None, None): [
        'LAND Labour CAPITAL ENTERPRISE',
    ],
    (2018, 'ol', '1', 13, None, None): [
        'Vodafone and Irish Rugby Team: Sponsorship',
        'David Beckham and H&M Store: Celebrity Endorsement',
        'Apple announcement: Press Release',
    ],
    (2018, 'ol', '2', 1, 'e', None): [
        'Gender',
        'Age',
        'Religious beliefs',
        'Sexual Orientation',
    ],
    (2018, 'ol', '2', 3, 'c', None): [
        'China',
        '16%',
    ],
    (2018, 'ol', '2', 5, 'c', None): [
        'Question one will result in a premium discount because an alarm/immobiliser will lead to a reduction in the risk of theft.',
        'Question two will lead to loading/increase on the premium.',
    ],
    (2019, 'hl', '1', 1, None, None): [
        'F C E B D',
    ],
    (2019, 'hl', '1', 7, None, None): [
        'REST OF EU',
        '(122 - 79) = €43bn surplus',
        'COFFEE or WINE',
        'Climate – Ireland does not have the climate to grow coffee beans/grapes.',
    ],
    (2019, 'hl', '1', 10, None, None): [
        'A = Fixed Costs B = Total Costs C = Total Revenue D = Break Even Point',
        '270,000 – 240,000 = €30,000',
        'The selling price is assumed to be constant regardless of output.',
    ],
    (2019, 'hl', '3', 6, 'c', None): [
        'To review the progress of employees in order to determine the appropriate reward.',
        'Goals can be set for future performance and these targets can be agreed by employees.',
        'To provide employees with feedback so their productivity can increase.',
    ],
    (2019, 'hl', '3', 7, 'c', None): [
        'Promotion-Colour/design/shape to attract the customer.',
        'Image/Aesthetics. It must look good using shape, size and colour.',
        'Protection- during storage and handling-Air compressed container to maintain freshness.',
    ],
    (2019, 'ol', '1', 2, None, None): [
        'Premium Pricing: Product B (Samsung Galaxy Note 9)',
        'Penetration Pricing: Product A (Alcatel 1)',
    ],
    (2019, 'ol', '1', 12, None, None): [
        'Launch Growth Maturity Saturation Decline A B C D E GM Self- Electric Car 2.0 Litre 1950’s The VW Golf Driving Car (EV) Diesel Jeep Chevy',
    ],
    (2019, 'ol', '1', 14, None, None): [
        'Visual communication, e.g. Powerpoint or flip charts displaying bar charts, line graphs or Excel presentations showing the financial performance.',
        'Written communication. A letter to ensure there is a record of the formal warning, followed by a meeting with staff member to discuss the issue confidentially.',
        'Oral communication. Face to face or telephone call to enable quick communication.',
    ],
    (2019, 'ol', '1', 15, None, None): [
        'D C A B F',
    ],
    (2020, 'hl', '1', 1, None, None): [
        'E F A C B',
    ],
    (2020, 'hl', '1', 9, None, None): [
        '(i) Decline Growth Saturation',
        'Reduce the Price: A business reduces price to attract more customers.',
        'Develop new features: New product features/new image/design/use.',
    ],
    (2020, 'ol', '1', 2, None, None): [
        '(i) Batch (ii) Job (iii) Mass',
    ],
    (2020, 'ol', '1', 4, None, None): [
        'Drafts all European laws European Commission',
        'Ensures the EU Budget is spent correctly European Court of Auditors',
        'Represents all EU citizens and debates all EU laws European Parliament',
    ],
    (2021, 'hl', '3', 6, 'c', 'ii'): [
        'Increased employee motivation from job enrichment/ improved staff morale/more challenging work.',
    ],
    (2024, 'hl', '1', 9, None, 'i'): [
        '€55,000',
    ],
}

FIGURE_META = {
    (2016, 'hl', '1', 7, None, None): {
        'figureKey': 'business-2016-HL-paper-p04-art-q7-trade-table',
    },
    (2016, 'ol', '1', 14, None, None): {
        'figureKey': 'business-2016-OL-paper-p05-art-q14-product-life-cycle',
    },
    (2017, 'hl', '3', 6, 'c', None): {
        'figureKey': 'business-2017-HL-paper-p09-art-q6-ratio-tables',
    },
    (2018, 'ol', '1', 5, None, None): {
        'figureKey': 'business-2018-OL-paper-p03-art-q5-swot-table',
    },
    (2020, 'hl', '1', 9, None, None): {
        'figureKey': 'business-2020-HL-paper-p07-art-q9-products-table',
    },
    (2020, 'ol', '1', 2, None, None): {
        'figureKey': 'business-2020-OL-paper-p03-art-q2-production-options',
    },
    (2020, 'ol', '1', 4, None, None): {
        'figureKey': 'business-2020-OL-paper-p04-art-q4-eu-table',
    },
    (2020, 'ol', '1', 11, None, None): {
        'figureKey': 'business-2020-OL-paper-p06-art-q11-pay-table',
        'labelKey': [
            {'letter': 'A', 'meaning': 'PRSI (4% of gross pay)',
             'askedInThisQuestion': True},
            {'letter': 'B', 'meaning': 'USC (3% of gross pay)',
             'askedInThisQuestion': True},
            {'letter': 'C', 'meaning': 'Total deductions',
             'askedInThisQuestion': True},
            {'letter': 'D', 'meaning': 'Net annual take-home pay',
             'askedInThisQuestion': True},
        ],
    },
    (2020, 'ol', '1', 14, None, None): {
        'figureKey': 'business-2020-OL-paper-p07-art-q14-development-table',
    },
}


def _token(text: str) -> str:
    return unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode().casefold()


def token_offsets(text: str):
    return [(_token(m.group()), m.start(), m.end()) for m in TOKEN.finditer(text)
            if _token(m.group())]


def candidates(question: str, haystack):
    """Longest exact word run in the opening paper wording."""
    qwords = [x[0] for x in token_offsets(question)]
    words = [x[0] for x in haystack]
    if not qwords:
        return []
    floor = min(4, len(qwords))
    for width in range(min(8, len(qwords)), floor - 1, -1):
        for offset in range(0, min(30, len(qwords) - width + 1)):
            needle = qwords[offset:offset + width]
            found = [i for i in range(len(words) - width + 1)
                     if words[i:i + width] == needle]
            if found:
                return found
    return []


def choose_location(found, haystack, raw):
    """Prefer a scheme prompt over the same words repeated in its answer."""
    options = []
    for index in found:
        pos = haystack[index][1]
        start = raw.rfind('\n', 0, pos) + 1
        end = raw.find('\n', pos)
        end = len(raw) if end < 0 else end
        line = raw[start:end].strip()
        score = 3 * bool(COMMAND.search(line))
        score += 2 * bool(re.match(
            r'^(?:\(?[A-Ea-e]\)|\d{1,2}[.)]|Question\s+\d)', line, re.I))
        score += bool('⟨' in line or re.search(r'\b\d+\s*marks?\b', line, re.I))
        score -= 3 * bool(line.startswith(('•', '-')))
        options.append((score, start))
    return max(options)[1]


def scheme_raw(year, level):
    path = os.path.join(
        ROOT, 'examiner-reports', 'business', 'schemes', f'{year}-{level}.md')
    raw = open(path, encoding='utf-8', errors='ignore').read()
    # Table-cell/column repair appendices are evidence for provenance but not a
    # second logical copy of the scheme to walk as question order.
    return raw.split('<!-- markbank:', 1)[0], path


def _clean_line(text):
    text = ANGLE.sub(' ', text)
    text = re.sub(
        r'\s+\(?\d+(?:\s*[+@x×]\s*\d+)+(?:m|\s*marks?)?\)?\s*$',
        '', text, flags=re.I)
    return ' '.join(text.split()).strip(' •x\t')


def has_unreadable_glyph(text):
    """Mirror build-deck's broken-subset refusal for proposed scheme rows."""
    for char in text:
        cp = ord(char)
        if not BROKEN_GLYPH.match(char):
            continue
        if 0x0370 <= cp <= 0x03FF or cp in (0x0302, 0x0305) \
                or 0x02B0 <= cp <= 0x02FF:
            continue
        return True
    return False


def answer_rows(question, chunk):
    """Answer paragraphs following the prompt's first explicit tariff."""
    tariff = MARK_TOKEN.search(chunk[:1800])
    body = chunk[tariff.end():] if tariff else '\n'.join(chunk.splitlines()[1:])
    rows = []
    current = ''

    def flush():
        nonlocal current
        text = current.strip()
        current = ''
        if not text:
            return
        pieces = ([text] if len(text) <= 520 else
                  re.split(r'(?<=[.!?])\s+(?=[A-Z])', text))
        for piece in pieces:
            piece = piece.strip()
            if 4 <= len(re.sub(r'\W', '', piece)) and len(piece) <= 520 \
                    and piece not in rows:
                rows.append(piece)

    for raw_line in body.splitlines():
        bullet = raw_line.lstrip().startswith(('•', '-'))
        line = _clean_line(raw_line)
        if not line:
            continue
        if NOISE.match(line) or TARIFF_ONLY.fullmatch(line):
            continue
        # A later unlocated part is still a hard boundary, never an answer.
        if re.match(r'^\([A-Ea-e]\)\s*', line) and COMMAND.search(line):
            break
        if COMMAND_HEAD.match(line):
            continue
        qwords = [_token(m.group()) for m in TOKEN.finditer(question)][:5]
        lwords = [_token(m.group()) for m in TOKEN.finditer(line)][:5]
        if len(qwords) >= 4 and lwords[:4] == qwords[:4]:
            continue
        if bullet:
            flush()
            current = line
        elif current and not re.search(r'[.!?]$', current):
            current += ' ' + line
        else:
            flush()
            current = line
    flush()
    return rows


def join_answer_fragments(lines):
    """Join scheme-reader line wraps without inventing punctuation."""
    rows, current = [], ''
    for raw in lines:
        line = _clean_line(raw)
        if not line or NOISE.match(line) or TARIFF_ONLY.fullmatch(line):
            continue
        if current and not re.search(r'[.!?]$', current) and len(current) < 360:
            current += ' ' + line
        else:
            if current:
                rows.append(current)
            current = line
    if current:
        rows.append(current)
    return [r for r in rows if 4 <= len(re.sub(r'\W', '', r)) <= 520]


def traceable(scheme_path, claims):
    if not claims:
        return set()
    proc = subprocess.run(
        ['node', VERIFY], cwd=ROOT, text=True, capture_output=True,
        input=json.dumps({'scheme': os.path.relpath(scheme_path, ROOT),
                          'claims': claims}))
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or 'verify-claims failed')
    return set(json.loads(proc.stdout)['ok'])


def natural(key):
    return (str(key[0]), str(key[1]), key[2] or '',
            ROMANS.index(key[3]) if key[3] in ROMANS else 99)


def refresh_targets():
    census = census_subject('business')
    audit = reconcile_subject('business', census)
    payload = {
        'paperLeafCount': audit['leaves'],
        'targetCount': audit['open'],
        'censusCounts': {
            f"{p['year']}-{p['level']}": p['leafCount'] for p in census['papers']
        },
        'targets': [
            {'year': p['year'], 'level': p['level'], 'label': label}
            for p in audit['papers'] for label in p['open']
        ],
    }
    with open(TARGETS_PATH, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'wrote {TARGETS_PATH}', file=sys.stderr)


def load_targets():
    payload = json.load(open(TARGETS_PATH, encoding='utf-8'))
    by_sitting = defaultdict(set)
    for row in payload['targets']:
        by_sitting[(row['year'], row['level'])].add(row['label'])
    if sum(map(len, by_sitting.values())) != payload['targetCount']:
        raise AssertionError('Business target sidecar count is stale')
    return payload, by_sitting


def grouped_targets(year, level, target_labels):
    parts, texts, _ = census_sections('business', year, level)
    leaves = leaves_of(parts)
    lookup = {key_label(k): k for k in leaves}
    missing = target_labels - set(lookup)
    if missing:
        raise AssertionError(f'{year} {level}: missing target(s) {sorted(missing)}')
    targets = {lookup[label] for label in target_labels}
    groups, used = [], set()
    for key in leaves:
        if key not in targets or key in used:
            continue
        section, q, letter, roman = key
        # The older short-answer section prices each numbered question as one
        # ten-mark unit, even where it prints answer slots or small sub-prompts.
        if section == '1' and year <= 2020:
            members = [k for k in leaves if k[:2] == key[:2]]
            if set(members) <= targets:
                groups.append(((section, q, None, None), members))
                used.update(members)
                continue
        # A letter whose roman children are all still open is one parent card;
        # the paper prints their common total at that letter boundary.
        if roman:
            members = [k for k in leaves if k[:3] == key[:3]]
            if set(members) <= targets:
                groups.append(((section, q, letter, None), members))
                used.update(members)
                continue
        groups.append((key, [key]))
        used.add(key)
    if used != targets:
        raise AssertionError(f'{year} {level}: target grouping lost leaves')
    return groups, leaves, texts


def question_for(group, members, texts):
    lines = []
    parent = texts.get(group, '')
    if parent:
        lines.append(parent)
    for member in members:
        text = texts.get(member, '')
        if text and text not in lines:
            suffix = ''.join(f'({x})' for x in member[2:] if x)
            lines.append(f'{suffix} {text}'.strip() if member != group else text)
    text = ' '.join(lines)
    text = re.sub(r'_{3,}', ' ', text)
    text = re.split(
        r'\b(?:Answerbook for Section|Instructions Questions for Section|'
        r'Start each question on a new page|Copyright notice)\b', text, 1)[0]
    return ' '.join(text.split()).strip()


def total_for(year, level, group, members, texts, chunks, mapped):
    if group[0] == '1' and year <= 2020:
        return 10
    printed = []
    for key in members:
        printed.extend(int(x) for x in PAPER_MARKS.findall(texts.get(key, ''))
                       if 0 < int(x) <= 80)
    if printed:
        return printed[-1]
    for key in members:
        chunk = chunks.get(key, '')
        # The first explicit max mark after a support-note prompt is its total.
        for match in SCHEME_TOTAL.finditer(chunk[:1600]):
            value = int(match.group(1) or match.group(2))
            if 0 < value <= 80:
                return value
    values = []
    for key in [group] + members:
        p = mapped.get(key)
        if p:
            values.extend(int(v) for v in p.get('marks', []) if str(v).isdigit())
    if values:
        return max(values)
    if group[0] == '1':
        return 10 if level == 'hl' else 15
    return None


def topic_for(question):
    text = _token(question)
    rules = [
        (r'contract|consumer|sale of goods|redress|small claims|ccpc', 'business-0-13'),
        (r'trade union|industrial|dismissal|employment equality|discrimin', 'business-0-14'),
        (r'entrepreneur|enterprise|intrapreneur|risk tak', 'business-1-5'),
        (r'motivat|maslow|mcgregor|leadership|team', 'business-2-11'),
        (r'communicat|meeting|memo|notice|agenda|ict|technology', 'business-2-12'),
        (r'planning|organis|control|span of control|chain of command', 'business-2-13'),
        (r'insurance|indemnity|utmost good faith|premium|assessor', 'business-3-17'),
        (r'tax|paye|prsi|usc|dirt|vat|take home pay', 'business-3-18'),
        (r'ratio|break.even|liquid|working capital|gross profit|net profit', 'business-3-19'),
        (r'recruit|training|human resource|reward|job description|wage|salary', 'business-3-20'),
        (r'change|quality|tqm', 'business-3-21'),
        (r'cash.flow|finance|loan|overdraft|grant|share capital|budget', 'business-3-16'),
        (r'product development|prototype|business idea', 'business-4-14'),
        (r'business plan|start.up|sole trader|franchise', 'business-4-15'),
        (r'market research|segment|target market', 'business-4-16'),
        (r'marketing mix|product life|price|promotion|advertis|brand|packag|distribution', 'business-4-17'),
        (r'expan|merger|takeover|strategic alliance|economies of scale', 'business-4-18'),
        (r'primary sector|secondary sector|tertiary sector|factor of production', 'business-5-13'),
        (r'ownership|partnership|limited liability|plc|co-operative', 'business-5-14'),
        (r'government|econom|inflation|interest rate|employment|privatis', 'business-5-15'),
        (r'community|environment|social responsib|ethic', 'business-5-17'),
        (r'european union|eurozone|directive|regulation|commission|parliament', 'business-6-14'),
        (r'global|multinational|international market', 'business-6-15'),
        (r'import|export|trade|tariff|quota|balance of payments|exchange rate', 'business-6-13'),
    ]
    for pattern, topic in rules:
        if re.search(pattern, text):
            return topic
    return 'business-0-12'


def slug(question):
    stop = {'a', 'an', 'and', 'the', 'of', 'to', 'in', 'for', 'on', 'with',
            'each', 'following', 'one', 'two', 'three', 'four', 'explain',
            'outline', 'describe', 'discuss', 'name', 'state'}
    words = [_token(m.group()) for m in TOKEN.finditer(question)]
    words = [w for w in words if w and w not in stop][:9]
    return '-'.join(words) or 'paper-task'


def card_id(year, level, key):
    section, q, letter, roman = key
    tail = 'abq' if q == 'ABQ' else f'q{q}'
    tail += letter or ''
    tail += roman or ''
    return f'bus-{year}-{level}-s{section}-{tail}'


def make_card(year, level, group, question, total, rows):
    card = {
        'id': card_id(year, level, group),
        'topicId': topic_for(question),
        'conceptId': slug(question),
        'level': 'higher' if level == 'hl' else 'ordinary',
        'year': year,
        'subjectId': 'business',
        'section': str(group[0]),
        'questionRef': f'{year} {level.upper()} {key_label(group)}',
        'questionText': question,
        'schemeCitation': (
            'Question wording is lifted from the SEC Business paper; marking '
            f'points are lifted from the {year} {level.upper()} SEC marking '
            'scheme/support notes — © State Examinations Commission.'),
        'tariffModel': {'kind': 'questionTotal'},
        'totalMarks': total,
        'rows': [
            {'id': f'r-{i}', 'kind': 'point', 'verbatim': row, 'marks': None}
            for i, row in enumerate(rows, 1)
        ],
        'notes': ('The paper leaves in this card share the printed total shown; '
                  'row-level values are not inferred.'),
    }
    card.update(FIGURE_META.get((year, level, *group), {}))
    return card


def build():
    payload, target_sets = load_targets()
    cards, held = [], []
    observed_targets = 0
    for year in range(2016, 2026):
        for level in ('hl', 'ol'):
            labels = target_sets.get((year, level), set())
            groups, leaves, texts = grouped_targets(year, level, labels)
            observed_targets += sum(len(members) for _, members in groups)
            expected = payload['censusCounts'][f'{year}-{level}']
            if len(leaves) != expected:
                raise AssertionError(
                    f'{year} {level}: census drifted {expected} -> {len(leaves)}')

            raw, scheme_path = scheme_raw(year, level)
            haystack = token_offsets(raw)
            locations = {}
            for key in leaves:
                found = candidates(texts[key], haystack)
                if found:
                    locations[key] = choose_location(found, haystack, raw)
            ordered = sorted(set(locations.values()))
            following = {
                at: ordered[i + 1] if i + 1 < len(ordered) else len(raw)
                for i, at in enumerate(ordered)
            }
            chunks = {key: raw[at:following[at]]
                      for key, at in locations.items()}
            mapped = {}
            for part in scheme_parts(year, level):
                key = (str(part['section']),
                       'ABQ' if part['section'] == 2 and part['question'] == 0
                       else part['question'],
                       part['part'], part['roman'])
                mapped[key] = part

            proposals = {}
            all_claims = []
            for group, members in groups:
                rows = list(MANUAL_ROWS.get((year, level, *group), ()))
                for key in members:
                    if key in chunks:
                        rows.extend(answer_rows(texts[key], chunks[key]))
                    for candidate in (key, group):
                        part = mapped.get(candidate)
                        if part and part.get('answers'):
                            rows.extend(join_answer_fragments(part['answers']))
                            # Keep the scheme's original wrapped lines as
                            # candidates too.  A tariff column can sit between
                            # two visual lines, making their joined form non-
                            # contiguous for provenance even though each line
                            # is independently exact.
                            rows.extend(
                                line for line in
                                (_clean_line(raw) for raw in part['answers'])
                                if 4 <= len(re.sub(r'\W', '', line)) <= 520
                                and not NOISE.match(line)
                                and not TARIFF_ONLY.fullmatch(line))
                rows = list(dict.fromkeys(
                    ' '.join(row.split()) for row in rows
                    if ' '.join(row.split()) and not has_unreadable_glyph(row)))
                proposals[group] = rows
                all_claims.extend(rows)
            good = traceable(scheme_path, list(dict.fromkeys(all_claims)))

            made = 0
            for group, members in groups:
                question = question_for(group, members, texts)
                rows = [row for row in proposals[group] if row in good][:12]
                total = total_for(
                    year, level, group, members, texts, chunks, mapped)
                if not question:
                    held.append((year, level, group, 'no paper wording'))
                elif total is None:
                    held.append((year, level, group, 'no printed total'))
                elif not rows:
                    held.append((year, level, group, 'no traceable answer row'))
                else:
                    cards.append(make_card(
                        year, level, group, question, total, rows))
                    made += 1
            print(f'{year} {level}: {made}/{len(groups)} cards', file=sys.stderr)

    if observed_targets != payload['targetCount']:
        raise AssertionError(
            f'target total drifted {payload["targetCount"]} -> {observed_targets}')
    for year, level, key, why in held:
        print(f'HELD {year} {level} {key_label(key)} — {why}', file=sys.stderr)
    return cards


if __name__ == '__main__':
    if '--refresh-targets' in sys.argv:
        refresh_targets()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=1))
