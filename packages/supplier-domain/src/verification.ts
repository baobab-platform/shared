import { z } from "zod"

/**
 * Shared by capabilities and certifications: declared != verified.
 * Generalized from baobab-platform/zuribeans' `verification_status` enum
 * (ADR-0006).
 */
export const verificationStatusSchema = z.enum(["declared", "verified", "rejected"])
export type VerificationStatus = z.infer<typeof verificationStatusSchema>

export const verificationRecordSchema = z.object({
  verificationStatus: verificationStatusSchema.default("declared"),
  verifiedAt: z.string().datetime().nullable().default(null),
  verifiedBy: z.string().nullable().default(null),
})
export type VerificationRecord = z.infer<typeof verificationRecordSchema>
