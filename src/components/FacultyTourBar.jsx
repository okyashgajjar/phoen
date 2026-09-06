import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function FacultyTourBar({ currentUser, onSwitchRole, onOpenArchitecture }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const navigate = useNavigate();

  const personas = [
    { label: 'Sales Rep', name: 'Marcus Vance', email: 'marcus@phoen.io', role: 'sales_rep', icon: 'badge' },
    { label: 'Sales Manager', name: 'Sarah Jenkins', email: 'sarah@phoen.io', role: 'manager', icon: 'supervisor_account' },
    { label: 'Finance Controller', name: 'David Chen', email: 'david@phoen.io', role: 'finance', icon: 'account_balance' },
    { label: 'Customer (Portal)', name: 'Acme Corp', email: 'acme@portal.dealflow360.com', role: 'customer', icon: 'storefront' },
    { label: 'Platform Admin', name: 'System Admin', email: 'admin@phoen.io', role: 'admin', icon: 'admin_panel_settings' },
  ];

  const scenarios = [
    { label: '1. High-Risk CPQ Discount', path: '/quote-detail/Q-1040', icon: 'warning', hint: 'Compounded discount leaks triggering L2 Manager & Finance sign-off' },
    { label: '2. AI Upsell & Margin Lift', path: '/quote-detail/Q-1042', icon: 'auto_awesome', hint: 'Graph-mined co-purchases with live margin meter' },
    { label: '3. Multi-Warehouse Split', path: '/fulfillment', icon: 'local_shipping', hint: 'Algorithmic inventory allocation across 5 regional DCs' },
    { label: '4. Customer Negotiation Portal', path: '/negotiation/Q-1040', icon: 'handshake', hint: 'Restricted client portal with digital sign & PDF export' },
  ];

  if (isCollapsed) {
    return (
      <div className="bg-[#1e1427] border-b border-[#714B67]/40 px-4 py-1.5 flex items-center justify-between text-xs text-purple-200 z-50 sticky top-0 shadow-md">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-[#714B67] text-white text-[10px] font-bold">P</span>
          <span className="font-bold tracking-wide text-white">Phoen Faculty & Evaluator Benchmark Bar</span>
          <span className="text-purple-300 text-[11px] hidden sm:inline">&bull; 16 Relational Tables &bull; Real ACID CPQ Engine</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={onOpenArchitecture}
            className="px-2.5 py-1 rounded bg-purple-900/60 hover:bg-purple-800 text-purple-200 font-medium text-[11px] border border-purple-500/30 flex items-center gap-1 transition-all"
          >
            <span className="material-symbols-outlined text-[14px]">account_tree</span>
            Why Phoen Wins
          </button>
          <button
            onClick={() => setIsCollapsed(false)}
            className="px-2 py-1 rounded bg-[#714B67] hover:bg-[#835677] text-white font-bold text-[11px] flex items-center gap-1 transition-all"
          >
            <span className="material-symbols-outlined text-[14px]">keyboard_arrow_down</span>
            Open Tour Mode
          </button>
        </div>
      </div>
    );
  }

  return (
    <aside aria-label="Evaluator and Faculty Tour Mode Bar" className="bg-gradient-to-r from-[#170e20] via-[#241530] to-[#170e20] border-b border-[#714B67]/50 text-white px-4 py-2.5 z-50 sticky top-0 shadow-xl backdrop-blur-md">
      <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-start lg:items-center justify-between gap-3">
        {/* Left: Brand + Evaluator Notice */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-[#714B67] to-[#e08ba6] flex items-center justify-center font-black text-white shadow-md text-sm shrink-0">
            Ψ
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-sm tracking-tight text-white">Phoen Evaluator Mode</span>
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-bold border border-emerald-500/40">
                100% ACID DB &bull; 0 Fake Data
              </span>
            </div>
            <p className="text-[11px] text-purple-200/80 mt-0.5">
              Switch personas or launch CPQ scenarios instantly to evaluate live algorithms.
            </p>
          </div>
        </div>

        {/* Center: 1-Click Persona Switcher */}
        <div className="flex flex-wrap items-center gap-1.5 bg-black/30 p-1 rounded-xl border border-white/10">
          <span className="text-[10px] font-bold uppercase tracking-wider text-purple-300/70 px-2">Personas:</span>
          {personas.map((p) => {
            const isActive = currentUser?.email?.toLowerCase() === p.email.toLowerCase() || currentUser?.role === p.role;
            return (
              <button
                key={p.role}
                onClick={() => onSwitchRole(p.email)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-[#714B67] text-white shadow-md border border-purple-400/50 scale-[1.02]'
                    : 'bg-white/5 hover:bg-white/15 text-slate-300 hover:text-white border border-transparent'
                }`}
                title={`Log in as ${p.name} (${p.email})`}
              >
                <span className="material-symbols-outlined text-[14px]">{p.icon}</span>
                <span>{p.label}</span>
              </button>
            );
          })}
        </div>

        {/* Right: Scenario Shortcuts & Architecture Modal Trigger */}
        <div className="flex items-center gap-2 w-full lg:w-auto justify-end">
          <div className="hidden xl:flex items-center gap-1 bg-black/20 p-1 rounded-xl border border-white/5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-purple-300/70 px-2">Demos:</span>
            {scenarios.map((sc, i) => (
              <button
                key={i}
                onClick={() => navigate(sc.path)}
                className="px-2 py-1 rounded-lg bg-white/5 hover:bg-white/15 text-purple-200 hover:text-white text-[11px] font-medium border border-transparent hover:border-purple-400/30 transition-all flex items-center gap-1"
                title={sc.hint}
              >
                <span className="material-symbols-outlined text-[13px] text-amber-400">{sc.icon}</span>
                <span>{sc.label}</span>
              </button>
            ))}
          </div>

          <button
            onClick={onOpenArchitecture}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-purple-600 to-[#714B67] hover:from-purple-500 hover:to-[#855879] text-white font-bold text-xs shadow-md border border-purple-300/30 transition-all active:scale-[0.98] shrink-0"
          >
            <span className="material-symbols-outlined text-[16px]">verified</span>
            <span>Why Phoen Wins</span>
          </button>

          <button
            onClick={() => setIsCollapsed(true)}
            className="p-1 rounded-lg hover:bg-white/10 text-slate-400 hover:text-white transition-colors"
            title="Collapse Evaluator Bar"
          >
            <span className="material-symbols-outlined text-[18px]">keyboard_arrow_up</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
