// Generated declarations for the compiled control runtime.
import { type ReactNode } from 'react';
import { type AlertTone } from './alert';
export declare const LINE_HEIGHT = 36;
export type ToastSide = 'top' | 'bottom';
export type ToastAlign = 'left' | 'center' | 'right';
export type ToastPosition = `${ToastSide}-${ToastAlign}`;
export declare const toastPositions: readonly ["top-left", "top-center", "top-right", "bottom-left", "bottom-center", "bottom-right"];
export type ToastState = 'pending' | AlertTone;
export type ToastAction = {
    label: string;
    run: () => void;
};
export type ToastInput = {
    id?: string;
    message: string;
    state?: ToastState;
    action?: ToastAction;
    lifetime?: number;
};
export type Note = ToastInput & {
    id: string;
};
export type ToastClock = {
    waits: Map<string, number>;
    since: number | null;
};
export type StackSlot = {
    y: number;
    scale: number;
    opacity: number;
};
export type StackCard = {
    id: string;
    render: (behind: boolean) => ReactNode;
};
export declare function toast(input: string | ToastInput): void;
export declare function dismissToast(id: string): void;
export declare function upsertToast(notes: readonly Note[], note: Note): Note[];
export declare function dismissDelay(state: ToastState | undefined, hasAction: boolean, lifetime?: number): number | null;
export declare function tick(clock: ToastClock, at: number): void;
export declare function pileSlot(index: number): StackSlot;
export declare function fanSlot(index: number, heights: readonly number[]): StackSlot;
export declare function Toasts({ position }: {
    position?: ToastPosition;
}): import("react").JSX.Element;
