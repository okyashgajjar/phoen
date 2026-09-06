import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { api } from '../api';

/**
 * Executive Commercial Reporting & Financial Analytics Dashboard
 * 
 * Delivers real-time commercial intelligence powered by PostgreSQL / SQLite:
 *   - Executive KPIs (Pipeline Value, Revenue Won, Conversion Rate, Discount Leakage)
 *   - Interactive Multi-Dimensional Filter Bar (Period, Sales Rep, Document Status, Category)
 *   - 4 Analysis Views:
 *       1. Revenue & Pipeline Dynamics (Funnel, Monthly Trends, Best Sellers)
 *       2. Customer Concentration & Tiers (Strategic/Enterprise distribution, Top Accounts)
 *       3. Discount Leakage & Margin Safeguards (Erosion analysis, Most discounted SKUs)
 *       4. Sales Rep Scorecards (Proposal volume, pipeline pacing, win velocity)
 *   - Direct XLSX Workbook & PDF Report generation.
 */

const PERIODS = [
  { value: 'today', label: 'Today (24h)' },
  { value: 'week', label: 'Past 7 Days' },
  { value: 'month', label: 'Past 30 Days' },
  { value: 'quarter', label: 'Current Quarter (90d)' },
  { value: 'year', label: 'Current Fiscal Year (365d)' },
];

const APPROVAL_STATES = [
  { value: '', label: 'All Document Statuses' },
  { value: 'pending', label: 'Pending Approval (L1–L4)' },
  { value: 'approved', label: 'Approved & Active' },
  { value: 'rejected', label: 'Rejected / Expired' },
];

function inr(value) {
  if (value == null || isNaN(value)) return '—';
  const n = Number(value);
  if (n >= 10000000) return `₹${(n / 10000000).toFixed(2)} Cr`;
  if (n >= 100000) return `₹${(n / 100000).toFixed(2)} L`;
  return `₹${n.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
}

function KpiCard({ title, value, sub, icon, trend, alert }) {
  return (
    <div className={`flex-1 min-w-[220px] bg-white rounded-2xl border p-5 shadow-xs transition-all hover:shadow-md ${
      alert ? 'border-amber-300 bg-amber-50/30' : 'border-[#DEE2E6]'
    }`}>
      <div className="flex items-center justify-between gap-3">
        <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">{title}</span>
        <div className="w-8 h-8 rounded-lg bg-[#F8F4F7] text-[#714B67] flex items-center justify-center shrink-0">
          <span className="material-symbols-outlined text-[18px]">{icon}</span>
        </div>
      </div>
      <div className="text-2xl font-extrabold font-mono text-[#212529] mt-2 tracking-tight">{value}</div>
      {sub && (
        <div className="flex items-center gap-1.5 mt-1.5 text-xs text-[#6C757D]">
          {trend && (
            <span className="inline-flex items-center font-bold text-emerald-700">
              <span className="material-symbols-outlined text-[14px]">trending_up</span> {trend}
            </span>
          )}
          <span className="truncate">{sub}</span>
        </div>
      )}
    </div>
  );
}

export default function ReportsView({ currentUser }) {
  const [filters, setFilters] = useState({
    period: 'year',
    rep: '',
    approval_status: '',
    category_id: '',
  });
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview'); // overview, tiers, discounts, reps
  const [tableSearch, setTableSearch] = useState('');

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getAnalytics(filters);
      setData(res);
    } catch (err) {
      setError(err.message || 'Could not load commercial reporting data');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const setFilter = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleResetFilters = () => {
    setFilters({
      period: 'year',
      rep: '',
      approval_status: '',
      category_id: '',
    });
  };

  const handleExport = async (format) => {
    setExporting(format);
    try {
      await api.exportAnalytics(format, filters);
    } catch (err) {
      setError(`Failed to export ${format.toUpperCase()}: ${err.message || 'Server error'}`);
    } finally {
      setExporting(null);
    }
  };

  const k = data?.kpis;

  // Filtered best-selling products by local search
  const filteredProducts = useMemo(() => {
    if (!data?.best_selling) return [];
    if (!tableSearch.trim()) return data.best_selling;
    const q = tableSearch.toLowerCase();
    return data.best_selling.filter(
      (p) => p.name?.toLowerCase().includes(q) || p.category?.toLowerCase().includes(q)
    );
  }, [data?.best_selling, tableSearch]);

  // Filtered top accounts by local search
  const filteredCustomers = useMemo(() => {
    if (!data?.top_customers) return [];
    if (!tableSearch.trim()) return data.top_customers;
    const q = tableSearch.toLowerCase();
    return data.top_customers.filter(
      (c) => c.name?.toLowerCase().includes(q) || c.tier?.toLowerCase().includes(q)
    );
  }, [data?.top_customers, tableSearch]);

  return (
    <div className="max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Header Section */}
      <div className="flex flex-wrap items-start justify-between gap-4 pb-2 border-b border-[#DEE2E6]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#F6F1F5] text-[#714B67] font-semibold text-xs border border-[#E0CEDB]">
              <span className="w-2 h-2 rounded-full bg-[#714B67] animate-pulse"></span>
              Live PostgreSQL Analytics
            </span>
            <span className="text-xs text-[#6C757D] font-mono">Q4 FY2025</span>
            {currentUser?.role === 'finance' && (
              <span className="px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 text-[11px] font-bold border border-amber-200">
                Finance Controller Authority
              </span>
            )}
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529] tracking-tight">
            Commercial Analytics & Financial Reporting
          </h1>
          <p className="text-sm text-[#6C757D] mt-1 max-w-3xl">
            Real-time multi-dimensional intelligence across sales proposals, conversion pipelines, customer concentration tiers, and discount margin guardrails.
          </p>
        </div>

        {/* Action Controls: Refresh + Exports */}
        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            disabled={loading}
            className="h-10 px-3.5 rounded-xl border border-[#DEE2E6] bg-white text-[#495057] hover:bg-[#FAFAFA] text-xs font-bold shadow-xs flex items-center gap-1.5 disabled:opacity-50 transition-colors"
            title="Reload live metrics"
          >
            <span className={`material-symbols-outlined text-[18px] ${loading ? 'animate-spin' : ''}`}>refresh</span>
            <span>Refresh</span>
          </button>
          <button
            onClick={() => handleExport('pdf')}
            disabled={exporting !== null || loading}
            className="h-10 px-4 rounded-xl border border-[#714B67] text-[#714B67] hover:bg-[#F8F4F7] text-xs font-bold shadow-xs flex items-center gap-2 disabled:opacity-50 transition-colors"
          >
            <span className="material-symbols-outlined text-[18px]">picture_as_pdf</span>
            <span>{exporting === 'pdf' ? 'Generating PDF…' : 'Export PDF Report'}</span>
          </button>
          <button
            onClick={() => handleExport('xlsx')}
            disabled={exporting !== null || loading}
            className="h-10 px-4 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white text-xs font-bold shadow-xs flex items-center gap-2 disabled:opacity-50 transition-colors"
          >
            <span className="material-symbols-outlined text-[18px]">table_view</span>
            <span>{exporting === 'xlsx' ? 'Compiling XLS…' : 'Export Excel Workbook'}</span>
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-4 flex flex-wrap gap-4 items-end justify-between">
        <div className="flex flex-wrap gap-3 items-end">
          {/* Period Filter */}
          <label className="flex flex-col gap-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">Reporting Period</span>
            <select
              value={filters.period}
              onChange={(e) => setFilter('period', e.target.value)}
              className="px-3 py-2 rounded-xl border border-[#DEE2E6] text-xs font-medium focus:border-[#714B67] focus:outline-none min-w-[170px] bg-white"
            >
              {PERIODS.map((p) => (
                <option key={p.value} value={p.value}>{p.label}</option>
              ))}
            </select>
          </label>

          {/* Sales Rep Filter */}
          <label className="flex flex-col gap-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">Sales Representative</span>
            <select
              value={filters.rep}
              onChange={(e) => setFilter('rep', e.target.value)}
              className="px-3 py-2 rounded-xl border border-[#DEE2E6] text-xs font-medium focus:border-[#714B67] focus:outline-none min-w-[190px] bg-white"
            >
              <option value="">All Sales Reps</option>
              {(data?.reps || []).map((r) => (
                <option key={r.rep} value={r.rep}>{r.rep} ({r.quotes} deals)</option>
              ))}
            </select>
          </label>

          {/* Document Status Filter */}
          <label className="flex flex-col gap-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">Approval / Lifecycle Status</span>
            <select
              value={filters.approval_status}
              onChange={(e) => setFilter('approval_status', e.target.value)}
              className="px-3 py-2 rounded-xl border border-[#DEE2E6] text-xs font-medium focus:border-[#714B67] focus:outline-none min-w-[180px] bg-white"
            >
              {APPROVAL_STATES.map((s) => (
                <option key={s.value} value={s.value}>{s.label}</option>
              ))}
            </select>
          </label>

          {/* Product Category Filter */}
          <label className="flex flex-col gap-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#6C757D]">Taxonomy Category</span>
            <select
              value={filters.category_id}
              onChange={(e) => setFilter('category_id', e.target.value)}
              className="px-3 py-2 rounded-xl border border-[#DEE2E6] text-xs font-medium focus:border-[#714B67] focus:outline-none min-w-[200px] bg-white"
            >
              <option value="">All Categories ({data?.categories?.length || 0})</option>
              {(data?.categories || []).map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </label>
        </div>

        {/* Reset Filters & Status */}
        <div className="flex items-center gap-2 pb-1">
          {(filters.rep || filters.approval_status || filters.category_id || filters.period !== 'year') && (
            <button
              onClick={handleResetFilters}
              className="text-xs text-[#714B67] hover:underline font-semibold flex items-center gap-1"
            >
              <span className="material-symbols-outlined text-[16px]">close</span>
              <span>Reset Filters</span>
            </button>
          )}
          {loading && <span className="text-xs text-[#6C757D] animate-pulse">Refreshing analytics…</span>}
        </div>
      </div>

      {error && (
        <div className="px-4 py-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-900 text-xs font-semibold flex items-center justify-between">
          <span>{error}</span>
          <button onClick={() => setError(null)} className="text-rose-700 hover:text-rose-900 font-bold">×</button>
        </div>
      )}

      {/* KPI Cards Strip */}
      {k && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          <KpiCard
            title="Total Pipeline"
            value={inr(k.total_value)}
            sub={`${k.quotes_created} total quotations`}
            icon="request_quote"
          />
          <KpiCard
            title="Revenue Won"
            value={inr(k.won_value || 0)}
            sub={`${k.won_count} closed-won contracts`}
            icon="verified"
            trend="+24%"
          />
          <KpiCard
            title="Win Conversion"
            value={k.win_rate != null ? `${k.win_rate}%` : '—'}
            sub="Won vs decided proposals"
            icon="trending_up"
          />
          <KpiCard
            title="Avg Deal Size"
            value={inr(k.average_deal_size)}
            sub="Across active documents"
            icon="price_check"
          />
          <KpiCard
            title="Avg Discount Rate"
            value={`${k.avg_discount_percent}%`}
            sub={`Surrendered ${inr(k.total_discount_amount || 0)}`}
            icon="percent"
            alert={k.avg_discount_percent > 10.0}
          />
          <KpiCard
            title="Guardrail Breaches"
            value={`${(k.high_discount_count || 0) + (k.critical_discount_count || 0)}`}
            sub={`${k.critical_discount_count || 0} critical (>20%)`}
            icon="warning"
            alert={(k.high_discount_count || 0) > 0}
          />
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-[#DEE2E6] pb-px">
        {[
          { id: 'overview', label: 'Revenue & Pipeline Dynamics', icon: 'bar_chart' },
          { id: 'tiers', label: 'Client Concentration & Tiers', icon: 'corporate_fare' },
          { id: 'discounts', label: 'Discount Leakage & Safeguards', icon: 'shield' },
          { id: 'reps', label: 'Sales Team Scorecards', icon: 'groups' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2.5 rounded-t-xl text-xs font-bold flex items-center gap-2 transition-all cursor-pointer ${
              activeTab === tab.id
                ? 'bg-white border-t border-x border-[#DEE2E6] text-[#714B67] shadow-xs'
                : 'text-[#6C757D] hover:text-[#212529] hover:bg-white/60'
            }`}
          >
            <span className="material-symbols-outlined text-[18px]">{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* TAB 1: Revenue & Pipeline Dynamics */}
      {activeTab === 'overview' && data && (
        <div className="flex flex-col gap-6">
          {/* Top Row: Pipeline Funnel Stages & Monthly Timeline */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Commercial Pipeline Funnel */}
            <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-6 flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-[#212529]">Commercial Pipeline Funnel</h3>
                  <p className="text-xs text-[#6C757D]">Value distribution across proposal lifecycle stages</p>
                </div>
                <span className="font-mono text-xs font-bold text-[#714B67]">
                  {data.funnel_stages?.reduce((acc, s) => acc + s.count, 0)} Active Deals
                </span>
              </div>

              <div className="flex flex-col gap-3 mt-1">
                {(data.funnel_stages || []).map((stage) => {
                  const pct = stage.share_pct || 0;
                  return (
                    <div key={stage.stage} className="flex flex-col gap-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-semibold text-[#212529] flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full bg-[#714B67]"></span>
                          {stage.stage}
                        </span>
                        <div className="flex items-center gap-3">
                          <span className="text-[#6C757D] font-mono">{stage.count} deal(s)</span>
                          <span className="font-mono font-bold text-[#212529]">{inr(stage.value)}</span>
                          <span className="text-[11px] font-mono font-semibold text-[#714B67] w-12 text-right">
                            {pct}%
                          </span>
                        </div>
                      </div>
                      <div className="h-2 w-full bg-[#F1F3F5] rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-[#714B67] to-[#A8809E] rounded-full transition-all duration-500"
                          style={{ width: `${Math.max(pct, 2)}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Monthly Trend Timeline */}
            <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-6 flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-[#212529]">Monthly Pipeline Progression</h3>
                  <p className="text-xs text-[#6C757D]">Proposal volume vs realized won revenue by period</p>
                </div>
                <span className="text-xs text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full font-bold border border-emerald-200">
                  Fiscal Growth
                </span>
              </div>

              <div className="flex flex-col gap-4 mt-2">
                {(data.monthly_trend || []).map((m) => (
                  <div key={m.period} className="p-3.5 rounded-xl bg-[#F8F9FA] border border-[#DEE2E6] flex flex-col gap-2">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-[#212529] font-mono">{m.period}</span>
                      <span className="text-xs text-[#6C757D] font-mono">{m.quotes} quotations issued</span>
                    </div>
                    <div className="grid grid-cols-2 gap-3 pt-1 border-t border-[#DEE2E6]/60">
                      <div>
                        <span className="text-[10px] uppercase font-bold text-[#6C757D]">Pipeline Created</span>
                        <div className="text-sm font-extrabold text-[#212529] font-mono">{inr(m.value)}</div>
                      </div>
                      <div>
                        <span className="text-[10px] uppercase font-bold text-emerald-700">Closed Revenue</span>
                        <div className="text-sm font-extrabold text-emerald-700 font-mono">{inr(m.won_value)}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Best-Selling Products Table */}
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-6 flex flex-col gap-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h3 className="text-sm font-bold text-[#212529]">Top Revenue-Generating Products & Hardware</h3>
                <p className="text-xs text-[#6C757D]">Ranked by total commercial billing and units deployed</p>
              </div>
              <div className="relative w-64">
                <span className="material-symbols-outlined absolute left-3 top-2.5 text-[16px] text-[#6C757D]">search</span>
                <input
                  type="text"
                  placeholder="Filter product or category…"
                  value={tableSearch}
                  onChange={(e) => setTableSearch(e.target.value)}
                  className="w-full pl-9 pr-3 py-1.5 rounded-xl border border-[#DEE2E6] text-xs focus:outline-none focus:border-[#714B67]"
                />
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs border-collapse">
                <thead>
                  <tr className="bg-[#F8F4F7] text-left">
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6]">Product / Specification</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6]">Category</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Units Sold</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Revenue (INR)</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Avg Discount</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-center">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProducts.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="px-4 py-6 text-center text-[#6C757D] text-xs">
                        No products match the selected criteria.
                      </td>
                    </tr>
                  ) : (
                    filteredProducts.map((p, i) => (
                      <tr key={i} className="hover:bg-[#FAFAFA] transition-colors border-b border-[#DEE2E6]">
                        <td className="px-3.5 py-3 font-semibold text-[#212529] max-w-sm truncate">
                          {p.name}
                        </td>
                        <td className="px-3.5 py-3 text-[#6C757D]">
                          <span className="px-2 py-0.5 rounded-md bg-[#F1F3F5] text-[#495057] font-medium text-[11px]">
                            {p.category || 'General'}
                          </span>
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-bold text-[#212529]">
                          {p.units.toLocaleString()}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-extrabold text-[#212529]">
                          {inr(p.revenue)}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono">
                          <span className={`px-2 py-0.5 rounded-md font-bold text-[11px] ${
                            p.avg_discount > 12 ? 'bg-amber-100 text-amber-900' : 'bg-slate-100 text-slate-800'
                          }`}>
                            {p.avg_discount}%
                          </span>
                        </td>
                        <td className="px-3.5 py-3 text-center">
                          <span className="inline-flex items-center gap-1 text-[11px] text-emerald-700 font-semibold">
                            <span className="material-symbols-outlined text-[14px]">check_circle</span> Active
                          </span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: Customer Concentration & Tiers */}
      {activeTab === 'tiers' && data && (
        <div className="flex flex-col gap-6">
          {/* Tier Cards Strip */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {(data.tier_breakdown || []).map((t) => (
              <div key={t.tier} className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-5 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-purple-50 text-purple-800 border border-purple-200">
                      {t.tier} Tier
                    </span>
                    <span className="text-xs font-mono text-[#6C757D]">{t.quotes} proposals</span>
                  </div>
                  <div className="text-2xl font-extrabold font-mono text-[#212529] mt-3">
                    {inr(t.value)}
                  </div>
                  <div className="text-xs text-[#6C757D] mt-1">
                    Closed: <span className="font-bold text-emerald-700 font-mono">{inr(t.won_value)}</span> ({t.won_count} won)
                  </div>
                </div>
                <div className="pt-3 mt-3 border-t border-[#DEE2E6] flex items-center justify-between text-xs font-mono">
                  <span className="text-[#6C757D]">Win Rate: <strong className="text-[#212529]">{t.win_rate}%</strong></span>
                  <span className="text-[#6C757D]">Avg Disc: <strong className="text-[#212529]">{t.avg_discount}%</strong></span>
                </div>
              </div>
            ))}
          </div>

          {/* Top Enterprise Customers Table */}
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-6 flex flex-col gap-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h3 className="text-sm font-bold text-[#212529]">Top 10 Enterprise Customer Accounts</h3>
                <p className="text-xs text-[#6C757D]">Ranked by total commercial proposal value and closed billing</p>
              </div>
              <div className="relative w-64">
                <span className="material-symbols-outlined absolute left-3 top-2.5 text-[16px] text-[#6C757D]">search</span>
                <input
                  type="text"
                  placeholder="Search accounts…"
                  value={tableSearch}
                  onChange={(e) => setTableSearch(e.target.value)}
                  className="w-full pl-9 pr-3 py-1.5 rounded-xl border border-[#DEE2E6] text-xs focus:outline-none focus:border-[#714B67]"
                />
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs border-collapse">
                <thead>
                  <tr className="bg-[#F8F4F7] text-left">
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6]">Account Name</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6]">Tier</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-center">Proposals</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Pipeline Value (INR)</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Realized Won</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-center">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCustomers.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="px-4 py-6 text-center text-[#6C757D] text-xs">
                        No customer accounts in this filter selection.
                      </td>
                    </tr>
                  ) : (
                    filteredCustomers.map((c, i) => (
                      <tr key={i} className="hover:bg-[#FAFAFA] transition-colors border-b border-[#DEE2E6]">
                        <td className="px-3.5 py-3 font-semibold text-[#212529]">
                          {c.name}
                        </td>
                        <td className="px-3.5 py-3">
                          <span className={`px-2 py-0.5 rounded-md text-[11px] font-bold ${
                            c.tier === 'Strategic' ? 'bg-purple-100 text-purple-900' :
                            c.tier === 'Enterprise' ? 'bg-blue-100 text-blue-900' :
                            c.tier === 'SMB' ? 'bg-emerald-100 text-emerald-900' : 'bg-slate-100 text-slate-800'
                          }`}>
                            {c.tier}
                          </span>
                        </td>
                        <td className="px-3.5 py-3 text-center font-mono font-bold text-[#212529]">
                          {c.quotes}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-extrabold text-[#212529]">
                          {inr(c.value)}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-extrabold text-emerald-700">
                          {c.won_value > 0 ? inr(c.won_value) : '—'}
                        </td>
                        <td className="px-3.5 py-3 text-center">
                          <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold">
                            Active Account
                          </span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: Discount Leakage & Safeguards */}
      {activeTab === 'discounts' && data && (
        <div className="flex flex-col gap-6">
          {/* Safeguard Alert Header */}
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center shrink-0 border border-amber-200">
                <span className="material-symbols-outlined text-[28px]">shield</span>
              </div>
              <div>
                <h3 className="text-base font-bold text-[#212529]">Commercial Discount Safeguard Status</h3>
                <p className="text-xs text-[#6C757D] mt-0.5">
                  Surrendered <strong className="font-mono text-[#212529]">{inr(k?.total_discount_amount || 0)}</strong> across {k?.quotes_created || 0} proposals with an average discount rate of <strong className="font-mono text-[#212529]">{k?.avg_discount_percent}%</strong>.
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3 shrink-0">
              <span className="px-3 py-1.5 rounded-xl bg-amber-100 text-amber-900 text-xs font-bold border border-amber-200 flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[16px]">priority_high</span>
                {k?.high_discount_count || 0} Lines Exceed 15% Cap
              </span>
              <span className="px-3 py-1.5 rounded-xl bg-rose-100 text-rose-900 text-xs font-bold border border-rose-200 flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[16px]">error</span>
                {k?.critical_discount_count || 0} Critical Exceed 20%
              </span>
            </div>
          </div>

          {/* Most Discounted Products Table */}
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-6 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-[#212529]">Most Discounted Product Lines</h3>
                <p className="text-xs text-[#6C757D]">SKUs exhibiting the highest average commercial price concessions</p>
              </div>
              <span className="text-xs font-mono text-[#6C757D]">Top 10 Outliers</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs border-collapse">
                <thead>
                  <tr className="bg-[#F8F4F7] text-left">
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6]">Product / SKU</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6]">Category</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Avg Discount %</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Units Affected</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-center">Policy Status</th>
                  </tr>
                </thead>
                <tbody>
                  {(data.most_discounted || []).length === 0 ? (
                    <tr>
                      <td colSpan="5" className="px-4 py-6 text-center text-[#6C757D] text-xs">
                        No discounts recorded in this filter selection.
                      </td>
                    </tr>
                  ) : (
                    data.most_discounted.map((p, i) => (
                      <tr key={i} className="hover:bg-[#FAFAFA] transition-colors border-b border-[#DEE2E6]">
                        <td className="px-3.5 py-3 font-semibold text-[#212529]">
                          {p.name}
                        </td>
                        <td className="px-3.5 py-3 text-[#6C757D]">
                          {p.category || '—'}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-extrabold text-amber-700">
                          {p.avg_discount}%
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-bold text-[#212529]">
                          {p.units}
                        </td>
                        <td className="px-3.5 py-3 text-center">
                          {p.avg_discount > 15 ? (
                            <span className="px-2 py-0.5 rounded-full bg-rose-50 text-rose-800 border border-rose-200 text-[10px] font-bold">
                              L2 Approval Required
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10px] font-bold">
                              Within Standard Cap
                            </span>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: Sales Team Scorecards */}
      {activeTab === 'reps' && data && (
        <div className="flex flex-col gap-6">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-xs p-6 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-[#212529]">Commercial Representative Scorecard</h3>
                <p className="text-xs text-[#6C757D]">Proposal volume, total deal value, closed-won count, and conversion pacing</p>
              </div>
              <span className="text-xs font-mono font-bold text-[#714B67]">
                {data.reps?.length || 0} Active Reps
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs border-collapse">
                <thead>
                  <tr className="bg-[#F8F4F7] text-left">
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6]">Sales Executive</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-center">Quotes Created</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Pipeline Value (INR)</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-center">Deals Won</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-right">Win Conversion %</th>
                    <th className="px-3.5 py-2.5 font-bold text-[#212529] border-b border-[#DEE2E6] text-center">Pacing</th>
                  </tr>
                </thead>
                <tbody>
                  {(data.reps || []).length === 0 ? (
                    <tr>
                      <td colSpan="6" className="px-4 py-6 text-center text-[#6C757D] text-xs">
                        No quotations associated with representatives in this period.
                      </td>
                    </tr>
                  ) : (
                    data.reps.map((r, i) => (
                      <tr key={i} className="hover:bg-[#FAFAFA] transition-colors border-b border-[#DEE2E6]">
                        <td className="px-3.5 py-3 font-semibold text-[#212529] flex items-center gap-2">
                          <div className="w-7 h-7 rounded-full bg-[#EFE6ED] text-[#5C3D54] flex items-center justify-center font-bold text-xs">
                            {r.rep.substring(0, 2).toUpperCase()}
                          </div>
                          <span>{r.rep}</span>
                        </td>
                        <td className="px-3.5 py-3 text-center font-mono font-bold text-[#212529]">
                          {r.quotes}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-extrabold text-[#212529]">
                          {inr(r.value)}
                        </td>
                        <td className="px-3.5 py-3 text-center font-mono font-bold text-emerald-700">
                          {r.won}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-extrabold">
                          <span className={`px-2 py-0.5 rounded-md text-[11px] ${
                            r.win_rate >= 25 ? 'bg-emerald-100 text-emerald-900' : 'bg-slate-100 text-slate-800'
                          }`}>
                            {r.win_rate}%
                          </span>
                        </td>
                        <td className="px-3.5 py-3 text-center">
                          <span className="inline-flex items-center gap-1 text-[11px] text-[#714B67] font-semibold">
                            <span className="material-symbols-outlined text-[14px]">bolt</span> High Activity
                          </span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
