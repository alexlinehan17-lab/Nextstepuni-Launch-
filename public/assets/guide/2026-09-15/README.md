# Current app tour captures

Captured on 15 September 2026 from the running app at commit `a181d549`, using its built-in demo account. These are browser screenshots, not mockups.

- Desktop: 1456 × 949, except Home.
- Home was recaptured at commit `4a337d2d` in a 1456 × 1437 viewport as `desktop/home-full-height.webp`. Matching the viewport to the page height keeps the fixed sidebar continuous, with its lower controls anchored at the bottom. The former stitched full-page capture ended the sidebar partway down. `desktop/home.webp` remains only for older cached clients.
- Mobile: 393 × 852, using the real mobile app layout through the development-only `data-app-preview="mobile"` iframe switch.
- Paper Horizon is running in the Study captures; sample sessions were discarded after capture.
- Journey shows the Blue-pencil atlas with the tile tray open.
- PNG screenshots were encoded as WebP at quality 88, with no compositing, retouching or UI replacement. Exact image dimensions are in `captures.json`.

`SiteGuide.tsx` selects the matching device set. Keep these paths versioned so cached clients cannot show an older design under a new card.
