/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { beforeEach, describe, expect, test, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  isNative: false,
  initializeAppCheck: vi.fn(),
  nativeInitialize: vi.fn(),
  nativeGetToken: vi.fn(),
}));

vi.mock('@capacitor/core', () => ({
  Capacitor: {
    isNativePlatform: () => mocks.isNative,
  },
}));

vi.mock('@capacitor-firebase/app-check', () => ({
  FirebaseAppCheck: {
    initialize: mocks.nativeInitialize,
    getToken: mocks.nativeGetToken,
  },
}));

vi.mock('firebase/app-check', () => {
  class CustomProvider {
    readonly options: { getToken: () => Promise<{ token: string; expireTimeMillis: number }> };

    constructor(options: CustomProvider['options']) {
      this.options = options;
    }
  }

  class ReCaptchaEnterpriseProvider {
    constructor(readonly siteKey: string) {}
  }

  return {
    CustomProvider,
    ReCaptchaEnterpriseProvider,
    initializeAppCheck: mocks.initializeAppCheck,
  };
});

import { configureFirebaseAppCheck } from '@/firebaseAppCheck';

describe('Firebase App Check configuration', () => {
  beforeEach(() => {
    mocks.isNative = false;
    mocks.initializeAppCheck.mockReset().mockReturnValue({ configured: true });
    mocks.nativeInitialize.mockReset().mockResolvedValue(undefined);
    mocks.nativeGetToken.mockReset().mockResolvedValue({
      token: 'native-token',
      expireTimeMillis: Date.now() + 60_000,
    });
  });

  test('does not initialize the web provider without a configured site key', () => {
    expect(configureFirebaseAppCheck({} as never)).toBeUndefined();
    expect(mocks.initializeAppCheck).not.toHaveBeenCalled();
    expect(mocks.nativeInitialize).not.toHaveBeenCalled();
  });

  test('uses reCAPTCHA Enterprise for the web build', () => {
    configureFirebaseAppCheck({} as never, 'site-key');

    const options = mocks.initializeAppCheck.mock.calls[0]?.[1] as {
      provider: { siteKey: string };
      isTokenAutoRefreshEnabled: boolean;
    };
    expect(options.provider.siteKey).toBe('site-key');
    expect(options.isTokenAutoRefreshEnabled).toBe(true);
    expect(mocks.nativeInitialize).not.toHaveBeenCalled();
  });

  test('bridges a native attestation token into the Firebase JavaScript SDK', async () => {
    mocks.isNative = true;
    configureFirebaseAppCheck({} as never, 'unused-web-key');

    expect(mocks.nativeInitialize).toHaveBeenCalledWith({
      isTokenAutoRefreshEnabled: true,
    });
    const options = mocks.initializeAppCheck.mock.calls[0]?.[1] as {
      provider: { options: { getToken: () => Promise<unknown> } };
      isTokenAutoRefreshEnabled: boolean;
    };
    await expect(options.provider.options.getToken()).resolves.toMatchObject({
      token: 'native-token',
    });
    expect(mocks.nativeGetToken).toHaveBeenCalledWith({ forceRefresh: false });
    expect(options.isTokenAutoRefreshEnabled).toBe(true);
  });

  test('fails closed when the native provider returns no usable expiry', async () => {
    mocks.isNative = true;
    mocks.nativeGetToken.mockResolvedValue({ token: 'native-token' });
    configureFirebaseAppCheck({} as never);

    const options = mocks.initializeAppCheck.mock.calls[0]?.[1] as {
      provider: { options: { getToken: () => Promise<unknown> } };
    };
    await expect(options.provider.options.getToken()).rejects.toThrow(
      'Native App Check returned an invalid token.',
    );
  });

  test('fails closed when the native provider cannot initialize', async () => {
    mocks.isNative = true;
    mocks.nativeInitialize.mockRejectedValue(new Error('attestation unavailable'));
    configureFirebaseAppCheck({} as never);

    const options = mocks.initializeAppCheck.mock.calls[0]?.[1] as {
      provider: { options: { getToken: () => Promise<unknown> } };
    };
    await expect(options.provider.options.getToken()).rejects.toThrow(
      'attestation unavailable',
    );
    expect(mocks.nativeGetToken).not.toHaveBeenCalled();
  });
});
