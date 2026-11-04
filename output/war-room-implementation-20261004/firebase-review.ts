// The portable review has no Firebase app, account or writes.
export const db = {};
export const auth = { currentUser: null, authStateReady: () => Promise.resolve() };
