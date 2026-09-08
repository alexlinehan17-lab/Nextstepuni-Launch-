/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Dive in" — the page after a guest finishes onboarding without an account.
 *
 * A placeholder, deliberately. It says plainly that accounts and payment open
 * at launch (September 2027) and offers the two things a visitor can actually
 * do today: go and create an account on the existing sign-up path, or go back
 * to the landing page. No payment UI, no prices: none of that exists yet and
 * a mock of it would be a promise the product has not made.
 *
 * DECISION PENDING (do not resolve here): whether the account is created
 * BEFORE payment (sign up free, pay to unlock) or AFTER it (pay, then the
 * account is provisioned) is undecided. "Create your account" below is the
 * existing sign-up path either way; when the order is decided, this page is
 * the one that changes — the guest draft it leaves behind is order-agnostic.
 */

import React from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { MotionDiv } from './Motion';
import { CREATE_ACCOUNT_URL, LANDING_PAGE_URL } from './onboarding/guest';

export const LAUNCH_WINDOW = 'September 2027';

interface DiveInProps {
  /** Fired before the browser follows the sign-up link; end the guest phase, keep the draft. */
  onCreateAccount?: () => void;
  /** Fired before the browser goes back to the landing page. */
  onBackToLanding?: () => void;
}

const DiveIn: React.FC<DiveInProps> = ({ onCreateAccount, onBackToLanding }) => (
  <div className="theme-compat fixed inset-0 z-[60] overflow-y-auto bg-white dark:bg-zinc-950">
    <main className="mx-auto flex min-h-full w-full max-w-xl flex-col justify-center px-7 py-12 sm:px-6">
      <MotionDiv
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
      >
        <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[#8D857E] dark:text-zinc-500">
          Setup finished · Nextstepuni
        </p>
        <h1 className="mt-4 font-serif text-4xl font-bold leading-[1.02] tracking-tight text-[#1A1A1A] sm:text-5xl dark:text-white">
          You&rsquo;re set up.<br />The doors open at launch.
        </h1>
        <div className="mt-8 border-t border-[#1A1A1A]/15 pt-6 dark:border-white/15">
          <p className="text-[17px] leading-relaxed text-[#1A1A1A] dark:text-zinc-100">
            Accounts and payment open at launch, in <strong className="font-semibold">{LAUNCH_WINDOW}</strong>.
            Nothing you answered has been sent anywhere: your setup is kept in this browser tab only, and nothing was saved to a server.
          </p>
          <p className="mt-4 text-[15px] leading-relaxed text-[#78716C] dark:text-zinc-400">
            Until then, there is nothing to pay and no card to add. If you would rather have an account ready, you can create one now.
          </p>
        </div>

        <div className="mt-10 flex flex-col items-start gap-5">
          <a
            href={CREATE_ACCOUNT_URL}
            onClick={onCreateAccount}
            className="inline-flex min-h-12 items-center gap-2.5 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] px-8 py-3 font-sans text-[15px] font-semibold text-white shadow-[4px_4px_0_0_#1A1A1A] transition-all duration-150 hover:-translate-y-0.5 hover:shadow-[6px_6px_0_0_#1A1A1A] active:translate-x-1 active:translate-y-1 active:shadow-none"
          >
            Create your account
            <ArrowRight size={16} aria-hidden="true" />
          </a>
          <a
            href={LANDING_PAGE_URL}
            onClick={onBackToLanding}
            className="inline-flex items-center gap-1.5 border-b-[1.5px] border-[#1A1A1A] pb-0.5 font-sans text-[15px] font-semibold text-[#1A1A1A] transition-colors hover:text-[#B84A0C] hover:border-[#B84A0C] dark:border-zinc-200 dark:text-zinc-100"
          >
            <ArrowLeft size={15} aria-hidden="true" />
            Back to the landing page
          </a>
        </div>
      </MotionDiv>
    </main>
  </div>
);

export default DiveIn;
