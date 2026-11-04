/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * What chapter VII's frame holds: the course search, and — once a course
 * is chosen — the course as a card in the page's own idiom: serif title,
 * the points figure, a ruled list of level, length, subjects and careers.
 * Every value is the course's own field (courses.ts).
 */

import React from 'react';
import { COPY } from '../copy';
import { CourseSearch } from './CourseSearch';
import { durationWords, institutionName, pointsLabel, regionName, routeOf, subjectsOf, type CAOCourse } from './courses';

const T = COPY.futurefinder;

const CourseCard: React.FC<{ course: CAOCourse }> = ({ course }) => {
  const subjects = subjectsOf(course);
  const hasPoints = course.typicalPoints > 0;
  return (
    <div className="fxf-card">
      <div className="fxf-card-head">
        <div style={{ minWidth: 0 }}>
          <p className="fxf-card-kicker">{course.code} · {T.routes[routeOf(course)]}</p>
          <h4 className="fxf-card-title">{course.title}</h4>
          <p className="fxf-card-sub">{institutionName(course)} · {regionName(course)}</p>
        </div>
        <div className="fxf-points">
          <span className={`fxf-points-n${hasPoints ? '' : ' fxf-points-n--words'}`}>{pointsLabel(course)}</span>
          <span className="fxf-points-k">{T.card.points}</span>
        </div>
      </div>
      <dl className="fxf-kv">
        <div><dt>{T.card.level}</dt><dd>{course.level}</dd></div>
        <div><dt>{T.card.length}</dt><dd>{durationWords(course.duration)}</dd></div>
        {subjects.length > 0 && <div><dt>{T.card.subjects}</dt><dd>{subjects.join(', ')}</dd></div>}
        {course.careerPaths.length > 0 && <div><dt>{T.card.careers}</dt><dd>{course.careerPaths.join(' · ')}</dd></div>}
      </dl>
      {hasPoints && <p className="fxf-source">{T.card.source}</p>}
    </div>
  );
};

export const CourseFrame: React.FC<{
  course: CAOCourse | null;
  onChoose: (course: CAOCourse) => void;
  inputRef: React.RefObject<HTMLInputElement | null>;
}> = ({ course, onChoose, inputRef }) => (
  <div className="fxf-pad">
    <CourseSearch course={course} onChoose={onChoose} inputRef={inputRef} />
    {course && <CourseCard course={course} />}
  </div>
);

export default CourseFrame;
