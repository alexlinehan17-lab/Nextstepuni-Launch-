// Generated declarations for the compiled control runtime.
import * as React from 'react';
import { type VariantProps } from 'class-variance-authority';
declare const ALERT_MARKS: {
    readonly error: React.ForwardRefExoticComponent<import("@tabler/icons-react").IconProps & React.RefAttributes<SVGSVGElement>>;
    readonly warning: React.ForwardRefExoticComponent<import("@tabler/icons-react").IconProps & React.RefAttributes<SVGSVGElement>>;
    readonly success: React.ForwardRefExoticComponent<import("@tabler/icons-react").IconProps & React.RefAttributes<SVGSVGElement>>;
    readonly info: React.ForwardRefExoticComponent<import("@tabler/icons-react").IconProps & React.RefAttributes<SVGSVGElement>>;
};
type AlertTone = keyof typeof ALERT_MARKS;
declare const alertVariants: (props?: {
    variant?: "success" | "error" | "warning" | "info";
} & import("class-variance-authority/types").ClassProp) => string;
declare function Alert({ className, variant, children, ...props }: React.ComponentProps<'div'> & VariantProps<typeof alertVariants>): React.JSX.Element;
declare function AlertTitle({ className, ...props }: React.ComponentProps<'div'>): React.JSX.Element;
declare function AlertDescription({ className, ...props }: React.ComponentProps<'div'>): React.JSX.Element;
declare function AlertAction({ className, ...props }: React.ComponentProps<'div'>): React.JSX.Element;
export { Alert, AlertTitle, AlertDescription, AlertAction, ALERT_MARKS, type AlertTone };
