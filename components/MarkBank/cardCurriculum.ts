import { findCanonicalTopic, resolveCurriculumSpecification } from '../../curriculumRegistry';

/** The examined specification is distinct from the current practice filter. */
export function examCardCurriculum(subject: string, year: number, nodeIds: string[]) {
  const specification = resolveCurriculumSpecification(subject, year);
  if (!specification) throw new Error(`No curriculum for ${subject} ${year}`);
  const curriculumNodeIds = nodeIds.map(id => {
    const topic = findCanonicalTopic(specification, id);
    if (!topic) throw new Error(`${id} is absent from ${specification.id}`);
    return topic.id;
  });
  return { specVersion: specification.id, specificationId: specification.id, curriculumNodeIds };
}
