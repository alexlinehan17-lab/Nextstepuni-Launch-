# Approved app release — 13 September 2026

The live Journey now uses the loose-and-lively raised paper tiles and Blue-pencil atlas. The build tray offers 54 placeable tiles from the 56-piece collection; the starter home and discoverable treasure complete the set. Tiles join without gaps, exposed shores retain depth, and stable random edge marks use only the four approved treatments. Students select a tile, an adjacent open corner, and confirm. Previewing and panning never reveal or purchase anything.

Exploration reveals the map around confirmed placements, ten approved mythic discoveries, and two hidden destinations with treasure. The fieldbook keeps discovered stories. Chests award two meadow tiles once; collecting a chest commits its approach and ends the last-placement undo. New ranks award three meadow tiles to place, rather than automatically adding land.

The new authenticated `updatePaperIsland` callable saves the island and its spending in one Firestore transaction. A revision check rejects stale windows and request IDs make retries safe. Undo returns the last tile's exact cost or earned tile and restores visibility. Firestore rules prevent direct writes to the island and its refund receipt. The single-document island supports up to 3,000 placed tiles; a multi-document layout will be needed beyond that size.

On the first Journey visit, existing pre-launch 3D layouts are replaced with the seven-tile paper starter. Only the retired island's recorded spending is refunded. Student profiles, subjects, learning progress and other purchases remain. Reset happens once per account; there is no bulk deletion of progress documents.

Desktop onboarding now uses the approved full-page desktop artwork and grade sheet, backed by the same validated, account-scoped draft and completion controller as mobile. Guests still use session-only storage and write no account data. Junior Cycle, LCA and transition-to-senior paths remain supported.

The release also integrates the outstanding mobile lesson interactions, module-completion dialog, recorded-evidence Insights and Site Guide work from PR #94. The Launchpad and Study Session redesigns were already on main (#138 and #143) and are retained. The older charcoal ToolHero proposal from PR #93 is superseded by the current ToolMasthead design. Rejected artwork and design comparison pages are not part of this release.

Browser checks cover choosing a tile and a westward position, unchanged JP and visibility during preview, placement, reload persistence of the edge, exact undo, and phone layout. The map uses raster artwork, a lightweight canvas reveal mask and lazy tile thumbnails; the live Journey no longer imports the old Three.js world.
