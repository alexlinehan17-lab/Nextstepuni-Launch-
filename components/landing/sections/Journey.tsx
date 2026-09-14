import React, { lazy, Suspense, useEffect, useRef, useState } from 'react';
import { COPY } from '../copy';
import { Button, Container, Eyebrow } from '../primitives';
import { APP_URL } from '../theme';
import '../journey/journey.css';

const JourneyIsland = lazy(() => import('../journey/JourneyIsland'));

/** The artwork and builder load as this section approaches the viewport. */
export default function Journey() {
  const ref = useRef<HTMLElement>(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setReady(true);
        observer.disconnect();
      }
    }, { rootMargin: '500px' });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  const copy = COPY.journey;
  const placeholder = <div className="journey-demo-placeholder" role="status">Your little elsewhere is taking shape…</div>;
  return (
    <section id="journey" ref={ref} className="landing-journey" aria-labelledby="journey-title">
      <Container>
        <div className="landing-journey-intro">
          <div>
            <Eyebrow>{copy.eyebrow}</Eyebrow>
            <h2 id="journey-title">{copy.title}<br /><em>{copy.titleEnd}</em></h2>
          </div>
          <div className="landing-journey-story">
            <p>{copy.body}</p>
            <Button href={APP_URL}>{copy.cta}<span aria-hidden="true">↗</span></Button>
          </div>
        </div>
      </Container>
      <div className="landing-journey-atlas">
        {ready ? <Suspense fallback={placeholder}><JourneyIsland /></Suspense> : placeholder}
      </div>
      <Container>
        <ol className="landing-journey-steps">
          {copy.steps.map((step, index) => (
            <li key={step.title}>
              <span aria-hidden="true">0{index + 1}</span>
              <h3>{step.title}</h3>
              <p>{step.body}</p>
            </li>
          ))}
        </ol>
      </Container>
    </section>
  );
}
