import fs from 'node:fs';
import path from 'node:path';
import { build, transform } from 'esbuild';
import { execFileSync } from 'node:child_process';

// Local-only vendor refresh. Purchased editable sources are deliberately ignored.
// CI consumes the compiled application runtime; it does not need the originals.
if (!fs.existsSync('components/kobra/source.css')) {
  throw new Error('Refreshing account controls requires the local purchased Kobra originals in components/kobra. Normal builds use the committed compiled runtime.');
}
execFileSync(process.execPath, ['scripts/build-kobra-css.mjs'], { stdio: 'inherit' });
await build({
  stdin: { contents: `export {Checkbox} from './components/kobra/components/ui/checkbox';
    export {Combobox,ComboboxTrigger,ComboboxValue,ComboboxContent,ComboboxInput,ComboboxEmpty,ComboboxList,ComboboxItem} from './components/kobra/components/ui/combobox';
    export {RadioGroup,RadioGroupItem} from './components/kobra/components/ui/radio-group';`, resolveDir: process.cwd(), loader: 'tsx' },
  bundle: true, minify: true, sourcemap: false, format: 'esm', platform: 'browser', target: 'es2022', packages: 'external',
  outfile: 'components/account-ui-runtime.js',
  banner: { js: '/* Compiled purchased Kobra controls for NextStepUni. Editable originals remain local. */' },
  plugins: [{ name: 'local-kobra-alias', setup(api) { api.onResolve({ filter: /^@\/components\/kobra\// }, args => {
    const base = path.resolve(args.path.slice(2));
    return { path: [base + '.tsx', base + '.ts'].find(file => fs.existsSync(file)) };
  }); } }],
});
const css = await transform(fs.readFileSync('components/kobra/scoped.css', 'utf8'), { loader: 'css', minify: true });
fs.writeFileSync('components/account-ui-runtime.css', '/* Compiled account control styles, scoped to .nsu-kobra. */\n' + css.code);
