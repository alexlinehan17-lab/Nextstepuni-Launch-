#!/usr/bin/env python3
"""File a Physical Education ask under an LCPE topic from its wording.

    python3 scripts/markbank/authoring/pe_topics.py     # the unmatched report

The topics ARE the specification's own and they are already in this repo:
`curriculum.ts` holds the canonical `physical-education` entry — Strand 1
"Towards Optimum Performance" with Topics 1-4, Strand 2 "Contemporary Issues"
with Topics 5-10, and the six Physical Activity Areas — and the ids here are
that entry's ids, so a card filed by this module resolves in
curriculumRegistry.ts without a second list to keep in step.

Anything unmatched is REPORTED, never filed under a default: a wrong shelf
sends a student to revise the wrong thing, and a gap only asks a person to
look.
"""
import collections
import re
import sys

# (topic id, weight, pattern). The highest weight that matches wins, so a
# sub-topic beats its own parent Topic and a Topic beats nothing.
RULES = [
    # ── Strand 1, Topic 1: Learning and Improving Skill and Technique ────
    ('physical-education-0-1', 12,
     r'\b(skilled performance|characteristics? of skill|creative application'
     r'|fluency|kinaesthetic|anticipation|consistency|define skill|what is skill'
     r'|characteristics? (?:does|that|of a|of an|display))'),
    ('physical-education-0-2', 12,
     r'\b(analys\w+ (?:skill|technique|performance)|method of analysis'
     r'|notational analysis|video analysis|movement analysis|technique analysis)'),
    ('physical-education-0-3', 12,
     r'\b(skill acquisition|stages? of learning|practice (?:method|type|schedule)'
     r'|whole practice|part practice|massed|distributed|feedback|transfer of learning'
     r'|information processing|motor programme|guidance)'),
    # Biomechanics is examined under "Analysing Skill and Technique": the
    # specification's own topic list names no biomechanics topic, and the
    # papers set planes, axes, levers, Newton's laws and vector quantities as
    # ways of ANALYSING a movement. Filed there rather than invented as a
    # topic of its own — a card must resolve against curriculum.ts.
    ('physical-education-0-2', 12,
     r'\b(plane of movement|planes? and axes|sagittal|frontal plane|transverse plane'
     r'|longitudinal axis|vertical axis|mediolateral|lever system|first class lever'
     r'|fulcrum|newton|vector|scalar|momentum|centre of (?:mass|gravity)'
     r'|biomechanic|movement pattern|force\b|velocity|body type|somatotype'
     r'|ectomorph|mesomorph|endomorph|elbow flexion|flexion|extension'
     r'|class of lever|lever)'),
    ('physical-education-0-0', 6,
     r'\b(skill|technique|practice method|types? of practice)'),
    # ── Strand 1, Topic 2: Demands of Performance ────────────────────────
    ('physical-education-0-6', 12,
     r'\b(health[- ]related (?:fitness|component)|cardiovascular endurance'
     r'|muscular endurance|body composition|flexibility)'),
    ('physical-education-0-7', 12,
     r'\b(performance[- ]related (?:fitness|component)|agility|power|speed'
     r'|reaction time|co[- ]?ordination|balance)'),
    ('physical-education-0-9', 12,
     r'\b(fitness test|test to measure|assessing physical fitness|protocol'
     r'|norm(?:ative)? data|sit and reach|bleep test|vo2)'),
    ('physical-education-0-10', 12,
     r'\b(training (?:plan|programme|principles)|principles? of training'
     r'|approaches? to training'
     r'|periodisation|overload|specificity|progression|reversibility|detraining'
     r'|fitness plan|method of physical fitness training|continuous training'
     r'|interval training|fartlek|plyometric|circuit training|weight training)'),
    ('physical-education-0-11', 12,
     r'\b(psychological preparation|motivation|arousal|anxiety|goal setting'
     r'|self[- ]talk|visualis|imagery|mental (?:preparation|rehearsal|health)'
     r'|thought stopping|centring|attentional focus|confidence)'),
    ('physical-education-0-12', 12,
     r'\b(diet|nutrition|hydration|carbohydrate|protein|nutrient'
     r'|supplement(?!s? for)'
     r'|energy system|atp|glycolytic|aerobic system|anaerobic)'),
    ('physical-education-0-5', 8,
     r'\b(physical fitness|fitness component|components? of fitness)'),
    ('physical-education-0-4', 6,
     r'\b(demands? of performance|fitness)'),
    # ── Strand 1, Topic 3: Structures, Strategies, Roles, Conventions ────
    ('physical-education-0-16', 12,
     r'\b(safe practice|safety equipment|injur|first aid|risk assessment'
     r'|warm[- ]?up|cool[- ]?down|protective)'),
    ('physical-education-0-18', 12,
     r'\b(coach|choreographer|coaching)'),
    ('physical-education-0-19', 12,
     r'\b(official|referee|umpire|judge\b|scoring/recording|conflict between '
     r'participants)'),
    ('physical-education-0-17', 12,
     r'\b(ritual|convention|rules? of (?:the game|play)|etiquette)'),
    ('physical-education-0-14', 12,
     r'\b(structures? and strategies|attacking strateg|defensive strateg'
     r'|game strateg|formation|tactic)'),
    ('physical-education-0-15', 10,
     r'\b(roles? and relationships|team role|leadership|captain)'),
    ('physical-education-0-13', 6, r'\b(strateg|role\b)'),
    # ── Strand 1, Topic 4: Planning for Performance ──────────────────────
    ('physical-education-0-23', 12,
     r'\b(aesthetic|artistic|choreograph\w*\s+criteria|composition of a routine)'),
    ('physical-education-0-21', 12,
     r'\b(personal performance analysis|performance goal|performance profile'
     r'|reflection on|post[- ]training analysis)'),
    ('physical-education-0-22', 10,
     r'\b(questionnaire|checklist|coach feedback|data collect|scat test)'),
    ('physical-education-0-24', 10,
     r'\b(planning for (?:optimum )?performance|training/practice plan|rationale)'),
    # ── Strand 2, Topic 5: Promoting Physical Activity ───────────────────
    ('physical-education-1-1', 12,
     r'\b(benefits? of (?:physical activity|participation)|health and wellbeing'
     r'|social benefit|personal benefit)'),
    ('physical-education-1-2', 12,
     r'\b(participation (?:levels?|rates?|in physical activity)|barriers? to '
     r'physical activity|reasons for (?:non[- ])?participation|drop[- ]?out'
     r'|participate the most|participation between|lifelong participation'
     r'|participation of (?:men|women|young))'),
    ('physical-education-1-3', 12,
     r'\b(promot\w+ physical activity|physical activity promotion|campaign'
     r'|initiative|support(?:s)? for physical activity|tip sheet'
     r'|encourage (?:lifelong )?participation|school sport)'),
    ('physical-education-1-4', 12,
     r'\b(pathway(?:s)? to excellence|talent (?:identification|development)'
     r'|pathways between school and community|elite)'),
    ('physical-education-1-0', 6, r'\b(physical activity)'),
    # ── Strand 2, Topic 6: Ethics and Fair Play ──────────────────────────
    ('physical-education-1-9', 12,
     r'\b(anti[- ]?doping rule|whereabouts|prohibited (?:substance|method)'
     r'|sport ireland anti[- ]doping|wada|therapeutic use exemption|\btue\b'
     r'|banned substance)'),
    ('physical-education-1-8', 12,
     r'\b(performance[- ]enhancing drug|anabolic steroid|doping|beta blocker'
     r'|blood doping|stimulant|diuretic|erythropoietin|epo\b)'),
    ('physical-education-1-10', 12, r'\b(supplement)'),
    ('physical-education-1-7', 12, r'\b(code of ethics|code of conduct)'),
    ('physical-education-1-6', 10,
     r'\b(fair play|sportsmanship|gamesmanship|ethical|equity|integrity'
     r'|cheating)'),
    ('physical-education-1-5', 6, r'\b(ethic)'),
    # ── Strand 2, Topic 7: Physical Activity and Inclusion ───────────────
    ('physical-education-1-15', 12,
     r'\b(adapted physical activity|disabilit|para[- ]?sport|special olympics'
     r'|inclusive (?:sport|activity|practice))'),
    ('physical-education-1-14', 12,
     r'\b(over the past 20 years|last twenty years|developments? over)'),
    ('physical-education-1-13', 10, r'\b(address\w* barriers?|overcome barriers?)'),
    ('physical-education-1-12', 10,
     r'\b(supports? and barriers?|socio[- ]?economic|older adult|life stage)'),
    ('physical-education-1-11', 6, r'\b(inclusion|inclusive)'),
    # ── Strand 2, Topic 8: Technology, Media and Sport ───────────────────
    ('physical-education-1-17', 12,
     r'\b(technolog\w+|wearable|gps|hawk[- ]?eye|var\b|goal[- ]line'
     r'|data analytics)'),
    ('physical-education-1-18', 12,
     r'\b(media (?:coverage|in sport)|spectator (?:behaviour|experience)'
     r'|social media|broadcast|television coverage|journalis'
     r'|sports programmes?|top 10|information is available from)'),
    ('physical-education-1-16', 6, r'\b(media|technology)'),
    # ── Strand 2, Topic 9: Gender and Physical Activity ──────────────────
    ('physical-education-1-21', 12,
     r'\b(body image|gender.{0,20}media|media.{0,20}gender)'),
    ('physical-education-1-22', 12, r'\b(gender socialisation|stereotyp)'),
    ('physical-education-1-20', 10,
     r'\b(gender|women in sport|female athlete|social regulation of the body'
     r'|male and female|men and women)'),
    ('physical-education-1-19', 6, r'\b(gender)'),
    # ── Strand 2, Topic 10: Business and Enterprise ──────────────────────
    ('physical-education-1-24', 12,
     r'\b(sponsorship|sponsor|endorsement|advertis|merchandis|branding)'),
    ('physical-education-1-26', 12,
     r'\b(mass[- ]participation|parkrun|marathon event|club membership)'),
    ('physical-education-1-27', 12, r'\b(tourism|major event|hosting)'),
    ('physical-education-1-25', 10,
     r'\b(business (?:of|dimension)|national governing bod|funding|revenue'
     r'|commercial)'),
    ('physical-education-1-23', 6, r'\b(business|enterprise)'),
    # ── Physical Activity Areas ──────────────────────────────────────────
    ('physical-education-2-0', 8,
     r'\b(orienteering|kayak|canoe|hill ?walking|climbing|surfing)'),
    ('physical-education-2-1', 8, r'\b(dance|gymnastic|floor exercise|routine)'),
    ('physical-education-2-2', 8,
     r'\b(athletics|sprint|hammer throw|javelin|discus|long jump|high jump'
     r'|400m|800m|relay)'),
    ('physical-education-2-3', 8, r'\b(aquatic|swim|water polo|diving)'),
    ('physical-education-2-5', 8,
     r'\b(personal exercise and fitness|gym programme)'),
]
COMPILED = [(t, w, re.compile(p, re.I)) for t, w, p in RULES]

# The concept id is level-independent so a Higher card and its Ordinary sibling
# share one identity — a student who drops to Ordinary in spring keeps a year's
# review history. Built from the topic and the ask's own content words, never
# from the year or the level.
STOP = {'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'is', 'are',
        'on', 'at', 'by', 'with', 'from', 'that', 'this', 'it', 'as', 'be',
        'your', 'you', 'named', 'physical', 'activity', 'choice', 'two',
        'three', 'four', 'one', 'each', 'following', 'above', 'below', 'can',
        'how', 'what', 'why', 'which', 'may', 'give', 'name', 'state',
        'explain', 'describe', 'discuss', 'outline', 'identify', 'define'}


def topic_for(text):
    """The finest LCPE topic the ask's wording names, or None."""
    best, best_weight = None, 0
    for topic, weight, rx in COMPILED:
        if weight > best_weight and rx.search(text or ''):
            best, best_weight = topic, weight
    return best


def concept_for(topic, text):
    words = [w for w in re.findall(r"[a-z']+", (text or '').lower())
             if w not in STOP and len(w) > 3]
    tail = '-'.join(words[:4]) or 'ask'
    return f'{topic.replace("physical-education", "pe")}-{tail}'[:80]


if __name__ == '__main__':
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pe_lib as L
    from paper import Paper
    missed, hit = [], collections.Counter()
    for year, level in L.SITTINGS:
        P = Paper(L.SUBJECT, year, level)
        for key in P.paths():
            text = P.text(*key) or ''
            t = topic_for(text)
            if t:
                hit[t] += 1
            else:
                missed.append((year, level, key, text[:90]))
    print(f'{sum(hit.values())} filed, {len(missed)} unmatched')
    for t, n in hit.most_common():
        print(f'  {n:>4}  {t}')
    print('\n-- unmatched')
    for row in missed[:40]:
        print('   ', row)
