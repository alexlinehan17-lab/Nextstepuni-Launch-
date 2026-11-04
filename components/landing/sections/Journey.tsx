import React, { lazy, Suspense, useEffect, useRef, useState } from 'react';
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

  const placeholder = <div className="journey-demo-placeholder" role="status">Your little elsewhere is taking shape…</div>;
  return (
    <section id="journey" ref={ref} className="landing-journey-atlas" aria-label="Try Journey mode">
      {ready ? <Suspense fallback={placeholder}><JourneyIsland /></Suspense> : placeholder}
    </section>
  );
}
