

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';

/**
 * Suspense fallback for code-split routes. Route transitions deliberately render
 * nothing here: fast chunks feel immediate, and no temporary screen flashes in
 * the wrong layout while a slower chunk resolves.
 */
export const LoadingSpinner: React.FC = () => null;
