// Stage the licensed, compiled component gallery without publishing its source
// or large media files in this public repository.
import { createHash } from 'node:crypto';
import { createWriteStream } from 'node:fs';
import { mkdir, readFile, rename, rm } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';

const MAX_FILE_BYTES = 320 * 1024 * 1024;
const MAX_TOTAL_BYTES = 384 * 1024 * 1024;
const ALLOWED_PATH = /^(?:index\.html|showcase\/index\.html|burst\.json|assets\/[\w.-]+\.(?:js|css)|fonts\/[\w.-]+\.woff2|images\/(?:carousel|halftone|previews)\/[\w.-]+\.(?:png|webp)|logos\/[\w.-]+\.(?:png|svg)|media\/[\w.-]+\.(?:webm|webp))$/;

export function validateManifest(manifest) {
  if (manifest?.schemaVersion !== 1
    || manifest.bucket !== 'nextstepuni-app.firebasestorage.app'
    || !/^private-builds\/component-library\/[\w.-]+$/.test(manifest.prefix)
    || !Array.isArray(manifest.files)
    || manifest.files.length === 0
    || manifest.files.length > 120) {
    throw new Error('Invalid component library manifest');
  }

  const seen = new Set();
  let totalBytes = 0;
  for (const file of manifest.files) {
    if (typeof file?.path !== 'string' || !ALLOWED_PATH.test(file.path) || seen.has(file.path)) {
      throw new Error('Unsafe or duplicate component library path');
    }
    if (!Number.isSafeInteger(file.size) || file.size < 0 || file.size > MAX_FILE_BYTES) {
      throw new Error('Invalid component library file size');
    }
    if (typeof file.sha256 !== 'string' || !/^[a-f0-9]{64}$/.test(file.sha256)) {
      throw new Error('Invalid component library checksum');
    }
    seen.add(file.path);
    totalBytes += file.size;
  }
  if (!seen.has('index.html') || !seen.has('showcase/index.html') || totalBytes > MAX_TOTAL_BYTES) {
    throw new Error('Incomplete or oversized component library');
  }
  return manifest.files;
}

export async function stageLibrary(manifest, destination, openStream) {
  const files = validateManifest(manifest);
  await rm(destination, { recursive: true, force: true });

  try {
    for (const file of files) {
      const target = resolve(destination, file.path);
      const temporary = `${target}.part`;
      await mkdir(dirname(target), { recursive: true });

      const hash = createHash('sha256');
      let bytes = 0;
      const verifier = new Transform({
        transform(chunk, _encoding, callback) {
          bytes += chunk.length;
          hash.update(chunk);
          callback(null, chunk);
        },
      });

      await pipeline(await openStream(file), verifier, createWriteStream(temporary, { flags: 'wx' }));
      if (bytes !== file.size || hash.digest('hex') !== file.sha256) {
        await rm(temporary, { force: true });
        throw new Error(`Component library verification failed: ${file.path}`);
      }
      await rename(temporary, target);
    }
  } catch (error) {
    await rm(destination, { recursive: true, force: true });
    throw error;
  }

  return files.length;
}

async function main() {
  const root = fileURLToPath(new URL('../', import.meta.url));
  const manifest = JSON.parse(await readFile(resolve(root, 'deployment/component-library.json'), 'utf8'));
  validateManifest(manifest);

  const require = createRequire(import.meta.url);
  const firebaseRequire = createRequire(require.resolve('firebase-tools/package.json'));
  const { GoogleAuth } = firebaseRequire('google-auth-library');
  const auth = new GoogleAuth({ scopes: ['https://www.googleapis.com/auth/devstorage.read_only'] });
  const client = await auth.getClient();

  const count = await stageLibrary(manifest, resolve(root, 'dist/components'), async file => {
    const object = `${manifest.prefix}/${file.path}`;
    const url = `https://storage.googleapis.com/storage/v1/b/${manifest.bucket}/o/${encodeURIComponent(object)}?alt=media`;
    const response = await client.request({ url, responseType: 'stream' });
    return response.data;
  });
  console.log(`Verified and staged component library (${count} files).`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main().catch(error => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
