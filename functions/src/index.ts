import { onCall, HttpsError } from "firebase-functions/v2/https";
import { initializeApp } from "firebase-admin/app";
import { getAuth } from "firebase-admin/auth";
import { getFirestore } from "firebase-admin/firestore";

initializeApp();

/**
 * resetStudentPassword
 *
 * Called by a Guidance Counsellor from the GC Dashboard.
 * Verifies the caller is a GC for the student's school,
 * then resets the student's password to a temporary value
 * and returns it for the GC to share with the student.
 */
export const resetStudentPassword = onCall(
  { cors: true },
  async (request) => {
    // Require authentication
    if (!request.auth) {
      throw new HttpsError("unauthenticated", "Must be logged in.");
    }

    const { studentUid } = request.data as { studentUid?: string };
    if (!studentUid || typeof studentUid !== "string") {
      throw new HttpsError("invalid-argument", "studentUid is required.");
    }

    const db = getFirestore();
    const auth = getAuth();

    // Verify caller is a GC
    const callerDoc = await db.collection("users").doc(request.auth.uid).get();
    if (!callerDoc.exists) {
      throw new HttpsError("permission-denied", "Caller not found.");
    }
    const callerData = callerDoc.data()!;
    if (callerData.role !== "gc") {
      throw new HttpsError("permission-denied", "Only guidance counsellors can reset passwords.");
    }

    // Verify student exists and is in the same school
    const studentDoc = await db.collection("users").doc(studentUid).get();
    if (!studentDoc.exists) {
      throw new HttpsError("not-found", "Student not found.");
    }
    const studentData = studentDoc.data()!;
    if (studentData.school !== callerData.school) {
      throw new HttpsError("permission-denied", "Student is not in your school.");
    }

    // Generate a temporary password (8 chars, alphanumeric, easy to read aloud)
    const chars = "abcdefghjkmnpqrstuvwxyz23456789"; // no i/l/o/0/1 to avoid confusion
    let tempPassword = "";
    for (let i = 0; i < 8; i++) {
      tempPassword += chars.charAt(Math.floor(Math.random() * chars.length));
    }

    // Reset the password
    try {
      await auth.updateUser(studentUid, { password: tempPassword });
    } catch {
      throw new HttpsError("internal", "Failed to reset password.");
    }

    return { tempPassword, studentName: studentData.name };
  }
);
