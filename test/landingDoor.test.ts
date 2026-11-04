import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { runInNewContext } from 'node:vm';
import { afterEach, describe, expect, it } from 'vitest';

const source = readFileSync(resolve('public/landing-door.js'), 'utf8');
type Reveal = { viewTransition?: { finished: Promise<void> } };

const setup = () => {
  const mark = document.createElement('div');
  mark.id = 'landing-mark';
  document.body.append(mark);
  let reveal: (event: Reveal) => void = () => { throw new Error('Reveal handler was not installed'); };
  runInNewContext(source, {
    document,
    addEventListener: (_name: string, handler: (event: Reveal) => void) => { reveal = handler; },
  });
  return { mark, reveal };
};

afterEach(() => document.getElementById('landing-mark')?.remove());

describe('landing transition mascot', () => {
  it.each(['finished', 'skipped'] as const)('clears the temporary mascot when the transition is %s without relying on a new traveller', async outcome => {
    const { mark, reveal } = setup();
    let finish!: () => void;
    let skip!: () => void;
    const finished = new Promise<void>((resolve, reject) => {
      finish = resolve;
      skip = () => reject(new Error('Transition skipped'));
    });
    reveal({ viewTransition: { finished } });
    expect(mark).toHaveAttribute('data-here');
    expect(mark.style.viewTransitionName).toBe('starguy');

    if (outcome === 'finished') finish(); else skip();
    await finished.catch(() => undefined);

    expect(mark).not.toHaveAttribute('data-here');
    expect(mark.style.viewTransitionName).toBe('');
  });

  it('does not show a second mascot on normal page loads', () => {
    const { mark, reveal } = setup();
    reveal({});
    expect(mark).not.toHaveAttribute('data-here');
  });
});
