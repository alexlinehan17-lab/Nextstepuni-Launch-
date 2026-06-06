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
    "image": "career-icons/nurse.png",
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
  },
  {
    "id": "data-scientist",
    "title": "Data Scientist",
    "field": "tech",
    "emoji": "📊",
    "iconKey": "database",
    "tagline": "Find the story hidden in messy data.",
    "whatYouDo": [
      "Clean and wrangle messy data, then explore it for patterns",
      "Build and test models that predict or sort things (e.g. fraud, churn, demand)",
      "Turn the results into clear charts and plain-English advice for the business"
    ],
    "salary": {
      "startK": 42,
      "experiencedK": 75,
      "note": "Indeed.ie/Morgan McKinley; higher in Dublin big tech & finance"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (BSc Data Science / CS)",
        "detail": "4-yr degree like Maynooth Data Science (~425 pts), DCU or UCD Data Science & AI (~450-550 pts). Strong maths is a must. Most do a paid internship in 3rd year."
      },
      {
        "label": "CAO degree · Level 8 (Maths / Stats / Computing)",
        "detail": "Or do a broader Science/Computing/Maths degree (points vary widely, ~300+), then specialise. Many land here from physics or economics too."
      },
      {
        "label": "Conversion route · HCI/Springboard+ HDip or MSc",
        "detail": "Already have a degree? 1-yr Higher Diploma or MSc in Data Analytics (NCI, UCC, Maynooth), often 90-100% State-funded via Springboard+/HCI."
      }
    ],
    "skills": [
      "Maths and statistics",
      "Python or R coding",
      "SQL and databases",
      "Curiosity and problem-solving",
      "Explaining findings simply",
      "Patience with messy data"
    ],
    "pros": [
      "Well paid and in demand across tech, finance, pharma and health",
      "Mostly office or remote work, good conditions",
      "Genuinely interesting: every dataset is a new puzzle"
    ],
    "cons": [
      "Heavy on maths and coding; not a route if you dislike both",
      "A lot of the job is boring data cleaning, not flashy AI",
      "Tools change fast, so you never really stop learning"
    ],
    "matchStrings": [
      "Data Scientist",
      "Data Analyst",
      "Data Engineer",
      "AI Engineer",
      "AI Researcher",
      "Machine Learning Specialist",
      "Analytics Consultant"
    ],
    "sources": [
      "https://www.morganmckinley.com/ie/salary-guide/data/data-scientist/ireland",
      "https://ie.indeed.com/career/data-scientist/salaries",
      "https://gradireland.com/tech-sector-salaries-what-can-i-earn-it-graduate",
      "https://www.maynoothuniversity.ie/study-maynooth/undergraduate-studies/courses/bsc-data-science",
      "https://www.springboardcourses.ie/"
    ]
  },
  {
    "id": "cybersecurity-analyst",
    "title": "Cybersecurity Analyst",
    "field": "tech",
    "emoji": "🛡️",
    "iconKey": "shield",
    "tagline": "Hunt hackers, defend systems, always one step behind nobody.",
    "whatYouDo": [
      "Watch live alerts for break-ins and shut down threats fast",
      "Hunt for weak spots in apps, networks and laptops before hackers do",
      "Investigate dodgy logins, phishing emails and data leaks, then write it up"
    ],
    "salary": {
      "startK": 42,
      "experiencedK": 70,
      "note": "Higher in Dublin and big tech/finance firms; certs push it up"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (Cyber Security/Computing)",
        "detail": "4-yr honours degree, e.g. TU Dublin Digital Forensics & Cyber Security (TU863), ~300-550 pts in 2025; needs Maths O6/H7. Strong route into graduate cyber jobs."
      },
      {
        "label": "Tech apprenticeship · QQI Level 6 (earn while you learn)",
        "detail": "ICT Associate Cybersecurity Apprenticeship via FIT/ETBs: 2 yrs, paid, work for a real company while you study. Needs 5 Leaving Cert subjects incl. Ordinary-level Maths & English, age 18+."
      },
      {
        "label": "CAO degree · Level 8 (MTU/other unis)",
        "detail": "Other named options like MTU's IT Management & Cybersecurity (MT805) or general computing degrees you specialise in. Lower-points computing routes exist if cyber points are high."
      }
    ],
    "skills": [
      "Networks and how computers talk",
      "Logical problem-solving",
      "Attention to detail",
      "Thinking like a hacker",
      "Calm under pressure",
      "Clear writing and reporting"
    ],
    "pros": [
      "Huge demand in Ireland – jobs in tech, banks, hospitals, gov",
      "Pays well early and climbs fast with certs and experience",
      "Skills work anywhere in the world; often hybrid/remote"
    ],
    "cons": [
      "Real on-call and night shifts – attacks don’t wait for 9-to-5",
      "You must keep learning forever; threats change every month",
      "High stakes and stress when a breach actually happens"
    ],
    "matchStrings": [
      "Cybersecurity Analyst",
      "Cybersecurity Specialist"
    ],
    "sources": [
      "https://www.morganmckinley.com/ie/salary-guide/data/security-analyst/ireland",
      "https://ie.indeed.com/career/cybersecurity-analyst/salaries",
      "https://gradireland.com/careers-advice/job-descriptions/it-security-specialist",
      "https://www.tudublin.ie/study/undergraduate/courses/computing-dig-forensics-and-cyber-sec-tu863/",
      "https://fit.ie/course/fit-ict-associate-apprenticeship-cyber-security/"
    ]
  },
  {
    "id": "it-support-specialist",
    "title": "IT Support Specialist",
    "field": "tech",
    "emoji": "🖥️",
    "iconKey": "headset",
    "tagline": "Fixing tech all day so everyone else can work.",
    "whatYouDo": [
      "Take calls and tickets: reset passwords, fix laptops, printers, Wi-Fi",
      "Set up new staff PCs, accounts and phones; install software updates",
      "Track jobs in a helpdesk system and escalate the tricky ones"
    ],
    "salary": {
      "startK": 30,
      "experiencedK": 45,
      "note": "helpdesk/desktop level; specialise (cloud, networks, security) to earn more"
    },
    "routes": [
      {
        "label": "Apprenticeship · NFQ Level 6 (ICT Computer Networking Associate)",
        "detail": "2-yr FIT/SOLAS apprenticeship: get paid while you train, no degree needed. Entry: 5 O6/H7 incl Maths & English (Ordinary). Apply via fit.ie."
      },
      {
        "label": "CAO · Level 7/6 Computing",
        "detail": "Higher Cert/Ordinary degree in Computing or Computer Networks, ~150-280 pts (e.g. TUS, ATU, NCI). 2-3 yrs, then progress to a Level 8 if you want."
      },
      {
        "label": "Industry cert (fast route in)",
        "detail": "CompTIA A+ then Network+ shows employers you can do the job. Often done via a PLC/QQI course or self-study alongside your first helpdesk role."
      }
    ],
    "skills": [
      "Troubleshooting",
      "Patience with frustrated people",
      "Clear communication",
      "Computer hardware and networks",
      "Staying organised",
      "Quick learning"
    ],
    "pros": [
      "Tech jobs everywhere in Ireland; great first step into IT",
      "Get in without a degree via apprenticeship and earn while you learn",
      "Clear path up: specialise in cloud, networks or security for bigger pay"
    ],
    "cons": [
      "Repetitive: same password resets and 'have you tried restarting it?'",
      "Users get stressed and take it out on you; you stay calm",
      "Sometimes shift work, on-call or covering out-of-hours problems"
    ],
    "matchStrings": [
      "IT Support",
      "IT Support Specialist",
      "IT Consultant",
      "Network Technician",
      "Systems Analyst"
    ],
    "sources": [
      "https://www.morganmckinley.com/ie/salary-guide/data/helpdesk-support/ireland",
      "https://ie.indeed.com/career/it-support/salaries",
      "https://www.glassdoor.ie/Salaries/it-support-specialist-salary-SRCH_KO0,21.htm",
      "https://fit.ie/tech-apprenticeships/become-an-apprentice/",
      "https://www.qualifax.ie/course/104928"
    ]
  },
  {
    "id": "physiotherapist",
    "title": "Physiotherapist",
    "field": "health",
    "emoji": "🦵",
    "iconKey": "activity",
    "tagline": "Get people moving again after injury, surgery or illness.",
    "whatYouDo": [
      "Assess injuries and design exercise plans to rebuild strength and movement",
      "Hands-on treatment: massage, mobilisations, teaching patients how to recover safely",
      "Work across hospitals, sports clubs, ICU, stroke wards or private clinics"
    ],
    "salary": {
      "startK": 45,
      "experiencedK": 64,
      "note": "HSE staff-grade scale; Senior physio rises to ~€76k"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (BSc Physiotherapy)",
        "detail": "4-yr degree at UCD (DN420 ~579 pts), Trinity (TR053 ~577 pts), RCSI (RC004 ~566 pts) or UL. Points are very high. Then register with CORU before you can work."
      },
      {
        "label": "Professional Master's · Level 9",
        "detail": "If you already have a relevant science degree, a 2-yr MSc Physiotherapy (e.g. UL, RCSI) also leads to CORU registration."
      }
    ],
    "skills": [
      "Anatomy knowledge",
      "Hands-on treatment",
      "Motivating people",
      "Communication",
      "Problem-solving",
      "Patience"
    ],
    "pros": [
      "Genuinely change lives, helping people walk and move again",
      "Huge variety: sport, hospitals, kids, elderly, private practice",
      "In demand at home and abroad, with clear pay progression"
    ],
    "cons": [
      "CAO points are sky-high (550+), so it's hard to get in",
      "Physically tiring and you must register with CORU to practise",
      "Progress with patients can be slow and some never fully recover"
    ],
    "matchStrings": [
      "Physiotherapist",
      "Sports Physio",
      "Rehabilitation Specialist",
      "Musculoskeletal Specialist",
      "Sports Rehabilitation"
    ],
    "sources": [
      "https://www.forsa.ie/pay-scales/health-salary-scales/",
      "https://www2.cao.ie/points/l8.php",
      "https://coru.ie/health-and-social-care-professionals/education/approved-qualifications/physiotherapists/",
      "https://www.rcsi.com/dublin/undergraduate/physiotherapy/entry-requirements",
      "https://gradireland.com/courses/physiotherapy-23538"
    ]
  },
  {
    "id": "dentist",
    "title": "Dentist",
    "field": "health",
    "emoji": "🦷",
    "iconKey": "smile",
    "tagline": "Steady hands, fine detail, your own busy chair.",
    "whatYouDo": [
      "Check teeth and gums, take X-rays, fill cavities and pull teeth",
      "Numb, drill and treat nervous patients while keeping them calm",
      "Run a clinic: charts, infection control, and managing your day"
    ],
    "salary": {
      "startK": 65,
      "experiencedK": 100,
      "note": "New associates often ~€55-70k (sometimes a % of fees); experienced owners €100k+; HSE/specialist grades higher."
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (Dental Science / BDS)",
        "detail": "5-yr degree at TCD, UCC or RCSI. Very high points (~610-625, often random selection at the top). Then register with the Dental Council of Ireland before you can work."
      }
    ],
    "skills": [
      "Steady hands",
      "Fine attention to detail",
      "Putting nervous people at ease",
      "Science (biology, chemistry)",
      "Communication",
      "Running a small business"
    ],
    "pros": [
      "Strong, secure pay from early in your career",
      "Hands-on, skilled work where you see results that day",
      "Good hours: mostly weekdays, few nights or call-outs"
    ],
    "cons": [
      "Entry points are brutal (~625) and often a lottery even at max",
      "Fiddly, close-up work on anxious or in-pain patients all day",
      "Long 5-year degree, then big costs to set up your own practice"
    ],
    "matchStrings": [
      "Dentist",
      "Oral Surgeon",
      "Orthodontist",
      "Dental Researcher"
    ],
    "sources": [
      "https://dentistryjobs.ie/how-much-do-entry-level-dentists-make-in-ireland/",
      "https://dentistryjobs.ie/how-much-do-dentists-make-in-ireland/",
      "https://healthservice.hse.ie/staff/pay/pay-scales/",
      "https://www.dentalcouncil.ie/registration/irish-graduates",
      "https://www.tcd.ie/courses/undergraduate/courses/dental-science/"
    ]
  },
  {
    "id": "healthcare-assistant",
    "title": "Healthcare Assistant",
    "field": "health",
    "emoji": "🧑‍⚕️",
    "iconKey": "heart-pulse",
    "tagline": "Hands-on caring work you can start without a degree.",
    "whatYouDo": [
      "Wash, dress, feed and toilet patients who can't manage alone",
      "Help people move, take vitals, change beds, restock supplies",
      "Spot when someone's gone downhill and tell the nurse fast"
    ],
    "salary": {
      "startK": 30,
      "experiencedK": 42,
      "note": "HSE public scale starts higher (~€37k); nursing homes/agencies pay less but night & weekend shifts add on top"
    },
    "routes": [
      {
        "label": "QQI Level 5 · Healthcare Support (PLC / FET)",
        "detail": "No CAO points needed. One-year course at an ETB college (e.g. DFEi, Galway CC) or free FET/Skillnet course. Do 8 modules + 300 hrs placement, then you can work in hospitals, nursing homes, home care or disability services."
      },
      {
        "label": "Get hired, train on the job",
        "detail": "Some private nursing homes and agencies hire with a Leaving Cert and good English/maths, then pay for your QQI Level 5 while you work. Ask about funded training before you sign."
      },
      {
        "label": "Stepping-stone to Nursing (CAO Level 8)",
        "detail": "Lots of HCAs go on to a BSc in Nursing (~340-440 pts) later. Your HCA experience and references genuinely help your application and your first placements."
      }
    ],
    "skills": [
      "Personal care",
      "Kindness and patience",
      "Communication",
      "Teamwork",
      "Lifting and stamina",
      "Staying calm under pressure"
    ],
    "pros": [
      "Quick way in: a one-year course, no high points or degree",
      "Huge demand everywhere; easy to find work at home or abroad",
      "Real first-hand step toward nursing or other health careers"
    ],
    "cons": [
      "Hard physical work: lifting, on your feet, nights and weekends",
      "Private homes and agencies often pay less than the HSE",
      "Emotionally tough: illness, dementia, death and short staffing"
    ],
    "matchStrings": [
      "Healthcare Assistant",
      "Home Care Worker",
      "Disability Support Worker",
      "Disability Support",
      "Disability Services"
    ],
    "sources": [
      "https://www.hse.ie/eng/staff/resources/hr-circulars/august-1st-2025-pay-scales.pdf",
      "https://careerhub.hse.ie/pathways_hca/",
      "https://ie.indeed.com/career/healthcare-assistant/salaries",
      "https://www.dfei.ie/community-healthcare-and-nursing/healthcare-assistant",
      "https://www.lhpskillnet.ie/courses/chs"
    ]
  },
  {
    "id": "social-worker",
    "title": "Social Worker",
    "field": "psychology",
    "emoji": "🤝",
    "iconKey": "hands-helping",
    "tagline": "Helping families through their hardest moments.",
    "whatYouDo": [
      "Visit families, assess risk and protect children at risk of harm",
      "Write up case notes, attend case conferences and give evidence in court",
      "Link people to housing, mental health, addiction and disability supports"
    ],
    "salary": {
      "startK": 51,
      "experiencedK": 65,
      "note": "HSE/Tusla public scale; tops out near €73k after years"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (Social Work)",
        "detail": "4-yr professional degree, e.g. Trinity BSS (TR084, ~455 pts) or UCC BSW. Includes ~220 days placement. Garda vetting required. Then register with CORU to practise."
      },
      {
        "label": "Social science degree + Master's",
        "detail": "Do a Level 8 like Maynooth BSocSc (~348 pts) or UCD social science, then a CORU-approved Master in Social Work (2 yrs). Longer route, same end point."
      }
    ],
    "skills": [
      "Listening without judging",
      "Staying calm under pressure",
      "Clear writing and record-keeping",
      "Decision-making",
      "Empathy",
      "Boundaries and resilience"
    ],
    "pros": [
      "Steady, pensionable public job, always in demand",
      "You can change a child or family's whole future",
      "Real variety: child protection, mental health, disability, hospitals"
    ],
    "cons": [
      "Heavy caseloads and a lot of paperwork and court time",
      "Emotionally draining: abuse, neglect, crisis after crisis",
      "You can be blamed when things go wrong, even unfairly"
    ],
    "matchStrings": [
      "Social Worker",
      "Social Care Worker",
      "Family Support Worker",
      "Community Support Worker"
    ],
    "sources": [
      "https://www.forsa.ie/pay-scales/health-salary-scales/",
      "https://healthservice.hse.ie/staff/pay/pay-scales/",
      "https://coru.ie/health-and-social-care-professionals/education/approved-qualifications/social-workers/",
      "https://www.tcd.ie/swsp/undergraduate/social-studies/",
      "https://www.tusla.ie/uploads/content/PQSW-_Job_Spec.pdf"
    ]
  },
  {
    "id": "youth-community-worker",
    "title": "Youth & Community Worker",
    "field": "education",
    "emoji": "🤝",
    "iconKey": "users",
    "tagline": "Walk beside young people the system often forgets.",
    "whatYouDo": [
      "Run clubs, drop-ins and programmes for 10-25 year-olds",
      "Support teens through tough stuff: school, family, addiction, exclusion",
      "Plan trips and projects, write reports, chase funding and referrals"
    ],
    "salary": {
      "startK": 38,
      "experiencedK": 45,
      "note": "Youth Work Ireland / ETB scales (benchmarked to social-care grades); senior coordinators reach low 50s"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (UCC, Youth & Community Work)",
        "detail": "BSocSc (CK114), 3 yrs, ~317+ pts BUT you also need ~1 yr youth/community experience (paid or voluntary) and pass an interview. A recognised professional youth-work qualification."
      },
      {
        "label": "CAO degree · Level 8 (Maynooth, MH116)",
        "detail": "BSocSc Community & Youth Work, 3 yrs. Restricted course: NOT points-based. You apply by 1 Feb, write a statement, then do a group + individual interview. Garda vetting required."
      },
      {
        "label": "Start volunteering / PLC first",
        "detail": "No experience yet? Volunteer with a local youth project or do a QQI Level 5/6 social/community course, then apply to the degree with that experience behind you."
      }
    ],
    "skills": [
      "Building trust with teens",
      "Listening without judging",
      "Patience",
      "Group facilitation",
      "Boundaries and safeguarding",
      "Report writing"
    ],
    "pros": [
      "You're the steady adult a struggling young person can rely on",
      "Real variety: clubs, streetwork, projects, trips, one-to-ones",
      "Hands-on degree with paid/voluntary placements built in"
    ],
    "cons": [
      "Pay is modest and rises slowly; sector relies on grant funding",
      "Evenings, weekends and short-term contracts are common",
      "Emotionally heavy: you carry kids' problems home with you"
    ],
    "matchStrings": [
      "Youth Worker",
      "Community Worker",
      "Community Development Worker"
    ],
    "sources": [
      "https://www.ucc.ie/en/ck114/",
      "https://www.maynoothuniversity.ie/study-maynooth/find-course/community-and-youth-work",
      "https://gradireland.com/careers-advice/job-descriptions/youth-worker",
      "https://www.payscale.com/research/IE/Job=Youth_Worker/Salary",
      "https://ie.indeed.com/career/youth-worker/salaries"
    ]
  },
  {
    "id": "journalist",
    "title": "Journalist",
    "field": "creative",
    "emoji": "📰",
    "iconKey": "newspaper",
    "tagline": "Chase the story, hit the deadline, no matter what.",
    "whatYouDo": [
      "Chase leads, interview people, dig out the real story",
      "Write and file articles fast, often to a same-day deadline",
      "Cover courts, councils, sport or news live from the scene"
    ],
    "salary": {
      "startK": 25,
      "experiencedK": 45,
      "note": "Entry pay is low; freelance rates frozen for years"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (BA Journalism, DCU DC132)",
        "detail": "3-yr degree, ~409 pts, needs H4 English. Includes 8-week newsroom placement. Build a portfolio of published work as you go."
      },
      {
        "label": "CAO degree · Level 8 (Arts/Journalism, UL LM039 or Galway)",
        "detail": "~381 pts. A general Arts or media degree works too – editors care more about clips and contacts than the exact course."
      },
      {
        "label": "Start small + NUJ",
        "detail": "Write for local papers, radio or online, pitch as a freelancer, join the National Union of Journalists. Many break in this way, no single 'official' route."
      }
    ],
    "skills": [
      "Clear, fast writing",
      "Asking good questions",
      "Curiosity",
      "Working to deadline",
      "Fact-checking",
      "Building contacts"
    ],
    "pros": [
      "Front-row seat to news, courts, sport and big stories",
      "Your name and your work out in public",
      "Skills travel: print, radio, TV, online, PR, abroad"
    ],
    "cons": [
      "Entry pay is low and freelance rates have been frozen for years",
      "Insecure: papers are shrinking and staff jobs are scarce",
      "Pressure, unsocial hours and tight deadlines are constant"
    ],
    "matchStrings": [
      "Journalist",
      "Writer",
      "Broadcaster",
      "Content Creator",
      "Digital Content Creator",
      "Communications Officer"
    ],
    "sources": [
      "https://www.dcu.ie/courses/undergraduate/school-communications/journalism",
      "https://www.payscale.com/research/IE/Job=Journalist/Salary",
      "https://ie.indeed.com/career/journalist/salaries",
      "https://dublinfreelance.org/",
      "https://www2.cao.ie/points/l8.php"
    ]
  },
  {
    "id": "marketing-manager",
    "title": "Marketing Manager",
    "field": "business",
    "emoji": "📣",
    "iconKey": "megaphone",
    "tagline": "Sell the story, hit the numbers, chase the trends.",
    "whatYouDo": [
      "Plan campaigns: social posts, ads, emails, events and launches",
      "Track what's working in the numbers and tweak the plan",
      "Pitch ideas to the boss and brief designers, agencies and sales"
    ],
    "salary": {
      "startK": 30,
      "experiencedK": 65,
      "note": "Start as a marketing exec (~€28-32k); manager pay higher in Dublin/big firms"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (BSc Marketing)",
        "detail": "4-yr degree like TU Dublin Marketing (TU922, ~380-495 pts) or DCU Marketing, Innovation & Tech (DC240, ~487 pts). Start as a marketing exec, work up to manager."
      },
      {
        "label": "PLC / QQI Level 5 → CAO",
        "detail": "1-yr Level 5 Marketing/Business course (no points needed straight from the Leaving Cert), then use it to get a CAO degree place at DCU, TU Dublin and others."
      },
      {
        "label": "Professional body · while working",
        "detail": "Once in a job, build up with the Marketing Institute of Ireland or CIM (UK) diplomas. Employers value real campaign experience as much as letters."
      }
    ],
    "skills": [
      "Creativity",
      "Writing and copy",
      "Reading data",
      "Social media",
      "Communication",
      "Organisation"
    ],
    "pros": [
      "Creative and varied: no two campaigns are the same",
      "Skills work in any industry, anywhere in the world",
      "Clear ladder: exec to manager to head of marketing"
    ],
    "cons": [
      "You're judged on results: sales, clicks and targets",
      "Deadlines, late launches and last-minute changes",
      "Junior pay is modest; takes years to reach manager money"
    ],
    "matchStrings": [
      "Marketing Manager",
      "Marketing Executive",
      "Social Media Manager",
      "PR Manager",
      "PR Specialist",
      "Content Strategist"
    ],
    "sources": [
      "https://www.morganmckinley.com/ie/salary-guide/data/marketing-manager/ireland",
      "https://ie.indeed.com/career/marketing-manager/salaries",
      "https://www.glassdoor.ie/Salaries/marketing-graduate-salary-SRCH_KO0,18.htm",
      "https://www.tudublin.ie/study/undergraduate/courses/marketing-tu922/",
      "https://www.dcu.ie/courses/undergraduate/business-school/marketing-innovation-and-technology"
    ]
  },
  {
    "id": "financial-advisor",
    "title": "Financial Advisor",
    "field": "business",
    "emoji": "💶",
    "iconKey": "coins",
    "tagline": "Help people grow, protect and plan their money.",
    "whatYouDo": [
      "Meet clients, work out their goals, debts and what they can save",
      "Recommend pensions, life cover, mortgages and investments to suit them",
      "Write up advice, do the paperwork, and review plans as life changes"
    ],
    "salary": {
      "startK": 30,
      "experiencedK": 50,
      "note": "Base pay; commission/bonus on top. Wealth roles in Dublin pay more"
    },
    "routes": [
      {
        "label": "Pro exams · QFA (Qualified Financial Adviser)",
        "detail": "NFQ Level 7 via the IOB (a recognised college of UCD) or LIA (awarded by ATU). Entry: 5 Leaving Cert passes incl. English + Maths. 6 modules, ~1 year, often studied while working a trainee/bank job. The legal must-have to advise."
      },
      {
        "label": "CAO degree · Business/Finance (Level 7/8)",
        "detail": "e.g. Business, Accounting & Finance at TU Dublin, DCU, UCC, MTU. Points range widely (~250-510+). Then add the QFA exams on the job."
      }
    ],
    "skills": [
      "Good with numbers",
      "Listening and explaining clearly",
      "Building trust",
      "Sales and persuasion",
      "Organisation and paperwork",
      "Honesty under pressure"
    ],
    "pros": [
      "You can start from the Leaving Cert and qualify while you earn",
      "Real money for ambitious people: commission rewards results",
      "Steady demand - everyone needs pensions, mortgages and cover"
    ],
    "cons": [
      "Pay can lean on commission - quiet months hit your wages",
      "Targets and sales pressure can feel relentless",
      "Strict rules and exams: get advice wrong and it's serious"
    ],
    "matchStrings": [
      "Financial Advisor",
      "Risk Analyst",
      "Risk Manager",
      "Insurance Underwriter",
      "Fund Manager",
      "Finance Manager"
    ],
    "sources": [
      "https://gradireland.com/careers-advice/job-descriptions/financial-adviser",
      "https://ie.indeed.com/career/financial-advisor/salaries",
      "https://www.morganmckinley.com/ie/salary-guide/data/financial-advisor/ireland",
      "https://iob.ie/programme/financial-advice-qfa",
      "https://www.lia.ie/courses/certificate-in-professional-financial-advice"
    ]
  },
  {
    "id": "sports-scientist",
    "title": "Sports Scientist",
    "field": "science",
    "emoji": "🏃",
    "iconKey": "dumbbell",
    "tagline": "Turn science into faster, fitter, fewer-injured athletes.",
    "whatYouDo": [
      "Test athletes' fitness, strength and movement in a lab or gym",
      "Build training and recovery plans from the data you collect",
      "Film and analyse games, then feed findings back to coaches"
    ],
    "salary": {
      "startK": 28,
      "experiencedK": 45,
      "note": "Entry pay is low (~€25-30k); only a few elite GAA/IRFU/pro roles pay more"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (BSc Sport & Exercise Science)",
        "detail": "4-yr honours degree. UL (LM089, ~498 pts) and DCU Sport Science & Health (DC202, ~510+ pts) are the big names; need O4/H6 Maths + a lab science. Higher-points courses."
      },
      {
        "label": "CAO degree · lower-points route (Level 7/8)",
        "detail": "MTU, SETU, TU Dublin and ATU run Sport & Exercise Science degrees with lower points than UL/DCU — same field, often a Level 7 you can top up to Level 8."
      },
      {
        "label": "Postgrad to specialise",
        "detail": "Most applied roles (strength & conditioning, physiology, performance analysis) want a Level 9 master's on top. Sport Ireland Institute and pro teams expect this."
      }
    ],
    "skills": [
      "Exercise physiology",
      "Data analysis",
      "Strength & conditioning",
      "Communicating with coaches",
      "Attention to detail",
      "Practical lab skills"
    ],
    "pros": [
      "You work in elite sport — GAA, rugby, soccer, the Olympics",
      "Mix of lab, gym, pitch and screen — not a desk all day",
      "Science with a visible result: real athletes getting better"
    ],
    "cons": [
      "Starting pay is low and the top jobs are few and hard to get",
      "Evening, weekend and match-day hours follow the sport's calendar",
      "Many roles are short contracts — a postgrad is often needed to progress"
    ],
    "matchStrings": [
      "Sports Scientist",
      "Sports Science Degree (via progression)",
      "Performance Analyst",
      "Strength Coach",
      "Sports Coordinator",
      "Fitness Instructor",
      "Fitness Consultant"
    ],
    "sources": [
      "https://careersportal.ie/careers/detail.php?job_id=560",
      "https://gradireland.com/careers-advice/hospitality-and-event-management/sport-leisure-and-entertainment",
      "https://www.ul.ie/courses/bachelor-science-sport-and-exercise-sciences",
      "https://www.dcu.ie/courses/undergraduate/school-health-and-human-performance/sport-science-and-health",
      "https://www.sportireland.ie/institute/performance-service/strength-and-conditioning"
    ]
  },
  {
    "id": "chef",
    "title": "Chef",
    "field": "trades",
    "emoji": "👨‍🍳",
    "iconKey": "chef",
    "tagline": "Fast, hot, hands-on — you feed a full room every night.",
    "whatYouDo": [
      "Prep ingredients, then cook dishes to order on a hot, busy line",
      "Plate food fast and consistent during the dinner rush ('service')",
      "Keep your station clean, stocked and food-safe to HACCP standards"
    ],
    "salary": {
      "startK": 29,
      "experiencedK": 48,
      "note": "Commis ~€29-31k; chef de partie ~€38k; head/exec chefs €60k+"
    },
    "routes": [
      {
        "label": "Commis Chef Apprenticeship · QQI Level 6",
        "detail": "Get a job in a SOLAS-approved kitchen, then earn while you learn. 2 years, 3 days in the kitchen + 2 in college. Entry: a Pass Leaving Cert (NFQ Level 4). Can progress to the Chef de Partie apprenticeship (Level 7)."
      },
      {
        "label": "PLC / QQI Level 5-6 Culinary Arts",
        "detail": "1-2 year full-time course at a College of FET (e.g. Cork, Crumlin, Kerry). No points needed — Leaving Cert pass. Hands-on training plus work placement; a route into a kitchen job or on to the CAO."
      },
      {
        "label": "CAO degree · Level 8 Culinary Arts (TU942, TU Dublin)",
        "detail": "4-yr honours degree, ~210+ points. Also Level 7/6 options at MTU, ATU, TUS, DkIT from ~130-220 pts. More theory, management and food science — good if you want to run kitchens later."
      }
    ],
    "skills": [
      "Knife skills & cooking technique",
      "Working fast under pressure",
      "Time management & multitasking",
      "Food safety / hygiene (HACCP)",
      "Teamwork on the line",
      "Stamina and standing all day"
    ],
    "pros": [
      "Real skill in your hands — you can get work anywhere in the world",
      "No big points or college fees needed: earn while you learn",
      "Creative and satisfying — you make something people enjoy every day"
    ],
    "cons": [
      "Long, unsocial hours: nights, weekends, Christmas and bank holidays",
      "Hot, loud, high-pressure kitchens — burns, cuts and sore feet are normal",
      "Starting pay is modest; the big money only comes near the top"
    ],
    "matchStrings": [
      "Chef",
      "Head Chef",
      "Restaurant Manager",
      "Restaurant Owner"
    ],
    "sources": [
      "https://www.excelrecruitment.com/wp-content/uploads/2024/11/Hotel-Catering-Salary-Guide-2025.pdf",
      "https://commischefapprenticeship.ie/become-an-apprentice/",
      "https://ie.indeed.com/career/chef/salaries",
      "https://www.tudublin.ie/study/undergraduate/courses/culinary-arts--tu942/",
      "https://www.jobted.ie/salary/commis-chef"
    ]
  },
  {
    "id": "research-scientist",
    "title": "Research Scientist",
    "field": "science",
    "emoji": "🔬",
    "iconKey": "microscope",
    "tagline": "Curiosity as a job: question, test, repeat.",
    "whatYouDo": [
      "Run experiments in the lab, record data and analyse results",
      "Read papers, design studies and write up what you find",
      "Troubleshoot when results don't make sense and try again"
    ],
    "salary": {
      "startK": 35,
      "experiencedK": 60,
      "note": "Graduate entry ~€34-41k; €53k average; postdoc/PhD pushes it higher"
    },
    "routes": [
      {
        "label": "CAO degree · Level 8 (BSc Science)",
        "detail": "4-yr honours science degree (UCD, UCC, Galway, Trinity, DCU). Points vary a lot: ~300 at some colleges up to 540+ for UCD general science. Pick a stream like biology, chemistry, physics or biomed."
      },
      {
        "label": "PhD · 4 yrs (for true research roles)",
        "detail": "Most research scientist jobs need a PhD after your degree. You're paid a stipend (~€25k tax-free) while you research and publish. Get a 2:1 honours degree to qualify."
      },
      {
        "label": "Industry route · pharma/biotech",
        "detail": "With just a Level 8 you can start as a lab/research analyst in Irish pharma (Pfizer, Lilly, MSD). Some employers fund a part-time MSc or PhD later."
      }
    ],
    "skills": [
      "Lab technique",
      "Data analysis",
      "Patience and curiosity",
      "Problem-solving",
      "Scientific writing",
      "Attention to detail"
    ],
    "pros": [
      "Ireland is full of pharma/biotech and university research jobs",
      "You get paid to figure out how things actually work",
      "Skills travel: you can research anywhere in the world"
    ],
    "cons": [
      "Most real research roles need a PhD: that's 8+ years of study",
      "Early pay is modest and a lot of work is short contracts",
      "Experiments fail constantly: progress can feel painfully slow"
    ],
    "matchStrings": [
      "Research Scientist",
      "Researcher",
      "Biotech Researcher",
      "Lab Analyst",
      "Lab Manager",
      "Food Scientist",
      "Environmental Scientist",
      "Clinical Researcher",
      "Biomedical Scientist"
    ],
    "sources": [
      "https://ie.indeed.com/career/research-scientist/salaries",
      "https://www.payscale.com/research/IE/Job=Research_Scientist/Salary",
      "https://fdii.ie/2025/07/10/iua-salary-scales-what-irish-university-researchers-can-expect-in-2025-2026/",
      "https://www.iua.ie/for-researchers/researcher-salary-scales-career-framework/",
      "https://www2.cao.ie/points/l8.php"
    ]
  },
  {
    "id": "farmer-agri",
    "title": "Farmer / Agri-Business",
    "field": "animals",
    "emoji": "🐄",
    "iconKey": "tractor",
    "tagline": "Up at dawn, animals first, no two days same.",
    "whatYouDo": [
      "Feed, milk, herd and check livestock, plus calving and lambing",
      "Drive tractors, fence, spread slurry and fix whatever breaks",
      "Watch animal health, keep records and meet EU/Bord Bia rules"
    ],
    "salary": {
      "startK": 28,
      "experiencedK": 45,
      "note": "Employed farm/dairy assistants ~€33-35k; your own farm income swings hugely by year and type"
    },
    "routes": [
      {
        "label": "Teagasc Green Cert · Level 5/6 (QQI)",
        "detail": "Certificate in Agriculture at a Teagasc college (Kildalton, Gurteen, Clonakilty, Ballyhaise). Open to Leaving Cert leavers, often no points barrier; the 'Green Cert' you need to farm in your own name and claim grants/schemes."
      },
      {
        "label": "CAO degree · Level 8 (BAgrSc / Animal Science)",
        "detail": "UCD Agricultural Science (~430-455 pts, 2025) or Animal & Crop Production. WIT/SETU and ATU also run Level 7/8 ag courses with lower points. Leads to advisory, agribusiness and breeding roles."
      },
      {
        "label": "Start working + Part-Time Green Cert",
        "detail": "Get hired as a farm/dairy assistant straight from school, learn on the job, then do the part-time or distance Green Cert (open at 23+) to qualify formally."
      }
    ],
    "skills": [
      "Animal handling and care",
      "Hard physical graft",
      "Machinery and practical fixing",
      "Watching herd health",
      "Record-keeping and rules",
      "Being your own boss"
    ],
    "pros": [
      "Outdoors with animals, not stuck at a desk",
      "Real demand: dairy and tillage farms always need hands",
      "Clear path to running your own land one day"
    ],
    "cons": [
      "Long, early, physical days including weekends and calving season",
      "Income is volatile, weather, prices and EU payments swing it",
      "Hard, sometimes lonely, with real injury risk around animals and machinery"
    ],
    "matchStrings": [
      "Farm Manager",
      "Agricultural Advisor",
      "Agri-Business Manager",
      "Agricultural Consultant"
    ],
    "sources": [
      "https://teagasc.ie/education/courses/green-cert/",
      "https://ie.indeed.com/career/farm-worker/salaries",
      "https://www.rte.ie/news/business/2025/0623/1519861-average-farm-income-up-87-to-just-under-36-000/",
      "https://www.ucd.ie/courses/bagrsc-agricultural-science",
      "https://www.farmersjournal.ie/dairy/news/agri-jobs-dairy-farm-assistant-34-000-salary-870734"
    ]
  }
];
