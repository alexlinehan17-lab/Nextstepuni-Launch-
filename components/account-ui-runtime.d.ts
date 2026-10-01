import type { JSX } from 'react';
import type { Combobox as ComboboxPrimitive } from '@base-ui/react';
import type { Checkbox as CheckboxPrimitive } from '@base-ui/react/checkbox';
import type { Radio as RadioPrimitive } from '@base-ui/react/radio';
import type { RadioGroup as RadioGroupPrimitive } from '@base-ui/react/radio-group';

// Public type surface for the compiled account controls. No editable vendor source.
export declare function Checkbox(props: CheckboxPrimitive.Root.Props & { shape?: 'square' | 'round' }): JSX.Element;
export declare function RadioGroup(props: RadioGroupPrimitive.Props & { animated?: boolean }): JSX.Element;
export declare function RadioGroupItem(props: RadioPrimitive.Root.Props): JSX.Element;
export declare function Combobox<Value, Multiple extends boolean | undefined = false>(props: ComboboxPrimitive.Root.Props<Value, Multiple>): JSX.Element;
export declare function ComboboxTrigger(props: ComboboxPrimitive.Trigger.Props): JSX.Element;
export declare function ComboboxValue(props: ComboboxPrimitive.Value.Props): JSX.Element;
export declare function ComboboxContent(props: ComboboxPrimitive.Popup.Props & Pick<ComboboxPrimitive.Positioner.Props, 'side' | 'align' | 'sideOffset' | 'alignOffset' | 'anchor'>): JSX.Element;
export declare function ComboboxInput(props: ComboboxPrimitive.Input.Props & { showTrigger?: boolean; showClear?: boolean }): JSX.Element;
export declare function ComboboxEmpty(props: ComboboxPrimitive.Empty.Props): JSX.Element;
export declare function ComboboxList(props: ComboboxPrimitive.List.Props): JSX.Element;
export declare function ComboboxItem(props: ComboboxPrimitive.Item.Props): JSX.Element;
