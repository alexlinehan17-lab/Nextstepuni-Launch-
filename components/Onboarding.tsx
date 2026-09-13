import React from 'react';
import SetupFlow, { type OnboardingProps } from './onboarding/SetupFlow';
import DesktopOnboarding from './onboarding/DesktopSetup';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';

export default function Onboarding(props: OnboardingProps) {
  const mobile = useMobileAppDesign();
  return mobile ? <SetupFlow key={`${props.userId}:${props.mode ?? 'fresh'}`} {...props} /> : <DesktopOnboarding key={`${props.userId}:${props.mode ?? 'fresh'}`} {...props} />;
}
