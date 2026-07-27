/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the offline-write rule documented in utils/firestoreWrite.ts:
 *
 *   NEVER gate UI on a Firestore write promise.
 *
 * With persistentLocalCache (firebase.ts), a write promise resolves only on
 * SERVER acknowledgement — offline it never resolves and never rejects. Any
 * `await` on a write, with UI work after it, is a permanent hang: a dead
 * button, a spinner that never clears, a modal that never closes. A sweep in
 * 2026-07 found 36 such sites across 22 files, including one that stranded
 * students at the end of onboarding with no error at all.
 *
 * Part 1 is a source scan that fails if the pattern comes back.
 * Part 2 tests the helpers that replaced it.
 */
import { describe, it, expect, vi } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { saveInBackground, awaitWriteOrTimeout } from '../utils/firestoreWrite';

const ROOT = resolve(__dirname, '..');
const SCAN_DIRS = ['components', 'hooks', 'contexts', 'utils', 'data'];

function sourceFiles(dir: string): string[] {
  const out: string[] = [];
  const walk = (d: string) => {
    for (const entry of readdirSync(d)) {
      if (entry === 'node_modules' || entry.startsWith('.')) continue;
      const full = join(d, entry);
      if (statSync(full).isDirectory()) walk(full);
      else if (/\.tsx?$/.test(entry)) out.push(full);
    }
  };
  walk(join(ROOT, dir));
  return out;
}

const FILES = SCAN_DIRS.flatMap(sourceFiles).concat([join(ROOT, 'App.tsx')]);

// Writes only. getDoc/getDocs resolve from cache offline and are fine to await.
const AWAITED_WRITE = /\bawait\s+(setDoc|updateDoc|addDoc|deleteDoc)\s*\(/g;

describe('no awaited Firestore writes', () => {
  it('finds none in app source', () => {
    const offenders: string[] = [];
    for (const file of FILES) {
      // utils/firestoreWrite.ts documents the banned pattern in its comment.
      if (file.endsWith('utils/firestoreWrite.ts')) continue;
      // Strip comments so documentation of the anti-pattern doesn't self-trip.
      const src = readFileSync(file, 'utf8')
        .replace(/\/\*[\s\S]*?\*\//g, '')
        .replace(/^\s*\/\/.*$/gm, '');
      for (const m of src.matchAll(AWAITED_WRITE)) {
        const line = src.slice(0, m.index).split('\n').length;
        offenders.push(`${file.replace(ROOT + '/', '')}:${line}  await ${m[1]}(`);
      }
    }
    expect(
      offenders,
      'A Firestore write promise settles only on SERVER ack — offline it never settles at all, so\n' +
      'anything after the await never runs. Use saveInBackground() (fire + rollback on rejection) or\n' +
      'awaitWriteOrTimeout() (bounded wait) from utils/firestoreWrite.\n' +
      `Offenders:\n${offenders.join('\n')}`,
    ).toEqual([]);
  });

  it('still allows awaited READS, which resolve from the local cache', () => {
    // Sanity check that the pattern is write-only: the codebase awaits getDoc
    // in many places and that is correct.
    const anyAwaitedRead = FILES.some(f => /\bawait\s+getDocs?\s*\(/.test(readFileSync(f, 'utf8')));
    expect(anyAwaitedRead).toBe(true);
  });
});

describe('saveInBackground', () => {
  it('does not block the caller', async () => {
    // A promise that never settles — exactly what an offline write looks like.
    const neverSettles = new Promise<void>(() => {});
    const reached = await Promise.race([
      (async () => { saveInBackground(neverSettles, 'test.never'); return 'returned'; })(),
      new Promise(r => setTimeout(() => r('timed-out'), 50)),
    ]);
    expect(reached).toBe('returned');
  });

  it('runs the rollback on a genuine rejection', async () => {
    const rollback = vi.fn();
    saveInBackground(Promise.reject(new Error('permission-denied')), 'test.rejects', rollback);
    await new Promise(r => setTimeout(r, 0));
    expect(rollback).toHaveBeenCalledOnce();
  });

  it('does not run the rollback when the write succeeds', async () => {
    const rollback = vi.fn();
    saveInBackground(Promise.resolve(), 'test.resolves', rollback);
    await new Promise(r => setTimeout(r, 0));
    expect(rollback).not.toHaveBeenCalled();
  });

  it('survives a throwing rollback', async () => {
    saveInBackground(Promise.reject(new Error('x')), 'test.badRollback', () => { throw new Error('rollback blew up'); });
    await new Promise(r => setTimeout(r, 0));
    // No unhandled rejection — reaching here is the assertion.
    expect(true).toBe(true);
  });
});

describe('awaitWriteOrTimeout', () => {
  it('reports "pending" instead of hanging forever on an unsettled write', async () => {
    const neverSettles = new Promise<void>(() => {});
    const outcome = await awaitWriteOrTimeout(neverSettles, 'test.offline', 20);
    expect(outcome).toBe('pending');
  });

  it('reports "acked" when the server confirms', async () => {
    expect(await awaitWriteOrTimeout(Promise.resolve(), 'test.ok', 50)).toBe('acked');
  });

  it('reports "failed" on a real rejection', async () => {
    expect(await awaitWriteOrTimeout(Promise.reject(new Error('denied')), 'test.denied', 50)).toBe('failed');
  });

  it('distinguishes "pending" from "failed" — queued is not an error', async () => {
    // The whole point: offline must not be reported to the student as a
    // failure, because the write is queued and will flush on reconnect.
    const pending = await awaitWriteOrTimeout(new Promise<void>(() => {}), 'test.p', 10);
    const failed = await awaitWriteOrTimeout(Promise.reject(new Error('e')), 'test.f', 10);
    expect(pending).not.toBe(failed);
  });
});
