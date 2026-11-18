import { describe, expect, test } from 'vitest';
import { courseworkBrief, courseworkCatalogue } from '../data/curriculum/coursework';
import research from '../data/curriculum/courseworkResearch.json';
import { courseworkDemo } from '../components/CourseworkStudio/demo';
import { activeEvidence, calendarExport, connectionComplete, createProject, mergeBackup, nextMove, parseBackup, reviewExport, safeUrl } from '../components/CourseworkStudio/model';

describe('Coursework Studio cohort and source boundaries',()=>{
  test('every researched subject resolves through the canonical registry in both supported cohorts',()=>{
    for(const id of Object.keys(research.rows)) for(const year of [2027,2028]) {
      expect(courseworkBrief(id,year),`${id}:${year}`).toBeDefined();
      expect(courseworkBrief(id,year)?.sources.length).toBeGreaterThan(0);
    }
  });
  test('Geography and Engineering keep outgoing and incoming assessment structures separate',()=>{
    expect(courseworkBrief('geography',2027)?.assessment).toContain('20%');
    expect(courseworkBrief('geography',2028)?.assessment).toContain('40%');
    expect(courseworkBrief('engineering',2027)?.assessment).toContain('Ordinary 30% + 30% + 40%');
    expect(courseworkBrief('engineering',2028)?.assessment).toContain('50% Design and Manufacture');
    expect(courseworkBrief('engineering',2027)?.specification.id).not.toBe(courseworkBrief('engineering',2028)?.specification.id);
  });
  test('annual word limits never leak into the next exam year or unknown future cohorts',()=>{
    expect(courseworkBrief('business',2027)?.limits?.words).toBe(1500);
    expect(courseworkBrief('business',2028)?.limits).toBeUndefined();
    expect(courseworkBrief('business',2029)).toBeUndefined();
    expect(courseworkCatalogue(2029).every(s=>s.research===undefined)).toBe(true);
  });
  test('orals and learning portfolios do not become submitted coursework',()=>{
    for(const id of ['irish','arabic','french','mandarin-chinese','mathematics']) {
      expect(courseworkBrief(id,2027)?.canCreate).toBe(false);
      expect(()=>createProject(id,2027,'higher','Standard','Test')).toThrow();
    }
  });
});
describe('Evidence, backup and handover',()=>{
  test('a connected claim needs live evidence, reasoning and a limitation',()=>{
    const p=courseworkDemo().projects[0]; const c=p.connections[0];
    expect(connectionComplete(p,c)).toBe(true);
    expect(connectionComplete(p,{...c,reasoning:''})).toBe(false);
    expect(connectionComplete(p,{...c,limitation:''})).toBe(false);
    p.evidence=p.evidence.map(e=>({...e,archived:true}));
    expect(activeEvidence(p)).toHaveLength(0);
    expect(connectionComplete(p,c)).toBe(false);
  });
  test('next moves flag untraceable sources before suggesting a polished conclusion',()=>{
    const p=courseworkDemo().projects[0];p.evidence[0].locator='';
    expect(nextMove(p).title).toBe('Make a source traceable.');
    p.focus='';expect(nextMove(p).action).toBe('focus');
  });
  test('backup round trip retains references, links and attached originals',()=>{
    const data=courseworkDemo();data.projects[0].evidence[0].files=[{id:'file1',name:'note.txt',type:'text/plain',size:5,data:'data:text/plain;base64,SGVsbG8='}];
    expect(parseBackup(JSON.stringify(data))).toEqual(data);
  });
  test('imports reject invalid nested records and dangling evidence references',()=>{
    const data=courseworkDemo();data.projects[0].connections[0].evidenceIds=['missing'];
    expect(()=>parseBackup(JSON.stringify(data))).toThrow('valid Coursework Studio backup');
    const other=courseworkDemo();other.projects[0].milestones[0].minutes=-4;
    expect(()=>parseBackup(JSON.stringify(other))).toThrow();
    const badDate=courseworkDemo();badDate.projects[0].evidence[0].date='2027-02-31';
    expect(()=>parseBackup(JSON.stringify(badDate))).toThrow();
  });
  test('a mismatched specification cannot be imported under another exam cohort',()=>{
    const data=courseworkDemo();data.projects=[createProject('geography',2027,'higher','Standard','Fieldwork')];data.projects[0].examYear=2028;
    expect(()=>parseBackup(JSON.stringify(data))).toThrow();
  });
  test('imports create separate copies, without replacing existing project data',()=>{
    const data=courseworkDemo();const merged=mergeBackup(data,data);
    expect(merged.projects).toHaveLength(4);expect(merged.projects[0]).toEqual(data.projects[0]);
    expect(merged.projects[2].id).not.toBe(data.projects[0].id);
    expect(merged.projects[2].connections[0].evidenceIds).toEqual(data.projects[0].connections[0].evidenceIds);
  });
  test('review exports escape student text and never execute source URLs',()=>{
    const p=courseworkDemo().projects[0];p.title='<script>alert(1)</script>';p.evidence[0].url='javascript:alert(1)';
    const html=reviewExport(p);expect(html).not.toContain('<script>');expect(html).toContain('&lt;script&gt;');
    expect(html).not.toContain('href="javascript:');expect(safeUrl(p.evidence[0].url)).toBe('');
    expect(html).toContain('not an SEC submission');
  });
  test('calendar exports include only dated unfinished personal checkpoints',()=>{
    const p=courseworkDemo().projects[0];p.milestones[0].date='2026-11-01';p.milestones[2].date='2026-11-07';
    const ics=calendarExport(p);expect(ics).toContain('DTSTART;VALUE=DATE:20261107');expect(ics).not.toContain('DTSTART;VALUE=DATE:20261101');expect(ics).toContain('not an SEC deadline');
  });
});
