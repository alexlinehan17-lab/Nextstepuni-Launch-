/**
 * Global navigation and gamification chrome should step aside while a student
 * is onboarding or reading a module so the primary task has the full viewport.
 */
export const shouldShowStudentChrome = (viewState: string): boolean => (
  viewState !== 'onboarding' && viewState !== 'module'
);

/**
 * Sidebar B stays beside a module on a laptop (area 5 of the design build, board c-read-desk: "Sidebar B;
 * then, as one group centred in the space beside it, the steps ... and the step"). It mounts only from
 * 768px, so a phone's reader keeps the whole screen; the rest of the chrome still steps aside.
 */
export const shouldShowStudentSidebar = (viewState: string): boolean => (
  shouldShowStudentChrome(viewState) || viewState === 'module'
);
