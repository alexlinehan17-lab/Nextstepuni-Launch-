import { CAREERS } from '../careerPathsData';
import type { CareerCard, CareerField } from '../types/careerPaths';

export const LIFE_PRIORITIES = [
  'creative', 'secure', 'social', 'independent', 'outdoors', 'useful',
  'flexible', 'challenging', 'calm', 'well-paid', 'close-to-home', 'open-to-travel',
] as const;

export type LifePriority = typeof LIFE_PRIORITIES[number];

export const PRIORITY_LABELS: Record<LifePriority, string> = {
  creative: 'Creative', secure: 'Secure', social: 'Social', independent: 'Independent',
  outdoors: 'Outdoors', useful: 'Useful', flexible: 'Flexible', challenging: 'Challenging',
  calm: 'Calm', 'well-paid': 'Well-paid', 'close-to-home': 'Close to home',
  'open-to-travel': 'Open to travel',
};

const FIELD_SIGNALS: Partial<Record<LifePriority, CareerField[]>> = {
  creative: ['creative', 'design', 'tech'], secure: ['health', 'education', 'engineering', 'trades'],
  social: ['health', 'psychology', 'education', 'business', 'law'], independent: ['tech', 'creative', 'design', 'science'],
  outdoors: ['animals', 'engineering', 'trades', 'science'], useful: ['health', 'education', 'psychology', 'engineering', 'trades'],
  flexible: ['tech', 'creative', 'design', 'business'], challenging: ['health', 'law', 'engineering', 'science', 'tech'],
  calm: ['design', 'science', 'education', 'animals'], 'well-paid': ['tech', 'law', 'health', 'engineering', 'business'],
};

const KEYWORDS: Partial<Record<LifePriority, string[]>> = {
  social: ['people', 'team', 'client', 'patient', 'teach'], independent: ['independent', 'focus', 'autonomy'],
  outdoors: ['outdoor', 'site', 'field', 'land'], flexible: ['flexible', 'remote', 'freelance', 'hybrid'],
  creative: ['creative', 'design', 'build', 'make'], useful: ['help', 'care', 'solve', 'support'],
  challenging: ['complex', 'problem', 'pressure', 'research'], calm: ['calm', 'steady', 'quiet'],
  'open-to-travel': ['travel', 'international', 'abroad'], 'close-to-home': ['community', 'local'],
};

const haystack = (career: CareerCard) => [career.tagline, ...career.whatYouDo, ...career.skills, ...career.pros].join(' ').toLowerCase();

export function scoreCareer(career: CareerCard, priorities: LifePriority[], matchedIds: string[] = []): number {
  const text = haystack(career);
  return priorities.reduce((score, priority) => {
    const fieldScore = FIELD_SIGNALS[priority]?.includes(career.field) ? 4 : 0;
    const wordScore = KEYWORDS[priority]?.some((word) => text.includes(word)) ? 2 : 0;
    const payScore = priority === 'well-paid' ? career.salary.experiencedK / 25 : 0;
    return score + fieldScore + wordScore + payScore;
  }, matchedIds.includes(career.id) ? 7 : 0);
}

/** Three possibilities, deliberately diversified. They are lenses, not a ranking. */
export function buildPossibilities(priorities: LifePriority[], matchedIds: string[] = []): CareerCard[] {
  const ranked = [...CAREERS].sort((a, b) => scoreCareer(b, priorities, matchedIds) - scoreCareer(a, priorities, matchedIds) || a.title.localeCompare(b.title));
  const picked: CareerCard[] = [];
  const match = ranked.find((career) => matchedIds.includes(career.id));
  if (match) picked.push(match);
  if (!picked.length && ranked[0]) picked.push(ranked[0]);
  const adjacent = ranked.find((career) => !picked.some((item) => item.id === career.id) && career.field !== picked[0]?.field);
  if (adjacent) picked.push(adjacent);
  const different = ranked.find((career) => !picked.some((item) => item.id === career.id) && !picked.some((item) => item.field === career.field));
  if (different) picked.push(different);
  for (const career of ranked) if (picked.length < 3 && !picked.some((item) => item.id === career.id)) picked.push(career);
  return picked.slice(0, 3);
}

export interface PossibleDayBeat {
  /** Illustrative time, never presented as a standard working schedule. */
  time: string;
  title: string;
  detail: string;
}

export interface PossibleDayProfile {
  /** Names which version of a broad career the example follows. */
  setting: string;
  beats: readonly [PossibleDayBeat, PossibleDayBeat, PossibleDayBeat];
  /** A condition of doing the job, never an admissions or education barrier. */
  workplaceReality: string;
}

/**
 * Career-specific ordinary days.
 *
 * A field-level template was too coarse: it made a community pharmacist sound
 * like a laboratory researcher, and using `career.cons[0]` made CAO points look
 * like something that happened at 16:50. These profiles deliberately keep job
 * activity here and leave entry routes, qualifications and points to the route
 * screen where they belong.
 */
export const CAREER_DAY_PROFILES: Record<string, PossibleDayProfile> = {
  nurse: {
    setting: 'This follows a ward-based day shift; community, theatre and specialist nursing have different rhythms.',
    beats: [
      { time: '07:15', title: 'Handover and first checks', detail: 'Read the overnight notes, assess who needs attention first, then check observations and medicines.' },
      { time: '12:10', title: 'Care changes quickly', detail: 'Dress wounds, coordinate tests and explain what is happening to patients and families.' },
      { time: '19:20', title: 'Hand the ward on', detail: 'Update charts, flag concerns and brief the next team before leaving.' },
    ],
    workplaceReality: 'A day shift can be long and physically demanding; nights, weekends, grief and short-staffing are part of many roles.',
  },
  veterinarian: {
    setting: 'This follows a mixed first-opinion practice; farm, referral and public-service veterinary work differ.',
    beats: [
      { time: '08:30', title: 'Consultations begin', detail: 'Examine animals, ask owners what changed and decide which tests or treatment are justified.' },
      { time: '12:45', title: 'Procedure or farm call', detail: 'Move from surgery or scans to a farm visit, with welfare and safety shaping every decision.' },
      { time: '18:10', title: 'The list can change', detail: 'Finish notes and follow-ups, unless an urgent case or on-call request extends the day.' },
    ],
    workplaceReality: 'The work combines unpredictable hours, difficult euthanasia decisions, distressed owners and physical risk around animals.',
  },
  'software-developer': {
    setting: 'This follows a team product role; office, hybrid and remote routines vary by employer.',
    beats: [
      { time: '09:10', title: 'Agree what matters', detail: 'Clarify a feature or bug with the team before touching the code.' },
      { time: '11:30', title: 'Build and debug', detail: 'Write, test and revise code; a large part of progress is finding why something failed.' },
      { time: '16:20', title: 'Review before release', detail: 'Read a teammate’s changes, document decisions and check the software behaves as expected.' },
    ],
    workplaceReality: 'Long screen time, shifting tools and deadline pressure are real; some days end with the same stubborn bug still open.',
  },
  engineer: {
    setting: 'This blends desk and site work; civil, mechanical, electrical and other branches differ substantially.',
    beats: [
      { time: '08:30', title: 'Check the design', detail: 'Run calculations, review drawings and test whether a proposed solution is safe and workable.' },
      { time: '12:20', title: 'Reality interrupts the plan', detail: 'A site, workshop or lab issue forces you to balance materials, cost, safety and time.' },
      { time: '16:45', title: 'Record the decision', detail: 'Update drawings, calculations or reports so the next person can build or test accurately.' },
    ],
    workplaceReality: 'Responsibility for safety is serious, and deadlines can pull the day between desk work, site visits and difficult compromises.',
  },
  'solicitor-barrister': {
    setting: 'This leans towards a solicitor’s day; a barrister may spend more time in independent preparation and court.',
    beats: [
      { time: '08:45', title: 'Prepare the file', detail: 'Read evidence, correspondence and case law; identify what the client needs decided today.' },
      { time: '12:30', title: 'Advise or advocate', detail: 'Meet a client, negotiate, or attend court depending on the practice area.' },
      { time: '17:40', title: 'Turn judgement into writing', detail: 'Draft contracts, letters or submissions and check every detail against a deadline.' },
    ],
    workplaceReality: 'Hours can run well past the visible working day, with high consequences for missed details and pressure from clients or court dates.',
  },
  psychologist: {
    setting: 'This resembles a clinical service; educational, organisational and research psychology look different.',
    beats: [
      { time: '09:00', title: 'Prepare, don’t presume', detail: 'Review notes and choose an assessment or session plan without deciding the answer in advance.' },
      { time: '12:30', title: 'Listen for the pattern', detail: 'Conduct an assessment or therapy session, keeping careful professional boundaries.' },
      { time: '16:30', title: 'Write and consult', detail: 'Score measures, document what happened and discuss complex work in supervision or with a wider team.' },
    ],
    workplaceReality: 'Sustained listening is emotionally demanding, progress can be slow, and reports and risk decisions continue after the session ends.',
  },
  accountant: {
    setting: 'This follows an employed accounting team; practice, audit and self-employed work shift the balance.',
    beats: [
      { time: '08:45', title: 'Reconcile the evidence', detail: 'Check invoices, bank records and ledgers, then investigate anything that does not match.' },
      { time: '12:15', title: 'Explain the numbers', detail: 'Turn accounts into a forecast or clear advice for a manager or client.' },
      { time: '17:15', title: 'Close and document', detail: 'Finish controls, record assumptions and prepare the next deadline.' },
    ],
    workplaceReality: 'Much of the work is desk-based and repetitive; month-end, audit and tax deadlines can stretch hours sharply.',
  },
  teacher: {
    setting: 'This follows a school day; subject, age group and school setting change the routine.',
    beats: [
      { time: '08:20', title: 'Before the bell', detail: 'Set up the lesson, review the plan and deal with the first student or staff questions.' },
      { time: '11:40', title: 'Teach and adapt', detail: 'Explain, question, manage behaviour and change approach when the class is not understanding.' },
      { time: '15:45', title: 'The pupils leave first', detail: 'Mark work, contact home, prepare tomorrow and record progress after class ends.' },
    ],
    workplaceReality: 'The timetable looks predictable, but classroom energy, pastoral issues and substantial preparation outside class make it demanding.',
  },
  architect: {
    setting: 'This follows a design practice during delivery; the project stage determines whether the day is studio, meetings or site.',
    beats: [
      { time: '09:00', title: 'Turn needs into space', detail: 'Develop drawings or a 3D model around the client’s brief, planning rules and budget.' },
      { time: '12:30', title: 'Test it against reality', detail: 'Meet consultants or visit a site to resolve details that do not work on paper.' },
      { time: '17:30', title: 'Revise the package', detail: 'Update drawings and specifications so builders have precise, coordinated information.' },
    ],
    workplaceReality: 'Creative decisions sit inside regulation, cost and safety constraints; revisions and project deadlines can produce long days.',
  },
  pharmacist: {
    setting: 'This follows a community pharmacy; hospital, industry and research pharmacy are different careers within the profession.',
    beats: [
      { time: '08:45', title: 'Safety before speed', detail: 'Check prescriptions, patient details, doses and interactions before anything is dispensed.' },
      { time: '13:00', title: 'Questions at the counter', detail: 'Advise on medicines and minor illnesses while protecting privacy and spotting when referral is safer.' },
      { time: '18:00', title: 'Final checks', detail: 'Resolve outstanding prescriptions, document interventions and make sure stock and handover are in order.' },
    ],
    workplaceReality: 'The role involves prolonged standing, busy public-facing shifts and serious consequences if a safety check is missed.',
  },
  electrician: {
    setting: 'This follows a site or service job; industrial maintenance and specialist electrical work can run different shifts.',
    beats: [
      { time: '07:30', title: 'Make the job safe', detail: 'Read the plan, identify the circuit and isolate the supply before installation or fault-finding.' },
      { time: '11:45', title: 'Install and diagnose', detail: 'Run cable, fit equipment or trace a fault while coordinating with the customer and other trades.' },
      { time: '16:10', title: 'Test before power', detail: 'Measure, verify and document the circuit before it is put into service.' },
    ],
    workplaceReality: 'Early starts, changing sites, awkward spaces and electrical risk make method and concentration non-negotiable.',
  },
  'graphic-designer': {
    setting: 'This follows an agency or in-house project; freelance schedules and client mix vary.',
    beats: [
      { time: '09:15', title: 'Interrogate the brief', detail: 'Clarify the audience, message, formats and deadline before exploring ideas.' },
      { time: '12:30', title: 'Make and compare', detail: 'Build layouts, test type and colour, and prepare a few defensible directions.' },
      { time: '16:45', title: 'Feedback changes the work', detail: 'Present a route, absorb criticism and revise the design for delivery.' },
    ],
    workplaceReality: 'Creative control is shared with clients and deadlines; revisions and production detail take more of the day than pure idea generation.',
  },
  'data-scientist': {
    setting: 'This follows an employed analytics team; research and product roles differ.',
    beats: [
      { time: '09:05', title: 'Define the real question', detail: 'Translate a broad request into something the available data can actually answer.' },
      { time: '11:30', title: 'Clean before modelling', detail: 'Find missing values, broken definitions and bias before testing an analysis or model.' },
      { time: '16:20', title: 'Explain the limits', detail: 'Turn results into a clear chart and tell decision-makers what the evidence cannot prove.' },
    ],
    workplaceReality: 'A large share of the job is cleaning and validating data, and a technically good model can still be unusable or misunderstood.',
  },
  'cybersecurity-analyst': {
    setting: 'This follows a monitoring and incident-response role; governance, testing and consulting can be more planned.',
    beats: [
      { time: '08:30', title: 'Triage the signals', detail: 'Review overnight alerts and separate routine noise from activity that needs investigation.' },
      { time: '12:15', title: 'Contain and strengthen', detail: 'Trace suspicious behaviour, close a weakness or help staff respond safely to phishing.' },
      { time: '17:10', title: 'Leave a clean handover', detail: 'Document evidence, actions and remaining risk for the next analyst or on-call rota.' },
    ],
    workplaceReality: 'Most alerts are routine until one is not; genuine incidents create high pressure and can pull work into nights or weekends.',
  },
  'it-support-specialist': {
    setting: 'This follows a helpdesk role; field service and infrastructure support involve more travel or specialist work.',
    beats: [
      { time: '08:30', title: 'Sort the queue', detail: 'Prioritise access, device and network problems by who is blocked and what is at risk.' },
      { time: '12:00', title: 'Fix or escalate', detail: 'Troubleshoot with a user, set up equipment and pass specialist issues on with useful evidence.' },
      { time: '16:30', title: 'Close the loop', detail: 'Document the solution, update the user and prepare devices or accounts for tomorrow.' },
    ],
    workplaceReality: 'The same faults recur, users may be frustrated, and some workplaces require shifts or out-of-hours cover.',
  },
  physiotherapist: {
    setting: 'This follows a clinical caseload; hospital, community, sports and private practice differ.',
    beats: [
      { time: '08:30', title: 'Review the caseload', detail: 'Read clinical notes and decide what each patient needs assessed before treatment starts.' },
      { time: '11:45', title: 'Movement is the evidence', detail: 'Test strength and mobility, deliver hands-on treatment and coach exercises safely.' },
      { time: '16:30', title: 'Measure what changed', detail: 'Record progress, adapt plans and coordinate with the wider care or sports team.' },
    ],
    workplaceReality: 'The work is physically tiring and progress can be slow; motivating someone through pain or setbacks takes patience.',
  },
  dentist: {
    setting: 'This follows general dental practice; hospital and specialist dentistry have different case mixes.',
    beats: [
      { time: '08:30', title: 'Prepare for precision', detail: 'Review charts and X-rays, check the surgery and plan the morning’s treatments.' },
      { time: '12:15', title: 'Treat the person too', detail: 'Examine, numb and restore teeth while explaining each step to an anxious patient.' },
      { time: '17:00', title: 'Close every loop', detail: 'Complete records, review follow-up needs and ensure instruments and the surgery are ready.' },
    ],
    workplaceReality: 'Close-up clinical work demands sustained concentration, and pain, anxiety or an unexpected complication can change the schedule.',
  },
  'healthcare-assistant': {
    setting: 'This follows a hospital or residential day shift; home care and other settings differ.',
    beats: [
      { time: '07:30', title: 'Start with dignity', detail: 'Take handover, help patients wash and dress, and notice who is less well than yesterday.' },
      { time: '12:00', title: 'Meals, movement and checks', detail: 'Support eating and mobility, record observations and report changes promptly.' },
      { time: '19:00', title: 'Hand over what matters', detail: 'Settle patients, update records and brief the next team on concerns.' },
    ],
    workplaceReality: 'Personal care is intimate and physically demanding; shifts can include nights, weekends, illness, dementia and bereavement.',
  },
  'social-worker': {
    setting: 'This follows a safeguarding caseload; hospital, disability, mental-health and community teams differ.',
    beats: [
      { time: '08:45', title: 'Triage risk and need', detail: 'Review referrals and decide which family, child or adult needs contact first.' },
      { time: '12:00', title: 'See beyond the file', detail: 'Visit a home or meet other professionals to understand safety, support and conflicting accounts.' },
      { time: '17:00', title: 'Write the defensible record', detail: 'Document evidence, agree actions and escalate when a person cannot be kept safe.' },
    ],
    workplaceReality: 'Heavy caseloads, court or safeguarding decisions and exposure to crisis make the emotional load substantial.',
  },
  'youth-community-worker': {
    setting: 'This follows a community project; school-based and residential services keep different hours.',
    beats: [
      { time: '11:00', title: 'Plan and connect', detail: 'Follow up referrals, prepare an activity and coordinate with schools or support services.' },
      { time: '15:30', title: 'The door opens', detail: 'Run a drop-in or one-to-one conversation when young people are actually available.' },
      { time: '20:15', title: 'Close and record', detail: 'Check everyone leaves safely, write notes and debrief any concern with the team.' },
    ],
    workplaceReality: 'Useful contact often happens after school and at weekends; emotional boundaries and short-term project funding affect the working life.',
  },
  journalist: {
    setting: 'This follows a general-news day; broadcast, sport, investigative and production roles differ.',
    beats: [
      { time: '08:30', title: 'Find the real lead', detail: 'Scan the news, pitch an angle and start checking which claims and sources stand up.' },
      { time: '12:45', title: 'Report, don’t assume', detail: 'Interview people, attend a court or council meeting, and verify details against documents.' },
      { time: '18:00', title: 'File, then update', detail: 'Write to deadline, respond to edits and keep watching a story that may still change.' },
    ],
    workplaceReality: 'Deadlines and unsocial hours are routine, while insecure roles and public criticism can add pressure beyond the reporting itself.',
  },
  'marketing-manager': {
    setting: 'This follows an in-house campaign team; agency and specialist roles vary.',
    beats: [
      { time: '09:00', title: 'Read the signal', detail: 'Check campaign results and decide what needs attention rather than chasing every metric.' },
      { time: '12:30', title: 'Coordinate the launch', detail: 'Brief creative, sales or agency partners and resolve gaps in message, budget or timing.' },
      { time: '17:30', title: 'Adjust in public', detail: 'Approve work, respond to late changes and revise the plan from live results.' },
    ],
    workplaceReality: 'You are accountable for visible targets while relying on many other people; launches and last-minute changes can extend the day.',
  },
  'financial-advisor': {
    setting: 'This follows a regulated client-advice role; employer, client base and pay model change the rhythm.',
    beats: [
      { time: '08:45', title: 'Prepare the whole picture', detail: 'Review a client’s goals, income, debts and existing cover before recommending anything.' },
      { time: '11:30', title: 'Make risk understandable', detail: 'Discuss pensions, protection or investments without hiding uncertainty or trade-offs.' },
      { time: '16:45', title: 'Evidence the advice', detail: 'Complete compliance records, applications and follow-ups so the recommendation can be defended.' },
    ],
    workplaceReality: 'Sales targets or commission can pull against impartial advice, while errors carry serious financial and regulatory consequences.',
  },
  'sports-scientist': {
    setting: 'This follows a performance setting; clinical exercise, research and participation roles differ.',
    beats: [
      { time: '07:30', title: 'Collect good evidence', detail: 'Run a fitness or movement test consistently so the results can be compared.' },
      { time: '12:00', title: 'Turn data into a plan', detail: 'Analyse training load or match footage and identify one useful change.' },
      { time: '17:30', title: 'Feed it back where it counts', detail: 'Explain findings to coaches and athletes, then observe how the plan works in training.' },
    ],
    workplaceReality: 'The calendar follows athletes and competition, so early starts, evenings, weekends and short contracts are common.',
  },
  chef: {
    setting: 'This follows a restaurant evening service; hotels, cafés, catering and institutional kitchens keep different hours.',
    beats: [
      { time: '10:30', title: 'Preparation decides service', detail: 'Check deliveries, prep ingredients and organise the station before orders arrive.' },
      { time: '17:30', title: 'Service begins', detail: 'Cook and plate several orders at once while keeping timing, consistency and food safety under control.' },
      { time: '22:45', title: 'Clean down and reset', detail: 'Store food safely, deep-clean the station and prepare the kitchen for the next shift.' },
    ],
    workplaceReality: 'Kitchens are hot, loud and physical; nights, weekends, burns, cuts and pressure during service are part of the bargain.',
  },
  'research-scientist': {
    setting: 'This follows laboratory research; field, computational and industrial research can look very different.',
    beats: [
      { time: '08:45', title: 'Set up carefully', detail: 'Prepare samples, controls and equipment so the experiment can be interpreted later.' },
      { time: '12:30', title: 'Run, record, question', detail: 'Collect data without quietly changing the method when results look inconvenient.' },
      { time: '17:20', title: 'Progress may mean failure', detail: 'Analyse results, troubleshoot and plan the next run or write up what the evidence supports.' },
    ],
    workplaceReality: 'Experiments fail often, progress can be slow and early research work may involve short contracts and uncertain timelines.',
  },
  'farmer-agri': {
    setting: 'This follows a livestock day; tillage, horticulture and agri-business roles follow different seasons and tasks.',
    beats: [
      { time: '06:00', title: 'First checks', detail: 'Inspect livestock, feed or milk, and respond quickly if an animal is unwell or calving.' },
      { time: '12:30', title: 'Land, machinery and records', detail: 'Move between fieldwork, repairs, supplies and the records required to run the farm.' },
      { time: '18:30', title: 'Second round', detail: 'Check animals and equipment again; seasonal work can continue well beyond the planned finish.' },
    ],
    workplaceReality: 'The work is physical and tied to weather, animals and seasons, with weekends and volatile income difficult to separate from daily life.',
  },
};

const ENTRY_ROUTE_COPY = /\b(?:CAO|Leaving Cert|entry points?|points? to get in|degree|college|university|PLC|apprenticeship|qualification|qualify|doctorate|PhD|years? of study|years? of exams?)\b/i;

export function isEntryRouteCopy(text: string): boolean {
  return ENTRY_ROUTE_COPY.test(text);
}

/** Keep the day screen's upside about doing the work, not getting into it. */
export function workplaceUpsideFor(career: CareerCard): string {
  return career.pros.find(item => !isEntryRouteCopy(item))
    ?? 'The role can become more rewarding as skill, judgement and responsibility grow.';
}

/**
 * The fallback is intentionally safe for a future career added before its
 * authored profile: it may be generic, but it cannot turn an entry barrier into
 * a timed workplace event.
 */
export function possibleDayFor(career: CareerCard): PossibleDayProfile {
  const authored = CAREER_DAY_PROFILES[career.id];
  if (authored) return authored;

  const task = (index: number) => career.whatYouDo[index] ?? career.whatYouDo[0] ?? 'Work on the role’s core responsibilities.';
  return {
    setting: 'This is one illustrative sequence; the setting and schedule vary by employer and specialism.',
    beats: [
      { time: '09:00', title: 'Begin with the priorities', detail: task(0) },
      { time: '12:30', title: 'The main work', detail: task(1) },
      { time: '16:30', title: 'Finish and hand over', detail: task(2) },
    ],
    workplaceReality: career.cons.find(item => !isEntryRouteCopy(item))
      ?? 'The pace, responsibility and working conditions vary substantially between workplaces.',
  };
}
