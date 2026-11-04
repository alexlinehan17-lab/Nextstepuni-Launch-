import { downloadText } from '../../utils/downloadText';
export function PrivateDraftControls({ title, retain, setRetain, onClear, error, text }: { title: string; retain: boolean; setRetain: (retain: boolean) => void; onClear: () => void; error: boolean; text: string }) {
  return <div className="mr-private-draft">
    <p>Private to you. This stays in this session unless you choose to keep a device copy.</p>
    <label><input type="checkbox" checked={retain} onChange={event => setRetain(event.target.checked)} /> Keep on this device until sign-out</label>
    <p role="status">{error ? 'The device copy could not be saved. Download a copy before leaving.' : retain ? 'Device copy saved. Signing out clears it. This does not sync to your account.' : 'Kept for this session. It will be lost when you refresh or sign out.'}</p>
    <div><button type="button" onClick={() => downloadText(`${title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.txt`, text)} data-wide-button="true">Download a copy</button><button type="button" onClick={onClear} data-wide-button="true">Clear this draft</button></div>
  </div>;
}
