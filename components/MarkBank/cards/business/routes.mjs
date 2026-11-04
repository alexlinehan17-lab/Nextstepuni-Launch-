/** @license SPDX-License-Identifier: Apache-2.0 */

/** Every unordered choose-k selection keeps the published route tariff. */
export function expandBusinessRoutePools(pools) {
  return pools.flatMap(pool => {
    const { options, choose, template } = pool;
    if (!Number.isInteger(choose) || choose < 1 || choose > options.length
      || new Set(options.map(option => option.id)).size !== options.length
      || (pool.orderedResponses && pool.orderedResponses.length !== choose)) {
      throw new Error(`Invalid Business route pool ${pool.id}`);
    }
    const selections = [];
    const visit = (start, picked) => {
      if (picked.length === choose) { selections.push(picked); return; }
      for (let i = start; i <= options.length - (choose - picked.length); i++) {
        visit(i + 1, [...picked, options[i]]);
      }
    };
    visit(0, []);
    // A card that shipped before its pool was expanded keeps its ID as one
    // printed route, so saved progress survives; the other routes are added.
    const legacy = pool.legacyRoute;
    const isLegacy = selected => legacy
      && selected.map(option => option.id).join('\n') === legacy.selectedOptionIds.join('\n');
    if (legacy && (selections.filter(isLegacy).length !== 1 || !legacy.correction?.reason)) {
      throw new Error(`Invalid Business legacy route ${pool.id}`);
    }
    return selections.map(selected => {
      // An unequal 7/7/6 sequence prices the candidate's three responses,
      // not particular named options. Keep that sequence separate from the
      // printed option order rather than fixing a larger tariff to one topic.
      const responses = pool.orderedResponses
        ? pool.orderedResponses.map(response => ({ ...response,
          allocations: response.allocations.map(allocation => ({ ...allocation })) }))
        : selected.map(option => ({
          ...option.response, id: option.id, label: option.label,
        }));
      const marks = responses.flatMap(response => response.allocations)
        .reduce((sum, allocation) => sum + allocation.maxMarks, 0);
      if (marks !== template.totalMarks) throw new Error(`Business route tariff changed: ${pool.id}`);
      return {
        ...template,
        id: isLegacy(selected) ? legacy.id : `${pool.id}-${selected.map(option => option.id).join('-')}`,
        ...(isLegacy(selected) ? { correction: legacy.correction } : {}),
        questionText: `${pool.routePrompt}\n${selected.map(option => option.label).join('\n')}`,
        topicId: selected[0].topicId,
        additionalTopicIds: [...new Set(selected.map(option => option.topicId))]
          .filter(id => id !== selected[0].topicId),
        routePoolId: pool.id,
        selectedOptionIds: selected.map(option => option.id),
        rubric: { ...template.rubric, responses },
      };
    });
  });
}
