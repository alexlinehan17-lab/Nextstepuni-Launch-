"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.changeOwnPassword = exports.resetStudentPassword = void 0;
const https_1 = require("firebase-functions/v2/https");
const app_1 = require("firebase-admin/app");
const auth_1 = require("firebase-admin/auth");
const firestore_1 = require("firebase-admin/firestore");
(0, app_1.initializeApp)();
/**
 * resetStudentPassword
 *
 * Called by a Guidance Counsellor from the GC Dashboard.
 * Verifies the caller is a GC for the student's school,
 * then resets the student's password to a temporary value
 * and returns it for the GC to share with the student.
 */
exports.resetStudentPassword = (0, https_1.onCall)({ cors: true }, async (request) => {
    // Require authentication
    if (!request.auth) {
        throw new https_1.HttpsError("unauthenticated", "Must be logged in.");
    }
    const { studentUid } = request.data;
    if (!studentUid || typeof studentUid !== "string") {
        throw new https_1.HttpsError("invalid-argument", "studentUid is required.");
    }
    const db = (0, firestore_1.getFirestore)();
    const auth = (0, auth_1.getAuth)();
    // Verify caller is a GC
    const callerDoc = await db.collection("users").doc(request.auth.uid).get();
    if (!callerDoc.exists) {
        throw new https_1.HttpsError("permission-denied", "Caller not found.");
    }
    const callerData = callerDoc.data();
    if (callerData.role !== "gc") {
        throw new https_1.HttpsError("permission-denied", "Only guidance counsellors can reset passwords.");
    }
    // Verify student exists and is in the same school
    const studentDoc = await db.collection("users").doc(studentUid).get();
    if (!studentDoc.exists) {
        throw new https_1.HttpsError("not-found", "Student not found.");
    }
    const studentData = studentDoc.data();
    if (studentData.school !== callerData.school) {
        throw new https_1.HttpsError("permission-denied", "Student is not in your school.");
    }
    // Generate a temporary password (8 chars, alphanumeric, easy to read aloud)
    const chars = "abcdefghjkmnpqrstuvwxyz23456789"; // no i/l/o/0/1 to avoid confusion
    let tempPassword = "";
    for (let i = 0; i < 8; i++) {
        tempPassword += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    // Reset the password and flag account for password change
    try {
        await auth.updateUser(studentUid, { password: tempPassword });
        await db.collection("users").doc(studentUid).update({ needsPasswordChange: true });
    }
    catch {
        throw new https_1.HttpsError("internal", "Failed to reset password.");
    }
    return { tempPassword, studentName: studentData.name };
});
/**
 * changeOwnPassword
 *
 * Called by a student who has been flagged with needsPasswordChange.
 * Uses Admin SDK to bypass the requires-recent-login restriction.
 */
exports.changeOwnPassword = (0, https_1.onCall)({ cors: true }, async (request) => {
    if (!request.auth) {
        throw new https_1.HttpsError("unauthenticated", "Must be logged in.");
    }
    const { newPassword } = request.data;
    if (!newPassword || typeof newPassword !== "string" || newPassword.length < 6) {
        throw new https_1.HttpsError("invalid-argument", "Password must be at least 6 characters.");
    }
    const db = (0, firestore_1.getFirestore)();
    const auth = (0, auth_1.getAuth)();
    const uid = request.auth.uid;
    // Verify the user actually needs a password change
    const userDoc = await db.collection("users").doc(uid).get();
    if (!userDoc.exists || !userDoc.data()?.needsPasswordChange) {
        throw new https_1.HttpsError("failed-precondition", "No password change required.");
    }
    try {
        await auth.updateUser(uid, { password: newPassword });
        await db.collection("users").doc(uid).update({ needsPasswordChange: false });
    }
    catch {
        throw new https_1.HttpsError("internal", "Failed to change password.");
    }
    return { success: true };
});
//# sourceMappingURL=index.js.map