import { describe, expect, test } from 'vitest';
import type { CAOCourse } from '@/components/futureFinderData';
import { CAO_COURSES } from '@/components/futureFinderData';
import { COURSE_RIASEC } from '@/components/futureFinderRiasecData';
import { codeFromProfile, profileFromCode, scoreCourseFit, type CourseFitResult, type WorkValue } from '@/components/futureFinderRiasec';
import type { StudentSubjectProfile } from '@/components/subjectData';
import {
  compareRecommendations,
  computeTargetCAOPoints,
  pointsFeasibility,
  routeAlignment,
  scoreRecommendation,
} from '@/components/futureFinderRecommendation';

const course = (level: 5 | 6 | 7 | 8, typicalPoints: number, pathwayType?: CAOCourse['pathwayType']): CAOCourse => ({
  code: `TEST-${level}-${typicalPoints}`, title: 'Test', institution: 'Test', level, typicalPoints,
  duration: 4, interestTags: [], workStyleTags: [], careerPaths: [], subjectBonus: [], region: 'dublin',
  description: '', employability: 3, salaryBand: 'mid', pathwayType,
});
const fit = (fitR: number, reach: CourseFitResult['reach']): CourseFitResult => ({
  fitR, fitBucket: 'best', matchPct: 90, reach, eligibility: { eligible: true, missing: [] }, valuesCongruence: 0.5,
});

describe('Future Finder recommendation ranking', () => {
  test('uses target grades, best six and the Higher Maths bonus', () => {
    const profile: StudentSubjectProfile = {
      subjects: [
        { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H7', targetGrade: 'H2' },
        { subjectName: 'English', level: 'higher', currentGrade: 'H7', targetGrade: 'H1' },
        { subjectName: 'Irish', level: 'higher', currentGrade: 'H7', targetGrade: 'H2' },
        { subjectName: 'Biology', level: 'higher', currentGrade: 'H7', targetGrade: 'H3' },
        { subjectName: 'Chemistry', level: 'higher', currentGrade: 'H7', targetGrade: 'H4' },
        { subjectName: 'Business', level: 'higher', currentGrade: 'H7', targetGrade: 'H5' },
        { subjectName: 'History', level: 'higher', currentGrade: 'H7', targetGrade: 'H6' },
      ],
      examStartDate: '2027-06-09', restDays: [], createdAt: '', updatedAt: '',
    };
    // Best six: Maths H2 88 + 25 bonus, then 100 + 88 + 77 + 66 + 56.
    expect(computeTargetCAOPoints(profile)).toBe(500);
  });
  test('points feasibility declines as the target gap grows', () => {
    expect(pointsFeasibility(400, 400)).toBe(1);
    expect(pointsFeasibility(400, 450)).toBeGreaterThan(pointsFeasibility(400, 500));
    expect(pointsFeasibility(100, 500)).toBeLessThan(0.1);
  });
  test('route alignment favours Level 8 for a 500-point student', () => {
    expect(routeAlignment(500, course(8, 480))).toBeGreaterThan(routeAlignment(500, course(7, 200)));
  });
  test('route alignment favours accessible routes for a 100-point student', () => {
    expect(routeAlignment(100, course(5, 0, 'plc'))).toBeGreaterThan(routeAlignment(100, course(8, 500)));
  });
  test('a realistic strong fit outranks a slightly better impossible fit', () => {
    const realistic = scoreRecommendation(course(7, 180), fit(0.75, 'match'), 170);
    const impossible = scoreRecommendation(course(8, 500), fit(0.9, 'out-of-reach'), 170);
    expect(realistic.score).toBeGreaterThan(impossible.score);
    expect(realistic.band).toBe('realistic');
    expect(impossible.band).toBe('explore');
  });

  const catalogueRanking = (code: string, targetPoints: number) => {
    const studentProfile = profileFromCode(code);
    const studentCode = codeFromProfile(studentProfile);
    const values: WorkValue[] = [];
    return CAO_COURSES.flatMap((catalogueCourse) => {
      const metadata = COURSE_RIASEC[catalogueCourse.code];
      if (!metadata) return [];
      const courseFit = scoreCourseFit({
        studentProfile,
        studentCode,
        studentPoints: targetPoints,
        studentSubjects: [],
        studentValues: values,
        course: { ...metadata, typicalPoints: catalogueCourse.typicalPoints },
      });
      return [{
        course: catalogueCourse,
        fit: courseFit,
        recommendation: scoreRecommendation(catalogueCourse, courseFit, targetPoints),
      }];
    }).sort(compareRecommendations);
  };

  test('a 100-point profile receives accessible routes before 500-point stretches', () => {
    const topTen = catalogueRanking('IRC', 100).slice(0, 10);
    expect(topTen.slice(0, 5).every((entry) => entry.recommendation.band === 'realistic')).toBe(true);
    expect(topTen.every((entry) => entry.course.typicalPoints < 400)).toBe(true);
    expect(topTen.slice(0, 2).map((entry) => entry.course.code)).toEqual(
      expect.arrayContaining(['PLC-IT', 'APP-SWDEV']),
    );
  });

  test('a 500-point profile is not headed by lower-level routes when comparable Level 8 routes fit', () => {
    const topTen = catalogueRanking('IRC', 500).slice(0, 10);
    expect(topTen.filter((entry) => entry.course.level === 8).length).toBeGreaterThanOrEqual(7);
  });

  test('a social profile is led by education and care routes at a lower target', () => {
    const topTen = catalogueRanking('SAE', 180).slice(0, 10);
    expect(topTen.slice(0, 2).map((entry) => entry.course.code)).toEqual(
      expect.arrayContaining(['PLC-CHILD', 'AU190']),
    );
    expect(topTen.every((entry) => entry.course.typicalPoints <= 430)).toBe(true);
  });

  test('a strong artistic profile can see a closely matched ambitious route before weak realistic routes', () => {
    const topTen = catalogueRanking('AES', 350).slice(0, 10);
    expect(topTen[0].course.code).toBe('DC131');
    expect(topTen.findIndex((entry) => entry.course.code === 'DC132')).toBeLessThan(6);
  });

  test('a high-target enterprising profile is led by business and commerce', () => {
    const topTen = catalogueRanking('ECI', 500).slice(0, 10);
    expect(topTen.every((entry) => /business|commerce|accounting/i.test(entry.course.title))).toBe(true);
  });
});
