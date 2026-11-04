"""Read the older Ordinary answer layout without inventing tariffs.

The heading number and first answer often share a line. Full-credit answers
use dashes and partial answers use asterisks. Normalize only the reading
section, retaining every source line and page marker for the complete guide.
"""
import re

RC = re.compile(r'^Question\s+(\d)\s*[–-]\s*(\d+)\s+marks$', re.I)
ITEM = re.compile(r'^(\d{1,2})\.\s*(.*)$')
RATE = re.compile(r'(\d+(?:\s*\+\s*\d+)?)\s+marks?\s*$', re.I)


def normalize_ordinary(lines, part_splits=None, combined_parts=None):
    # Older PDFs expose the printed partial-credit asterisk in Symbol font.
    lines = [line.replace('\uf02a', '*').replace('\uf02d', '-') for line in lines]
    out, active, finished = [], False, False
    part_splits = part_splits or {}
    combined_parts = combined_parts or {}
    rc_number = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if not finished and re.match(r'^Section I\b', line, re.I):
            active = True
        if re.match(r'^Section II\b', line, re.I):
            active = False
            finished = True
        rc = RC.match(line) if active else None
        item = ITEM.match(line) if active else None
        if rc:
            rc_number = rc[1]
            out.append(f'Q.{rc[1]} ({rc[2]} Marks)')
        elif item:
            end = i + 1
            while end < len(lines) and not (ITEM.match(lines[end]) or RC.match(lines[end]) or re.match(r'^Section II\b', lines[end], re.I)):
                end += 1
            block = [item[2], *lines[i + 1:end]]
            rates = [RATE.search(s) for s in block]
            rate = next((m[1] for m in rates if m), None)
            if rate is None:
                raise ValueError(f'Unpriced legacy Ordinary reading item: {line}')
            combined = combined_parts.get(f'A{rc_number}-Q{item[1]}')
            if combined:
                meaningful = [s for s in block if s and not re.match(r'^(?:## Page |\d+$)', s)]
                assert meaningful == combined['sourceLines'] and combined['reason'], meaningful
                rates = [RATE.search(s)[1] for s in meaningful if re.match(r'^\(i+\)\s*-', s)]
                assert rates == list(map(str, combined['marks'])), rates
                assert len(rates) == 2 and rates[0] == rates[1], rates
                rate = '+'.join(rates)
                block = [re.sub(r'^\(i+\)\s*', '', s) for s in block]
            split = part_splits.get(f'A{rc_number}-Q{item[1]}')
            if split:
                # Separately required, separately priced response categories
                # (e.g. Japan / France), reviewed against the printed paper.
                # Every answer and shared rung must be pinned; no line is
                # silently discarded by this split.
                meaningful = [s for s in block if s and not re.match(r'^(?:## Page |\d+$)', s)]
                assert meaningful == split['sourceLines'], meaningful
                assert split['reason']
                if 'answerLines' in split['parts'][0]:
                    covered = set(split.get('contextLines', []) + split['sharedRungs'])
                    covered.update(index for part in split['parts'] for index in part['answerLines'])
                    assert covered == set(range(len(meaningful))), covered
                    assert sum(part['marks'] for part in split['parts']) == split['totalMarks']
                for part in split['parts']:
                    if 'answerLines' in part:
                        marks = part['marks']
                        indices = part['answerLines']
                    else:
                        indices = [part['answerLine']]
                        marks = RATE.search(split['sourceLines'][indices[0]])[1]
                    out.append(f'{item[1]}.({part["letter"]}) ........ {marks} Marks')
                    for index in indices + split['sharedRungs']:
                        answer = re.sub(r'^\(i+\)\s*', '', split['sourceLines'][index])
                        answer = re.sub(r'^-\s*', '• ', answer)
                        out.append(re.sub(r'^[*∗]\s*', '– ', answer))
                # Keep the following page boundary so subsequent items do
                # not inherit this split item's scheme-page citation.
                furniture = lambda s: not s or re.match(r'^(?:## Page |\d+$)', s)
                first_page = next((n for n, s in enumerate(block) if re.match(r'^## Page ', s)), len(block))
                assert all(furniture(s) for s in block[first_page:]), block
                out.extend(s for s in block if s and furniture(s))
                i = end
                continue
            matching = re.match(r'^\(a\)\s*-', next((s for s in block if s), ''))
            if matching:
                parts = [re.match(r'^\(([a-d])\)\s*-\s*(.*)', s) for s in block]
                parts = [m for m in parts if m]
                assert [m[1] for m in parts] == list('abcd'), line
                assert all(RATE.search(m[2])[1] == rate for m in parts), line
                head = f'{item[1]}.(a-d) ........ {rate} x 4 Marks'
            else:
                head = f'{item[1]}. ........ {rate} Marks'
            out.append(head)
            for s in block:
                if matching:
                    s = re.sub(r'^\([a-d]\)\s*-\s*', '• ', s)
                else:
                    s = re.sub(r'^\(i\)\s*&\s*\(ii\)\s*', '', s)
                    s = re.sub(r'^-\s*', '• ', s)
                s = re.sub(r'^[*∗]\s*', '– ', s)
                if s in ('Yes', 'No'):
                    s += ':'
                out.append(s)
            i = end
            continue
        else:
            out.append(line)
        i += 1
    return out


def apply_reviewed_blocks(lines, blocks):
    """Pin older shared tariffs to the complete visually reviewed source span.

    Replacements preserve every answer and note, but put one numbered head at
    each shared mark boundary. Fail if any word in the reviewed span changes.
    """
    if not blocks:
        return lines
    lines = [' '.join(line.split()) for line in lines if line.strip()]
    for block in blocks:
        source = block['sourceLines']
        matches = [i for i in range(len(lines) - len(source) + 1)
                   if lines[i:i + len(source)] == source]
        assert len(matches) == 1 and block['reason'], block['address']
        i = matches[0]
        lines[i:i + len(source)] = block['replacementLines']
    return lines
