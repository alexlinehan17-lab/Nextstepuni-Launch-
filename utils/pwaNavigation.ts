/** Workbox matches pathname + search, so standalone documents must also be
 * excluded when they carry query parameters (including embedded previews). */
export const standaloneDocumentRoutes = [
  /^\/(?:privacy|terms)(?:\.html)?(?:\?|$)/,
  /^\/landing(?:-dev\.html|-demo\.html)?(?:\?|$)/,
  /^\/certle(?:\.html|\/)?(?:\?|$)/,
];
