#!/usr/bin/env python3
"""Verify or restore the 2026-10-08 subject checkpoints without altering a checkout."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / 'docs/subject-handoffs/2026-10-08'


def run(*args):
    subprocess.run(args, cwd=REPO, check=True)


def assemble(destination, manifest):
    whole = hashlib.sha256()
    total = 0
    with destination.open('wb') as output:
        for part in manifest['parts']:
            path = ROOT / part['path']
            if path.resolve().parent != (ROOT / 'archive').resolve():
                raise ValueError('Invalid archive part path')
            digest = hashlib.sha256()
            size = 0
            with path.open('rb') as source:
                for block in iter(lambda: source.read(1024 * 1024), b''):
                    digest.update(block)
                    whole.update(block)
                    output.write(block)
                    size += len(block)
            if digest.hexdigest() != part['sha256'] or size != part['bytes']:
                raise ValueError(f'Archive checksum mismatch: {path.name}')
            total += size
    if whole.hexdigest() != manifest['sha256'] or total != manifest['bytes']:
        raise ValueError('Complete archive checksum mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List saved subjects without unpacking')
    parser.add_argument('--verify', action='store_true', help='Verify all parts and Git prerequisites')
    parser.add_argument('--subject', help='Subject slug from --list')
    parser.add_argument('--destination', type=Path, help='New, nonexistent worktree directory')
    parser.add_argument('--branch', help='New branch name; default resume/SUBJECT-20261008')
    args = parser.parse_args()
    subjects = json.loads((ROOT / 'snapshots.json').read_text())['subjects']
    if args.list:
        for subject in subjects:
            print(f"{subject['subject']:24} {subject['snapshotCommit']}  {subject['handoff']}")
        return
    if not args.verify and not (args.subject and args.destination):
        parser.error('Choose --list, --verify, or --subject SLUG --destination NEW_DIRECTORY')
    selected = next((item for item in subjects if item['subject'] == args.subject), None)
    if args.subject and selected is None:
        parser.error('Unknown subject; use --list')
    if args.subject and (args.destination.exists() or args.destination.is_symlink()):
        parser.error('Destination must not exist; original worktrees are never overwritten')
    manifest = json.loads((ROOT / 'archive-manifest.json').read_text())
    with tempfile.TemporaryDirectory(prefix='nsu-subject-checkpoint-') as directory:
        bundle = Path(directory) / 'subjects.bundle'
        assemble(bundle, manifest)
        run('git', 'bundle', 'verify', str(bundle))
        print('All archive parts and the complete bundle match their SHA-256 checksums.')
        if not args.subject:
            return
        ref = selected['snapshotRef']
        run('git', 'fetch', '--no-tags', str(bundle), f'{ref}:{ref}')
        restored = subprocess.check_output(['git', 'rev-parse', ref], cwd=REPO, text=True).strip()
        if restored != selected['snapshotCommit']:
            raise ValueError('Restored commit differs from manifest')
        branch = args.branch or f'resume/{args.subject}-20261008'
        run('git', 'worktree', 'add', '-b', branch, str(args.destination.resolve()), restored)
        print(f"Restored {args.subject} exactly. Read {args.destination / 'docs/subject-handoffs/2026-10-08' / selected['handoff']} before doing work.")
        print('Install dependencies and follow source-corpus instructions in the handoff. Do not merge this entire historical tree onto main.')


if __name__ == '__main__':
    main()
