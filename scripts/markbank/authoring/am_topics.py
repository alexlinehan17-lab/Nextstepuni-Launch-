#!/usr/bin/env python3
"""Where an Applied Maths card is filed.

The taxonomy is the CANONICAL one — curriculum.ts's four strands for
`applied-mathematics`, read out of that file rather than retyped here, for the
reason LCVP's strands are read from it: a second copy of a syllabus drifts, and
a card filed against a topic id the registry does not hold resolves into a
specification that contains no such topic.

    Strand 1  Mathematical Modelling
    Strand 2  Mathematical Modelling with Networks and Graphs
    Strand 3  Mathematically Modelling the Physical World; Kinematics and Dynamics
    Strand 4  Mathematically Modelling a Changing World

The 2021 and 2022 papers are the OLD syllabus — pure mechanics — and every one
of their questions is a Strand 3 topic, because Strand 3 is where the revised
specification kept the mechanics course: relative velocity, projectiles,
connected masses, collisions, circular motion, statics, hydrostatics, moments
of inertia and simple harmonic motion are all named subtopics of it. So one
taxonomy files both sides of the break, and a student who drops down a year
still finds their work.

A card is filed on the words the SEC printed — the paper's question and the
scheme's own working — never on a guess. `--audit` reports what fell through.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CURRICULUM = os.path.join(ROOT, 'curriculum.ts')


def strands():
    """[(strand id, name, [(topic id, name)])] for applied-mathematics."""
    text = open(CURRICULUM, encoding='utf-8').read()
    start = text.index('"id": "applied-mathematics"')
    end = text.index('"id": "physics"', start)
    body = text[start:end]
    out, cur = [], None
    for m in re.finditer(r'"id":\s*"(applied-mathematics-\d+(?:-\d+)?)",\s*\n?\s*"name":\s*"([^"]+)"', body):
        tid, name = m.group(1), m.group(2)
        if tid.count('-') == 2:               # applied-mathematics-N
            cur = (tid, name, [])
            out.append(cur)
        elif cur is not None:
            cur[2].append((tid, name))
    if len(out) != 4:
        raise AssertionError(f'expected four Applied Maths strands, read {len(out)}')
    return out


STRANDS = strands()
TOPIC_NAME = {tid: name for _s, _n, ts in STRANDS for tid, name in ts}

# What each topic is recognised BY: the words the SEC prints when it sets one.
# Every phrase here occurs in the corpus; the audit below names the asks that
# match none of them so the table is answerable to the papers rather than to a
# guess about the specification.
RULES = [
    # -- Strand 2, networks and graphs
    ('applied-mathematics-1-2', r'\b(minimum spanning tree|spanning tree|kruskal|prim)'),
    ('applied-mathematics-1-5', r'\b(critical path|float|scheduling|precedence|activity network|earliest start|latest start|dummy activit)'),
    ('applied-mathematics-1-3', r"\b(shortest path|dijkstra|bellman|dynamic programming|shortest route|quickest route)"),
    ('applied-mathematics-1-1', r'\b(adjacency|matrix|matrices)\b'),
    ('applied-mathematics-1-0', r'\b(network|graph theory|vertex|vertices|node|edge weight|degree of)\b'),
    # -- Strand 4, a changing world
    ('applied-mathematics-3-2', r'\b(auxiliary equation|general solution of the difference|homogeneous)'),
    ('applied-mathematics-3-1', r'\b(difference equation|recurrence relation|first order recurrence)'),
    ('applied-mathematics-3-0', r'\b(u_?n\s*\+\s*1|term of the sequence|geometric sequence|arithmetic sequence)'),
    ('applied-mathematics-3-4', r'\b(separating the variables|separable|integrating factor|second[- ]order differential)'),
    ('applied-mathematics-3-3', r'\b(differential equation|rate of change is proportional|dx/dt|dy/dx = k)'),
    # -- Strand 3, the physical world
    ('applied-mathematics-2-13', r'\b(simple harmonic|elastic string|natural length|hooke|amplitude|periodic time)'),
    ('applied-mathematics-2-12', r'\b(moment of inertia|angular (velocity|acceleration)|rigid body|compound pendulum|radius of gyration)'),
    ('applied-mathematics-2-11', r'\b(relative density|buoyanc|submerged|floats|hydrostat|pressure at|density of water|archimedes)'),
    ('applied-mathematics-2-10', r'\b(centre of gravity|lamina|uniform (rod|beam|ladder)|in equilibrium|reaction at the (wall|hinge)|moments about)'),
    ('applied-mathematics-2-9', r'\b(relative (velocity|to)|appears to the pilot|shortest distance between the|intercept)'),
    ('applied-mathematics-2-8', r'\b(dimensional analysis|dimensions of|units for)\b'),
    ('applied-mathematics-2-7', r'\b(circular (motion|path)|vertical circle|conical pendulum|centripetal|angular speed)'),
    ('applied-mathematics-2-6', r'\b(kinetic energy|potential energy|work done|conservation of energy|power (developed|output))'),
    ('applied-mathematics-2-5', r'\b(coefficient of friction|rough (plane|surface|table)|pulley|wedge|connected|air resistance|resistance to the motion|drag)'),
    ('applied-mathematics-2-4', r'\b(coefficient of restitution|collide|collision|impulse|momentum|sphere [ab] |bounce|rebound)'),
    ('applied-mathematics-2-3', r"\b(newton's|free[- ]body|forces acting|tension in the string|normal reaction|mass of\b)"),
    ('applied-mathematics-2-2', r'\b(projected|projectile|angle of projection|range|time of flight|inclined plane|i⃗|j⃗|unit vector)'),
    ('applied-mathematics-2-1', r'\b(dv/ds|dv/dt|velocity[- ]time graph|acceleration is given by|in terms of t|integrat)'),
    ('applied-mathematics-2-0', r'\b(uniform acceleration|uniform retardation|decelerat|from rest|speed[- ]time graph|travels|m s–1|m s-1|m s\^)'),
    # -- Strand 1, the modelling cycle itself
    ('applied-mathematics-0-4', r'\b(comment on (the )?(this )?(model|assumption)|is the model|reasonable|validity)'),
    ('applied-mathematics-0-1', r'\b(assumption|model this|formulate)\b'),
]
COMPILED = [(tid, re.compile(pat, re.I)) for tid, pat in RULES]

# Where an ask that matches nothing goes. Kinematics is the paper's own
# default: every Applied Maths question is set in motion, and the specification
# puts "particle motion in one dimension" first for the same reason. Counted
# separately by the audit so the fallback can never hide a bad table.
FALLBACK = 'applied-mathematics-2-0'


def topic_for(text):
    """(topic id, matched) — matched is False when the fallback was used."""
    flat = ' '.join((text or '').split())
    for tid, pat in COMPILED:
        if pat.search(flat):
            return tid, True
    return FALLBACK, False


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'were', 'this', 'that', 'with', 'from', 'by', 'on', 'at', 'as', 'it',
        'what', 'which', 'how', 'why', 'you', 'your', 'their', 'they', 'one',
        'two', 'three', 'each', 'any', 'following', 'above', 'below', 'find',
        'show', 'calculate', 'state', 'prove', 'write', 'down', 'value',
        'values', 'terms', 'given', 'hence', 'otherwise', 'when', 'where'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where the two papers ask
    the same thing, which is what keeps a student's work when they drop level.
    Derived from the ask, never typed.
    """
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback


if __name__ == '__main__':
    for sid, name, topics in STRANDS:
        print(f'{sid}  {name}')
        for tid, tname in topics:
            print(f'    {tid:28} {tname}')
    print(f'\n{len(TOPIC_NAME)} topics, {len(RULES)} rules')
    unruled = [t for t in TOPIC_NAME if t not in {r[0] for r in RULES}]
    if unruled:
        print('topics with no rule (never assigned): '
              + ', '.join(TOPIC_NAME[t] for t in unruled))
    sys.exit(0)
