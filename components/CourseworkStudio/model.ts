import { validSupport, validPressureReview, type SupportData, type PressureReview } from './supportState';
import { courseworkBrief, workflowGuides } from '../../data/curriculum/coursework';
export const evidenceKinds = ['Source', 'Observation', 'Decision', 'Feedback', 'Reflection'] as const;
export type EvidenceKind = typeof evidenceKinds[number];
export interface CourseworkFile { id: string; name: string; type: string; size: number; data: string }
export interface Evidence { id: string; kind: EvidenceKind; title: string; notes: string; why: string; author: string; locator: string; url: string; quote: string; date: string; files: CourseworkFile[]; archived: boolean }
export interface Connection { pressureReview?: PressureReview; id: string; claim: string; evidenceIds: string[]; reasoning: string; limitation: string }
export interface Milestone { details?: string; evidenceId?: string; id: string; label: string; done: boolean; date: string; setting: 'Anywhere' | 'With my teacher'; minutes: number }
export interface CourseworkProject { support?: SupportData; id: string; subjectId: string; specificationId: string; examYear: number; level: string; route: string; title: string; focus: string; evidence: Evidence[]; connections: Connection[]; milestones: Milestone[]; reflection: string; reportText: string; imageCount: number; reviewChecks: string[]; updatedAt: string; createdAt: string }
export interface CourseworkWorkspace { version: 1; revision: number; projects: CourseworkProject[] }
export const emptyWorkspace = (): CourseworkWorkspace => ({ version: 1, revision: 0, projects: [] });
export const newId = () => crypto.randomUUID();
export const today = () => new Date().toLocaleDateString('en-CA', { timeZone: 'Europe/Dublin' });
export const safeUrl = (value: string) => { try { const url = new URL(value); return ['http:', 'https:'].includes(url.protocol) ? url.href : ''; } catch { return ''; } };
export const wordCount = (value: string) => value.trim().match(/\S+/g)?.length ?? 0;
export function createProject(subjectId: string, examYear: number, level: string, route: string, title: string): CourseworkProject {
  const brief = courseworkBrief(subjectId, examYear);
  if (!brief?.canCreate) throw new Error('Choose a supported coursework subject and exam year.');
  const now = new Date().toISOString();
  return { id: newId(), subjectId, specificationId: brief.specification.id, examYear, level, route, title: title.trim() || brief.specification.subjectName + ' project', focus: '', evidence: [], connections: [],
    milestones: workflowGuides[brief.family].steps.map((label, i) => ({ id: newId(), label, done: false, date: '', setting: i === 0 ? 'With my teacher' : 'Anywhere', minutes: 25 })), reflection: '', reportText: '', imageCount: 0, reviewChecks: [], createdAt: now, updatedAt: now };
}
export const activeEvidence = (project: CourseworkProject) => project.evidence.filter(item => !item.archived);
export const connectedEvidence = (project: CourseworkProject, connection: Connection) => activeEvidence(project).filter(item => connection.evidenceIds.includes(item.id));
export const connectionComplete = (project: CourseworkProject, connection: Connection) => !!(connectedEvidence(project, connection).length && connection.reasoning.trim() && connection.limitation.trim());
export function nextMove(project: CourseworkProject): { title: string; detail: string; action: 'focus' | 'evidence' | 'connections' | 'review' | 'plan' } {
  if (!project.focus.trim()) return { title: 'Give your project a clear question.', detail: 'A small, answerable question makes the next decision easier.', action: 'focus' };
  const evidence = activeEvidence(project);
  if (!evidence.length) return { title: 'Save the first piece of your process.', detail: 'A source, observation or decision is enough to begin.', action: 'evidence' };
  if (evidence.some(item => item.kind === 'Source' && (!item.author.trim() || !item.locator.trim()))) return { title: 'Make a source traceable.', detail: 'One source still needs its author or page / publication detail. Add it while it is easy to find.', action: 'evidence' };
  if (!project.connections.length) return { title: 'Turn evidence into understanding.', detail: 'Choose one thing you learned and show what supports it.', action: 'connections' };
  if (project.connections.some(item => !connectionComplete(project, item))) return { title: 'Strengthen a connection.', detail: 'Link evidence, explain the connection and acknowledge a limitation.', action: 'connections' };
  if (project.milestones.some(item => !item.done)) return { title: project.milestones.find(item => !item.done)!.label, detail: 'Your next unfinished milestone. Adjust the plan if your work has changed.', action: 'plan' };
  return { title: 'Get ready to explain your work.', detail: 'Review the evidence trail and prepare a question for your teacher.', action: 'review' };
}
export const reviewQuestions = ['I have checked the current brief and my level / elective with my teacher.', 'My evidence and reflections describe my own work.', 'I have referenced quotations, sources and any assistance.', 'I have checked the required files and their readability.', 'I know my teacher’s handover and authentication arrangements.'];

const mimeTypes = ['image/png', 'image/jpeg', 'image/webp', 'application/pdf', 'text/plain', 'text/csv', 'audio/mpeg', 'audio/mp4', 'video/mp4'];
export const MAX_FILE_BYTES = 8 * 1024 * 1024;
export const MAX_BACKUP_BYTES = 80 * 1024 * 1024;
export async function readEvidenceFile(file: File): Promise<CourseworkFile> {
  if (!mimeTypes.includes(file.type)) throw new Error('Use PNG, JPG, WebP, PDF, TXT, CSV, MP3, M4A or MP4.');
  if (file.size > MAX_FILE_BYTES) throw new Error('Each attachment can be up to 8 MB. Keep larger originals in your own backed-up folder.');
  const data = await new Promise<string>((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(String(reader.result)); reader.onerror = () => reject(new Error('This file could not be read. Your note is still here.')); reader.readAsDataURL(file); });
  return { id: newId(), name: file.name, type: file.type, size: file.size, data };
}
/** Validate every nested import before it can enter the store. Never silently drop corrupt records. */
export function parseBackup(text: string): CourseworkWorkspace {
  if (text.length > MAX_BACKUP_BYTES) throw new Error('This backup is too large (80 MB maximum).');
  const raw: unknown = JSON.parse(text);
  const object = (v: unknown): v is Record<string, unknown> => !!v && typeof v === 'object' && !Array.isArray(v);
  const string = (v: unknown, max = 50000): v is string => typeof v === 'string' && v.length <= max;
  const strings = (v: unknown): v is string[] => Array.isArray(v) && v.length <= 1000 && v.every(x => string(x, 200));
  const date = (v: unknown) => v === '' || (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v) && !Number.isNaN(Date.parse(v)) && new Date(v).toISOString().slice(0,10) === v);
  const unique = (v: { id: string }[]) => new Set(v.map(x => x.id)).size === v.length;
  const file = (v: unknown): v is CourseworkFile => object(v) && string(v.id, 100) && string(v.name, 300) && typeof v.size === 'number' && v.size >= 0 && v.size <= MAX_FILE_BYTES && mimeTypes.includes(String(v.type)) && typeof v.data === 'string' && v.data.length <= MAX_FILE_BYTES * 1.4 && v.data.startsWith(`data:${v.type};base64,`) && /^[A-Za-z0-9+/=]*$/.test(v.data.split(',')[1] ?? '');
  const evidence = (v: unknown): v is Evidence => object(v) && ['id','title','notes','why','author','locator','url','quote'].every(k => string(v[k])) && evidenceKinds.includes(v.kind as EvidenceKind) && date(v.date) && typeof v.archived === 'boolean' && Array.isArray(v.files) && v.files.length <= 20 && v.files.every(file) && unique(v.files);
  const connection = (v: unknown): v is Connection => object(v) && (v.pressureReview === undefined || validPressureReview(v.pressureReview)) && ['id','claim','reasoning','limitation'].every(k => string(v[k])) && strings(v.evidenceIds);
  const milestone = (v: unknown): v is Milestone => object(v) && (v.details === undefined || string(v.details)) && (v.evidenceId === undefined || string(v.evidenceId, 100)) && string(v.id, 100) && string(v.label, 500) && typeof v.done === 'boolean' && date(v.date) && ['Anywhere','With my teacher'].includes(String(v.setting)) && Number.isInteger(v.minutes) && Number(v.minutes) >= 5 && Number(v.minutes) <= 240;
  const project = (v: unknown): v is CourseworkProject => object(v) && (v.support === undefined || validSupport(v.support)) && ['id','subjectId','specificationId','level','route','title','focus','reflection','reportText','updatedAt','createdAt'].every(k => string(v[k])) && [2027,2028].includes(Number(v.examYear)) && typeof v.examYear === 'number' && Number.isInteger(v.imageCount) && Number(v.imageCount) >= 0 && Number(v.imageCount) <= 1000 && strings(v.reviewChecks) && Array.isArray(v.evidence) && v.evidence.length <= 1000 && v.evidence.every(evidence) && unique(v.evidence) && Array.isArray(v.connections) && v.connections.length <= 1000 && v.connections.every(connection) && unique(v.connections) && v.connections.every(c => c.evidenceIds.every(id => (v.evidence as Evidence[]).some(e => e.id === id))) && Array.isArray(v.milestones) && v.milestones.length <= 1000 && v.milestones.every(milestone) && unique(v.milestones) && v.milestones.every(m => !m.evidenceId || (v.evidence as Evidence[]).some(e => e.id === m.evidenceId)) && v.connections.every(c => !c.pressureReview || Object.keys(c.pressureReview.roles).every(id => (v.evidence as Evidence[]).some(e => e.id === id)) && (!c.pressureReview.withheld || (v.evidence as Evidence[]).some(e => e.id === c.pressureReview!.withheld))) && courseworkBrief(String(v.subjectId), Number(v.examYear))?.specification.id === v.specificationId;
  if (!object(raw) || raw.version !== 1 || !Number.isInteger(raw.revision) || Number(raw.revision) < 0 || !Array.isArray(raw.projects) || raw.projects.length > 100 || !raw.projects.every(project) || !unique(raw.projects)) throw new Error('This is not a valid Coursework Studio backup. Nothing has been changed.');
  return raw as unknown as CourseworkWorkspace;
}
export function mergeBackup(workspace: CourseworkWorkspace, imported: CourseworkWorkspace): CourseworkWorkspace {
  if (workspace.projects.length + imported.projects.length > 100) throw new Error('A workspace can contain up to 100 projects.');
  return { ...workspace, projects: [...workspace.projects, ...imported.projects.map(p => ({ ...p, id: newId(), title: p.title + ' (imported)' }))] };
}
export function download(content: string, type: string, name: string) {
  const url = URL.createObjectURL(new Blob([content], { type })); const a = document.createElement('a'); a.href = url; a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export function calendarExport(project: CourseworkProject): string {
  const escape = (value: string) => value.replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;').replace(/\r/g, '');
  const events = project.milestones.filter(m => m.date && !m.done).map(m => ['BEGIN:VEVENT', `UID:${project.id}.${m.id}@nextstepuni`, `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}Z`, `DTSTART;VALUE=DATE:${m.date.replace(/-/g, '')}`, `SUMMARY:${escape(m.label)}`, `DESCRIPTION:${escape(project.title + ' · Personal checkpoint, not an SEC deadline. ' + m.setting)}`, 'END:VEVENT'].join('\r\n'));
  return ['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//NextStepUni//Coursework Studio//EN',...events,'END:VCALENDAR'].join('\r\n');
}
export function reviewExport(project: CourseworkProject): string {
  const esc = (value: string) => value.replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]!));
  const paragraph = (value: string) => `<p>${esc(value).replace(/\n/g, '<br>')}</p>`;
  const evidence = activeEvidence(project);
  return `<!doctype html><html lang="en"><meta charset="utf-8"><title>${esc(project.title)} — teacher review</title><style>body{font:16px/1.6 system-ui;max-width:850px;margin:50px auto;padding:20px;color:#202020}h1,h2{font-family:Georgia}article{border-top:1px solid #ccc;padding:20px 0}small{color:#555}@media print{article{break-inside:avoid}}</style><h1>${esc(project.title)}</h1><p>NextStepUni / Coursework Studio · ${project.examYear} · ${esc(project.level)} · ${esc(project.route)}</p><p>Teacher discussion pack. This is not an SEC submission or authentication.</p><h2>My question</h2>${paragraph(project.focus)}<h2>My evidence trail</h2>${evidence.map(e => `<article><h3>${esc(e.title)}</h3><small>${esc(e.kind)} · ${esc(e.date)}</small>${paragraph(e.notes)}${paragraph('Why I kept it: ' + e.why)}${e.quote ? paragraph('Quotation: ' + e.quote) : ''}${paragraph([e.author,e.locator,e.url].filter(Boolean).join(' · '))}${paragraph('Attachments retained in backup: ' + (e.files.map(f => f.name).join(', ') || 'none'))}</article>`).join('')}<h2>Connections I can explain</h2>${project.connections.map(c => `<article><h3>${esc(c.claim)}</h3>${paragraph('Evidence: ' + connectedEvidence(project,c).map(e => e.title).join('; '))}${paragraph(c.reasoning)}${paragraph('Limitations: ' + c.limitation)}${c.pressureReview ? paragraph('Next investigation: ' + c.pressureReview.next) : ''}</article>`).join('')}<h2>Reflection and questions for my teacher</h2>${paragraph(project.reflection)}<h2>My plan</h2>${project.milestones.map(m => paragraph(`${m.done ? 'Done' : 'To do'} · ${m.label}${m.date ? ' · '+m.date : ''} · ${m.setting}${m.details ? '\n'+m.details : ''}`)).join('')}</html>`;
}
