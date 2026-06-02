/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Catch-Up Lane content — absence-recovery micro-units.
 *
 * FIRST SLICE: Leaving Cert Biology (8 topics), tagged to real curriculum.ts
 * subtopic IDs. Authored from the LC Biology syllabus, source-grounded, the
 * same discipline as examRepsData.ts. Content scales subject-by-subject (the
 * way Exam Reps rolled out); these prove the format end to end.
 *
 * Content rule (per CLAUDE.md): no verbatim exam material; plain-language
 * paraphrase of syllabus content with the source named. Re-verify against the
 * current syllabus on the same cadence as examRepsData.ts.
 */

import { type RecoveryCard } from './types/catchUpLane';

export const RECOVERY_CARDS: RecoveryCard[] = [
  {
    id: 'bio-cell-structure',
    subjectId: 'biology', topicId: 'biology-1-0',
    subjectLabel: 'Biology', topicLabel: 'Cell Structure', level: 'common',
    gist: 'The cell is the basic unit of life. Animal and plant cells both have a cell membrane, cytoplasm, a nucleus, mitochondria and ribosomes. Plant cells have three extra structures: a cell wall (made of cellulose), a large permanent vacuole and chloroplasts.',
    oneMove: {
      label: 'Know what each organelle DOES, not just its name',
      text: 'Nucleus = controls the cell and holds the DNA · mitochondrion = releases energy (respiration) · chloroplast = photosynthesis · ribosome = makes protein · cell wall = support. The exam asks for the function, not just a label.',
    },
    check: {
      prompt: 'Name two structures found in a plant cell but not an animal cell, and give the function of one.',
      modelAnswer: 'Cell wall (made of cellulose) — gives the cell support and shape; and chloroplast — the site of photosynthesis. (A large permanent vacuole is also acceptable as the second structure.)',
      needed: ['Cell wall (cellulose)', 'Chloroplast (or large vacuole)', 'A correct function for one'],
    },
    source: 'LC Biology syllabus — Unit 2: The Cell',
    marksWeight: 9,
  },
  {
    id: 'bio-enzymes',
    subjectId: 'biology', topicId: 'biology-1-1',
    subjectLabel: 'Biology', topicLabel: 'Cell Metabolism', level: 'common',
    gist: 'Enzymes are biological catalysts — proteins that speed up reactions without being used up. Each enzyme is specific to its substrate (the lock-and-key idea). Activity rises with temperature up to an optimum, then falls sharply as the enzyme denatures. pH affects them in the same way.',
    oneMove: {
      label: "Say 'denatures', never 'dies'",
      text: "Above its optimum temperature the enzyme's shape changes permanently (it denatures), so the substrate no longer fits the active site and the reaction slows or stops. Enzymes aren't alive, so 'the enzyme dies' loses the mark.",
    },
    check: {
      prompt: "Explain what happens to an enzyme's activity above its optimum temperature, and why.",
      modelAnswer: "Activity falls sharply. The high temperature denatures the enzyme (changes its shape), so the active site no longer fits the substrate and the reaction slows or stops.",
      needed: ['Activity decreases / stops', 'Enzyme denatures (shape changes)', 'Active site no longer fits substrate'],
    },
    source: 'LC Biology syllabus — Unit 2: Cell Metabolism',
    marksWeight: 9,
  },
  {
    id: 'bio-cell-continuity',
    subjectId: 'biology', topicId: 'biology-1-2',
    subjectLabel: 'Biology', topicLabel: 'Cell Continuity', level: 'common',
    gist: 'Cell continuity is about how cells divide. Mitosis makes two daughter cells genetically identical to the parent — used for growth and repair. Meiosis makes four cells that are not identical and have half the chromosome number — used to make gametes (sex cells).',
    oneMove: {
      label: 'Match the division to its job',
      text: 'Mitosis → 2 identical cells → growth and repair. Meiosis → 4 different cells, half the chromosomes → gametes and variation. State the number of cells and the purpose and the marks are yours.',
    },
    check: {
      prompt: 'State one way the daughter cells of meiosis differ from those of mitosis.',
      modelAnswer: 'Meiosis produces cells with half the chromosome number (haploid) that are genetically different from one another; mitosis produces genetically identical cells with the full (diploid) chromosome number.',
      needed: ['Half the chromosome number (meiosis)', 'Genetically different / not identical', '(vs identical in mitosis)'],
    },
    source: 'LC Biology syllabus — Unit 2: Cell Continuity',
    marksWeight: 8,
  },
  {
    id: 'bio-genetics',
    subjectId: 'biology', topicId: 'biology-1-4',
    subjectLabel: 'Biology', topicLabel: 'Genetics', level: 'common',
    gist: 'A gene is a section of DNA that codes for a characteristic. You inherit two versions (alleles), one from each parent. A dominant allele shows its effect even with one copy; a recessive allele shows only when both copies are recessive. Genotype = the alleles (e.g. Tt); phenotype = the physical trait (e.g. tall).',
    oneMove: {
      label: 'Set up a Punnett square cleanly',
      text: 'Define your symbols first. Put one parent’s alleles along the top, the other’s down the side, fill the four boxes. Two heterozygous parents (Tt × Tt) give a 3:1 ratio of dominant:recessive.',
    },
    check: {
      prompt: 'Two parents are both Tt (T = tall, dominant). What ratio of tall to short offspring is expected?',
      modelAnswer: '3 tall : 1 short. The cross Tt × Tt gives TT, Tt, Tt, tt — three with at least one T (tall) and one tt (short).',
      needed: ['3 : 1 ratio', 'Tall : short', 'Shown via TT, Tt, Tt, tt'],
    },
    source: 'LC Biology syllabus — Unit 2: Genetics',
    marksWeight: 10,
  },
  {
    id: 'bio-nutrition-food-tests',
    subjectId: 'biology', topicId: 'biology-0-2',
    subjectLabel: 'Biology', topicLabel: 'Nutrition', level: 'common',
    gist: 'Food is made of biomolecules: carbohydrates (energy), lipids/fats (energy store and membranes) and proteins (growth and repair), plus vitamins, minerals and water. You should know a simple chemical test for the main food types.',
    oneMove: {
      label: 'Learn each test as reagent → colour change',
      text: 'Starch + iodine → blue-black. Reducing sugar + Benedict’s solution, heated → brick-red. Protein + biuret → purple/violet. Name the reagent AND the colour change — half an answer gets half the marks.',
    },
    check: {
      prompt: 'Describe a test for starch, including the result.',
      modelAnswer: 'Add iodine solution to the food sample. If starch is present, the iodine changes from orange/brown to blue-black.',
      needed: ['Iodine solution', 'Blue-black result', 'Colour change stated'],
    },
    source: 'LC Biology syllabus — Unit 1: Nutrition',
    marksWeight: 7,
  },
  {
    id: 'bio-ecology-principles',
    subjectId: 'biology', topicId: 'biology-0-3',
    subjectLabel: 'Biology', topicLabel: 'General Principles of Ecology', level: 'common',
    gist: 'An ecosystem is the living organisms in an area plus their non-living environment. Energy enters through producers (plants, by photosynthesis) and passes along a food chain to consumers. About 90% of the energy is lost at each step (as heat, movement and waste), so only ~10% passes on.',
    oneMove: {
      label: 'Use the 10% rule to explain short food chains',
      text: 'Because ~90% of energy is lost between trophic levels, there isn’t enough left to support many links — so food chains are usually only 4–5 organisms long. Food-chain arrows point the way the energy flows (eaten → eater).',
    },
    check: {
      prompt: 'Why are food chains rarely longer than four or five links?',
      modelAnswer: 'Because roughly 90% of the energy is lost at each trophic level (as heat, movement and waste), so after a few links there is too little energy left to support another organism.',
      needed: ['~90% energy lost per level', 'Too little energy left', '(hence short chains)'],
    },
    source: 'LC Biology syllabus — Unit 1: General Principles of Ecology',
    marksWeight: 8,
  },
  {
    id: 'bio-ecosystem-study',
    subjectId: 'biology', topicId: 'biology-0-4',
    subjectLabel: 'Biology', topicLabel: 'A Study of an Ecosystem', level: 'common',
    gist: 'This is the mandatory ecosystem study. Examiners expect a NAMED ecosystem you actually studied, named organisms in it, how you identified and counted them, and an adaptation. The marks are in the specifics, not general statements.',
    oneMove: {
      label: 'Bank a method + a named organism',
      text: 'Know two methods (e.g. a quadrat or line transect for plants; a pitfall trap or beating tray for animals) and exactly how you used one — plus one named organism and an adaptation it has to that habitat.',
    },
    check: {
      prompt: 'Name a method you could use to estimate the number of a plant species in an ecosystem, and outline how you used it.',
      modelAnswer: 'A quadrat. Place it at random points in the area, count the species inside each quadrat, repeat several times, find the average per quadrat, then scale up to the whole area.',
      needed: ['A named method (quadrat / transect)', 'Random / repeated sampling', 'Count then average / scale up'],
    },
    source: 'LC Biology syllabus — Unit 1: A Study of an Ecosystem (mandatory practical)',
    marksWeight: 8,
  },
  {
    id: 'bio-characteristics-of-life',
    subjectId: 'biology', topicId: 'biology-0-1',
    subjectLabel: 'Biology', topicLabel: 'The Characteristics of Life', level: 'common',
    gist: 'All living organisms carry out the same basic life processes: nutrition, excretion, response to stimuli, movement, growth, reproduction and respiration. These are what separate living things from non-living things.',
    oneMove: {
      label: 'Have the list ready as quick definitions',
      text: 'You can be asked to name characteristics OR define one: nutrition = obtaining food/energy; excretion = removing the waste products of metabolism; response = reacting to a stimulus. Short, precise definitions score.',
    },
    check: {
      prompt: 'List three characteristics of all living organisms.',
      modelAnswer: 'Any three of: nutrition, excretion, response, movement, growth, reproduction, respiration.',
      needed: ['Three valid characteristics', 'From the syllabus list', 'Correctly named'],
    },
    source: 'LC Biology syllabus — Unit 1: The Characteristics of Life',
    marksWeight: 6,
  },
];

/** Subject ids that currently have recovery content (drives the picker). */
export function subjectsWithContent(): { subjectId: string; subjectLabel: string; count: number }[] {
  const map = new Map<string, { subjectId: string; subjectLabel: string; count: number }>();
  for (const c of RECOVERY_CARDS) {
    const e = map.get(c.subjectId) ?? { subjectId: c.subjectId, subjectLabel: c.subjectLabel, count: 0 };
    e.count++;
    map.set(c.subjectId, e);
  }
  return [...map.values()];
}

/** All recovery cards for a subject, in curriculum (syllabus) order. */
export function cardsForSubject(subjectId: string): RecoveryCard[] {
  return RECOVERY_CARDS.filter(c => c.subjectId === subjectId);
}
