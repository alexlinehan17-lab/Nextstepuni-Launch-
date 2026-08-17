/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { getFirestore, FieldValue, Timestamp } from "firebase-admin/firestore";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import {
  FEEDBACK_RETENTION_DAYS,
  feedbackLimitReached,
  feedbackRateLimitId,
  isEligibleFeedbackUser,
  validateFeedbackRequest,
  type FeedbackRequest,
} from "./anonymousFeedbackPolicy";

/**
 * Accept product feedback without persisting any account identifier.
 *
 * Authentication is required so the public endpoint cannot be used as an open
 * message relay. The UID is used only in-memory to derive a rotating,
 * pseudonymous rate-limit bucket; neither the UID nor that bucket is written
 * to the feedback record the administrator reads. App Check should additionally be enforced
 * once every released web/native client has been registered for attestation.
 */
export const submitAnonymousFeedback = onCall(
  { cors: true, maxInstances: 10 },
  async request => {
    if (!request.auth) {
      throw new HttpsError("unauthenticated", "Must be logged in.");
    }

    const data = (request.data || {}) as FeedbackRequest;
    const validation = validateFeedbackRequest(data);
    if (!validation.ok && validation.reason === "category") {
      throw new HttpsError("invalid-argument", "Choose a feedback category.");
    }
    if (!validation.ok && validation.reason === "message") {
      throw new HttpsError("invalid-argument", "Feedback must be between 10 and 2,000 characters.");
    }
    if (!validation.ok) {
      throw new HttpsError("invalid-argument", "Invalid platform.");
    }

    const db = getFirestore();
    const userSnapshot = await db.collection("users").doc(request.auth.uid).get();
    if (!isEligibleFeedbackUser(userSnapshot.data())) {
      throw new HttpsError("permission-denied", "Only student accounts can send feedback.");
    }

    const { category, message, context, platform, appVersion } = validation.value;
    const now = new Date();
    const day = now.toISOString().slice(0, 10);
    const rateLimitId = feedbackRateLimitId(request.auth.uid, day);
    const rateLimitRef = db.collection("feedbackRateLimits").doc(rateLimitId);
    const feedbackRef = db.collection("anonymousFeedback").doc();
    const expiresAt = Timestamp.fromDate(new Date(now.getTime() + FEEDBACK_RETENTION_DAYS * 24 * 60 * 60 * 1000));

    await db.runTransaction(async transaction => {
      const rateLimitSnapshot = await transaction.get(rateLimitRef);
      const currentCount = rateLimitSnapshot.exists
        ? Number(rateLimitSnapshot.data()?.count || 0)
        : 0;
      if (feedbackLimitReached(currentCount)) {
        throw new HttpsError(
          "resource-exhausted",
          "You have sent several messages today. Please try again tomorrow.",
        );
      }

      transaction.set(rateLimitRef, {
        count: currentCount + 1,
        day,
        expiresAt: Timestamp.fromDate(new Date(now.getTime() + 48 * 60 * 60 * 1000)),
      });
      transaction.create(feedbackRef, {
        category,
        message,
        context,
        platform,
        appVersion,
        status: "new",
        createdAt: FieldValue.serverTimestamp(),
        expiresAt,
      });
    });

    return { success: true as const };
  },
);
