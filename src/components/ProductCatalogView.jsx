import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../api';

/**
 * Product catalog — mockup Screens 16 and 17.
 *
 * One component serves both: without an :id it renders the catalog list, with
 * an :id it renders the detail panels (general info, variants, price lists).
 * They share the same data shapes and navigation, so splitting them would
 * duplicate the formatting helpers for no benefit.
 */

function inr(v) {
  if (v == null) return '—';
  return `₹${Number(v).toLocaleString('en-IN', { maximumFractionDigits: 2 })}`;
}

function Pill({ children, tone = 'default' }) {
  const tones = {
    default: 'bg-[#F1F1F1] text-[#4A4A4A]',
    plum: 'bg-[#EFE6ED] text-[#5C3D54]',
    teal: 'bg-[#DCEDEE] text-[#01585C]',
    good: 'bg-emerald-50 text-emerald-800',
    warn: 'bg-amber-50 text-amber-800',
  };
  return <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${tones[tone]}`}>{children}</span>;
}

function Stat({ label, value, sub }) {
  return (
    <div className="flex-1 min-w-[150px] bg-white rounded-xl border border-[#DEE2E6] p-4">
      <div className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">{label}</div>
      <div className="text-2xl font-extrabold font-mono text-[#212529] mt-1">{value}</div>
      {sub && <div className="text-[11px] text-[#6C757D] mt-0.5">{sub}</div>}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────
// Screen 16 — catalog list
// ─────────────────────────────────────────────────────────────────────
function CatalogList() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [search, setSearch] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setData(await api.getCatalog({ search, category_id: categoryId, limit: 100 }));
    } catch (err) {
      setError(err.message || 'Could not load catalog');
    } finally {
      setLoading(false);
    }
  }, [search, categoryId]);

  useEffect(() => {
    const t = setTimeout(load, search ? 300 : 0);  // debounce typing
    return () => clearTimeout(t);
  }, [load, search]);

  const s = data?.summary;

  return (
    <div className="max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-extrabold text-[#212529] tracking-tight">Product catalog</h1>
        <p className="text-sm text-[#6C757D] mt-1">Every product, variant and price list in one place.</p>
      </div>

      {s && (
        <div className="flex flex-wrap gap-3">
          <Stat label="Total products" value={s.total_products} sub={`${s.active} active, ${s.archived} archived`} />
          <Stat label="Variants" value={s.variants} sub="SKUs across all products" />
          <Stat label="Pricing rules" value={s.pricing_rules} sub={`${s.categories} categories`} />
        </div>
      )}

      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-4 flex flex-wrap gap-3 items-end">
        <label className="flex flex-col gap-1 flex-1 min-w-[220px]">
          <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">Search</span>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Product name…"
            className="px-3 py-2 rounded-xl border border-[#DEE2E6] text-xs focus:border-[#714B67] focus:outline-none"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">Category</span>
          <select
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
            className="px-3 py-2 rounded-xl border border-[#DEE2E6] text-xs focus:border-[#714B67] focus:outline-none min-w-[200px]"
          >
            <option value="">All categories</option>
            {(data?.categories || []).map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </label>
        {loading && <span className="text-xs text-[#6C757D] pb-2">Loading…</span>}
      </div>

      {error && (
        <div className="px-4 py-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-900 text-xs font-semibold">{error}</div>
      )}

      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-5">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-bold text-[#212529]">Products</h2>
          {data && <span className="text-[11px] text-[#6C757D]">{data.products.length} of {data.total}</span>}
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-xs border-collapse">
            <thead>
              <tr className="bg-[#F8F4F7] text-left">
                {['Product name', 'Category', 'Variants', 'Price', 'Unit', 'Tax', 'Margin', 'Status'].map((h) => (
                  <th key={h} className="px-3 py-2 font-bold text-[#212529] border-b border-[#DEE2E6] whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(data?.products || []).map((p) => (
                <tr
                  key={p.id}
                  onClick={() => navigate(`/products/${p.id}`)}
                  className="hover:bg-[#F8F4F7] cursor-pointer"
                >
                  <td className="px-3 py-2 border-b border-[#DEE2E6]">
                    <div className="font-bold text-[#212529]">{p.name}</div>
                    <div className="text-[10px] text-[#6C757D] font-mono">{p.code}</div>
                  </td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] text-[#4A4A4A]">{p.category || '—'}</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] text-center">{p.variant_count || '—'}</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono font-bold text-[#212529] whitespace-nowrap">
                    {inr(p.base_price)}{p.is_recurring ? <span className="text-[#017E84]">/{(p.billing_frequency || 'mo').toLowerCase()}</span> : null}
                  </td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] text-[#6C757D]">{p.unit}</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] text-[#6C757D]">{p.tax_rate}%</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono">{p.margin_percent}%</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6]">
                    <Pill tone={p.status === 'ACTIVE' ? 'good' : 'default'}>{p.status}</Pill>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-[11px] text-[#6C757D] mt-3">
          Click a product row to open its general info, variants and tier / currency price lists.
        </p>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────
// Screen 17 — product detail
// ─────────────────────────────────────────────────────────────────────
function ProductDetail({ productId }) {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let alive = true;
    api.getProductDetail(productId)
      .then((d) => alive && setData(d))
      .catch((e) => alive && setError(e.message || 'Could not load product'));
    return () => { alive = false; };
  }, [productId]);

  if (error) {
    return (
      <div className="max-w-[1440px] mx-auto px-4 lg:px-8 py-10">
        <div className="px-4 py-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-900 text-xs font-semibold">{error}</div>
      </div>
    );
  }
  if (!data) {
    return <div className="max-w-[1440px] mx-auto px-4 lg:px-8 py-10 text-sm text-[#6C757D]">Loading product…</div>;
  }

  const g = data.general;

  const field = (label, value, hint) => (
    <div className="flex flex-col gap-0.5">
      <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">{label}</span>
      <span className="text-sm text-[#212529] font-semibold">{value ?? '—'}</span>
      {hint && <span className="text-[10px] text-[#6C757D]">{hint}</span>}
    </div>
  );

  return (
    <div className="max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <button
            onClick={() => navigate('/products')}
            className="text-[11px] font-bold text-[#714B67] hover:text-[#5C3D54] mb-1"
          >
            ← Product catalog
          </button>
          <h1 className="text-3xl font-extrabold text-[#212529] tracking-tight">{g.name}</h1>
          <div className="flex flex-wrap items-center gap-2 mt-2">
            <Pill tone="plum">{g.category || 'Uncategorised'}</Pill>
            <Pill>{g.item_type}</Pill>
            {g.is_subscription && <Pill tone="teal">Subscription · {g.billing_frequency || 'Monthly'}</Pill>}
            <Pill tone={g.status === 'ACTIVE' ? 'good' : 'default'}>{g.status}</Pill>
            <span className="text-[11px] text-[#6C757D] font-mono">{g.code}</span>
          </div>
        </div>
        <div className="flex flex-wrap gap-3">
          <Stat label="Qty on hand" value={g.quantity_on_hand} sub={`${data.stock_summary.warehouses} warehouse(s)`} />
          <Stat label="Margin" value={`${g.margin_percent}%`} sub={`Cost ${inr(g.base_cost)}`} />
          <Stat label="Times quoted" value={g.times_quoted} />
        </div>
      </div>

      {/* General info */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
        <h2 className="text-lg font-bold text-[#212529]">General info</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
          {field('Product name', g.name)}
          {field('Category', g.category)}
          {field('Brand', g.brand)}
          {field('Unit', g.unit)}
          {field('Price', inr(g.base_price))}
          {field('Tax %', `${g.tax_rate}%`)}
          {field('Subscription', g.is_subscription ? 'Yes' : 'No')}
          {/* The mockup notes: if subscription is yes, recurring becomes visible */}
          {g.is_subscription
            ? field('Recurring', g.billing_frequency || 'Monthly',
                'Recurring orders are invoiced at the beginning of the period')
            : field('Warranty', g.warranty_months ? `${g.warranty_months} months` : '—')}
          {field('Manufacturer part no.', g.manufacturer_part_number)}
          {field('Quantity on hand', g.quantity_on_hand, 'Live across all warehouses')}
        </div>
        {g.description && (
          <div className="pt-2 border-t border-[#DEE2E6]">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">Description</span>
            <p className="text-xs text-[#4A4A4A] mt-1">{g.description}</p>
          </div>
        )}
      </div>

      {/* Variants */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
        <div>
          <h2 className="text-lg font-bold text-[#212529]">Product variants</h2>
          <p className="text-xs text-[#6C757D]">{data.variants.length} SKU(s), with live stock per warehouse.</p>
        </div>

        {data.attribute_summary.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full text-xs border-collapse mb-3">
              <thead>
                <tr className="bg-[#F8F4F7] text-left">
                  {['Attribute', 'Values', 'Extra price'].map((h) => (
                    <th key={h} className="px-3 py-2 font-bold text-[#212529] border-b border-[#DEE2E6]">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.attribute_summary.map((a) => (
                  <tr key={a.attribute} className="hover:bg-[#FAFAFA]">
                    <td className="px-3 py-2 border-b border-[#DEE2E6] font-bold text-[#212529]">{a.attribute}</td>
                    <td className="px-3 py-2 border-b border-[#DEE2E6] text-[#4A4A4A]">{a.values.join(', ')}</td>
                    <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono text-[#4A4A4A]">
                      {a.extra_prices.map((p) => (p ? `+${inr(p)}` : '0')).join(' / ')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="overflow-x-auto">
          <table className="w-full text-xs border-collapse">
            <thead>
              <tr className="bg-[#F8F4F7] text-left">
                {['SKU', 'Variant', 'Selling price', 'Extra', 'Margin', 'Free stock', 'Warehouses'].map((h) => (
                  <th key={h} className="px-3 py-2 font-bold text-[#212529] border-b border-[#DEE2E6] whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.variants.map((v) => (
                <tr key={v.id} className="hover:bg-[#FAFAFA]">
                  <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono text-[10px] text-[#6C757D]">{v.sku}</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] text-[#212529]">{v.name}</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono font-bold">{inr(v.selling_price)}</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono text-[#6C757D]">
                    {v.extra_price ? `+${inr(v.extra_price)}` : '—'}
                  </td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono">{v.margin_percent}%</td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6]">
                    <Pill tone={v.total_free > 0 ? 'good' : 'warn'}>{v.total_free}</Pill>
                  </td>
                  <td className="px-3 py-2 border-b border-[#DEE2E6] text-[10px] text-[#6C757D]">
                    {v.stock.length
                      ? v.stock.map((s) => `${s.warehouse} (${s.free})`).join(', ')
                      : 'No stock records'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Price lists */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
        <div>
          <h2 className="text-lg font-bold text-[#212529]">Price lists</h2>
          <p className="text-xs text-[#6C757D]">
            Tier and currency rules that apply to this product. These are the same rules the blended
            risk score checks each quotation line against.
          </p>
        </div>
        {data.price_lists.length === 0 ? (
          <p className="text-xs text-[#6C757D] py-3">
            No tier-specific rules. This product falls back to the global ceiling.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs border-collapse">
              <thead>
                <tr className="bg-[#F8F4F7] text-left">
                  {['Tier', 'Currency', 'Price rule', 'Max discount', 'Min margin', 'Approval level'].map((h) => (
                    <th key={h} className="px-3 py-2 font-bold text-[#212529] border-b border-[#DEE2E6] whitespace-nowrap">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.price_lists.map((p) => (
                  <tr key={p.rule_id} className="hover:bg-[#FAFAFA]">
                    <td className="px-3 py-2 border-b border-[#DEE2E6] font-bold text-[#5C3D54]">{p.tier || 'All'}</td>
                    <td className="px-3 py-2 border-b border-[#DEE2E6] text-[#6C757D]">{p.currency}</td>
                    <td className="px-3 py-2 border-b border-[#DEE2E6] text-[#4A4A4A]">{p.rule}</td>
                    <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono">
                      {p.max_discount_percent != null ? `${p.max_discount_percent}%` : '—'}
                    </td>
                    <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono">
                      {p.min_margin_percent != null ? `${p.min_margin_percent}%` : '—'}
                    </td>
                    <td className="px-3 py-2 border-b border-[#DEE2E6] font-mono text-[10px] text-[#6C757D]">
                      {p.approval_level || 'default routing'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ProductCatalogView() {
  const { id } = useParams();
  return id ? <ProductDetail productId={id} /> : <CatalogList />;
}
