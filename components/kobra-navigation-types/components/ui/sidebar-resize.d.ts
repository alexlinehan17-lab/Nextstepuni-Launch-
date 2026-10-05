export declare function SidebarResize({ width, minWidth, maxWidth, defaultWidth, onWidthChange, onResizingChange }: {
    width: number;
    minWidth: number;
    maxWidth: number;
    defaultWidth: number;
    onWidthChange: (width: number) => void;
    onResizingChange: (resizing: boolean) => void;
}): import("react").JSX.Element;
