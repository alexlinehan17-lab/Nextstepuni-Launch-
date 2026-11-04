import React, { Component, lazy, Suspense, useEffect, useState } from "react";
import { motion, useMotionValue } from "framer-motion";
import { floatingMotion } from "../landing/starguy/floating";

const StarguyFigure = lazy(() => import("../landing/starguy/StarguyFigure"));
const Still = () => (
  <img
    src="/assets/landing/starguy-512.png"
    alt=""
    width={1030}
    height={1193}
  />
);

class AnimationBoundary extends Component<
  { children: React.ReactNode },
  { failed: boolean }
> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  render() {
    return this.state.failed ? <Still /> : this.props.children;
  }
}

/** The landing page's Rive rig and scroll response, with a reserved home so
 * the character never crosses the question, answer field or mobile controls. */
export default function CertleCompanion() {
  const [animated, setAnimated] = useState(false);
  const x = useMotionValue(0),
    y = useMotionValue(0);
  const speed = useMotionValue(14),
    lean = useMotionValue(0),
    squash = useMotionValue(0);
  const lookX = useMotionValue(0.25),
    lookY = useMotionValue(0);
  useEffect(() => {
    const preference = window.matchMedia(
      "(prefers-reduced-motion: no-preference)",
    );
    const update = () => setAnimated(preference.matches);
    update();
    preference.addEventListener("change", update);
    return () => preference.removeEventListener("change", update);
  }, []);
  useEffect(() => {
    if (!animated) {
      x.set(0);
      y.set(0);
      return;
    }
    let frame = 0,
      lastY = window.scrollY,
      lastAt = performance.now(),
      velocity = 0;
    const tick = (at: number) => {
      const dt = Math.max(1, at - lastAt);
      velocity +=
        (((window.scrollY - lastY) / dt) * 1000 - velocity) *
        Math.min(1, dt / 80);
      lastY = window.scrollY;
      lastAt = at;
      const pose = floatingMotion(at, velocity);
      x.set(pose.x);
      y.set(pose.y);
      speed.set(pose.speed);
      lean.set(pose.lean);
      squash.set(pose.squash);
      frame = requestAnimationFrame(tick);
    };
    const resume = () => {
      cancelAnimationFrame(frame);
      if (!document.hidden) {
        lastAt = performance.now();
        lastY = window.scrollY;
        frame = requestAnimationFrame(tick);
      }
    };
    resume();
    document.addEventListener("visibilitychange", resume);
    return () => {
      cancelAnimationFrame(frame);
      document.removeEventListener("visibilitychange", resume);
    };
  }, [animated, x, y, speed, lean, squash]);
  return (
    <motion.div
      className="certle-companion"
      aria-hidden="true"
      style={{ x, y }}
    >
      {animated ? (
        <AnimationBoundary>
          <Suspense fallback={<Still />}>
            <StarguyFigure
              speed={speed}
              lean={lean}
              squash={squash}
              lookX={lookX}
              lookY={lookY}
            />
          </Suspense>
        </AnimationBoundary>
      ) : (
        <Still />
      )}
    </motion.div>
  );
}
