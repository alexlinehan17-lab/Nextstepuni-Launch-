import { useMobileAppDesign } from './useMobileAppDesign';

/** Single-tap module lists for the mobile/tablet rollout only. */
export function useCompactLayout() {
  return useMobileAppDesign();
}
