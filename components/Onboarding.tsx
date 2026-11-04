import React from 'react';
import SetupFlow, { type OnboardingProps } from './onboarding/SetupFlow';
import DesktopOnboarding from './onboarding/DesktopSetup';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import { SoundEffects } from './approved-ui-runtime';

export default function Onboarding(props: OnboardingProps) {
  const mobile = useMobileAppDesign();
  const flow = mobile ? <SetupFlow key={`${props.userId}:${props.mode ?? 'fresh'}`} {...props} /> : <DesktopOnboarding key={`${props.userId}:${props.mode ?? 'fresh'}`} {...props} />;
  // One listener for the entire flow also covers menus rendered in portals.
  return typeof globalThis.AudioContext === 'function' ? <SoundEffects>{flow}</SoundEffects> : flow;
}
