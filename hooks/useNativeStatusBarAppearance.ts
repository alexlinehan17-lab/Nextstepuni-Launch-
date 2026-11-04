import { useLayoutEffect } from 'react';

/** Full-screen experiences can own a palette independently of account settings. */
export function useNativeStatusBarAppearance(appearance: 'light' | 'dark') {
  useLayoutEffect(() => {
    const root = document.documentElement;
    if (!root.classList.contains('native-ios')) return;
    const previous = root.dataset.nativeStatusBarAppearance;
    root.dataset.nativeStatusBarAppearance = appearance;
    return () => {
      if (previous === undefined) delete root.dataset.nativeStatusBarAppearance;
      else root.dataset.nativeStatusBarAppearance = previous;
    };
  }, [appearance]);
}
