// Generated declarations for the compiled control runtime.
import { type ReactNode } from 'react';
export type CitationSource = {
    name: string;
    title: string;
    url: string;
    description?: string;
    date?: string;
    icon?: ReactNode;
};
export declare function Citation({ sources, className, }: {
    sources: Array<CitationSource>;
    className?: string;
}): import("react").JSX.Element;
