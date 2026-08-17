/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext } from 'react';

export interface ModulePosition {
  displayNumber: string;
  position: number;
  total: number;
}

interface PositionedModule {
  id: string;
  category: string;
}

export function resolveModulePosition(
  visibleModules: readonly PositionedModule[],
  moduleId: string,
): ModulePosition | null {
  const activeModule = visibleModules.find(module => module.id === moduleId);
  if (!activeModule) return null;

  const categoryModules = visibleModules.filter(module => module.category === activeModule.category);
  const index = categoryModules.findIndex(module => module.id === moduleId);
  if (index < 0) return null;

  const position = index + 1;
  return {
    displayNumber: String(position).padStart(2, '0'),
    position,
    total: categoryModules.length,
  };
}

const ModulePositionContext = createContext<ModulePosition | null>(null);

export const ModulePositionProvider: React.FC<{
  value: ModulePosition | null;
  children: React.ReactNode;
}> = ({ value, children }) => (
  <ModulePositionContext.Provider value={value}>
    {children}
  </ModulePositionContext.Provider>
);

export const useModulePosition = (): ModulePosition | null => useContext(ModulePositionContext);
