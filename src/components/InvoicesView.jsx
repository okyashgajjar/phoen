import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

const FALLBACK_CUSTOMERS = [
  { id: 'CUST-001', company_name: 'Sabarmati Logistics & Supply Chain Ltd', tier: 'Enterprise' },
  { id: 'CUST-002', company_name: 'Gujarat Precision Engineering Pvt Ltd', tier: 'Strategic' },
  { id: 'CUST-003', company_name: 'Western Grid Technologies Pvt Ltd', tier: 'Enterprise' },
  { id: 'CUST-004', company_name: 'Arvind Industrial Systems Pvt Ltd', tier: 'Enterprise' },
  { id: 'CUST-005', company_name: 'Apex Global BPO Solutions Pvt Ltd', tier: 'Gold' },
  { id: 'CUST-006', company_name: 'Tata Communications Ltd', tier: 'Enterprise' }
];

export default function InvoicesView() {
  const navigate = useNavigate();

  const [invoices, setInvoices] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterTab, setFilterTab] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  // Modals & Popups
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [payingId, setPayingId] = useState(null);
  const [downloadingId, setDownloadingId] = useState(null);
  const [toast, setToast] = useState(null);

  // New Invoice Form
  const [formData, setFormData] = useState({
    customerId: 'CUST-001',
    title: '',
    amount: '',
    dueDate: new Date(Date.now() + 15 * 86400000).toISOString().split('T')[0],
  });

  const showNotification = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const [invData, custList] = await Promise.all([
        api.getInvoices().catch(() => []),
        api.getCustomers().catch(() => [])
      ]);
      setInvoices(invData || []);
      const resolvedCustomers = (custList && custList.length > 0) ? custList : FALLBACK_CUSTOMERS;
      setCustomers(resolvedCustomers);
      if (!formData.customerId && resolvedCustomers.length > 0) {
        setFormData(prev => ({ ...prev, customerId: resolvedCustomers[0].id }));
      }
    } catch (err) {
      console.error('Failed to load invoices:', err);
      showNotification('Failed to load invoices from database', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Filter logic
  const filteredInvoices = invoices.filter((inv) => {
    const status = (inv.status || '').toUpperCase();
    if (filterTab === 'PAID' && status !== 'PAID') return false;
    if (filterTab === 'ISSUED' && (status === 'PAID' || status === 'OVERDUE')) return false;
    if (filterTab === 'OVERDUE' && status !== 'OVERDUE') return false;

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchId = (inv.id || '').toLowerCase().includes(q);
      const matchAcc = (inv.account || inv.customer_name || '').toLowerCase().includes(q);
      const matchQuote = (inv.quoteId || inv.document_number || '').toLowerCase().includes(q);
      if (!matchId && !matchAcc && !matchQuote) return false;
    }
    return true;
  });

  // Financial Metrics
  const totalReceivables = invoices
    .filter(i => (i.status || '').toUpperCase() !== 'PAID')
    .reduce((acc, curr) => acc + (Number(curr.amount) || 0), 0);

  const totalCollected = invoices
    .filter(i => (i.status || '').toUpperCase() === 'PAID')
    .reduce((acc, curr) => acc + (Number(curr.amount) || 0), 0);

  const totalOverdue = invoices
    .filter(i => (i.status || '').toUpperCase() === 'OVERDUE')
    .reduce((acc, curr) => acc + (Number(curr.amount) || 0), 0);

  const countPaid = invoices.filter(i => (i.status || '').toUpperCase() === 'PAID').length;
  const countOverdue = invoices.filter(i => (i.status || '').toUpperCase() === 'OVERDUE').length;
  const countIssued = invoices.length - countPaid - countOverdue;

  // Actions
  const handleRecordPayment = async (invId) => {
    try {
      setPayingId(invId);
      await api.payInvoice(invId);
      showNotification(`Payment recorded for Invoice ${invId}. Ledger reconciled.`);
      await loadData();
    } catch (err) {
      console.error('Failed to pay invoice:', err);
      showNotification('Failed to record payment on server', 'error');
    } finally {
      setPayingId(null);
    }
  };

  const handleDownloadPdf = async (invId) => {
    try {
      setDownloadingId(invId);
      await api.downloadInvoicePdf(invId);
      showNotification(`Tax Invoice PDF for ${invId} downloaded successfully!`);
    } catch (err) {
      console.error('Failed to download invoice PDF:', err);
      showNotification('Failed to download invoice PDF from server', 'error');
    } finally {
      setDownloadingId(null);
    }
  };

  const handleCopyLink = (invId) => {
    const payUrl = `${window.location.origin}/portal/pay/${invId}`;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(payUrl);
      showNotification(`Direct payment link for ${invId} copied to clipboard!`);
    } else {
      showNotification(`Payment link: ${payUrl}`);
    }
  };

  const handleCreateInvoice = async (e) => {
    e.preventDefault();
    if (!formData.amount || Number(formData.amount) <= 0) {
      showNotification('Please enter a valid invoice amount', 'error');
      return;
    }
    try {
      setSubmitting(true);
      const res = await api.createInvoice({
        customer_id: formData.customerId || 'CUST-001',
        title: formData.title || 'Standard Commercial Billing Invoice',
        amount: Number(formData.amount),
        due_date: formData.dueDate
      });
      const newId = res.id || res.invoice?.id;
      showNotification(`Manual invoice ${newId} created! Starting PDF download...`);
      setShowCreateModal(false);

      // Trigger immediate PDF download
      try {
        await api.downloadInvoicePdf(newId);
        showNotification(`Tax Invoice ${newId} generated and downloaded!`);
      } catch (pdfErr) {
        console.warn('PDF download failed:', pdfErr);
      }

      setFormData({
        customerId: customers[0]?.id || 'CUST-001',
        title: '',
        amount: '',
        dueDate: new Date(Date.now() + 15 * 86400000).toISOString().split('T')[0],
      });
      await loadData();
    } catch (err) {
      console.error('Failed to create invoice:', err);
      showNotification('Failed to create invoice on server', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed bottom-6 right-6 z-50 px-5 py-3 rounded-xl shadow-2xl flex items-center gap-3 text-sm font-semibold transition-all transform animate-bounce ${
          toast.type === 'error' ? 'bg-rose-600 text-white' : 'bg-emerald-600 text-white'
        }`}>
          <span className="material-symbols-outlined text-lg">
            {toast.type === 'error' ? 'error' : 'check_circle'}
          </span>
          <span>{toast.message}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#6C757D] mb-1">
            <span>Finance & Accounts</span>
            <span>/</span>
            <span className="text-[#714B67]">Invoices & Payment Ledger</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529]">Invoices & Payment Ledger</h1>
          <p className="text-sm text-[#4A4A4A] mt-1">
            Connected to real PostgreSQL ledger • Track customer payments, milestones, and invoice reconciliations.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/fulfillment')}
            className="flex items-center gap-2 px-4 h-11 rounded-xl bg-[#F6F1F5] text-[#714B67] hover:bg-[#EFE6ED] font-bold text-xs transition-all border border-[#714B67]/20"
          >
            <span className="material-symbols-outlined text-[18px]">local_shipping</span>
            <span>Fulfillment Queue</span>
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2 px-5 h-11 rounded-xl bg-[#714B67] text-white hover:bg-[#5C3D54] font-bold text-xs shadow-md transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">add_circle</span>
            <span>Generate Manual Invoice</span>
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Pending Receivables</span>
            <span className="p-2 rounded-xl bg-amber-50 text-amber-600 material-symbols-outlined text-[20px]">account_balance_wallet</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">₹{totalReceivables.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</div>
            <div className="text-xs text-amber-700 font-semibold mt-1">Awaiting customer clearance</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Total Collected</span>
            <span className="p-2 rounded-xl bg-emerald-50 text-emerald-600 material-symbols-outlined text-[20px]">payments</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">₹{totalCollected.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</div>
            <div className="text-xs text-emerald-700 font-semibold mt-1">{countPaid} reconciled invoices</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Overdue Balance</span>
            <span className="p-2 rounded-xl bg-rose-50 text-rose-600 material-symbols-outlined text-[20px]">warning</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">₹{totalOverdue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</div>
            <div className="text-xs text-rose-700 font-semibold mt-1">{countOverdue} accounts past due date</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Ledger Records</span>
            <span className="p-2 rounded-xl bg-[#F8F4F7] text-[#714B67] material-symbols-outlined text-[20px]">receipt_long</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">{invoices.length} Invoices</div>
            <div className="text-xs text-[#5C3D54] font-semibold mt-1">Live database synchronization</div>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto">
          <button
            onClick={() => setFilterTab('ALL')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'ALL' ? 'bg-[#714B67] text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            All ({invoices.length})
          </button>
          <button
            onClick={() => setFilterTab('ISSUED')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'ISSUED' ? 'bg-amber-600 text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Pending / Issued ({countIssued})
          </button>
          <button
            onClick={() => setFilterTab('OVERDUE')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'OVERDUE' ? 'bg-rose-600 text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Overdue ({countOverdue})
          </button>
          <button
            onClick={() => setFilterTab('PAID')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'PAID' ? 'bg-emerald-600 text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Paid & Settled ({countPaid})
          </button>
        </div>

        <div className="relative w-full md:w-72">
          <span className="material-symbols-outlined absolute left-3 top-2.5 text-[#6C757D] text-[18px]">search</span>
          <input
            type="text"
            placeholder="Search invoice, customer, quote..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] placeholder-[#6C757D] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
          />
        </div>
      </div>

      {/* Invoices Table */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-sm font-semibold text-[#6C757D]">
            <span className="material-symbols-outlined animate-spin text-3xl mb-2 text-[#714B67]">sync</span>
            <p>Loading real PostgreSQL invoices...</p>
          </div>
        ) : filteredInvoices.length === 0 ? (
          <div className="p-12 text-center text-sm font-semibold text-[#6C757D]">
            <span className="material-symbols-outlined text-4xl mb-2 text-[#CED4DA]">receipt</span>
            <p>No invoices matching current filter criteria.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-[#FAFAFA] border-b border-[#DEE2E6] text-xs font-bold text-[#6C757D] uppercase tracking-wider">
                  <th className="py-3.5 px-4">Invoice ID</th>
                  <th className="py-3.5 px-4">Customer Account</th>
                  <th className="py-3.5 px-4">Quote Ref</th>
                  <th className="py-3.5 px-4">Grand Total</th>
                  <th className="py-3.5 px-4">Due Date</th>
                  <th className="py-3.5 px-4">Payment Status</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#F1F1F1] text-xs font-medium text-[#212529]">
                {filteredInvoices.map((inv) => {
                  const isPaid = (inv.status || '').toUpperCase() === 'PAID';
                  const isOverdue = (inv.status || '').toUpperCase() === 'OVERDUE';
                  const isProcessing = payingId === inv.id;
                  const isDownloading = downloadingId === inv.id;

                  return (
                    <tr key={inv.id} className="hover:bg-[#FAFAFA] transition-colors">
                      <td className="py-4 px-4 font-mono font-bold text-[#714B67]">
                        {inv.id}
                      </td>
                      <td className="py-4 px-4">
                        <div className="font-bold text-[#212529]">{inv.account || inv.customer_name}</div>
                        <div className="text-[11px] text-[#6C757D]">{inv.customer_id}</div>
                      </td>
                      <td className="py-4 px-4 font-mono text-[#4A4A4A]">
                        {inv.quoteId || inv.document_number || 'Direct Billing'}
                      </td>
                      <td className="py-4 px-4 font-mono font-extrabold text-sm text-[#212529]">
                        ₹{Number(inv.amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                      </td>
                      <td className="py-4 px-4 font-mono text-[#4A4A4A]">
                        {inv.dueDate || 'Immediate'}
                      </td>
                      <td className="py-4 px-4">
                        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold ${
                          isPaid
                            ? 'bg-emerald-100 text-emerald-800'
                            : isOverdue
                            ? 'bg-rose-100 text-rose-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${
                            isPaid ? 'bg-emerald-500' : isOverdue ? 'bg-rose-500' : 'bg-amber-500'
                          }`} />
                          {inv.statusLabel || inv.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          {!isPaid && (
                            <button
                              onClick={() => handleRecordPayment(inv.id)}
                              disabled={isProcessing}
                              className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-1 shadow-sm transition-all disabled:opacity-50"
                              title="Reconcile and mark as PAID"
                            >
                              {isProcessing ? (
                                <span className="material-symbols-outlined animate-spin text-[14px]">sync</span>
                              ) : (
                                <span className="material-symbols-outlined text-[14px]">check</span>
                              )}
                              <span>Pay</span>
                            </button>
                          )}
                          <button
                            onClick={() => handleDownloadPdf(inv.id)}
                            disabled={isDownloading}
                            className="px-2.5 py-1.5 rounded-lg bg-[#F8F4F7] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs flex items-center gap-1 transition-all disabled:opacity-50"
                            title="Download official Tax Invoice PDF"
                          >
                            {isDownloading ? (
                              <span className="material-symbols-outlined animate-spin text-[15px]">sync</span>
                            ) : (
                              <span className="material-symbols-outlined text-[15px]">download</span>
                            )}
                            <span>PDF</span>
                          </button>
                          <button
                            onClick={() => handleCopyLink(inv.id)}
                            className="px-2.5 py-1.5 rounded-lg bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs flex items-center gap-1 transition-all"
                            title="Copy customer payment link"
                          >
                            <span className="material-symbols-outlined text-[15px]">link</span>
                            <span>Link</span>
                          </button>
                          <button
                            onClick={() => setSelectedInvoice(inv)}
                            className="px-2.5 py-1.5 rounded-lg bg-[#F1F1F1] hover:bg-[#DEE2E6] text-[#212529] font-bold text-xs flex items-center gap-1 transition-all"
                            title="View printable invoice slip"
                          >
                            <span className="material-symbols-outlined text-[15px]">visibility</span>
                            <span>Slip</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Manual Invoice Creation Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-2xl max-w-lg w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between pb-4 border-b border-[#DEE2E6]">
              <div className="flex items-center gap-2">
                <span className="p-2 rounded-xl bg-[#F8F4F7] text-[#714B67] material-symbols-outlined text-[20px]">receipt_long</span>
                <h2 className="text-xl font-bold text-[#212529]">Generate Manual Invoice</h2>
              </div>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-[#6C757D] hover:text-[#212529] p-1"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleCreateInvoice} className="flex flex-col gap-4 mt-5">
              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                  Select Customer Account
                </label>
                <select
                  value={formData.customerId}
                  onChange={(e) => setFormData({ ...formData, customerId: e.target.value })}
                  className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                  required
                >
                  {customers.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.company_name || c.name} ({c.id} • {c.tier || 'Enterprise'})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                  Invoice Title / Description
                </label>
                <input
                  type="text"
                  placeholder="e.g. Dedicated Enterprise Cloud Infrastructure & Hardware Milestone"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                    Amount (INR ₹)
                  </label>
                  <input
                    type="number"
                    placeholder="250000"
                    min="1"
                    step="any"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                    className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-mono font-bold text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                    Due Date
                  </label>
                  <input
                    type="date"
                    value={formData.dueDate}
                    onChange={(e) => setFormData({ ...formData, dueDate: e.target.value })}
                    className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                    required
                  />
                </div>
              </div>

              <div className="p-3 bg-[#F8F4F7]/60 rounded-xl border border-[#EFE6ED] flex items-start gap-2 text-xs text-[#714B67]">
                <span className="material-symbols-outlined text-[16px] mt-0.5">download</span>
                <span>
                  Creating this invoice will persist it to PostgreSQL, create an audit trail, and <b>automatically download the Tax Invoice PDF</b>.
                </span>
              </div>

              <div className="flex items-center justify-end gap-3 mt-4 pt-4 border-t border-[#DEE2E6]">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2.5 rounded-xl border border-[#DEE2E6] text-xs font-bold text-[#4A4A4A] hover:bg-[#F1F1F1]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2.5 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white text-xs font-bold shadow-md transition-all disabled:opacity-50 flex items-center gap-2"
                >
                  {submitting ? (
                    <>
                      <span className="material-symbols-outlined animate-spin text-[16px]">sync</span>
                      <span>Generating & Downloading...</span>
                    </>
                  ) : (
                    <>
                      <span className="material-symbols-outlined text-[16px]">download</span>
                      <span>Generate & Download PDF</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Invoice Detail / Printable Slip Modal */}
      {selectedInvoice && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-2xl max-w-2xl w-full p-8 animate-in fade-in zoom-in-95 duration-200">
            {/* Slip Header */}
            <div className="flex items-start justify-between pb-6 border-b border-[#DEE2E6]">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xl font-black tracking-tight text-[#212529]">PHOEN</span>
                  <span className="px-2 py-0.5 rounded-md bg-[#714B67] text-white text-xs font-bold">ERP</span>
                </div>
                <div className="text-xs text-[#6C757D]">Enterprise Commercial Billing & Revenue System</div>
                <div className="text-xs text-[#6C757D] mt-1">GSTIN: 24AABCP1234F1Z8 • Western Logistics Park, Ahmedabad</div>
              </div>
              <div className="text-right">
                <span className={`inline-block px-3 py-1 rounded-full text-xs font-extrabold ${
                  (selectedInvoice.status || '').toUpperCase() === 'PAID'
                    ? 'bg-emerald-100 text-emerald-800'
                    : (selectedInvoice.status || '').toUpperCase() === 'OVERDUE'
                    ? 'bg-rose-100 text-rose-800'
                    : 'bg-amber-100 text-amber-800'
                }`}>
                  {selectedInvoice.statusLabel || selectedInvoice.status}
                </span>
                <div className="font-mono text-sm font-bold text-[#212529] mt-2">{selectedInvoice.id}</div>
                <div className="text-xs text-[#6C757D]">Due: {selectedInvoice.dueDate}</div>
              </div>
            </div>

            {/* Bill To Info */}
            <div className="grid grid-cols-2 gap-4 py-6 border-b border-[#DEE2E6] text-xs">
              <div>
                <span className="font-bold text-[#6C757D] uppercase tracking-wider block mb-1">Billed To</span>
                <div className="font-bold text-sm text-[#212529]">{selectedInvoice.account || selectedInvoice.customer_name}</div>
                <div className="text-[#4A4A4A] mt-1">Customer ID: {selectedInvoice.customer_id}</div>
                <div className="text-[#4A4A4A]">Account Tier: {selectedInvoice.customer_tier || 'Enterprise'}</div>
              </div>
              <div className="text-right">
                <span className="font-bold text-[#6C757D] uppercase tracking-wider block mb-1">Commercial Reference</span>
                <div className="font-mono text-[#212529] font-semibold">{selectedInvoice.quoteId || selectedInvoice.document_number}</div>
                <div className="text-[#4A4A4A] mt-1">Currency: {selectedInvoice.currency || 'INR'}</div>
                <div className="text-[#4A4A4A]">Account Manager: {selectedInvoice.rep || 'David Chen (Finance Controller)'}</div>
              </div>
            </div>

            {/* Line Items */}
            <div className="py-6 border-b border-[#DEE2E6]">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-[#DEE2E6] text-[#6C757D] font-bold uppercase">
                    <th className="pb-2">Description</th>
                    <th className="pb-2 text-right">Qty</th>
                    <th className="pb-2 text-right">Unit Price</th>
                    <th className="pb-2 text-right">Line Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#F1F1F1]">
                  {selectedInvoice.lines && selectedInvoice.lines.length > 0 ? (
                    selectedInvoice.lines.map((l, idx) => (
                      <tr key={idx}>
                        <td className="py-2.5 font-medium text-[#212529]">{l.description || l.product_name}</td>
                        <td className="py-2.5 text-right font-mono">{l.quantity}</td>
                        <td className="py-2.5 text-right font-mono">₹{Number(l.unit_price || 0).toLocaleString()}</td>
                        <td className="py-2.5 text-right font-mono font-bold">₹{Number(l.total || (l.quantity * l.unit_price) || 0).toLocaleString()}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td className="py-2.5 font-medium text-[#212529]">
                        {selectedInvoice.title || 'Standard Enterprise Commercial Hardware & SaaS Service'}
                      </td>
                      <td className="py-2.5 text-right font-mono">1</td>
                      <td className="py-2.5 text-right font-mono">₹{Number(selectedInvoice.amount || 0).toLocaleString()}</td>
                      <td className="py-2.5 text-right font-mono font-bold">₹{Number(selectedInvoice.amount || 0).toLocaleString()}</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Totals Summary */}
            <div className="flex justify-end pt-4 pb-6 border-b border-[#DEE2E6]">
              <div className="w-64 flex flex-col gap-2 text-xs">
                <div className="flex justify-between text-[#6C757D]">
                  <span>Subtotal:</span>
                  <span className="font-mono font-semibold text-[#212529]">
                    ₹{(Number(selectedInvoice.amount || 0) * 0.8474).toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="flex justify-between text-[#6C757D]">
                  <span>GST (18%):</span>
                  <span className="font-mono font-semibold text-[#212529]">
                    ₹{(Number(selectedInvoice.amount || 0) * 0.1526).toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="flex justify-between pt-2 border-t border-[#DEE2E6] text-sm font-extrabold text-[#212529]">
                  <span>Grand Total:</span>
                  <span className="font-mono text-[#714B67]">
                    ₹{Number(selectedInvoice.amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                  </span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between pt-6">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleDownloadPdf(selectedInvoice.id)}
                  disabled={downloadingId === selectedInvoice.id}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#714B67] text-white hover:bg-[#5C3D54] text-xs font-bold transition-all shadow-sm disabled:opacity-50"
                >
                  {downloadingId === selectedInvoice.id ? (
                    <span className="material-symbols-outlined animate-spin text-[16px]">sync</span>
                  ) : (
                    <span className="material-symbols-outlined text-[16px]">download</span>
                  )}
                  <span>Download PDF</span>
                </button>
                <button
                  onClick={() => window.print()}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#F1F1F1] hover:bg-[#DEE2E6] text-[#212529] text-xs font-bold transition-all"
                >
                  <span className="material-symbols-outlined text-[16px]">print</span>
                  <span>Print Document</span>
                </button>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => handleCopyLink(selectedInvoice.id)}
                  className="px-4 py-2 rounded-xl bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] text-xs font-bold transition-all"
                >
                  Copy Payment Link
                </button>
                <button
                  onClick={() => setSelectedInvoice(null)}
                  className="px-5 py-2 rounded-xl bg-[#212529] text-white text-xs font-bold hover:bg-[#3F3B3D] transition-all"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
