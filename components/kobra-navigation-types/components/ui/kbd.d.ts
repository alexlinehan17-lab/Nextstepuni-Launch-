declare const kbdSizes: {
    readonly sm: "h-4 min-w-4 rounded-sm px-1 text-[0.625rem] [&_svg:not([class*='size-'])]:size-2.5";
    readonly md: "h-5 min-w-5 rounded-sm px-1 text-xs [&_svg:not([class*='size-'])]:size-3";
    readonly lg: "h-6 min-w-6 rounded-md px-1.5 text-[0.8125rem] [&_svg:not([class*='size-'])]:size-3.5";
    readonly xl: "h-7 min-w-7 rounded-lg px-2 text-sm [&_svg:not([class*='size-'])]:size-4";
};
type KbdSize = keyof typeof kbdSizes;
declare function Kbd({ className, size, ...props }: React.ComponentProps<'kbd'> & {
    size?: KbdSize;
}): import("react").JSX.Element;
declare function KbdGroup({ className, ...props }: React.ComponentProps<'div'>): import("react").JSX.Element;
export { Kbd, KbdGroup, kbdSizes };
export type { KbdSize };
