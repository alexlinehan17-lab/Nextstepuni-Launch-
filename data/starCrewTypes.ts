export interface StarCrewArtwork {
  src: string;
  /** Percentages measured from the approved artwork's visible ink bounds. */
  frame: { width: number; left: number; top: number; tile?: number };
}
