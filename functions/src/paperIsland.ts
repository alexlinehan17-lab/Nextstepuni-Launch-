import { onCall, HttpsError } from "firebase-functions/v2/https";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { randomInt } from "crypto";
import { CALLABLE_OPTIONS, assertSensitiveAuth } from "./security";
import {
  applyPaperCommand,
  PaperIslandError,
  type PaperCommand,
  type PaperProgress,
} from "./paperIslandModel";

/** Purchases, refunds and the pre-launch reset are one authenticated transaction. */
export const updatePaperIsland = onCall(CALLABLE_OPTIONS, async (request) => {
  if (!request.auth)
    throw new HttpsError("unauthenticated", "Sign in to build your island.");
  await assertSensitiveAuth(request.auth);
  if (!request.data || typeof request.data !== "object")
    throw new HttpsError("invalid-argument", "Choose an island action.");
  const ref = getFirestore().doc(`progress/${request.auth.uid}`);
  try {
    return await getFirestore().runTransaction(async (transaction) => {
      const snapshot = await transaction.get(ref);
      if (!snapshot.exists)
        throw new HttpsError(
          "failed-precondition",
          "Finish setting up your account first.",
        );
      const result = applyPaperCommand(
        snapshot.data() as PaperProgress,
        request.data as PaperCommand,
        () => randomInt(0x100000000) / 0x100000000,
      );
      transaction.update(ref, {
        paperIsland: result.state,
        "pointsData.totalSpent": result.totalSpent,
        ...(result.migrated ? { islandState: FieldValue.delete() } : {}),
      });
      return result;
    });
  } catch (error) {
    if (error instanceof PaperIslandError)
      throw new HttpsError("failed-precondition", error.message);
    throw error;
  }
});
