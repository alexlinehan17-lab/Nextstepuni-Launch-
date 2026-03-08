/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useGLTF } from '@react-three/drei';
import { MODEL_CATALOG } from './modelCatalog';

/**
 * Preload all Kenney GLB models at import time.
 * This triggers downloads early so models are cached before scenes render.
 * Import this file from JourneyCanvas.tsx to activate preloading.
 */
for (const entry of Object.values(MODEL_CATALOG)) {
  useGLTF.preload(entry.path);
}
