/**
 * Generic, estate-agnostic lifecycle mechanism. The states and transition
 * table are the caller's business decision — this file only supplies the
 * enforcement mechanism (canTransition / assertTransition), generalized
 * from the concrete lifecycle baobab-platform/zuribeans proved out in
 * docs/adr/0006-supplier-registration-data-ownership.md.
 */
export type TransitionTable<TStatus extends string> = Readonly<Record<TStatus, readonly TStatus[]>>

export interface Lifecycle<TStatus extends string> {
  canTransition(from: TStatus, to: TStatus): boolean
  assertTransition(from: TStatus, to: TStatus): void
}

export const createLifecycle = <TStatus extends string>(
  transitions: TransitionTable<TStatus>,
): Lifecycle<TStatus> => {
  const canTransition = (from: TStatus, to: TStatus): boolean => transitions[from].includes(to)

  const assertTransition = (from: TStatus, to: TStatus): void => {
    if (!canTransition(from, to)) {
      throw new Error(`Cannot transition a supplier onboarding case from "${from}" to "${to}".`)
    }
  }

  return { canTransition, assertTransition }
}

/**
 * The concrete lifecycle baobab-platform/zuribeans proved out for its supplier
 * registration vertical slice (ADR-0006). Estates may reuse it as-is via
 * `supplierApplicationLifecycle`, or define their own status union and pass
 * a different transition table to `createLifecycle` if their qualification
 * process genuinely differs — the mechanism above does not assume this
 * specific shape.
 */
export const SUPPLIER_APPLICATION_STATUSES = [
  "draft",
  "submitted",
  "under_review",
  "more_information_required",
  "sample_required",
  "qualification",
  "approved",
  "rejected",
  "active",
  "suspended",
  "offboarded",
] as const

export type SupplierApplicationStatus = (typeof SUPPLIER_APPLICATION_STATUSES)[number]

export const SUPPLIER_APPLICATION_TRANSITIONS: TransitionTable<SupplierApplicationStatus> = {
  draft: ["submitted"],
  submitted: ["under_review"],
  under_review: ["more_information_required", "sample_required", "qualification", "rejected"],
  more_information_required: ["under_review"],
  sample_required: ["under_review"],
  qualification: ["approved", "rejected"],
  approved: ["active"],
  rejected: [],
  active: ["suspended", "offboarded"],
  suspended: ["active", "offboarded"],
  offboarded: [],
}

export const supplierApplicationLifecycle: Lifecycle<SupplierApplicationStatus> = createLifecycle(
  SUPPLIER_APPLICATION_TRANSITIONS,
)
