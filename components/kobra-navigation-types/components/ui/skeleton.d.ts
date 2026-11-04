type Surface = 'background' | 'shell';
declare function Skeleton({ className, on, ...props }: React.ComponentProps<'div'> & {
    on?: Surface;
}): import("react").JSX.Element;
export { Skeleton };
