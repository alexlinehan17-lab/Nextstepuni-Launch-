"""Re-run every reviewed-paper generator and prove it reproduces the committed output.

    python3 scripts/markbank/authoring/maths/reproduce.py [review_2020_hl_p1 ...]

Run from the repository root on a clean worktree. Each generator rewrites its
review ledger and updates its cards in scripts/markbank/authored/maths.json in
place (cards it added are rebuilt and compared, never appended twice). After
each one, `git diff --exit-code` must find nothing in either file: the
generator reproduces the committed bytes. Any difference is printed, the files
are restored from git, and the script exits non-zero.
"""
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEVEL = {'hl': 'higher', 'ol': 'ordinary'}
AUTHORED = 'scripts/markbank/authored/maths.json'


def ledger(name):
    year, lv, key = re.fullmatch(r'review_(\d{4})_(hl|ol)_(p\d)', name).groups()
    return f'scripts/markbank/mathematics/reviews/{year}-{LEVEL[lv]}-{key}.json'


def main():
    names = sys.argv[1:] or sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(HERE, 'review_20*.py')))
    dirty = subprocess.run(['git', 'diff', '--quiet', '--', AUTHORED, 'scripts/markbank/mathematics/reviews'])
    if dirty.returncode:
        sys.exit('authored deck or review ledgers have uncommitted changes; commit or restore them first')
    failed = []
    for name in names:
        out = ledger(name)
        run = subprocess.run([sys.executable, os.path.join(HERE, name + '.py')], capture_output=True, text=True)
        if run.returncode:
            failed.append(name)
            print(f'FAIL {name}: exited {run.returncode}\n{run.stdout[-1500:]}{run.stderr[-1500:]}')
        else:
            diff = subprocess.run(['git', 'diff', '--stat', '--', AUTHORED, out], capture_output=True, text=True).stdout
            if diff.strip():
                failed.append(name)
                print(f'FAIL {name}: output differs from the commit\n{diff}')
            else:
                print(f'ok   {name}: {out} and its cards reproduced byte for byte')
        subprocess.run(['git', 'checkout', '--', AUTHORED, out], check=True)
    print(f'{len(names) - len(failed)} of {len(names)} generators reproduce the committed output')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
