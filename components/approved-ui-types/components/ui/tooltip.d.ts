// Generated declarations for the compiled control runtime.
import { Tooltip as TooltipPrimitive } from '@base-ui/react/tooltip';
import * as React from 'react';
declare function TooltipProvider({ delay, closeDelay, ...props }: TooltipPrimitive.Provider.Props): React.JSX.Element;
declare function Tooltip<Payload>({ ...props }: TooltipPrimitive.Root.Props<Payload>): React.JSX.Element;
declare function TooltipTrigger<Payload>({ ...props }: TooltipPrimitive.Trigger.Props<Payload>): React.JSX.Element;
declare const createTooltipHandle: typeof TooltipPrimitive.createHandle;
declare function TooltipContent({ className, side, sideOffset, align, alignOffset, children, ...props }: TooltipPrimitive.Popup.Props & Pick<TooltipPrimitive.Positioner.Props, 'align' | 'alignOffset' | 'side' | 'sideOffset'>): React.JSX.Element;
declare function TooltipArrow({ className, ...props }: TooltipPrimitive.Arrow.Props): React.JSX.Element;
export declare function Caption({ children }: {
    children: string;
}): React.JSX.Element;
declare function TooltipViewport({ className, ...props }: TooltipPrimitive.Viewport.Props): React.JSX.Element;
export { createTooltipHandle, Tooltip, TooltipArrow, TooltipTrigger, TooltipContent, TooltipProvider, TooltipViewport, };
