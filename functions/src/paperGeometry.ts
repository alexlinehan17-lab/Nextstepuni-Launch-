export const NEIGHBOURS = [
  [1, 0], [0, 1], [-1, 1], [-1, 0], [0, -1], [1, -1],
] as const;

export const axialDistance = (
  a: { q:number; r:number }, b: { q:number; r:number },
) => Math.max(Math.abs(a.q-b.q), Math.abs(a.r-b.r), Math.abs(a.q+a.r-b.q-b.r));
