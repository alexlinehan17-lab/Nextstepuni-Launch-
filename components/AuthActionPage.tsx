/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * AuthActionPage — where every Firebase Auth email link lands.
 *
 * Firebase sends password reset, email confirmation and email recovery links
 * to one configured URL (/reset-password). Until 2026-10-12 all of them
 * rendered the password-reset form, so a student who tapped "Verify your
 * email" was asked to set a new password, and only 1 of the 139 accounts
 * created in September and October 2026 ever confirmed its email. Dispatch
 * on `mode` instead.
 */

import React, { useEffect, useState } from 'react';
import { applyActionCode, checkActionCode } from 'firebase/auth';
import { auth } from '../firebase';
import { readAuthActionLink } from '../utils/authActionLink';
import ResetPasswordPage from './ResetPasswordPage';
import {
  AuthActionCard,
  AuthActionProblem,
  AuthActionProgress,
  AuthActionSuccess,
} from './AuthActionCard';

type Outcome =
  | { kind: 'done'; title: string; message: string }
  | { kind: 'problem'; title: string; message: string };

const errorCode = (err: unknown) => (err as { code?: string } | null)?.code ?? '';

const LINK_PROBLEM = 'This link doesn’t work';

// A code is one-use: applying it twice (React StrictMode runs effects twice in
// development) would report the second attempt as "already used". Every mount
// for the same code shares one attempt.
const attempts = new Map<string, Promise<Outcome>>();

async function confirmEmail(oobCode: string): Promise<Outcome> {
  try {
    await applyActionCode(auth, oobCode);
    return {
      kind: 'done',
      title: 'Email confirmed',
      message: 'Thanks. Your email address is confirmed. You can sign in now.',
    };
  } catch (err) {
    const code = errorCode(err);
    if (code === 'auth/expired-action-code') {
      return {
        kind: 'problem',
        title: 'This link has expired',
        message: 'Confirmation links only last a short while. Your account still works, so you can sign in as normal.',
      };
    }
    if (code === 'auth/invalid-action-code') {
      return {
        kind: 'problem',
        title: LINK_PROBLEM,
        message: 'This confirmation link has already been used or is no longer valid. If you already confirmed your email, there is nothing else to do. You can sign in as normal.',
      };
    }
    return {
      kind: 'problem',
      title: LINK_PROBLEM,
      message: 'We could not confirm your email just now. Check your connection, then open the link from the email again.',
    };
  }
}

async function confirmNewEmail(oobCode: string): Promise<Outcome> {
  try {
    await applyActionCode(auth, oobCode);
    return {
      kind: 'done',
      title: 'New email confirmed',
      message: 'Use your new email address the next time you sign in.',
    };
  } catch (err) {
    return {
      kind: 'problem',
      title: LINK_PROBLEM,
      message: errorCode(err) === 'auth/expired-action-code'
        ? 'This confirmation link has expired. Your sign-in email has not changed.'
        : 'This confirmation link has already been used or is no longer valid. Your sign-in email has not changed.',
    };
  }
}

async function recoverEmail(oobCode: string): Promise<Outcome> {
  try {
    const info = await checkActionCode(auth, oobCode);
    await applyActionCode(auth, oobCode);
    const restored = info.data.email;
    return {
      kind: 'done',
      title: 'Email address restored',
      message: restored
        ? `Your sign-in email is ${restored} again. If you did not ask for the change, reset your password from the sign-in page.`
        : 'Your previous sign-in email is restored. If you did not ask for the change, reset your password from the sign-in page.',
    };
  } catch (err) {
    return {
      kind: 'problem',
      title: LINK_PROBLEM,
      message: errorCode(err) === 'auth/expired-action-code'
        ? 'This link has expired. If your sign-in email was changed without your permission, contact nextstepuniinfo@gmail.com.'
        : 'This link has already been used or is no longer valid. If your sign-in email was changed without your permission, contact nextstepuniinfo@gmail.com.',
    };
  }
}

function runAction(mode: string, oobCode: string): Promise<Outcome> {
  const key = `${mode}:${oobCode}`;
  let attempt = attempts.get(key);
  if (!attempt) {
    attempt = mode === 'verifyEmail'
      ? confirmEmail(oobCode)
      : mode === 'verifyAndChangeEmail'
        ? confirmNewEmail(oobCode)
        : recoverEmail(oobCode);
    attempts.set(key, attempt);
  }
  return attempt;
}

const HANDLED = new Set(['verifyEmail', 'verifyAndChangeEmail', 'recoverEmail']);

const PROGRESS_LABEL: Record<string, string> = {
  verifyEmail: 'Confirming your email…',
  verifyAndChangeEmail: 'Confirming your new email…',
  recoverEmail: 'Restoring your email address…',
};

const EmailActionPage: React.FC<{ mode: string | null; oobCode: string | null }> = ({ mode, oobCode }) => {
  const runnable = Boolean(mode && oobCode && HANDLED.has(mode));
  const [outcome, setOutcome] = useState<Outcome | null>(() => {
    if (runnable) return null;
    if (!oobCode) {
      return {
        kind: 'problem',
        title: LINK_PROBLEM,
        message: 'This link is missing some information. Open it again from the email, or copy the whole link into your browser.',
      };
    }
    return {
      kind: 'problem',
      title: LINK_PROBLEM,
      message: 'This kind of link is not used by NextStepUni. Open the most recent email from us, or go back to sign in.',
    };
  });

  useEffect(() => {
    if (!runnable || !mode || !oobCode) return;
    let active = true;
    void runAction(mode, oobCode).then(result => { if (active) setOutcome(result); });
    return () => { active = false; };
  }, [runnable, mode, oobCode]);

  return (
    <AuthActionCard>
      {!outcome && <AuthActionProgress label={PROGRESS_LABEL[mode ?? ''] ?? 'Opening your link…'} />}
      {outcome?.kind === 'done' && <AuthActionSuccess title={outcome.title} message={outcome.message} />}
      {outcome?.kind === 'problem' && <AuthActionProblem title={outcome.title} message={outcome.message} />}
    </AuthActionCard>
  );
};

const AuthActionPage: React.FC = () => {
  const link = readAuthActionLink(window.location) ?? { mode: null, oobCode: null };
  // Links issued before `mode` existed carried only a reset code.
  const mode = link.mode ?? (link.oobCode ? 'resetPassword' : null);
  if (mode === 'resetPassword') return <ResetPasswordPage />;
  return <EmailActionPage mode={mode} oobCode={link.oobCode} />;
};

export default AuthActionPage;
