import type { StudySessionRecord } from '../../studySessionData';
import { toDateKey } from '../subjectData';

export function fieldNotesData(records: StudySessionRecord[], now = new Date()) {
  const today = toDateKey(now);
  const valid = records.filter(
    (record) =>
      record.date <= today && Number.isFinite(record.actualSeconds) && record.actualSeconds > 0,
  );
  const monday = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate() - ((now.getDay() + 6) % 7),
  );
  const days = Array.from({ length: 7 }, (_, index) => {
    const date = new Date(monday);
    date.setDate(date.getDate() + index);
    const key = toDateKey(date);
    const sessions = valid.filter((record) => record.date === key);
    const seconds = sessions.reduce((sum, record) => sum + record.actualSeconds, 0);
    return {
      key,
      label: date.toLocaleDateString('en-IE', { weekday: 'short' }),
      seconds,
      minutes: Math.floor(seconds / 60),
      sessions: sessions.length,
      future: key > today,
    };
  });
  // Allow yesterday to continue the streak until today's first study session.
  const dates = new Set(valid.map((record) => record.date));
  const cursor = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  if (!dates.has(today)) cursor.setDate(cursor.getDate() - 1);
  let streak = 0;
  while (dates.has(toDateKey(cursor))) {
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
  }
  return {
    days,
    streak,
    minutes: Math.floor(days.reduce((sum, day) => sum + day.seconds, 0) / 60),
    sessions: days.reduce((sum, day) => sum + day.sessions, 0),
    activeDays: days.filter((day) => day.sessions > 0).length,
  };
}
