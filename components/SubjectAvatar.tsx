import React from 'react';
import { getSubjectStarCrew } from '../data/subjectStarCrew';
import StarCrewArtwork from './StarCrewArtwork';

export default function SubjectAvatar({ subject, className = '' }: { subject: string; className?: string }) {
  const artwork = getSubjectStarCrew(subject);
  const initials = subject.trim().slice(0, 2).toLocaleUpperCase();
  const fallback = <span className="star-crew-initials">{initials}</span>;
  return artwork
    ? <StarCrewArtwork artwork={artwork} className={`subject-avatar ${className}`} fallback={fallback} />
    : <span className={`star-crew-avatar subject-avatar ${className}`} aria-hidden="true">{fallback}</span>;
}
