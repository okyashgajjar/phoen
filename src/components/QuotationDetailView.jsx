import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function QuotationDetailView({  }) {
  const navigate = useNavigate();

  const [quotation, setQuotation] = useState(null);
  const [lineItems, setLineItems] = useState([]);
  const [status, setStatus] = useState('DRAFT');

  useEffect(() => {
    async function loadQuote() {
      try {
        const data = await api.getQuotation('Q-1042');
        setQuotation(data);
        setLineItems(data.lines || []);
        setStatus(data.status);
      } catch (err) {
        console.error('Failed to load quotation Q-1042:', err);
      }
    }
    loadQuote();
  }, []);

  const updateQuantity = (id, delta) => {
    setLineItems((items) =>
      items.map((item) => {
        if (item.id === id) {
          const newQty = Math.max(1, item.qty + delta);
          return { ...item, qty: newQty };
        }
        return item;
      })
    );
  };

  const updateDiscount = (id, newDiscount) => {
    const disc = Math.min(100, Math.max(0, Number(newDiscount)));
    setLineItems((items) =>
      items.map((item) => {
        if (item.id === id) {
          const isHwFlagged = item.category === 'Hardware' && disc > 15;
          return {
            ...item,
            discount: disc,
            flagged: isHwFlagged,
            flagReason: isHwFlagged ? 'Exceeds 15% hardware discount threshold' : null,
          };
        }
        return item;
      })
    );
  };

  const addLineItem = () => {
    const newItem = {
      id: Date.now(),
      sku: 'SKU-ADD-NEW',
      name: 'Additional Enterprise Add-on Module',
      category: 'Software / SaaS',
      qty: 1,
      unitPrice: 1500,
      discount: 5,
      flagged: false,
    };
    setLineItems([...lineItems, newItem]);
  };

  const removeItem = (id) => {
    setLineItems(lineItems.filter((i) => i.id !== id));
  };

  // Financial calculations
  const calculateTotals = () => {
    let subtotal = 0;
    let totalDiscountAmount = 0;

    lineItems.forEach((item) => {
      const lineSub = item.qty * item.unitPrice;
      const discAmt = lineSub * (item.discount / 100);
      subtotal += lineSub;
      totalDiscountAmount += discAmt;
    });

    const netTotal = subtotal - totalDiscountAmount;
    const estCost = netTotal * 0.718; // Cost basis
    const grossProfit = netTotal - estCost;
    const blendedMargin = netTotal > 0 ? (grossProfit / netTotal) * 100 : 0;
    const hasFlags = lineItems.some((i) => i.flagged);

    return { subtotal, totalDiscountAmount, netTotal, blendedMargin, hasFlags };
  };

  const { subtotal, totalDiscountAmount, netTotal, blendedMargin, hasFlags } = calculateTotals();

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Top Header & Breadcrumbs */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#76777d] mb-1">
            <button onClick={() => navigate('/quotations')} className="hover:text-[#2563eb]">Quotations</button>
            <span>/</span>
            <span className="text-[#0b1c30] font-mono font-bold">Q-1042</span>
            <span>/</span>
            <span className="text-[#2563eb]">Acme Corp</span>
          </div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-extrabold text-[#0b1c30]">Quote Q-1042 Detail</h1>
            {hasFlags ? (
              <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-800 border border-amber-300 text-xs font-bold flex items-center gap-1">
                <span className="material-symbols-outlined text-[16px]">warning</span> Pending Approval (Flagged)
              </span>
            ) : (
              <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center gap-1">
                <span className="material-symbols-outlined text-[16px]">check_circle</span> Ready to Send
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/approvals')}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs shadow-md transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">verified_user</span>
            <span>Open Approval Cockpit</span>
          </button>
          <button
            onClick={() => navigate('/negotiation')}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#2563eb] hover:bg-[#1d4ed8] text-white font-bold text-xs shadow-md transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">handshake</span>
            <span>View Customer Portal</span>
          </button>
        </div>
      </div>

      {/* Flag Alert Banner */}
      {hasFlags && (
        <div className="rounded-2xl bg-amber-50 border border-amber-200 p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0">
              <span className="material-symbols-outlined text-[24px]">error</span>
            </div>
            <div>
              <h3 className="text-sm font-bold text-amber-900">Margin Guardrail Flag Activated</h3>
              <p className="text-xs text-amber-800 mt-0.5">
                Line item SKU-HW-709 has an 18% hardware discount, exceeding the standard 15% sales rep limit.
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/approvals')}
            className="px-4 py-2 rounded-xl bg-amber-900 text-white font-bold text-xs hover:bg-amber-950 transition-colors shrink-0"
          >
            Review Policy Exceptions
          </button>
        </div>
      )}

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Line Items Table (2 cols) */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-[#0b1c30]">Configured Line Items (CPQ)</h2>
                <p className="text-xs text-[#76777d]">Adjust quantities and discount percentages below</p>
              </div>
              <button
                onClick={addLineItem}
                className="flex items-center gap-1 px-3 py-2 rounded-xl bg-[#eff4ff] hover:bg-[#e5eeff] text-[#2563eb] font-bold text-xs transition-colors"
              >
                <span className="material-symbols-outlined text-[16px]">add</span> Add Line Item
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-[#f8fafc] border-b border-[#e2e8f0] text-xs font-bold text-[#76777d] uppercase tracking-wider">
                    <th className="py-3 px-3">Item Details</th>
                    <th className="py-3 px-3 text-center">Qty</th>
                    <th className="py-3 px-3 text-right">Unit Price</th>
                    <th className="py-3 px-3 text-center">Disc %</th>
                    <th className="py-3 px-3 text-right">Line Total</th>
                    <th className="py-3 px-3 text-center">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#f1f5f9] text-xs font-medium text-[#0b1c30]">
                  {lineItems.map((item) => {
                    const lineSub = item.qty * item.unitPrice;
                    const lineNet = lineSub * (1 - item.discount / 100);
                    return (
                      <tr key={item.id} className={item.flagged ? 'bg-amber-50/40' : ''}>
                        <td className="py-4 px-3">
                          <div className="flex flex-col">
                            <span className="font-mono text-[11px] font-bold text-[#2563eb]">{item.sku}</span>
                            <span className="font-bold text-[#0b1c30] mt-0.5">{item.name}</span>
                            <span className="text-[11px] text-[#76777d]">{item.category}</span>
                            {item.flagged && (
                              <span className="inline-flex items-center gap-1 text-[10px] text-amber-800 font-bold mt-1">
                                <span className="material-symbols-outlined text-[12px]">warning</span> {item.flagReason}
                              </span>
                            )}
                          </div>
                        </td>
                        <td className="py-4 px-3">
                          <div className="flex items-center justify-center gap-1">
                            <button
                              onClick={() => updateQuantity(item.id, -1)}
                              className="w-6 h-6 rounded bg-[#f1f5f9] hover:bg-[#e2e8f0] text-[#0b1c30] font-bold flex items-center justify-center"
                            >
                              -
                            </button>
                            <span className="w-8 text-center font-mono font-bold text-sm">{item.qty}</span>
                            <button
                              onClick={() => updateQuantity(item.id, 1)}
                              className="w-6 h-6 rounded bg-[#f1f5f9] hover:bg-[#e2e8f0] text-[#0b1c30] font-bold flex items-center justify-center"
                            >
                              +
                            </button>
                          </div>
                        </td>
                        <td className="py-4 px-3 text-right font-mono font-bold">${item.unitPrice.toLocaleString()}</td>
                        <td className="py-4 px-3">
                          <div className="flex items-center justify-center">
                            <input
                              type="number"
                              min="0"
                              max="100"
                              value={item.discount}
                              onChange={(e) => updateDiscount(item.id, e.target.value)}
                              className={`w-16 h-8 text-center rounded-lg border font-mono font-bold text-xs focus:outline-none focus:ring-2 ${
                                item.flagged ? 'border-amber-400 bg-amber-100 text-amber-900 focus:ring-amber-400' : 'border-[#e2e8f0] focus:ring-[#2563eb]/20'
                              }`}
                            />
                            <span className="ml-1 text-xs text-[#76777d]">%</span>
                          </div>
                        </td>
                        <td className="py-4 px-3 text-right font-mono font-extrabold text-sm text-[#0b1c30]">
                          ${lineNet.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </td>
                        <td className="py-4 px-3 text-center">
                          <button
                            onClick={() => removeItem(item.id)}
                            className="text-[#76777d] hover:text-rose-600 p-1"
                            title="Remove Line Item"
                          >
                            <span className="material-symbols-outlined text-[18px]">delete</span>
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column: Financial Summary Card (1 col) */}
        <div className="flex flex-col gap-6">
          <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-[#0b1c30] pb-3 border-b border-[#e2e8f0]">Proposal Commercial Summary</h2>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between text-[#45464d]">
                <span>List Gross Subtotal</span>
                <span className="font-mono font-bold text-[#0b1c30]">${subtotal.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-rose-700 font-semibold">
                <span>Total Applied Discount</span>
                <span className="font-mono font-bold">-${totalDiscountAmount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              </div>
              <div className="pt-3 border-t border-[#e2e8f0] flex justify-between items-baseline">
                <span className="text-sm font-bold text-[#0b1c30]">Net Contract Total</span>
                <span className="text-2xl font-extrabold text-[#2563eb] font-mono">
                  ${netTotal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
              </div>
            </div>

            {/* Margin Meter */}
            <div className="mt-4 p-4 rounded-xl bg-[#f8fafc] border border-[#e2e8f0] flex flex-col gap-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-bold text-[#0b1c30]">Blended Margin Analysis</span>
                <span className={`font-mono font-extrabold text-sm ${blendedMargin < 30 ? 'text-amber-700' : 'text-emerald-700'}`}>
                  {blendedMargin.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-[#e2e8f0] h-2.5 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${blendedMargin < 30 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                  style={{ width: `${Math.min(100, Math.max(0, blendedMargin))}%` }}
                ></div>
              </div>
              <span className="text-[11px] text-[#76777d]">Target margin threshold is 35.0%</span>
            </div>

            {/* Action CTAs */}
            <div className="flex flex-col gap-2 mt-4">
              <button
                onClick={() => navigate('/approvals')}
                className="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
              >
                <span className="material-symbols-outlined text-[18px]">verified_user</span>
                <span>Submit to Approval Cockpit</span>
              </button>
              <button
                onClick={() => navigate('/negotiation')}
                className="w-full py-3 rounded-xl bg-[#2563eb] hover:bg-[#1d4ed8] text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
              >
                <span className="material-symbols-outlined text-[18px]">send</span>
                <span>Publish to Customer Portal</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
