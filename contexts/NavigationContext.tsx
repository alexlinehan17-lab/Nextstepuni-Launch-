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

interface NavigationState {
  viewState: ViewState;
  currentCategory: CategoryType | null;
  currentModuleId: string | null;
  cameFromJourney: boolean;
}

type NavigationAction =
  | { type: 'NAVIGATE_TO_TREE' }
  | { type: 'NAVIGATE_TO_CATEGORY'; category: CategoryType }
  | { type: 'NAVIGATE_TO_MODULE'; moduleId: string; fromJourney?: boolean; category?: CategoryType | null }
  | { type: 'NAVIGATE_TO_INNOVATION_ZONE' }
  | { type: 'NAVIGATE_TO_DASHBOARD' }
  | { type: 'NAVIGATE_TO_LEARNING_PATHS' }
  | { type: 'NAVIGATE_TO_JOURNEY' }
  | { type: 'NAVIGATE_TO_GAMIFICATION_HUB' }
  | { type: 'NAVIGATE_TO_STUDY_SESSION' }
  | { type: 'NAVIGATE_TO_INSIGHTS' }
  | { type: 'NAVIGATE_TO_ONBOARDING' }
  | { type: 'RESTORE_STATE'; state: Partial<NavigationState> };

interface NavigationContextValue {
  state: NavigationState;
  dispatch: React.Dispatch<NavigationAction>;
  // Convenience handlers (push history + dispatch)
  navigateToTree: () => void;
  navigateToCategory: (category: CategoryType) => void;
  navigateToModule: (moduleId: string, currentViewState?: ViewState, currentCategory?: CategoryType | null) => void;
  navigateToInnovationZone: () => void;
  navigateToDashboard: () => void;
  navigateToLearningPaths: () => void;
  navigateToJourney: () => void;
  navigateToGamificationHub: () => void;
  navigateToStudySession: () => void;
  navigateToInsights: () => void;
  navigateToOnboarding: () => void;
  goBack: () => void;
}

// ─── Reducer ────────────────────────────────────────────────

function navigationReducer(state: NavigationState, action: NavigationAction): NavigationState {
  switch (action.type) {
    case 'NAVIGATE_TO_TREE':
      return { viewState: 'tree', currentCategory: null, currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_CATEGORY':
      return { ...state, viewState: 'category', currentCategory: action.category, currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_MODULE':
      return { ...state, viewState: 'module', currentModuleId: action.moduleId, cameFromJourney: action.fromJourney || false, currentCategory: action.category !== undefined ? action.category : state.currentCategory };
    case 'NAVIGATE_TO_INNOVATION_ZONE':
      return { ...state, viewState: 'innovation-zone', currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_DASHBOARD':
      return { ...state, viewState: 'dashboard', currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_LEARNING_PATHS':
      return { ...state, viewState: 'learning-paths', currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_JOURNEY':
      return { ...state, viewState: 'my-journey', currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_GAMIFICATION_HUB':
      return { ...state, viewState: 'gamification-hub', currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_STUDY_SESSION':
      return { ...state, viewState: 'study-session', currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_INSIGHTS':
      return { ...state, viewState: 'insights', currentModuleId: null, cameFromJourney: false };
    case 'NAVIGATE_TO_ONBOARDING':
      return { ...state, viewState: 'onboarding', currentModuleId: null, cameFromJourney: false };
    case 'RESTORE_STATE':
      return { ...state, ...action.state };
    default:
      return state;
  }
}

const initialState: NavigationState = {
  viewState: 'tree',
  currentCategory: null,
  currentModuleId: null,
  cameFromJourney: false,
};

// ─── Context ────────────────────────────────────────────────

const NavigationContext = createContext<NavigationContextValue | null>(null);

export const useNavigation = (): NavigationContextValue => {
  const ctx = useContext(NavigationContext);
  if (!ctx) throw new Error('useNavigation must be used within NavigationProvider');
  return ctx;
};

// ─── Provider ───────────────────────────────────────────────

export const NavigationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(navigationReducer, initialState);
  const isPopstateRef = useRef(false);

  // Browser back/forward support
  useEffect(() => {
    const handlePopState = (e: PopStateEvent) => {
      isPopstateRef.current = true;
      const s = e.state;
      if (!s || s.view === 'tree') {
        dispatch({ type: 'NAVIGATE_TO_TREE' });
      } else if (s.view === 'category') {
        dispatch({ type: 'NAVIGATE_TO_CATEGORY', category: s.category });
      } else if (s.view === 'innovation-zone') {
        dispatch({ type: 'NAVIGATE_TO_INNOVATION_ZONE' });
      } else if (s.view === 'dashboard') {
        dispatch({ type: 'NAVIGATE_TO_DASHBOARD' });
      } else if (s.view === 'learning-paths') {
        dispatch({ type: 'NAVIGATE_TO_LEARNING_PATHS' });
      } else if (s.view === 'my-journey') {
        dispatch({ type: 'NAVIGATE_TO_JOURNEY' });
      } else if (s.view === 'gamification-hub') {
        dispatch({ type: 'NAVIGATE_TO_GAMIFICATION_HUB' });
      } else if (s.view === 'study-session') {
        dispatch({ type: 'NAVIGATE_TO_STUDY_SESSION' });
      } else if (s.view === 'insights') {
        dispatch({ type: 'NAVIGATE_TO_INSIGHTS' });
      } else if (s.view === 'module') {
        dispatch({ type: 'NAVIGATE_TO_MODULE', moduleId: s.moduleId, category: s.category || null, fromJourney: s.fromJourney || false });
      }
      window.scrollTo(0, 0);
      isPopstateRef.current = false;
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Convenience navigation functions that push history
  const pushHistory = useCallback((view: string, extra?: Record<string, any>) => {
    if (!isPopstateRef.current) {
      window.history.pushState({ view, ...extra }, '');
    }
  }, []);

  const navigateToTree = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_TREE' });
    window.scrollTo(0, 0);
    pushHistory('tree');
  }, [pushHistory]);

  const navigateToCategory = useCallback((category: CategoryType) => {
    dispatch({ type: 'NAVIGATE_TO_CATEGORY', category });
    window.scrollTo(0, 0);
    pushHistory('category', { category });
  }, [pushHistory]);

  const navigateToModule = useCallback((moduleId: string, currentViewState?: ViewState, currentCategory?: CategoryType | null) => {
    const fromJourney = currentViewState === 'innovation-zone';
    dispatch({ type: 'NAVIGATE_TO_MODULE', moduleId, fromJourney, category: currentCategory });
    window.scrollTo(0, 0);
    pushHistory('module', { moduleId, category: currentCategory, fromJourney });
  }, [pushHistory]);

  const navigateToInnovationZone = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_INNOVATION_ZONE' });
    window.scrollTo(0, 0);
    pushHistory('innovation-zone');
  }, [pushHistory]);

  const navigateToDashboard = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_DASHBOARD' });
    window.scrollTo(0, 0);
    pushHistory('dashboard');
  }, [pushHistory]);

  const navigateToLearningPaths = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_LEARNING_PATHS' });
    window.scrollTo(0, 0);
    pushHistory('learning-paths');
  }, [pushHistory]);

  const navigateToJourney = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_JOURNEY' });
    window.scrollTo(0, 0);
    pushHistory('my-journey');
  }, [pushHistory]);

  const navigateToGamificationHub = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_GAMIFICATION_HUB' });
    window.scrollTo(0, 0);
    pushHistory('gamification-hub');
  }, [pushHistory]);

  const navigateToStudySession = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_STUDY_SESSION' });
    window.scrollTo(0, 0);
    pushHistory('study-session');
  }, [pushHistory]);

  const navigateToInsights = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_INSIGHTS' });
    window.scrollTo(0, 0);
    pushHistory('insights');
  }, [pushHistory]);

  const navigateToOnboarding = useCallback(() => {
    dispatch({ type: 'NAVIGATE_TO_ONBOARDING' });
  }, []);

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
    goBack,
  };

  return <NavigationContext.Provider value={value}>{children}</NavigationContext.Provider>;
};

export default NavigationContext;
