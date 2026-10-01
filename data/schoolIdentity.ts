import type { SchoolId } from '../schoolData';

// Display-only metadata. Existing school IDs and server-side membership checks stay authoritative.
export const SCHOOL_IDENTITY: Record<SchoolId, { fullName: string; crest: string; website: string }> = {
  marino: { fullName: 'Marino College', crest: 'marino.png', website: 'https://www.marinocollege.ie/' },
  joeys: { fullName: 'St Joseph’s, Fairview', crest: 'joeys.png', website: 'https://stjosephsfairview.ie/' },
  larkin: { fullName: 'Larkin Community College', crest: 'larkin.jpg', website: 'https://larkincommunitycollege.ie/' },
  oconnells: { fullName: 'O’Connell Secondary School', crest: 'oconnells.png', website: 'https://www.oconnellschool.ie/' },
  mountcarmel: { fullName: 'Mount Carmel Secondary School', crest: 'mountcarmel.png', website: 'https://mountcarmelsecondaryschool.ie/' },
  rosmini: { fullName: 'Grace Park Community School', crest: 'rosmini.jpg', website: 'https://rosmini.ie/' },
  pwc: { fullName: 'PwC', crest: 'pwc.svg', website: 'https://www.pwc.ie/' },
};
