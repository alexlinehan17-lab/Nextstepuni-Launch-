import { createHash } from "crypto";

export const MIN_PASSWORD_LENGTH = 12;
export const MAX_PASSWORD_LENGTH = 128;
export const RESET_LIFETIME_SECONDS = 24 * 60 * 60;

export function validateNewPassword(value: unknown): string | null {
  if (typeof value !== "string") return "Password is required.";
  if (value.length < MIN_PASSWORD_LENGTH) {
    return `Password must be at least ${MIN_PASSWORD_LENGTH} characters.`;
  }
  if (value.length > MAX_PASSWORD_LENGTH) {
    return `Password must be no more than ${MAX_PASSWORD_LENGTH} characters.`;
  }
  return null;
}

export function hashTemporaryPassword(password: string): string {
  return createHash("sha256").update(password, "utf8").digest("hex");
}

export function resetSessionIsEligible(
  resetAtSeconds: unknown,
  expiresAtSeconds: unknown,
  authTime: number,
  nowSeconds: number,
): boolean {
  return typeof resetAtSeconds === "number"
    && typeof expiresAtSeconds === "number"
    && Number.isFinite(resetAtSeconds)
    && Number.isFinite(expiresAtSeconds)
    && authTime >= resetAtSeconds
    && nowSeconds <= expiresAtSeconds;
}
