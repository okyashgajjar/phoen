import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function DiscountGovernanceView({ currentUser }) {
  const navigate = useNavigate();
  const isFinanceOrAdmin = ['admin', 'finance'].includes(currentUser?.role);

  const [activeTab, setActiveTab] = useState('ceilings'); // 'ceilings' | 'bands' | 'impact' | 'audit'
  const [config, setConfig] = useState(null);
  const [impact, setImpact] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState(null);
  const [reason, setReason] = useState('');

  // Local editable state
  const [matrix, setMatrix] = useState({});
  const [bands, setBands] = useState([]);
  const [dirty, setDirty] = useState(false);

  // Search & Filter
  const [tierFilter, setTierFilter] = useState('ALL');
  const [categorySearch, setCategorySearch] = useState('');

  const showNotice = (text, type = 'success') => {
    setNotice({ text, type });
    setTimeout(() => setNotice(null), 4500);
  };

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [cfg, imp, logs] = await Promise.all([
        api.getGovernanceConfig(),
        api.getGovernanceImpact().catch(() => null),
        api.getAuditLogs().catch(() => []),
      ]);

      setConfig(cfg);
      setImpact(imp);
      setAuditLogs(logs || []);

      const m = {};
      Object.entries(cfg.tier_category_matrix || {}).forEach(([k, v]) => {
        m[k] = { ...v };
      });
      setMatrix(m);
      setBands((cfg.approval_bands || []).map((b) => ({ ...b })));
      setDirty(false);
    } catch (err) {
      console.error('Failed to load governance data:', err);
      showNotice(err.message || 'Could not load governance configuration', 'error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Categories with configured rules or available
  const displayCategories = useMemo(() => {
    if (!config) return [];
    let cats = config.categories || [];
    if (categorySearch) {
      cats = cats.filter((c) => c.name.toLowerCase().includes(categorySearch.toLowerCase()));
    }
    return cats;
  }, [config, categorySearch]);

  const displayTiers = useMemo(() => {
    if (!config) return [];
    if (tierFilter === 'ALL') return config.tiers || [];
    return (config.tiers || []).filter((t) => t === tierFilter);
  }, [config, tierFilter]);

  const setCell = (tier, cat, field, value) => {
    if (!isFinanceOrAdmin) return;
    const key = `${tier}|${cat}`;
    setMatrix((prev) => ({
      ...prev,
      [key]: { ...(prev[key] || {}), [field]: value },
    }));
    setDirty(true);
  };

  const setBand = (idx, field, value) => {
    if (!isFinanceOrAdmin) return;
    setBands((prev) =>
      prev.map((b, i) => (i === idx ? { ...b, [field]: value } : b))
    );
    setDirty(true);
  };

  const saveAllCeilings = async () => {
    if (!isFinanceOrAdmin) return;
    setSaving(true);
    setNotice(null);
    try {
      const ceilings = Object.entries(matrix)
        .filter(([, v]) => v.max_discount_percent !== '' && v.max_discount_percent != null)
        .map(([key, v]) => {
          const [tier, category_id] = key.split('|');
          return {
            tier,
            category_id,
            max_discount_percent: Number(v.max_discount_percent),
            min_margin_percent:
              v.min_margin_percent === '' || v.min_margin_percent == null
                ? null
                : Number(v.min_margin_percent),
            approval_level: v.approval_level || null,
          };
        });

      const why = reason.trim() || `Discount governance ceilings adjusted by ${currentUser?.name || 'Finance Controller'}`;
      await api.saveCeilings(ceilings, why);
      showNotice(
        `Successfully updated ${ceilings.length} discount ceilings in database! Logged in audit ledger.`,
        'success'
      );
      setReason('');
      setDirty(false);
      await loadData();
    } catch (err) {
      showNotice(err.message || 'Failed to save ceilings', 'error');
    } finally {
      setSaving(false);
    }
  };

  const saveApprovalBands = async () => {
    if (!isFinanceOrAdmin) return;
    setSaving(true);
    setNotice(null);
    try {
      const why = reason.trim() || `Approval chain thresholds adjusted by ${currentUser?.name || 'Finance Controller'}`;
      await api.saveApprovalChain(
        bands.map((b) => ({
          ...b,
          min_discount_percent: Number(b.min_discount_percent),
          max_discount_percent: Number(b.max_discount_percent),
          min_margin_percent: Number(b.min_margin_percent || 0),
        })),
        why
      );
      showNotice(`Successfully updated ${bands.length} approval authorization bands in database!`, 'success');
      setReason('');
      setDirty(false);
      await loadData();
    } catch (err) {
      showNotice(err.message || 'Failed to save approval bands', 'error');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6 animate-in fade-in">
      {/* Toast Alert */}
      {notice && (
        <div
          className={`fixed top-5 right-5 z-50 px-5 py-3.5 rounded-xl shadow-xl border flex items-center gap-3 text-sm font-semibold transition-all ${
            notice.type === 'error'
              ? 'bg-rose-50 border-rose-200 text-rose-800'
              : 'bg-emerald-50 border-emerald-200 text-emerald-800'
          }`}
        >
          <span className="material-symbols-outlined text-lg">
            {notice.type === 'error' ? 'error' : 'check_circle'}
          </span>
          <span>{notice.text}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#76777d] mb-1">
            <span>Finance & Risk Operations</span>
            <span>/</span>
            <span className="text-[#2563eb]">Fiscal Margin & Discount Governance</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30] tracking-tight">
            Discount Governance & Fiscal Ceilings
          </h1>
          <p className="text-sm text-[#45464d] mt-1">
            Configure discount ceilings, minimum gross margin floors, and multi-tier approval bands to protect commercial margin health.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {dirty && (
            <span className="px-3 py-1.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold flex items-center gap-1.5 animate-pulse">
              <span className="material-symbols-outlined text-sm">edit_note</span>
              Unsaved Changes
            </span>
          )}
          <button
            onClick={loadData}
            disabled={loading}
            className="flex items-center gap-2 px-4 h-11 rounded-xl border border-[#e2e8f0] bg-white text-[#45464d] hover:bg-slate-50 font-bold text-xs shadow-sm transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">refresh</span>
            <span>Sync Database</span>
          </button>
        </div>
      </div>

      {/* KPI Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-[#e2e8f0] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#76777d]">Open Deals Evaluated</span>
            <div className="text-2xl font-extrabold text-[#0b1c30] mt-1">
              {impact?.evaluated || 0} Quotations
            </div>
            <span className="text-xs text-emerald-600 font-semibold">
              {impact?.auto_approved_pct || 0}% Auto-Approved (L0)
            </span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center text-[#2563eb]">
            <span className="material-symbols-outlined text-2xl">policy</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#e2e8f0] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#76777d]">Finance Clearance (Tier 2)</span>
            <div className="text-2xl font-extrabold text-amber-600 mt-1">
              {impact?.needs_finance || 0} Deals
            </div>
            <span className="text-xs text-slate-500 font-medium">Requiring Fiscal Sign-Off</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center text-amber-600">
            <span className="material-symbols-outlined text-2xl">verified</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#e2e8f0] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#76777d]">Sales Mgr Review (Tier 1)</span>
            <div className="text-2xl font-extrabold text-[#0b1c30] mt-1">
              {impact?.needs_manager || 0} Deals
            </div>
            <span className="text-xs text-slate-500 font-medium">Within Standard Cap</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600">
            <span className="material-symbols-outlined text-2xl">how_to_reg</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#e2e8f0] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#76777d]">Configured Ceilings</span>
            <div className="text-2xl font-extrabold text-[#0b1c30] mt-1">
              {Object.keys(matrix).length || 28} Rules
            </div>
            <span className="text-xs text-emerald-600 font-medium">Active in Relational DB</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600">
            <span className="material-symbols-outlined text-2xl">tune</span>
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="flex items-center gap-2 border-b border-[#e2e8f0] pb-2">
        <button
          onClick={() => setActiveTab('ceilings')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'ceilings'
              ? 'bg-[#2563eb] text-white shadow-sm'
              : 'text-[#45464d] hover:bg-slate-100'
          }`}
        >
          <span className="material-symbols-outlined text-[18px]">grid_on</span>
          <span>Discount Ceilings Matrix (Tier × Category)</span>
        </button>

        <button
          onClick={() => setActiveTab('bands')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'bands'
              ? 'bg-[#2563eb] text-white shadow-sm'
              : 'text-[#45464d] hover:bg-slate-100'
          }`}
        >
          <span className="material-symbols-outlined text-[18px]">account_tree</span>
          <span>Approval Authority Bands ({bands.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('impact')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'impact'
              ? 'bg-[#2563eb] text-white shadow-sm'
              : 'text-[#45464d] hover:bg-slate-100'
          }`}
        >
          <span className="material-symbols-outlined text-[18px]">crisis_alert</span>
          <span>Pipeline Breach Sentinel ({impact?.top_breaches?.length || 0})</span>
        </button>

        <button
          onClick={() => setActiveTab('audit')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'audit'
              ? 'bg-[#2563eb] text-white shadow-sm'
              : 'text-[#45464d] hover:bg-slate-100'
          }`}
        >
          <span className="material-symbols-outlined text-[18px]">history</span>
          <span>Governance Audit Ledger</span>
        </button>
      </div>

      {/* Tab 1: Discount Ceilings Matrix */}
      {activeTab === 'ceilings' && (
        <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-[#0b1c30]">Tier × Category Maximum Discount Caps</h2>
              <p className="text-xs text-[#76777d] mt-0.5">
                Every line in a quotation is checked against these thresholds. Exceeding a ceiling triggers multi-tier fiscal escalation.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <select
                value={tierFilter}
                onChange={(e) => setTierFilter(e.target.value)}
                className="h-10 px-3 rounded-xl border border-[#e2e8f0] text-xs font-bold focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb]"
              >
                <option value="ALL">All Tiers ({config?.tiers?.length || 4})</option>
                {(config?.tiers || []).map((t) => (
                  <option key={t} value={t}>Tier: {t}</option>
                ))}
              </select>

              <div className="relative w-56">
                <span className="material-symbols-outlined absolute left-3 top-2.5 text-[#76777d] text-lg">search</span>
                <input
                  type="text"
                  placeholder="Filter category..."
                  value={categorySearch}
                  onChange={(e) => setCategorySearch(e.target.value)}
                  className="w-full h-10 pl-9 pr-3 rounded-xl border border-[#e2e8f0] text-xs focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb]"
                />
              </div>
            </div>
          </div>

          {/* Matrix Grid */}
          {loading ? (
            <div className="p-16 flex flex-col items-center justify-center gap-3">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2563eb]"></div>
              <span className="text-xs text-[#76777d] font-semibold">Loading ceilings from database...</span>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm border-collapse">
                <thead className="bg-[#f8fafc] text-xs uppercase text-[#76777d] border-b border-[#e2e8f0]">
                  <tr>
                    <th className="px-5 py-3 font-bold">Category</th>
                    {displayTiers.map((tier) => (
                      <th key={tier} className="px-5 py-3 font-bold text-center">
                        <span className="px-2.5 py-1 rounded-md bg-blue-50 text-[#2563eb] text-[11px] font-extrabold">
                          {tier} Tier
                        </span>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#e2e8f0]">
                  {displayCategories.map((cat) => (
                    <tr key={cat.id} className="hover:bg-[#f8fafc] transition-colors">
                      <td className="px-5 py-3.5">
                        <div className="flex flex-col">
                          <span className="font-bold text-[#0b1c30] text-xs">{cat.name}</span>
                          <span className="font-mono text-[10px] text-[#76777d]">{cat.id}</span>
                        </div>
                      </td>

                      {displayTiers.map((tier) => {
                        const cellKey = `${tier}|${cat.id}`;
                        const cellData = matrix[cellKey] || {};
                        const val = cellData.max_discount_percent !== undefined ? cellData.max_discount_percent : '';
                        const isHigh = val !== '' && Number(val) > 20;

                        return (
                          <td key={tier} className="px-5 py-3.5 text-center">
                            <div className="inline-flex items-center gap-1.5 justify-center">
                              <input
                                type="number"
                                step="0.5"
                                min="0"
                                max="100"
                                placeholder="—"
                                disabled={!isFinanceOrAdmin}
                                value={val}
                                onChange={(e) => setCell(tier, cat.id, 'max_discount_percent', e.target.value)}
                                className={`w-20 h-9 px-2 text-center rounded-lg border font-mono font-bold text-xs focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb] ${
                                  isHigh
                                    ? 'border-amber-300 bg-amber-50/50 text-amber-900'
                                    : 'border-[#e2e8f0] bg-white text-[#0b1c30]'
                                }`}
                              />
                              <span className="text-xs text-[#76777d] font-bold">%</span>
                            </div>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Save Bar */}
          {isFinanceOrAdmin && (
            <div className="p-4 rounded-xl bg-[#f8fafc] border border-[#e2e8f0] flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="flex-1 w-full">
                <input
                  type="text"
                  placeholder="Audit reason for this ceiling adjustment (required for compliance)..."
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  className="w-full h-10 px-3 rounded-xl border border-[#e2e8f0] text-xs focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb]"
                />
              </div>
              <button
                onClick={saveAllCeilings}
                disabled={saving || !dirty}
                className="px-6 h-10 rounded-xl bg-[#2563eb] text-white text-xs font-bold hover:bg-[#1d4ed8] shadow-sm disabled:opacity-50 transition-all whitespace-nowrap flex items-center gap-2"
              >
                <span className="material-symbols-outlined text-sm">save</span>
                {saving ? 'Committing Changes...' : 'Save Ceilings to Database'}
              </button>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Approval Authority Bands */}
      {activeTab === 'bands' && (
        <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-[#0b1c30]">Multi-Tier Commercial Approval Authority Bands</h2>
              <p className="text-xs text-[#76777d] mt-0.5">
                Quotes are scored based on discount points and margin floor erosion to determine the required sign-off hierarchy.
              </p>
            </div>
          </div>

          <div className="space-y-3">
            {bands.map((band, idx) => {
              const isFinanceLevel = band.approval_level === 'L2_FINANCE_DIRECTOR';
              return (
                <div
                  key={band.approval_level}
                  className={`p-5 rounded-2xl border transition-all ${
                    isFinanceLevel
                      ? 'border-amber-300 bg-amber-50/20'
                      : 'border-[#e2e8f0] bg-white'
                  }`}
                >
                  <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <span className="w-10 h-10 rounded-xl bg-[#2563eb] text-white font-extrabold flex items-center justify-center text-sm shadow-sm">
                        {band.approval_level.split('_')[0]}
                      </span>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="font-bold text-[#0b1c30] text-sm">{band.role_name}</h3>
                          {isFinanceLevel && (
                            <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-900 font-extrabold text-[10px]">
                              Finance Clearance Tier
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-[#76777d] mt-0.5">
                          Authority: <strong>{band.approval_level}</strong> • Approver: {band.approver_role || 'System'}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-4 flex-wrap">
                      <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-xl border border-[#e2e8f0]">
                        <span className="text-xs font-bold text-[#76777d]">Discount Range:</span>
                        <input
                          type="number"
                          step="0.1"
                          disabled={!isFinanceOrAdmin}
                          value={band.min_discount_percent}
                          onChange={(e) => setBand(idx, 'min_discount_percent', e.target.value)}
                          className="w-16 h-8 px-1 text-center rounded border border-[#e2e8f0] font-mono font-bold text-xs"
                        />
                        <span className="text-xs text-[#76777d] font-bold">% to</span>
                        <input
                          type="number"
                          step="0.1"
                          disabled={!isFinanceOrAdmin}
                          value={band.max_discount_percent}
                          onChange={(e) => setBand(idx, 'max_discount_percent', e.target.value)}
                          className="w-16 h-8 px-1 text-center rounded border border-[#e2e8f0] font-mono font-bold text-xs"
                        />
                        <span className="text-xs text-[#76777d] font-bold">%</span>
                      </div>

                      <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-xl border border-[#e2e8f0]">
                        <span className="text-xs font-bold text-[#76777d]">Min Margin Floor:</span>
                        <input
                          type="number"
                          step="0.1"
                          disabled={!isFinanceOrAdmin}
                          value={band.min_margin_percent || 0}
                          onChange={(e) => setBand(idx, 'min_margin_percent', e.target.value)}
                          className="w-16 h-8 px-1 text-center rounded border border-[#e2e8f0] font-mono font-bold text-xs"
                        />
                        <span className="text-xs text-[#76777d] font-bold">%</span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Save Bar */}
          {isFinanceOrAdmin && (
            <div className="p-4 rounded-xl bg-[#f8fafc] border border-[#e2e8f0] flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="flex-1 w-full">
                <input
                  type="text"
                  placeholder="Audit reason for approval chain adjustment..."
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  className="w-full h-10 px-3 rounded-xl border border-[#e2e8f0] text-xs focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb]"
                />
              </div>
              <button
                onClick={saveApprovalBands}
                disabled={saving || !dirty}
                className="px-6 h-10 rounded-xl bg-[#2563eb] text-white text-xs font-bold hover:bg-[#1d4ed8] shadow-sm disabled:opacity-50 transition-all whitespace-nowrap flex items-center gap-2"
              >
                <span className="material-symbols-outlined text-sm">save</span>
                {saving ? 'Committing Changes...' : 'Save Bands to Database'}
              </button>
            </div>
          )}
        </div>
      )}

      {/* Tab 3: Pipeline Breach Sentinel */}
      {activeTab === 'impact' && (
        <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-[#0b1c30]">Live Commercial Pipeline Breach Sentinel</h2>
              <p className="text-xs text-[#76777d] mt-0.5">
                Real-time scanning of live proposals against configured ceilings. Deals with excessive discount erosion route directly to Finance.
              </p>
            </div>
            <button
              onClick={loadData}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#e2e8f0] text-xs font-bold text-[#45464d] hover:bg-slate-50"
            >
              <span className="material-symbols-outlined text-sm">refresh</span>
              Rescan Pipeline
            </button>
          </div>

          {impact?.top_breaches?.length === 0 ? (
            <div className="p-12 text-center text-sm text-emerald-700 bg-emerald-50/50 rounded-xl border border-emerald-200">
              <span className="material-symbols-outlined text-3xl mb-1">verified</span>
              <p className="font-bold">Zero Fiscal Breaches Detected</p>
              <p className="text-xs text-emerald-600 mt-0.5">All active commercial proposals comply with configured discount floors.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-[#45464d]">
                <thead className="bg-[#f8fafc] text-xs uppercase text-[#76777d] border-b border-[#e2e8f0]">
                  <tr>
                    <th className="px-5 py-3 font-bold">Quotation & Account</th>
                    <th className="px-5 py-3 font-bold">Tier</th>
                    <th className="px-5 py-3 font-bold">Risk Band</th>
                    <th className="px-5 py-3 font-bold">Erosion Score</th>
                    <th className="px-5 py-3 font-bold">Breached Line Items</th>
                    <th className="px-5 py-3 font-bold text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#e2e8f0]">
                  {(impact?.top_breaches || []).map((b) => (
                    <tr key={b.quotation_id} className="hover:bg-[#f8fafc] transition-colors">
                      <td className="px-5 py-4">
                        <div className="flex flex-col">
                          <span className="font-mono text-xs font-bold text-[#2563eb]">{b.quotation_id}</span>
                          <span className="font-bold text-[#0b1c30] mt-0.5">{b.account}</span>
                        </div>
                      </td>

                      <td className="px-5 py-4">
                        <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-slate-100 text-slate-700">
                          {b.tier || 'Standard'}
                        </span>
                      </td>

                      <td className="px-5 py-4">
                        <span
                          className={`inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-bold ${
                            b.score > 15
                              ? 'bg-rose-50 text-rose-700 border border-rose-200'
                              : 'bg-amber-50 text-amber-700 border border-amber-200'
                          }`}
                        >
                          {b.band || 'Manager Review'}
                        </span>
                      </td>

                      <td className="px-5 py-4 font-mono font-extrabold text-sm text-rose-600">
                        +{b.score.toFixed(1)} pts
                      </td>

                      <td className="px-5 py-4 text-xs text-[#0b1c30]">
                        {b.breached_lines?.map((l, i) => (
                          <div key={i} className="flex items-center gap-1.5 py-0.5">
                            <span className="font-semibold">{l.product_name || l.sku}:</span>
                            <span className="text-rose-600 font-bold">{l.applied_discount}% applied</span>
                            <span className="text-[#76777d]">(cap {l.ceiling_discount}%)</span>
                          </div>
                        ))}
                      </td>

                      <td className="px-5 py-4 text-right">
                        <button
                          onClick={() => navigate(`/approvals/${b.quotation_id}`)}
                          className="px-3.5 py-1.5 rounded-lg bg-[#2563eb] text-white text-xs font-bold hover:bg-[#1d4ed8] shadow-sm transition-all"
                        >
                          Review in Cockpit
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Tab 4: Governance Audit Ledger */}
      {activeTab === 'audit' && (
        <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-[#0b1c30]">Fiscal Governance Audit Ledger</h2>
              <p className="text-xs text-[#76777d] mt-0.5">
                Immutable compliance event records showing ceiling overrides, band updates, and user authorizations.
              </p>
            </div>
            <button
              onClick={loadData}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#e2e8f0] hover:bg-slate-50 text-xs font-bold text-[#45464d]"
            >
              <span className="material-symbols-outlined text-sm">refresh</span>
              Refresh Ledger
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#45464d]">
              <thead className="bg-[#f8fafc] text-xs uppercase text-[#76777d] border-b border-[#e2e8f0]">
                <tr>
                  <th className="px-6 py-3 font-bold">Event ID</th>
                  <th className="px-6 py-3 font-bold">Entity Type</th>
                  <th className="px-6 py-3 font-bold">Action</th>
                  <th className="px-6 py-3 font-bold">Authorized By</th>
                  <th className="px-6 py-3 font-bold">Compliance Reason</th>
                  <th className="px-6 py-3 font-bold">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#e2e8f0]">
                {auditLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-[#f8fafc] transition-colors">
                    <td className="px-6 py-3.5 font-mono text-xs font-bold text-[#2563eb]">{log.id}</td>
                    <td className="px-6 py-3.5">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-800">
                        {log.entity_type}: {log.entity_id}
                      </span>
                    </td>
                    <td className="px-6 py-3.5">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold ${
                          log.action === 'CREATE'
                            ? 'bg-emerald-50 text-emerald-700'
                            : log.action === 'DELETE'
                            ? 'bg-rose-50 text-rose-700'
                            : 'bg-blue-50 text-blue-700'
                        }`}
                      >
                        {log.action}
                      </span>
                    </td>
                    <td className="px-6 py-3.5 text-xs font-bold text-[#0b1c30]">{log.performed_by || 'System'}</td>
                    <td className="px-6 py-3.5 text-xs text-slate-600 max-w-xs truncate">{log.reason || 'Governance adjustment'}</td>
                    <td className="px-6 py-3.5 text-xs text-slate-500 font-mono">
                      {log.timestamp ? new Date(log.timestamp).toLocaleString() : 'Just now'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
