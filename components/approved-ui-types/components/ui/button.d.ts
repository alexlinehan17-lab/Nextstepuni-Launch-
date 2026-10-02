// Generated declarations for the compiled control runtime.
import { Button as ButtonPrimitive } from '@base-ui/react/button';
import { type VariantProps } from 'class-variance-authority';
declare const buttonVariants: (props?: {
    variant?: "outline" | "destructive" | "ghost" | "link" | "push" | "default" | "secondary";
    size?: "default" | "xs" | "sm" | "lg" | "icon" | "icon-xs" | "icon-sm" | "icon-lg";
    rounded?: boolean;
} & import("class-variance-authority/types").ClassProp) => string;
declare function Button({ className, variant, size, rounded, ...props }: ButtonPrimitive.Props & VariantProps<typeof buttonVariants>): import("react").JSX.Element;
export { Button, buttonVariants };
