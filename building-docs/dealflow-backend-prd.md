# DealFlow360 — Backend Product Requirements Document (PRD)

## 1. Purpose

DealFlow360 backend must power a self-governing B2B sales operations engine: discount governance with automated approval routing, live upsell/cross-sell scoring, multi-warehouse fulfillment splitting, hybrid (one-time + recurring) billing, deal health monitoring, and a restricted customer negotiation surface. All core business rules — approval routing, discount governance, warehouse splitting, billing proration — must live in application logic, not be hardcoded or faked.

## 2. User Roles & Backend Access

| Role | Backend Capabilities |
|---|---|
| Sales Rep | CRUD own quotations, apply discounts, add upsell lines, view own approval/fulfillment status |
| Sales Manager / Approver | Review/approve/reject quotations over threshold; configure discount tiers & approval chains; view deal health data |
| Finance / Operations | Second-level approval for high-risk discounts; manage warehouse splits & backorders; reconcile recurring billing/credit notes |
| Customer (Portal) | Restricted read/write scope: view own quotation, submit change/negotiation requests, confirm terms — no access to internal workspace endpoints |
| Admin | Full config CRUD: products, price lists, discount tiers, warehouses, subscription plans; platform-wide reporting access |

Role-based access control (RBAC) must be enforced at the API layer, not just hidden in UI.

## 3. Core Backend Modules

### 3.1 Authentication & Authorization (A1)
- Internal users: standard signup/login (email + password, or SSO if implemented), issued session/JWT with role claims.
- Customers: portal login via magic link or email/password, scoped strictly to their own quotation(s).
- Every endpoint must resolve caller role and enforce role-appropriate access; customer tokens must be rejected on any internal-only route.

### 3.2 Product & Price List Management (A2)
- Product entity: name, category, base price, unit, tax, description.
- Variant entity: attribute (e.g. Size/Pack), value, price delta — linked to parent product.
- Price List entity: customer-tier-based pricing, currency-specific overrides.
- Backend must resolve the effective price for a given product + customer tier + currency at quote-build time.

### 3.3 Discount Tier & Approval Chain Engine (A3)
- Discount Tier entity: customer tier (Bronze/Silver/Gold/etc.) → max discount %.
- Category Discount Ceiling entity: category → max discount % (independent of customer tier).
- Approval Chain Rule entity: discount range → required approver sequence (Manager only, or Manager → Finance).
- **Blended Discount Risk Score (core logic)**:
  - For every line, compare given discount % against the *stricter* of (customer tier ceiling, category ceiling).
  - Compute per-line overage (given − allowed, floor 0).
  - Aggregate overage across all lines into one blended score for the order (not just the worst single line) — many small overages must sum into a flag even when no single line looks alarming.
  - Blended score maps to required approval level; if categories with different ceilings are mixed, route to the highest level required by any contributing line.
  - Every approval/rejection/edit event must be logged with user, timestamp, and reason (immutable audit trail).

### 3.4 Warehouse & Fulfillment Engine (A4)
- Warehouse entity: name, stock levels per SKU, replenishment rules.
- Shipping Cost Weighting config: used by auto-split algorithm.
- **Auto-split logic**: given an order's line quantities and live stock across warehouses, compute a fulfillment split that minimizes shipment count while respecting stock availability and shipping cost weighting; must support manual override by Finance/Ops.
- Backorder handling: partial stock must generate a backorder record; when stock replenishes, system must expose a "consolidate remaining backorder" trigger.

### 3.5 Subscription / Recurring Billing Engine (A5)
- Subscription Plan entity: cadence (monthly/quarterly/yearly), attached product/service, proration rules, cancellation/partial-refund rules.
- Order must support mixed lines: one-time and recurring on the same order, billed and tracked separately but reconciled under one order/customer record.
- Proration logic: mid-cycle quantity or plan changes must recompute the current cycle's charge/credit correctly.
- Cancellation logic: must trigger correct partial refund or credit note per configured rules.

### 3.6 Upsell / Cross-Sell Recommendation Engine (A6, optional)
- Product Pairing entity: derived from historical co-purchase data.
- Promotion flag: boosts a product's rank in suggestions.
- Minimum margin threshold: suggestions below threshold must be filtered out before reaching the rep.
- On accept, backend must recompute order total and margin in real time.

### 3.7 Reporting & Dashboard Service (A7)
- Aggregation endpoints for: sales performance, deal health (stalled deals, discount anomalies, delivery slippage), and reporting filters (Period, Sales Team/Rep, Approval Status, Product/Category).
- Export support: PDF / XLS generation.
- Discount anomaly detection: flag discounts materially above a given rep's historical average.
- Stalled deal detection: quotations inactive beyond a configurable threshold (days).

### 3.8 Customer Portal API (backend for B8)
- Strictly scoped endpoints separate from internal workspace APIs.
- Supports: view quotation + status, line-level comments/change requests, counter-discount proposal, one-click confirm.
- On confirm: if final terms exceed approval thresholds, backend must automatically re-trigger the approval flow (3.3); otherwise auto-transition order to fulfillment.

## 4. Key Backend Business Rules (must be enforced server-side, not UI-only)

1. Discount approval routing is always computed server-side from live tier/category ceilings — never trusts client-submitted "requires approval" flags.
2. Blended risk score recalculates on every line edit, not just at submit time.
3. Warehouse split recalculates against live stock, not cached stock, at confirm time.
4. Subscription proration math is centralized in one billing service — no duplicate proration logic in fulfillment or portal modules.
5. Customer portal negotiation changes that cross approval thresholds cannot bypass the approval engine (no direct-to-fulfillment path from the portal once thresholds are exceeded).
6. All approval, discount override, and fulfillment override actions write an audit log entry (actor, timestamp, before/after state, reason).

## 5. Core Data Entities (minimum set)

`User (role)`, `Customer`, `Product`, `ProductVariant`, `PriceList`, `DiscountTier`, `CategoryDiscountCeiling`, `ApprovalChainRule`, `Quotation`, `QuotationLine`, `ApprovalEvent`, `Warehouse`, `StockLevel`, `FulfillmentSplit`, `BackorderRecord`, `SubscriptionPlan`, `BillingSchedule`, `Invoice`, `CreditNote`, `UpsellRule`, `AuditLogEntry`.

## 6. Non-Functional Requirements

- Real-time recompute of margin/total on line changes (low-latency read of price/stock/discount state).
- Full audit trail persistence for all approval and override actions.
- Strict RBAC isolation between internal workspace and customer portal APIs.
- Technology-agnostic: any backend language/framework/DB is acceptable; requirement is correct business logic, not a specific stack.
- Multi-currency / multi-company support: bonus, not required for MVP.

## 7. Acceptance Test Flow (backend must support end-to-end)

1. Set up a discount tier, warehouse, and subscription plan via config APIs.
2. Create a quotation, add a line with discount above allowed ceiling → API must auto-flag for manager approval without a manual request.
3. Accept an upsell suggestion → order total/margin update via API in real time.
4. Approve the quotation → stock pulled from correct warehouse(s), splitting across two if needed.
5. Confirm one-time + recurring lines on same order bill correctly and separately.
6. Customer portal requests larger discount → API auto re-enters approval flow.
7. Confirm order, record payment → invoice status updates correctly.

## 8. Out of Scope (for this backend PRD)

- Frontend screen implementations (covered in product's B1–B9 UI spec).
- Multi-currency/multi-company (bonus only).
- Non-core integrations not mentioned in source spec.
