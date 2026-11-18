import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import recovered from '../scripts/markbank/authored/irish-recovered-schemes.json';
import { hostedPaperDocumentUrl, paperStoragePath, paperUrl } from '../components/PaperTrail/storage';
import { resolveSibling } from '../components/PaperTrail/vaultResolve';

describe('recovered legacy Irish schemes', () => {
  it('ships the exact verified PDFs and resolves all affected paper kinds to those documents', () => {
    for(const record of recovered) {
      const data=readFileSync('public'+record.hostedPath);
      expect(data.byteLength).toBe(record.bytes);
      expect(data.subarray(0,5).toString()).toBe('%PDF-');
      expect(createHash('sha256').update(data).digest('hex')).toBe(record.sha256);
      const storage=paperStoragePath('lc','irish',record.year,'scheme',record.fileid);
      expect(hostedPaperDocumentUrl(storage)).toBe(record.hostedPath);
      expect(paperUrl(storage)).toBe(record.hostedPath);
      const code=record.level==='higher'?'A':record.level==='ordinary'?'G':'B';
      for(const [component,paperKey] of [['100','p1'],['200','p2'],['A00','aural']] as const) {
        if(record.level==='foundation' && component==='200') continue;
        const sibling=resolveSibling({subjectId:'irish',year:record.year,
          level:record.level as 'higher'|'ordinary'|'foundation',lang:'iv',paperKey,
          fileid:`LC001${code}LP${component}IV.pdf`,n:'1'})!;
        expect(sibling.schemeUrl).toBe(record.hostedPath);
      }
      // Same-year papers and other years must not accidentally use the scheme.
      expect(hostedPaperDocumentUrl(paperStoragePath('lc','irish',record.year,'paper',record.fileid))).toBeNull();
      expect(hostedPaperDocumentUrl(paperStoragePath('lc','irish',2026,'scheme',record.fileid))).toBeNull();
    }
  });
});
