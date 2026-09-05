import React, { useState } from 'react';

export default function CatalogRulesView({ setActiveTab }) {
  const [rules, setRules] = useState([
    { id: 'RULE-104', name: 'Hardware Maximum Discount Cap', category: 'Hardware', threshold: '15.0%', role: 'Sales Manager', active: true },
    { id: 'RULE-105', name: 'Software Tier 2 Volume Discount', category: 'Software', threshold: '25.0%', role: 'Auto-Approved', active: true },
    { id: 'RULE-208', name: 'Blended Contract Margin Floor', category: 'Global CPQ', threshold: '35.0%', role: 'Finance VP', active: true },
    { id: 'RULE-302', name: 'Multi-Year SLA Price Lock Guarantee', category: 'Services', threshold: '10.0%', role: 'Sales Ops Lead', active: true },
    { id: 'RULE-401', name: 'Non-Standard SLA Payment Terms (> 60 Days)', category: 'Billing', threshold: '60 Days', role: 'Treasury Admin', active: false },
  ]);

  const toggleRule = (id) => {
    setRules((rList) =>
      rList.map((r) => (r.id === id ? { ...r, active: !r.active } : r))
    );
  };

  const catalogProducts = [
    { sku: 'SKU-HW-709', name: 'Server Rack Ultra 2U Enterprise', category: 'Hardware', listPrice: '$4,500', costBasis: '$3,150', tierDiscount: 'Up to 15%' },
    { sku: 'SKU-SW-ENT', name: 'Cloud Ops Platform License', category: 'Software', listPrice: '$120/yr', costBasis: '$45/yr', tierDiscount: 'Up to 25%' },
    { sku: 'SKU-SLA-PREM', name: '24/7 Priority Support SLA', category: 'Services', listPrice: '$3,040', costBasis: '$1,200', tierDiscount: 'Up to 10%' },
    { sku: 'SKU-SEC-AUD', name: 'Cybersecurity Compliance Audit', category: 'Services', listPrice: '$15,000', costBasis: '$7,500', tierDiscount: 'Up to 12%' },
    { sku: 'SKU-NET-[#0051d5]', name: 'Fiber Optical Router Edge 10G', category: 'Hardware', listPrice: '$8,200', costBasis: '$5,900', tierDiscount: 'Up to 15%' },
  ];

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
