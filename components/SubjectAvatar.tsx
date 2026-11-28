import React from 'react';
import { getSubjectStarCrew } from '../data/subjectStarCrew';
import StarCrewArtwork from './StarCrewArtwork';

/** A subject's Star Crew character. `bare`: the artwork alone, with no circle
 *  or patch behind it (Alex, 25 Nov 2026: no tile behind a character), as it
 *  stands at the left of a row. */
export default function SubjectAvatar({ subject, className = '', bare = false }: { subject: string; className?: string; bare?: boolean }) {
  const artwork = getSubjectStarCrew(subject);
  const initials = subject.trim().slice(0, 2).toLocaleUpperCase();
  const fallback = <span className="star-crew-initials">{initials}</span>;
  const classes = `subject-avatar${bare ? ' subject-avatar--bare' : ''} ${className}`;
  return artwork
    ? <StarCrewArtwork artwork={artwork} className={classes} fallback={fallback} transparentBackground={bare || undefined} />
    : <span className={`star-crew-avatar ${classes}`} aria-hidden="true">{fallback}</span>;
}
