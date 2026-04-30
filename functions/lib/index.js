"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.onUserWritten = exports.onProgressWritten = exports.changeOwnPassword = exports.resetStudentPassword = void 0;
const https_1 = require("firebase-functions/v2/https");
const firestore_1 = require("firebase-functions/v2/firestore");
const v2_1 = require("firebase-functions/v2");
const app_1 = require("firebase-admin/app");
const auth_1 = require("firebase-admin/auth");
const firestore_2 = require("firebase-admin/firestore");
const islandProjection_1 = require("./islandProjection");
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
    const db = (0, firestore_2.getFirestore)();
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
    catch (err) {
        console.error('Failed to reset password:', err);
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
    const db = (0, firestore_2.getFirestore)();
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
    catch (err) {
        console.error('Failed to change password:', err);
        throw new https_1.HttpsError("internal", "Failed to change password.");
    }
    return { success: true };
});
/**
 * onProgressWritten
 *
 * Maintains /islandPublic/{uid} as a minimal public projection of a
 * student's island state. Triggered on any write to /progress/{uid}.
 *
 * The projection contains only what other students at the same school
 * see in the Peer Island feature — no academic data, no behavioural
 * timestamps. See compliance/PEER_ISLAND_REFACTOR_PLAN.md and
 * functions/src/islandProjection.ts for the field rationale.
 *
 * Behaviour:
 *   - If progress was deleted: delete the projection.
 *   - If progress exists but is for staff or has no island: delete any
 *     existing projection.
 *   - Otherwise: write/refresh the projection, joining identity fields
 *     from /users/{uid}.
 */
exports.onProgressWritten = (0, firestore_1.onDocumentWritten)("progress/{uid}", async (event) => {
    const uid = event.params.uid;
    const db = (0, firestore_2.getFirestore)();
    const islandPublicRef = db.collection("islandPublic").doc(uid);
    const progressData = event.data?.after?.data();
    if (!progressData) {
        await islandPublicRef.delete().catch((err) => {
            v2_1.logger.warn(`onProgressWritten: failed to delete projection for ${uid}`, err);
        });
        return;
    }
    const userSnap = await db.collection("users").doc(uid).get();
    if (!userSnap.exists) {
        v2_1.logger.warn(`onProgressWritten: user ${uid} not found; deleting any projection`);
        await islandPublicRef.delete().catch(() => { });
        return;
    }
    const projection = (0, islandProjection_1.buildPublicProjection)(userSnap.data(), progressData);
    if (!projection) {
        // Staff account, no island state, or no category — ensure no projection exists.
        await islandPublicRef.delete().catch(() => { });
        return;
    }
    await islandPublicRef.set({
        ...projection,
        updatedAt: firestore_2.FieldValue.serverTimestamp(),
    });
});
/**
 * onUserWritten
 *
 * Refreshes /islandPublic/{uid} when identity fields (name, avatar,
 * school) or role change on /users/{uid}. Also handles the cases where
 * a user is deleted or becomes staff (projection is deleted).
 *
 * Does NOT create a projection from scratch — that requires progress
 * data. If no projection exists when this trigger fires, it does
 * nothing; the progress trigger will create one when relevant data
 * arrives.
 */
exports.onUserWritten = (0, firestore_1.onDocumentWritten)("users/{uid}", async (event) => {
    const uid = event.params.uid;
    const db = (0, firestore_2.getFirestore)();
    const islandPublicRef = db.collection("islandPublic").doc(uid);
    const userData = event.data?.after?.data();
    if (!userData) {
        await islandPublicRef.delete().catch(() => { });
        return;
    }
    if (userData.role === "gc" || userData.role === "admin" || userData.isAdmin === true) {
        await islandPublicRef.delete().catch(() => { });
        return;
    }
    const islandPublicSnap = await islandPublicRef.get();
    if (!islandPublicSnap.exists) {
        // No projection to refresh; the progress trigger will create one
        // if/when an island appears. Avoid creating an empty/stub doc.
        return;
    }
    const progressSnap = await db.collection("progress").doc(uid).get();
    if (!progressSnap.exists) {
        // Existing projection but progress now missing — refresh identity
        // fields only. (Edge case: progress was deleted out-of-band.)
        await islandPublicRef.update({
            name: typeof userData.name === "string" ? userData.name : "Student",
            avatar: typeof userData.avatar === "string" ? userData.avatar : "James",
            school: typeof userData.school === "string" ? userData.school : "",
            updatedAt: firestore_2.FieldValue.serverTimestamp(),
        });
        return;
    }
    const projection = (0, islandProjection_1.buildPublicProjection)(userData, progressSnap.data());
    if (!projection) {
        await islandPublicRef.delete().catch(() => { });
        return;
    }
    await islandPublicRef.set({
        ...projection,
        updatedAt: firestore_2.FieldValue.serverTimestamp(),
    });
});
//# sourceMappingURL=index.js.map