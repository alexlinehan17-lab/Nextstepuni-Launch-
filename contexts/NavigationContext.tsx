/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useReducer, useCallback, useEffect, useRef } from 'react';
import { type CategoryType } from '../components/KnowledgeTree';

// ─── Types ──────────────────────────────────────────────────

export type ViewState =
  | 'tree' | 'category' | 'module' | 'innovation-zone'
  | 'dashboard' | 'learning-paths' | 'onboarding'
  | 'my-journey' | 'gamification-hub' | 'study-session' | 'insights';

export interface NavigationState {
  viewState: ViewState;
  currentCategory: CategoryType | null;
  currentModuleId: string | null;
  cameFromJourney: boolean;
  activeTool: string | null;
}

type NavigationAction =
  | { type: 'NAVIGATE_TO_TREE' }
  | { type: 'NAVIGATE_TO_CATEGORY'; category: CategoryType }
  | { type: 'NAVIGATE_TO_MODULE'; moduleId: string; fromJourney?: boolean; category?: CategoryType | null }
  | { type: 'NAVIGATE_TO_INNOVATION_ZONE'; tool?: string | null }
  | { type: 'NAVIGATE_TO_DASHBOARD' }
  | { type: 'NAVIGATE_TO_LEARNING_PATHS' }
  | { type: 'NAVIGATE_TO_JOURNEY' }
  | { type: 'NAVIGATE_TO_GAMIFICATION_HUB' }
  | { type: 'NAVIGATE_TO_STUDY_SESSION' }
  | { type: 'NAVIGATE_TO_INSIGHTS' }
  | { type: 'NAVIGATE_TO_ONBOARDING' }
  | { type: 'SET_ACTIVE_TOOL'; tool: string | null }
  | { type: 'RESTORE_STATE'; state: Partial<NavigationState> };

interface NavigationContextValue {
  state: NavigationState;
  dispatch: React.Dispatch<NavigationAction>;
  navigateToTree: () => void;
  navigateToCategory: (category: CategoryType) => void;
  navigateToModule: (moduleId: string, currentViewState?: ViewState, currentCategory?: CategoryType | null) => void;
  navigateToInnovationZone: (tool?: string | null) => void;
  navigateToDashboard: () => void;
  navigateToLearningPaths: () => void;
  navigateToJourney: () => void;
  navigateToGamificationHub: () => void;
  navigateToStudySession: () => void;
  navigateToInsights: () => void;
  navigateToOnboarding: () => void;
  setActiveTool: (tool: string | null) => void;
  goBack: () => void;
}

// ─── URL Serialization ─────────────────────────────────────

const VALID_VIEWS = new Set<string>([
  'tree', 'category', 'module', 'innovation-zone',
  'dashboard', 'learning-paths', 'onboarding',
  'my-journey', 'gamification-hub', 'study-session', 'insights',
]);

function serializeToURL(state: NavigationState): string {
  const params = new URLSearchParams();
  if (state.viewState && state.viewState !== 'tree') {
    params.set('view', state.viewState);
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
  if (view && VALID_VIEWS.has(view)) {
    result.viewState = view as ViewState;
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
      return { viewState: 'tree', currentCategory: null, currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_CATEGORY':
      return { ...state, viewState: 'category', currentCategory: action.category, currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_MODULE':
      return { ...state, viewState: 'module', currentModuleId: action.moduleId, cameFromJourney: action.fromJourney || false, currentCategory: action.category !== undefined ? action.category : state.currentCategory, activeTool: null };
    case 'NAVIGATE_TO_INNOVATION_ZONE':
      return { ...state, viewState: 'innovation-zone', currentModuleId: null, cameFromJourney: false, activeTool: action.tool ?? null };
    case 'NAVIGATE_TO_DASHBOARD':
      return { ...state, viewState: 'dashboard', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_LEARNING_PATHS':
      return { ...state, viewState: 'learning-paths', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_JOURNEY':
      return { ...state, viewState: 'my-journey', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_GAMIFICATION_HUB':
      return { ...state, viewState: 'gamification-hub', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_STUDY_SESSION':
      return { ...state, viewState: 'study-session', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_INSIGHTS':
      return { ...state, viewState: 'insights', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'NAVIGATE_TO_ONBOARDING':
      return { ...state, viewState: 'onboarding', currentModuleId: null, cameFromJourney: false, activeTool: null };
    case 'SET_ACTIVE_TOOL':
      return { ...state, activeTool: action.tool };
    case 'RESTORE_STATE':
      return { ...state, ...action.state };
    default:
      return state;
  }
}

function getInitialState(): NavigationState {
  const base: NavigationState = {
    viewState: 'tree',
    currentCategory: null,
    currentModuleId: null,
    cameFromJourney: false,
    activeTool: null,
  };
  const fromURL = deserializeFromURL();
  if (fromURL.viewState) {
    return { ...base, ...fromURL };
  }
  return base;
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
    const url = serializeToURL(state);
    // Replace (not push) on the initial mount to seed URL without adding a history entry
    if (!window.history.state?.__navSynced) {
      window.history.replaceState({ ...state, __navSynced: true }, '', url);
    } else {
      // State changed after initial mount — check if it actually differs from current history
      const prev = window.history.state;
      const changed = prev.viewState !== state.viewState
        || prev.currentCategory !== state.currentCategory
        || prev.currentModuleId !== state.currentModuleId
        || prev.activeTool !== state.activeTool
        || prev.cameFromJourney !== state.cameFromJourney;
      if (changed) {
        window.history.pushState({ ...state, __navSynced: true }, '', url);
      }
    }
  }, [state]);

  // Browser back/forward: restore from history.state
  useEffect(() => {
    const handlePopState = (e: PopStateEvent) => {
      isPopstateRef.current = true;
      const s = e.state;
      if (s && s.__navSynced) {
        // Restore full state from the history entry
        dispatch({
          type: 'RESTORE_STATE',
          state: {
            viewState: s.viewState || 'tree',
            currentCategory: s.currentCategory || null,
            currentModuleId: s.currentModuleId || null,
            cameFromJourney: s.cameFromJourney || false,
            activeTool: s.activeTool || null,
          },
        });
      } else {
        // No synced state (e.g. external history entry) — fall back to URL
        const fromURL = deserializeFromURL();
        if (fromURL.viewState) {
          dispatch({ type: 'RESTORE_STATE', state: fromURL });
        } else {
          dispatch({ type: 'NAVIGATE_TO_TREE' });
        }
      }
      window.scrollTo(0, 0);
      // isPopstateRef stays true — the URL-sync effect will clear it and skip pushing
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // ─── Convenience navigation functions ───────────────────

  const navigateToTree = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_TREE' });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToCategory = useCallback((category: CategoryType) => {
    navigate({ type: 'NAVIGATE_TO_CATEGORY', category });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToModule = useCallback((moduleId: string, currentViewState?: ViewState, currentCategory?: CategoryType | null) => {
    const fromJourney = currentViewState === 'innovation-zone';
    navigate({ type: 'NAVIGATE_TO_MODULE', moduleId, fromJourney, category: currentCategory });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToInnovationZone = useCallback((tool?: string | null) => {
    navigate({ type: 'NAVIGATE_TO_INNOVATION_ZONE', tool });
    window.scrollTo(0, 0);
  }, [navigate]);

  const navigateToDashboard = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_DASHBOARD' });
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

  const navigateToGamificationHub = useCallback(() => {
    navigate({ type: 'NAVIGATE_TO_GAMIFICATION_HUB' });
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

  const setActiveTool = useCallback((tool: string | null) => {
    navigate({ type: 'SET_ACTIVE_TOOL', tool });
  }, [navigate]);

  const goBack = useCallback(() => {
    window.history.back();
  }, []);

  const value: NavigationContextValue = {
    state,
    dispatch,
    navigateToTree,
    navigateToCategory,
    navigateToModule,
    navigateToInnovationZone,
    navigateToDashboard,
    navigateToLearningPaths,
    navigateToJourney,
    navigateToGamificationHub,
    navigateToStudySession,
    navigateToInsights,
    navigateToOnboarding,
    setActiveTool,
    goBack,
  };

  return <NavigationContext.Provider value={value}>{children}</NavigationContext.Provider>;
};

export default NavigationContext;
