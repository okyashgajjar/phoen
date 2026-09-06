import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

const DEMO_PERSONAS = [
  {
    role: 'sales_rep',
    title: 'Sales Person',
    name: 'Kavita Sharma',
    email: 'kavita@phoen.io',
    icon: 'badge',
    badgeColor: 'bg-[#EFE6ED] text-[#472F41] border-[#E0CEDB]',
    desc: 'Quotes, Line Items, Client Portal',
  },
  {
    role: 'manager',
    title: 'Sales Manager',
    name: 'Vikramaditya Singhania',
    email: 'vikram@phoen.io',
    icon: 'verified_user',
    badgeColor: 'bg-amber-100 text-amber-800 border-amber-200',
    desc: 'Tier 1 Approvals, Deal Health',
  },
  {
    role: 'finance',
    title: 'Finance Manager',
    name: 'David Chen',
    email: 'david@phoen.io',
    icon: 'receipt_long',
    badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-200',
    desc: 'Invoices, Subscriptions, Ledger',
  },
  {
    role: 'admin',
    title: 'System Admin',
    name: 'Alex Mercer',
    email: 'alex@phoen.io',
    icon: 'admin_panel_settings',
    badgeColor: 'bg-purple-100 text-purple-800 border-purple-200',
    desc: 'Pricing Catalog, Rules, Users',
  },
];

export default function Navbar({ 
  currentUser, 
  apiStatus, 
  onOpenNewQuote, 
  onSwitchRole, 
  searchQuery, 
  setSearchQuery
}) {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  const location = useLocation();
  const navigate = useNavigate();

  const role = currentUser?.role || 'sales_rep';

  // Strict role-tailored navigation items
  const allNavItems = [
    { id: 'dashboard', label: 'Dashboard', roles: ['sales_rep', 'manager', 'finance', 'admin', 'customer'] },
    { 
      id: 'quotations', 
      label: role === 'sales_rep' ? 'My Proposals' : role === 'manager' ? 'Team Pipeline' : role === 'finance' ? 'Quotations Audit' : 'Global Pipeline', 
      roles: ['sales_rep', 'manager', 'finance', 'admin'] 
    },
    { 
      id: 'quote-detail', 
      label: 'Quotation Builder', 
      badge: 'CPQ',
      badgeColor: 'bg-[#F8F4F7] text-[#5C3D54] border-[#E0CEDB]',
      roles: ['sales_rep', 'manager', 'admin'] 
    },
    { 
      id: 'negotiation', 
      label: 'Customer Negotiation', 
      badge: 'Live',
      badgeColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
      roles: ['sales_rep', 'manager', 'admin'] 
    },
    { 
      id: 'approvals', 
      label: role === 'finance' ? 'Financial Sign-Offs' : role === 'admin' ? 'Governance & Approvals' : 'Approval Cockpit', 
      badge: role === 'finance' ? 'Tier 2' : role === 'manager' ? 'Tier 1' : 'Policy', 
      badgeColor: 'bg-amber-50 text-amber-700 border-amber-200', 
      roles: ['manager', 'finance', 'admin'] 
    },
    { id: 'deal-health', label: 'Deal Health Sentinel', badge: 'Alerts', badgeColor: 'bg-rose-50 text-rose-700 border-rose-200', roles: ['manager', 'admin'] },
    { id: 'invoices', label: 'Invoices & Ledger', roles: ['finance', 'admin'] },
    { id: 'subscriptions', label: 'Subscriptions & ARR', roles: ['finance', 'admin'] },
    { id: 'fulfillment', label: 'Fulfillment & Splits', roles: ['finance', 'admin'] },
    { id: 'products', label: 'Product Catalog', roles: ['admin', 'manager', 'finance', 'sales_rep'] },
    { id: 'reports', label: 'Reporting', roles: ['admin', 'manager', 'finance'] },
    { id: 'governance', label: 'Discount Governance', roles: ['admin', 'manager', 'finance'] },
    { id: 'catalog', label: 'Catalog & Rules', roles: ['admin'] },
    { id: 'team', label: 'Team Management', roles: ['admin'] },
  ];

  const navItems = allNavItems.filter(item => item.roles.includes(role));

  const notifications = [
    { id: 1, title: 'Quote Q-1042 Flagged', time: '12m ago', desc: '18% hardware discount exceeds 15% tier limit.', type: 'warning' },
    { id: 2, title: 'Contract Signed!', time: '1h ago', desc: 'TechCorp Industries accepted Quote Q-1039 ($142,000).', type: 'success' },
    { id: 3, title: 'New Customer Counter-Offer', time: '2h ago', desc: 'Global Logistics submitted request on Q-1040.', type: 'info' },
    { id: 4, title: 'Stock Allocation Ready', time: '3h ago', desc: 'Batch #SKU-9940 reserved for Order #ORD-8821.', type: 'info' },
  ];

  const currentPersona = DEMO_PERSONAS.find(p => p.role === role) || {
    role,
    title: role.replace('_', ' '),
    name: currentUser?.name || 'User',
    email: currentUser?.email || '',
    badgeColor: 'bg-slate-100 text-slate-800 border-slate-200',
  };

  const handleRoleSelect = (persona) => {
    setShowProfileMenu(false);
    if (onSwitchRole) {
      onSwitchRole(persona.email, 'password');
    }
  };

  const canCreateQuote = ['sales_rep', 'admin'].includes(role);

  return (
    <header className="sticky top-0 left-0 w-full z-50 bg-[#ffffff] border-b border-[#CED4DA]/40 shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
      <div className="h-20 w-full px-4 lg:px-8 flex items-center justify-between gap-4">
        {/* Brand & Logo */}
        <div className="flex items-center gap-3 shrink-0 cursor-pointer" onClick={() => navigate('/dashboard')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#212529] via-[#212529] to-[#714B67] flex items-center justify-center text-white shadow-md relative">
            <span className="material-symbols-outlined text-[24px]">dataset</span>
            <div 
              className={`absolute -bottom-1 -right-1 w-3.5 h-3.5 border-2 border-white rounded-full ${apiStatus ? 'bg-emerald-500' : 'bg-red-500'}`} 
              title={apiStatus ? 'API Online' : 'API Offline'}
            ></div>
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-lg text-[#212529] tracking-tight leading-none">Phoen</span>
            <span className="text-[11px] font-semibold text-[#4A4A4A] leading-none mt-1 tracking-wider uppercase">CPQ & Revenue Ops</span>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="hidden lg:flex items-center h-full gap-1 overflow-x-auto shrink">
          {navItems.map((item) => {
            const isActive = location.pathname === '/' + item.id || location.pathname.startsWith('/' + item.id + '/');
            return (
              <Link
                key={item.id}
                to={`/${item.id}`}
                className={`h-full flex items-center px-3 text-sm font-semibold whitespace-nowrap transition-colors border-b-2 ${
                  isActive
                    ? 'text-[#714B67] border-[#714B67]'
                    : 'text-[#4A4A4A] border-transparent hover:text-[#212529]'
                }`}
              >
                <span>{item.label}</span>
                {item.badge && (
                  <span className={`ml-1.5 inline-flex items-center px-1.5 py-0.5 rounded-full border text-[10px] leading-none font-semibold ${item.badgeColor}`}>
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>

        {/* Action Controls */}
        <div className="flex items-center gap-3 shrink-0">
          {/* Global Search Input */}
          <div className="relative hidden md:flex items-center">
            <span className="material-symbols-outlined absolute left-3 text-[#6C757D] text-[20px] pointer-events-none">search</span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search accounts, quotes, SKUs..."
              className="h-10 w-52 lg:w-60 pl-10 pr-3 rounded-lg bg-[#F6F1F5] border border-[#CED4DA]/60 text-sm text-[#212529] placeholder:text-[#6C757D] focus:outline-none focus:border-[#714B67] focus:ring-2 focus:ring-[#714B67]/20 transition-all"
            />
          </div>

          {/* New Quote CTA (Only for Sales Rep & Admin) */}
          {canCreateQuote && (
            <button
              onClick={onOpenNewQuote}
              className="hidden sm:flex items-center gap-1.5 h-10 px-3.5 rounded-lg bg-[#714B67] hover:bg-[#5C3D54] text-white text-sm font-semibold shadow-sm transition-all active:scale-[0.98]"
            >
              <span className="material-symbols-outlined text-[18px]">add</span>
              <span>New Quote</span>
            </button>
          )}

          {/* Role Badge Indicator */}
          <div className="hidden sm:flex items-center">
            <span className={`px-2.5 py-1 rounded-lg border text-xs font-bold ${currentPersona.badgeColor}`}>
              {currentPersona.title}
            </span>
          </div>

          {/* Notification Button */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative flex items-center justify-center w-10 h-10 rounded-lg hover:bg-[#F6F1F5] text-[#4A4A4A] hover:text-[#212529] transition-colors"
              title="Notifications"
            >
              <span className="material-symbols-outlined text-[22px]">notifications</span>
              <span className="absolute top-2 right-2 w-2.5 h-2.5 rounded-full bg-[#714B67] ring-2 ring-white"></span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-xl bg-white border border-[#DEE2E6] shadow-xl z-50 p-4 animate-in fade-in slide-in-from-top-2">
                <div className="flex items-center justify-between pb-3 border-b border-[#DEE2E6]">
                  <span className="font-bold text-sm text-[#212529]">Role Notifications</span>
                  <button className="text-xs text-[#714B67] font-semibold hover:underline" onClick={() => setShowNotifications(false)}>
                    Mark all read
                  </button>
                </div>
                <div className="divide-y divide-[#DEE2E6] max-h-80 overflow-y-auto">
                  {notifications.map((n) => (
                    <div key={n.id} className="py-3 flex items-start gap-3 hover:bg-[#FAFAFA] px-2 rounded-lg transition-colors cursor-pointer">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5 ${
                        n.type === 'warning' ? 'bg-amber-100 text-amber-700' : n.type === 'success' ? 'bg-emerald-100 text-emerald-700' : 'bg-[#EFE6ED] text-[#5C3D54]'
                      }`}>
                        <span className="material-symbols-outlined text-[18px]">
                          {n.type === 'warning' ? 'warning' : n.type === 'success' ? 'check_circle' : 'info'}
                        </span>
                      </div>
                      <div className="flex flex-col min-w-0">
                        <div className="flex items-center justify-between gap-1">
                          <span className="text-xs font-bold text-[#212529] truncate">{n.title}</span>
                          <span className="text-[10px] text-[#6C757D] shrink-0">{n.time}</span>
                        </div>
                        <p className="text-xs text-[#4A4A4A] mt-0.5 leading-snug">{n.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="h-8 w-px bg-[#CED4DA]/50 hidden sm:block"></div>

          {/* User Profile & 1-Click Role Switcher */}
          <div className="relative">
            <div
              onClick={() => setShowProfileMenu(!showProfileMenu)}
              className="flex items-center gap-2 cursor-pointer p-1.5 rounded-xl hover:bg-[#F6F1F5] transition-colors border border-transparent hover:border-[#714B67]/20"
            >
              <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-[#714B67] to-[#8A6280] text-white flex items-center justify-center font-bold ring-2 ring-[#714B67]/20 shadow-xs">
                {currentUser?.name?.charAt(0) || 'U'}
              </div>
              <div className="hidden xl:flex flex-col text-left leading-tight">
                <span className="text-xs font-bold text-[#212529]">{currentUser?.name || 'User'}</span>
                <span className="text-[10px] text-[#6C757D] font-semibold capitalize">{currentPersona.title}</span>
              </div>
              <span className="material-symbols-outlined text-[18px] text-[#6C757D]">expand_more</span>
            </div>

            {showProfileMenu && (
              <div className="absolute right-0 mt-2 w-72 rounded-2xl bg-white border border-[#DEE2E6] shadow-2xl z-50 p-3 animate-in fade-in zoom-in-95">
                <div className="px-3 py-2 border-b border-[#DEE2E6]">
                  <span className="block text-xs font-bold text-[#212529]">{currentUser?.name || 'User'}</span>
                  <span className="block text-[11px] text-[#6C757D] font-mono">{currentUser?.email}</span>
                  <div className="mt-1">
                    <span className={`inline-block px-2 py-0.5 rounded-md text-[10px] font-bold border ${currentPersona.badgeColor}`}>
                      Current: {currentPersona.title}
                    </span>
                  </div>
                </div>

                {/* 1-Click Persona Switcher */}
                <div className="py-2 border-b border-[#DEE2E6]">
                  <span className="px-3 text-[10px] font-bold uppercase tracking-wider text-[#6C757D] block mb-1.5">
                    Switch Active Persona:
                  </span>
                  <div className="space-y-1">
                    {DEMO_PERSONAS.map((p) => {
                      const isCurrent = p.role === role;
                      return (
                        <button
                          key={p.role}
                          onClick={() => handleRoleSelect(p)}
                          className={`w-full text-left px-3 py-2 rounded-xl text-xs flex items-center justify-between transition-colors ${
                            isCurrent
                              ? 'bg-[#F6F1F5] text-[#714B67] font-bold'
                              : 'text-[#212529] hover:bg-[#FAFAFA] font-medium'
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            <span className={`material-symbols-outlined text-[18px] ${isCurrent ? 'text-[#714B67]' : 'text-[#6C757D]'}`}>
                              {p.icon}
                            </span>
                            <div>
                              <span className="block leading-tight">{p.title}</span>
                              <span className="text-[10px] text-[#6C757D] block font-normal">{p.name}</span>
                            </div>
                          </div>
                          {isCurrent && (
                            <span className="material-symbols-outlined text-[#714B67] text-[16px]">check</span>
                          )}
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div className="pt-2">
                  <button 
                    onClick={() => {
                      localStorage.removeItem('df360_token');
                      window.location.reload();
                    }}
                    className="w-full text-left px-3 py-2 text-xs text-red-600 hover:bg-red-50 rounded-xl flex items-center gap-2 font-semibold transition-colors"
                  >
                    <span className="material-symbols-outlined text-[16px]">logout</span> Sign Out
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Mobile Menu Toggle Button */}
          <button
            onClick={() => setShowMobileMenu(!showMobileMenu)}
            className="lg:hidden flex items-center justify-center w-10 h-10 rounded-lg hover:bg-[#F6F1F5] text-[#4A4A4A] hover:text-[#212529] transition-colors"
            title="Toggle Navigation Menu"
          >
            <span className="material-symbols-outlined text-[24px]">
              {showMobileMenu ? 'close' : 'menu'}
            </span>
          </button>
        </div>
      </div>

      {/* Mobile Navigation Drawer */}
      {showMobileMenu && (
        <div className="lg:hidden bg-white border-b border-[#DEE2E6] px-4 py-3 shadow-lg flex flex-col gap-1 animate-in slide-in-from-top-2">
          {navItems.map((item) => {
            const isActive = location.pathname === '/' + item.id || location.pathname.startsWith('/' + item.id + '/');
            return (
              <Link
                key={item.id}
                to={`/${item.id}`}
                onClick={() => setShowMobileMenu(false)}
                className={`flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-semibold transition-colors ${
                  isActive
                    ? 'bg-[#F6F1F5] text-[#714B67]'
                    : 'text-[#4A4A4A] hover:bg-[#FAFAFA] hover:text-[#212529]'
                }`}
              >
                <span>{item.label}</span>
                {item.badge && (
                  <span className={`px-2 py-0.5 rounded-full border text-[10px] leading-none font-semibold ${item.badgeColor}`}>
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
}
