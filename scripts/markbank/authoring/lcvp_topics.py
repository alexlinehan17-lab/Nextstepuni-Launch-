#!/usr/bin/env python3
"""File an LCVP part under a Link Modules unit from its wording.

    python3 scripts/markbank/authoring/lcvp_topics.py     # unmatched report

The ten units ARE the LCVP programme statement's own, and they are already in
this repo: `curriculum.ts` holds the canonical `lcvp-link-modules` entry with
its two link modules and five units each, and the ids here are that entry's
ids, so a card filed by this module resolves in curriculumRegistry.ts without
a second list to keep in step.

  Link Module 1 — Preparation for the World of Work
    0-0 Unit 1  Introduction to Working Life
    0-1 Unit 2  Job Seeking Skills
    0-2 Unit 3  Career Investigation
    0-3 Unit 4  Work Placement
    0-4 Unit 5  Curriculum Vitae & Summary Report
  Link Module 2 — Enterprise Education
    1-0 Unit 1  Enterprise Skills
    1-1 Unit 2  Local Business Enterprises
    1-2 Unit 3  Local Voluntary Organisations
    1-3 Unit 4  An Enterprise Activity
    1-4 Unit 5  Work Experience Diary, My Own Place & Recorded Interview

Anything unmatched is REPORTED, never filed under a default: a wrong shelf
sends a student to revise the wrong thing, and a gap only asks a person to
look.
"""
import collections
import re
import sys

M1 = 'lcvp-link-modules-0'
M2 = 'lcvp-link-modules-1'

# (topic id, weight, pattern). The highest weight that matches wins.
RULES = [
    # ── Link Module 1 ────────────────────────────────────────────────────
    # Unit 5 is the CV and the summary report, which the papers ask about by
    # name; it takes precedence over job seeking, where a CV is one tool.
    (f'{M1}-4', 14, r'\b(curriculum vitae|\bcv\b|cover(ing)? letter|referee|'
                    r'summary report|body of the report|report on this activity|'
                    r'report writing|sections? of (the|your) report)\b'),
    (f'{M1}-1', 12, r'\b(job application|application form|job interview|'
                    r'interview(er|ing|s)?\b|recruitment|shortlist|'
                    r'job seeking|job advertis|vacanc|scoring sheet|'
                    r'person specification|job description|apply for a job|'
                    r'job applicant|employable|employability)\b'),
    (f'{M1}-2', 12, r'\b(career investigation|choice of career|career path|'
                    r'career of your choice|career you|investigating (your|a) '
                    r'career|careers exhibition|career fair|apprenticeship|'
                    r'entry pathway|qualifax|careers portal|open day|'
                    r'sources of information .* career|career choices)\b'),
    (f'{M1}-3', 12, r'\b(work experience|work shadow|work placement|'
                    r'placement employer|shadowing)\b'),
    # Unit 1 is the world of work itself: the law, the union, the contract,
    # the workplace and its conditions.
    (f'{M1}-0', 10, r'\b(trade union|industrial relations|shop steward|'
                    r'contract of employment|employment act|health and safety|'
                    r'legal responsibilit|employer.{0,20}responsibilit|'
                    r'employee.{0,20}responsibilit|under 18|minimum wage|'
                    r'world of work|workplace|working from home|remote working|'
                    r'clearly defined role|world of work differs|'
                    r'unemploy|working week|conditions of employment|'
                    r'diversity|equal opportunit|inclusive|discriminat|'
                    r'staff turnover|retain staff|benefits of employment|'
                    r'dispute in the workplace|employee wellbeing|'
                    r'interpersonal skills|differences between work and school)\b'),
    # ── Link Module 2 ────────────────────────────────────────────────────
    (f'{M2}-2', 12, r'\b(voluntary (body|organisation|bodies|work)|volunteer|'
                    r'volunteering|charity|charitable|social enterprise|'
                    r'corporate social responsibility|\bcsr\b|fundrais)\b'),
    (f'{M2}-1', 11, r'\b(visit out|visit in|visits out|visits in|'
                    r'business enterprise (you|your|that you) visit|'
                    r'guest speaker|speaker from|local business|'
                    r'business/organisation|local enterprise office|\bleo\b|'
                    r'enterprise ireland|county enterprise|state agenc|'
                    r'business start-?up|start-?up business|'
                    r'sources of employment|economic activit)\b'),
    (f'{M2}-3', 11, r'\b(enterprise activity|class project|class activity|'
                    r'action plan|enterprise/action plan|agenda|committee|'
                    r'chairperson|secretary|treasurer|minutes|meeting|'
                    r'team activity|teamwork|team member|group project|'
                    r'evaluate (this|the) (activity|enterprise)|'
                    r'plan of work|assign roles|fashion show|'
                    r'apprenticeship fair|exhibition for the senior)\b'),
    (f'{M2}-4', 11, r'\b(my own place|local area|your area|local communit|'
                    r'tidy towns|questionnaire|survey|market research|'
                    r'public consultation|recreational facilities|'
                    r'facilities for young people|town centre|'
                    r'aspects? of your local|swot|scot)\b'),
    # Unit 1 is enterprise itself: the entrepreneur, the idea, the risk, the
    # money and why a business succeeds or fails.
    (f'{M2}-0', 9, r'\b(entrepreneur|enterprise skills|enterprising|'
                   r'generate ideas|idea generation|business plan|'
                   r'feasibility study|marketing mix|promotion|advertis|'
                   r'sources of finance|fund(ing)?|business might fail|'
                   r'business to fail|innovat|diversif|risk|initiative|'
                   r'online sales|selling online|social media presence|'
                   r'\bict\b|information and communication technology|'
                   r'technolog|brexit|tariff|competition|profit|'
                   r'marketing|customer|supplier|stakeholder|'
                   r'business plan|manager|leadership|leader|motivat)\b'),
    # ── the shelf a bare word puts something on ──────────────────────────
    # Lowest weight of all, so anything above takes it first. These are not
    # guesses about content: an ask about "Evan's business" IS about a local
    # business enterprise, and the Section A audio-visual questions that name
    # nothing else are about the enterprise or the worker the DVD showed.
    (f'{M2}-0', 3, r'\b(enterprise|innovat|creativ|idea|risk[- ]tak)\b'),
    (f'{M2}-1', 2, r'\b(business|company|firm|shop|workshop|trader|premises|'
                   r'product|service|sales|owner)\b'),
    (f'{M1}-0', 1, r'\b(employee|employer|worker|job|work|staff|skills?|'
                   r'qualit(y|ies)|career)\b'),
]
COMPILED = [(tid, weight, re.compile(rx, re.I)) for tid, weight, rx in RULES]


def _normalise(text):
    return ' '.join((text or '').split())


def topic_for(text):
    """(topic id, the phrase that decided it) — or (None, None)."""
    best = (0, None, None)
    haystack = _normalise(text)
    for tid, weight, rx in COMPILED:
        m = rx.search(haystack)
        if m and weight > best[0]:
            best = (weight, tid, m.group(0))
    return best[1], best[2]


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'were', 'this', 'that', 'with', 'from', 'by', 'on', 'at', 'as', 'it',
        'what', 'which', 'why', 'how', 'state', 'give', 'name', 'write',
        'explain', 'outline', 'describe', 'list', 'discuss', 'identify',
        'two', 'one', 'three', 'four', 'five', 'your', 'you', 'would', 'do'}


def concept_for(text, fallback='part'):
    """A slug for the card's concept, from the ask's own first words."""
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP][:6]
    return '-'.join(keep) or fallback


def main():
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from paper_census import census_lcvp                      # noqa: E402
    hit, miss = collections.Counter(), []
    for year in range(2018, 2026):
        parts, texts, _files, _marks = census_lcvp('lcvp', year, 'cl')
        for key in sorted(parts, key=str):
            tid, _why = topic_for(texts.get(key, ''))
            if tid:
                hit[tid] += 1
            else:
                miss.append((year, key, texts.get(key, '')[:80]))
    for tid, n in sorted(hit.items()):
        print(f'{n:4d}  {tid}')
    print(f'{len(miss)} unmatched')
    for row in miss[:30]:
        print('   ', row)


if __name__ == '__main__':
    main()
