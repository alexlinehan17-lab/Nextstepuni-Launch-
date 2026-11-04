
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';
import ReactDOM from 'react-dom/client';
import { Capacitor } from '@capacitor/core';
import { StatusBar, Style } from '@capacitor/status-bar';
import './index.css';
import './native-ios.css';
import { MotionConfig } from 'framer-motion';
import App from './App';
import IllustrationTheme from './components/IllustrationTheme';
import ErrorBoundary from './components/ErrorBoundary';
import { ToastProvider } from './components/Toast';
import { AuthProvider } from './contexts/AuthContext';
import { NavigationProvider } from './contexts/NavigationContext';
import { ProgressProvider } from './contexts/ProgressContext';

// Keep native chrome in step with the web theme. Settings updates the `dark`
// class directly on <html>, so observing that class also covers theme changes
// made after React has mounted (and the persisted preference loaded).
if (Capacitor.isNativePlatform()) {
  if (Capacitor.getPlatform() === 'ios') document.documentElement.classList.add('native-ios');
  // The web app owns safe-area padding. Let its background reach
  // behind the status bar instead of creating the plugin's default black strip.
  StatusBar.setOverlaysWebView({ overlay: Capacitor.getPlatform() === 'ios' }).catch(() => {});

  const syncNativeStatusBar = () => {
    const appearance = document.documentElement.dataset.nativeStatusBarAppearance;
    const isDark = appearance ? appearance === 'dark' : document.documentElement.classList.contains('dark');
    // Capacitor names these after the background: Dark uses light text.
    StatusBar.setStyle({ style: isDark ? Style.Dark : Style.Light }).catch(() => {});
  };

  syncNativeStatusBar();
  new MutationObserver(syncNativeStatusBar).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class', 'data-native-status-bar-appearance'],
  });
}

// Register the PWA service worker for web/offline only. NEVER in the Capacitor
// native shell: its navigateFallback can serve a stale or white screen inside
// the WebView. vite-plugin-pwa is configured with injectRegister:false so this
// is the single registration site. (audit 2026-06-01, item 12)
if (!Capacitor.isNativePlatform()) {
  // @ts-expect-error — virtual module provided by vite-plugin-pwa at build time
  import('virtual:pwa-register')
    .then(({ registerSW }) => registerSW({
      immediate: true,
      onRegisteredSW: (_workerUrl, registration) => {
        if (!registration) return;

        // Calling register() alone may reuse the browser's recent soft-update
        // result for up to 24 hours. Check explicitly at launch so an open PWA
        // cannot keep booting yesterday's hashed app shell after a deployment.
        // Keep long-running study tabs current as well.
        const checkForUpdate = () => registration.update().catch(() => {});
        void checkForUpdate();
        window.setInterval(checkForUpdate, 60 * 60 * 1000);
      },
    }))
    .catch(() => {});
}

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <IllustrationTheme />
    <ErrorBoundary>
      <ToastProvider>
        <AuthProvider>
          <ProgressProvider>
            <NavigationProvider>
              <MotionConfig reducedMotion="user">
                <App />
              </MotionConfig>
            </NavigationProvider>
          </ProgressProvider>
        </AuthProvider>
      </ToastProvider>
    </ErrorBoundary>
  </React.StrictMode>
);
