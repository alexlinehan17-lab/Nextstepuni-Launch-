/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const root = resolve(__dirname, '..');
const read = (path: string) => readFileSync(resolve(root, path), 'utf8');

describe('security deployment invariants', () => {
  it('puts every callable behind the shared App Check deployment option', () => {
    for (const file of [
      'functions/src/index.ts',
      'functions/src/aggregateCounters.ts',
      'functions/src/anonymousFeedback.ts',
      'functions/src/dataRights.ts',
      'functions/src/gcPasswordReset.ts',
      'functions/src/peerInteractions.ts',
      'functions/src/schoolAccess.ts',
      'functions/src/staffAccess.ts',
      'functions/src/staffMessage.ts',
    ]) {
      const source = read(file);
      const calls = [...source.matchAll(/onCall\s*\(/g)];
      expect(calls.length, `${file} should contain a callable`).toBeGreaterThan(0);
      expect(source, `${file} bypasses CALLABLE_OPTIONS`)
        .not.toMatch(/onCall\s*\(\s*\{(?!\s*\.\.\.CALLABLE_OPTIONS)/);
    }
  });

  it('enforces CSP and keeps executable scripts free of unsafe-inline', () => {
    const config = JSON.parse(read('firebase.json')) as {
      hosting: { headers: Array<{ headers: Array<{ key: string; value: string }> }> };
    };
    const headers = config.hosting.headers.flatMap(entry => entry.headers);
    const csp = headers.find(header => header.key === 'Content-Security-Policy')?.value ?? '';
    expect(csp).toContain("default-src 'self'");
    expect(csp).toContain("frame-ancestors 'none'");
    expect(csp.match(/script-src[^;]*/)?.[0]).not.toContain("'unsafe-inline'");
    expect(headers.some(header => header.key === 'Content-Security-Policy-Report-Only')).toBe(false);
  });

  it('uses short-lived CI credentials and immutable action revisions', () => {
    const workflow = read('.github/workflows/ci.yml');
    expect(workflow).toContain('workload_identity_provider:');
    expect(workflow).toContain('service_account:');
    expect(workflow).not.toContain('credentials_json:');
    expect(workflow).not.toMatch(/uses:\s+[^\s]+@v\d/);
    expect(workflow).toContain('npx --no-install firebase deploy');
    expect(workflow).not.toContain('--omit=dev');
  });

  it('does not retain account data in web caches or Android backups', () => {
    const firebase = read('firebase.ts');
    expect(firebase).toContain('browserSessionPersistence');
    expect(firebase).toContain('memoryLocalCache()');
    const manifest = read('android/app/src/main/AndroidManifest.xml');
    expect(manifest).toContain('android:allowBackup="false"');
    expect(manifest).toContain('android:fullBackupContent="false"');
  });

  it('keeps school binding live, atomic, and out of student token claims', () => {
    const schoolAccess = read('functions/src/schoolAccess.ts');
    const claims = read('functions/src/authClaims.ts');
    expect(schoolAccess).toContain('db.runTransaction');
    expect(schoolAccess).toContain('transaction.get(attemptsRef)');
    expect(schoolAccess).toContain('transaction.get(secretRef)');
    expect(schoolAccess).not.toContain('syncAuthorizationClaims');
    expect(claims).toContain('(role === "gc" || role === "staff")');
  });

  it('ends the one-use session that finalises an email password reset', () => {
    expect(read('functions/src/index.ts'))
      .toContain('sessionValidAfterSeconds: authTimeSeconds(request.auth)');
  });

  it('has removed the credential-spoofing provisioning script', () => {
    expect(existsSync(resolve(root, 'scripts/provision-gc.mjs'))).toBe(false);
    expect(existsSync(resolve(root, 'scripts/seed-demo.mjs'))).toBe(false);
    const reviewPasswordLines = [...read('docs/play-listing.md').matchAll(/^Password:\s*(.+)$/gm)]
      .map(([, value]) => value.trim());
    expect(reviewPasswordLines).toEqual([
      '[retrieve the current value from the release password manager]',
    ]);
    expect(read('docs/app-store-listing.md')).not.toContain('NextStep-Demo-2026');
  });
});
