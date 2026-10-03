/** @license SPDX-License-Identifier: Apache-2.0
 * Official strand/core-element maps, reviewed 3 October 2026. These are study
 * picker groupings, not a transcription of every learning outcome or a claim
 * that the question corpus covers the specification. IDs are cohort-specific.
 */
import type { CanonicalCurriculumSpecification, CanonicalCurriculumGroup } from '../../curriculumRegistry';
import type { CurriculumCategory } from '../../curriculum';

const source = (url: string, title: string) => ({ authority: 'Curriculum Online' as const, url, title, role: 'content' as const });
function group(subject: string, key: string, title: string, topics: [string, string][]): CanonicalCurriculumGroup {
  return { id: `${subject}-2027-${key}`, title, topics: topics.map(([id, name]) => ({ id: `${subject}-2027-${id}`, title: name })) };
}
function specification(subjectId: string, subjectName: string, category: CurriculumCategory, pdf: string, groups: CanonicalCurriculumGroup[], pages: string): CanonicalCurriculumSpecification {
  return {
    id: `${subjectId}:2027`, subjectId, subjectName, category, programme: 'leaving-certificate-established',
    title: `${subjectName} specification (introduced 2025)`, firstExamYear: 2027,
    status: 'verified', levels: ['higher', 'ordinary'], coverageNodeLevel: 'group', recommendedClassHours: 180,
    sources: [source(pdf, `${subjectName} specification — strand structure and core elements (${pages})`),
      { authority: 'Curriculum Online', role: 'transition', title: `${subjectName}: introduction in September 2025`, url: `https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/${subjectId}/` }],
    groups, notes: ['Study groupings follow official strands and core elements. They are not an exhaustive learning-outcome checklist.', 'Check current prescribed texts, specified areas of learning and annual assessment briefs with the SEC. Historical questions keep their original paper year.'],
  };
}

const classical = (subject: 'latin' | 'ancient-greek', name: string, culture: string, pdf: string) => specification(subject, name, 'language', pdf, [
  group(subject, 'language', `${name} Language`, [
    ['understanding-texts', `Understanding ${name} texts`],
    ['language-analysis', 'Language awareness and analytical skills'],
  ]),
  group(subject, 'literature-context', 'Literature in Context', [
    ['literature', `${name} literature`], ['culture-texts', `${culture} culture through texts`],
  ]),
], 'pp. 10–18');

export const INTRODUCED_2025_SPECIFICATIONS: CanonicalCurriculumSpecification[] = [
  classical('latin', 'Latin', 'Roman', 'https://www.curriculumonline.ie/getmedia/79ddb17e-6160-4045-b159-40899260c230/SC-Latin-Spec-EN.pdf'),
  classical('ancient-greek', 'Ancient Greek', 'Hellenic', 'https://www.curriculumonline.ie/getmedia/beade839-3da7-4e3d-8b32-8333a4f80ba0/SC-Ancient-Greek-Spec-ENG.pdf'),
  specification('arabic', 'Arabic', 'language', 'https://www.curriculumonline.ie/getmedia/ca3539e8-068d-4dda-9734-bccb04eb5144/SC_Arabic_Curriculum_Specification_EN.pdf', [
    group('arabic', 'communication', 'Communicative Language Competence', [
      ['reception', 'Reception'], ['production', 'Production'], ['interaction', 'Interaction'], ['mediation', 'Mediation'],
    ]),
    group('arabic', 'languages-cultures', 'Plurilingual and Pluricultural Competence', [
      ['plurilingual', 'Plurilingual competence'], ['pluricultural', 'Pluricultural competence'],
    ]),
  ], 'pp. 12–20'),
  specification('climate-action-and-sustainable-development', 'Climate Action and Sustainable Development', 'social-environmental', 'https://www.curriculumonline.ie/getmedia/df1d6c85-f630-436f-9383-7503b64d6ed5/SC-Climate-Action-Sustainable-Dev-Spec-ENG.pdf', [
    group('climate-action-and-sustainable-development', 'earth', 'Earth Systems, Life, and Environment', [
      ['earth-systems', 'Earth systems and ecosystems'], ['climate-evidence', 'Climate science and evidence'],
      ['biodiversity', 'Biodiversity and environmental limits'], ['ecosystem-fieldwork', 'Nature, local ecosystems and fieldwork'],
    ]),
    group('climate-action-and-sustainable-development', 'people', 'People, Power, and Place', [
      ['power-rights', 'Power, place and human rights'], ['community', 'Community and place'],
      ['collective-action', 'Individual and collective action'], ['policy-transition', 'Environmental policy and just transitions'],
    ]),
    group('climate-action-and-sustainable-development', 'global', 'Global Connections', [
      ['globalisation', 'Globalisation and sustainability'], ['justice', 'Climate justice'], ['media', 'Media and communication'],
      ['solutions', 'Mitigation, adaptation and decarbonisation'], ['commitments', 'International commitments'],
    ]),
    group('climate-action-and-sustainable-development', 'applied', 'Applied Learning Tasks', [
      ['dialogue', 'Climate and sustainability dialogue'], ['research', 'Researching action'],
      ['nature-experience', 'Designing a nature-based experience'], ['organising', 'Organising action'],
    ]),
  ], 'pp. 11–25'),
  specification('drama-film-and-theatre-studies', 'Drama, Film and Theatre Studies', 'arts', 'https://www.curriculumonline.ie/getmedia/a25c493e-1ab5-443f-a14e-b47180d2e14d/LC-Drama-Film-and-Theatre-Studies-Spec_EN.pdf', [
    group('drama-film-and-theatre-studies', 'creative', 'Creative Process', [
      ['performance-foundations', 'Foundations of performance and production'], ['imagining', 'Imagining and conceptualising'],
      ['developing', 'Developing'], ['refining', 'Refining'], ['producing', 'Producing and performing'], ['evaluating', 'Evaluating'],
    ]),
    group('drama-film-and-theatre-studies', 'response', 'Critical Response Process', [
      ['response-foundations', 'Foundations of critical response'], ['appraising', 'Appraising and responding'],
      ['analysing', 'Analysing and interpreting'], ['response-evaluation', 'Refining and evaluating'],
    ]),
    group('drama-film-and-theatre-studies', 'applied', 'Applied Creative Tasks', [
      ['ensemble', 'Ensemble-driven theatre'], ['sequence', 'Film sequence'], ['theatre-film', 'Theatre piece or short film'],
    ]),
  ], 'pp. 13–30'),
];
