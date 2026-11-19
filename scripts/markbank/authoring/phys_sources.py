"""Keep main and deferred Physics sittings distinct at every source boundary."""
import os


def sitting(ledger):
    value = getattr(ledger, 'SITTING', 'main')
    if value not in ('main', 'deferred'):
        raise ValueError(f'Unknown Physics sitting: {value!r}')
    return value


def key(ledger, year, level):
    return f'{year}-{level}' + ('-deferred' if sitting(ledger) == 'deferred' else '')


def ledger_name(ledger, year, level):
    return 'phys_review_' + key(ledger, year, level).replace('-', '_')


def owns(identifier, ledger, year, level, family='phys'):
    prefix = f'{family}-{year}-{level}-'
    if sitting(ledger) == 'deferred':
        return identifier.startswith(prefix + 'deferred-')
    return identifier.startswith(prefix) and not identifier.startswith(prefix + 'deferred-')


def source_path(root, ledger, kind):
    path = os.path.join(root, ledger.SOURCES[kind]['path'])
    if sitting(ledger) == 'deferred':
        fileid = f"LC021{'A' if ledger.LEVEL == 'hl' else 'G'}LP000EV.pdf"
        if ledger.LEVEL not in ('hl', 'ol') or ledger.SOURCES[kind]['fileid'] != fileid:
            raise ValueError(f'Deferred {kind} has the wrong level or edition')
        folder = {'paper': 'deferredexams', 'scheme': 'deferredmarkingschemes'}[kind]
        expected = os.path.join(root, 'paper-trail-corpus', folder, str(ledger.YEAR),
                                ledger.SOURCES[kind]['fileid'])
        if os.path.realpath(path) != os.path.realpath(expected):
            raise ValueError(f'Deferred {kind} resolves outside its SEC archive: {path}')
    return path


def indexed_fileid(ledger, kind):
    fileid = ledger.SOURCES[kind]['fileid']
    if sitting(ledger) == 'deferred':
        if not fileid.endswith('.pdf') or '-deferred' in fileid:
            raise ValueError(f'Expected the SEC archive basename, got {fileid}')
        return fileid[:-4] + '-deferred.pdf'
    return fileid
