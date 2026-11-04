import { describe, expect, it } from 'vitest';
import { readAuthActionLink } from '../utils/authActionLink';

const at = (url: string) => {
  const { pathname, search } = new URL(url, 'https://nextstepuni-app.web.app');
  return readAuthActionLink({ pathname, search });
};

describe('readAuthActionLink', () => {
  it.each(['resetPassword', 'verifyEmail', 'recoverEmail', 'verifyAndChangeEmail'])(
    'reads a %s link on the configured action path',
    (mode) => {
      expect(at(`/reset-password?mode=${mode}&oobCode=abc&apiKey=k&lang=en`)).toEqual({ mode, oobCode: 'abc' });
    },
  );

  it('reads an action link on the app root when it carries a known mode and a code', () => {
    expect(at('/?mode=verifyEmail&oobCode=abc')).toEqual({ mode: 'verifyEmail', oobCode: 'abc' });
  });

  it('still claims a malformed link on the action path, so it can be explained', () => {
    expect(at('/reset-password')).toEqual({ mode: null, oobCode: null });
    expect(at('/reset-password?mode=somethingNew&oobCode=abc')).toEqual({ mode: 'somethingNew', oobCode: 'abc' });
  });

  it('leaves ordinary app URLs alone', () => {
    expect(at('/')).toBeNull();
    expect(at('/?view=dashboard&section=progress')).toBeNull();
    expect(at('/?mode=verifyEmail')).toBeNull();
    expect(at('/?mode=somethingElse&oobCode=abc')).toBeNull();
  });
});
