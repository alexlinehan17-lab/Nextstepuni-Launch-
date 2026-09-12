import { createContext, useContext } from 'react';

/** Optional preview boundary. React context also reaches menus rendered in portals. */
export const SubjectAccessContext = createContext<((subject: string) => boolean) | undefined>(undefined);
const allowEverySubject = () => true;
export const useSubjectAccess = () => useContext(SubjectAccessContext) ?? allowEverySubject;
