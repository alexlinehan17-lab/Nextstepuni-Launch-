
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { initializeApp } from "firebase/app";
import { initializeAuth, indexedDBLocalPersistence } from "firebase/auth";
import { initializeFirestore, persistentLocalCache, persistentMultipleTabManager } from "firebase/firestore";

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

// Export the necessary Firebase services to be used throughout the app.
//
// We use `initializeAuth` with `indexedDBLocalPersistence` instead of the
// default `getAuth(app)` so the Auth SDK skips loading the gapi.iframes
// OAuth helper from apis.google.com. Inside Capacitor's WKWebView the
// origin is `capacitor://localhost`, which fails CORS against that helper
// and causes `onAuthStateChanged` to hang forever. IndexedDB persistence
// also works fine in normal browsers, so the same config is used everywhere.
export const auth = initializeAuth(app, {
  persistence: indexedDBLocalPersistence,
});
export const db = initializeFirestore(app, {
  localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() }),
});

export default app;
