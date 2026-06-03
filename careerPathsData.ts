/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Career Paths" content — 12 careers, source-grounded Irish data authored +
 * adversarially fact-checked (salary bands cross-checked vs HSE/public pay
 * scales, gradireland, Morgan McKinley/Hays guides; routes vs CAO/SOLAS/QQI and
 * the professional bodies). Salaries are € thousands, typical (not outliers).
 * `matchStrings` map each career to the real `careerPaths` strings in
 * futureFinderData's CAO_COURSES, so "courses that lead here" and the Future
 * Finder "jump to your matches" are computed from real catalog data.
 * Generated 2026-06-03 from the verified content workflow.
 */

import { type CareerCard } from './types/careerPaths';

export const CAREERS: CareerCard[] = [
  {
    "id": "nurse",
    "title": "Nurse",
    "field": "health",
    "emoji": "👩‍⚕️",
    "tagline": "Hands-on, high-pressure, never the same day twice.",
    "whatYouDo": [
      "Give meds, dress wounds, monitor vitals and charts",
      "Comfort scared patients and update worried families",
      "Work 12-hour shifts on your feet, days and nights"
    ],
    "salary": {
      "startK": 37,
      "experiencedK": 54,
      "note": "HSE public scale; shift/weekend premiums add more"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (BSc Nursing)",
        "detail": "4-yr degree, ~340-440 pts (general/mental health/children's/disability/midwifery). Register with NMBI, then work."
      },
      {
        "label": "Pre-Nursing PLC (QQI L5) → degree",
        "detail": "1-yr PLC, then apply to the BSc via CAO/QQI links. Places limited, often by random selection."
      }
    ],
    "skills": [
      "Clinical care",
      "Staying calm",
      "Communication",
      "Teamwork",
      "Attention to detail",
      "Stamina"
    ],
    "pros": [
      "Always in demand, secure job at home or abroad",
      "You genuinely help people every shift",
      "Real variety: wards, ICU, community, theatre"
    ],
    "cons": [
      "Long shifts, nights, weekends and bank holidays",
      "Emotionally heavy: death, stress, short-staffing",
      "Pay climbs slowly up fixed public scale"
    ],
    "matchStrings": [
      "Registered Nurse",
      "Nurse (via degree progression)",
      "Clinical Nurse Specialist",
      "Nurse Manager",
      "Clinical Nurse Manager",
      "Public Health Nurse",
      "Nurse Educator",
      "Emergency Nurse",
      "Mental Health Nurse",
      "Psychiatric Nurse",
      "Community Nurse",
      "Midwife",
      "Midwife (via progression)"
    ],
    "sources": [
      "https://jobvacancies.ie/nursing-pay-scales-explained-ireland-2025/",
      "https://www.hse.ie/eng/staff/resources/hr-circulars/august-1st-2025-pay-scales.pdf",
      "https://www.frsrecruitment.com/irish-nursing-salary-trends-2025-what-nurses-need-to-know",
      "https://www.ucc.ie/en/ck710/",
      "https://www2.cao.ie/points/l8.php"
    ]
  },
  {
    "id": "veterinarian",
    "title": "Veterinarian",
    "field": "animals",
    "emoji": "🐾",
    "tagline": "Animal doctor: blood, mud, hard CAO points.",
    "whatYouDo": [
      "Examine sick pets and farm animals, then diagnose and treat",
      "Do surgery, vaccinations, stitches, scans and put-downs",
      "Visit farms in all weather; comfort stressed owners"
    ],
    "salary": {
      "startK": 42,
      "experiencedK": 65,
      "note": "Higher in specialist or referral practice"
    },
    "routes": [
      {
        "label": "CAO degree (MVB) · Level 8",
        "detail": "UCD Veterinary Medicine (DN300), ~590 pts, 5 yrs. Needs H5 Chemistry + 60 hrs animal experience."
      },
      {
        "label": "Veterinary Nursing · Level 8",
        "detail": "A separate job (assists the vet). UCD DN310 ~500 pts, 4 yrs; also at DkIT, TUS, ATU, MTU."
      },
      {
        "label": "PLC / QQI then CAO",
        "detail": "A QQI Level 5 animal-care course can win a competitive place on Vet Nursing if you miss points."
      }
    ],
    "skills": [
      "Animal handling",
      "Diagnosis",
      "Steady surgical hands",
      "Strong science (biology/chemistry)",
      "Calm under pressure",
      "Talking to upset owners"
    ],
    "pros": [
      "Hands-on, never the same day twice",
      "You genuinely save animals' lives",
      "Skills work anywhere in the world"
    ],
    "cons": [
      "Brutal points: only one vet degree in Ireland",
      "Early starts, night calls, weekend on-call",
      "Euthanasia and heartbroken owners are hard"
    ],
    "matchStrings": [
      "Veterinarian",
      "Animal Researcher",
      "Veterinary Nurse",
      "Animal Welfare Officer"
    ],
    "sources": [
      "https://www.agriland.ie/farming-news/graduate-vets-in-ireland-earn-up-to-e45000-report/",
      "https://gradireland.com/careers-advice/job-descriptions/veterinary-surgeonnurse",
      "https://ie.indeed.com/career/veterinarian/salaries",
      "https://www.qualifax.ie/course/2355",
      "https://www.cao.ie/index.php?page=points&p=latest"
    ]
  },
  {
    "id": "software-developer",
    "title": "Software Developer",
    "field": "tech",
    "emoji": "💻",
    "tagline": "Build apps and tools, paid well, lots of Googling",
    "whatYouDo": [
      "Write and fix code so apps and websites actually work",
      "Hunt down bugs and figure out why something broke",
      "Plan features with your team, then test before it ships"
    ],
    "salary": {
      "startK": 39,
      "experiencedK": 75,
      "note": "higher in Dublin and big tech firms"
    },
    "routes": [
      {
        "label": "CAO Computer Science degree (Level 8)",
        "detail": "4 yrs at TCD/UCD/UCC/UL/DCU/Maynooth/Uni of Galway/TUS, ~340-540 pts. Most common route in."
      },
      {
        "label": "Software Developer Associate Apprenticeship",
        "detail": "2 yrs, QQI Level 6, earn while you learn (~€314-408/week). Leaving Cert entry, no CAO points."
      },
      {
        "label": "PLC then degree",
        "detail": "1-2 yr computing PLC, then transfer onto a degree if points fall short."
      }
    ],
    "skills": [
      "Coding (Python/Java/etc.)",
      "Logical problem-solving",
      "Debugging",
      "Teamwork",
      "Learning new tools fast",
      "Attention to detail"
    ],
    "pros": [
      "Strong pay, even starting out",
      "Jobs everywhere, remote-friendly",
      "You build real things people use"
    ],
    "cons": [
      "Stuck on one bug for hours",
      "Must keep learning new tech forever",
      "Long screen time, stressful near deadlines"
    ],
    "matchStrings": [
      "Software Developer",
      "Software Engineer",
      "Web Developer",
      "Junior Developer",
      "Junior Software Developer",
      "Full-Stack Developer",
      "DevOps Engineer",
      "Machine Learning Engineer"
    ],
    "sources": [
      "https://gradireland.com/careers-advice/information-technology/tech-sector-salaries",
      "https://www.morganmckinley.com/ie/salary-guide/data/software-engineer/ireland",
      "https://apprenticeship.ie/career-seekers/get-started/learn-more/ict/Software-Developer-Associate-L6",
      "https://fit.ie/course/fit-ict-associate-apprenticeship-software-developer/",
      "https://www2.cao.ie/points/l8.php"
    ]
  },
  {
    "id": "engineer",
    "title": "Engineer",
    "field": "engineering",
    "emoji": "⚙️",
    "tagline": "Build the real world — bridges, machines, medical kit",
    "whatYouDo": [
      "Design and test things on a screen, then check they get built right",
      "Solve problems on site or in the lab when stuff fails or won't fit",
      "Run the numbers so a structure, circuit or machine is safe"
    ],
    "salary": {
      "startK": 38,
      "experiencedK": 72,
      "note": "Chartered status adds €6-10k; software pays more"
    },
    "routes": [
      {
        "label": "CAO common-entry degree · Level 8",
        "detail": "~360-570+ pts. 4 yrs, pick your branch after first year. Chartered status comes with experience later."
      },
      {
        "label": "Engineering apprenticeship",
        "detail": "Earn while you learn, 2-4 yrs, no CAO points. Can ladder up to a degree."
      },
      {
        "label": "PLC then CAO degree",
        "detail": "One-year course builds points/portfolio, then progress into a Level 8 engineering degree."
      }
    ],
    "skills": [
      "Maths and physics",
      "Problem solving",
      "CAD / design software",
      "Attention to detail",
      "Teamwork",
      "Clear communication"
    ],
    "pros": [
      "Build real things people use every day",
      "Strong pay and jobs in demand",
      "Tons of branches to pick from"
    ],
    "cons": [
      "Maths-heavy degree, real workload",
      "High points for top colleges",
      "Some site/shift work and deadline crunch"
    ],
    "matchStrings": [
      "Mechanical Engineer",
      "Civil Engineer",
      "Electrical Engineer",
      "Electronic Engineer",
      "Structural Engineer",
      "Biomedical Engineer",
      "Control Systems Engineer",
      "Renewable Energy Engineer"
    ],
    "sources": [
      "https://gradireland.com/careers-advice/engineering-graduate-salaries",
      "https://www.engineersireland.ie/News/graduate-engineers-earn-39000-a-year-reveals-engineers-ireland-salary-report-2026",
      "https://www.morganmckinley.com/ie/salary-guide/data/civil-engineer/ireland",
      "https://apprenticeship.ie/career-seekers/get-started/learn-more/engineering/manufacturing-engineering-l7",
      "https://www2.cao.ie/points/l8.php"
    ]
  },
  {
    "id": "solicitor-barrister",
    "title": "Solicitor / Barrister",
    "field": "law",
    "emoji": "⚖️",
    "tagline": "Years of exams before you ever earn big.",
    "whatYouDo": [
      "Read case files, draft contracts, advise clients on the law",
      "Prepare arguments and represent people in court (barristers)",
      "Long hours researching, writing letters and filing legal paperwork"
    ],
    "salary": {
      "startK": 40,
      "experiencedK": 95,
      "note": "Trainee/first-year pay is modest; barristers' devilling year is unpaid"
    },
    "routes": [
      {
        "label": "CAO Law degree (LLB/BCL) · Level 8",
        "detail": "~3-4 yrs, points roughly 440-580. Then 8 FE-1 exams, a 2-yr training contract and the Law Society PPC."
      },
      {
        "label": "Law degree to King's Inns (barrister)",
        "detail": "Do the 1-yr Barrister-at-Law degree, then a year 'devilling' (shadowing a senior barrister) for no pay."
      },
      {
        "label": "Any degree to FE-1 exams (solicitor)",
        "detail": "You don't need a law degree: pass the 8 FE-1 exams, then do a training contract and the PPC."
      }
    ],
    "skills": [
      "Clear writing",
      "Reading dense text",
      "Public speaking",
      "Attention to detail",
      "Logical argument",
      "Research"
    ],
    "pros": [
      "Respected, well-paid career once you're established",
      "Genuinely varied work and interesting cases",
      "Many paths: firms, courts, business, government"
    ],
    "cons": [
      "Years of exams and training before good pay",
      "Long hours, deadline and court pressure",
      "Barristers earn little for the first few years"
    ],
    "matchStrings": [
      "Solicitor",
      "Barrister",
      "Legal Advisor",
      "Legal Executive",
      "Corporate Lawyer"
    ],
    "sources": [
      "https://www.morganmckinley.com/ie/salary-guide/data/solicitor/ireland",
      "https://www.lawsociety.ie/becoming-a-solicitor/final-examination---first-part-fe-1/",
      "https://www.kingsinns.ie/courses/degree-of-barrister-at-law",
      "https://gradireland.com/careers-advice/law/entry-and-training-barristers-republic-ireland",
      "https://gradireland.com/careers-advice/job-descriptions/barrister"
    ]
  },
  {
    "id": "psychologist",
    "title": "Psychologist",
    "field": "psychology",
    "emoji": "🧠",
    "tagline": "Help people through their hardest stuff. Long road in.",
    "whatYouDo": [
      "Assess and talk with clients - anxiety, trauma, learning needs, behaviour",
      "Run therapy sessions, build treatment plans, then track progress",
      "Write reports, score tests, work with families, teachers or doctors"
    ],
    "salary": {
      "startK": 63,
      "experiencedK": 100,
      "note": "HSE staff-grade scale (62.6k-100.7k); senior grades go higher"
    },
    "routes": [
      {
        "label": "CAO Psychology degree (Level 8)",
        "detail": "PSI-accredited BA/BSc, 3-4 yrs, points roughly 350-590 (UCD/TCD/UCC/DCU/Maynooth/TUS/ATU)."
      },
      {
        "label": "Degree then doctorate",
        "detail": "Degree, then 1-3 yrs as assistant psychologist, then a 3-yr HSE-funded (paid) doctorate to practise. 7-10 yrs total."
      },
      {
        "label": "Conversion route",
        "detail": "Non-psych degree? A PSI-accredited conversion course gets you onto the same postgrad path."
      }
    ],
    "skills": [
      "Active listening",
      "Empathy",
      "Research and stats",
      "Report writing",
      "Patience",
      "Emotional resilience"
    ],
    "pros": [
      "Genuinely change people's lives",
      "Stable, well-paid public sector roles",
      "Variety - kids, adults, courts, schools"
    ],
    "cons": [
      "Long road and low pay in the early assistant years",
      "Doctorate places are fiercely competitive",
      "Emotionally heavy - burnout is real"
    ],
    "matchStrings": [
      "Psychologist",
      "Clinical Psychologist",
      "Counsellor",
      "Behavioural Scientist"
    ],
    "sources": [
      "https://www.hse.ie/eng/staff/resources/hr-circulars/august-1st-2025-pay-scales.pdf",
      "https://careerhub.hse.ie/pathways_trainee_psychologist/",
      "https://www.psychologicalsociety.ie/accredited-courses",
      "https://gradireland.com/careers-advice/job-descriptions/psychologist-clinical",
      "https://www2.cao.ie/points/l8.php"
    ]
  },
  {
    "id": "accountant",
    "title": "Accountant",
    "field": "business",
    "emoji": "📊",
    "tagline": "Track the money, then qualify into a serious salary.",
    "whatYouDo": [
      "Check the numbers add up: invoices, payroll, tax, monthly accounts",
      "Build reports that tell a business what's really going on",
      "Spot mistakes, fraud and waste before they cost money"
    ],
    "salary": {
      "startK": 33,
      "experiencedK": 75,
      "note": "Newly qualified ~€60-65k; controllers €80k+"
    },
    "routes": [
      {
        "label": "CAO degree (Level 8) + pro exams",
        "detail": "Commerce/Accounting/Finance, ~360-560 pts, 3-4 yrs. Then ACA/ACCA/CIMA exams while working."
      },
      {
        "label": "Accounting Technician Apprenticeship",
        "detail": "Level 6, 2 yrs, paid ~€26-28k while you learn. Can ladder up to full qualification after."
      },
      {
        "label": "PLC then CAO",
        "detail": "Business/Accounting PLC course, then transfer to a degree if your points fall short."
      }
    ],
    "skills": [
      "Number confidence",
      "Excel / spreadsheets",
      "Attention to detail",
      "Honesty / ethics",
      "Explaining numbers clearly",
      "Meeting deadlines"
    ],
    "pros": [
      "Pay jumps a lot once you qualify",
      "Every business needs one - very safe job",
      "Skills work anywhere in the world"
    ],
    "cons": [
      "Years of tough exams while working full-time",
      "Long hours at month-end and tax season",
      "Repetitive and desk-bound a lot of the time"
    ],
    "matchStrings": [
      "Accountant",
      "Financial Analyst",
      "Actuary",
      "Investment Banker",
      "Quantitative Analyst",
      "Accounting Technician"
    ],
    "sources": [
      "https://www.morganmckinley.com/ie/salary-guide/data/newly-qualified-accountant/ireland",
      "https://www.morganmckinley.com/ie/salary-guide/accounting-finance/permanent-salaries",
      "https://apprenticeship.ie/career-seekers/get-started/learn-more/finance/Accounting-Technician",
      "https://accountingtechniciansireland.ie/apprenticeship-roi/",
      "https://www.charteredaccountants.ie/News/notable-salary-increases-for-experienced-and-newly-qualified-chartered-accountants"
    ]
  },
  {
    "id": "teacher",
    "title": "Teacher",
    "field": "education",
    "emoji": "🍎",
    "tagline": "30 kids, one room, and you're in charge.",
    "whatYouDo": [
      "Plan and teach lessons, then mark piles of homework and tests",
      "Manage a class of teens or kids: behaviour, motivation, the lot",
      "Track each student's progress and update parents and the school"
    ],
    "salary": {
      "startK": 46,
      "experiencedK": 72,
      "note": "Fixed public pay scale; rises yearly + allowances, tops ~86k"
    },
    "routes": [
      {
        "label": "BEd degree · Level 8 (CAO)",
        "detail": "4-year primary teaching degree, e.g. DCU/MIC ~485 pts. You qualify straight out, no extra course."
      },
      {
        "label": "Subject degree + PME",
        "detail": "Any Arts/Science degree (~300-420 pts), then a 2-year PME masters (Level 9) to teach secondary."
      },
      {
        "label": "Teaching Council registration",
        "detail": "After either route you must register with the Teaching Council before you can be paid to teach."
      }
    ],
    "skills": [
      "Explaining clearly",
      "Patience",
      "Classroom control",
      "Planning ahead",
      "Subject knowledge",
      "Reading the room"
    ],
    "pros": [
      "Long summer and Christmas breaks",
      "Secure, pensionable public job",
      "You genuinely shape young people"
    ],
    "cons": [
      "Tons of unpaid prep and marking at home",
      "Pay climbs slowly up a fixed scale",
      "Hard to get permanent hours early on"
    ],
    "matchStrings": [
      "Teacher",
      "Secondary School Teacher",
      "Primary School Teacher",
      "PE Teacher",
      "Science Teacher",
      "Special Education Teacher",
      "Learning Support Teacher"
    ],
    "sources": [
      "https://www.asti.ie/your-employment/pay/salary-scales/post-2011-common-basic-scale/",
      "https://www.into.ie/help-advice/pay/pay-scales-and-incremental-progression/",
      "https://www.teachingcouncil.ie/how-to-become-a-teacher/post-primary/",
      "https://www.dcu.ie/courses/undergraduate/institute-education/bachelor-education-primary-teaching",
      "https://www.qualifax.ie/course/110197"
    ]
  },
  {
    "id": "architect",
    "title": "Architect",
    "field": "design",
    "emoji": "📐",
    "tagline": "Design buildings — but it's a long road first.",
    "whatYouDo": [
      "Sketch and 3D-model buildings, then refine designs on CAD software",
      "Meet clients and planners; visit sites in a hard hat",
      "Draw up detailed plans builders actually build from"
    ],
    "salary": {
      "startK": 35,
      "experiencedK": 65,
      "note": "Fully qualified RIAI architects earn more; €100k+ at the top"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8",
        "detail": "5-yr accredited degree (UCD ~556 pts; also UCC, TUD, ATU Sligo), then 2 yrs office experience."
      },
      {
        "label": "Then: RIAI Professional Practice Exam",
        "detail": "After the degree + 2 yrs work, pass this to legally call yourself an architect. 7-9 yrs total."
      },
      {
        "label": "Portfolio matters",
        "detail": "Some courses (e.g. TU Dublin) score a portfolio and interview, not just points."
      }
    ],
    "skills": [
      "Drawing & sketching",
      "CAD / 3D modelling",
      "Spatial thinking",
      "Maths & geometry",
      "Client communication",
      "Attention to detail"
    ],
    "pros": [
      "Creative — you literally shape how places look",
      "Skills travel: work anywhere in the world",
      "Real pride seeing your building get built"
    ],
    "cons": [
      "Long road: 7-9 years before you're 'an architect'",
      "High points and a portfolio to get in",
      "Long hours and deadline crunches in practice"
    ],
    "matchStrings": [
      "Architect",
      "Urban Planner"
    ],
    "sources": [
      "https://www.morganmckinley.com/ie/salary-guide/data/architect/ireland",
      "https://ie.indeed.com/career/architect/salaries",
      "https://www.riai.ie/careers-in-architecture/education/riai-professional-practice-examination",
      "https://www.riai.ie/careers-in-architecture/accredited-programmes",
      "https://www.ucd.ie/courses/barchsc-architecture"
    ]
  },
  {
    "id": "pharmacist",
    "title": "Pharmacist",
    "field": "science",
    "emoji": "💊",
    "tagline": "Medicine expert who keeps a whole town safe.",
    "whatYouDo": [
      "Check and dispense prescriptions, flagging dangerous drug clashes",
      "Advise patients on doses, side effects and minor illnesses",
      "Run vaccinations, blood-pressure checks and manage stock"
    ],
    "salary": {
      "startK": 48,
      "experiencedK": 72,
      "note": "community typical; hospital/HSE scales reach 90k+"
    },
    "routes": [
      {
        "label": "Integrated MPharm (CAO Level 8)",
        "detail": "5-yr degree with placement at UCC/RCSI/TCD, ~560-620 pts, then PSI registration to practise."
      },
      {
        "label": "Pharmaceutical Science degree",
        "detail": "Level 8 route into drug-making industry (R&D, QC), not dispensing; lower points."
      }
    ],
    "skills": [
      "Chemistry knowledge",
      "Attention to detail",
      "Patient communication",
      "Calm under pressure",
      "Mental maths",
      "Confidentiality"
    ],
    "pros": [
      "Stable, well-paid, always in demand",
      "You genuinely help people every day",
      "Respected, trusted health professional"
    ],
    "cons": [
      "Very high CAO points to get in",
      "Long days on your feet, weekend shifts",
      "One dispensing mistake can be serious"
    ],
    "matchStrings": [
      "Pharmacist",
      "Pharmaceutical Scientist",
      "Clinical Pharmacist",
      "Pharmaceutical Researcher"
    ],
    "sources": [
      "https://www.forsa.ie/pay-scales/health-salary-scales/",
      "https://ie.indeed.com/career/pharmacist/salaries",
      "https://www.rcsi.com/dublin/undergraduate/pharmacy/entry-requirements",
      "https://www.ucc.ie/en/ck703/",
      "https://www.tcd.ie/pharmacy/courses/undergraduate/pharmacy-integrated-programme/"
    ]
  },
  {
    "id": "electrician",
    "title": "Electrician",
    "field": "trades",
    "emoji": "🔌",
    "tagline": "Get paid to learn a trade you'll never be short of.",
    "whatYouDo": [
      "Wire houses, offices and factories — sockets, panels, lights, alarms",
      "Read drawings, run cable, test circuits, fix faults safely",
      "Lots of call-outs, site work and solar/EV charger installs now"
    ],
    "salary": {
      "startK": 50,
      "experiencedK": 70,
      "note": "Apprentices earn while training; overtime and self-employed pay more"
    },
    "routes": [
      {
        "label": "SOLAS Electrical Apprenticeship · Level 6",
        "detail": "~4 years, no CAO points. Earn while you learn with an employer plus ETB training. Same model as plumbing or carpentry."
      },
      {
        "label": "PLC / pre-apprenticeship course",
        "detail": "1-year QQI Level 5 to build skills and help land an employer, then start the apprenticeship."
      }
    ],
    "skills": [
      "Wiring and circuits",
      "Reading drawings",
      "Fault-finding",
      "Safety awareness",
      "Maths and measuring",
      "Steady hands"
    ],
    "pros": [
      "Earn from day one, no college debt",
      "Skill in huge demand — easy to get work",
      "Can go self-employed and set your rates"
    ],
    "cons": [
      "Early starts, cold sites, physical work",
      "Apprentice pay is low for the first years",
      "Risk of shocks — safety mistakes are serious"
    ],
    "matchStrings": [
      "Electrician",
      "Electrical Contractor",
      "Maintenance Technician"
    ],
    "sources": [
      "https://ie.indeed.com/career/electrician/salaries",
      "https://aeci.ie/wp-content/uploads/2025/09/HOURLY-RATES-Aug-2024-1.pdf",
      "https://www.qualifax.ie/course/220217",
      "https://apprenticeship.ie/news-events/news/off-the-job-training-payments-allowances-for-craft-apprentices",
      "https://www.citizensinformation.ie/en/education/further-education-and-training/apprenticeships/"
    ]
  },
  {
    "id": "graphic-designer",
    "title": "Graphic Designer",
    "field": "creative",
    "emoji": "🎨",
    "tagline": "Make brands look good — portfolio beats points.",
    "whatYouDo": [
      "Design logos, posters, social posts and packaging in Photoshop, Illustrator, InDesign",
      "Take a client brief, pitch ideas, then tweak it after feedback",
      "Pick fonts, colours and layouts so the message lands"
    ],
    "salary": {
      "startK": 30,
      "experiencedK": 58,
      "note": "Higher in Dublin agencies and tech; freelance varies a lot"
    },
    "routes": [
      {
        "label": "PLC Art/Design portfolio (L5) → CAO degree (L8)",
        "detail": "1 yr PLC builds your portfolio, then a 3-4 yr Level 8 (NCAD, IADT, TU Dublin)"
      },
      {
        "label": "Direct CAO degree (Level 8)",
        "detail": "NCAD/IADT score on portfolio, not points — just meet minimum subjects (2 H5 + 4 O6/H7)"
      },
      {
        "label": "Self-taught + portfolio",
        "detail": "Some break in via online courses and freelance; a strong portfolio is the real gate"
      }
    ],
    "skills": [
      "Adobe Creative Suite",
      "Typography",
      "Layout and colour",
      "Taking feedback",
      "Sketching ideas",
      "Meeting deadlines"
    ],
    "pros": [
      "Get paid to be creative every day",
      "Portfolio matters more than your points",
      "Skills work anywhere — freelance or agency"
    ],
    "cons": [
      "Starting pay is modest, climbs slowly",
      "Endless client edits and tight deadlines",
      "Competitive — lots of designers chasing jobs"
    ],
    "matchStrings": [
      "Graphic Designer",
      "Interior Designer"
    ],
    "sources": [
      "https://www.morganmckinley.com/ie/salary-guide/data/graphic-designer/ireland",
      "https://ie.indeed.com/career/graphic-designer/salaries",
      "https://www.payscale.com/research/IE/Job=Graphic_Designer/Salary",
      "https://www.ncad.ie/undergraduate/school-of-design/graphic-design/",
      "https://iadt.ie/courses/graphic-design/"
    ]
  }
];
