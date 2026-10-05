import fs from 'node:fs';
import path from 'node:path';
import { build, transform } from 'esbuild';
import ts from 'typescript';
import { execFileSync } from 'node:child_process';

// Purchased editable sources remain local, as with the existing approved controls.
// Normal app/CI builds consume this generated runtime, types and scoped stylesheet.
const root = process.cwd();
const source = path.join(root, 'components/kobra/navigation');
if (!fs.existsSync(path.join(source, 'registry/sidebar.json'))) {
  throw new Error('The locally purchased Kobra navigation sources are required to refresh this runtime.');
}
execFileSync(process.execPath, ['scripts/build-kobra-navigation-css.mjs'], { stdio: 'inherit' });
const modules = ['sidebar', 'sidebar-resize', 'dropdown-menu', 'avatar', 'kbd', 'tooltip', 'sound'];
const entry = modules.map(name => `export * from './components/ui/${name}';`).join('\n')
  + "\nexport { useIsMobile } from './hooks/use-mobile';\n";
const entryFile = path.join(source, 'entry.ts');
fs.writeFileSync(entryFile, entry);
await build({
  entryPoints: [entryFile], bundle: true, minify: true, format: 'esm',
  platform: 'browser', target: 'es2022', jsx: 'automatic', packages: 'external',
  outfile: 'components/kobra-navigation-runtime.js',
  banner: { js: '/* Kobra navigation, purchased registry source retrieved 4 October 2026. */\nimport "./kobra-navigation-runtime.css";' },
});
const css = await transform(fs.readFileSync(path.join(source, 'scoped.css'), 'utf8'), { loader: 'css', minify: true });
fs.writeFileSync('components/kobra-navigation-runtime.css', '/* Isolated purchased Kobra navigation styles. */\n' + css.code);
const typeRoot = path.join(root, 'components/kobra-navigation-types');
const config = ts.readConfigFile('tsconfig.json', ts.sys.readFile);
const parsed = ts.parseJsonConfigFileContent(config.config, ts.sys, root);
const program = ts.createProgram([entryFile], {
  ...parsed.options, noEmit: false, declaration: true, emitDeclarationOnly: true,
  rootDir: source, outDir: typeRoot,
});
if (program.emit().emitSkipped) throw new Error('Navigation declarations could not be emitted.');
fs.writeFileSync('components/kobra-navigation-runtime.d.ts',
  modules.map(name => `export * from './kobra-navigation-types/components/ui/${name}';`).join('\n')
  + "\nexport { useIsMobile } from './kobra-navigation-types/hooks/use-mobile';\n");
const provenance = JSON.parse(fs.readFileSync(path.join(source, 'registry/provenance.json'), 'utf8'));
fs.mkdirSync('docs/design', { recursive: true });
fs.writeFileSync('docs/design/kobra-sidebar-source-provenance.json', JSON.stringify(provenance, null, 2) + '\n');
console.log('Built current Kobra navigation, sidebar resize and shared sounds.');
