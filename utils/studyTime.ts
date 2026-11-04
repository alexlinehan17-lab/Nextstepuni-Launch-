export function formatStudyTime(seconds: number) {
  const minutes = Math.floor(Math.max(0, seconds) / 60);
  const remainder = Math.floor(Math.max(0, seconds) % 60);
  return remainder ? `${minutes} min ${remainder} sec` : `${minutes} minute${minutes === 1 ? '' : 's'}`;
}
