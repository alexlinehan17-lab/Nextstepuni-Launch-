import React from 'react';
import { LoadingSpinner } from './LoadingSpinner';

/** Shared crew entrance while real account hydration runs; never a timed gate. */
export default function AppLaunch() {
  return <LoadingSpinner overlay selection="random" label="Opening NextStepUni" />;
}
