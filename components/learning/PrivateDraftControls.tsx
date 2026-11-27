import { downloadText } from '../../utils/downloadText';
import { TextButton } from '../ui/Button';
import { SelectionMark } from '../ui/Choice';
import { CheckRow } from '../ui/List';
// Area 5b: the keep-a-copy setting is the shared row you tick (44 tall, the square mark), its two actions text buttons.
export function PrivateDraftControls({ title, retain, setRetain, onClear, error, text }: { title: string; retain: boolean; setRetain: (retain: boolean) => void; onClear: () => void; error: boolean; text: string }) {
  return <div className="mr-private-draft">
    <p>Private to you. This stays in this session unless you choose to keep a device copy.</p>
    <CheckRow checked={retain} onChange={setRetain} mark={<SelectionMark on={retain} shape="square" />} className="mr-private-keep">Keep on this device until sign-out</CheckRow>
    <p role="status">{error ? 'The device copy could not be saved. Download a copy before leaving.' : retain ? 'Device copy saved. Signing out clears it. This does not sync to your account.' : 'Kept for this session. It will be lost when you refresh or sign out.'}</p>
    <div><TextButton onClick={() => downloadText(`${title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.txt`, text)}>Download a copy</TextButton><TextButton tone="danger" onClick={onClear}>Clear this draft</TextButton></div>
  </div>;
}
