import pdfjsPackage from 'pdfjs-dist/package.json' with { type: 'json' };

// Keep decoder URLs tied to the PDF.js version, including in the offline cache.
export const PDFJS_WASM_PATH = `assets/pdfjs-${pdfjsPackage.version}/wasm/`;

export const pdfjsDocumentOptions = () => ({
  wasmUrl: new URL(`${import.meta.env.BASE_URL}${PDFJS_WASM_PATH}`, window.location.href).href,
});
