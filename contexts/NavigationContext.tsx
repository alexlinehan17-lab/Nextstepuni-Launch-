/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useReducer, useCallback, useEffect, useRef } from 'react';
import { type CategoryType } from '../components/KnowledgeTree';
import { useAuth } from './AuthContext';

// ─── Types ──────────────────────────────────────────────────

export type ViewState =
  | 'tree' | 'modules' | 'category' | 'module' | 'innovation-zone'
  | 'dashboard' | 'learning-paths' | 'onboarding'
  | 'my-journey' | 'my-direction' | 'study-session' | 'insights'
  | 'jc-coming-soon' | 'cut-content' | 'accreditation' | 'year-plans' | 'wip-tools';

export type DashboardSection = 'overview' | 'study' | 'confidence' | 'practice' | 'milestones';

export interface NavigationState {
  viewState: ViewState;
  dashboardSection: DashboardSection;
  currentCategory: CategoryType | null;
  currentModuleId: string | null;
  cameFromJourney: boolean;
  activeTool: string | null;
}

type NavigationAction =
  | { type: 'NAVIGATE_TO_TREE' }
  | { type: 'NAVIGATE_TO_MODULES' }
  | { type: 'NAVIGATE_TO_CATEGORY'; category: CategoryType }
  | { type: 'NAVIGATE_TO_MODULE'; moduleId: string; fromJourney?: boolean; category?: CategoryType | null }
  | { type: 'NAVIGATE_TO_INNOVATION_ZONE'; tool?: string | null }
  | { type: 'NAVIGATE_TO_DASHBOARD'; section?: DashboardSection }
  | { type: 'NAVIGATE_TO_LEARNING_PATHS' }
  | { type: 'NAVIGATE_TO_JOURNEY' }
  | { type: 'NAVIGATE_TO_DIRECTION' }
  | { type: 'NAVIGATE_TO_STUDY_SESSION' }
  | { type: 'NAVIGATE_TO_INSIGHTS' }
  | { type: 'NAVIGATE_TO_ONBOARDING' }
  | { type: 'NAVIGATE_TO_JC_COMING_SOON'; fromModuleId: string }
  | { type: 'NAVIGATE_TO_CUT_CONTENT' }
  | { type: 'NAVIGATE_TO_ACCREDITATION' }
  | { type: 'NAVIGATE_TO_YEAR_PLANS' }
  | { type: 'NAVIGATE_TO_WIP_TOOLS' }
  | { type: 'SET_DASHBOARD_SECTION'; section: DashboardSection }
  | { type: 'SET_ACTIVE_TOOL'; tool: string | null }
  | { type: 'RESTORE_STATE'; state: Partial<NavigationState> };

interface NavigationContextValue {
  state: NavigationState;
  dispatch: React.Dispatch<NavigationAction>;
  navigateToTree: () => void;
  navigateToModules: () => void;
  navigateToCategory: (category: CategoryType) => void;
  navigateToModule: (moduleId: string, currentViewState?: ViewState, currentCategory?: CategoryType | null, fromJourney?: boolean) => void;
  navigateToInnovationZone: (tool?: string | null) => void;
  navigateToDashboard: (section?: DashboardSection) => void;
  navigateToLearningPaths: () => void;
  navigateToJourney: () => void;
  navigateToDirection: () => void;
  navigateToStudySession: () => void;
  navigateToInsights: () => void;
  navigateToOnboarding: () => void;
  navigateToJCComingSoon: (fromModuleId: string) => void;
  navigateToCutContent: () => void;
  navigateToAccreditation: () => void;
  navigateToYearPlans: () => void;
  navigateToWipTools: () => void;
  setDashboardSection: (section: DashboardSection) => void;
  setActiveTool: (tool: string | null) => void;
  goBack: () => void;
}

// ─── URL Serialization ─────────────────────────────────────

const VALID_VIEWS = new Set<string>([
  'tree', 'modules', 'category', 'module', 'innovation-zone',
  'dashboard', 'learning-paths', 'onboarding',
  'my-journey', 'my-direction', 'study-session', 'insights',
  'jc-coming-soon', 'cut-content', 'accreditation', 'year-plans', 'wip-tools',
]);

const VALID_DASHBOARD_SECTIONS = new Set<DashboardSection>([
  'overview', 'study', 'confidence', 'practice', 'milestones',
]);

const DEFAULT_NAVIGATION_STATE: NavigationState = {
  viewState: 'tree',
  dashboardSection: 'overview',
  currentCategory: null,
  currentModuleId: null,
  cameFromJourney: false,
  activeTool: null,
};

const isDashboardSection = (value: unknown): value is DashboardSection => (
  typeof value === 'string' && VALID_DASHBOARD_SECTIONS.has(value as DashboardSection)
);

const isFirebaseAuthActionRoute = () => {
  const path = window.location.pathname;
  const search = window.location.search;
  return path === '/reset-password'
    || path.startsWith('/reset-password/')
    || search.includes('mode=resetPassword');
};

function serializeToURL(state: NavigationState): string {
  const params = new URLSearchParams();
  if (state.viewState && state.viewState !== 'tree') {
    params.set('view', state.viewState);
  }
  if (state.viewState === 'dashboard' && state.dashboardSection !== 'overview') {
    params.set('section', state.dashboardSection);
  }
  if (state.currentCategory) params.set('cat', state.currentCategory);
  if (state.currentModuleId) params.set('mod', state.currentModuleId);
  if (state.activeTool) params.set('tool', state.activeTool);
  if (state.cameFromJourney) params.set('from', 'journey');
  const qs = params.toString();
  return qs ? `?${qs}` : window.location.pathname;
}

function deserializeFromURL(): Partial<NavigationState> {
  const params = new URLSearchParams(window.location.search);
  const result: Partial<NavigationState> = {};

  const view = params.get('view');
  // Training Hub was consolidated into My Progress. Keep old bookmarks and
  // shared links useful by resolving the retired view to its new section.
  if (view === 'gamification-hub') {
    result.viewState = 'dashboard';
    result.dashboardSection = 'milestones';
  } else if (view && VALID_VIEWS.has(view)) {
    result.viewState = view as ViewState;
    if (view === 'dashboard') {
      const section = params.get('section');
      result.dashboardSection = isDashboardSection(section) ? section : 'overview';
    }
  }
  const cat = params.get('cat');
  if (cat) result.currentCategory = cat as CategoryType;
  const mod = params.get('mod');
  if (mod) result.currentModuleId = mod;
  const tool = params.get('tool');
  if (tool) result.activeTool = tool;
  const from = params.get('from');
  if (from === 'journey') result.cameFromJourney = true;

  return result;
}

// ─── Reducer ────────────────────────────────────────────────

function navigationReducer(state: NavigationState, action: NavigationAction): NavigationState {
  switch (action.type) {
    case 'NAVIGATE_TO_TREE':
      return { ...DEFAULT_NAVIGATION_STATE };
    case 'NAVIGATE_TO_MODULES':
      return { ...state, viewState: 'modules', currentCategory: null, currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_CATEGORY':
      return { ...state, viewState: 'category', currentCategory: action.category, currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_MODULE':
      return { ...state, viewState: 'module', currentModuleId: action.moduleId, cameFromJourney: action.fromJourney || false, currentCategory: action.category !== undefined ? action.category : state.currentCategory, activeTool: null };
    case 'NAVIGATE_TO_INNOVATION_ZONE':
      return { ...state, viewState: 'innovation-zone', currentModuleId: null, cameFromJourney: false, activeTool: action.tool ?? null };
    case 'NAVIGATE_TO_DASHBOARD':
      return { ...state, viewState: 'dashboard', dashboardSection: action.section ?? 'overview', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_LEARNING_PATHS':
      return { ...state, viewState: 'learning-paths', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_JOURNEY':
      return { ...state, viewState: 'my-journey', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_DIRECTION':
      return { ...state, viewState: 'my-direction', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_STUDY_SESSION':
      return { ...state, viewState: 'study-session', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_INSIGHTS':
      return { ...state, viewState: 'insights', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_ONBOARDING':
      return { ...state, viewState: 'onboarding', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_JC_COMING_SOON':
      // Reuse `currentModuleId` to remember which module the JC user clicked
      // so the placeholder can show its title and so browser back works.
      return { ...state, viewState: 'jc-coming-soon', currentModuleId: action.fromModuleId, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_CUT_CONTENT':
      return { ...state, viewState: 'cut-content', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_ACCREDITATION':
      return { ...state, viewState: 'accreditation', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_YEAR_PLANS':
      return { ...state, viewState: 'year-plans', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_WIP_TOOLS':
      return { ...state, viewState: 'wip-tools', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'SET_DASHBOARD_SECTION':
      if (state.viewState !== 'dashboard' || state.dashboardSection === action.section) return state;
      return { ...state, dashboardSection: action.section };
    case 'SET_ACTIVE_TOOL':
      if (state.activeTool === action.tool) return state;
      return { ...state, activeTool: action.tool };
    case 'RESTORE_STATE':
      return { ...state, ...action.state };
    default:
      return state;
  }
}

function getInitialState(): NavigationState {
  const fromURL = deserializeFromURL();
  if (fromURL.viewState) {
    return { ...DEFAULT_NAVIGATION_STATE, ...fromURL };
  }
  return { ...DEFAULT_NAVIGATION_STATE };
}

// ─── Context ────────────────────────────────────────────────

const NavigationContext = createContext<NavigationContextValue | null>(null);

export const useNavigation = (): NavigationContextValue => {
  const ctx = useContext(NavigationContext);
  if (!ctx) throw new Error('useNavigation must be used within NavigationProvider');
  return ctx;
};

// ─── Provider ───────────────────────────────────────────────

export const NavigationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(navigationReducer, undefined, getInitialState);
  const isPopstateRef = useRef(false);
  const { user, authResolved } = useAuth();
  const prevUserUidRef = useRef<string | null | undefined>(undefined);

  // Single atomic helper: dispatch + pushState + URL update
  const navigate = useCallback((action: NavigationAction) => {
    dispatch(action);
  }, []);

  // Sync URL after every state change.
  // When popstate fires, isPopstateRef is set true; this effect clears it and skips,
  // preventing a duplicate pushState for the browser-initiated navigation.
  useEffect(() => {
    if (isPopstateRef.current) {
      isPopstateRef.current = false;
      return;
    }
    // Skip URL sync entirely when we're on a Firebase auth action route — the
    // query params (mode=resetPassword, oobCode, apiKey) carry the reset code
    // and must survive long enough for ResetPasswordPage to read them.
    // Re-rewriting the URL from navigation state strips those params.
    if (typeof window !== 'undefined' && isFirebaseAuthActionRoute()) {
      return;
    }
    const url = serializeToURL(state);
    const currentHistoryState = window.history.state;
    const currentURLView = new URLSearchParams(window.location.search).get('view');
    const isLegacyTrainingHubEntry = currentHistoryState?.viewState === 'gamification-hub'
      || currentURLView === 'gamification-hub';
    // Replace (not push) on the initial mount to seed URL without adding a history entry
    if (!currentHistoryState?.__navSynced || isLegacyTrainingHubEntry) {
      window.history.replaceState({ ...state, __navSynced: true }, '', url);
    } else {
      // State changed after initial mount — check if it actually differs from current history
      const prev = currentHistoryState;
      const routeChanged = prev.viewState !== state.viewState
        || prev.currentCategory !== state.currentCategory
        || prev.currentModuleId !== state.currentModuleId
        || prev.activeTool !== state.activeTool
        || prev.cameFromJourney !== state.cameFromJourney;
      const dashboardSectionChanged = state.viewState === 'dashboard'
        && prev.viewState === 'dashboard'
        && (prev.dashboardSection ?? 'overview') !== state.dashboardSection;
      if (dashboardSectionChanged && !routeChanged) {
        // Tabs are sections of one destination, not extra stops. Replace the
        // dashboard entry so leaving it remains a single Back action, while a
        // later Back from another page still restores the selected section.
        window.history.replaceState({ ...state, __navSynced: true }, '', url);
      } else if (routeChanged || dashboardSectionChanged) {
        window.history.pushState({ ...state, __navSynced: true }, '', url);
      }
    }
  }, [state]);

  // Browser back/forward: restore from history.state
  useEffect(() => {
    const handlePopState = (e: PopStateEvent) => {
      isPopstateRef.current = true;
      const s = e.state;
      let restoredState: NavigationState;
      if (s && s.__navSynced) {
        const isLegacyTrainingHub = s.viewState === 'gamification-hub';
        const restoredView = isLegacyTrainingHub
          ? 'dashboard'
          : (VALID_VIEWS.has(s.viewState) ? s.viewState as ViewState : 'tree');
        restoredState = {
          viewState: restoredView,
          dashboardSection: isLegacyTrainingHub
            ? 'milestones'
            : (isDashboardSection(s.dashboardSection) ? s.dashboardSection : 'overview'),
          currentCategory: s.currentCategory || null,
          currentModuleId: s.currentModuleId || null,
          cameFromJourney: s.cameFromJourney || false,
          activeTool: s.activeTool || null,
        };
      } else {
        // No synced state (e.g. external history entry) — fall back to URL
        const fromURL = deserializeFromURL();
        restoredState = fromURL.viewState
          ? { ...DEFAULT_NAVIGATION_STATE, ...fromURL }
          : { ...DEFAULT_NAVIGATION_STATE };
      }

      // Seed or normalize the entry in place. This keeps browser Back from
      // resurfacing the retired Training Hub URL or creating a duplicate entry.
      if (!isFirebaseAuthActionRoute()) {
        window.history.replaceState(
          { ...restoredState, __navSynced: true },
          '',
          serializeToURL(restoredState),
        );
      }
      dispatch({ type: 'RESTORE_STATE', state: restoredState });
      window.scrollTo(0, 0);
      // isPopstateRef stays true — the URL-sync effect will clear it and skip pushing
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Reset navigation state on logout or user change to prevent stale state leaking
  // between sessions.
  //
  // Gated on `authResolved` because on page reload the auth flow goes
  // null → resolved user across multiple renders. Without this gate, the
  // first transition (null → user) trips the "user changed" branch and
  // wipes the URL-restored view back to tree on every reload.
  useEffect(() => {
    if (!authResolved) return;
    const currentUid = user?.uid ?? null;
    if (prevUserUidRef.current !== undefined && prevUserUidRef.current !== currentUid) {
      dispatch({ type: 'NAVIGATE_TO_TREE' });
    }
    prevUserUidRef.current = currentUid;
  }, [user, authResolved]);

  // ─── Convenience navigation functions ───────────────────

  const navigateToTree = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_TREE' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToModules = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_MODULES' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToCategory = useCallback((category: CategoryType) => {
    navigate({ type: 'NAVIGATE_TO_CATEGORY', category });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToModule = useCallback((moduleId: string, _currentViewState?: ViewState, currentCategory?: CategoryType | null, fromJourney = false) => {
    // Journey provenance is explicit. Inferring it from the current screen is
    // unsafe because global overlays (notably the mobile profile) can open a
    // module while the Journey tool happens to be visible underneath.
    navigate({ type: 'NAVIGATE_TO_MODULE', moduleId, fromJourney, category: currentCategory });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToInnovationZone = useCallback((tool?: string | null) => {
    navigate({ type: 'NAVIGATE_TO_INNOVATION_ZONE', tool });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToDashboard = useCallback((section: DashboardSection = 'overview') => {
    navigate({ type: 'NAVIGATE_TO_DASHBOARD', section });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToLearningPaths = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_LEARNING_PATHS' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToJourney = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_JOURNEY' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToDirection = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_DIRECTION' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToStudySession = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_STUDY_SESSION' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToInsights = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_INSIGHTS' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToOnboarding = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_ONBOARDING' });
  }, [navigate]);

  const navigateToJCComingSoon = useCallback((fromModuleId: string) => {
    navigate({ type: 'NAVIGATE_TO_JC_COMING_SOON', fromModuleId });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToCutContent = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_CUT_CONTENT' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToYearPlans = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_YEAR_PLANS' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToWipTools = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_WIP_TOOLS' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToAccreditation = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_ACCREDITATION' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const setActiveTool = useCallback((tool: string | null) => {
    navigate({ type: 'SET_ACTIVE_TOOL', tool });
  }, [navigate]);

  const setDashboardSection = useCallback((section: DashboardSection) => {
    navigate({ type: 'SET_DASHBOARD_SECTION', section });
    window.scrollTo(0, 0);
  }, [navigate]);

  const goBack = useCallback(() => {
    window.history.back();
  }, []);

  const value: NavigationContextValue = {
    state,
    dispatch,
    navigateToTree,
    navigateToModules,
    navigateToCategory,
    navigateToModule,
    navigateToInnovationZone,
    navigateToDashboard,
    navigateToLearningPaths,
    navigateToJourney,
    navigateToDirection,
    navigateToStudySession,
    navigateToInsights,
    navigateToOnboarding,
    navigateToJCComingSoon,
    navigateToCutContent,
    navigateToAccreditation,
    navigateToYearPlans,
    navigateToWipTools,
    setDashboardSection,
    setActiveTool,
    goBack,
  };

  return <NavigationContext.Provider value={value}>{children}</NavigationContext.Provider>;
};

export default NavigationContext;
