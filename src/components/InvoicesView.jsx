import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function InvoicesView({ setActiveTab }) {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await api.getInvoices();
        setInvoices(data);
      } catch (err) {
        console.error('Failed to load invoices:', err);
      }
    }
    loadData();
  }, []);

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#76777d] mb-1">
            <span>Billing & Revenue</span>
            <span>/</span>
            <span className="text-[#2563eb]">Invoices & Payment Ledger</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30]">Invoices & Payment Ledger</h1>
          <p className="text-sm text-[#45464d] mt-1">Track customer billing schedules, payment links, and milestone receivables.</p>
        </div>
        <button
          onClick={() => alert('New Billing Invoice generated!')}
          className="flex items-center gap-2 px-5 h-11 rounded-xl bg-[#2563eb] text-white hover:bg-[#1d4ed8] font-bold text-xs shadow-md transition-all"
        >
          <span className="material-symbols-outlined text-[18px]">receipt_long</span>
          <span>Generate Manual Invoice</span>
        </button>
      </div>

      <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#f8fafc] border-b border-[#e2e8f0] text-xs font-bold text-[#76777d] uppercase">
              <th className="py-3.5 px-4">Invoice ID</th>
              <th className="py-3.5 px-4">Customer Account</th>
              <th className="py-3.5 px-4">Quote Ref</th>
              <th className="py-3.5 px-4">Amount</th>
              <th className="py-3.5 px-4">Due Date</th>
              <th className="py-3.5 px-4">Status</th>
              <th className="py-3.5 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#f1f5f9] text-xs font-medium text-[#0b1c30]">
            {invoices.map((inv) => (
              <tr key={inv.id} className="hover:bg-[#f8fafc] transition-colors">
                <td className="py-4 px-4 font-mono font-bold text-[#2563eb]">{inv.id}</td>
                <td className="py-4 px-4 font-bold">{inv.account}</td>
                <td className="py-4 px-4 font-mono text-[#45464d]">{inv.quoteId}</td>
                <td className="py-4 px-4 font-mono font-extrabold text-sm text-[#0b1c30]">{inv.amount}</td>
                <td className="py-4 px-4 font-mono">{inv.dueDate}</td>
                <td className="py-4 px-4">
                  <span className={`px-2.5 py-1 rounded-full text-[11px] font-bold ${
                    inv.status === 'PAID'
                      ? 'bg-emerald-100 text-emerald-800'
                      : inv.status === 'OVERDUE'
                      ? 'bg-rose-100 text-rose-800'
                      : 'bg-amber-100 text-amber-800'
                  }`}>
                    {inv.statusLabel}
                  </span>
                </td>
                <td className="py-4 px-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <button
                      onClick={() => alert(`Payment link for ${inv.id} copied to clipboard!`)}
                      className="px-3 py-1.5 rounded-lg bg-[#eff4ff] hover:bg-[#e5eeff] text-[#2563eb] font-bold text-xs"
                    >
                      Copy Payment Link
                    </button>
                    <button
                      onClick={() => alert(`Downloading PDF for ${inv.id}...`)}
                      className="px-2.5 py-1.5 rounded-lg bg-[#f1f5f9] hover:bg-[#e2e8f0] text-[#0b1c30]"
                    >
                      <span className="material-symbols-outlined text-[16px]">download</span>
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
