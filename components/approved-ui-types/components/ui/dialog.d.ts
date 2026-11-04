// Generated declarations for the compiled control runtime.
import * as React from 'react';
import { Dialog as DialogPrimitive } from '@base-ui/react/dialog';
import { type VariantProps } from 'class-variance-authority';
import { Button } from './button';
declare function Dialog({ ...props }: DialogPrimitive.Root.Props): React.JSX.Element;
declare function DialogTrigger({ ...props }: DialogPrimitive.Trigger.Props): React.JSX.Element;
declare function DialogPortal({ ...props }: DialogPrimitive.Portal.Props): React.JSX.Element;
declare function DialogClose({ ...props }: DialogPrimitive.Close.Props): React.JSX.Element;
declare function DialogOverlay({ className, ...props }: DialogPrimitive.Backdrop.Props): React.JSX.Element;
declare const dialogContentVariants: (props?: {
    size?: "default" | "sm" | "lg" | "md" | "xl";
} & import("class-variance-authority/types").ClassProp) => string;
declare function DialogContent({ className, children, showCloseButton, size, ...props }: DialogPrimitive.Popup.Props & {
    showCloseButton?: boolean;
} & VariantProps<typeof dialogContentVariants>): React.JSX.Element;
declare function DialogHeader({ className, ...props }: React.ComponentProps<'div'>): React.JSX.Element;
declare function DialogFooter({ className, showCloseButton, children, ...props }: React.ComponentProps<'div'> & {
    showCloseButton?: boolean;
}): React.JSX.Element;
declare function DialogTitle({ className, ...props }: DialogPrimitive.Title.Props): React.JSX.Element;
declare function DialogDescription({ className, ...props }: DialogPrimitive.Description.Props): React.JSX.Element;
declare function AlertDialogContent({ className, ...props }: React.ComponentProps<typeof DialogContent>): React.JSX.Element;
declare function AlertDialogCancel({ className, variant, size, ...props }: React.ComponentProps<typeof DialogClose> & Pick<React.ComponentProps<typeof Button>, 'variant' | 'size'>): React.JSX.Element;
declare function AlertDialogAction({ className, ...props }: React.ComponentProps<typeof Button>): React.JSX.Element;
export { Dialog, DialogClose, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogOverlay, DialogPortal, DialogTitle, DialogTrigger, Dialog as AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, DialogDescription as AlertDialogDescription, DialogFooter as AlertDialogFooter, DialogHeader as AlertDialogHeader, DialogOverlay as AlertDialogOverlay, DialogPortal as AlertDialogPortal, DialogTitle as AlertDialogTitle, DialogTrigger as AlertDialogTrigger, };
