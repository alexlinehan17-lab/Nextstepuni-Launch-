import { Tooltip as TooltipPrimitive } from '@base-ui/react/tooltip';
declare function TooltipProvider({ delay, closeDelay, ...props }: TooltipPrimitive.Provider.Props): import("react").JSX.Element;
declare function Tooltip<Payload>({ ...props }: TooltipPrimitive.Root.Props<Payload>): import("react").JSX.Element;
declare function TooltipTrigger<Payload>({ ...props }: TooltipPrimitive.Trigger.Props<Payload>): import("react").JSX.Element;
declare const createTooltipHandle: typeof TooltipPrimitive.createHandle;
declare function TooltipContent({ className, side, sideOffset, align, alignOffset, children, ...props }: TooltipPrimitive.Popup.Props & Pick<TooltipPrimitive.Positioner.Props, 'align' | 'alignOffset' | 'side' | 'sideOffset'>): import("react").JSX.Element;
declare function TooltipArrow({ className, ...props }: TooltipPrimitive.Arrow.Props): import("react").JSX.Element;
export declare function Caption({ children }: {
    children: string;
}): import("react").JSX.Element;
declare function TooltipViewport({ className, ...props }: TooltipPrimitive.Viewport.Props): import("react").JSX.Element;
export { createTooltipHandle, Tooltip, TooltipArrow, TooltipTrigger, TooltipContent, TooltipProvider, TooltipViewport, };
