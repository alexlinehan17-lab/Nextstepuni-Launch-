/**
 * The notification bell lives in App's global header, while several page
 * sidebars expose a second control for the same panel. A shared event keeps
 * those controls on one toggle path without simulating delayed DOM clicks.
 */
export const NOTIFICATION_PANEL_TOGGLE_EVENT = 'nextstepuni:toggle-notifications';

export function toggleNotificationPanel(): void {
  window.dispatchEvent(new Event(NOTIFICATION_PANEL_TOGGLE_EVENT));
}

