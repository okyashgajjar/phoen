import React, { useState, useEffect, useMemo } from 'react';
import { api } from '../api';

export default function CatalogRulesView() {
  const [rules, setRules] = useState([]);
  const [catalogProducts, setCatalogProducts] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('rules'); // 'rules' | 'products' | 'audit'

  // Filtering & Search
  const [categoryFilter, setCategoryFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [productSearch, setProductSearch] = useState('');

  // Modals state
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedRule, setSelectedRule] = useState(null);
  const [deleteConfirmRule, setDeleteConfirmRule] = useState(null);

  // Form states
  const [ruleForm, setRuleForm] = useState({
    id: '',
    name: '',
    rule_type: 'MARGIN_FLOOR',
    scope_type: 'GLOBAL',
    customer_tier: 'Enterprise',
    min_margin_percent: 15.0,
    max_discount_percent: 10.0,
    approval_level: 'L1_SALES_MANAGER',
    active: true,
  });

  const [notification, setNotification] = useState(null);

  const showNotification = (msg, type = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const loadData = async () => {
    try {
      setLoading(true);
      const [catalogData, logsData] = await Promise.all([
        api.getCatalogRules(),
        api.getAuditLogs().catch(() => []),
      ]);
      setRules(catalogData.rules || []);
      setCatalogProducts(catalogData.products || []);
      setAuditLogs(logsData || []);
    } catch (err) {
      console.error('Failed to load catalog rules:', err);
      showNotification('Failed to load database rules: ' + (err.message || 'Error'), 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Live Toggle active state
  const handleToggleRule = async (rule) => {
    const newActiveState = !rule.active;
    // Optimistic UI update
    setRules((prev) =>
      prev.map((r) => (r.id === rule.id ? { ...r, active: newActiveState } : r))
    );

    try {
      await api.updateCatalogRule(rule.id, { active: newActiveState });
      showNotification(
        `Rule ${rule.id} is now ${newActiveState ? 'ACTIVE' : 'DISABLED'} in database & audit ledger.`,
        'success'
      );
      // Refresh audit logs in background
      api.getAuditLogs().then(setAuditLogs).catch(() => {});
    } catch (err) {
      // Rollback on failure
      setRules((prev) =>
        prev.map((r) => (r.id === rule.id ? { ...r, active: rule.active } : r))
      );
      showNotification(`Failed to update rule ${rule.id}: ${err.message}`, 'error');
    }
  };

  // Open Create Modal
  const openCreateModal = () => {
    const nextNum = String(rules.length + 1).padStart(3, '0');
    setRuleForm({
      id: `AC-${nextNum}`,
      name: '',
      rule_type: 'MARGIN_FLOOR',
      scope_type: 'GLOBAL',
      customer_tier: 'Enterprise',
      min_margin_percent: 15.0,
      max_discount_percent: 10.0,
      approval_level: 'L1_SALES_MANAGER',
      active: true,
    });
    setIsAddModalOpen(true);
  };

  // Submit Create Rule
  const handleCreateRule = async (e) => {
    e.preventDefault();
    try {
      await api.createCatalogRule({
        ...ruleForm,
        min_margin_percent: ruleForm.min_margin_percent ? parseFloat(ruleForm.min_margin_percent) : null,
        max_discount_percent: ruleForm.max_discount_percent ? parseFloat(ruleForm.max_discount_percent) : null,
      });
      showNotification(`Rule ${ruleForm.id} created successfully and committed to database!`, 'success');
      setIsAddModalOpen(false);
      loadData();
    } catch (err) {
      showNotification(`Failed to create rule: ${err.message}`, 'error');
    }
  };

  // Open Edit Modal
  const openEditModal = (rule) => {
    setSelectedRule(rule);
    setRuleForm({
      id: rule.id,
      name: rule.name || '',
      rule_type: rule.rule_type || 'MARGIN_FLOOR',
      scope_type: rule.scope_type || 'GLOBAL',
      customer_tier: rule.customer_tier || 'Enterprise',
      min_margin_percent: rule.min_margin_percent !== null ? rule.min_margin_percent : 15.0,
      max_discount_percent: rule.max_discount_percent !== null ? rule.max_discount_percent : 10.0,
      approval_level: rule.approval_level || 'L1_SALES_MANAGER',
      active: rule.active,
    });
    setIsEditModalOpen(true);
  };

  // Submit Edit Rule
  const handleUpdateRule = async (e) => {
    e.preventDefault();
    if (!selectedRule) return;

    try {
      await api.updateCatalogRule(selectedRule.id, {
        name: ruleForm.name,
        rule_type: ruleForm.rule_type,
        customer_tier: ruleForm.customer_tier,
        min_margin_percent: ruleForm.min_margin_percent ? parseFloat(ruleForm.min_margin_percent) : null,
        max_discount_percent: ruleForm.max_discount_percent ? parseFloat(ruleForm.max_discount_percent) : null,
        approval_level: ruleForm.approval_level,
        active: ruleForm.active,
      });
      showNotification(`Rule ${selectedRule.id} updated and persisted to database!`, 'success');
      setIsEditModalOpen(false);
      setSelectedRule(null);
      loadData();
    } catch (err) {
      showNotification(`Failed to update rule: ${err.message}`, 'error');
    }
  };

  // Delete Rule
  const handleDeleteRule = async () => {
    if (!deleteConfirmRule) return;
    try {
      await api.deleteCatalogRule(deleteConfirmRule.id);
      showNotification(`Rule ${deleteConfirmRule.id} deleted from database!`, 'success');
      setDeleteConfirmRule(null);
      loadData();
    } catch (err) {
      showNotification(`Failed to delete rule: ${err.message}`, 'error');
    }
  };

  // Filtered Rules
  const filteredRules = useMemo(() => {
    return rules.filter((r) => {
      const matchesType =
        categoryFilter === 'ALL' ||
        r.rule_type === categoryFilter ||
        (categoryFilter === 'APPROVAL' && r.rule_type === 'MARGIN_FLOOR');

      const matchesSearch =
        !searchQuery ||
        r.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (r.name && r.name.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (r.role && r.role.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (r.customer_tier && r.customer_tier.toLowerCase().includes(searchQuery.toLowerCase()));

      return matchesType && matchesSearch;
    });
  }, [rules, categoryFilter, searchQuery]);

  // Filtered Products
  const filteredProducts = useMemo(() => {
    if (!productSearch) return catalogProducts;
    return catalogProducts.filter(
      (p) =>
        p.sku.toLowerCase().includes(productSearch.toLowerCase()) ||
        p.name.toLowerCase().includes(productSearch.toLowerCase())
    );
  }, [catalogProducts, productSearch]);

  // Metric stats
  const activeRulesCount = rules.filter((r) => r.active).length;
  const marginFloorRulesCount = rules.filter((r) => r.rule_type === 'MARGIN_FLOOR').length;
  const discountRulesCount = rules.filter((r) => r.rule_type === 'DISCOUNT_LIMIT').length;

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6 animate-in fade-in">
      {/* Toast Notification */}
      {notification && (
        <div
          className={`fixed top-5 right-5 z-50 px-5 py-3 rounded-xl shadow-lg border flex items-center gap-3 text-sm font-semibold transition-all ${
            notification.type === 'error'
              ? 'bg-rose-50 border-rose-200 text-rose-800'
              : 'bg-emerald-50 border-emerald-200 text-emerald-800'
          }`}
        >
          <span className="material-symbols-outlined text-lg">
            {notification.type === 'error' ? 'error' : 'check_circle'}
          </span>
          <span>{notification.msg}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#6C757D] mb-1">
            <span>CPQ Administration</span>
            <span>/</span>
            <span className="text-[#714B67]">Pricing & Governance Engine</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529] tracking-tight">CPQ Pricing & Approval Governance</h1>
          <p className="text-sm text-[#4A4A4A] mt-1">
            Configure automated margin floors, discount ceilings, pricing matrices, and live approval authorization chains.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={openCreateModal}
            className="flex items-center gap-2 px-5 h-11 rounded-xl bg-[#714B67] text-white hover:bg-[#5C3D54] font-bold text-xs shadow-md transition-all hover:scale-[1.02]"
          >
            <span className="material-symbols-outlined text-[18px]">add_circle</span>
            <span>Add Custom Rule</span>
          </button>
        </div>
      </div>

      {/* Key Metric KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Total Governance Rules</span>
            <div className="text-2xl font-extrabold text-[#212529] mt-1">{rules.length} Rules</div>
            <span className="text-xs text-emerald-600 font-semibold">{activeRulesCount} Active in Database</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#F8F4F7] flex items-center justify-center text-[#714B67]">
            <span className="material-symbols-outlined text-2xl">policy</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Approval Margin Floors</span>
            <div className="text-2xl font-extrabold text-[#212529] mt-1">{marginFloorRulesCount} Chains</div>
            <span className="text-xs text-slate-500 font-medium">L0 Auto up to L4 Board</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#F8F4F7] flex items-center justify-center text-[#714B67]">
            <span className="material-symbols-outlined text-2xl">verified_user</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Tier Discount Caps</span>
            <div className="text-2xl font-extrabold text-[#212529] mt-1">{discountRulesCount} Limits</div>
            <span className="text-xs text-amber-600 font-medium">Auto-Flag Thresholds</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center text-amber-600">
            <span className="material-symbols-outlined text-2xl">tune</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Live Catalog SKUs</span>
            <div className="text-2xl font-extrabold text-[#212529] mt-1">{catalogProducts.length} Items</div>
            <span className="text-xs text-emerald-600 font-medium">Direct PostgreSQL / SQLite</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600">
            <span className="material-symbols-outlined text-2xl">inventory_2</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-[#DEE2E6] pb-2">
        <button
          onClick={() => setActiveTab('rules')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'rules'
              ? 'bg-[#714B67] text-white shadow-sm'
              : 'text-[#4A4A4A] hover:bg-slate-100'
          }`}
        >
          <span className="material-symbols-outlined text-[18px]">rule</span>
          <span>Pricing & Approval Rules ({rules.length})</span>
        </button>
        <button
          onClick={() => setActiveTab('products')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'products'
              ? 'bg-[#714B67] text-white shadow-sm'
              : 'text-[#4A4A4A] hover:bg-slate-100'
          }`}
        >
          <span className="material-symbols-outlined text-[18px]">inventory_2</span>
          <span>Database Product SKUs ({catalogProducts.length})</span>
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'audit'
              ? 'bg-[#714B67] text-white shadow-sm'
              : 'text-[#4A4A4A] hover:bg-slate-100'
          }`}
        >
          <span className="material-symbols-outlined text-[18px]">history</span>
          <span>Governance Audit Ledger ({auditLogs.length})</span>
        </button>
      </div>

      {/* Tab 1: Rules View */}
      {activeTab === 'rules' && (
        <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-6">
          {/* Controls Bar: Categories & Search */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex flex-wrap items-center gap-2">
              {[
                { id: 'ALL', label: 'All Rules' },
                { id: 'MARGIN_FLOOR', label: 'Approval Margins' },
                { id: 'DISCOUNT_LIMIT', label: 'Discount Caps' },
                { id: 'CUSTOMER_OVERRIDE', label: 'Customer Overrides' },
                { id: 'PRICE_LIST', label: 'Price Lists' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setCategoryFilter(tab.id)}
                  className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    categoryFilter === tab.id
                      ? 'bg-[#212529] text-white'
                      : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="relative w-full md:w-72">
              <span className="material-symbols-outlined absolute left-3 top-2.5 text-[#6C757D] text-lg">
                search
              </span>
              <input
                type="text"
                placeholder="Search rule ID, role, tier..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full h-10 pl-9 pr-3 rounded-xl border border-[#DEE2E6] text-sm focus:outline-none focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
              />
            </div>
          </div>

          {/* Rules List Table */}
          {loading ? (
            <div className="p-12 flex flex-col items-center justify-center gap-3">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#714B67]"></div>
              <span className="text-xs text-[#6C757D] font-semibold">Loading real rules from database...</span>
            </div>
          ) : filteredRules.length === 0 ? (
            <div className="p-12 text-center text-sm text-[#6C757D]">
              No pricing rules match your search or category filter.
            </div>
          ) : (
            <div className="divide-y divide-[#F1F1F1] overflow-hidden">
              {filteredRules.map((rule) => (
                <div
                  key={rule.id}
                  className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-[#FAFAFA] px-3 rounded-xl transition-colors"
                >
                  <div className="flex flex-col gap-1 max-w-xl">
                    <div className="flex items-center gap-2.5 flex-wrap">
                      <span className="font-mono text-xs font-bold text-[#714B67] bg-[#F8F4F7] px-2 py-0.5 rounded-md">
                        {rule.id}
                      </span>
                      <span className="px-2 py-0.5 rounded bg-slate-100 text-[10px] font-bold text-slate-700">
                        {rule.category}
                      </span>
                      {rule.customer_tier && (
                        <span className="px-2 py-0.5 rounded bg-amber-50 text-[10px] font-bold text-amber-800">
                          Tier: {rule.customer_tier}
                        </span>
                      )}
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          rule.active ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                        }`}
                      >
                        {rule.active ? 'ACTIVE' : 'INACTIVE'}
                      </span>
                    </div>

                    <span className="text-sm font-bold text-[#212529] mt-0.5">{rule.name}</span>
                    <div className="text-xs text-[#6C757D] flex items-center gap-2 flex-wrap">
                      <span>Threshold: <strong className="text-[#212529]">{rule.threshold}</strong></span>
                      <span>•</span>
                      <span>Authorized Approver: <strong className="text-[#714B67]">{rule.role}</strong></span>
                      {rule.scope_type && (
                        <>
                          <span>•</span>
                          <span>Scope: {rule.scope_type}</span>
                        </>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-4 self-end sm:self-center">
                    {/* Active Switch */}
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-[#6C757D]">
                        {rule.active ? 'Enabled' : 'Disabled'}
                      </span>
                      <button
                        type="button"
                        onClick={() => handleToggleRule(rule)}
                        className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
                          rule.active ? 'bg-[#714B67]' : 'bg-[#CED4DA]'
                        }`}
                      >
                        <span
                          className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                            rule.active ? 'translate-x-5' : 'translate-x-0'
                          }`}
                        />
                      </button>
                    </div>

                    {/* Edit Button */}
                    <button
                      onClick={() => openEditModal(rule)}
                      className="p-1.5 rounded-lg text-[#6C757D] hover:text-[#714B67] hover:bg-[#F8F4F7] transition-colors"
                      title="Edit Rule Parameters"
                    >
                      <span className="material-symbols-outlined text-[20px]">edit</span>
                    </button>

                    {/* Delete Button */}
                    <button
                      onClick={() => setDeleteConfirmRule(rule)}
                      className="p-1.5 rounded-lg text-[#6C757D] hover:text-rose-600 hover:bg-rose-50 transition-colors"
                      title="Delete Rule"
                    >
                      <span className="material-symbols-outlined text-[20px]">delete</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Catalog Products View */}
      {activeTab === 'products' && (
        <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-[#212529]">Connected Catalog Items & SKUs</h2>
              <p className="text-xs text-[#6C757D] mt-0.5">
                Real-time variant and catalog data loaded from the relational enterprise database.
              </p>
            </div>
            <div className="relative w-full sm:w-72">
              <span className="material-symbols-outlined absolute left-3 top-2.5 text-[#6C757D] text-lg">
                search
              </span>
              <input
                type="text"
                placeholder="Search SKU or product name..."
                value={productSearch}
                onChange={(e) => setProductSearch(e.target.value)}
                className="w-full h-10 pl-9 pr-3 rounded-xl border border-[#DEE2E6] text-sm focus:outline-none focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#4A4A4A]">
              <thead className="bg-[#FAFAFA] text-xs uppercase text-[#6C757D] border-b border-[#DEE2E6]">
                <tr>
                  <th className="px-6 py-3.5 font-bold">SKU & Product Name</th>
                  <th className="px-6 py-3.5 font-bold">Category</th>
                  <th className="px-6 py-3.5 font-bold">List Price</th>
                  <th className="px-6 py-3.5 font-bold">Cost Basis</th>
                  <th className="px-6 py-3.5 font-bold">Base Margin</th>
                  <th className="px-6 py-3.5 font-bold">Discount Policy</th>
                  <th className="px-6 py-3.5 font-bold">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#DEE2E6]">
                {filteredProducts.map((p) => (
                  <tr key={p.sku} className="hover:bg-[#FAFAFA] transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="font-mono text-xs font-bold text-[#714B67]">{p.sku}</span>
                        <span className="font-bold text-[#212529] mt-0.5">{p.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-slate-100 text-slate-700">
                        {p.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-mono font-bold text-[#212529]">{p.listPrice}</td>
                    <td className="px-6 py-4 font-mono text-slate-600">{p.costBasis}</td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700">
                        {p.margin || '30.0%'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-xs font-semibold text-slate-600">{p.tierDiscount}</td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-[#F8F4F7] text-[#5C3D54]">
                        {p.status || 'ACTIVE'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Governance Audit Ledger */}
      {activeTab === 'audit' && (
        <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-[#212529]">Enterprise Governance Audit Ledger</h2>
              <p className="text-xs text-[#6C757D] mt-0.5">
                Immutable compliance event records showing rule creations, threshold adjustments, and user actions.
              </p>
            </div>
            <button
              onClick={loadData}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#DEE2E6] hover:bg-slate-50 text-xs font-bold text-[#4A4A4A]"
            >
              <span className="material-symbols-outlined text-sm">refresh</span>
              Refresh Ledger
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#4A4A4A]">
              <thead className="bg-[#FAFAFA] text-xs uppercase text-[#6C757D] border-b border-[#DEE2E6]">
                <tr>
                  <th className="px-6 py-3 font-bold">Event ID</th>
                  <th className="px-6 py-3 font-bold">Entity</th>
                  <th className="px-6 py-3 font-bold">Action</th>
                  <th className="px-6 py-3 font-bold">Performed By</th>
                  <th className="px-6 py-3 font-bold">Reason / Notes</th>
                  <th className="px-6 py-3 font-bold">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#DEE2E6]">
                {auditLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-[#FAFAFA] transition-colors">
                    <td className="px-6 py-3.5 font-mono text-xs font-bold text-[#714B67]">{log.id}</td>
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
                            : 'bg-[#F8F4F7] text-[#5C3D54]'
                        }`}
                      >
                        {log.action}
                      </span>
                    </td>
                    <td className="px-6 py-3.5 text-xs font-bold text-[#212529]">{log.performed_by || 'System'}</td>
                    <td className="px-6 py-3.5 text-xs text-slate-600 max-w-xs truncate">{log.reason || 'Operational action'}</td>
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

      {/* Modal: Add Custom Rule */}
      {isAddModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
          <div className="bg-white w-full max-w-lg rounded-2xl shadow-xl border border-[#DEE2E6] overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-6 border-b border-[#DEE2E6] flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-[#212529]">Add Custom CPQ Rule</h3>
                <p className="text-xs text-[#6C757D] mt-0.5">Persists directly to the database governance matrix.</p>
              </div>
              <button onClick={() => setIsAddModalOpen(false)} className="text-slate-400 hover:text-slate-700">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleCreateRule} className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Rule ID / Code</label>
                  <input
                    type="text"
                    required
                    value={ruleForm.id}
                    onChange={(e) => setRuleForm({ ...ruleForm, id: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Rule Category</label>
                  <select
                    value={ruleForm.rule_type}
                    onChange={(e) => setRuleForm({ ...ruleForm, rule_type: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  >
                    <option value="MARGIN_FLOOR">Margin Floor Governance</option>
                    <option value="DISCOUNT_LIMIT">Discount Limit Ceiling</option>
                    <option value="CUSTOMER_OVERRIDE">Customer Price Override</option>
                    <option value="PRICE_LIST">Standard Price List</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Rule Title & Description</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Strategic High-Volume Margin Cap"
                  value={ruleForm.name}
                  onChange={(e) => setRuleForm({ ...ruleForm, name: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Customer Tier</label>
                  <select
                    value={ruleForm.customer_tier}
                    onChange={(e) => setRuleForm({ ...ruleForm, customer_tier: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  >
                    <option value="Enterprise">Enterprise</option>
                    <option value="Strategic">Strategic</option>
                    <option value="Standard">Standard</option>
                    <option value="Gold">Gold</option>
                    <option value="Silver">Silver</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Approval Matrix Level</label>
                  <select
                    value={ruleForm.approval_level}
                    onChange={(e) => setRuleForm({ ...ruleForm, approval_level: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  >
                    <option value="L0_AUTO">L0 - Auto-Approval</option>
                    <option value="L1_SALES_MANAGER">L1 - Sales Manager</option>
                    <option value="L2_FINANCE_DIRECTOR">L2 - Commercial Finance</option>
                    <option value="L3_COMMERCIAL_VP">L3 - Commercial VP</option>
                    <option value="L4_EXECUTIVE_BOARD">L4 - Executive Board</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Min Margin Floor (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    value={ruleForm.min_margin_percent}
                    onChange={(e) => setRuleForm({ ...ruleForm, min_margin_percent: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Max Discount Cap (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    value={ruleForm.max_discount_percent}
                    onChange={(e) => setRuleForm({ ...ruleForm, max_discount_percent: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  />
                </div>
              </div>

              <div className="pt-4 flex items-center justify-end gap-3 border-t border-[#DEE2E6]">
                <button
                  type="button"
                  onClick={() => setIsAddModalOpen(false)}
                  className="px-4 py-2 text-xs font-bold text-[#6C757D] hover:text-[#212529]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-[#714B67] text-white text-xs font-bold hover:bg-[#5C3D54] shadow-sm transition-all"
                >
                  Save & Commit Rule
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Edit Rule */}
      {isEditModalOpen && selectedRule && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
          <div className="bg-white w-full max-w-lg rounded-2xl shadow-xl border border-[#DEE2E6] overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-6 border-b border-[#DEE2E6] flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-[#212529]">Edit Governance Rule: {selectedRule.id}</h3>
                <p className="text-xs text-[#6C757D] mt-0.5">Update thresholds and authorization authority.</p>
              </div>
              <button onClick={() => setIsEditModalOpen(false)} className="text-slate-400 hover:text-slate-700">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleUpdateRule} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Rule Name</label>
                <input
                  type="text"
                  required
                  value={ruleForm.name}
                  onChange={(e) => setRuleForm({ ...ruleForm, name: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Approval Matrix Level</label>
                  <select
                    value={ruleForm.approval_level}
                    onChange={(e) => setRuleForm({ ...ruleForm, approval_level: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  >
                    <option value="L0_AUTO">L0 - Auto-Approval</option>
                    <option value="L1_SALES_MANAGER">L1 - Sales Manager</option>
                    <option value="L2_FINANCE_DIRECTOR">L2 - Commercial Finance</option>
                    <option value="L3_COMMERCIAL_VP">L3 - Commercial VP</option>
                    <option value="L4_EXECUTIVE_BOARD">L4 - Executive Board</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Customer Tier</label>
                  <select
                    value={ruleForm.customer_tier || ''}
                    onChange={(e) => setRuleForm({ ...ruleForm, customer_tier: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  >
                    <option value="">Global (All Tiers)</option>
                    <option value="Enterprise">Enterprise</option>
                    <option value="Strategic">Strategic</option>
                    <option value="Standard">Standard</option>
                    <option value="Gold">Gold</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Min Margin Floor (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    value={ruleForm.min_margin_percent || ''}
                    onChange={(e) => setRuleForm({ ...ruleForm, min_margin_percent: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Max Discount Cap (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    value={ruleForm.max_discount_percent || ''}
                    onChange={(e) => setRuleForm({ ...ruleForm, max_discount_percent: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  />
                </div>
              </div>

              <div className="pt-4 flex items-center justify-end gap-3 border-t border-[#DEE2E6]">
                <button
                  type="button"
                  onClick={() => setIsEditModalOpen(false)}
                  className="px-4 py-2 text-xs font-bold text-[#6C757D] hover:text-[#212529]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-[#714B67] text-white text-xs font-bold hover:bg-[#5C3D54] shadow-sm transition-all"
                >
                  Update & Commit
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Delete Confirmation */}
      {deleteConfirmRule && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
          <div className="bg-white w-full max-w-md rounded-2xl shadow-xl border border-[#DEE2E6] p-6 animate-in zoom-in-95 duration-200">
            <div className="flex items-center gap-3 text-rose-600 mb-3">
              <span className="material-symbols-outlined text-2xl">warning</span>
              <h3 className="text-lg font-bold text-[#212529]">Delete Governance Rule</h3>
            </div>
            <p className="text-sm text-[#4A4A4A]">
              Are you sure you want to delete rule <strong className="text-[#212529]">{deleteConfirmRule.id}</strong> ({deleteConfirmRule.name})? This action cannot be undone and will be logged to the audit ledger.
            </p>
            <div className="mt-6 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setDeleteConfirmRule(null)}
                className="px-4 py-2 text-xs font-bold text-[#6C757D] hover:text-[#212529]"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDeleteRule}
                className="px-5 py-2.5 rounded-xl bg-rose-600 text-white text-xs font-bold hover:bg-rose-700 shadow-sm transition-all"
              >
                Confirm Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
