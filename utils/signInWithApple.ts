/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { registerPlugin } from '@capacitor/core';

export interface AppleAuthorizeOptions {
  /** SHA-256 hash of the raw nonce. Apple embeds it in the identity token;
   *  Firebase verifies it against the raw nonce on the JS side. */
  nonce?: string;
}

export interface AppleAuthorizeResult {
  identityToken: string;
  /** Present only on the FIRST authorization for a given Apple ID. */
  givenName?: string;
  familyName?: string;
  email?: string;
  /** Apple's stable user identifier (the `sub` claim). */
  user?: string;
}

export interface SignInWithApplePlugin {
  authorize(options: AppleAuthorizeOptions): Promise<AppleAuthorizeResult>;
}

// Bridges to the native SignInWithApplePlugin
// (ios/App/App/SignInWithApplePlugin.swift), which uses Apple's system
// AuthenticationServices framework — no third-party SDK is bundled. Native-only;
// not called on the web (the welcome/login UI gates the button on isNativePlatform).
export const SignInWithApple = registerPlugin<SignInWithApplePlugin>('SignInWithApple');
