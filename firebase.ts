
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore, enableIndexedDbPersistence } from "firebase/firestore";

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

// Export the necessary Firebase services to be used throughout the app
export const auth = getAuth(app);
export const db = getFirestore(app);

// Enable offline persistence for Firestore
enableIndexedDbPersistence(db).catch((err) => {
  if (err.code === 'failed-precondition') {
    console.warn('Firestore persistence unavailable: multiple tabs open');
  } else if (err.code === 'unimplemented') {
    console.warn('Firestore persistence unavailable: browser not supported');
  }
});

export default app;