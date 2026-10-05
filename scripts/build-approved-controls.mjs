import fs from 'node:fs';
import path from 'node:path';
import { build, transform } from 'esbuild';
import ts from 'typescript';
import { execFileSync } from 'node:child_process';

// Refresh locally from purchased originals. CI only consumes the compiled runtime,
// generated declarations and scoped styles; editable vendor source stays private.
const sourceRoot = process.env.NSU_CONTROLS_SOURCE;
if (!sourceRoot || !fs.existsSync(path.join(sourceRoot, 'components/kobra/KobraScope.tsx'))) {
  throw new Error('Set NSU_CONTROLS_SOURCE to the local checkout containing the purchased controls. Normal app builds do not require it.');
}
const root = process.cwd();
const vendor = path.join(sourceRoot, 'components/kobra');
const modules = JSON.parse(fs.readFileSync('scripts/approved-controls-exports.json', 'utf8'));
execFileSync(process.execPath, ['scripts/build-kobra-css.mjs'], { cwd: sourceRoot, stdio: 'inherit' });
const entry = Object.entries(modules).map(([file, names]) =>
  `export { ${names.join(', ')} } from ${JSON.stringify(path.join(vendor, file))};`
).join('\n');
const result = await build({
  stdin: { contents: entry, resolveDir: sourceRoot, loader: 'tsx' },
  bundle: true, minify: true, sourcemap: false, format: 'esm', platform: 'browser',
  target: 'es2022', packages: 'external', metafile: true, jsx: 'automatic',
  outfile: 'components/approved-ui-runtime.js',
  banner: { js: '/* Compiled purchased controls for NextStepUni. Editable originals remain local. */\nimport "./approved-ui-runtime.css";\nimport "./approved-ui-theme.css";' },
  plugins: [{ name: 'private-control-sources', setup(api) {
    // Every Kobra scope shares the same sound runtime and listener ownership.
    // The navigation runtime contains the current purchased sound patches.
    api.onResolve({ filter: /(?:^|\/)sound$/ }, args => {
      if (args.path.startsWith(vendor) || args.importer.startsWith(vendor)) {
        return { path: './kobra-navigation-runtime', external: true };
      }
    });
    api.onResolve({ filter: /^@\/hooks\/useModal$/ }, () => ({ path: '../hooks/useModal', external: true }));
    api.onResolve({ filter: /^@\// }, args => {
      const base = path.join(sourceRoot, args.path.slice(2));
      return { path: [base, base+'.tsx', base+'.ts'].find(file => fs.existsSync(file) && fs.statSync(file).isFile()) };
    });
    api.onLoad({ filter: /\.css$/ }, () => ({ contents: '', loader: 'empty' }));
  } }],
});
for (const [input, output] of [['scoped.css','approved-ui-runtime.css'], ['nextstepuni.css','approved-ui-theme.css']]) {
  const css = await transform(fs.readFileSync(path.join(vendor,input),'utf8'), { loader:'css', minify:true });
  fs.writeFileSync(path.join(root,'components',output), '/* Compiled scoped NextStepUni control styles. */\n'+css.code);
}

// TypeScript emits declarations only. Retain the genuine component type surface
// (including generic Select/Combobox props) without publishing implementations.
const declarationRoot = path.join(root,'node_modules/.cache/nsu-approved-control-declarations');
fs.mkdirSync(declarationRoot,{recursive:true});
const entryFile = path.join(sourceRoot,'node_modules/.cache/nsu-approved-controls-entry.ts');
fs.mkdirSync(path.dirname(entryFile),{recursive:true});
fs.writeFileSync(entryFile,entry);
const config = ts.readConfigFile(path.join(sourceRoot,'tsconfig.json'),ts.sys.readFile);
const parsed = ts.parseJsonConfigFileContent(config.config,ts.sys,sourceRoot);
const program = ts.createProgram([entryFile],{
  ...parsed.options, noEmit:false, declaration:true, emitDeclarationOnly:true,
  outDir:declarationRoot, rootDir:sourceRoot,
});
const emitted = program.emit();
if (emitted.emitSkipped) throw new Error('Control declaration emission failed.');
const typeRoot = path.join(root,'components/approved-ui-types');
fs.mkdirSync(typeRoot,{recursive:true});
const declarations = path.join(declarationRoot,'components/kobra');
function copyDeclarations(dir) {
  for (const item of fs.readdirSync(dir,{withFileTypes:true})) {
    const from=path.join(dir,item.name);
    if(item.isDirectory()){copyDeclarations(from);continue;}
    if(!item.name.endsWith('.d.ts')) continue;
    const to=path.join(typeRoot,path.relative(declarations,from));
    fs.mkdirSync(path.dirname(to),{recursive:true});
    const text=fs.readFileSync(from,'utf8')
      .replace(/^import ['"].*\.css['"];?\n/gm,'')
      .replace(/(['"])@\/components\/kobra\/([^'"]+)\1/g,(_,quote,suffix)=>{
        let relative=path.relative(path.dirname(to),path.join(typeRoot,suffix)).replaceAll(path.sep,'/');
        if(!relative.startsWith('.'))relative='./'+relative;
        return quote+relative+quote;
      });
    fs.writeFileSync(to,'// Generated declarations for the compiled control runtime.\n'+text);
  }
}
copyDeclarations(declarations);
fs.writeFileSync('components/approved-ui-runtime.d.ts',Object.entries(modules).map(([file,names])=>
  `export { ${names.join(', ')} } from './approved-ui-types/${file.replace(/\.(ts|tsx)$/,'')}';`
).join('\n')+'\n');
const packages = [...new Set(Object.values(result.metafile.outputs).flatMap(output=>output.imports)
  .filter(item=>item.external&&!item.path.startsWith('.')).map(item=>item.path.startsWith('@')?item.path.split('/').slice(0,2).join('/'):item.path.split('/')[0]))].sort();
console.log('Runtime external packages:',packages.join(', '));
