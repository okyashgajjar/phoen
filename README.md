# DealFlow360 — B2B Sales Operations Engine

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[React + Vite](https://vitejs.dev/)

## Project Overview

DealFlow360 is a **self-governing B2B sales operations engine** that powers discount governance with automated approval routing, live upsell/cross-sell scoring, multi-warehouse fulfillment splitting, hybrid (one-time + recurring) billing, deal health monitoring, and a restricted customer negotiation surface. All core business rules live in application logic, not hardcoded or faked.

The system consists of a **FastAPI backend** (Python) and a **React + Vite frontend** that together provide a complete CPQ (Configure, Price, Quote) and revenue operations platform.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Backend Framework** | FastAPI |
| **Database** | Mock in-memory DB (extensible to PostgreSQL) |
| **API** | RESTful JSON via FastAPI |
| **Frontend** | React 18 + Vite |
| **Styling** | TailwindCSS |
| **Auth** | JWT / Session cookies (magic link capable) |

---

## User Roles & RBAC

| Role | Capabilities |
|---|---|
| **Sales Rep** | CRUD own quotations, apply discounts, add upsell lines, view own approval/fulfillment status |
| **Sales Manager / Approver** | Review/approve/reject quotations over threshold; configure discount tiers & approval chains; view deal health data |
| **Finance / Operations** | Second-level approval for high-risk discounts; manage warehouse splits & backorders; reconcile recurring billing/credit notes |
| **Customer (Portal)** | Restricted read/write: view own quotation, submit change/negotiation requests, confirm terms — no access to internal workspace endpoints |
| **Admin** | Full config CRUD: products, price lists, discount tiers, warehouses, subscription plans; platform-wide reporting access |

> **RBAC is enforced at the API layer**, not just hidden in UI. Customer tokens are rejected on any internal-only route.

---

## Core Backend Modules

| Module | Key Endpoints | PRD Section |
|---|---|---|
| **Authentication** | `POST /auth/signup`, `POST /auth/login`, `GET /auth/me` | A1 |
| **Products & Price Lists** | `GET/POST /products/` | A2 |
| **Discount & Approval Engine** | `GET /approvals/pending`, `GET /approvals/{id}/chain`, `POST /approvals/{id}/approve/reject` | A3 |
| **Warehouse & Fulfillment** | `GET /fulfillment/orders`, `POST /fulfillment/orders/{id}/override`, `GET /fulfillment/backorders`, `POST /fulfillment/backorders/{id}/consolidate` | A4 |
| **Subscription / Billing** | `GET /billing/invoices`, `GET /billing/subscriptions`, `POST /billing/subscriptions/{id}/cancel` | A5 |
| **Upsell / Cross-Sell** | `GET /reports/catalog` | A6 |
| **Reporting & Dashboard** | `GET /reports/dashboard`, `GET /reports/deal-health`, `GET /reports/catalog` | A7 |
| **Customer Portal** | `GET /portal/quotes/{id}`, `POST /portal/quotes/{id}/negotiate`, `POST /portal/quotes/{id}/counter`, `POST /portal/quotes/{id}/confirm` | B8 |

---

## API Endpoints (Full Listing)

### Auth
- `POST /api/v1/auth/signup` — Register new user
- `POST /api/v1/auth/login` — Login (returns JWT)
- `GET /api/v1/auth/me` — Get current user profile

### Products
- `GET /api/v1/products/` — List all products
- `POST /api/v1/products/` — Create product

### Quotations
- `GET /api/v1/quotations/` — List quotations (filtered by role)
- `GET /api/v1/quotations/{id}` — Get quotation detail
- `POST /api/v1/quotations/` — Create new quotation
- `POST /api/v1/quotations/{id}/lines` — Add line item (auto-flags discount violations)
- `PUT /api/v1/quotations/{id}/lines/{line_id}` — Update line item (recalculates risk score)
- `POST /api/v1/quotations/{id}/submit` — Submit for approval (routes based on blended risk score)
- `POST /api/v1/quotations/{id}/lines/{line_id}/flag` — Manual flag toggle

### Approvals
- `GET /api/v1/approvals/pending` — List pending approvals (manager+)
- `GET /api/v1/approvals/{id}/chain` — Get multi-tier approval chain
- `POST /api/v1/approvals/{id}/approve` — Approve quotation (with audit log)
- `POST /api/v1/approvals/{id}/reject` — Reject quotation (with audit log)
- `GET /api/v1/approvals/events/{id}` — Get audit trail for quotation

### Fulfillment
- `GET /api/v1/fulfillment/orders` — List fulfillment splits
- `GET /api/v1/fulfillment/orders/{id}` — Get split detail
- `POST /api/v1/fulfillment/orders/{id}/override` — Manual split override (finance only)
- `GET /api/v1/fulfillment/backorders` — List backorder records
- `POST /api/v1/fulfillment/backorders/{id}/consolidate` — Consolidate backorder (finance)

### Billing
- `GET /api/v1/billing/invoices` — List invoices
- `GET /api/v1/billing/subscriptions` — List billing schedules
- `POST /api/v1/billing/subscriptions/{id}/cancel` — Cancel subscription

### Portal (Customer)
- `GET /api/v1/portal/quotes/{id}` — View quotation (customer-scoped)
- `POST /api/v1/portal/quotes/{id}/negotiate` — Submit discount proposal
- `POST /api/v1/portal/quotes/{id}/counter` — Submit counter-proposal note
- `POST /api/v1/portal/quotes/{id}/confirm` — Confirm quotation (re-enters approval if thresholds exceeded, otherwise WON)

### Reports
- `GET /api/v1/reports/dashboard` — KPI dashboard (manager+)
- `GET /api/v1/reports/deal-health` — Deal health anomalies (manager+)
- `GET /api/v1/reports/catalog` — Catalog rules & products (all roles)

---

## Data Model Summary

### Core Entities

| Entity | Key Fields |
|---|---|
| **User** | id, email, password, role (RoleEnum), name, tier (Gold/Silver/Bronze) |
| **Product** | id, name, category, base_price, unit, is_recurring |
| **DiscountTier** | customer_tier, max_discount_percent (Gold=15%, Silver=10%, Bronze=5%) |
| **CategoryDiscountCeiling** | category, max_discount_percent (Hardware=15%, Software/SaaS=25%, Services=10%) |
| **ApprovalChainRule** | min_blended_score, max_blended_score, required_role (manager/finance) |
| **Quotation** | id, customer_id, sales_rep_id, status, lines, blended_risk_score, amount, margin |
| **QuotationLine** | id, sku, name, category, qty, unit_price, discount_percent, is_recurring, flagged, flagReason |
| **ApprovalEvent** | id, quotation_id, actor_id, action, reason, timestamp, before_state, after_state |
| **Warehouse** | id, name, location, shipping_cost_weighting, stock (per SKU) |
| **FulfillmentSplit** | id, quotation_id, splits (per product+warehouse), estimated_cost, is_manual_override |
| **BackorderRecord** | id, quotation_id, product_id, missing_quantity, resolved |
| **SubscriptionPlan** | cadence (monthly/quarterly/yearly), product_id, proration_rules |
| **BillingSchedule** | quotation_id, subscription_plan_id, start_date, next_billing_date, active |
| **Invoice** | id, quotation_id, amount, due_date, status, is_recurring |
| **UpsellRule** | name, category, threshold, role, active |

---

## End-to-End Workflow

### 1. Quote Creation & Submission

```
Sales Rep → Create Quotation → Add Lines → Discount Auto-Flagging → Submit → Approval Routing
```

1. Sales Rep creates a quotation and adds line items
2. **Every line addition triggers** `calculate_blended_risk_score()` which:
   - Compares discount % against stricter of (customer tier ceiling, category ceiling)
   - Computes per-line overage (given − allowed, floor 0)
   - **Aggregates all overages** into one blended score (many small overages sum into a flag)
3. On submit, `determine_approval_routing(score)` routes to:
   - `READY` if score ≤ 0 (no approval needed)
   - `PENDING_APPROVAL` if score > 0 (manager or finance required based on rule ranges)
4. Quotation status changes flow: `DRAFT → PENDING_APPROVAL → READY → WON/REJECTED`

### 2. Approval Flow

```
Quotation Pending → Manager Reviews Chain → Finance May Be Required → Approve/Reject → Audit Log
```

1. Manager views approval chain via `GET /approvals/{id}/chain`
2. Chain shows 3 tiers (Tier 1: Sales Ops Lead, Tier 2: Finance Administrator, Tier 3: VP Commercial Sales)
3. **Exceptions** are highlighted: discount limit overages, margin floor violations
4. Manager approves → `POST /approvals/{id}/approve`:
   - Updates status to READY
   - Writes audit log entry (actor, timestamp, before/after, reason)
   - Triggers `calculate_warehouse_split()` to auto-split stock across warehouses
5. If finance required, finance approves second tier

### 3. Warehouse Auto-Split

```
Quotation Approved → calculate_warehouse_split() → Fulfillment Split Record
```

1. For each line, algorithm distributes quantity across warehouses:
   - Prefers warehouse with sufficient stock
   - Minimizes shipment count
   - Respects shipping cost weighting
2. If any line has insufficient stock across all warehouses → **BackorderRecord** created
3. Finance can manually override splits via `POST /fulfillment/orders/{id}/override`
4. When stock replenishes → `POST /fulfillment/backorders/{id}/consolidate`

### 4. Customer Portal Negotiation

```
Customer → Submit Negotiation → API Re-enters Approval → Finance Reviews → Confirm → Invoices
```

1. Customer views their quotation via portal
2. Customer submits proposed discounts → `POST /portal/quotes/{id}/negotiate`
3. API re-flags any discounts exceeding category ceilings
4. API recalculates blended risk score and **re-enters approval flow** (`determine_approval_routing`)
5. If final terms exceed thresholds → status reverts to `PENDING_APPROVAL`
6. If within thresholds → status → `WON`, invoices generated via `generate_invoices_and_schedules()`
7. Order contains **both one-time and recurring lines** billed separately but reconciled under one record

### 5. Subscription & Billing

```
Quotation Confirmed → generate_invoices_and_schedules() → Invoices + Billing Schedules
```

1. On confirmation, backend separates lines into:
   - **One-time**: summed into single invoice
   - **Recurring**: each line generates a billing schedule
2. Recurring lines linked to subscription plans (cadence: monthly/quarterly/yearly)
3. Proration logic handles mid-cycle quantity/plan changes
4. Cancellation triggers correct partial refund/credit note per rules

### 6. Deal Health Monitoring

```
Dashboard → Deal Health Endpoint → Anomalies Displayed
```

1. **Stalled deals**: Quotations inactive > 7 days (configurable) → marked medium severity, "Churn Risk"
2. **Discount anomalies**: Blended risk score > 10.0 → flagged HIGH severity
3. **Overdue invoices**: Status = OVERDUE → flagged MEDIUM severity, "Delayed Receivables"
4. Health score aggregated (e.g., 88.4/100)
5. Filters available: Period, Sales Team/Rep, Approval Status, Product/Category

---

## Diagrams (from Wireframe)

The wireframe (`dealflow-wireframe.excalidraw`) defines the following module structure:

### Navigation Tabs (top-level modules)

| Tab | Screen Path | Description |
|---|---|---|
| **Dashboard** | Screen 1 → Screen 2 | Overview KPIs; internal users land on Sales Dashboard; customers land on Quotation Portal |
| **Quotations** | Screen 3 (list) → Screen 4 (detail) | List all quotations; open detail by clicking row |
| **Approvals** | Screen 5 (list) → Screen 6 (detail) | Pending approvals; multi-tier chain view |
| **Fulfillment** | Screen 7 (list) → Screen 8 (detail) | Warehouse splits; backorder management |
| **Subscriptions** | Screen 9 (list) → Screen 10 (detail) | Recurring billing schedules |
| **Invoices** | Screen 11 (list) → Screen 12 (detail) | Invoice status; payment tracking |
| **Deal Health** | Screen 13 → Screen 14 | Anomalies, stalled deals, discount flags |
| **Reports** | Screen 15 | Catalog rules & filtering |

### Customer Portal Screen (Screen 11)

- **My Quotation / Messages / Profile** — accessible from navbar
- Opens customer portal with quotation view, change requests, counter-proposals, one-click confirm

### Login / Signup (Frame "1")

- Entry point for internal users and customers
- Company/team selector for multi-team setups
- Basic validation on email and password fields
- "Forgot Password?" link

### Key UI Concepts from Wireframe

- **White highlighted tab** shows current module
- **Each module** has one list screen (all records) and one detail screen (one record, opened by clicking a row)
- **Customer portal** has restricted scope separate from internal workspace APIs

---

## Acceptance Test Flow (Backend Must Support)

1. Set up a discount tier, warehouse, and subscription plan via config APIs
2. Create a quotation, add a line with discount above allowed ceiling → API must auto-flag for manager approval without a manual request
3. Accept an upsell suggestion → order total/margin update via API in real time
4. Approve the quotation → stock pulled from correct warehouse(s), splitting across two if needed
5. Confirm one-time + recurring lines on same order bill correctly and separately
6. Customer portal requests larger discount → API auto re-enters approval flow
7. Confirm order, record payment → invoice status updates correctly

---

## Development & Running

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- pip, npm

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # if exists, otherwise: fastapi uvicorn python-multipart pydantic
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`
Docs at `http://localhost:8000/docs`

### Frontend

```bash
cd src
npm install
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Seed Data

Run `python backend/seed.py` to populate the mock database with demo data matching the frontend.

---

## Key Business Rules (Enforced Server-Side)

1. **Discount approval routing** is always computed server-side from live tier/category ceilings — never trusts client-submitted "requires approval" flags
2. **Blended risk score** recalculates on every line edit, not just at submit time
3. **Warehouse split** recalculates against live stock, not cached stock, at confirm time
4. **Subscription proration math** is centralized in one billing service — no duplicate proration logic
5. **Customer portal negotiation** changes that cross approval thresholds cannot bypass the approval engine
6. **All approval, discount override, and fulfillment override actions** write an audit log entry (actor, timestamp, before/after state, reason)

---

## Repository Structure

```
phoen/
├── backend/          # FastAPI Python backend
│   ├── main.py       # App entrypoint, router inclusion
│   ├── config.py     # Settings/configuration
│   ├── seed.py      # Demo data seeder
│   ├── models/      # Pydantic models (User, Product, Quotation, etc.)
│   ├── routers/     # API endpoints (auth, products, quotations, approvals, etc.)
│   └── services/    # Business logic (discount_engine, routing_engine, billing_engine, split_engine)
├── src/             # React + Vite frontend
│   ├── App.jsx      # Main app component with tab navigation
│   ├── main.jsx     # React root render
│   ├── api.js       # API service layer (fetch wrapper)
│   └── components/  # UI views (Dashboard, Quotations, Approvals, etc.)
├── building-docs/   # PRD & wireframe specifications
│   ├── dealflow-backend-prd.md
│   ├── dealflow-wireframe.excalidraw
│   └── Dealflow360.pdf
├── README.md        # This file
└── vite.config.js   # Vite configuration
```