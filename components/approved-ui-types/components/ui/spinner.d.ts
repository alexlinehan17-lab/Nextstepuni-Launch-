// Generated declarations for the compiled control runtime.
type SpinnerVariant = 'default' | 'gradient' | 'bars';
declare function Spinner({ className, variant, ...props }: React.ComponentProps<'svg'> & {
    variant?: SpinnerVariant;
}): import("react").JSX.Element;
type CheckState = 'loading' | 'done';
declare function StatusBadge({ state, label, chime, variant, spinner, }: {
    state?: CheckState;
    label?: string;
    chime?: boolean;
    variant?: 'solid' | 'outline';
    spinner?: SpinnerVariant;
}): import("react").JSX.Element;
export { Spinner, StatusBadge, type CheckState, type SpinnerVariant };
