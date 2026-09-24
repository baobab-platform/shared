import { z } from "zod"

/**
 * Auditable history of every lifecycle status change. Generalized from
 * baobab-platform/zuribeans' `supplier_status_events` table (ADR-0006): a status
 * change is always recorded with an origin-carrying actor (e.g.
 * "customer:cus_123" or "system"), never a bare name.
 */
export const supplierStatusEventSchema = z.object({
  id: z.string().optional(),
  supplierOrganisationId: z.string(),
  fromStatus: z.string().nullable(),
  toStatus: z.string(),
  actor: z.string().min(1),
  reason: z.string().nullable().default(null),
  occurredAt: z.string().datetime().optional(),
})
export type SupplierStatusEvent = z.infer<typeof supplierStatusEventSchema>
