"""Construction Studies figure crops: one rect, or a composite of several scheme panels.

A card carries one solution figure. When a printed choice became one card (choice is not a route),
the scheme's drawn solution for every item must still reach the student after reveal, so the card's
figure is a vertical composite of each item's scheme panel, rendered at 2x with a 24 px white gap.
A spec is either (source, page, rect, solution) or composite(panels, solution).
"""
import hashlib
from pathlib import Path

import fitz
from PIL import Image, ImageChops

R = Path(__file__).resolve().parents[3]
SCALE = 2
GAP = 24


def composite(panels, solution=True):
    return ('panels', tuple((s, p, tuple(r)) for s, p, r in panels), solution)


def is_composite(spec):
    return spec[0] == 'panels'


def panels_of(spec):
    return [(s, p, list(r)) for s, p, r in spec[1]] if is_composite(spec) else [(spec[0], spec[1], list(spec[2]))]


def solution_of(spec):
    return spec[2] if is_composite(spec) else spec[3]


def render(panels):
    ims = []
    for source, page, rect in panels:
        with fitz.open(R / source) as pdf:
            px = pdf[page - 1].get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=fitz.Rect(rect), alpha=False)
        ims.append(Image.frombytes('RGB', (px.width, px.height), px.samples))
    if len(ims) == 1:
        return ims[0]
    out = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims) + GAP * (len(ims) - 1)), 'white')
    y = 0
    for im in ims:
        out.paste(im, (0, y))
        y += im.height + GAP
    return out


def entry(key, spec, path):
    """Write the crop to path and return its questionFigures entry."""
    render(panels_of(spec)).save(path)
    base = dict(key=key)
    if is_composite(spec):
        base['panels'] = [dict(source=s, page=p, rect=r) for s, p, r in panels_of(spec)]
        base.update(renderScale=SCALE, panelGap=GAP)
    else:
        base.update(source=spec[0], page=spec[1], rect=list(spec[2]), renderScale=SCALE)
    return dict(base, solution=solution_of(spec), sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(), visuallyInspected=True)


def check(f, spec, figure_dir, images=True):
    """The entry matches its spec, its file matches its hash, and its pixels match a fresh render."""
    if is_composite(spec):
        assert 'source' not in f and f['panels'] == [dict(source=s, page=p, rect=r) for s, p, r in panels_of(spec)], f['key']
        assert f['panelGap'] == GAP and len(f['panels']) >= 2, f['key']
    else:
        assert 'panels' not in f and (f['source'], f['page'], f['rect']) == (spec[0], spec[1], list(spec[2])), f['key']
    assert f['solution'] == solution_of(spec) and f['visuallyInspected'] and f['renderScale'] == SCALE, f['key']
    path = Path(figure_dir) / f"{f['key']}.png"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == f['sha256'], f['key']
    if images:
        a, saved = render(panels_of(spec)), Image.open(path).convert('RGB')
        assert a.size == saved.size and ImageChops.difference(a, saved).getbbox() is None, f['key']
