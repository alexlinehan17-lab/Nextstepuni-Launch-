
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { initializeApp } from "firebase/app";
import { initializeAuth, browserSessionPersistence, indexedDBLocalPersistence } from "firebase/auth";
import { initializeFirestore, memoryLocalCache } from "firebase/firestore";
import { initializeAppCheck, ReCaptchaEnterpriseProvider } from "firebase/app-check";
import { Capacitor } from "@capacitor/core";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCoNBVVlJifQ_n3Pf1P1BA9QalOOcK0kNA",
  authDomain: "nextstepuni-app.firebaseapp.com",
  projectId: "nextstepuni-app",
  storageBucket: "nextstepuni-app.firebasestorage.app",
  messagingSenderId: "52864318610",
  appId: "1:52864318610:web:24f445c78a71f215c2ba4b",
  measurementId: "G-PJYB9DN2C9"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// App Check is activated when the console-provisioned Enterprise site key is
// supplied at build time. Cloud Functions enforcement is independently gated
// by ENFORCE_APP_CHECK so providers can be rolled out and observed before the
// backend begins rejecting unattested clients.
const appCheckSiteKey = (import.meta as unknown as {
  env?: Record<string, string | undefined>;
}).env?.VITE_FIREBASE_APPCHECK_SITE_KEY;
if (!Capacitor.isNativePlatform() && appCheckSiteKey) {
  initializeAppCheck(app, {
    provider: new ReCaptchaEnterpriseProvider(appCheckSiteKey),
    isTokenAutoRefreshEnabled: true,
  });
}

// Export the necessary Firebase services to be used throughout the app.
//
// We use `initializeAuth` instead of the default `getAuth(app)` so the Auth
// SDK skips loading the gapi.iframes OAuth helper from apis.google.com. Inside
// Capacitor's WKWebView the `capacitor://localhost` origin fails CORS against
// that helper and can leave `onAuthStateChanged` waiting indefinitely.
export const auth = initializeAuth(app, {
  // Web sessions end with the browser session, which is safer on shared school
  // computers. Native apps retain sign-in in their private app sandbox.
  persistence: Capacitor.isNativePlatform() ? indexedDBLocalPersistence : browserSessionPersistence,
});
export const db = initializeFirestore(app, {
  // Do not put student records in a durable browser-wide Firestore cache. The
  // app's explicit, non-sensitive PDF cache remains available for offline use.
  localCache: memoryLocalCache(),
});

export default app;
