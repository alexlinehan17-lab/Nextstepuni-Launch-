/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Things that come up over the screen (components.md, "Sheets, dialogs,
 * toasts"; the kit's .sheet and the confirm): one Sheet and one Confirm.
 *
 *   <Sheet open={open} onClose={close} title="What are you studying?"
 *     footer={<Button kind="main" size="lg" block arrow="forward">Choose Mathematics</Button>}>
 *     ...choice tiles...
 *   </Sheet>
 *   <Sheet open title="This week's goal" titleSize="small" onClose={discard} save={{ label: 'Save', onPress: keep }}>   Cancel left, Save right
 *   <Confirm open sentence="Delete your account?" detail="Everything ... cannot be brought back."
 *     keepLabel="Keep my account" dangerLabel="Delete account" onKeep={close} onDanger={erase} />
 *
 * The Sheet rises from the bottom on a phone and is a centred dialog from
 * 640px, on the frame's frame-sheet-backdrop / frame-sheet primitives, so it
 * can never reach the island or the home indicator. One way out at its top
 * left: Close (an X), or Cancel when there are unsaved changes (with Save or
 * Done at the right). It also closes by Escape, a tap on the dimmed page, or
 * a swipe down on its handle. Behaviour is the house contract, useModal: the
 * page behind is locked, focus moves in and stays in, and returns to what
 * opened it.
 *
 * The Confirm is the only centred pop-up on a phone: one sentence saying what
 * happens, the safe choice as the main button (it takes focus), the
 * destructive one as red text. Escape and the dimmed page choose the safe one.
 *
 * Migration: ModalFrame, SignatureCard, CelebrationFrame, the Kobra Dialog
 * and the hand-built dialogs keep today's look; each moves onto these in
 * stage 2B or 4. The Kobra Dialog is not reused here: it is always centred
 * and its compiled parts do not expose a bottom-sheet form.
 */
import { useEffect, useId, useRef, useState, type CSSProperties, type PointerEvent as ReactPointerEvent, type ReactNode } from 'react';
import { X } from 'lucide-react';
import { useModal } from '../../hooks/useModal';
import { FramePortal } from './Frame';
import { Button, TextButton } from './Button';
import './parts.css';

type Phase = 'closed' | 'entering' | 'open' | 'leaving';

/** Mount, then open on the next frame so the rise is drawn; on close, leave,
 *  then unmount. Reduced motion: the CSS fades in place instead. */
function usePresence(open: boolean, leaveMs: number): Phase {
  const [phase, setPhase] = useState<Phase>(open ? 'entering' : 'closed');
  useEffect(() => {
    if (open) {
      setPhase(current => (current === 'open' ? current : 'entering'));
      let second = 0;
      const first = requestAnimationFrame(() => { second = requestAnimationFrame(() => setPhase('open')); });
      return () => { cancelAnimationFrame(first); cancelAnimationFrame(second); };
    }
    setPhase(current => (current === 'closed' ? current : 'leaving'));
    const timer = window.setTimeout(() => setPhase('closed'), leaveMs);
    return () => window.clearTimeout(timer);
  }, [open, leaveMs]);
  return phase;
}

/** A sheet leaves in 320ms (motion.md); a confirm in about 80% of its 260ms. */
const SHEET_LEAVE_MS = 320;
const CONFIRM_LEAVE_MS = 210;
/** Past this share of its height, or faster than this (px per ms), a drag closes the sheet. */
const DRAG_CLOSE_SHARE = 0.4;
const FLICK_SPEED = 0.5;

export interface SheetAction { label: string; onPress: () => void }

export interface SheetProps {
  open: boolean;
  /** Close, Cancel, Escape, the dimmed page and a swipe down all call this. */
  onClose: () => void;
  title: ReactNode;
  /** small (17px) for a sheet whose body opens with its own headline. */
  titleSize?: 'heading' | 'small';
  /** Unsaved changes: Cancel (left) throws them away, this (right) keeps them. Close is not shown. */
  save?: SheetAction;
  /** The main action, pinned at the bottom above the home indicator. */
  footer?: ReactNode;
  children: ReactNode;
  /** Name for Close (default "Close"). */
  closeLabel?: string;
}

export function Sheet({ open, onClose, title, titleSize = 'heading', save, footer, children, closeLabel = 'Close' }: SheetProps) {
  const phase = usePresence(open, SHEET_LEAVE_MS);
  const panel = useRef<HTMLDivElement>(null);
  const titleId = useId();
  useModal(open && phase !== 'closed', onClose, panel);
  const [drag, setDrag] = useState<{ y0: number; t0: number; dy: number } | null>(null);
  if (phase === 'closed') return null;

  const onDragStart = (event: ReactPointerEvent<HTMLDivElement>) => {
    if ((event.target as HTMLElement).closest('button')) return;
    event.currentTarget.setPointerCapture?.(event.pointerId);
    setDrag({ y0: event.clientY, t0: event.timeStamp, dy: 0 });
  };
  const onDragMove = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (drag) setDrag({ ...drag, dy: Math.max(0, event.clientY - drag.y0) });
  };
  const onDragEnd = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (!drag) return;
    const height = panel.current?.offsetHeight ?? 1;
    const speed = drag.dy / Math.max(1, event.timeStamp - drag.t0);
    setDrag(null);
    if (drag.dy > height * DRAG_CLOSE_SHARE || (drag.dy > 24 && speed > FLICK_SPEED)) onClose();
  };
  const dragHandlers = { onPointerDown: onDragStart, onPointerMove: onDragMove, onPointerUp: onDragEnd, onPointerCancel: onDragEnd };

  return (
    <FramePortal>
      <div
        className="ui-part ui-layer frame-sheet-backdrop"
        data-state={phase === 'leaving' ? 'leaving' : phase === 'open' ? 'open' : 'entering'}
        data-dragging={drag ? '' : undefined}
        style={drag ? ({ '--sheet-drag': `${drag.dy}px` } as CSSProperties) : undefined}
      >
        <div className="ui-scrim" aria-hidden="true" onClick={onClose} />
        <div ref={panel} role="dialog" aria-modal="true" aria-labelledby={titleId} tabIndex={-1} className="ui-sheet frame-sheet">
          <div className="ui-sheet-drag" {...dragHandlers}>
            <span className="ui-sheet-grab" aria-hidden="true" />
            <div className="ui-sheet-head frame-dialog-head">
              {save
                ? <button type="button" className="ui-sheet-text" onClick={onClose}>Cancel</button>
                : <button type="button" className="ui-icon-btn" aria-label={closeLabel} onClick={onClose}>
                    <X className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />
                  </button>}
              <h2 id={titleId} className={`ui-sheet-title${titleSize === 'small' ? ' ui-sheet-title--small' : ''}`}>{title}</h2>
              {save
                ? <button type="button" className="ui-sheet-text ui-sheet-text--strong" onClick={save.onPress}>{save.label}</button>
                : <span aria-hidden="true" />}
            </div>
          </div>
          <div className="ui-sheet-body">{children}</div>
          {footer ? <div className="ui-sheet-foot">{footer}</div> : null}
        </div>
      </div>
    </FramePortal>
  );
}

export interface ConfirmProps {
  open: boolean;
  /** One sentence saying what happens ("Delete your account?"). */
  sentence: ReactNode;
  /** What it means, if the sentence needs it. */
  detail?: ReactNode;
  /** The safe choice: the main button, focused first. */
  keepLabel: string;
  onKeep: () => void;
  /** The destructive choice, in red text. */
  dangerLabel: string;
  onDanger: () => void;
}

export function Confirm({ open, sentence, detail, keepLabel, onKeep, dangerLabel, onDanger }: ConfirmProps) {
  const phase = usePresence(open, CONFIRM_LEAVE_MS);
  const card = useRef<HTMLDivElement>(null);
  const titleId = useId();
  const detailId = useId();
  useModal(open && phase !== 'closed', onKeep, card);
  if (phase === 'closed') return null;
  return (
    <FramePortal>
      <div className="ui-part ui-confirm-layer frame-dialog" data-state={phase === 'leaving' ? 'leaving' : phase === 'open' ? 'open' : 'entering'}>
        <div className="ui-scrim" aria-hidden="true" onClick={onKeep} />
        <div ref={card} role="alertdialog" aria-modal="true" aria-labelledby={titleId} aria-describedby={detail ? detailId : undefined}
          tabIndex={-1} className="ui-confirm frame-dialog-card">
          <h2 id={titleId} className="ui-confirm-title">{sentence}</h2>
          {detail ? <p id={detailId} className="ui-confirm-text">{detail}</p> : null}
          <Button kind="main" block onClick={onKeep}>{keepLabel}</Button>
          <TextButton tone="danger" onClick={onDanger}>{dangerLabel}</TextButton>
        </div>
      </div>
    </FramePortal>
  );
}
