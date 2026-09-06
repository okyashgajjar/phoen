import React, { useState } from 'react';

export default function LandingView({ onNavigateToAuth }) {
  const [appsDropdownOpen, setAppsDropdownOpen] = useState(false);

  const apps = [
    {
      id: 'sales',
      name: 'Sales & Dynamic CPQ',
      icon: 'point_of_sale',
      color: '#714B67',
      bgColor: 'bg-[#714B67]/10',
      textColor: 'text-[#714B67]',
      description: 'Configure complex quotes, calculate dynamic margins, and generate executive PDFs in seconds.'
    },
    {
      id: 'governance',
      name: 'Discount Sentinel',
      icon: 'gavel',
      color: '#E9A227',
      bgColor: 'bg-amber-500/10',
      textColor: 'text-amber-700',
      description: 'Automated margin defense with real-time risk scores and multi-tier approval routing.'
    },
    {
      id: 'fulfillment',
      name: 'Split Warehouse Engine',
      icon: 'local_shipping',
      color: '#017E84',
      bgColor: 'bg-teal-500/10',
      textColor: 'text-teal-700',
      description: 'Auto-split orders across regional hubs to optimize shipping costs and expedite delivery.'
    },
    {
      id: 'invoicing',
      name: 'Invoicing & Accounting',
      icon: 'receipt_long',
      color: '#28A745',
      bgColor: 'bg-emerald-500/10',
      textColor: 'text-emerald-700',
      description: 'One-click GST tax invoices, payment schedule tracking, and automated ledger sync.'
    },
    {
      id: 'subscriptions',
      name: 'Hybrid Billing & ARR',
      icon: 'sync',
      color: '#6366F1',
      bgColor: 'bg-indigo-500/10',
      textColor: 'text-indigo-700',
      description: 'Combine CAPEX hardware purchases with recurring OPEX SaaS licenses on a single invoice.'
    },
    {
      id: 'portal',
      name: 'Negotiation Portal',
      icon: 'forum',
      color: '#EC4899',
      bgColor: 'bg-pink-500/10',
      textColor: 'text-pink-700',
      description: 'Real-time collaborative deal room with live margin recalculation and digital sign-off.'
    },
    {
      id: 'reports',
      name: 'Executive BI Analytics',
      icon: 'analytics',
      color: '#0284C7',
      bgColor: 'bg-sky-500/10',
      textColor: 'text-sky-700',
      description: 'Pipeline velocity heatmaps, sales rep leaderboards, and discount impact forecasting.'
    },
    {
      id: 'rbac',
      name: 'Enterprise Security & RBAC',
      icon: 'shield',
      color: '#EA580C',
      bgColor: 'bg-orange-500/10',
      textColor: 'text-orange-700',
      description: 'Granular role-based controls for Reps, Managers, Finance, and Admins with tamper-proof audit trails.'
    }
  ];

  return (
    <div className="min-h-screen bg-[#F8F9FA] text-[#212529] font-sans antialiased selection:bg-[#714B67] selection:text-white">
      {/* Top Banner (Odoo Style) */}
      <div className="bg-gradient-to-r from-[#714B67] via-[#5C3D54] to-[#017E84] text-white text-xs py-2 px-4 text-center font-medium shadow-sm flex items-center justify-center gap-2">
        <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-white/20 text-white font-semibold text-[11px]">
          NEW
        </span>
        <span>Phoen Enterprise v2.4 • Odoo-Inspired Commercial Cloud • Flexible Instant Login Enabled</span>
        <button 
          onClick={() => onNavigateToAuth('login')}
          className="ml-2 underline font-bold hover:text-amber-200 transition-colors cursor-pointer"
        >
          Sign in now →
        </button>
      </div>

      {/* Main Navigation (Odoo Navbar) */}
      <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-[#DEE2E6] shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
          {/* Brand Logo */}
          <div className="flex items-center gap-8">
            <div 
              onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
              className="flex items-center gap-3 cursor-pointer group"
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#714B67] to-[#5C3D54] flex items-center justify-center shadow-md shadow-[#714B67]/20 group-hover:scale-105 transition-transform">
                <span className="material-symbols-outlined text-white text-[22px]">view_quilt</span>
              </div>
              <div>
                <span className="text-xl font-extrabold tracking-tight text-[#212529] flex items-center gap-1.5">
                  Phoen
                  <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-[#EFE6ED] text-[#714B67] border border-[#714B67]/20">
                    Enterprise
                  </span>
                </span>
                <span className="text-[10px] text-[#6C757D] block -mt-1 font-medium">
                  Commercial ERP Cloud
                </span>
              </div>
            </div>

            {/* Desktop Navigation Links */}
            <nav className="hidden md:flex items-center gap-1 text-sm font-medium text-[#4A4A4A]">
              <div className="relative">
                <button 
                  onClick={() => setAppsDropdownOpen(!appsDropdownOpen)}
                  className="flex items-center gap-1.5 px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-[#714B67] transition-colors"
                >
                  <span className="material-symbols-outlined text-[18px]">apps</span>
                  Apps
                  <span className="material-symbols-outlined text-[16px] text-slate-400">expand_more</span>
                </button>

                {appsDropdownOpen && (
                  <div 
                    onMouseLeave={() => setAppsDropdownOpen(false)}
                    className="absolute top-full left-0 mt-2 w-[480px] bg-white rounded-2xl shadow-2xl border border-slate-200 p-4 grid grid-cols-2 gap-2 z-50 animate-in fade-in slide-in-from-top-2 duration-200"
                  >
                    {apps.map((app) => (
                      <div 
                        key={app.id}
                        onClick={() => { setAppsDropdownOpen(false); onNavigateToAuth('login'); }}
                        className="p-2.5 rounded-xl hover:bg-slate-50 transition-colors cursor-pointer flex items-start gap-3 group"
                      >
                        <div className={`w-8 h-8 rounded-lg ${app.bgColor} flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform`}>
                          <span className={`material-symbols-outlined text-[18px] ${app.textColor}`}>{app.icon}</span>
                        </div>
                        <div>
                          <div className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors">
                            {app.name}
                          </div>
                          <div className="text-[11px] text-[#6C757D] line-clamp-1 leading-snug">
                            {app.description}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <a 
                href="#features" 
                className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-[#714B67] transition-colors"
              >
                Features
              </a>
              <a 
                href="#mockup" 
                className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-[#714B67] transition-colors"
              >
                Live Preview
              </a>
              <a 
                href="#comparison" 
                className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-[#714B67] transition-colors"
              >
                Why Us
              </a>
              <a 
                href="#personas" 
                className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-[#714B67] transition-colors"
              >
                Demo Roles
              </a>
            </nav>
          </div>

          {/* Right Action CTAs */}
          <div className="flex items-center gap-3">
            <button 
              onClick={() => onNavigateToAuth('login')}
              className="text-sm font-semibold text-[#4A4A4A] hover:text-[#714B67] px-3.5 py-2 rounded-lg hover:bg-slate-100 transition-colors"
            >
              Sign in
            </button>
            <button 
              onClick={() => onNavigateToAuth('login')}
              className="text-sm font-bold text-white bg-[#00A09D] hover:bg-[#008784] active:scale-95 px-5 py-2.5 rounded-lg shadow-sm hover:shadow-md transition-all flex items-center gap-1.5"
            >
              Start Now — It's Free
              <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section (Odoo Signature Style) */}
      <section className="relative overflow-hidden pt-16 pb-20 md:pt-24 md:pb-28">
        {/* Subtle decorative mesh background */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1200px] h-[600px] bg-gradient-to-b from-[#EFE6ED]/70 via-[#F8F4F7]/40 to-transparent rounded-full blur-3xl -z-10"></div>
          <div className="absolute top-40 right-10 w-72 h-72 bg-teal-50 rounded-full blur-3xl -z-10"></div>
          <div className="absolute top-60 left-10 w-72 h-72 bg-purple-50 rounded-full blur-3xl -z-10"></div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-[#E0CEDB] shadow-sm mb-8 hover:shadow transition-shadow">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#00A09D] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#00A09D]"></span>
            </span>
            <span className="text-xs font-semibold text-[#714B67]">
              Odoo-Engineered Commercial Revenue Cloud • Enterprise Edition
            </span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-5xl md:text-7xl font-extrabold tracking-tight text-[#212529] max-w-5xl mx-auto leading-[1.15]">
            All your commercial deals, <br className="hidden sm:inline"/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#714B67] via-[#5C3D54] to-[#017E84]">
              on one unified platform.
            </span>
          </h1>

          {/* Subtitle */}
          <p className="mt-6 max-w-3xl mx-auto text-lg sm:text-xl text-[#6C757D] leading-relaxed font-normal">
            Simple, efficient, yet fully integrated. Automate CPQ pricing, multi-tier discount governance, 
            smart warehouse fulfillment, and hybrid hardware-SaaS billing. Zero spreadsheets, 100% PostgreSQL consistency.
          </p>

          {/* CTA Buttons */}
          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button 
              onClick={() => onNavigateToAuth('login')}
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-[#00A09D] hover:bg-[#008784] text-white font-bold text-lg shadow-lg shadow-[#00A09D]/30 transition-all hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-2"
            >
              Start Now — It's Free
              <span className="material-symbols-outlined text-[20px]">rocket_launch</span>
            </button>
            <a 
              href="#mockup"
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-white hover:bg-slate-50 text-[#714B67] font-bold text-lg border-2 border-[#714B67]/20 shadow-sm transition-all hover:border-[#714B67]/40 flex items-center justify-center gap-2"
            >
              <span className="material-symbols-outlined text-[20px] text-[#714B67]">visibility</span>
              Explore ERP Window
            </a>
          </div>

          {/* Trust Guarantees */}
          <div className="mt-6 flex flex-wrap items-center justify-center gap-6 text-xs text-[#6C757D] font-medium">
            <span className="flex items-center gap-1.5">
              <span className="material-symbols-outlined text-emerald-600 text-[16px]">check_circle</span>
              Free instant access
            </span>
            <span className="flex items-center gap-1.5">
              <span className="material-symbols-outlined text-emerald-600 text-[16px]">check_circle</span>
              Any email & password logs in
            </span>
            <span className="flex items-center gap-1.5">
              <span className="material-symbols-outlined text-emerald-600 text-[16px]">check_circle</span>
              Real PostgreSQL Database
            </span>
            <span className="flex items-center gap-1.5">
              <span className="material-symbols-outlined text-emerald-600 text-[16px]">check_circle</span>
              No credit card required
            </span>
          </div>
        </div>

        {/* Live ERP Window Mockup (Odoo Desktop UI) */}
        <div id="mockup" className="mt-16 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="rounded-2xl shadow-2xl border border-[#DEE2E6] overflow-hidden bg-white">
            {/* Top Odoo App Bar */}
            <div className="bg-[#714B67] text-white px-4 py-2.5 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <button className="p-1 rounded hover:bg-white/10 transition-colors">
                  <span className="material-symbols-outlined text-[20px]">apps</span>
                </button>
                <div className="flex items-center gap-2 font-bold text-sm">
                  <span>Phoen</span>
                  <span className="text-white/60">/</span>
                  <span className="text-white/90">Sales</span>
                </div>
              </div>
              {/* Odoo Global Search Mock */}
              <div className="hidden sm:flex items-center bg-white/15 px-3 py-1 rounded-md text-xs text-white/90 w-72">
                <span className="material-symbols-outlined text-[16px] mr-2 text-white/70">search</span>
                <span>Search quotes, customers, invoices...</span>
              </div>
              {/* User Avatar */}
              <div className="flex items-center gap-3 text-xs">
                <span className="material-symbols-outlined text-[18px] text-white/80 cursor-pointer">chat_bubble</span>
                <span className="material-symbols-outlined text-[18px] text-white/80 cursor-pointer">notifications</span>
                <div className="flex items-center gap-2 bg-white/15 px-2.5 py-1 rounded-full">
                  <div className="w-5 h-5 rounded-full bg-white text-[#714B67] font-bold flex items-center justify-center text-[10px]">
                    KS
                  </div>
                  <span className="font-semibold text-white">Kavita Sharma</span>
                </div>
              </div>
            </div>

            {/* Control Panel / Breadcrumb & Status Ribbon */}
            <div className="bg-[#F8F9FA] border-b border-[#DEE2E6] px-6 py-3 flex flex-wrap items-center justify-between gap-4">
              {/* Breadcrumb & Action Buttons */}
              <div className="flex items-center gap-3">
                <span className="text-lg font-bold text-[#212529]">
                  Quotations <span className="text-[#6C757D] font-normal">/</span> SO-2026-0049
                </span>
                <div className="flex items-center gap-2 ml-4">
                  <button 
                    onClick={() => onNavigateToAuth('login')}
                    className="px-3 py-1.5 rounded bg-[#00A09D] text-white font-semibold text-xs hover:bg-[#008784] shadow-sm transition-colors flex items-center gap-1"
                  >
                    <span className="material-symbols-outlined text-[14px]">send</span>
                    Send by Email
                  </button>
                  <button 
                    onClick={() => onNavigateToAuth('login')}
                    className="px-3 py-1.5 rounded bg-[#714B67] text-white font-semibold text-xs hover:bg-[#5C3D54] shadow-sm transition-colors flex items-center gap-1"
                  >
                    <span className="material-symbols-outlined text-[14px]">check</span>
                    Confirm Order
                  </button>
                  <button 
                    onClick={() => onNavigateToAuth('login')}
                    className="px-3 py-1.5 rounded bg-white border border-[#DEE2E6] text-[#4A4A4A] font-semibold text-xs hover:bg-slate-50 transition-colors"
                  >
                    Print / PDF
                  </button>
                </div>
              </div>

              {/* Authentic Odoo Status Pipeline Widget */}
              <div className="flex items-center text-xs font-semibold overflow-x-auto">
                <div className="px-3 py-1.5 bg-slate-200 text-[#4A4A4A] rounded-l-md">
                  Quotation
                </div>
                <div className="px-3 py-1.5 bg-slate-200 text-[#4A4A4A] border-l border-white">
                  Quotation Sent
                </div>
                <div className="px-3 py-1.5 bg-[#714B67] text-white font-bold border-l border-white flex items-center gap-1 shadow-inner">
                  <span className="material-symbols-outlined text-[14px]">verified</span>
                  Under Approval
                </div>
                <div className="px-3 py-1.5 bg-slate-100 text-slate-400 border-l border-white rounded-r-md">
                  Sales Order
                </div>
              </div>
            </div>

            {/* Document Body (Clean Paper Layout) */}
            <div className="p-6 md:p-8 bg-white">
              {/* Document Header */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-6 border-b border-[#DEE2E6]">
                <div>
                  <div className="text-2xl font-extrabold text-[#714B67] mb-2">SO-2026-0049</div>
                  <div className="space-y-1 text-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-[#6C757D] font-medium w-32">Customer:</span>
                      <span className="font-bold text-[#212529]">Tata Consultancy Services Ltd</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[#6C757D] font-medium w-32">Invoice Address:</span>
                      <span className="text-[#4A4A4A]">Cyber City, Phase II, Gurugram, HR</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[#6C757D] font-medium w-32">Salesperson:</span>
                      <span className="text-[#4A4A4A]">Kavita Sharma (Lead AE)</span>
                    </div>
                  </div>
                </div>

                <div className="md:text-right space-y-1 text-sm">
                  <div className="flex items-center md:justify-end gap-2">
                    <span className="text-[#6C757D] font-medium w-32 md:w-auto">Expiration Date:</span>
                    <span className="font-semibold text-[#212529]">30 Days (Apr 15, 2026)</span>
                  </div>
                  <div className="flex items-center md:justify-end gap-2">
                    <span className="text-[#6C757D] font-medium w-32 md:w-auto">Payment Terms:</span>
                    <span className="text-[#4A4A4A]">Net 30 Days (Immediate Delivery)</span>
                  </div>
                  <div className="flex items-center md:justify-end gap-2">
                    <span className="text-[#6C757D] font-medium w-32 md:w-auto">Pricelist:</span>
                    <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200">
                      Tier-1 Enterprise (INR)
                    </span>
                  </div>
                </div>
              </div>

              {/* Order Lines Table */}
              <div className="mt-6 overflow-x-auto">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="border-b-2 border-[#DEE2E6] text-[#6C757D] uppercase font-bold">
                      <th className="py-2.5 px-3">Product Description</th>
                      <th className="py-2.5 px-3 text-right">Quantity</th>
                      <th className="py-2.5 px-3 text-right">Unit Price</th>
                      <th className="py-2.5 px-3 text-right">Discount</th>
                      <th className="py-2.5 px-3 text-right">Blended Margin</th>
                      <th className="py-2.5 px-3 text-right">Subtotal</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-sm">
                    <tr className="hover:bg-[#F8F4F7]/40 transition-colors">
                      <td className="py-3 px-3 font-semibold text-[#212529]">
                        Enterprise Cloud Core Server (Hardware)
                        <span className="block text-[11px] text-[#6C757D] font-normal">
                          Warehouse: BLR-WH-01 • S/N Stock Reserved
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right font-medium">4.00 Units</td>
                      <td className="py-3 px-3 text-right font-medium">₹4,50,000</td>
                      <td className="py-3 px-3 text-right text-amber-600 font-semibold">8.00%</td>
                      <td className="py-3 px-3 text-right text-emerald-600 font-semibold">38.2%</td>
                      <td className="py-3 px-3 text-right font-bold text-[#212529]">₹16,56,000</td>
                    </tr>
                    <tr className="hover:bg-[#F8F4F7]/40 transition-colors">
                      <td className="py-3 px-3 font-semibold text-[#212529]">
                        Phoen Annual Platform License (SaaS)
                        <span className="block text-[11px] text-[#6C757D] font-normal">
                          Recurring 12-Mo Billing • Automated Renewal
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right font-medium">150.00 Seats</td>
                      <td className="py-3 px-3 text-right font-medium">₹12,000</td>
                      <td className="py-3 px-3 text-right text-amber-600 font-semibold">12.00%</td>
                      <td className="py-3 px-3 text-right text-emerald-600 font-semibold">62.5%</td>
                      <td className="py-3 px-3 text-right font-bold text-[#212529]">₹15,84,000</td>
                    </tr>
                    <tr className="hover:bg-[#F8F4F7]/40 transition-colors">
                      <td className="py-3 px-3 font-semibold text-[#212529]">
                        Tier-1 24/7 Dedicated Support SLA
                        <span className="block text-[11px] text-[#6C757D] font-normal">
                          Enterprise Priority Response • 99.9% Cloud SLA
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right font-medium">1.00 SLA</td>
                      <td className="py-3 px-3 text-right font-medium">₹3,20,000</td>
                      <td className="py-3 px-3 text-right text-amber-600 font-semibold">5.00%</td>
                      <td className="py-3 px-3 text-right text-emerald-600 font-semibold">54.0%</td>
                      <td className="py-3 px-3 text-right font-bold text-[#212529]">₹3,04,000</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Financial Calculation Summary */}
              <div className="mt-8 flex flex-col sm:flex-row justify-between items-start sm:items-end gap-6 pt-6 border-t border-[#DEE2E6]">
                <div className="bg-[#F8F4F7] p-4 rounded-xl border border-[#E0CEDB] max-w-md">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#714B67] mb-1">
                    <span className="material-symbols-outlined text-[16px]">local_shipping</span>
                    Smart Multi-Warehouse Split Route
                  </div>
                  <p className="text-xs text-[#5C3D54] leading-relaxed">
                    Auto-allocated across Bengaluru Hub (60%) and Mumbai Hub (40%) to minimize logistics transit time by 48 hours.
                  </p>
                </div>

                <div className="w-full sm:w-80 space-y-2 text-sm">
                  <div className="flex justify-between text-[#6C757D]">
                    <span>Untaxed Amount:</span>
                    <span className="font-semibold text-[#212529]">₹35,44,000</span>
                  </div>
                  <div className="flex justify-between text-[#6C757D]">
                    <span>GST (18%):</span>
                    <span className="font-semibold text-[#212529]">₹6,37,920</span>
                  </div>
                  <div className="flex justify-between text-emerald-700 font-semibold">
                    <span>Blended Gross Margin:</span>
                    <span>51.8% (Healthy)</span>
                  </div>
                  <div className="border-t-2 border-[#714B67] pt-2 flex justify-between text-lg font-extrabold text-[#714B67]">
                    <span>Total Amount:</span>
                    <span>₹41,81,920</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* App Ecosystem Grid (Odoo Signature 8 Apps) */}
      <section id="features" className="py-20 bg-white border-y border-[#DEE2E6]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-extrabold uppercase tracking-wider text-[#714B67] bg-[#EFE6ED] px-3 py-1 rounded-full">
              Modular Architecture
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#212529] mt-3">
              A complete suite of commercial apps.
            </h2>
            <p className="text-[#6C757D] text-lg mt-3">
              Say goodbye to fragmented SaaS tools. Every Phoen app connects natively into one shared PostgreSQL core.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {apps.map((app) => (
              <div 
                key={app.id}
                onClick={() => onNavigateToAuth('login')}
                className="p-6 rounded-2xl border border-[#DEE2E6] bg-[#F8F9FA] hover:bg-white hover:border-[#714B67]/30 hover:shadow-xl transition-all duration-300 cursor-pointer group flex flex-col justify-between"
              >
                <div>
                  <div className={`w-14 h-14 rounded-2xl ${app.bgColor} flex items-center justify-center mb-5 group-hover:scale-110 transition-transform`}>
                    <span className={`material-symbols-outlined text-[28px] ${app.textColor}`}>
                      {app.icon}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-[#212529] mb-2 group-hover:text-[#714B67] transition-colors">
                    {app.name}
                  </h3>
                  <p className="text-sm text-[#6C757D] leading-relaxed">
                    {app.description}
                  </p>
                </div>
                <div className="mt-6 pt-4 border-t border-slate-200/60 flex items-center justify-between text-xs font-bold text-[#714B67]">
                  <span>Explore App</span>
                  <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">
                    arrow_forward
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Comparison Section (Odoo vs Broken Tools) */}
      <section id="comparison" className="py-20 bg-[#F8F9FA]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-extrabold uppercase tracking-wider text-[#017E84] bg-teal-50 px-3 py-1 rounded-full border border-teal-200">
              Zero Fragmentation
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#212529] mt-3">
              Why commercial teams switch to Phoen.
            </h2>
            <p className="text-[#6C757D] text-lg mt-3">
              Compare traditional disconnected revenue operations with Phoen's unified Odoo-inspired model.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* The Old Way */}
            <div className="p-8 rounded-3xl bg-white border border-rose-200 shadow-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 px-4 py-1.5 bg-rose-100 text-rose-800 text-xs font-bold rounded-bl-xl">
                The Old Broken Way
              </div>
              <h3 className="text-xl font-extrabold text-slate-800 mb-6 flex items-center gap-2">
                <span className="material-symbols-outlined text-rose-500">cancel</span>
                Disconnected SaaS Stacks
              </h3>
              <ul className="space-y-4 text-sm text-[#4A4A4A]">
                <li className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-rose-500 text-[18px] flex-shrink-0 mt-0.5">close</span>
                  <span>Sales reps calculate discounts on fragile offline Excel spreadsheets.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-rose-500 text-[18px] flex-shrink-0 mt-0.5">close</span>
                  <span>Finance manually creates GST invoices, leading to reconciliation discrepancies.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-rose-500 text-[18px] flex-shrink-0 mt-0.5">close</span>
                  <span>Warehouses lack visibility into pending quotations and stock reservations.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-rose-500 text-[18px] flex-shrink-0 mt-0.5">close</span>
                  <span>Complex multi-role approvals take 3–5 days over scattered email threads.</span>
                </li>
              </ul>
            </div>

            {/* The Phoen Way */}
            <div className="p-8 rounded-3xl bg-white border-2 border-[#714B67] shadow-lg relative overflow-hidden">
              <div className="absolute top-0 right-0 px-4 py-1.5 bg-[#714B67] text-white text-xs font-bold rounded-bl-xl">
                The Phoen Unified Way
              </div>
              <h3 className="text-xl font-extrabold text-[#714B67] mb-6 flex items-center gap-2">
                <span className="material-symbols-outlined text-emerald-600">check_circle</span>
                Unified Odoo Architecture
              </h3>
              <ul className="space-y-4 text-sm text-[#212529]">
                <li className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-emerald-600 text-[18px] flex-shrink-0 mt-0.5">done_all</span>
                  <span className="font-medium">Real-time dynamic margin scoring built directly into the quotation screen.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-emerald-600 text-[18px] flex-shrink-0 mt-0.5">done_all</span>
                  <span className="font-medium">Automatic GST invoice generation upon order confirmation with PDF exports.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-emerald-600 text-[18px] flex-shrink-0 mt-0.5">done_all</span>
                  <span className="font-medium">Smart split engine auto-allocates inventory across closest regional hubs.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-emerald-600 text-[18px] flex-shrink-0 mt-0.5">done_all</span>
                  <span className="font-medium">Instant 1-click approvals for Sales & Finance managers with audit compliance.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Enterprise Metrics & Social Proof */}
      <section className="py-16 bg-gradient-to-br from-[#714B67] to-[#472F41] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center divide-y lg:divide-y-0 lg:divide-x divide-white/15">
            <div className="pt-4 lg:pt-0">
              <div className="text-4xl sm:text-5xl font-extrabold text-white">₹3.5B+</div>
              <div className="text-sm text-white/80 mt-1 font-medium">Pipeline Value Governed</div>
            </div>
            <div className="pt-4 lg:pt-0">
              <div className="text-4xl sm:text-5xl font-extrabold text-amber-300">198+</div>
              <div className="text-sm text-white/80 mt-1 font-medium">Active Production Quotes</div>
            </div>
            <div className="pt-4 lg:pt-0">
              <div className="text-4xl sm:text-5xl font-extrabold text-teal-300">70.4%</div>
              <div className="text-sm text-white/80 mt-1 font-medium">Commercial Win Rate</div>
            </div>
            <div className="pt-4 lg:pt-0">
              <div className="text-4xl sm:text-5xl font-extrabold text-white">100%</div>
              <div className="text-sm text-white/80 mt-1 font-medium">PostgreSQL Integrity</div>
            </div>
          </div>
        </div>
      </section>

      {/* One-Click Persona Test Drive Section */}
      <section id="personas" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-extrabold uppercase tracking-wider text-[#714B67] bg-[#EFE6ED] px-3 py-1 rounded-full">
              Flexible Login Experience
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#212529] mt-3">
              Test drive any enterprise role instantly.
            </h2>
            <p className="text-[#6C757D] text-lg mt-3">
              You can log in with <strong className="text-[#212529]">ANY email and ANY password</strong>. Or pick any of our pre-configured enterprise personas below:
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Sales Rep */}
            <div 
              onClick={() => onNavigateToAuth('login')}
              className="p-6 rounded-2xl border border-[#DEE2E6] bg-[#F8F9FA] hover:border-[#714B67] hover:shadow-xl transition-all cursor-pointer group"
            >
              <div className="w-12 h-12 rounded-xl bg-[#714B67]/10 flex items-center justify-center mb-4 text-[#714B67]">
                <span className="material-symbols-outlined text-[24px]">badge</span>
              </div>
              <div className="text-xs font-bold uppercase tracking-wider text-[#714B67]">Sales Executive</div>
              <div className="text-lg font-bold text-[#212529] mt-1">Kavita Sharma</div>
              <div className="text-xs text-[#6C757D] mt-1 font-mono">kavita@phoen.io</div>
              <p className="text-xs text-[#6C757D] mt-3 leading-relaxed">
                Create new quotations, test margin calculations, and trigger real-time approval requests.
              </p>
              <div className="mt-5 text-xs font-bold text-[#714B67] flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                Sign In as Sales Rep →
              </div>
            </div>

            {/* Sales Manager */}
            <div 
              onClick={() => onNavigateToAuth('login')}
              className="p-6 rounded-2xl border border-amber-200 bg-amber-50/50 hover:border-amber-400 hover:shadow-xl transition-all cursor-pointer group"
            >
              <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center mb-4 text-amber-700">
                <span className="material-symbols-outlined text-[24px]">verified_user</span>
              </div>
              <div className="text-xs font-bold uppercase tracking-wider text-amber-700">Commercial Manager</div>
              <div className="text-lg font-bold text-amber-950 mt-1">Vikramaditya S.</div>
              <div className="text-xs text-amber-800 mt-1 font-mono">vikram@phoen.io</div>
              <p className="text-xs text-amber-900/80 mt-3 leading-relaxed">
                Review pending quotations, approve or reject high-discount deals, and monitor margin health.
              </p>
              <div className="mt-5 text-xs font-bold text-amber-800 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                Sign In as Manager →
              </div>
            </div>

            {/* Finance Manager */}
            <div 
              onClick={() => onNavigateToAuth('login')}
              className="p-6 rounded-2xl border border-teal-200 bg-teal-50/50 hover:border-teal-400 hover:shadow-xl transition-all cursor-pointer group"
            >
              <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center mb-4 text-teal-700">
                <span className="material-symbols-outlined text-[24px]">receipt_long</span>
              </div>
              <div className="text-xs font-bold uppercase tracking-wider text-teal-700">Finance & Billing</div>
              <div className="text-lg font-bold text-teal-950 mt-1">David Chen</div>
              <div className="text-xs text-teal-800 mt-1 font-mono">david@phoen.io</div>
              <p className="text-xs text-teal-900/80 mt-3 leading-relaxed">
                Generate manual GST invoices, track split shipments, and configure discount rules.
              </p>
              <div className="mt-5 text-xs font-bold text-teal-800 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                Sign In as Finance →
              </div>
            </div>

            {/* System Admin */}
            <div 
              onClick={() => onNavigateToAuth('login')}
              className="p-6 rounded-2xl border border-purple-200 bg-purple-50/50 hover:border-purple-400 hover:shadow-xl transition-all cursor-pointer group"
            >
              <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center mb-4 text-purple-700">
                <span className="material-symbols-outlined text-[24px]">admin_panel_settings</span>
              </div>
              <div className="text-xs font-bold uppercase tracking-wider text-purple-700">System Administrator</div>
              <div className="text-lg font-bold text-purple-950 mt-1">Alex Admin</div>
              <div className="text-xs text-purple-800 mt-1 font-mono">admin@phoen.io</div>
              <p className="text-xs text-purple-900/80 mt-3 leading-relaxed">
                Manage user permissions, inspect audit logs, and configure enterprise CPQ policies.
              </p>
              <div className="mt-5 text-xs font-bold text-purple-800 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                Sign In as Admin →
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Banner (Odoo Plum & Teal) */}
      <section className="py-16 bg-[#F8F9FA] border-t border-[#DEE2E6]">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="p-10 md:p-14 rounded-3xl bg-gradient-to-br from-[#714B67] to-[#5C3D54] text-white shadow-xl relative overflow-hidden">
            <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight">
              Ready to modernize your quote-to-cash?
            </h2>
            <p className="mt-4 text-lg text-white/80 max-w-2xl mx-auto">
              Join leading commercial enterprises scaling with Phoen. Instant login enabled — no credit card needed.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={() => onNavigateToAuth('login')}
                className="px-8 py-4 rounded-xl bg-[#00A09D] hover:bg-[#008784] text-white font-bold text-lg shadow-lg transition-all hover:scale-105 active:scale-95 flex items-center justify-center gap-2"
              >
                Launch Live App Now
                <span className="material-symbols-outlined text-[20px]">arrow_forward</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Odoo-Style Enterprise Multi-Column Footer */}
      <footer className="bg-white border-t border-[#DEE2E6] text-xs text-[#6C757D] py-14">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
          {/* Brand Column */}
          <div className="col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#714B67] to-[#5C3D54] flex items-center justify-center text-white font-bold">
                <span className="material-symbols-outlined text-[18px]">view_quilt</span>
              </div>
              <span className="text-lg font-extrabold text-[#212529]">
                Phoen
              </span>
            </div>
            <p className="text-xs text-[#6C757D] max-w-sm leading-relaxed mb-4">
              The next-generation Quote-to-Cash, CPQ, and Revenue Operations platform inspired by Odoo's open, modular architecture.
            </p>
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-[#F8F4F7] text-[#714B67] font-semibold border border-[#E0CEDB]">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              PostgreSQL Database Connected
            </div>
          </div>

          {/* Solutions Column */}
          <div>
            <h4 className="font-bold text-[#212529] uppercase tracking-wider mb-3 text-[11px]">Solutions</h4>
            <ul className="space-y-2">
              <li><a href="#features" className="hover:text-[#714B67]">Enterprise CPQ</a></li>
              <li><a href="#features" className="hover:text-[#714B67]">Discount Governance</a></li>
              <li><a href="#features" className="hover:text-[#714B67]">Multi-Warehouse Routing</a></li>
              <li><a href="#features" className="hover:text-[#714B67]">SaaS + Hardware Billing</a></li>
              <li><a href="#features" className="hover:text-[#714B67]">Buyer Negotiation Portal</a></li>
            </ul>
          </div>

          {/* Applications Column */}
          <div>
            <h4 className="font-bold text-[#212529] uppercase tracking-wider mb-3 text-[11px]">Applications</h4>
            <ul className="space-y-2">
              <li><a href="#features" className="hover:text-[#714B67]">Sales & Quotations</a></li>
              <li><a href="#features" className="hover:text-[#714B67]">Approval Sentinel</a></li>
              <li><a href="#features" className="hover:text-[#714B67]">Invoicing & Ledger</a></li>
              <li><a href="#features" className="hover:text-[#714B67]">Subscriptions & ARR</a></li>
              <li><a href="#features" className="hover:text-[#714B67]">Executive BI Reports</a></li>
            </ul>
          </div>

          {/* Architecture & Trust */}
          <div>
            <h4 className="font-bold text-[#212529] uppercase tracking-wider mb-3 text-[11px]">Architecture</h4>
            <ul className="space-y-2">
              <li><span className="text-[#4A4A4A]">PostgreSQL 16 Engine</span></li>
              <li><span className="text-[#4A4A4A]">FastAPI Async Backend</span></li>
              <li><span className="text-[#4A4A4A]">React 19 Frontend</span></li>
              <li><span className="text-[#4A4A4A]">Odoo-Inspired UI/UX</span></li>
              <li><span className="text-[#4A4A4A]">RBAC Matrix Governance</span></li>
            </ul>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 border-t border-[#DEE2E6] flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px]">
          <div>
            © 2026 Phoen Inc. All rights reserved. Inspired by Odoo Enterprise UX.
          </div>
          <div className="flex items-center gap-6">
            <span className="text-[#6C757D]">Production Release 2.4.0</span>
            <span className="text-[#6C757D]">phoen_prod</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
