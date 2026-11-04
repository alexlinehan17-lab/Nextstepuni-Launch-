import { describe, expect, it } from 'vitest';
import { floatingHome, floatingMotion } from '../components/landing/starguy/floating';
import { CANVAS } from '../components/landing/fx-char/control';

describe('Star Guy’s floating margin', () => {
  it('keeps the full moving figure between the viewport edge and the content', () => {
    for (const margin of [96, 128, 160, 280, 480]) {
      const home = floatingHome(margin, 68, 800)!;
      for (const velocity of [-12000, 0, 12000]) {
        for (let time = 0; time <= 19200; time += 200) {
          const motion = floatingMotion(time, velocity);
          expect(home.left + motion.x).toBeGreaterThan(12);
          expect(home.left + home.width + motion.x).toBeLessThan(margin - 12);
          expect(home.top + motion.y).toBeGreaterThan(68 + 32);
          expect(home.top + motion.y + home.width * CANVAS.height / CANVAS.width).toBeLessThan(800 - 24);
        }
      }
    }
  });
  it('returns to the nav instead of obscuring content on a narrow or short viewport', () => {
    expect(floatingHome(32, 68, 800)).toBeNull();
    expect(floatingHome(72, 68, 800)).toBeNull();
    expect(floatingHome(280, 68, 220)).toBeNull();
  });
  it('keeps the float gentle and drives Rive with bounded inputs even during fast scrolling', () => {
    for (const velocity of [-12000, 0, 12000]) {
      for (let time = 0; time < 20000; time += 200) {
        const motion = floatingMotion(time, velocity);
        expect(Math.abs(motion.y)).toBeLessThanOrEqual(8);
        expect(Math.abs(motion.lean)).toBeLessThanOrEqual(5);
        expect(Math.abs(motion.squash)).toBeLessThanOrEqual(0.055);
        expect(motion.speed).toBeGreaterThan(0);
        expect(motion.speed).toBeLessThanOrEqual(100);
      }
    }
    expect(floatingMotion(0, 1000).lean).toBeGreaterThan(floatingMotion(0, -1000).lean);
    expect(floatingMotion(0, 1800).speed).toBeGreaterThan(floatingMotion(0, 0).speed);
  });
});
