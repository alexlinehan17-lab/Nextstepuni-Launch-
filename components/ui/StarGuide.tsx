import React from 'react';

/** The original onboarding character is the app's shared mascot. */
export default function StarGuide({ size = 96, className = '' }: { size?: number; className?: string }) {
  return <img src="/icons/onboarding/star-person.png" alt="" aria-hidden="true" width={size} height={size} className={`object-contain ${className}`} style={{ width: size, height: size }} />;
}
