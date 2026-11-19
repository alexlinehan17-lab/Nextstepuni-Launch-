"""Resolve reviewed booklet identities to the SEC archive's local filenames."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def source_path(year, fileid, kind, sitting='main'):
    if sitting not in ('main', 'deferred') or kind not in ('paper', 'scheme'):
        raise ValueError('unsupported Mathematics source')
    if Path(fileid).name != fileid:
        raise ValueError('source must name one booklet')
    deferred = sitting == 'deferred'
    if fileid.endswith('-deferred.pdf') != deferred:
        raise ValueError('booklet identity disagrees with sitting')
    directory = ({'paper': 'deferredexams', 'scheme': 'deferredmarkingschemes'} if deferred
                 else {'paper': 'exampapers', 'scheme': 'markingschemes'})[kind]
    filename = fileid.replace('-deferred.pdf', '.pdf') if deferred else fileid
    return ROOT / 'paper-trail-corpus' / directory / str(year) / filename


def review_source(review, kind):
    return source_path(review['year'], review[f'{kind}Fileid'], kind, review.get('sitting', 'main'))
