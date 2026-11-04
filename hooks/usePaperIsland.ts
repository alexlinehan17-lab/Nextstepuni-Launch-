import { useCallback, useEffect, useRef, useState } from "react";
import { getFunctions, httpsCallable } from "firebase/functions";
import { doc, getDoc } from "firebase/firestore";
import app, { db } from "../firebase";
import { useProgress } from "../contexts/ProgressContext";
import { DEMO_STUDENT_UID } from "../data/devStudent";
import {
  applyPaperCommand,
  type PaperCommand,
  type PaperIsland,
} from "../functions/src/paperIslandModel";

type Result = ReturnType<typeof applyPaperCommand>;
export function usePaperIsland(uid: string) {
  const { rawProgressDoc, updateDemoProgress, reloadProgress } = useProgress();
  const current = useRef(rawProgressDoc);
  current.current = rawProgressDoc;
  const [result, setResult] = useState<Result | null>(null),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const pending = useRef(false),
    mounted = useRef(true);
  const island = useRef<PaperIsland | null>(null);
  const execute = useCallback(
    async (command: PaperCommand) => {
      if (pending.current) return false;
      pending.current = true;
      setBusy(true);
      setError("");
      try {
        let next: Result;
        if (uid === DEMO_STUDENT_UID) {
          next = applyPaperCommand(
            {
              ...current.current,
              paperIsland: island.current ?? current.current.paperIsland,
            },
            command,
          );
          updateDemoProgress((progress) => {
            const { islandState: _old, ...rest } = progress;
            return {
              ...rest,
              paperIsland: next.state,
              pointsData: {
                ...progress.pointsData,
                totalSpent: next.totalSpent,
              },
            };
          });
        } else {
          const call = httpsCallable<PaperCommand, Result>(
            getFunctions(app),
            "updatePaperIsland",
            { timeout: 20000 },
          );
          next = (await call(command)).data;
        }
        if (mounted.current) {
          island.current = next.state;
          setResult(next);
          if (uid !== DEMO_STUDENT_UID) reloadProgress();
        }
        return true;
      } catch (reason) {
        // Re-read after a lost response: a purchase may already have committed.
        if (uid !== DEMO_STUDENT_UID) {
          try {
            const fresh = (await getDoc(doc(db, "progress", uid))).data();
            if (fresh?.paperIsland && mounted.current) {
              island.current = fresh.paperIsland;
              setResult({
                state: fresh.paperIsland,
                totalEarned: fresh.pointsData?.totalEarned ?? 0,
                totalSpent: fresh.pointsData?.totalSpent ?? 0,
                migrated: false,
              });
            }
          } catch {
            /* Keep the last confirmed island. */
          }
        }
        if (mounted.current)
          setError(
            reason instanceof Error
              ? reason.message.replace(/^Firebase:\s*/, "")
              : "Could not save your island. Please try again.",
          );
        return false;
      } finally {
        pending.current = false;
        if (mounted.current) setBusy(false);
      }
    },
    [uid, updateDemoProgress, reloadProgress],
  );
  useEffect(() => {
    mounted.current = true;
    void execute({ action: "open" });
    return () => {
      mounted.current = false;
    };
  }, [execute]);
  // Points earned elsewhere in this session remain visible without reopening Journey.
  const earned = Math.max(
    result?.totalEarned ?? 0,
    rawProgressDoc.pointsData?.totalEarned ?? 0,
  );
  return {
    island: result?.state ?? null,
    balance: Math.max(
      0,
      earned -
        (result?.totalSpent ?? rawProgressDoc.pointsData?.totalSpent ?? 0),
    ),
    busy,
    error,
    execute,
  };
}
