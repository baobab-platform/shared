import { describe, expect, it } from "vitest"
import { createLifecycle, supplierApplicationLifecycle } from "../src/lifecycle"

describe("createLifecycle (generic mechanism)", () => {
  type ToyStatus = "open" | "closed"
  const toy = createLifecycle<ToyStatus>({ open: ["closed"], closed: [] })

  it("allows a declared transition", () => {
    expect(toy.canTransition("open", "closed")).toBe(true)
  })

  it("rejects an undeclared transition", () => {
    expect(toy.canTransition("closed", "open")).toBe(false)
  })

  it("throws with a descriptive message for a disallowed transition", () => {
    expect(() => toy.assertTransition("closed", "open")).toThrow(/cannot transition/i)
  })

  it("does not throw for an allowed transition", () => {
    expect(() => toy.assertTransition("open", "closed")).not.toThrow()
  })
})

describe("supplierApplicationLifecycle (proven default, from baobab-platform/zuribeans ADR-0006)", () => {
  it("allows submitting a draft application", () => {
    expect(supplierApplicationLifecycle.canTransition("draft", "submitted")).toBe(true)
  })

  it("does not allow skipping straight from draft to approved", () => {
    expect(supplierApplicationLifecycle.canTransition("draft", "approved")).toBe(false)
  })

  it("allows review to branch into more-information or sample requests", () => {
    expect(supplierApplicationLifecycle.canTransition("under_review", "more_information_required")).toBe(true)
    expect(supplierApplicationLifecycle.canTransition("under_review", "sample_required")).toBe(true)
  })

  it("allows returning from more-information/sample requests back to review", () => {
    expect(supplierApplicationLifecycle.canTransition("more_information_required", "under_review")).toBe(true)
    expect(supplierApplicationLifecycle.canTransition("sample_required", "under_review")).toBe(true)
  })

  it("allows qualification to resolve into approved or rejected", () => {
    expect(supplierApplicationLifecycle.canTransition("qualification", "approved")).toBe(true)
    expect(supplierApplicationLifecycle.canTransition("qualification", "rejected")).toBe(true)
  })

  it("allows active suppliers to be suspended, reactivated, or offboarded", () => {
    expect(supplierApplicationLifecycle.canTransition("active", "suspended")).toBe(true)
    expect(supplierApplicationLifecycle.canTransition("suspended", "active")).toBe(true)
    expect(supplierApplicationLifecycle.canTransition("active", "offboarded")).toBe(true)
    expect(supplierApplicationLifecycle.canTransition("suspended", "offboarded")).toBe(true)
  })

  it("treats rejected and offboarded as terminal", () => {
    expect(supplierApplicationLifecycle.canTransition("rejected", "under_review")).toBe(false)
    expect(supplierApplicationLifecycle.canTransition("offboarded", "active")).toBe(false)
  })

  it("throws for a disallowed transition", () => {
    expect(() => supplierApplicationLifecycle.assertTransition("draft", "approved")).toThrow(/cannot transition/i)
  })
})
