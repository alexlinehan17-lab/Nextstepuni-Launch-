import { useCallback, useRef, useState } from "react";
import { readAnswer, writeAnswer, type AnswerRecord } from "./answerDeskStore";
/** Synchronous per-question saves: no pending debounce to lose on closing a reader. */
export function useAnswerBook(ns: string) {
  const cache = useRef(new Map<string, AnswerRecord>());
  const problems = useRef(new Map<string, string>());
  const [, refresh] = useState(0);
  const get = useCallback(
    (id: string) => {
      if (!cache.current.has(id)) {
        const loaded = readAnswer(ns, id);
        cache.current.set(id, loaded.record);
        if (loaded.problem) problems.current.set(id, loaded.problem);
      }
      return cache.current.get(id)!;
    },
    [ns],
  );
  const change = useCallback(
    (id: string, update: (r: AnswerRecord) => AnswerRecord) => {
      const result = writeAnswer(ns, id, update(get(id)));
      cache.current.set(id, result.record);
      if (result.problem) problems.current.set(id, result.problem);
      else problems.current.delete(id);
      refresh((n) => n + 1);
      return result.record;
    },
    [get, ns],
  );
  return {
    get,
    change,
    problem: (id: string) => problems.current.get(id),
    hasProblems: () => problems.current.size > 0,
  };
}
