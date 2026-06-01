
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';
import ReactDOM from 'react-dom/client';
import { Capacitor } from '@capacitor/core';
import { StatusBar, Style } from '@capacitor/status-bar';
import './index.css';
import App from './App';
import ErrorBoundary from './components/ErrorBoundary';
import PullToRefresh from './components/PullToRefresh';
import { ToastProvider } from './components/Toast';
import { AuthProvider } from './contexts/AuthContext';
import { NavigationProvider } from './contexts/NavigationContext';
import { ProgressProvider } from './contexts/ProgressContext';

// Configure the native status bar so the web view doesn't extend underneath it.
// `setOverlaysWebView({ overlay: false })` pushes our content below the clock /
// dynamic island, and `Style.Dark` keeps the status bar icons readable against
// our light cream background.
if (Capacitor.isNativePlatform()) {
  StatusBar.setOverlaysWebView({ overlay: false }).catch(() => {});
  StatusBar.setStyle({ style: Style.Dark }).catch(() => {});
}

// Register the PWA service worker for web/offline only. NEVER in the Capacitor
// native shell: its navigateFallback can serve a stale or white screen inside
// the WebView. vite-plugin-pwa is configured with injectRegister:false so this
// is the single registration site. (audit 2026-06-01, item 12)
if (!Capacitor.isNativePlatform()) {
  // @ts-ignore — virtual module provided by vite-plugin-pwa at build time
  import('virtual:pwa-register')
    .then(({ registerSW }) => registerSW({ immediate: true }))
    .catch(() => {});
}

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <ToastProvider>
        <AuthProvider>
          <ProgressProvider>
            <NavigationProvider>
              <PullToRefresh>
                <App />
              </PullToRefresh>
            </NavigationProvider>
          </ProgressProvider>
        </AuthProvider>
      </ToastProvider>
    </ErrorBoundary>
  </React.StrictMode>
);