import { useCallback, useRef } from 'react';
import { useModuleResponses } from './useModuleResponses';
import type { Dispatch, SetStateAction } from 'react';

export function useModuleDraft<T>(moduleId: string, key: string, initial: T): [T, Dispatch<SetStateAction<T>>] {
  const { responses, saveResponse } = useModuleResponses(moduleId);
  const value = responses[key] === undefined ? initial : responses[key] as T;
  const current = useRef(value); current.current = value;
  const update = useCallback<Dispatch<SetStateAction<T>>>(next => {
    current.current = typeof next === 'function' ? (next as (previous: T) => T)(current.current) : next;
    saveResponse(key, current.current);
  }, [key, saveResponse]);
  return [value, update];
}
