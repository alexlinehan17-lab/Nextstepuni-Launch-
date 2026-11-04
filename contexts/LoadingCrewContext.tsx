import React, { createContext, useContext, useMemo } from 'react';

const LoadingCrewContext = createContext<{ avatar?: string; draw: number } | undefined>(undefined);

/** Share one draw across nested lazy boundaries; never retain another account's avatar. */
export function LoadingCrewProvider({ avatar, transitionKey, children }: {
  avatar?: string;
  transitionKey: string;
  children: React.ReactNode;
}) {
  const transition = useMemo(() => ({ key: transitionKey, draw: Math.random() }), [transitionKey]);
  const value = useMemo(() => ({ avatar, draw: transition.draw }), [avatar, transition]);
  return <LoadingCrewContext.Provider value={value}>{children}</LoadingCrewContext.Provider>;
}

export const useLoadingCrew = () => useContext(LoadingCrewContext);
