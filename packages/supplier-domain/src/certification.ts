import { z } from "zod"
import { verificationStatusSchema } from "./verification"

/** Generalized from baobab-platform/zuribeans' `supplier_certifications` table (ADR-0006). */
export const supplierCertificationSchema = z.object({
  id: z.string().optional(),
  supplierOrganisationId: z.string(),
  certificationType: z.string().min(1),
  issuer: z.string().nullable().default(null),
  referenceNumber: z.string().nullable().default(null),
  issuedOn: z.string().nullable().default(null),
  expiresOn: z.string().nullable().default(null),
  verificationStatus: verificationStatusSchema.default("declared"),
  verifiedAt: z.string().datetime().nullable().default(null),
  verifiedBy: z.string().nullable().default(null),
  declaredAt: z.string().datetime().optional(),
})
export type SupplierCertification = z.infer<typeof supplierCertificationSchema>

export const supplierCertificationInputSchema = supplierCertificationSchema.pick({
  certificationType: true,
  issuer: true,
  referenceNumber: true,
  issuedOn: true,
  expiresOn: true,
})
export type SupplierCertificationInput = z.infer<typeof supplierCertificationInputSchema>
