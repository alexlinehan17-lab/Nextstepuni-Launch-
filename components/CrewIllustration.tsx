import React from 'react';
import { getPersonalStarCrew } from '../data/personalStarCrew';
import { getSubjectStarCrew } from '../data/subjectStarCrew';
import StarCrewArtwork from './StarCrewArtwork';
import './crew-experiences.css';

/** Approved artwork without an account-avatar circle, for editorial illustrations. */
export default function CrewIllustration({ character = 'star-crew:maker', subject, className = '', label = '' }: {
  character?: string; subject?: string; className?: string; label?: string;
}) {
  const artwork = subject ? getSubjectStarCrew(subject) : getPersonalStarCrew(character);
  const fallback = <img src="/assets/landing/starguy-512.png" alt={label} className={`crew-original theme-ink-art ${className}`} />;
  return artwork ? <StarCrewArtwork artwork={artwork} alt={label} className={`crew-illustration ${className}`} fallback={fallback} /> : fallback;
}
