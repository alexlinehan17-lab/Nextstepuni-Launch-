/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Local-only student data for the Vite "DEV: Skip Login" affordance. The
 * reserved uid is never authenticated and none of this is written to
 * Firestore; it simply gives UI work a complete, realistic student state.
 */
import { type StudentSubjectProfile } from '../components/subjectData';
import { type NorthStar } from '../types';
import { type SessionUser } from '../utils/authUtils';

export const DEV_STUDENT_UID = 'dev-student';

const nextLeavingCertDate = (today: Date): string => {
  const examYear = today.getMonth() >= 5 ? today.getFullYear() + 1 : today.getFullYear();
  return `${examYear}-06-09`;
};

export const createDevStudentSession = (): SessionUser => ({
  uid: DEV_STUDENT_UID,
  name: 'Dev User',
  avatar: 'Casper',
  role: 'student',
  isAdmin: false,
  yearGroup: '6th',
  curriculumLevel: 'senior',
});

export const createDevStudentProfile = (today = new Date()): StudentSubjectProfile => {
  const now = today.toISOString();
  return {
    yearGroup: '6th',
    curriculumLevel: 'senior',
    examStartDate: nextLeavingCertDate(today),
    restDays: ['Sunday'],
    defaultBlockDuration: 45,
    createdAt: now,
    updatedAt: now,
    subjects: [
      { subjectName: 'Politics & Society', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'Geography', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'Applied Maths', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'English', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'Irish', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'Accounting', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
    ],
  };
};

export const createDevStudentNorthStar = (today = new Date()): NorthStar => {
  const now = today.toISOString();
  return {
    category: 'options-freedom',
    statement: 'Get enough points so I have choices',
    visionBoard: ['real-choices', 'see-world', 'freedom-no'],
    createdAt: now,
    updatedAt: now,
    reviewedAt: now,
    authoredByStudent: false,
  };
};

export const createDevStudentLoadedData = (today = new Date()) => {
  const studentProfile = createDevStudentProfile(today);
  const northStar = createDevStudentNorthStar(today);
  return {
    userProgress: {},
    northStar,
    studentProfile,
    needsOnboarding: false,
    unlockedAvatarSeeds: [],
    unlockedThemes: [],
    unlockedCardStyles: [],
    dismissedGuides: {},
    timetableCompletions: {},
    rawProgressDoc: {
      subjectProfile: studentProfile,
      northStar,
    },
  };
};
