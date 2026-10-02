// Generated declarations for the compiled control runtime.
import { type ComponentProps } from 'react';
type SwitchProps = Omit<ComponentProps<'button'>, 'checked' | 'defaultChecked' | 'onChange'> & {
    checked?: boolean;
    defaultChecked?: boolean;
    onCheckedChange?: (checked: boolean) => void;
};
declare function Switch({ className, checked, defaultChecked, onCheckedChange, onClick, ...props }: SwitchProps): import("react").JSX.Element;
export { Switch };
