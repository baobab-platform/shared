import { z } from "zod"
import { SUPPLIER_APPLICATION_STATUSES } from "./lifecycle"

/**
 * Generalized from baobab-platform/zuribeans' `supplier_organisations` table
 * (ADR-0006), with two deliberate differences that keep it estate-agnostic:
 *
 * - `applicantIdentityRef` replaces Zuribeans' `medusaCustomerId`. Each
 *   estate owns its own applicant identity (Zuribeans: a Medusa customer;
 *   Thamani: whatever its own future account system mints) — this package
 *   only defines the join point, never the identity system itself.
 * - `canonicalOrganisationId` remains reserved, nullable, and unpopulated
 *   here for the same reason it is in Zuribeans: baobab-platform/baobab-cp has no
 *   canonical Organisation type yet, and baobab-platform/shared's own
 *   contracts/erp/v1/system-of-record.yaml deliberately keeps the
 *   "Organisation" concept's canonical_owner "unassigned" until an explicit
 *   contract is approved (that invariant is CI-enforced there — this
 *   package must never imply an owner exists).
 */
export const supplierApplicationStatusSchema = z.enum(SUPPLIER_APPLICATION_STATUSES)

export const supplierOrganisationSchema = z.object({
  id: z.string().optional(),
  /** Opaque reference to the authenticated applicant identity in the hosting estate. */
  applicantIdentityRef: z.string(),
  legalName: z.string().min(1),
  registrationNumber: z.string().nullable().default(null),
  taxIdentifier: z.string().nullable().default(null),
  /** ISO 3166-1 alpha-2. */
  countryCode: z.string().length(2),
  status: supplierApplicationStatusSchema.default("draft"),
  /** Reserved for reconciliation once a canonical Organisation owner is approved. Never populated by this package. */
  canonicalOrganisationId: z.string().nullable().default(null),
  createdAt: z.string().datetime().optional(),
  updatedAt: z.string().datetime().optional(),
  submittedAt: z.string().datetime().nullable().default(null),
})
export type SupplierOrganisation = z.infer<typeof supplierOrganisationSchema>

export const supplierContactSchema = z.object({
  id: z.string().optional(),
  supplierOrganisationId: z.string(),
  name: z.string().min(1),
  email: z.string().email(),
  role: z.string().min(1),
  phone: z.string().nullable().default(null),
  createdAt: z.string().datetime().optional(),
})
export type SupplierContact = z.infer<typeof supplierContactSchema>
