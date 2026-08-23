/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { FirebaseAppCheck } from '@capacitor-firebase/app-check';
import { Capacitor } from '@capacitor/core';
import type { FirebaseApp } from 'firebase/app';
import {
  CustomProvider,
  initializeAppCheck,
  ReCaptchaEnterpriseProvider,
  type AppCheck,
} from 'firebase/app-check';

/**
 * Register App Check before any Firebase service starts making requests.
 *
 * The web build uses reCAPTCHA Enterprise. Native builds obtain a platform
 * attestation from App Attest or Play Integrity through the Capacitor plugin,
 * then bridge that token into the Firebase JavaScript SDK. This keeps Auth,
 * Firestore and callable Functions on the same attested Firebase app.
 */
export function configureFirebaseAppCheck(
  app: FirebaseApp,
  webSiteKey?: string,
): AppCheck | undefined {
  if (Capacitor.isNativePlatform()) {
    let initializationError: unknown;
    const nativeInitialization = FirebaseAppCheck.initialize({
      isTokenAutoRefreshEnabled: true,
    }).catch((error: unknown) => {
      // Handle the promise immediately so a native configuration failure never
      // becomes an unhandled rejection. The token request still fails closed.
      initializationError = error;
    });

    return initializeAppCheck(app, {
      provider: new CustomProvider({
        getToken: async () => {
          await nativeInitialization;
          if (initializationError) throw initializationError;

          const { token, expireTimeMillis } = await FirebaseAppCheck.getToken({
            forceRefresh: false,
          });
          if (
            !token
            || typeof expireTimeMillis !== 'number'
            || !Number.isFinite(expireTimeMillis)
            || expireTimeMillis <= Date.now()
          ) {
            throw new Error('Native App Check returned an invalid token.');
          }
          return { token, expireTimeMillis };
        },
      }),
      isTokenAutoRefreshEnabled: true,
    });
  }

  if (!webSiteKey) return undefined;

  return initializeAppCheck(app, {
    provider: new ReCaptchaEnterpriseProvider(webSiteKey),
    isTokenAutoRefreshEnabled: true,
  });
}
