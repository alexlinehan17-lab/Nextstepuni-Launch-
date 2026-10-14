"""Source-pinned review of selection wording in both Business paper editions."""
import hashlib
import re
import unicodedata


SELECTION = re.compile(
    r"\b(?:choose|select|either|(?:one|two|three|four|five|six|\d+)\s+of|"
    r"or|nó|any\s+(?:one|two|three|four|five|six|\d+)|"
    r"answer\s+(?:one|two|three|four|five|six|seven|eight|\d+)|following\s+(?:two|three)|"
    r"roghnaigh|freagair|ceachtar|ceann\s+amháin|"
    r"(?:aon|cibé)\s+(?:dá|dhá|trí|cheithre|chúig|sé|seacht|ocht)|"
    r"(?:dhá|trí|ceithre|cúig|sé|seacht|ocht)\s+cheann)\b", re.I)

# finite-choice: the candidate chooses N of M printed items and the scheme
# marks every choice alike, so ONE card carries all M items (it names the card,
# cardId). finite-pool: the choices are marked differently, so each is a route
# of a pool (poolId).
CLASSIFICATIONS = {
    'exam-navigation', 'case-context', 'open-response',
    'required-headings', 'finite-pool', 'finite-choice',
}


def page_directives(year, fileid, page, raw_text, paper_sha256):
    text = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', raw_text)).strip()
    result = []
    for match in SELECTION.finditer(text):
        wording = text[max(0, match.start() - 70):match.end() + 170]
        key = f'{year}:{fileid}:{page}:{match.start()}:{wording}'
        result.append({
            'id': hashlib.sha256(key.encode()).hexdigest()[:24],
            'page': page, 'matchedText': match.group(), 'wording': wording,
            'paperSha256': paper_sha256, 'reviewStatus': 'unclassified',
        })
    return result


def apply_reviews(directives, reviews):
    """Fail on stale review keys/text/source hashes, never silently reuse them."""
    by_id = {item['id']: item for item in directives}
    if len(by_id) != len(directives):
        raise ValueError('Duplicate Business selection directive IDs')
    for key, review in reviews.items():
        item = by_id.get(key)
        if item is None:
            raise ValueError(f'Stale Business selection review: {key}')
        if any(review.get(field) != item[field] for field in ['wording', 'paperSha256']):
            raise ValueError(f'Business selection source changed: {key}')
        if review.get('classification') not in CLASSIFICATIONS or not review.get('reason'):
            raise ValueError(f'Unexplained Business selection review: {key}')
        if review['classification'] == 'finite-pool' and not review.get('poolId'):
            raise ValueError(f'Business finite selection lacks a route pool: {key}')
        if review['classification'] == 'finite-choice' and not review.get('cardId'):
            raise ValueError(f'Business finite choice lacks its card: {key}')
        item.update(reviewStatus='reviewed', classification=review['classification'],
                    reason=review['reason'])
        if review.get('poolId'):
            item['poolId'] = review['poolId']
        if review.get('cardId'):
            item['cardId'] = review['cardId']


def require_reviewed(directives):
    pending = [item for item in directives if item['reviewStatus'] != 'reviewed']
    if pending:
        raise ValueError(f'{len(pending)} unclassified Business selection directives')
