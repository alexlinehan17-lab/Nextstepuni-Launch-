/** Vite's `?raw` import: the generated SVGs under fx/ are inlined as strings. */
declare module '*.svg?raw' {
  const src: string;
  export default src;
}
