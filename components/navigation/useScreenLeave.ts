/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { useOptionalNavigation } from '../../contexts/NavigationContext';
import { isPlace } from '../../utils/places';
import type { LeaveControl } from '../ui/Bars';

/** The one leave control for the screen being shown (navigation.md, "Three
 *  kinds of screen"): none on one of the five places, Back on a page. Back is
 *  the screen's own handler when it passes one (a step of its own to go back
 *  through), else the app's one Back (contexts/NavigationContext.tsx, goBack):
 *  the screen you came from, or this screen's parent when there is no history.
 *  Outside the app's navigation (a part on its own) it is the handler given. */
export function useScreenLeave(onBack?: () => void, label?: string): LeaveControl | undefined {
  const nav = useOptionalNavigation();
  if (nav && isPlace(nav.state)) return undefined;
  const onPress = onBack ?? nav?.goBack;
  return onPress ? { kind: 'back', onPress, label } : undefined;
}
