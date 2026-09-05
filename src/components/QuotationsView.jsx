import React, { useState, useEffect } from 'react';
import { api, setToken } from '../api';

export default function QuotationsView({ setActiveTab, onOpenNewQuote }) {
  const [viewMode, setViewMode] = useState('board'); // 'board' or 'table'
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatusFilter, setSelectedStatusFilter] = useState('ALL');
  const [quotesData, setQuotesData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Auto-login as sales rep for demo
    async function loadData() {
      try {
        let token = localStorage.getItem('df360_token');
        if (!token) {
          const loginRes = await api.login('marcus@phoen.io', 'password');
          token = loginRes.access_token;
          setToken(token);
        }
        const data = await api.getQuotations();
        setQuotesData(data);
      } catch (err) {
        console.error('Failed to load quotations:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const filteredQuotes = quotesData.filter((q) => {
    const matchesSearch =
      q.account.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = selectedStatusFilter === 'ALL' || q.status === selectedStatusFilter;
    return matchesSearch && matchesStatus;
  });

  const columns = [
    { key: 'DRAFT', title: 'Draft', color: 'bg-[#76777d]', items: filteredQuotes.filter((q) => q.status === 'DRAFT') },
    { key: 'PENDING_APPROVAL', title: 'Pending Approval', color: 'bg-amber-500', items: filteredQuotes.filter((q) => q.status === 'PENDING_APPROVAL') },
    { key: 'READY', title: 'Ready to Send', color: 'bg-emerald-500', items: filteredQuotes.filter((q) => q.status === 'READY') },
    { key: 'NEGOTIATION', title: 'In Negotiation', color: 'bg-[#2563eb]', items: filteredQuotes.filter((q) => q.status === 'NEGOTIATION') },
    { key: 'WON', title: 'Won / Confirmed', color: 'bg-emerald-600', items: filteredQuotes.filter((q) => q.status === 'WON') },
  ];

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Title & Action Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-bold uppercase tracking-wider text-[#76777d]">Commercial Lifecycle</span>
            <span className="w-1.5 h-1.5 rounded-full bg-[#2563eb]"></span>
            <span className="font-mono text-xs text-[#45464d]">FY25 Q2 Portfolio</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30] tracking-tight">Quotations Pipeline</h1>
          <p className="text-sm text-[#45464d] mt-1">Track and manage customer proposals from initial draft to confirmed orders.</p>
        </div>
        <div className="flex items-center flex-wrap gap-3">
          {/* View Mode Switcher */}
          <div className="inline-flex p-1 bg-[#eff4ff] rounded-xl border border-[#e2e8f0]">
            <button
              onClick={() => setViewMode('board')}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                viewMode === 'board' ? 'bg-white text-[#0b1c30] shadow-sm' : 'text-[#45464d] hover:text-[#0b1c30]'
              }`}
            >
              <span className="material-symbols-outlined text-[18px] text-[#2563eb]">view_kanban</span>
              <span>Pipeline Board</span>
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                viewMode === 'table' ? 'bg-white text-[#0b1c30] shadow-sm' : 'text-[#45464d] hover:text-[#0b1c30]'
              }`}
            >
              <span className="material-symbols-outlined text-[18px]">table_rows</span>
              <span>Table View</span>
            </button>
          </div>

          <button
            onClick={onOpenNewQuote}
            className="flex items-center gap-2 px-5 h-11 rounded-xl bg-[#2563eb] text-white hover:bg-[#1d4ed8] shadow-md text-sm font-semibold transition-all active:scale-[0.98]"
          >
            <span className="material-symbols-outlined text-[20px]">add_circle</span>
            <span>New Quotation</span>
          </button>
        </div>
      </div>

      {/* Metrics Bar */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="bg-white p-4 rounded-xl border border-[#e2e8f0] shadow-xs flex flex-col justify-between">
          <span className="text-xs font-bold text-[#76777d] uppercase">Total Pipeline</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#0b1c30] font-mono">$570,050</span>
            <span className="text-xs font-bold text-emerald-700">+14.2%</span>
          </div>
          <span className="text-xs text-[#76777d] mt-1">16 Active Proposals</span>
        </div>
        <div className="bg-white p-4 rounded-xl border border-[#e2e8f0] shadow-xs flex flex-col justify-between">
          <span className="text-xs font-bold text-[#76777d] uppercase">Pending Review</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#0b1c30] font-mono">$128,600</span>
            <span className="text-xs font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-800">3 Deals</span>
          </div>
          <span className="text-xs text-[#76777d] mt-1">Avg turnaround: 4.1h</span>
        </div>
        <div className="bg-white p-4 rounded-xl border border-[#e2e8f0] shadow-xs flex flex-col justify-between">
          <span className="text-xs font-bold text-[#76777d] uppercase">Ready to Send</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#0b1c30] font-mono">$94,750</span>
            <span className="text-xs font-bold text-emerald-700">4 Approved</span>
          </div>
          <span className="text-xs text-[#76777d] mt-1">0 escalations active</span>
        </div>
        <div className="bg-white p-4 rounded-xl border border-[#e2e8f0] shadow-xs flex flex-col justify-between">
          <span className="text-xs font-bold text-[#76777d] uppercase">In Negotiation</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#0b1c30] font-mono">$62,000</span>
            <span className="text-xs font-bold text-[#2563eb]">2 Portals</span>
          </div>
          <span className="text-xs text-[#76777d] mt-1">Customer reply 18m ago</span>
        </div>
        <div className="bg-white p-4 rounded-xl border border-[#e2e8f0] shadow-xs flex flex-col justify-between col-span-2 lg:col-span-1">
          <span className="text-xs font-bold text-[#76777d] uppercase">Win Velocity</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#0b1c30]">11.4 Days</span>
            <span className="text-xs font-bold text-emerald-700">Fast</span>
          </div>
          <span className="text-xs text-[#76777d] mt-1">-2.8 days vs benchmark</span>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-[#e2e8f0] shadow-sm flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
        <div className="relative flex-1">
          <span className="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-[20px] text-[#76777d] pointer-events-none">search</span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by customer, quote number (e.g. Q-1042), or title..."
            className="w-full h-11 pl-11 pr-4 bg-[#eff4ff] rounded-lg text-sm text-[#0b1c30] placeholder:text-[#76777d] focus:outline-none focus:bg-white focus:ring-2 focus:ring-[#2563eb]/20 transition-all"
          />
        </div>
        <div className="flex items-center flex-wrap gap-2">
          {['ALL', 'DRAFT', 'PENDING_APPROVAL', 'READY', 'NEGOTIATION', 'WON'].map((st) => (
            <button
              key={st}
              onClick={() => setSelectedStatusFilter(st)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                selectedStatusFilter === st
                  ? 'bg-[#0f172a] text-white'
                  : 'bg-[#eff4ff] text-[#45464d] hover:bg-[#e5eeff]'
              }`}
            >
              {st.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Board View */}
      {viewMode === 'board' && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4 items-start">
          {columns.map((col) => (
            <div key={col.key} className="flex flex-col bg-[#eff4ff]/60 rounded-2xl p-3 border border-[#e2e8f0] gap-3 min-h-[500px]">
              <div className="flex items-center justify-between px-2 py-1">
                <div className="flex items-center gap-2">
                  <div className={`w-2.5 h-2.5 rounded-full ${col.color}`}></div>
                  <h2 className="text-sm font-bold text-[#0b1c30]">{col.title}</h2>
                  <span className="px-2 py-0.5 rounded-full bg-white text-xs font-bold text-[#0b1c30] shadow-xs">
                    {col.items.length}
                  </span>
                </div>
                <span className="font-mono text-xs font-bold text-[#45464d]">
                  ${col.items.reduce((sum, item) => sum + item.amount, 0).toLocaleString()}
                </span>
              </div>

              <div className="flex flex-col gap-3">
                {col.items.map((q) => (
                  <div
                    key={q.id}
                    onClick={() => {
                      if (q.id === 'Q-1042' && q.flagged) {
                        setActiveTab('approvals');
                      } else {
                        setActiveTab('quote-detail');
                      }
                    }}
                    className={`group bg-white p-4 rounded-xl shadow-xs border ${
                      q.flagged ? 'border-amber-400 ring-2 ring-amber-100' : 'border-[#e2e8f0] hover:border-[#2563eb]'
                    } transition-all cursor-pointer flex flex-col gap-2 relative overflow-hidden`}
                  >
                    {q.flagged && <div className="absolute top-0 left-0 bottom-0 w-1.5 bg-amber-500"></div>}
                    <div className="flex items-center justify-between">
                      <span className="px-2 py-0.5 rounded bg-[#eff4ff] text-xs font-mono font-bold text-[#0b1c30]">{q.id}</span>
                      {q.flagged ? (
                        <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-rose-50 text-rose-700 text-[10px] font-bold">
                          <span className="material-symbols-outlined text-[12px]">warning</span> Flagged
                        </span>
                      ) : (
                        <span className="text-[11px] text-[#76777d]">{q.time}</span>
                      )}
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-[#0b1c30] group-hover:text-[#2563eb] transition-colors">{q.account}</h3>
                      <p className="text-xs text-[#45464d] mt-0.5 line-clamp-1">{q.title}</p>
                      {q.flagReason && (
                        <div className="mt-1.5 p-2 rounded-lg bg-amber-50 text-amber-900 text-[11px] leading-tight font-semibold">
                          {q.flagReason}
                        </div>
                      )}
                    </div>
                    <div className="flex items-center justify-between pt-2 border-t border-[#f1f5f9]">
                      <span className="text-xs text-[#76777d]">{q.items} line items</span>
                      <span className="text-sm font-extrabold text-[#0b1c30] font-mono">${q.amount.toLocaleString()}</span>
                    </div>
                    <div className="flex items-center justify-between pt-1">
                      <div className="flex items-center gap-1.5">
                        <img src={q.repAvatar} alt={q.rep} className="w-5 h-5 rounded-full object-cover" />
                        <span className="text-[11px] text-[#45464d] font-medium">{q.rep}</span>
                      </div>
                      <span className="text-[11px] font-bold text-emerald-700">{q.margin} margin</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Table View */}
      {viewMode === 'table' && (
        <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#f8fafc] border-b border-[#e2e8f0] text-xs font-bold text-[#76777d] uppercase tracking-wider">
                <th className="py-3.5 px-4">Quote ID</th>
                <th className="py-3.5 px-4">Customer Account</th>
                <th className="py-3.5 px-4">Proposal Name</th>
                <th className="py-3.5 px-4">Sales Rep</th>
                <th className="py-3.5 px-4">Amount</th>
                <th className="py-3.5 px-4">Margin %</th>
                <th className="py-3.5 px-4">Status</th>
                <th className="py-3.5 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f1f5f9] text-xs font-medium text-[#0b1c30]">
              {filteredQuotes.map((q) => (
                <tr key={q.id} className="hover:bg-[#f8fafc] transition-colors cursor-pointer" onClick={() => setActiveTab('quote-detail')}>
                  <td className="py-3.5 px-4 font-mono font-bold text-[#2563eb]">{q.id}</td>
                  <td className="py-3.5 px-4 font-bold">{q.account}</td>
                  <td className="py-3.5 px-4 text-[#45464d]">{q.title}</td>
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-2">
                      <img src={q.repAvatar} alt={q.rep} className="w-6 h-6 rounded-full object-cover" />
                      <span>{q.rep}</span>
                    </div>
                  </td>
                  <td className="py-3.5 px-4 font-mono font-bold text-sm">${q.amount.toLocaleString()}</td>
                  <td className="py-3.5 px-4 font-bold text-emerald-700">{q.margin}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2.5 py-1 rounded-full text-[11px] font-bold ${
                      q.flagged ? 'bg-amber-100 text-amber-800' : 'bg-[#eff4ff] text-[#2563eb]'
                    }`}>
                      {q.statusLabel}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setActiveTab(q.flagged ? 'approvals' : 'quote-detail');
                      }}
                      className="px-3 py-1 rounded-lg bg-[#eff4ff] hover:bg-[#e5eeff] text-[#2563eb] font-bold text-xs"
                    >
                      {q.flagged ? 'Review Flags' : 'Open CPQ'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
