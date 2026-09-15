import React, { useLayoutEffect, useRef, useState } from 'react';
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import { MotionDiv } from './Motion';
import Avatar from './Avatar';
import { WelcomeCharacter } from './WelcomeCharacter';
import { getAvatarName } from '../data/personalStarCrew';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';

export const AuthWordmark = () => (
  <span className="font-sans text-[26px] font-bold leading-none tracking-[-0.03em]">nextstepuni</span>
);

function WelcomeArtworkPanel() {
  return <div className="auth-paper-story hidden md:flex md:flex-col w-1/2 relative">
    <div className="flex items-center gap-3">
      <div style={{ color: '#1a1a1a' }}><AuthWordmark /></div>
      <div style={{ flex: 1, height: 1, backgroundColor: 'rgba(26,26,26,0.12)' }} />
    </div>
    <div className="flex-1 flex flex-col items-center justify-center text-center">
      <WelcomeCharacter />
      <h2 className="auth-paper-caption">Built around how you learn.</h2>
      <p className="auth-paper-caption-detail">Personalised study, examiner-grounded.</p>
    </div>
  </div>;
}

function RegistrationStory({ step, avatar, name }: { step: number; avatar: string; name: string }) {
  const reducedMotion = useReducedMotion();
  const transition = { duration: reducedMotion ? 0 : 0.24, ease: 'easeOut' };
  return <aside className="auth-registration-story">
    <AnimatePresence mode="wait" initial={false}>
      <MotionDiv key={step} className="auth-registration-story-content"
        initial={{ opacity: 0, y: reducedMotion ? 0 : 10 }} animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: reducedMotion ? 0 : -8 }} transition={transition}>
        <p className="auth-paper-eyebrow">{step === 3 ? 'Your account. Your character.' : step === 2 ? 'Make yourself at home.' : 'Let’s make it personal.'}</p>
        <h2>{step === 3 ? <>A little<br />more<br /><em>you.</em></> : step === 2 ? <>A space<br />of your<br /><em>own.</em></> : <>Your next<br /><em>chapter.</em></>}</h2>
        <p className="auth-registration-story-copy">{step === 3 ? 'Pick the one that feels like you. They’ll be right here as you find your way.' : step === 2 ? 'Your subjects, your progress, your plans. One place to make them yours.' : 'A few details to get started. Then we’ll make room for your subjects, your goals and you.'}</p>
        {step === 3 ? <div className="auth-crew-selected">
          <AnimatePresence mode="wait" initial={false}>
            <MotionDiv key={avatar} className="auth-crew-selected-inner"
              initial={{ opacity: 0, y: reducedMotion ? 0 : 6 }} animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: reducedMotion ? 0 : -4 }} transition={{ ...transition, duration: reducedMotion ? 0 : 0.14 }}>
              <Avatar seed={avatar} alt="" className="auth-crew-portrait" />
              <div><h3>{getAvatarName(avatar)}</h3><p>{name.trim().split(/\s+/)[0] || 'Your'}{name.trim() ? '’s' : ''} Star Crew character</p></div>
            </MotionDiv>
          </AnimatePresence>
        </div> : <Avatar seed={step === 1 ? 'star-crew:reader' : 'star-crew:hugger'} alt="" className="auth-registration-illustration" />}
      </MotionDiv>
    </AnimatePresence>
  </aside>;
}

interface AccountCardProps {
  children: React.ReactNode;
  devButton?: React.ReactNode;
  view: string;
  registerStep: number;
  avatar: string;
  name: string;
  onRegistrationBack: () => void;
}

export default function AccountCard({ children, devButton, view, registerStep, avatar, name, onRegistrationBack }: AccountCardProps) {
  const mobileAppDesign = useMobileAppDesign();
  const reducedMotion = useReducedMotion();
  const registering = view === 'register';
  const contentRef = useRef<HTMLDivElement>(null);
  const [cardHeight, setCardHeight] = useState<number>();
  const [desktop, setDesktop] = useState(false);

  // Animate the box's real height so the text and artwork never stretch. The
  // inner content remains naturally sized, including errors and text zoom.
  // Phones retain normal document flow for scrolling with the keyboard open.
  useLayoutEffect(() => {
    const media = window.matchMedia('(min-width: 768px)');
    const updateViewport = () => setDesktop(media.matches);
    updateViewport();
    media.addEventListener('change', updateViewport);
    const measure = () => {
      const content = contentRef.current;
      const height = content?.getBoundingClientRect().height;
      if (height && content?.parentElement) {
        const style = getComputedStyle(content.parentElement);
        setCardHeight(Math.ceil(height + parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth)));
      }
    };
    measure();
    const observer = new ResizeObserver(measure);
    if (contentRef.current) observer.observe(contentRef.current);
    return () => { observer.disconnect(); media.removeEventListener('change', updateViewport); };
  }, []);

  return <div data-view={view} className={`auth-paper ${mobileAppDesign ? 'account-entry' : 'theme-compat'} relative flex min-h-[100dvh] flex-col items-center justify-center overflow-x-hidden bg-[var(--surface-canvas)] [overflow-anchor:none] md:min-h-screen md:p-8`}>
    <MotionDiv initial={{ opacity: 0, y: reducedMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0, height: desktop && cardHeight ? cardHeight : 'auto' }}
      transition={{ duration: reducedMotion ? 0 : 0.55, ease: [0.22, 1, 0.36, 1] }}
      className="account-card auth-adaptive-card w-full">
      <div ref={contentRef}>
        {registering && <header className="auth-registration-header">
          <AuthWordmark />
          <div>
            <button type="button" className="auth-registration-back" onClick={onRegistrationBack}><ArrowLeft size={15} aria-hidden="true" /> Back</button>
            <span className="auth-registration-tagline">A beginning, built around you.</span>
            <span role="status" aria-label={`Account creation, step ${registerStep} of 3`}>0{registerStep} / 03</span>
          </div>
        </header>}
        <div className="auth-card-body">
          {registering ? <RegistrationStory step={registerStep} avatar={avatar} name={name} /> : <WelcomeArtworkPanel />}
          <div className="account-form flex w-full flex-1 flex-col justify-start px-5 pb-[calc(24px+var(--sab,0px))] pt-[calc(20px+var(--sat,0px))] sm:px-8 md:w-1/2 md:flex-none md:justify-center md:px-14 md:py-12">
            <div className="mx-auto flex w-full max-w-[420px] flex-1 flex-col md:max-w-[380px] md:flex-none">
              {mobileAppDesign && !registering && <div className="account-wordmark"><AuthWordmark /></div>}
              {children}
            </div>
          </div>
        </div>
      </div>
    </MotionDiv>
    {devButton}
  </div>;
}
