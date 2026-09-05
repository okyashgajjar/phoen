import React from 'react';

export default function DashboardView({ setActiveTab, onOpenNewQuote }) {
  const modules = [
    {
      id: 'quote-detail',
      title: 'Quotation Builder',
      desc: 'Configure line items, volume discount schedules, and contract terms.',
      icon: 'calculate',
      badge: '12 drafts',
      tab: 'quote-detail',
    },
    {
      id: 'approvals',
      title: 'Approval Cockpit',
      desc: 'Review margin exceptions, multi-tier approvals, and policy overrides.',
      icon: 'verified_user',
      badge: '4 pending',
      badgeColor: 'bg-amber-100 text-amber-800',
      tab: 'approvals',
    },
    {
      id: 'catalog',
      title: 'Catalog & Rule Engine',
      desc: 'Manage CPQ pricing tiers, margin guardrails, and discount thresholds.',
      icon: 'rule',
      badge: '32 active rules',
      tab: 'catalog',
    },
    {
      id: 'negotiation',
      title: 'Customer Portal',
      desc: 'Monitor client engagement, counter-offers, and e-signatures in real time.',
      icon: 'handshake',
      badge: '2 active portals',
      tab: 'negotiation',
    },
    {
      id: 'fulfillment',
      title: 'Fulfillment & Stock',
      desc: 'Allocate serial numbers, dispatch inventory, and track shipments.',
      icon: 'inventory',
      badge: '8 orders queued',
      tab: 'fulfillment',
    },
  ];

  const recentActivity = [
    {
      id: 1,
      user: 'Marcus Vance',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAPPCmZWSHv5-hqsV8B7a1ZAECPiQItn-WV9xogMiJF9w-Wwv0lW7nz_la1neL_umllylkeWsgu_7FSD2pOWnm8q6XPvfiKqQhyu7j1xzouHlH_s2STTn1V9JHHdo0Eu0j3SAECmMOP6qrMR_PrChQgZgSVqVy4tyYNOMJUlvjFrvny8XcszlX1_cJIy-5LvL05M6wWURQqleEiw4-DcrpFqbL078c-3nWaf7c9-9c1r63DGe_rRAUQ',
      action: 'submitted quote for executive approval',
      target: 'Q-1042 (Acme Corp)',
      time: '12 mins ago',
      amount: '$28,600',
      status: 'Pending VP Review',
      statusBg: 'bg-amber-50 text-amber-800 border-amber-200',
    },
    {
      id: 2,
      user: 'Rachel Torres',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDDy3o_lnWgGPSUoB6P7Lp4hkbJFgtCgcakv09lYBTZEbeu45LrPMl-4j7D0fkePZHXv0SFP1ARMob5zvodbhlCTX9_i_ZNXVUl4gOB_g-RzHoTv_zqTypCWZyAlVCatqoMEUNzUaJds22kANc4-RQ4UwSK9Du9ZPIAiPkL-Q40vCvfw9YyzywdZ9NKDCgjYbrQatymSh81iyvilkTl4OuioHwk3E6wEqqj5gaJi_EYElr5UK2kTIkQ',
      action: 'executed e-signature on portal',
      target: 'Q-1039 (TechCorp)',
      time: '1 hour ago',
      amount: '$142,000',
      status: 'Won & Signed',
      statusBg: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    },
    {
      id: 3,
      user: 'David Chen',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD6eGnNwcM2SWzLN7P5S_9fzAl71lAafDpxahswhQgzYLqqw_UYITDveOBT58W0KmwcQOrX4LYatjjzmk-y6DwcLx5R6RAk3k2dcTlzY52hxYLej98xxzfmBXfxl9rP__hIUR_nV7p524_UzAOEL4XkKSANGLIb6NcLx8gG654E6TSYV8JuaKRPE4Qdpu6MXyn18gJuHb1pLmcnJBQixHFZG3WZUz9Ina6EKZp_uqg8Z0hEccvcG-HL',
      action: 'approved discount override rule',
      target: 'RULE-104 (Tier 2 Cloud)',
      time: '3 hours ago',
      amount: '15% Margin Cap',
      status: 'Rule Updated',
      statusBg: 'bg-blue-50 text-blue-800 border-blue-200',
    },
  ];

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-8">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-white p-6 lg:p-8 shadow-sm border border-[#e2e8f0] flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div className="absolute -right-16 -top-16 w-80 h-80 rounded-full bg-[#2563eb]/5 blur-3xl pointer-events-none"></div>
        <div className="relative flex flex-col gap-2.5 z-10">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#eff4ff] text-[#003ea8] font-semibold text-xs">
              <span className="w-2 h-2 rounded-full bg-[#2563eb] animate-pulse"></span>
              Live Commercial Operations
            </span>
            <span className="font-mono text-xs text-[#76777d]">Q4 FY2025</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30] tracking-tight">
            Welcome back, Sarah
          </h1>
          <p className="text-sm text-[#45464d] max-w-2xl leading-relaxed">
            Here is what’s happening across your active deals, automated margin checks, and pending commercial approvals today.
          </p>
        </div>
        <div className="relative flex flex-wrap items-center gap-3 shrink-0 z-10">
          <button
            onClick={onOpenNewQuote}
            className="group h-12 px-6 rounded-xl bg-[#2563eb] hover:bg-[#1d4ed8] text-white font-semibold text-sm shadow-md flex items-center gap-2 transition-all active:scale-[0.98]"
          >
            <span className="material-symbols-outlined text-[20px] transition-transform group-hover:rotate-90">add</span>
            <span>New Quotation</span>
          </button>
          <button
            onClick={() => setActiveTab('approvals')}
            className="h-12 px-6 rounded-xl bg-white hover:bg-[#f8fafc] text-[#0b1c30] font-semibold text-sm border border-[#e2e8f0] shadow-sm flex items-center gap-2.5 transition-all active:scale-[0.98]"
          >
            <span className="material-symbols-outlined text-[#76777d] text-[20px]">task_alt</span>
            <span>View Approvals</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 font-bold text-xs">
              4 awaiting review
            </span>
          </button>
        </div>
      </div>

      {/* 3-Step Guided Workflow Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-[#2563eb]/10 via-[#eff4ff] to-[#e5eeff] p-6 shadow-sm border border-[#2563eb]/20 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-4 shrink-0">
          <div className="w-12 h-12 rounded-xl bg-[#2563eb] text-white flex items-center justify-center shadow-md">
            <span className="material-symbols-outlined text-[28px]">lightbulb</span>
          </div>
          <div>
            <span className="font-bold text-base text-[#0b1c30] block">How Phoen CPQ Works</span>
            <span className="text-xs text-[#45464d]">End-to-end Quote-to-Cash workflow optimized for non-technical sales operators</span>
          </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full md:max-w-2xl">
          <div
            onClick={() => setActiveTab('quotations')}
            className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#e2e8f0] hover:border-[#2563eb] cursor-pointer transition-all shadow-xs"
          >
            <span className="w-7 h-7 rounded-full bg-[#dbe1ff] text-[#00174b] flex items-center justify-center font-mono text-xs font-bold shrink-0">1</span>
            <div className="flex flex-col min-w-0">
              <span className="text-xs font-bold text-[#0b1c30] truncate">1. Create Quote</span>
              <span className="text-[11px] text-[#45464d] truncate">Pick tiered catalog SKUs</span>
            </div>
          </div>
          <div
            onClick={() => setActiveTab('approvals')}
            className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#e2e8f0] hover:border-[#2563eb] cursor-pointer transition-all shadow-xs"
          >
            <span className="w-7 h-7 rounded-full bg-[#dbe1ff] text-[#00174b] flex items-center justify-center font-mono text-xs font-bold shrink-0">2</span>
            <div className="flex flex-col min-w-0">
              <span className="text-xs font-bold text-[#0b1c30] truncate">2. Auto Rule Engine</span>
              <span className="text-[11px] text-[#45464d] truncate">Margins & approval matrix</span>
            </div>
          </div>
          <div
            onClick={() => setActiveTab('invoices')}
            className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#e2e8f0] hover:border-[#2563eb] cursor-pointer transition-all shadow-xs"
          >
            <span className="w-7 h-7 rounded-full bg-[#dbe1ff] text-[#00174b] flex items-center justify-center font-mono text-xs font-bold shrink-0">3</span>
            <div className="flex flex-col min-w-0">
              <span className="text-xs font-bold text-[#0b1c30] truncate">3. Fulfill & Invoice</span>
              <span className="text-[11px] text-[#45464d] truncate">Dispatch to billing ledger</span>
            </div>
          </div>
        </div>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* KPI 1: Pending Approvals */}
        <div
          onClick={() => setActiveTab('approvals')}
          className="group rounded-2xl bg-white p-6 shadow-sm border border-[#e2e8f0] flex flex-col justify-between hover:shadow-md hover:border-[#2563eb]/40 transition-all cursor-pointer"
        >
          <div>
            <div className="flex items-start justify-between gap-4 mb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#76777d]">Action Queue</span>
                <h3 className="text-lg font-bold text-[#0b1c30] mt-0.5">Pending Approvals</h3>
              </div>
              <div className="w-11 h-11 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center shrink-0">
                <span className="material-symbols-outlined text-[24px]">hourglass_top</span>
              </div>
            </div>
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-4xl font-extrabold text-[#0b1c30]">4</span>
              <span className="text-sm text-[#45464d]">quotations awaiting sign-off</span>
            </div>
            <div className="flex items-center gap-2 mb-4">
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 text-xs font-semibold border border-amber-200">
                <span className="material-symbols-outlined text-[14px]">priority_high</span> Action required
              </span>
              <span className="text-xs text-[#76777d]">Avg review: 42m</span>
            </div>
          </div>
          <div className="pt-4 border-t border-[#e2e8f0] flex items-center justify-between">
            <span className="text-sm font-bold text-[#2563eb] group-hover:underline flex items-center gap-1">
              Review pending queue <span class="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </span>
            <span className="font-mono text-xs text-[#45464d]">3 High • 1 Med</span>
          </div>
        </div>

        {/* KPI 2: Open Quotations */}
        <div
          onClick={() => setActiveTab('quotations')}
          className="group rounded-2xl bg-white p-6 shadow-sm border border-[#e2e8f0] flex flex-col justify-between hover:shadow-md hover:border-[#2563eb]/40 transition-all cursor-pointer"
        >
          <div>
            <div className="flex items-start justify-between gap-4 mb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#76777d]">Active Pipeline</span>
                <h3 className="text-lg font-bold text-[#0b1c30] mt-0.5 font-sans">Open Quotations</h3>
              </div>
              <div className="w-11 h-11 rounded-xl bg-[#eff4ff] text-[#2563eb] flex items-center justify-center shrink-0">
                <span className="material-symbols-outlined text-[24px]">request_quote</span>
              </div>
            </div>
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-4xl font-extrabold text-[#0b1c30]">12</span>
              <span className="text-sm text-[#45464d]">active proposals</span>
            </div>
            <div className="flex items-center gap-2 mb-4">
              <span className="text-xl font-bold text-[#0b1c30] font-mono">$284,500</span>
              <span className="inline-flex items-center gap-0.5 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold">
                <span className="material-symbols-outlined text-[14px]">trending_up</span> +18% vs last mo
              </span>
            </div>
          </div>
          <div className="pt-4 border-t border-[#e2e8f0] flex items-center justify-between">
            <span className="text-sm font-bold text-[#2563eb] group-hover:underline flex items-center gap-1">
              Explore pipeline <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </span>
            <span className="font-mono text-xs text-[#45464d]">8 in contract draft</span>
          </div>
        </div>

        {/* KPI 3: At-Risk Deals */}
        <div
          onClick={() => setActiveTab('deal-health')}
          className="group rounded-2xl bg-white p-6 shadow-sm border border-[#e2e8f0] flex flex-col justify-between hover:shadow-md hover:border-rose-400 transition-all cursor-pointer"
        >
          <div>
            <div className="flex items-start justify-between gap-4 mb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#76777d]">Deal Health Sentinel</span>
                <h3 className="text-lg font-bold text-[#0b1c30] mt-0.5">At-Risk Deals</h3>
              </div>
              <div className="w-11 h-11 rounded-xl bg-rose-50 text-rose-700 flex items-center justify-center shrink-0">
                <span className="material-symbols-outlined text-[24px]">warning</span>
              </div>
            </div>
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-4xl font-extrabold text-rose-700">3</span>
              <span className="text-sm text-[#45464d]">flagged items</span>
            </div>
            <div className="flex items-center gap-2 mb-4">
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-800 text-xs font-semibold border border-rose-200">
                <span className="material-symbols-outlined text-[14px]">error</span> Acme Corp & Beta Ind.
              </span>
            </div>
          </div>
          <div className="pt-4 border-t border-[#e2e8f0] flex items-center justify-between">
            <span className="text-sm font-bold text-rose-700 group-hover:underline flex items-center gap-1">
              Fix deal guardrails <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </span>
            <span className="font-mono text-xs text-[#45464d]">14.8% max variance</span>
          </div>
        </div>
      </div>

      {/* Commercial Engine Modules Grid */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-[#0b1c30]">Commercial Engine Workspaces</h2>
            <p className="text-xs text-[#45464d]">Select a module to jump straight into configuring, reviewing, or fulfilling orders</p>
          </div>
          <span className="text-xs text-[#76777d] font-semibold hidden sm:inline">Press any workspace card to open</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {modules.map((m) => (
            <div
              key={m.id}
              onClick={() => setActiveTab(m.tab)}
              className="group rounded-2xl bg-white p-5 shadow-sm border border-[#e2e8f0] hover:shadow-md hover:border-[#2563eb] transition-all cursor-pointer flex flex-col justify-between hover:-translate-y-0.5"
            >
              <div className="flex flex-col gap-3">
                <div className="w-11 h-11 rounded-xl bg-[#eff4ff] flex items-center justify-center text-[#2563eb] group-hover:bg-[#2563eb] group-hover:text-white transition-colors">
                  <span className="material-symbols-outlined text-[24px]">{m.icon}</span>
                </div>
                <div>
                  <span className="text-sm font-bold text-[#0b1c30] block group-hover:text-[#2563eb] transition-colors">{m.title}</span>
                  <p className="text-xs text-[#45464d] mt-1 leading-snug">{m.desc}</p>
                </div>
              </div>
              <div className="mt-4 pt-3 border-t border-[#f1f5f9] flex items-center justify-between text-xs font-semibold text-[#76777d]">
                <span className={`px-2 py-0.5 rounded-full ${m.badgeColor || 'bg-[#f1f5f9] text-[#0b1c30]'}`}>{m.badge}</span>
                <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform text-[#2563eb]">chevron_right</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Activity Stream & Quick Action Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Commercial Activity */}
        <div className="lg:col-span-2 rounded-2xl bg-white p-6 shadow-sm border border-[#e2e8f0]">
          <div className="flex items-center justify-between pb-4 mb-4 border-b border-[#e2e8f0]">
            <div>
              <h3 className="text-base font-bold text-[#0b1c30]">Recent Commercial Activity</h3>
              <p className="text-xs text-[#76777d]">Live audit trail of quote submissions and rule updates</p>
            </div>
            <button onClick={() => setActiveTab('quotations')} className="text-xs font-bold text-[#2563eb] hover:underline">
              View all history
            </button>
          </div>
          <div className="divide-y divide-[#f1f5f9]">
            {recentActivity.map((item) => (
              <div key={item.id} className="py-4 flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <img src={item.avatar} alt={item.user} className="w-10 h-10 rounded-full object-cover ring-2 ring-[#e2e8f0]" />
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-[#0b1c30]">{item.user}</span>
                      <span className="text-xs text-[#45464d]">{item.action}</span>
                    </div>
                    <span className="text-xs font-semibold text-[#2563eb] cursor-pointer hover:underline" onClick={() => setActiveTab('quote-detail')}>
                      {item.target}
                    </span>
                  </div>
                </div>
                <div className="flex flex-col items-end shrink-0">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${item.statusBg}`}>
                    {item.status}
                  </span>
                  <span className="text-[11px] text-[#76777d] mt-1">{item.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Priority Quick Actions */}
        <div className="rounded-2xl bg-white p-6 shadow-sm border border-[#e2e8f0] flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-[#0b1c30] mb-1">Commercial Priorities</h3>
            <p className="text-xs text-[#76777d] mb-4">Recommended actions for Sarah Jenkins</p>
            <div className="space-y-3">
              <div
                onClick={() => setActiveTab('approvals')}
                className="p-3 rounded-xl bg-amber-50/70 border border-amber-200 hover:border-amber-400 cursor-pointer transition-all flex items-start gap-3"
              >
                <span className="material-symbols-outlined text-amber-700 text-[20px] mt-0.5">priority_high</span>
                <div>
                  <span className="text-xs font-bold text-amber-900 block">Approve Acme Corp Q-1042</span>
                  <span className="text-[11px] text-amber-800">18% discount flag requires executive sign-off</span>
                </div>
              </div>
              <div
                onClick={() => setActiveTab('negotiation')}
                className="p-3 rounded-xl bg-blue-50/70 border border-blue-200 hover:border-blue-400 cursor-pointer transition-all flex items-start gap-3"
              >
                <span className="material-symbols-outlined text-blue-700 text-[20px] mt-0.5">question_answer</span>
                <div>
                  <span className="text-xs font-bold text-blue-900 block">Review Customer Counter-Offer</span>
                  <span className="text-[11px] text-blue-800">Global Logistics requested 2-year term lock</span>
                </div>
              </div>
              <div
                onClick={() => setActiveTab('fulfillment')}
                className="p-3 rounded-xl bg-emerald-50/70 border border-emerald-200 hover:border-emerald-400 cursor-pointer transition-all flex items-start gap-3"
              >
                <span className="material-symbols-outlined text-emerald-700 text-[20px] mt-0.5">local_shipping</span>
                <div>
                  <span className="text-xs font-bold text-emerald-900 block">Dispatch Stock Order #ORD-8821</span>
                  <span className="text-[11px] text-emerald-800">Hardware serials assigned, ready to ship</span>
                </div>
              </div>
            </div>
          </div>
          <button
            onClick={() => setActiveTab('quotations')}
            className="w-full mt-4 py-2.5 rounded-xl bg-[#eff4ff] hover:bg-[#e5eeff] text-[#2563eb] font-bold text-xs transition-colors flex items-center justify-center gap-1"
          >
            <span>Open All Pipeline Items</span>
            <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
          </button>
        </div>
      </div>
    </div>
  );
}
