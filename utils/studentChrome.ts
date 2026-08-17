/**
 * Global navigation and gamification chrome should step aside while a student
 * is onboarding or reading a module so the primary task has the full viewport.
 */
export const shouldShowStudentChrome = (viewState: string): boolean => (
  viewState !== 'onboarding' && viewState !== 'module'
);
