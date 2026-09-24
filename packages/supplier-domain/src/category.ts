/**
 * Extensible supplier product-category registry shape. Generalized from
 * baobab-platform/zuribeans' `SUPPLIER_CAPABILITY_CATEGORIES` (ADR-0006): a
 * category is a registry entry, never a dedicated column
 * (`coffee_*`/`vanilla_*`) on the capability schema. The actual category
 * list is a business decision each estate owns for its own supplier base
 * (Zuribeans sources green coffee; Thamani sources general retail goods) —
 * this package defines only the shape and the lookup helper.
 */
export type SupplierCategoryDefinition = {
  key: string
  label: string
}

export type SupplierCategoryRegistry = {
  categories: readonly SupplierCategoryDefinition[]
  isKnownCategory: (value: string) => boolean
}

export const defineCategoryRegistry = (
  categories: readonly SupplierCategoryDefinition[],
): SupplierCategoryRegistry => ({
  categories,
  isKnownCategory: (value: string) => categories.some((category) => category.key === value),
})
