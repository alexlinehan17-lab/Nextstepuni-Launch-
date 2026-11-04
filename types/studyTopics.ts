/** @license SPDX-License-Identifier: Apache-2.0 */
export interface StudyTopicSelection {
  subjectId: string;
  specificationId: string;
  topicIds: string[];
}

export interface StudyTopicAllocation {
  topicId: string;
  seconds: number;
}
