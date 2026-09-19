import { z } from "zod"
import { verificationStatusSchema } from "./verification"

/**
 * Generalized from baobab-platform/zuribeans' `supplier_capabilities` table
 * (ADR-0006). `category` is a key into the consuming estate's own
 * SupplierCategoryRegistry (see category.ts) — this package does not fix
 * the category list.
 */
export const supplierCapabilitySchema = z.object({
  id: z.string().optional(),
  supplierOrganisationId: z.string(),
  category: z.string().min(1),
  variety: z.string().nullable().default(null),
  grade: z.string().nullable().default(null),
  /** ISO 3166-1 alpha-2. */
  originCountryCode: z.string().length(2).nullable().default(null),
  capacityDescription: z.string().nullable().default(null),
  season: z.string().nullable().default(null),
  leadTimeDays: z.number().int().nonnegative().nullable().default(null),
  verificationStatus: verificationStatusSchema.default("declared"),
  verifiedAt: z.string().datetime().nullable().default(null),
  verifiedBy: z.string().nullable().default(null),
  declaredAt: z.string().datetime().optional(),
})
export type SupplierCapability = z.infer<typeof supplierCapabilitySchema>

export const supplierCapabilityInputSchema = supplierCapabilitySchema.pick({
  category: true,
  variety: true,
  grade: true,
  originCountryCode: true,
  capacityDescription: true,
  season: true,
  leadTimeDays: true,
})
export type SupplierCapabilityInput = z.infer<typeof supplierCapabilityInputSchema>
