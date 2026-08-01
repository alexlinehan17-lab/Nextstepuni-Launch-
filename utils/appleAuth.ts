/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One place that turns a native Sign in with Apple authorization into a Firebase
 * credential. Both the sign-IN path (LoginPage) and the re-authentication path
 * (DataRightsModal, before account deletion) need the identical nonce dance, and
 * a second hand-rolled copy of it is exactly how the two drift apart.
 *
 * Apple embeds the SHA-256 HASH of the nonce in the identity token; Firebase
 * verifies that hash against the RAW nonce. Hand Firebase the hashed one and the
 * exchange fails with an opaque error, so the pairing lives here rather than at
 * each call site.
 */

import { OAuthProvider, type OAuthCredential } from 'firebase/auth';
import { SignInWithApple, type AppleAuthorizeResult } from './signInWithApple';

const generateNonce = (length = 32): string => {
  const charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-._';
  const bytes = new Uint8Array(length);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => charset[b % charset.length]).join('');
};

const sha256Hex = async (input: string): Promise<string> => {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input));
  return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, '0')).join('');
};

/**
 * Run the native Apple authorization and build the Firebase credential from it.
 *
 * Returns the raw Apple result alongside the credential because Apple hands back
 * the user's name ONLY on the first authorization for a given Apple ID — the
 * sign-in path needs it to seed the profile, and it is gone forever afterwards.
 *
 * Throws if Apple returns no identity token (user cancelled, or the capability
 * is not enabled on the App ID).
 */
export async function authorizeWithApple(): Promise<{
  credential: OAuthCredential;
  result: AppleAuthorizeResult;
}> {
  const rawNonce = generateNonce();
  const hashedNonce = await sha256Hex(rawNonce);
  const result = await SignInWithApple.authorize({ nonce: hashedNonce });
  if (!result.identityToken) {
    throw new Error('Apple sign-in did not return an identity token.');
  }
  const provider = new OAuthProvider('apple.com');
  const credential = provider.credential({ idToken: result.identityToken, rawNonce });
  return { credential, result };
}
