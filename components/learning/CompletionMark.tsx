import './completion-markers.css';
/** The adjacent text supplies the accessible completion state. */
export function CompletionMark({
  direction = 'tabs',
  number,
  complete,
  current = false,
}: {
  direction?: 'tabs';
  number: number;
  complete: boolean;
  current?: boolean;
}) {
  return (
    <span
      className={`cm-mark cm-${direction}`}
      data-complete={complete}
      data-current={current}
      aria-hidden="true"
    >
      <span>{String(number).padStart(2, '0')}</span>
    </span>
  );
}
