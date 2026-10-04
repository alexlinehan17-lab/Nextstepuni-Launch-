/** Workbox matches pathname + search, so standalone documents must also be
 * excluded when they carry query parameters (including embedded previews). */
export const standaloneDocumentRoutes = [
  /^\/components(?:\/|\?|$)/,
  /^\/(?:privacy|terms)(?:\.html)?(?:\?|$)/,
  /^\/legal\/\d{4}-\d{2}-\d{2}\/(?:privacy|terms)\.html(?:\?|$)/,
  /^\/landing(?:-dev\.html|-demo\.html)?(?:\?|$)/,
  /^\/certle(?:\.html|\/)?(?:\?|$)/,
];
