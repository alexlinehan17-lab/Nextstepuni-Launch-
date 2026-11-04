// Generated declarations for the compiled control runtime.
export interface Searchable {
    label: string;
    keywords?: Array<string>;
    disabled?: boolean;
}
export declare function matches(option: Searchable, query: string): boolean;
export declare function rank(label: string, query: string): 0 | 2 | 3 | 1;
export declare function search<T extends Searchable>(options: Array<T>, query: string): Array<T>;
