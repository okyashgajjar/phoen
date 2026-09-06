import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../api';

export default function QuotationsView({ currentUser, onOpenNewQuote }) {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [viewMode, setViewMode] = useState('board'); // 'board' or 'table'
  const [searchQuery, setSearchQuery] = useState('');
  
  const initialStatus = searchParams.get('status') || 'ALL';
  const [selectedStatusFilter, setSelectedStatusFilter] = useState(initialStatus);
  const [selectedRepFilter, setSelectedRepFilter] = useState('ALL');
  const [quotesData, setQuotesData] = useState([]);

  const role = currentUser?.role || 'sales_rep';
  const canCreateQuote = ['sales_rep', 'manager', 'admin'].includes(role);

  // Sync state if URL query param changes
  useEffect(() => {
    const statusParam = searchParams.get('status');
    if (statusParam && ['ALL', 'DRAFT', 'PENDING_APPROVAL', 'READY', 'NEGOTIATION', 'WON'].includes(statusParam)) {
      setSelectedStatusFilter(statusParam);
    } else if (!statusParam) {
      setSelectedStatusFilter('ALL');
    }
  }, [searchParams]);

  const handleStatusFilterChange = (status) => {
    setSelectedStatusFilter(status);
    if (status === 'ALL') {
      searchParams.delete('status');
      setSearchParams(searchParams);
    } else {
      setSearchParams({ status });
    }
  };

  useEffect(() => {
    async function loadData() {
      try {
        const data = await api.getQuotations();
        setQuotesData(data);
      } catch (err) {
        console.error('Failed to load quotations:', err);
      }
    }
    loadData();
  }, [currentUser]);

  // Extract unique sales reps for the manager filter
  const uniqueReps = Array.from(new Set(quotesData.map(q => q.rep).filter(Boolean)));

  const filteredQuotes = (quotesData || []).filter((q) => {
    if (!q) return false;
    const accountStr = (q.account || q.customer_name || '').toLowerCase();
    const idStr = (q.id || '').toLowerCase();
    const titleStr = (q.title || '').toLowerCase();
    const repStr = (q.rep || '').toLowerCase();
    const search = (searchQuery || '').toLowerCase();
    const matchesSearch =
      accountStr.includes(search) ||
      idStr.includes(search) ||
      titleStr.includes(search) ||
      repStr.includes(search);
    const matchesStatus = selectedStatusFilter === 'ALL' || q.status === selectedStatusFilter;
    const matchesRep = selectedRepFilter === 'ALL' || q.rep === selectedRepFilter;
    return matchesSearch && matchesStatus && matchesRep;
  });

  const columns = [
    { key: 'DRAFT', title: 'Draft', color: 'bg-[#6C757D]', items: filteredQuotes.filter((q) => q.status === 'DRAFT') },
    { key: 'PENDING_APPROVAL', title: 'Pending Approval', color: 'bg-amber-500', items: filteredQuotes.filter((q) => q.status === 'PENDING_APPROVAL') },
    { key: 'READY', title: 'Ready to Send', color: 'bg-emerald-500', items: filteredQuotes.filter((q) => q.status === 'READY') },
    { key: 'NEGOTIATION', title: 'In Negotiation', color: 'bg-[#714B67]', items: filteredQuotes.filter((q) => q.status === 'NEGOTIATION') },
    { key: 'WON', title: 'Won / Confirmed', color: 'bg-emerald-600', items: filteredQuotes.filter((q) => q.status === 'WON') },
  ];

  const visibleColumns = selectedStatusFilter === 'ALL'
    ? columns
    : columns.filter((col) => col.key === selectedStatusFilter);

  const totalPipeline = quotesData.reduce((acc, q) => acc + (Number(q.amount) || 0), 0);
  const pendingQuotes = quotesData.filter(q => q.status === 'PENDING_APPROVAL');
  const readyQuotes = quotesData.filter(q => q.status === 'READY');
  const negotiationQuotes = quotesData.filter(q => q.status === 'NEGOTIATION');

  const getPageTitle = () => {
    switch (role) {
      case 'sales_rep': return 'My Proposals Pipeline';
      case 'manager': return 'Team Sales Pipeline';
      case 'finance': return 'Quotations Commercial Audit';
      case 'admin':
      default:
        return 'Global Commercial Pipeline';
    }
  };

  const getPageSubtitle = () => {
    switch (role) {
      case 'sales_rep': return 'Create, configure, and advance your personal commercial quotations and customer proposals.';
      case 'manager': return 'Supervise team sales pipeline, review flagged margin exceptions, and track deal conversions.';
      case 'finance': return 'Read-only financial governance of commercial proposals, invoice schedules, and contract commitments.';
      case 'admin':
      default:
        return 'Enterprise-wide CPQ visibility across all customer accounts, sales representatives, and approval states.';
    }
  };

  const handleCardClick = (quote) => {
    if (role === 'manager' && quote.status === 'PENDING_APPROVAL') {
      navigate(`/approvals/${quote.id}`);
    } else {
      navigate(`/quote-detail/${quote.id}`);
    }
  };

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#6C757D] mb-1">
            <span>Commercial Operations</span>
            <span>/</span>
            <span className="text-[#714B67]">{getPageTitle()}</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529]">{getPageTitle()}</h1>
          <p className="text-sm text-[#4A4A4A] mt-1">{getPageSubtitle()}</p>
        </div>

        <div className="flex items-center gap-2">
          <div className="bg-[#F6F1F5] p-1 rounded-xl flex items-center gap-1 border border-[#DEE2E6]">
            <button
              onClick={() => setViewMode('board')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                viewMode === 'board' ? 'bg-white text-[#212529] shadow-xs' : 'text-[#6C757D] hover:text-[#212529]'
              }`}
            >
              <span className="material-symbols-outlined text-[18px]">view_kanban</span>
              <span>Board</span>
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                viewMode === 'table' ? 'bg-white text-[#212529] shadow-xs' : 'text-[#6C757D] hover:text-[#212529]'
              }`}
            >
              <span className="material-symbols-outlined text-[18px]">table_rows</span>
              <span>Table</span>
            </button>
          </div>

          {canCreateQuote && (
            <button
              onClick={onOpenNewQuote}
              className="flex items-center gap-2 px-5 h-11 rounded-xl bg-[#714B67] text-white hover:bg-[#5C3D54] font-bold text-xs shadow-md transition-all active:scale-[0.98]"
            >
              <span className="material-symbols-outlined text-[18px]">add_circle</span>
              <span>New Quotation</span>
            </button>
          )}
        </div>
      </div>

      {/* Metrics Bar — Interactive quick-filters */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <div 
          onClick={() => handleStatusFilterChange('ALL')}
          className={`p-4 rounded-xl border shadow-xs flex flex-col justify-between cursor-pointer transition-all ${
            selectedStatusFilter === 'ALL'
              ? 'bg-[#F8F4F7]/70 border-[#714B67] ring-2 ring-[#714B67]/20'
              : 'bg-white border-[#DEE2E6] hover:border-[#714B67]/40'
          }`}
        >
          <span className="text-xs font-bold text-[#6C757D] uppercase">Total Pipeline</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#212529] font-mono">
              ${totalPipeline.toLocaleString()}
            </span>
            <span className="text-xs font-bold text-emerald-700">+14.2%</span>
          </div>
          <span className="text-xs text-[#6C757D] mt-1">{quotesData.length} Total Proposals &bull; Show All</span>
        </div>

        <div 
          onClick={() => handleStatusFilterChange(selectedStatusFilter === 'PENDING_APPROVAL' ? 'ALL' : 'PENDING_APPROVAL')}
          className={`p-4 rounded-xl border shadow-xs flex flex-col justify-between cursor-pointer transition-all ${
            selectedStatusFilter === 'PENDING_APPROVAL'
              ? 'bg-amber-50 border-amber-500 ring-2 ring-amber-300 shadow-md'
              : 'bg-white border-[#DEE2E6] hover:border-amber-400'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase">Pending Review</span>
            {selectedStatusFilter === 'PENDING_APPROVAL' && (
              <span className="px-1.5 py-0.5 rounded bg-amber-500 text-white text-[9px] font-extrabold tracking-wider">ACTIVE</span>
            )}
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#212529] font-mono">
              ${pendingQuotes.reduce((acc, q) => acc + (Number(q.amount) || 0), 0).toLocaleString()}
            </span>
            <span className="text-xs font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-800">
              {pendingQuotes.length} Deals
            </span>
          </div>
          <span className="text-xs text-[#6C757D] mt-1">
            {selectedStatusFilter === 'PENDING_APPROVAL' ? 'Click to show all proposals' : 'Click to view only pending deals'}
          </span>
        </div>

        <div 
          onClick={() => handleStatusFilterChange(selectedStatusFilter === 'READY' ? 'ALL' : 'READY')}
          className={`p-4 rounded-xl border shadow-xs flex flex-col justify-between cursor-pointer transition-all ${
            selectedStatusFilter === 'READY'
              ? 'bg-emerald-50 border-emerald-500 ring-2 ring-emerald-300 shadow-md'
              : 'bg-white border-[#DEE2E6] hover:border-emerald-400'
          }`}
        >
          <span className="text-xs font-bold text-[#6C757D] uppercase">Ready to Send</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#212529] font-mono">
              ${readyQuotes.reduce((acc, q) => acc + (Number(q.amount) || 0), 0).toLocaleString()}
            </span>
            <span className="text-xs font-bold text-emerald-700">{readyQuotes.length} Approved</span>
          </div>
          <span className="text-xs text-[#6C757D] mt-1">0 escalations active</span>
        </div>

        <div 
          onClick={() => handleStatusFilterChange(selectedStatusFilter === 'NEGOTIATION' ? 'ALL' : 'NEGOTIATION')}
          className={`p-4 rounded-xl border shadow-xs flex flex-col justify-between cursor-pointer transition-all ${
            selectedStatusFilter === 'NEGOTIATION'
              ? 'bg-[#F8F4F7] border-[#8A6280] ring-2 ring-[#C7A9BF] shadow-md'
              : 'bg-white border-[#DEE2E6] hover:border-[#A8809E]'
          }`}
        >
          <span className="text-xs font-bold text-[#6C757D] uppercase">In Negotiation</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#212529] font-mono">
              ${negotiationQuotes.reduce((acc, q) => acc + (Number(q.amount) || 0), 0).toLocaleString()}
            </span>
            <span className="text-xs font-bold text-[#714B67]">{negotiationQuotes.length} Portals</span>
          </div>
          <span className="text-xs text-[#6C757D] mt-1">Customer reply 18m ago</span>
        </div>

        <div className="bg-white p-4 rounded-xl border border-[#DEE2E6] shadow-xs flex flex-col justify-between col-span-2 lg:col-span-1">
          <span className="text-xs font-bold text-[#6C757D] uppercase">Win Velocity</span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-[#212529]">11.4 Days</span>
            <span className="text-xs font-bold text-emerald-700">Fast</span>
          </div>
          <span className="text-xs text-[#6C757D] mt-1">-2.8 days vs benchmark</span>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-[#DEE2E6] shadow-sm flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
        <div className="relative flex-1">
          <span className="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-[20px] text-[#6C757D] pointer-events-none">search</span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by customer, quote number (e.g. Q-1042), or title..."
            className="w-full h-11 pl-11 pr-4 bg-[#F6F1F5] rounded-lg text-sm text-[#212529] placeholder:text-[#6C757D] focus:outline-none focus:bg-white focus:ring-2 focus:ring-[#714B67]/20 transition-all"
          />
        </div>

        {/* Sales Rep Filter for Manager, Admin & Finance */}
        {role !== 'sales_rep' && uniqueReps.length > 0 && (
          <div className="flex items-center gap-2 shrink-0">
            <span className="text-xs font-bold text-[#6C757D]">Rep:</span>
            <select
              value={selectedRepFilter}
              onChange={(e) => setSelectedRepFilter(e.target.value)}
              className="h-10 px-3 rounded-lg bg-[#F6F1F5] border border-[#DEE2E6] text-xs font-bold text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20"
            >
              <option value="ALL">All Representatives ({quotesData.length})</option>
              {uniqueReps.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="flex items-center flex-wrap gap-2">
          {['ALL', 'DRAFT', 'PENDING_APPROVAL', 'READY', 'NEGOTIATION', 'WON'].map((st) => (
            <button
              key={st}
              onClick={() => handleStatusFilterChange(st)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                selectedStatusFilter === st
                  ? 'bg-[#212529] text-white shadow-xs'
                  : 'bg-[#F6F1F5] text-[#4A4A4A] hover:bg-[#EFE6ED]'
              }`}
            >
              {st.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Active Filter Banner */}
      {selectedStatusFilter !== 'ALL' && (
        <div className="bg-amber-50 border border-amber-300 rounded-xl p-3 px-4 flex items-center justify-between gap-4 animate-in fade-in">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-amber-700 text-[20px]">filter_alt</span>
            <span className="text-xs font-bold text-amber-950">
              Filtered View: Showing only <strong className="underline">{selectedStatusFilter.replace('_', ' ')}</strong> requests ({filteredQuotes.length} proposals found)
            </span>
          </div>
          <button
            onClick={() => handleStatusFilterChange('ALL')}
            className="text-xs font-bold text-[#714B67] hover:underline flex items-center gap-1 bg-white px-3 py-1 rounded-lg border border-amber-200 shadow-xs"
          >
            <span>Show all proposals</span>
            <span className="material-symbols-outlined text-[16px]">close</span>
          </button>
        </div>
      )}

      {/* Empty State */}
      {filteredQuotes.length === 0 && (
        <div className="bg-white rounded-2xl border border-[#DEE2E6] p-12 text-center flex flex-col items-center gap-3">
          <div className="w-14 h-14 rounded-2xl bg-slate-100 flex items-center justify-center text-slate-400">
            <span className="material-symbols-outlined text-[32px]">search_off</span>
          </div>
          <h3 className="text-base font-bold text-[#212529]">No Proposals Found</h3>
          <p className="text-xs text-[#6C757D] max-w-sm">
            {selectedStatusFilter !== 'ALL' 
              ? `There are currently no proposals in ${selectedStatusFilter.replace('_', ' ')} status matching your criteria.`
              : 'No proposals match your current search query.'}
          </p>
          <button
            onClick={() => {
              setSelectedStatusFilter('ALL');
              setSearchQuery('');
              handleStatusFilterChange('ALL');
            }}
            className="mt-2 px-4 py-2 rounded-xl bg-[#F6F1F5] text-[#714B67] font-bold text-xs hover:bg-[#EFE6ED]"
          >
            Clear Filters & View All Proposals
          </button>
        </div>
      )}

      {/* Board View */}
      {viewMode === 'board' && filteredQuotes.length > 0 && (
        <div className={`grid grid-cols-1 ${
          selectedStatusFilter !== 'ALL' ? 'max-w-3xl mx-auto w-full' : 'md:grid-cols-2 xl:grid-cols-5'
        } gap-4 items-start`}>
          {visibleColumns.map((col) => (
            <div key={col.key} className="flex flex-col bg-[#F6F1F5]/60 rounded-2xl p-3 border border-[#DEE2E6] gap-3 min-h-[500px]">
              <div className="flex items-center justify-between px-2 py-1">
                <div className="flex items-center gap-2">
                  <div className={`w-2.5 h-2.5 rounded-full ${col.color}`}></div>
                  <h2 className="text-sm font-bold text-[#212529]">{col.title}</h2>
                  <span className="px-2 py-0.5 rounded-full bg-white text-xs font-bold text-[#212529] shadow-xs">
                    {col.items.length}
                  </span>
                </div>
                <span className="font-mono text-xs font-bold text-[#4A4A4A]">
                  ${col.items.reduce((sum, item) => sum + (Number(item.amount) || 0), 0).toLocaleString()}
                </span>
              </div>

              <div className="flex flex-col gap-3">
                {col.items.map((q) => (
                  <div
                    key={q.id}
                    onClick={() => handleCardClick(q)}
                    className={`group bg-white p-4 rounded-xl shadow-xs border ${
                      q.flagged ? 'border-amber-400 ring-2 ring-amber-100' : 'border-[#DEE2E6] hover:border-[#714B67]'
                    } transition-all cursor-pointer flex flex-col gap-2 relative overflow-hidden`}
                  >
                    {q.flagged && <div className="absolute top-0 left-0 bottom-0 w-1.5 bg-amber-500"></div>}
                    <div className="flex items-center justify-between">
                      <span className="px-2 py-0.5 rounded bg-[#F6F1F5] text-xs font-mono font-bold text-[#212529]">{q.id}</span>
                      {q.flagged ? (
                        <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-rose-50 text-rose-700 text-[10px] font-bold">
                          <span className="material-symbols-outlined text-[12px]">warning</span> Flagged
                        </span>
                      ) : (
                        <span className="text-[11px] text-[#6C757D]">{q.time}</span>
                      )}
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-[#212529] group-hover:text-[#714B67] transition-colors">{q.account || q.customer_name || 'Customer Account'}</h3>
                      <p className="text-xs text-[#4A4A4A] mt-0.5 line-clamp-1">{q.title}</p>
                      {q.flagReason && (
                        <div className="mt-1.5 p-2 rounded-lg bg-amber-50 text-amber-900 text-[11px] leading-tight font-semibold">
                          {q.flagReason}
                        </div>
                      )}
                    </div>
                    <div className="flex items-center justify-between pt-2 border-t border-[#F1F1F1]">
                      <span className="text-xs text-[#6C757D]">{q.items || 3} line items</span>
                      <span className="text-sm font-extrabold text-[#212529] font-mono">${(Number(q.amount) || 0).toLocaleString()}</span>
                    </div>
                    <div className="flex items-center justify-between pt-1">
                      <div className="flex items-center gap-1.5">
                        {q.repAvatar ? (
                          <img src={q.repAvatar} alt={q.rep} className="w-5 h-5 rounded-full object-cover" />
                        ) : (
                          <div className="w-5 h-5 rounded-full bg-[#714B67] text-white text-[10px] flex items-center justify-center font-bold">
                            {(q.rep || 'S')[0]}
                          </div>
                        )}
                        <span className="text-[11px] text-[#4A4A4A] font-medium">{q.rep || 'Marcus Vance'}</span>
                      </div>
                      <span className="text-[11px] font-bold text-emerald-700">{q.margin || '28.2%'} margin</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Table View */}
      {viewMode === 'table' && filteredQuotes.length > 0 && (
        <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#FAFAFA] border-b border-[#DEE2E6] text-xs font-bold text-[#6C757D] uppercase tracking-wider">
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
            <tbody className="divide-y divide-[#F1F1F1] text-xs font-medium text-[#212529]">
              {filteredQuotes.map((q) => (
                <tr key={q.id} className="hover:bg-[#FAFAFA] transition-colors cursor-pointer" onClick={() => handleCardClick(q)}>
                  <td className="py-3.5 px-4 font-mono font-bold text-[#714B67]">{q.id}</td>
                  <td className="py-3.5 px-4 font-bold">{q.account || q.customer_name || 'Customer Account'}</td>
                  <td className="py-3.5 px-4 text-[#4A4A4A]">{q.title}</td>
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-2">
                      {q.repAvatar ? (
                        <img src={q.repAvatar} alt={q.rep} className="w-6 h-6 rounded-full object-cover" />
                      ) : (
                        <div className="w-6 h-6 rounded-full bg-[#714B67] text-white text-[10px] flex items-center justify-center font-bold">
                          {(q.rep || 'S')[0]}
                        </div>
                      )}
                      <span>{q.rep || 'Marcus Vance'}</span>
                    </div>
                  </td>
                  <td className="py-3.5 px-4 font-mono font-bold text-sm">${(Number(q.amount) || 0).toLocaleString()}</td>
                  <td className="py-3.5 px-4 font-bold text-emerald-700">{q.margin || '28.2%'}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2.5 py-1 rounded-full text-[11px] font-bold ${
                      q.flagged ? 'bg-amber-100 text-amber-800' : 'bg-[#F6F1F5] text-[#714B67]'
                    }`}>
                      {q.statusLabel || q.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCardClick(q);
                      }}
                      className="px-3 py-1 rounded-lg bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs"
                    >
                      {role === 'manager' && q.status === 'PENDING_APPROVAL' ? 'Review Approval' : 'Open Details'}
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
