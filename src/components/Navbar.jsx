import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

export default function Navbar({ currentUser, apiStatus, onOpenNewQuote, searchQuery, setSearchQuery }) {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const location = useLocation();
  const navigate = useNavigate();
  const currentPath = location.pathname.substring(1) || 'dashboard';

  const role = currentUser?.role || 'sales_rep';

  const allNavItems = [
    { id: 'dashboard', label: 'Dashboard', roles: ['admin', 'sales_rep', 'manager', 'finance', 'customer'] },
    { id: 'quotations', label: 'Quotations', roles: ['sales_rep'] },
    { id: 'approvals', label: 'Approvals', badge: '4 pending', badgeColor: 'bg-amber-50 text-amber-700 border-amber-200', roles: ['manager', 'finance'] },
    { id: 'catalog', label: 'Catalog & Rules', roles: ['admin'] },
    { id: 'team', label: 'Team Management', roles: ['admin'] },
    { id: 'negotiation', label: 'Customer Portal', roles: ['sales_rep', 'customer'] },
    { id: 'fulfillment', label: 'Fulfillment', roles: ['sales_rep', 'customer'] },
    { id: 'subscriptions', label: 'Subscriptions', roles: ['finance', 'customer'] },
    { id: 'invoices', label: 'Invoices', roles: ['finance', 'customer'] },
    { id: 'deal-health', label: 'Deal Health', badge: '3 alerts', badgeColor: 'bg-rose-50 text-rose-700 border-rose-200', roles: ['manager'] },
  ];

  const navItems = allNavItems.filter(item => item.roles.includes(role));

  const notifications = [
    { id: 1, title: 'Quote Q-1042 Flagged', time: '12m ago', desc: '18% hardware discount exceeds 15% tier limit.', type: 'warning' },
    { id: 2, title: 'Contract Signed!', time: '1h ago', desc: 'TechCorp Industries accepted Quote Q-1039 ($142,000).', type: 'success' },
    { id: 3, title: 'New Customer Counter-Offer', time: '2h ago', desc: 'Global Logistics submitted request on Q-1040.', type: 'info' },
    { id: 4, title: 'Stock Allocation Ready', time: '3h ago', desc: 'Batch #SKU-9940 reserved for Order #ORD-8821.', type: 'info' },
  ];

  return (
    <header className="fixed top-0 left-0 w-full z-50 bg-[#ffffff] border-b border-[#c6c6cd]/40 shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
      <div className="h-20 w-full px-4 lg:px-8 flex items-center justify-between gap-4">
        {/* Brand & Logo */}
        <div className="flex items-center gap-3 shrink-0 cursor-pointer" onClick={() => navigate('/dashboard')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#0f172a] via-[#131b2e] to-[#2563eb] flex items-center justify-center text-white shadow-md relative">
            <span className="material-symbols-outlined text-[24px]">dataset</span>
            <div 
              className={`absolute -bottom-1 -right-1 w-3.5 h-3.5 border-2 border-white rounded-full ${apiStatus ? 'bg-emerald-500' : 'bg-red-500'}`} 
              title={apiStatus ? 'API Online' : 'API Offline'}
            ></div>
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-lg text-[#0b1c30] tracking-tight leading-none">Phoen</span>
            <span className="text-[11px] font-semibold text-[#45464d] leading-none mt-1 tracking-wider uppercase">CPQ & Revenue Ops</span>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="hidden xl:flex items-center h-full gap-1 overflow-x-auto shrink">
          {navItems.map((item) => {
            const isActive = currentPath === item.id;
            return (
              <Link
                key={item.id}
                to={`/${item.id}`}
                className={`h-full flex items-center px-3 text-sm font-semibold whitespace-nowrap transition-colors border-b-2 ${
                  isActive
                    ? 'text-[#2563eb] border-[#2563eb]'
                    : 'text-[#45464d] border-transparent hover:text-[#0b1c30]'
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
            <span className="material-symbols-outlined absolute left-3 text-[#76777d] text-[20px] pointer-events-none">search</span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search quotes, accounts, SKUs..."
              className="h-10 w-56 lg:w-64 pl-10 pr-3 rounded-lg bg-[#eff4ff] border border-[#c6c6cd]/60 text-sm text-[#0b1c30] placeholder:text-[#76777d] focus:outline-none focus:border-[#2563eb] focus:ring-2 focus:ring-[#2563eb]/20 transition-all"
            />
          </div>

          {/* New Quote CTA */}
          <button
            onClick={onOpenNewQuote}
            className="hidden sm:flex items-center gap-1.5 h-10 px-3.5 rounded-lg bg-[#2563eb] hover:bg-[#1d4ed8] text-white text-sm font-semibold shadow-sm transition-all active:scale-[0.98]"
          >
            <span className="material-symbols-outlined text-[18px]">add</span>
            <span>New Quote</span>
          </button>

          {/* Notification Button & Drawer */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative flex items-center justify-center w-10 h-10 rounded-lg hover:bg-[#eff4ff] text-[#45464d] hover:text-[#0b1c30] transition-colors"
              title="Notifications"
            >
              <span className="material-symbols-outlined text-[22px]">notifications</span>
              <span className="absolute top-2 right-2 w-2.5 h-2.5 rounded-full bg-[#2563eb] ring-2 ring-white"></span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-xl bg-white border border-[#e2e8f0] shadow-xl z-50 p-4 animate-in fade-in slide-in-from-top-2">
                <div className="flex items-center justify-between pb-3 border-b border-[#e2e8f0]">
                  <span className="font-bold text-sm text-[#0b1c30]">Notifications (4)</span>
                  <button className="text-xs text-[#2563eb] font-semibold hover:underline" onClick={() => setShowNotifications(false)}>
                    Mark all read
                  </button>
                </div>
                <div className="divide-y divide-[#e2e8f0] max-h-80 overflow-y-auto">
                  {notifications.map((n) => (
                    <div key={n.id} className="py-3 flex items-start gap-3 hover:bg-[#f8fafc] px-2 rounded-lg transition-colors cursor-pointer">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5 ${
                        n.type === 'warning' ? 'bg-amber-100 text-amber-700' : n.type === 'success' ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700'
                      }`}>
                        <span className="material-symbols-outlined text-[18px]">
                          {n.type === 'warning' ? 'warning' : n.type === 'success' ? 'check_circle' : 'info'}
                        </span>
                      </div>
                      <div className="flex flex-col min-w-0">
                        <div className="flex items-center justify-between gap-1">
                          <span className="text-xs font-bold text-[#0b1c30] truncate">{n.title}</span>
                          <span className="text-[10px] text-[#76777d] shrink-0">{n.time}</span>
                        </div>
                        <p className="text-xs text-[#45464d] mt-0.5 leading-snug">{n.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="h-8 w-px bg-[#c6c6cd]/50 hidden sm:block"></div>

          {/* User Profile */}
          <div className="relative">
            <div
              onClick={() => setShowProfileMenu(!showProfileMenu)}
              className="flex items-center gap-2 cursor-pointer p-1 rounded-lg hover:bg-[#eff4ff] transition-colors"
            >
              <div className="w-9 h-9 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold ring-2 ring-[#2563eb]/20">
                {currentUser?.name?.charAt(0) || 'U'}
              </div>
              <div className="hidden xl:flex flex-col text-left leading-tight">
                <span className="text-xs font-bold text-[#0b1c30]">{currentUser?.name || 'User'}</span>
                <span className="text-[11px] text-[#45464d] capitalize">{currentUser?.role?.replace('_', ' ') || 'Role'}</span>
              </div>
              <span className="material-symbols-outlined text-[18px] text-[#76777d]">expand_more</span>
            </div>

            {showProfileMenu && (
              <div className="absolute right-0 mt-2 w-56 rounded-xl bg-white border border-[#e2e8f0] shadow-xl z-50 p-2">
                <div className="px-3 py-2 border-b border-[#e2e8f0]">
                  <span className="block text-xs font-bold text-[#0b1c30]">{currentUser?.name || 'User'}</span>
                  <span className="block text-[11px] text-[#76777d]">{currentUser?.email || 'user@example.com'}</span>
                </div>
                <div className="py-1">
                  <button className="w-full text-left px-3 py-1.5 text-xs text-[#0b1c30] hover:bg-[#f1f5f9] rounded-md flex items-center gap-2">
                    <span className="material-symbols-outlined text-[16px]">person</span> User Settings
                  </button>
                  <button className="w-full text-left px-3 py-1.5 text-xs text-[#0b1c30] hover:bg-[#f1f5f9] rounded-md flex items-center gap-2">
                    <span className="material-symbols-outlined text-[16px]">settings</span> Preferences
                  </button>
                  <button 
                    onClick={() => {
                      localStorage.removeItem('df360_token');
                      window.location.reload();
                    }}
                    className="w-full text-left px-3 py-1.5 text-xs text-red-600 hover:bg-red-50 rounded-md flex items-center gap-2"
                  >
                    <span className="material-symbols-outlined text-[16px]">logout</span> Sign Out
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
