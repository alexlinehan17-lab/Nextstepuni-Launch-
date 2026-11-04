import { Button as ButtonPrimitive } from '@base-ui/react/button';
import { type VariantProps } from 'class-variance-authority';
declare const buttonVariants: (props?: {
    variant?: "outline" | "default" | "secondary" | "ghost" | "destructive" | "link" | "push";
    size?: "default" | "xs" | "sm" | "lg" | "icon" | "icon-xs" | "icon-sm" | "icon-lg";
    rounded?: boolean;
    flat?: boolean;
} & import("class-variance-authority/types").ClassProp) => string;
export declare const surfaceCalm: (length: number) => number;
declare function Button({ className, variant, size, rounded, flat, ref, ...props }: ButtonPrimitive.Props & VariantProps<typeof buttonVariants>): import("react").JSX.Element;
export { Button, buttonVariants };
