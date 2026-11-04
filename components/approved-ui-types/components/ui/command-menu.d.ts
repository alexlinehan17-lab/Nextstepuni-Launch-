// Generated declarations for the compiled control runtime.
import type { CommandOption as CommandOptionType } from 'kmenu';
import { type ReactNode } from 'react';
export interface CommandMenuAction extends Omit<CommandOptionType, 'children'> {
    icon?: ReactNode;
    shortcut?: Array<string>;
    hint?: string;
    badge?: string;
    crumb?: string;
    hidden?: boolean;
    children?: Array<CommandMenuAction>;
}
declare const OPEN_EVENT = "kobra:open-command-menu";
export declare function openCommandMenu(scope?: string): void;
declare global {
    interface WindowEventMap {
        [OPEN_EVENT]: CustomEvent<{
            scope?: string;
        }>;
    }
}
export declare function CommandMenu({ actions, scopes, placeholder, }: {
    actions: Array<CommandMenuAction>;
    scopes?: Record<string, {
        actions: Array<CommandMenuAction>;
        placeholder: string;
        crumb?: string;
    }>;
    placeholder?: string;
}): import("react").JSX.Element;
export {};
