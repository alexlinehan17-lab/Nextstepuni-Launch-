import * as React from 'react';
import { Menu as MenuPrimitive } from '@base-ui/react/menu';
type DropdownMenuSize = 'sm' | 'default';
declare function DropdownMenu({ ...props }: MenuPrimitive.Root.Props): React.JSX.Element;
declare function DropdownMenuPortal({ ...props }: MenuPrimitive.Portal.Props): React.JSX.Element;
declare function DropdownMenuTrigger({ className, onPointerDown, ...props }: MenuPrimitive.Trigger.Props): React.JSX.Element;
declare function DropdownMenuContent({ className, align, alignOffset, side, sideOffset, size, ...props }: MenuPrimitive.Popup.Props & Pick<MenuPrimitive.Positioner.Props, 'align' | 'alignOffset' | 'side' | 'sideOffset'> & {
    size?: DropdownMenuSize;
}): React.JSX.Element;
declare function DropdownMenuGroup({ ...props }: MenuPrimitive.Group.Props): React.JSX.Element;
declare function DropdownMenuLabel({ className, inset, ...props }: MenuPrimitive.GroupLabel.Props & {
    inset?: boolean;
}): React.JSX.Element;
declare function DropdownMenuItem({ className, inset, variant, highlighted, ...props }: MenuPrimitive.Item.Props & {
    inset?: boolean;
    variant?: 'default' | 'destructive';
    highlighted?: boolean;
}): React.JSX.Element;
declare function DropdownMenuSub({ ...props }: MenuPrimitive.SubmenuRoot.Props): React.JSX.Element;
declare function DropdownMenuSubTrigger({ className, inset, children, highlighted, ...props }: MenuPrimitive.SubmenuTrigger.Props & {
    inset?: boolean;
    highlighted?: boolean;
}): React.JSX.Element;
declare function DropdownMenuSubContent({ className, align, alignOffset, side, sideOffset, ...props }: React.ComponentProps<typeof DropdownMenuContent>): React.JSX.Element;
declare function DropdownMenuCheckboxItem({ className, children, checked, inset, marked, ...props }: MenuPrimitive.CheckboxItem.Props & {
    inset?: boolean;
    marked?: boolean;
}): React.JSX.Element;
declare function DropdownMenuRadioGroup({ ...props }: MenuPrimitive.RadioGroup.Props): React.JSX.Element;
declare function DropdownMenuRadioItem({ className, children, inset, marked, ...props }: MenuPrimitive.RadioItem.Props & {
    inset?: boolean;
    marked?: boolean;
}): React.JSX.Element;
declare function DropdownMenuSeparator({ className, ...props }: MenuPrimitive.Separator.Props): React.JSX.Element;
declare function DropdownMenuShortcut({ className, ...props }: React.ComponentProps<'span'>): React.JSX.Element;
export type { DropdownMenuSize };
export { DropdownMenu, DropdownMenuPortal, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuGroup, DropdownMenuLabel, DropdownMenuItem, DropdownMenuCheckboxItem, DropdownMenuRadioGroup, DropdownMenuRadioItem, DropdownMenuSeparator, DropdownMenuShortcut, DropdownMenuSub, DropdownMenuSubTrigger, DropdownMenuSubContent, };
