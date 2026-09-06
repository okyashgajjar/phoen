# DealFlow360 — System Design Fixes

What changed in this pass, why, and what is still open.

---

## The root cause

606 of 719 quotation lines (84%) had **no link to any catalog record** — just
free text. Everything downstream depends on that link:

  * no variant  → no inventory row → the split engine found zero stock and every
    order silently became a backorder
  * no category → no discount ceiling → the blended risk score fell back to a
    flat rate for every line, so **tier and category discount governance never
    actually applied**

### Why the fix is not "import the CSV column"

`seed-data-mumbai/quotation_lines.csv` has a `product_variant_id` column, and
importing it looks like the obvious repair. It is wrong. **The database was
seeded from a different generation of the dataset than the current CSVs.**

Measured:

| check | agreement |
|---|---|
| variant names vs `product_variants.csv` | 121 / 652 |
| variant parent vs CSV parent | 132 / 652 |
| product names vs `products.csv` | 97 / 361 |
| variant name aligns with **DB** catalog name | **473** |
| variant name aligns with **CSV** product name | 107 |

So the database is the internally coherent generation and the one to trust.
Importing that CSV column attaches a "Dell USB-C Dock" line to an HPE ProLiant
server — only 19 of 392 such links survived a description check. Every id
resolves, so the import succeeds silently and the corruption is invisible.

`scripts/backfill_line_links.py` instead matches each line's **own description
text** against variant and catalog item names using Jaccard token overlap, and
writes a link only at ≥0.75 confidence. Weaker matches are left NULL on purpose:
a null link is a visible gap, a wrong link is a silent corruption.

```
python scripts/backfill_line_links.py --dry-run   # report first
python scripts/backfill_line_links.py
```

Result: 321 exact + 127 fuzzy = **462 of 719 linked**, 349 resolving to a real
category, 56 recurring lines correctly flagged. Spot-checked: dock → CAT-PERIPH,
laptop → CAT-COMP.

> **SQLite on mounted or synced folders** can fail with `disk I/O error`. Copy
> the DB to a local disk, run the scripts, copy it back. `DEALFLOW_DB` and
> `DATABASE_URL` both let you point the scripts at a copy.

## 1. Status vocabulary was breaking the API

The seeded data carries **18 distinct status spellings** across three
vocabularies — `Approved`, `CONFIRMED`, `Confirmed`, `Sent`, `ISSUED`,
`Approved by Sarah Jenkins`, … — while the Pydantic enum allowed six.

Any approved quotation therefore raised a validation error and **500'd the
endpoint**. 198 of 198 quotations now parse.

- `QuotationStatus` extended to the real lifecycle: DRAFT → PENDING_APPROVAL →
  APPROVED → READY → NEGOTIATION → CONFIRMED → DISPATCHED → PAID → WON, plus
  REJECTED / EXPIRED.
- `normalize_status()` added in `backend/models/sales.py` as the single
  normaliser, including prefix matching for `"Approved by <name>"` forms.
- `backend/models/base.py` now calls it instead of its own partial inline map.

## 2. Discount engine — real governance, not a flat threshold

`backend/services/discount_engine.py` was rewritten, backed by a new
`backend/services/pricing_rules.py` resolver.

Before: read `db.list("discount_tiers")` and `db.list("category_discount_ceilings")`,
both of which returned **hardcoded Python literals**, and looked the customer up
in the `users` table (customers live in `customers`).

Now: every ceiling comes from the `pricing_rules` table
(`rule_type = DISCOUNT_LIMIT`), resolved most-specific-first:

```
TIER + CATEGORY  →  CATEGORY  →  TIER  →  GLOBAL
```

The blended score is the **higher of**:

- **worst line** — the largest single-line breach, so one line 8 points over its
  own ceiling requires approval even when the headline tier number looks fine;
- **value-weighted spread** — catches many small breaches that individually look
  harmless but give away real margin across the order.

`evaluate_quotation()` returns the full per-line breakdown (given / allowed /
over-by / which rule decided it), which is exactly what Screen 6 needs to
explain *why* a quote was flagged.

Verified against live data: `QT-0012`, SMB tier, `CAT-INFRA` allows 7%, 10% was
given → 3.0 points over → routed to Sales Manager.

## 3. Routing engine — clean quotes can now skip approval

Before: **every** quotation returned `PENDING_APPROVAL`, including clean ones, so
nothing could ever auto-approve.

Now: score 0 → `READY`. Otherwise Sales Manager up to 5 points, Sales Manager
then Finance beyond that. A rule authored as `L3_VP_COMMERCIAL` / `L4_CFO`
escalates to Finance regardless of band. `build_approval_chain()` emits the
ordered steps with Finance present only when required, as the mockup specifies.

## 4. Split engine — allocates against real inventory

Before: read `warehouse.stock[product_id]` — a dict that **does not exist** on the
`Warehouse` model. Stock was always zero, so every order backordered. Costs were
`len(splits) * 15.0` and warehouse names and serial numbers were hardcoded
fallbacks.

Now: joins `inventory → variant → catalog_item`, reserves against
`available_quantity − reserved_quantity`, and prefers a single warehouse that can
cover the whole line, splitting largest-first only when none can — which keeps
shipment count at the minimum. Backorders carry the real
`next_expected_restock` date that drives the consolidation prompt. Approving an
order now actually reserves the stock.

Verified: `QT-0004` splits across Hyderabad Cyber Logistics Center and Delhi NCR
Enterprise Supply Hub, 2 shipments.

## 5. Billing engine — real hybrid billing and real proration

Before: fell back to a hardcoded order total of `28600.0`, an `mrr` of
`$900/mo`, and `calculate_proration()` returned the constant `15.50` for every
change.

Now: one-time and recurring lines are separated, the invoice is computed from
actual line nets plus tax with the due date from the customer's own
`payment_terms_days`, and each recurring line becomes a schedule with a real
cycle length and next-bill date.

`calculate_proration()` credits the unused portion of the current cycle and
charges the new rate for the days remaining; a negative delta flags that a credit
note is due. `calculate_cancellation_refund()` added for the cancel flow.

## 6. `DATABASE_URL` is now honoured for SQLite

`database/config.py` ignored `DATABASE_URL` on the SQLite path and always bound to
the repo-root file, so the app could not be pointed at a test or scratch copy.
Relative `sqlite:///./x.db` URLs now resolve against the project root rather than
the current working directory.

Also set `APP_DEBUG=false` in `.env` — it was echoing every SQL statement to the
console.

## 7. Odoo theme

The UI was blue (`#2563eb`, 281 occurrences) and the footer still branded the
product "Phoen".

- Odoo palette applied across 16 files: plum `#714B67` primary, `#5C3D54` hover,
  teal `#017E84` secondary, `#212529` ink, `#F9F9F9` ground.
- Tailwind's `blue-*` / `indigo-*` scales mapped to an equivalent plum scale at
  matching lightness steps.
- Design tokens added to `src/index.css` as CSS custom properties
  (`--odoo-primary`, …) plus `.odoo-btn-primary` / `.odoo-btn-secondary`, so
  future work sets a variable instead of chasing hex codes.
- Rebranded to DealFlow360.

---

## 8. Upsell / cross-sell engine — built from scratch

The suggestion panel (spec B5) is step 4 of the judged test flow and **did not
exist**: no table, no data, no service, no endpoint, and no UI. `grep -i upsell
src/` returned nothing.

**Four tables added** to `database/models.py`: `product_recommendations`,
`deal_health`, `approval_chains`, `warehouse_allocations`.

**Recommendations are generated from the database's own order history**, not
imported from `product_recommendations.csv`. The CSV is the other data
generation, so its 744 pairs reference products that mean something different in
this database — the ids resolve, the pairings are wrong.
`scripts/build_recommendations.py` mines real co-purchase pairs out of
`document_lines`:

```
co_purchase_rate = co-occurrences / times the source appears
confidence       = rate damped by evidence volume, so a 1-of-1 pair
                   does not outrank a 40-of-60 pair
type             = UPSELL (same category, dearer) / CROSS_SELL / ATTACHMENT
```

917 co-purchase pairs across 198 source products, plus 270 category-affinity
fallbacks at low confidence so the panel is never empty during a demo. Genuine
evidence always outranks a fallback.

`backend/services/upsell_engine.py` ranks them
(0.45 confidence + 0.25 co-purchase + 0.20 margin + 0.10 promo, minus a priority
penalty), filters anything already in the cart, and **enforces the spec's
minimum margin floor** so thin-margin suggestions never surface.
`margin_impact()` returns what accepting one does to the order's blended margin.

Live output:

```
CROSS_SELL  Jabra Evolve2 40 MS USB-C Wired Stereo    margin 23.53%  [PROMO]
  why: Bought together on 2 of 4 orders containing HP E24 G4 23.8-inch
  → order margin 11.63% → 11.70% (+0.07 pts), adds ₹10,200
```

100 of 113 quotations produce live suggestions.

**Three endpoints added** to `backend/routers/quotations.py`:

| endpoint | purpose |
|---|---|
| `GET /quotations/{id}/suggestions` | ranked panel data |
| `GET /quotations/{id}/suggestions/{product_id}/impact` | margin preview before accepting |
| `GET /quotations/{id}/risk` | per-line breakdown for "Why This Quote Was Flagged" (spec B4) |

**UI**: `src/components/UpsellPanel.jsx` — ranked cards with type badge, promo
tag, margin delta, the co-purchase reason, a hover margin preview, and Add to
Quote / Dismiss. Mounted in the quotation detail right column; accepting a
suggestion adds a real line so totals, margin and risk score all recompute.

## 9. Discount Tier & Approval Chain Setup — mockup Screen 18

The screen the demo's first step needs ("set up a discount tier") did not exist,
so the ceilings driving the entire approval flow could only be changed in SQL.

**`backend/routers/governance.py`** — five endpoints, admin-gated for writes:

| endpoint | purpose |
|---|---|
| `GET /governance/config` | tiers, categories, every ceiling in force, approval bands |
| `PUT /governance/ceilings` | upsert tier / category / tier×category ceilings |
| `DELETE /governance/ceilings/{id}` | retire a ceiling (deactivate, so audit keeps its referent) |
| `PUT /governance/approval-chain` | replace the approval bands |
| `GET /governance/impact` | how current ceilings score the open pipeline |

Every write lands in the audit ledger with user, timestamp and reason, which is
the spec's "all approvals, rejections, and edits must be logged" requirement.
Approval bands are validated for inversion and overlap and rejected with a
message naming the two bands that collide.

`GET /governance/impact` is the piece worth demoing. It scores the whole open
pipeline against the ceilings as they stand:

```
before: 55 auto-approved / 27 manager / 31 finance
  → tighten SMB × CAT-INFRA from 7% to 2%
after : 54 auto-approved / 15 manager / 44 finance
```

Twelve quotations changed approver because one cell changed. That is the
governance story the project is about, visible in one screen.

**`src/components/DiscountGovernanceView.jsx`** — the tier × category ceiling
matrix with a per-cell approval level, the approval band table, the live impact
tiles, and a sticky save bar that requires a reason. Non-admins get a read-only
view. Wired at `/governance` with a nav entry for admin, manager and finance.

Verified: config and impact return 200 on real data, a rep's write attempt
returns 403, overlapping bands return 400 with the colliding pair named, and
audit rows are written with the acting user and reason.

## 10. Authentication — real JWT, hashed passwords, a genuinely restricted portal

The bearer token **was the user's own id or email**, so knowing an address was
enough to act as that person. There was no expiry, no revocation, and the eight
accounts lived in a hardcoded `CORE_USERS` dict with plaintext passwords, so
signup never persisted and an account could not be disabled.

**`backend/services/security.py`** — stdlib only, deliberately. bcrypt/argon2
wheels need a build toolchain on some Windows setups and a hackathon cannot
afford "it won't install on the demo laptop":

- PBKDF2-HMAC-SHA256, 240k iterations, per-password salt, constant-time compare
- HS256 JWT with `exp` / `nbf` / `iat` / `iss`, signature verified before the
  payload is trusted
- `alg` is pinned, so the `{"alg":"none"}` forgery is rejected
- legacy plaintext credentials still verify, and are rehashed on first login

**`app_users` table** — accounts now persist. `scripts/seed_users.py` migrates
the personas across and provisions portal logins, preferring customers that
actually have a customer-visible quotation (seeding the first N by id gave
accounts whose quotes were all drafts, so the portal opened empty).

**The portal is now genuinely restricted.** Three separate holes were closed:

1. **Scoping never worked.** The access check compared the quotation's
   `customer_id` to the *user's own id* — two different id spaces. Portal
   accounts now carry a `customer_id` and every read filters on it.
2. **A portal login could list every quotation in the system.** `GET
   /quotations/` accepted any authenticated user and applied that same broken
   filter. The customer role is now refused outright; customers read their own
   through `GET /portal/quotes`.
3. **A customer could set their own price.** The negotiate endpoint wrote the
   customer's requested discount straight onto the line, bypassing discount
   governance entirely. Requests are now recorded in `negotiation_data` for a
   rep to accept or counter.

Cross-tenant reads return **404, not 403** — a 403 would confirm the quotation
exists and let one customer enumerate another's document ids. The customer view
also strips cost basis, margin, blended risk score, approval chain and rep
identity before anything leaves the building.

**Two more bugs surfaced while testing this:**

- `db.update()` silently dropped `negotiation_data`, `warehouse_id`,
  `fulfillment_status` and document `metadata`. The API accepted a customer's
  negotiation request, returned 200, and lost it. Now persisted.
- `_enrich_quotation()` returns *the same dict object* it was given, so building
  the customer view in place rewrote the underlying record's lines with the
  slimmed customer shape. Fixed with a defensive copy.

**`scripts/repair_orphan_customers.py`** — nine customer ids referenced by 40+
sales documents (`cust_acme`, `cust_zenith`, ...) had **no row in `customers`**.
Their tier lookup silently fell back to "Standard", so the discount engine
scored those deals against the wrong ceilings, and no portal login could be
scoped to them. Customer records created, tier inferred from document value.
Zero documents remain orphaned.

**Tests.** 40 of the 47 existing tests were asserting the insecure behaviour —
`assert data["access_token"] == "rep_marcus"` encoded the exact vulnerability
being fixed. They now log in properly through `tests/auth_helper.py`. Three
assertions were changed deliberately, each with the reason recorded in the test:
the "customer cannot access internal routes" test asserted 200 (contradicting
its own name), the cross-tenant check expected 403 where 404 is correct, and
confirmation now yields CONFIRMED rather than WON. Two new tests were added for
the forged-token and tampered-token cases.

**49 tests pass**, up from 47.

## 11. Admin Reporting (Screen 15) and Product Catalog / Detail (Screens 16-17)

### Reporting — `backend/routers/analytics.py`

All four filters the spec names actually narrow the data, and the same filters
are passed to the exports so a downloaded report matches the screen:

```
period=year                           -> 198 quotes
period=week                           ->  18
period=year&approval_status=pending   ->  24
period=year&category_id=CAT-COMP      ->  33
```

KPIs are computed from the documents: quotes created, pipeline value, average
deal size, win rate, average discount, best selling and most discounted
products, and per-rep performance.

Two decisions worth naming:

- **Average approval time returns `null` with a note when no submit/approve
  events are on record**, rather than substituting a plausible constant. The
  older `/reports/dashboard` endpoint still returns a hardcoded
  `win_velocity_days: 11.4` and `active_mrr: 48200.0` — that habit is what this
  avoids, and those two are still worth removing.
- **Unlinked lines are excluded from product rankings.** Aggregated together
  they formed a phantom "Unlinked line" product with 3,806 units that topped
  every chart. They are now reported separately as a data-quality figure
  (142 lines) with a pointer to the backfill script.

**Exports** use openpyxl and reportlab, both already installed. XLSX is a
five-sheet workbook (Summary, Best Selling, Most Discounted, Rep Performance,
Status Breakdown) with Odoo-plum headers and frozen panes; PDF is an A4 report
with the filter set in the header. Both verified as real files (`%PDF-` and
`PK` magic bytes).

### Product catalog — `backend/routers/catalog_products.py`

`/products/` returned a flat model with no variants, price rules or stock, so
there was nothing for a detail screen to render.

- `GET /products/catalog` — Screen 16 list with search, category filter and the
  header counters (458 products, 652 variants, 137 active rules, 20 categories)
- `GET /products/catalog/{id}` — Screen 17: general info, variants with their
  attributes rolled up into the attribute / values / extra-price table the
  mockup shows, tier and currency price lists, and live stock per warehouse

Registered **before** the existing products router, whose `/{product_id}` route
would otherwise match `/catalog` and shadow both endpoints.

### Frontend

- `src/components/ReportsView.jsx` — filter bar, KPI tiles, four tables, and
  working PDF / XLS download buttons
- `src/components/ProductCatalogView.jsx` — serves both screens: catalog list
  without an `:id`, detail panels with one. Honours the mockup's "if
  subscription yes then recurring will be visible" conditional field.
- Routes `/reports`, `/products`, `/products/:id` with nav entries

RBAC verified: analytics and exports are admin/manager/finance only, the catalog
is open to reps too, and the customer role is refused everywhere (403).

---

## Verification

- **49 of 49 backend tests pass** (47 original, updated for the auth rewrite, plus 2 new token-forgery tests).
- All frontend source files compile under esbuild (19 JSX + api.js + index.css).
- API verified end to end against the real database: quotation list, detail,
  risk breakdown, suggestions and margin impact all return 200 with correct data.
- 198 of 198 quotations parse (previously any approved one 500'd).
- Warehouse splits verified across two real warehouses.

Not verified: the full `npm run build`. `node_modules` holds Windows binaries and
cannot run under Linux here, so Tailwind compilation and bundling are unproven.
**Run `npm run build` before you rely on it.**

---

## Still open

0. **Hardcoded values remain in `/reports/dashboard`.** `win_velocity_days:
   11.4`, `active_mrr: 48200.0` and a `total_receivables or 312400.0` fallback
   are still fabricated. The new analytics endpoint computes its equivalents
   properly; the dashboard should be moved onto it.

0b. **A GET mutates state.** `GET /approvals/pending` changes Q-1042's status
   back to PENDING_APPROVAL as a side effect — a read endpoint should never
   write. Found while debugging a test; not yet fixed.


1. **Screens still missing against the mockup.** 15, 16, 17 and 18 are now
   built. Still absent: dedicated **detail routes for fulfilment (8), billing
   (10) and invoices (13)** — those list views exist, but clicking a row has
   nowhere to go. The engines behind them already return the data those screens
   need (`plan_split`, `split_billing_lines`, `calculate_proration`), so this is
   frontend work rather than new backend logic.

2. **Auth is not real.** `dependencies.py` accepts the user's **email as the
   bearer token** and the 8 users live in a hardcoded `CORE_USERS` dict, so
   signup does not persist. The spec explicitly requires the customer portal to
   be "a real, separate, restricted view".

3. **Deal Health uses a flat 15% cap.** `reports.py` still hardcodes
   `disc > 15.0` to flag an anomaly, the same flat-threshold bug fixed
   everywhere else. It should call `evaluate_quotation()` and compare against
   each line's own ceiling. The `deal_health` table is seeded but its rows come
   from the other data generation — prefer computing health live.

4. **`price_lists.csv` has 2,608 rows; `pricing_rules` has 137.** Tier and
   currency pricing is largely unseeded.

5. **257 lines remain unlinked** (description too different to match safely) and
   97 catalog items have no category, so they fall through to the global
   backstop ceiling rather than a category-specific one.

6. **Four duplicate seed folders and three `.db` files.** Collapse to one before
   the demo so nobody loads the wrong one. Note `seed-data-mumbai` is a
   *different generation* from the seeded DB — do not re-import from it blindly.
