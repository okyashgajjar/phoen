import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function CatalogRulesView({ setActiveTab }) {
  const [rules, setRules] = useState([]);
  const [catalogProducts, setCatalogProducts] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await api.getCatalogRules();
        setRules(data.rules || []);
        setCatalogProducts(data.products || []);
      } catch (err) {
        console.error('Failed to load catalog rules:', err);
      }
    }
    loadData();
  }, []);

  const toggleRule = (id) => {
    setRules((rList) =>
      rList.map((r) => (r.id === id ? { ...r, active: !r.active } : r))
    );
  };

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#76777d] mb-1">
            <span>CPQ Administration</span>
            <span>/</span>
            <span className="text-[#2563eb]">Catalog & Rules Engine</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30]">CPQ Pricing & Approval Rules</h1>
          <p className="text-sm text-[#45464d] mt-1">Configure automated margin guardrails, product pricing tiers, and approval matrix thresholds.</p>
        </div>
        <button
          onClick={() => alert('New Approval Rule wizard initialized!')}
          className="flex items-center gap-2 px-5 h-11 rounded-xl bg-[#2563eb] text-white hover:bg-[#1d4ed8] font-bold text-xs shadow-md transition-all"
        >
          <span className="material-symbols-outlined text-[18px]">add_circle</span>
          <span>Add Custom Rule</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Rules Matrix (2 Cols) */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
          <h2 className="text-lg font-bold text-[#0b1c30]">Active Governance & Approval Rules</h2>
          <div className="divide-y divide-[#f1f5f9]">
            {rules.map((rule) => (
              <div key={rule.id} className="py-4 flex items-center justify-between gap-4">
                <div className="flex flex-col">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-[#2563eb]">{rule.id}</span>
                    <span className="px-2 py-0.5 rounded bg-[#eff4ff] text-[10px] font-bold text-[#0b1c30]">{rule.category}</span>
                  </div>
                  <span className="text-sm font-bold text-[#0b1c30] mt-1">{rule.name}</span>
                  <span className="text-xs text-[#76777d]">Threshold: {rule.threshold} • Approver: {rule.role}</span>
                </div>
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => toggleRule(rule.id)}
                    className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out ${
                      rule.active ? 'bg-[#2563eb]' : 'bg-[#c6c6cd]'
                    }`}
                  >
                    <span
                      className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                        rule.active ? 'translate-x-5' : 'translate-x-0'
                      }`}
                    />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Product Catalog Overview (1 Col) */}
        <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
          <h2 className="text-lg font-bold text-[#0b1c30]">Catalog Product SKUs</h2>
          <div className="space-y-3">
            {catalogProducts.map((p) => (
              <div key={p.sku} className="p-3.5 rounded-xl border border-[#e2e8f0] bg-[#f8fafc] flex flex-col gap-1">
                <div className="flex justify-between items-center">
                  <span className="font-mono text-xs font-bold text-[#2563eb]">{p.sku}</span>
                  <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 text-[10px] font-bold">{p.tierDiscount}</span>
                </div>
                <span className="text-xs font-bold text-[#0b1c30] mt-0.5">{p.name}</span>
                <div className="flex justify-between text-[11px] text-[#76777d] mt-1">
                  <span>List: {p.listPrice}</span>
                  <span>Cost Basis: {p.costBasis}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
