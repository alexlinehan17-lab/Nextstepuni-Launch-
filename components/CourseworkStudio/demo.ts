import { createProject, newId, type CourseworkWorkspace } from './model';
/** Fictional process notes for the explicitly labelled, isolated review account. No real results. */
export function courseworkDemo(): CourseworkWorkspace {
  const business=createProject('business',2027,'higher','Standard','The changing working day');
  business.focus='How could digital scheduling affect the working day for employees in a small café?';
  business.milestones[0].done=true;business.milestones[1].done=true;
  business.evidence=[
    {id:newId(),kind:'Source',title:'The brief: one work practice, one perspective',notes:'The task lets me focus on employers or employees. I am narrowing my question to employees so that my investigation stays manageable.',why:'This keeps the question connected to the actual brief.',author:'State Examinations Commission',locator:'Business Alive 2027 brief, section 5',url:'https://exams.ie/project-files/lc/business/2026-27-project-brief.pdf',quote:'',date:'2026-10-27',files:[],archived:false},
    {id:newId(),kind:'Decision',title:'Keep the enquiry small enough to answer',notes:'I will focus on scheduling, rather than every kind of digital technology used in a café. I still need to agree what evidence is practical to collect.',why:'A narrower question leaves room to analyse the evidence properly.',author:'',locator:'',url:'',quote:'',date:'2026-10-28',files:[],archived:false},
    {id:newId(),kind:'Reflection',title:'A faster process is not the whole story',notes:'I need to distinguish time saved by a manager from the employee’s experience. I have not collected enough evidence to claim an effect yet.',why:'This is a question to investigate, not a finding.',author:'',locator:'',url:'',quote:'',date:'2026-10-29',files:[],archived:false},
  ];
  business.connections=[{id:newId(),claim:'My investigation should focus on one work practice and the employee perspective.',evidenceIds:[business.evidence[0].id,business.evidence[1].id],reasoning:'The brief permits either perspective. Keeping the scope small gives me a question I can investigate and explain.',limitation:'A narrower scope will not describe every effect of digitalisation on a workplace.'}];
  const biology=createProject('biology',2027,'higher','Standard','Food preservation, under the lens');
  biology.focus='Which aspect of osmosis and food preservation can I investigate safely with my teacher?';
  return {version:1,revision:0,projects:[business,biology]};
}
