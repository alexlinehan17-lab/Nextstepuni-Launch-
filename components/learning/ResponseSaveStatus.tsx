import type { ResponseSaveStatus as Status } from '../../services/moduleResponseStore';
export function ResponseSaveStatus({ status, onRetry }: { status: Status; onRetry: () => void }) {
  return <p className="mr-draft-status" role="status">{status === 'saved' ? 'Drafts saved to your private account.' : status === 'saving' ? 'Saving drafts… Keep this tab open until saved.' : status === 'loading' ? 'Loading your drafts…' : status === 'device' ? 'Preview drafts stay on this device until sign-out.' : <>Account save hasn’t completed. Keep a copy before signing out. <button type="button" onClick={onRetry}>Retry save</button></>}</p>;
}
