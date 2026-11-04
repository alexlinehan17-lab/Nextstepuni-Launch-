/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// The in-app reader and public pages use the same versioned copy.
// School arrangements and company details confirmed by the owner on 4 October 2026.
// This publication does not represent solicitor certification of the documents.
import { PRIVACY_POLICY_VERSION, TERMS_VERSION, LEGAL_LAST_UPDATED } from '../../functions/src/legalAgreementPolicy';
export { PRIVACY_POLICY_VERSION, TERMS_VERSION, LEGAL_LAST_UPDATED };
export const SUPPORT_EMAIL = 'nextstepuniinfo@gmail.com';
export const COMPANY_NAME = 'NextStepUni Limited';
export const COMPANY_NUMBER = '818010';
export const COMPANY_ADDRESS = '75 Grange Park Road, Ireland';

export type LegalDoc = 'privacy' | 'terms';

export interface Section { heading: string; body: string[] }

/**
 * Bare https:// URLs written into the copy above, so both renderers can turn
 * them into real links. Google Play's Misleading Claims policy asks for
 * "clear and accessible URL/link(s)" to the original government sources — a URL
 * printed as plain text is neither. Global + sticky is deliberate: callers use
 * it with split()/exec(), so it must be reset (lastIndex = 0) before each pass
 * or shared state leaks between calls.
 */
export const LEGAL_URL_RE = /(https?:\/\/[^\s,)]+)/g;

export const LEGAL_TITLES: Record<LegalDoc, string> = {
  privacy: 'Privacy Notice',
  terms: 'Terms of Use',
};

export const PRIVACY_NOTICE: Section[] = [
  {
    heading: 'About this notice',
    body: [
      'This notice explains how NextStepUni handles personal information when students and authorised school staff use the Learning Lab, how the school programme works, and how to exercise your rights. It also covers enquiries and feedback sent directly to us.',
      `Published ${LEGAL_LAST_UPDATED}. Privacy Notice version ${PRIVACY_POLICY_VERSION}. Reading this notice is different from consenting to the use of your information.`,
    ],
  },
  {
    heading: 'Who looks after your information',
    body: [
      `NextStepUni is operated by ${COMPANY_NAME}, an Irish company registered under number ${COMPANY_NUMBER}. Our contact address is ${COMPANY_ADDRESS}. Contact our privacy team at ${SUPPORT_EMAIL}.`,
      'For your school-managed learning programme, your participating school is the data controller: it decides why your programme information is used. NextStepUni processes that information on its instructions under a data-processing agreement. Your school is shown in your account; its guidance counsellor or school office can provide its full identity, privacy notice and data-protection contact. You can also ask us to put you in touch.',
      'NextStepUni is a controller for information used to manage enquiries, respond to product feedback, administer its own service relationships and protect or establish its legal rights. We explain those purposes and legal bases below. We do not treat school learning records as information we may use freely for our own purposes.',
      'PwC Ireland sponsors the programme. Sponsorship does not give PwC access to student accounts, individual study records or identifiable student information. Any programme reporting shared with a sponsor must be anonymised so individuals cannot reasonably be identified.',
    ],
  },
  {
    heading: 'What we collect',
    body: [
      '• Account information: name, email address, chosen avatar, school, year group, account role and account creation/sign-in information. Firebase handles passwords; we do not store readable passwords in our application database. If you choose Google or Apple sign-in, we receive the account information needed to sign you in, such as your name, email and provider identifier.',
      '• Agreement records: the Privacy Notice and Terms versions you reviewed, an explicit agreement record, its server-recorded time and, for students, confirmation that you are aged 16 or over. We do not request your date of birth.',
      '• Study information: subjects, levels, target grades, exam dates, rest days, goals, module answers and progress, sessions, reflections, practice and spaced-repetition records, mock results, confidence/mastery, points, achievements, island items and display settings.',
      '• School support and peer information: kudos and gifts sent or received, notifications, and school-created support flags or cohort tags. Your school is responsible for the accuracy, necessity and lawful use of support information it adds.',
      '• Programme measurement, when enabled for an approved school programme: structured app/feature events, completed activities, broad practice accuracy and study-time bands, and an optional 1-to-5 confidence response. These use a separate random identifier linked to the account in a server-only mapping. Raw events do not contain your name, email, written answers, reflections or exact study duration. They are pseudonymous personal data, not anonymous data.',
      '• Onboarding diagnostics: setup steps, time, platform and a random per-visit identifier used to understand where setup fails. These records do not include your name, email or school and are not deliberately linked to your account.',
      '• Product feedback: the message, category, optional page context, platform and app version you submit. We do not automatically attach your name, email, school or account ID to the feedback message. Information you type may nevertheless identify you. A separate one-way account marker and daily count limit spam.',
      '• Technical and security information: IP addresses, browser/device information, authentication and security logs, and integrity/attestation information processed by the infrastructure and security services needed to operate the app. This differs from advertising tracking.',
    ],
  },
  {
    heading: 'Where information comes from',
    body: [
      'Most information comes from you or your use of the app. Your school supplies or confirms programme membership, staff access and support information. Google or Apple provides sign-in information if you choose that provider. Our hosting and security providers process technical information from requests and devices.',
      'Your account identity, participating school and a valid sign-in are needed for a school account. Without them, we cannot provide a private school workspace. Study choices and progress are needed for the features you use. Reflections, product feedback, peer interactions and confidence responses are optional; you can leave optional free-text fields blank.',
      'Your school decides whether participation forms part of its educational programme and explains any school requirements separately. We do not make optional feedback or sensitive disclosures a condition of using the app.',
    ],
  },
  {
    heading: 'Why we use information & our legal bases',
    body: [
      '• School programme delivery: providing relevant learning material, saving your work and progress, enabling authorised school support, and running approved peer features. The school identifies and documents the lawful basis. For the participating school programme, this is the public educational task under GDPR Article 6(1)(e), supported by the school’s applicable statutory education and guidance functions. Your school’s notice explains the specific legal provisions and any additional purposes.',
      '• School programme evaluation: where approved by the school, first-party measurement assesses participation and use of learning features. We act on the school’s documented instructions and use restricted, pseudonymous events and reports that suppress small groups. Measurement is not permission for advertising, individual disciplinary scoring or unrelated commercial profiling.',
      '• Enquiries, product feedback and service administration: where NextStepUni acts as controller, Article 6(1)(f) supports our legitimate interests in answering questions, fixing problems, managing school relationships and improving service quality using the minimum necessary information. Those interests must be balanced against your rights, with particular care for under-18s. You can object to this processing.',
      '• Security and legal requirements: security processing for the school follows its instructions and lawful basis. For our own security, abuse prevention and legal claims, we rely on necessary and proportionate legitimate interests under Article 6(1)(f). Where a specific legal obligation requires processing, we rely on Article 6(1)(c).',
      'The school programme is intended for students aged 16 or over. We ask students to confirm eligibility rather than collect a date of birth. Being 16 does not remove other protections for children under 18. Article 8 parental authorisation applies to relevant online processing based on consent for children under 16; it is not the legal basis for this school’s public-task processing. Acknowledging this notice or agreeing to the Terms does not give blanket data-processing consent.',
      'If a future optional feature needs consent, we will explain the particular purpose and obtain the appropriate separate consent before that processing starts. You may withdraw that consent as easily as you gave it, without affecting earlier lawful processing.',
    ],
  },
  {
    heading: 'Sensitive information & safeguarding',
    body: [
      'Please keep reflections and feedback focused on learning. Do not include medical details, religion, ethnicity, sexuality, other particularly sensitive information, or someone else’s private information unless your school has expressly arranged an appropriate, lawful process for it.',
      'School-created support records and accidental free-text disclosures can contain sensitive information. Before intentionally collecting or using special-category information, the school must identify both an Article 6 basis and a valid Article 9 condition, apply suitable safeguards and explain the purpose. There is no blanket education exemption created by accepting these documents.',
      `If unnecessary sensitive information is entered, contact your school or ${SUPPORT_EMAIL} so we can help restrict or remove it on the appropriate instructions. We do not repurpose it for advertising or infer health conditions from your learning activity.`,
      'NextStepUni is a study service, not an emergency or safeguarding reporting channel. Where information must be handled to protect someone or comply with law, the responsible organisation must use the applicable lawful basis and share only what is necessary with appropriate recipients.',
    ],
  },
  {
    heading: 'Who can see your information',
    body: [
      '• You can access your account and study information.',
      '• Authorised guidance counsellors and teaching staff at your school can access student account/progress information through the school dashboard to support the programme. They are not limited to seeing aggregate statistics. Your school manages staff authorisation and appropriate use.',
      '• Classmates at your school can see the limited peer-island view: first name, avatar, school, chosen goal category, island decorations/score and peer interactions. Private reflections, study sessions, mock grades, private answers, points balance and purchases are not included in that public projection.',
      '• Authorised NextStepUni personnel may access information where necessary for support, administration, security, rights requests or service operations, subject to confidentiality and access controls. Administrators can read submitted product feedback, including personal details you choose to include.',
      '• Programme measurement dashboards show totals and percentages by school, year group and period, with small-group suppression. Raw events and the identity mapping are server-only and are not displayed in that dashboard.',
      '• We may disclose information where required by law or necessary for a properly assessed safeguarding issue, legal claim or security incident. We assess the lawful basis, recipient and minimum information needed. No sponsor receives account access or identifiable student records.',
    ],
  },
  {
    heading: 'Service providers & international transfers',
    body: [
      'Google Firebase/Google Cloud provides authentication, hosting, databases, server functions and related security services. App Check may use Google reCAPTCHA Enterprise on web and Apple App Attest or Google Play Integrity on native devices. Google or Apple also handles your chosen social sign-in.',
      'Star Crew avatar artwork is served with the app. Legacy or purchased DiceBear avatars may be fetched from api.dicebear.com using an avatar seed. Although we do not intentionally send account identity with that seed, an external image request exposes ordinary network information such as an IP address and browser headers. Google Fonts requests similarly involve network information. These providers are not advertising partners.',
      'The application’s Firestore database is configured in London, United Kingdom. The UK is outside the EEA. Firebase Authentication processes information in the United States; other Google services and operational support may process information in additional countries. A database region does not mean every service stays in that region.',
      'Applicable international transfers use recognised protections under GDPR Chapter V: a current European Commission adequacy decision where its conditions are met, and/or the applicable contractual safeguards in the provider’s data-processing terms, including Standard Contractual Clauses where needed. Google describes its EU–US Data Privacy Framework participation and contractual terms here: https://firebase.google.com/support/privacy',
      `You can ask ${SUPPORT_EMAIL} for information about the safeguards applicable to your programme and how to obtain a copy. We do not sell personal information or share it for advertising.`,
    ],
  },
  {
    heading: 'Cookies, storage & recommendations',
    body: [
      'The app uses browser or device storage for sign-in, settings, local drafts and offline learning assets. Web authentication uses session persistence; native apps can retain sign-in in their app sandbox. External sign-in or security providers may use necessary storage under their own terms. We do not use advertising cookies, Google Analytics, cross-site behavioural tracking, session replay or advertising identifiers.',
      'The app uses your chosen subjects, dates and learning activity to suggest study work, revision timing and relevant content. These recommendations and confidence/mastery indicators support learning; they do not determine school admission, official grades, grant eligibility or disciplinary outcomes. We do not make decisions with legal or similarly significant effects on you solely by automated processing.',
      'We do not send your typed answers, reflections or feedback to an artificial-intelligence service. School staff remain responsible for educational and support decisions.',
    ],
  },
  {
    heading: 'How long we keep information',
    body: [
      'School account and study records are retained while needed for your participation and any school-authorised support period. The school determines that period under its programme agreement and retention obligations, considering the programme duration, support needs and any applicable recordkeeping duty. We delete or return programme information when instructed at the end of the service, subject to any specific legal requirement to retain it. Ask your school or us for the retention instructions applying to your account.',
      'Agreement records are kept with the account to show which published versions were acknowledged and agreed to. Account deletion removes the linked agreement records and programme measurement events. A limited rights-request or security audit record may remain where necessary for accountability or a legal claim; it is restricted and is not retained for unrelated use.',
      'Product feedback expires after 365 days; its separate spam marker expires after 48 hours. Raw programme-measurement events expire after 400 days and their rate-limit records after 48 hours. These expiry rules use scheduled infrastructure deletion, which can take a short additional processing period after expiry.',
      'Onboarding diagnostic records are retained only while needed to assess setup and resolve programme onboarding issues. Your school’s instructions and the purpose of the record determine the review/deletion point; they are not retained for advertising.',
      'Provider security logs and backups have separate limited operational retention. Deletion from live systems is followed by expiry from backups under the applicable provider process; deleted information is not brought back into ordinary use. Firebase describes its authentication, security-log and backup deletion periods at https://firebase.google.com/support/privacy',
      'Where information must be kept for a specific legal obligation or dispute, we limit it to that purpose and remove it when the obligation or justified need ends. Truly anonymised statistics may be retained because they no longer identify individuals.',
    ],
  },
  {
    heading: 'Your rights & how to use them',
    body: [
      'You can request access, correction, erasure, restriction and, where applicable, objection or a portable copy of your information. These rights depend on the circumstances and lawful basis: for example, statutory portability generally applies to automated processing based on consent or a contract, rather than a school’s public task. Where we rely on consent, you can withdraw it at any time.',
      'In Settings → Delete Account, you can download your data or request account deletion after verifying your sign-in. That route is optional; you can also contact us or your school. Deleting the app from your device does not delete your account. We help the school handle requests for information it controls.',
      `Email ${SUPPORT_EMAIL} or contact your school’s data-protection contact or guidance counsellor. We may ask for proportionate information to verify identity or authority. Requests are normally free. We respond without undue delay and ordinarily within one month; if the law permits an extension for complexity or multiple requests, we explain it within that first month. If a right cannot be fulfilled, we explain the relevant reason and complaint route.`,
      'Children have their own data-protection rights. A parent or guardian’s authority to exercise them is assessed in context, taking account of the student’s rights, wishes, capacity and applicable law; it is not automatic access to every record.',
      'You can complain to the Irish Data Protection Commission at https://www.dataprotection.ie/en/contact/how-contact-us or to the competent supervisory authority where you live, work or believe an infringement occurred. You do not have to contact us first.',
    ],
  },
  {
    heading: 'Changes & contact',
    body: [
      'We publish the version and date of this notice and make earlier published versions available. We highlight material changes in the app before a new purpose starts. A privacy acknowledgement records that information was provided; it does not replace any consent required by law.',
      `Privacy questions: ${SUPPORT_EMAIL}. Postal contact: ${COMPANY_NAME}, ${COMPANY_ADDRESS}. Company registration number: ${COMPANY_NUMBER}.`,
    ],
  },
];

export const TERMS_OF_USE: Section[] = [
  {
    heading: 'About these terms',
    body: [
      `NextStepUni is operated by ${COMPANY_NAME}, registered in Ireland under company number ${COMPANY_NUMBER}, with a contact address at ${COMPANY_ADDRESS}. Contact us at ${SUPPORT_EMAIL}.`,
      `These Terms govern your permitted use of the Learning Lab. Version ${TERMS_VERSION}, published ${LEGAL_LAST_UPDATED}. We ask you to review them and actively agree before using an account. You can open, save or print them at any time at https://www.nextstepuni.com/terms.html`,
      'The Privacy Notice explains personal-data handling separately. Agreeing to these Terms is not blanket consent to data processing and does not waive your privacy or consumer rights.',
    ],
  },
  {
    heading: 'School access & eligibility',
    body: [
      'Student accounts are for participants aged 16 or over whose school has arranged programme access. Authorised school staff may use staff accounts. Your school confirms programme eligibility and manages its own educational arrangements; you must not misrepresent your age or use another person’s join code or account.',
      'If you are 16 or 17, you remain a child for data-protection purposes. Any provision that requires contractual capacity or adult authorisation applies only to the extent permitted by Irish law. Your use under a school programme does not make you responsible for the school’s commercial obligations or make a parent a contracting party automatically.',
      'The school’s service and data-processing agreements govern its arrangements with NextStepUni. These user rules do not amend those agreements or bind your school or parent on your behalf. Where adult authorisation is required for a particular arrangement, it must be obtained separately.',
      'Student access through the school programme is not a paid subscription bought by the student. Any future paid offer or materially different service will have its price, duration and applicable terms clearly explained before you choose it.',
    ],
  },
  {
    heading: 'Your account & security',
    body: [
      '• Provide accurate account information and keep sign-in credentials secure. Students must use their own personal account; staff must use only the account authorised by their school for their role.',
      '• Use only access codes provided for you or your authorised school role. Do not share student accounts, disclose staff credentials outside their authorised role, or try to obtain another user’s private information.',
      `• Tell your school or ${SUPPORT_EMAIL} promptly if you think your account has been compromised. We will help investigate and secure it.`,
      'You are responsible for your own use and reasonable care of your sign-in details. You are not automatically responsible for activity caused by a security failure outside your control. We retain our own responsibilities for the service’s security and compliance.',
    ],
  },
  {
    heading: 'Respectful & permitted use',
    body: [
      'Use the app for learning and authorised school support. Peer features are for supporting classmates. Your school’s authorised staff can see relevant student account/progress and peer activity as explained in the Privacy Notice.',
      '• Do not bully, harass, impersonate, threaten or discriminate against others, or submit unlawful or inappropriate content.',
      '• Do not upload another person’s private information, infringe intellectual-property rights, introduce malicious code, defeat security controls, scrape private records or disrupt the service.',
      '• Do not falsify activity, exploit rewards or use automated accounts to manipulate programme reporting or peer features.',
      `Report misuse to your school or ${SUPPORT_EMAIL}. We may apply the proportionate suspension process below.`,
    ],
  },
  {
    heading: 'Learning content & your work',
    body: [
      'We grant you a personal, non-exclusive permission to use the app and available learning content for your own study, or for authorised staff support within your school programme, while access is available. Built-in download, export and printing features may be used for those purposes, subject to any stated third-party conditions.',
      'NextStepUni and its licensors retain their rights in the app, designs and learning materials. Do not sell, redistribute, publish or commercially exploit them, or copy substantial parts beyond the permitted study features or rights allowed by law. Third-party and official material remains owned by its respective rights holders.',
      'You retain your rights in original work, answers and reflections you create. You give us only the permission needed to store, display, back up, export and otherwise handle that work to provide the programme and features you choose, consistently with the Privacy Notice and the school’s instructions. This does not give us ownership of your work or permission to use private reflections for advertising or AI training.',
      'You must have the right to submit any material you provide. We may remove unlawful content or material that infringes another person’s rights, using the fair review process below.',
    ],
  },
  {
    heading: 'Where our content comes from',
    body: [
      'NextStepUni is an independent study app. It is not affiliated with, endorsed by, or acting on behalf of the State Examinations Commission, the Department of Education, the CAO, SUSI, the Higher Education Authority, or any other government body or public agency.',
      'Some learning material draws on official publications. Source references accompany exam material; State Examinations Commission material remains © State Examinations Commission, and other quoted works remain the property of their respective owners. Access through NextStepUni does not grant a right to redistribute third-party material.',
      'Official deadlines, fees, grants and entry requirements can change. Check the relevant authority before making an application or relying on an entitlement:',
      '• State Examinations Commission: https://www.examinations.ie',
      '• CAO: https://www.cao.ie',
      '• SUSI: https://www.susi.ie',
      '• Higher Education Authority: https://hea.ie',
      '• Qualifax: https://www.qualifax.ie',
      '• Citizens Information: https://www.citizensinformation.ie',
      '• Irish government information: https://www.gov.ie',
    ],
  },
  {
    heading: 'What the service can promise',
    body: [
      'We aim to provide a useful, reliable study service and exercise reasonable care and skill in operating it. The app is maintained and updated; maintenance, security work, outages and changes to official material can affect availability. We give reasonable notice of planned material disruption where practicable.',
      'Learning recommendations, practice feedback and self-marking are study aids, not official assessment. We do not guarantee a particular exam grade, college place, grant, career outcome or uninterrupted availability. Use your teachers and the relevant official sources for decisions that require authoritative advice.',
      'Nothing in these Terms excludes applicable statutory standards, remedies or consumer rights. Where the service does not meet a legal obligation, the rights and remedies provided by law remain available.',
    ],
  },
  {
    heading: 'Responsibility & liability',
    body: [
      'We are responsible, subject to applicable law, for reasonably foreseeable loss caused by our breach of these Terms or failure to exercise reasonable care and skill. Loss is reasonably foreseeable if it was an obvious consequence or reasonably contemplated when the relevant arrangement was made.',
      'The student service is supplied for personal educational use. To the extent permitted by law, we are not responsible under these student Terms for business losses arising from using it commercially or for loss that was not reasonably foreseeable. Any separate school contract governs the school’s commercial relationship with us.',
      'We do not exclude or limit liability that cannot lawfully be excluded or limited, including liability for fraud, fraudulent misrepresentation, death or personal injury caused by negligence, or any applicable statutory consumer or data-protection right. These Terms do not impose an indemnity on students or require them to compensate us for another person’s actions.',
    ],
  },
  {
    heading: 'Suspension & ending access',
    body: [
      'You may stop using the service at any time. Settings → Delete Account lets you download your information or request account deletion; you may also contact us or your school. Deleting the app alone does not close an account.',
      'Your school may end programme access when your participation ends. We may restrict a feature or suspend access where reasonably necessary to address a material breach, misuse, a security issue or a risk to students. The response should be proportionate to the issue.',
      'We normally explain the reason, give reasonable notice and allow a chance to correct the issue. Immediate action may be necessary for a serious or urgent risk, legal requirement or where notice would compromise an investigation. We explain the decision as soon as reasonably possible unless law or a justified safeguarding/security need prevents this.',
      `You can ask for a review by emailing ${SUPPORT_EMAIL} and, where appropriate, involving your school. We will consider the explanation fairly and restore access where the grounds no longer justify restriction.`,
      'When access ends, we help arrange an appropriate opportunity to obtain your information where practicable. Access ending does not remove your data-protection rights; deletion and retention follow the Privacy Notice, school instructions and any applicable legal requirements.',
    ],
  },
  {
    heading: 'Changes to the service & these terms',
    body: [
      'We may make reasonable changes for security, legal compliance, accessibility, technical improvements or programme needs. We do not use this clause to remove rights already required by law or impose unexpected charges.',
      'We publish the effective date and version of changes and highlight material changes in the app with reasonable advance notice where practicable. An urgent legal or security change may take effect sooner, with an explanation as soon as reasonably possible. Material changes to these Terms require a new explicit agreement before continued account use; we do not treat a date update alone as acceptance.',
      'Earlier published versions remain available. If you do not agree to a material change, you may stop using the service, download your information or request account deletion, subject to lawful retention requirements. Any additional rights to keep an unmodified service or end an arrangement under applicable law remain unaffected.',
    ],
  },
  {
    heading: 'Irish law, complaints & contact',
    body: [
      'Irish law governs these Terms. Where mandatory protections under the law of your usual place of residence apply, you keep those protections. You may bring proceedings in any court that applicable law permits; these Terms do not force a consumer to use an otherwise impermissible exclusive forum.',
      `Contact ${SUPPORT_EMAIL} with a complaint, the issue and the outcome you seek. We aim to acknowledge complaints promptly, investigate fairly and explain our response. School programme matters may also be raised with your school. This process does not restrict access to courts, regulators or other remedies available by law.`,
      'If a provision cannot lawfully be enforced, it applies only to the extent permitted; the remaining provisions continue so far as the arrangement can reasonably operate. A delay in exercising a right does not by itself waive it. Nothing here overrides a statutory right or the rights of a person who lacks capacity to be bound by a particular provision.',
      `${COMPANY_NAME} · Company number ${COMPANY_NUMBER} · ${COMPANY_ADDRESS} · ${SUPPORT_EMAIL}.`,
    ],
  },
];
