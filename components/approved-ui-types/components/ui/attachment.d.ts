// Generated declarations for the compiled control runtime.
import * as React from 'react';
import { useRender } from '@base-ui/react/use-render';
import { type VariantProps } from 'class-variance-authority';
import { Button } from './button';
declare const attachmentVariants: (props?: {
    size?: "default" | "xs" | "sm";
    orientation?: "horizontal" | "vertical";
} & import("class-variance-authority/types").ClassProp) => string;
declare function Attachment({ className, state, size, orientation, ...props }: React.ComponentProps<'div'> & VariantProps<typeof attachmentVariants> & {
    state?: 'idle' | 'uploading' | 'processing' | 'error' | 'done';
}): React.JSX.Element;
declare const attachmentMediaVariants: (props?: {
    variant?: "image" | "icon";
} & import("class-variance-authority/types").ClassProp) => string;
declare function AttachmentMedia({ className, variant, ...props }: React.ComponentProps<'div'> & VariantProps<typeof attachmentMediaVariants>): React.JSX.Element;
declare function AttachmentContent({ className, ...props }: React.ComponentProps<'div'>): React.JSX.Element;
declare function AttachmentTitle({ className, ...props }: React.ComponentProps<'span'>): React.JSX.Element;
declare function AttachmentDescription({ className, ...props }: React.ComponentProps<'span'>): React.JSX.Element;
declare function AttachmentActions({ className, ...props }: React.ComponentProps<'div'>): React.JSX.Element;
declare function AttachmentAction({ className, variant, size, ...props }: React.ComponentProps<typeof Button>): React.JSX.Element;
declare function AttachmentTrigger({ className, render, type, ...props }: useRender.ComponentProps<'button'>): null;
declare const attachmentGroupVariants: (props?: {
    layout?: "grid" | "scroll";
} & import("class-variance-authority/types").ClassProp) => string;
declare function AttachmentGroup({ className, layout, ...props }: React.ComponentProps<'div'> & VariantProps<typeof attachmentGroupVariants>): React.JSX.Element;
export { Attachment, AttachmentGroup, AttachmentMedia, AttachmentContent, AttachmentTitle, AttachmentDescription, AttachmentActions, AttachmentAction, AttachmentTrigger, };
