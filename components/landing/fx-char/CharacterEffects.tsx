/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The character effects of Volume II, mounted by the StarguyProvider only
 * while the traveller is live — so none of this exists on a phone, under
 * reduced motion, or in a static render. Each one is self-contained and
 * talks to him through fx-char/control.ts.
 *
 *   Topple      the hero headline falls and he restacks it (once a visit)
 *   Ragdoll     his star is grabbable in the hero; yank it and he goes over
 *   PaperThrow  a paper floor under the Paper Trail chapter to fling papers at him
 *   DevHarness  ?starguy=1 — buttons to fire each reaction for screenshots
 */

import React, { useState } from 'react';
import Topple from './Topple';
import Ragdoll from './Ragdoll';
import PaperThrow from './PaperThrow';
import DevHarness from './DevHarness';
import './fx-char.css';

const CharacterEffects: React.FC = () => {
  const [dev] = useState(() => typeof window !== 'undefined' && new URLSearchParams(window.location.search).has('starguy'));
  return (
    <>
      <Topple />
      <Ragdoll />
      <PaperThrow />
      {dev && <DevHarness />}
    </>
  );
};

export default CharacterEffects;
