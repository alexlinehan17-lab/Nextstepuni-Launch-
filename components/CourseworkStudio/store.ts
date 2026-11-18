import { emptyWorkspace, parseBackup, MAX_BACKUP_BYTES, type CourseworkWorkspace } from './model';
const DATABASE = 'nextstepuni-coursework-v1';
const STORE = 'workspaces';
export interface CourseworkStore { load(owner: string): Promise<CourseworkWorkspace>; save(owner: string, value: CourseworkWorkspace): Promise<CourseworkWorkspace> }
function openDatabase(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    if (!globalThis.indexedDB) { reject(new Error('Device storage is unavailable. Enable site storage to keep your coursework.')); return; }
    const request = indexedDB.open(DATABASE, 1);
    request.onupgradeneeded = () => request.result.createObjectStore(STORE);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(new Error('Your saved coursework could not be opened. Retry before making changes.'));
  });
}
export const courseworkStore: CourseworkStore = {
  async load(owner) {
    const db = await openDatabase();
    return new Promise((resolve, reject) => { const transaction = db.transaction(STORE, 'readonly'); const request = transaction.objectStore(STORE).get(owner); let result = emptyWorkspace();
      request.onsuccess = () => { try { result = request.result ? parseBackup(JSON.stringify(request.result)) : emptyWorkspace(); } catch (error) { reject(error); } };
      transaction.oncomplete = () => { db.close(); resolve(result); }; transaction.onerror = () => { db.close(); reject(new Error('Your saved workspace could not be read.')); };
    });
  },
  async save(owner, value) {
    const serialized = JSON.stringify(value);
    if (serialized.length > MAX_BACKUP_BYTES) throw new Error('This workspace has reached its 80 MB limit. Keep larger files in your own backed-up folder.');
    // A saved workspace must also be loadable by the same schema.
    try { parseBackup(serialized); } catch { throw new Error('This change exceeds a workspace limit or contains an invalid value. Your previous saved work is safe; keep this form open and review the entries.'); }
    const db = await openDatabase();
    return new Promise((resolve, reject) => { const tx = db.transaction(STORE, 'readwrite'); const store = tx.objectStore(STORE); const request = store.get(owner); let conflict = false;
      const next = { ...value, revision: value.revision + 1 };
      request.onsuccess = () => { if ((request.result?.revision ?? 0) !== value.revision) { conflict = true; tx.abort(); } else store.put(next, owner); };
      tx.oncomplete = () => { db.close(); resolve(next); };
      tx.onabort = tx.onerror = () => { db.close(); reject(new Error(conflict ? 'Another tab changed this workspace. Copy any open form text, then reload before saving. Your saved work has not been overwritten.' : 'Your change could not be saved. Keep the form open and copy its text before reloading. Check available device storage.')); };
    });
  },
};
