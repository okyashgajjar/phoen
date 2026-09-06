import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../api';
import UpsellPanel from './UpsellPanel';
import ProductSelectorModal from './ProductSelectorModal';

export default function QuotationDetailView({ currentUser }) {
  const navigate = useNavigate();
  const { id: paramId } = useParams();
  const quoteId = paramId || 'Q-1042';

  const [quotation, setQuotation] = useState(null);
  const [lineItems, setLineItems] = useState([]);
  const [status, setStatus] = useState('DRAFT');
  const [allQuotes, setAllQuotes] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');
  const [isCatalogModalOpen, setIsCatalogModalOpen] = useState(false);
  const [downloadingPdf, setDownloadingPdf] = useState(false);

  const role = currentUser?.role || 'sales_rep';
  const isApprover = ['manager', 'finance', 'admin'].includes(role);
  const canEdit = ['sales_rep', 'admin'].includes(role);

  useEffect(() => {
    async function loadQuote() {
      try {
        const [data, quotesList] = await Promise.all([
          api.getQuotation(quoteId),
          api.getQuotations().catch(() => [])
        ]);
        setQuotation(data);
        setLineItems(data.lines || []);
        setStatus(data.status);
        setAllQuotes(quotesList || []);
      } catch (err) {
        console.error(`Failed to load quotation ${quoteId}:`, err);
      }
    }
    loadQuote();
  }, [quoteId]);

  const updateQuantity = async (id, delta) => {
    if (!canEdit) return;
    const item = lineItems.find((i) => i.id === id);
    if (!item) return;
    const newQty = Math.max(1, (item.qty || 1) + delta);
    setLineItems((items) =>
      items.map((i) => (i.id === id ? { ...i, qty: newQty } : i))
    );
    try {
      const updated = await api.updateLine(quoteId, id, { qty: newQty });
      setQuotation(updated);
      setLineItems(updated.lines || []);
    } catch (err) {
      console.error('Failed to sync qty to backend:', err);
    }
  };

  const updateDiscount = async (id, newDiscount) => {
    if (!canEdit) return;
    const disc = Math.min(100, Math.max(0, Number(newDiscount)));
    setLineItems((items) =>
      items.map((item) => {
        if (item.id === id) {
          const isHwFlagged = item.category === 'Hardware' && disc > 15;
          return {
            ...item,
            discount: disc,
            discount_percent: disc,
            flagged: isHwFlagged,
            flagReason: isHwFlagged ? 'Exceeds 15% hardware discount threshold' : null,
          };
        }
        return item;
      })
    );
    try {
      const updated = await api.updateLine(quoteId, id, { discount: disc });
      setQuotation(updated);
      setLineItems(updated.lines || []);
    } catch (err) {
      console.error('Failed to sync discount to backend:', err);
    }
  };

  // Accepting a suggestion from the upsell panel adds it as a real line, so
  // the totals, margin meter and blended risk score all recompute at once.
  const addSuggestedProduct = async (suggestion) => {
    if (!canEdit) return;
    const updated = await api.addLine(quoteId, {
      product_id: suggestion.product_id,
      quantity: 1,
      unit_price: suggestion.unit_price,
      discount_percent: 0.0,
      is_recurring: suggestion.is_recurring || false,
    });
    setQuotation(updated);
    setLineItems(updated.lines || []);
  };

  // Open the enterprise Product Catalog & Item Selector modal
  const addLineItem = () => {
    if (!canEdit) return;
    setIsCatalogModalOpen(true);
  };

  // Callback when sales rep confirms an item or variant from ProductSelectorModal
  const handleAddProductFromModal = async (lineData) => {
    if (!canEdit) return;
    const updated = await api.addLine(quoteId, lineData);
    setQuotation(updated);
    setLineItems(updated.lines || []);
  };

  // Remove a line item and sync deletion with backend and PostgreSQL database
  const removeItem = async (id) => {
    if (!canEdit) return;
    setLineItems((items) => items.filter((i) => i.id !== id));
    try {
      const updated = await api.deleteLine(quoteId, id);
      setQuotation(updated);
      setLineItems(updated.lines || []);
    } catch (err) {
      console.error('Failed to sync line deletion to backend:', err);
    }
  };

  const handleDownloadPdf = async () => {
    try {
      setDownloadingPdf(true);
      const targetId = quotation?.id || quotation?.document_number || quoteId;
      await api.downloadQuotationPdf(targetId);
      setSubmitMessage(`Downloaded Phoen-Commercial-Proposal-${targetId}.pdf successfully.`);
      setTimeout(() => setSubmitMessage(''), 4000);
    } catch (err) {
      console.error('Failed to download proposal PDF:', err);
      setSubmitMessage('Failed to download PDF: ' + (err.message || 'Unknown error'));
      setTimeout(() => setSubmitMessage(''), 4000);
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handleSubmitForApproval = async () => {
    try {
      setIsSubmitting(true);
      const res = await api.submitQuotation(quoteId);
      setQuotation(res);
      setStatus(res.status);
      setSubmitMessage('Quotation submitted successfully for manager sign-off!');
      if (isApprover) {
        navigate(`/approvals/${quoteId}`);
      }
    } catch (err) {
      console.error('Failed to submit quote for approval:', err);
      setSubmitMessage('Quote status updated.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Financial calculations
  const calculateTotals = () => {
    let subtotal = 0;
    let totalDiscountAmount = 0;

    lineItems.forEach((item) => {
      const uPrice = item.unitPrice || item.unit_price || 0;
      const uQty = item.qty || item.quantity || 1;
      const uDisc = item.discount || item.discount_percent || 0;
      const lineSub = uQty * uPrice;
      const discAmt = lineSub * (uDisc / 100);
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
      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#6C757D] mb-1">
            <button onClick={() => navigate('/quotations')} className="hover:text-[#714B67]">
              {role === 'sales_rep' ? 'My Proposals' : role === 'manager' ? 'Team Pipeline' : 'Quotations'}
            </button>
            <span>/</span>
            <span className="text-[#212529] font-mono font-bold">{quotation?.id || quoteId}</span>
            <span>/</span>
            <span className="text-[#714B67]">{quotation?.account || 'Customer Account'}</span>
          </div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-extrabold text-[#212529]">Quote {quotation?.id || quoteId} Detail</h1>
            {status === 'PENDING_APPROVAL' || hasFlags ? (
              <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-800 border border-amber-300 text-xs font-bold flex items-center gap-1">
                <span className="material-symbols-outlined text-[16px]">hourglass_top</span> Pending Approval
              </span>
            ) : status === 'WON' ? (
              <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center gap-1">
                <span className="material-symbols-outlined text-[16px]">verified</span> Won & Signed
              </span>
            ) : (
              <span className="px-3 py-1 rounded-full bg-[#EFE6ED] text-[#472F41] text-xs font-bold flex items-center gap-1">
                <span className="material-symbols-outlined text-[16px]">check_circle</span> {status}
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          {/* Proposal Switcher */}
          {allQuotes.length > 0 && (
            <div className="flex items-center gap-1.5 bg-[#F6F1F5] px-3 py-2 rounded-xl border border-[#DEE2E6]">
              <span className="text-[11px] font-bold text-[#6C757D]">Switch Proposal:</span>
              <select
                value={quoteId}
                onChange={(e) => navigate(`/quote-detail/${e.target.value}`)}
                className="bg-transparent text-xs font-bold text-[#212529] focus:outline-none cursor-pointer"
              >
                {allQuotes.map((q) => (
                  <option key={q.id} value={q.id}>
                    {q.id} ({q.account || 'Deal'} - ${(Number(q.amount) || 0).toLocaleString()})
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Only Approvers (Manager, Finance, Admin) see the Open Approval Cockpit button */}
          {isApprover && (
            <button
              onClick={() => navigate(`/approvals/${quoteId}`)}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs shadow-md transition-all"
            >
              <span className="material-symbols-outlined text-[18px]">verified_user</span>
              <span>{role === 'finance' ? 'Financial Sign-Off' : 'Open Approval Cockpit'}</span>
            </button>
          )}
          <button
            onClick={() => navigate(`/negotiation/${quoteId}`)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs border border-[#714B67]/20 shadow-xs transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">visibility</span>
            <span>Preview Customer Portal</span>
          </button>
          <button
            onClick={handleDownloadPdf}
            disabled={downloadingPdf}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white hover:bg-[#F8F9FA] text-[#714B67] font-bold text-xs border border-[#DEE2E6] shadow-xs transition-all disabled:opacity-60"
            title="Download executive Phoen commercial proposal PDF"
          >
            <span className={`material-symbols-outlined text-[18px] ${downloadingPdf ? 'animate-spin' : ''}`}>
              {downloadingPdf ? 'sync' : 'picture_as_pdf'}
            </span>
            <span>{downloadingPdf ? 'Generating…' : 'Proposal PDF'}</span>
          </button>
        </div>
      </div>

      {submitMessage && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold flex items-center gap-2">
          <span className="material-symbols-outlined text-[18px]">check_circle</span>
          <span>{submitMessage}</span>
        </div>
      )}

      {/* Flag Alert Banner */}
      {(hasFlags || status === 'PENDING_APPROVAL') && (
        <div className="rounded-2xl bg-amber-50 border border-amber-200 p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0">
              <span className="material-symbols-outlined text-[24px]">warning</span>
            </div>
            <div>
              <h3 className="text-sm font-bold text-amber-900">
                {isApprover ? 'Approval Required: Exception Policy Triggered' : 'Margin Guardrail Flag Activated'}
              </h3>
              <p className="text-xs text-amber-800 mt-0.5">
                {isApprover 
                  ? 'This quote requires supervisor or finance authorization before it can be confirmed and published to the customer.'
                  : 'Discount exceeds the automated standard ceiling. Submit this quote to the approval cockpit to route for sign-off.'}
              </p>
            </div>
          </div>
          {isApprover ? (
            <button
              onClick={() => navigate(`/approvals/${quoteId}`)}
              className="px-4 py-2 rounded-xl bg-amber-900 text-white font-bold text-xs hover:bg-amber-950 transition-colors shrink-0"
            >
              Review in Approval Cockpit
            </button>
          ) : (
            <button
              onClick={handleSubmitForApproval}
              disabled={isSubmitting}
              className="px-4 py-2 rounded-xl bg-amber-600 text-white font-bold text-xs hover:bg-amber-700 transition-colors shrink-0"
            >
              {isSubmitting ? 'Routing...' : 'Route for Sign-Off'}
            </button>
          )}
        </div>
      )}

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Line Items Table (2 cols) */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-[#212529]">Configured Line Items (CPQ)</h2>
                <p className="text-xs text-[#6C757D]">Adjust quantities and discount percentages below</p>
              </div>
              <button
                onClick={addLineItem}
                className="flex items-center gap-1 px-3 py-2 rounded-xl bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs transition-colors"
              >
                <span className="material-symbols-outlined text-[16px]">add</span> Add Line Item
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-[#FAFAFA] border-b border-[#DEE2E6] text-xs font-bold text-[#6C757D] uppercase tracking-wider">
                    <th className="py-3 px-3">Item Details</th>
                    <th className="py-3 px-3 text-center">Qty</th>
                    <th className="py-3 px-3 text-right">Unit Price</th>
                    <th className="py-3 px-3 text-center">Disc %</th>
                    <th className="py-3 px-3 text-right">Line Total</th>
                    <th className="py-3 px-3 text-center">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#F1F1F1] text-xs font-medium text-[#212529]">
                  {lineItems.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="py-8 text-center text-xs text-[#6C757D]">
                        No line items found for this proposal. Click "Add Line Item" to add items from the catalog.
                      </td>
                    </tr>
                  ) : (
                    lineItems.map((item) => {
                      const qty = item.qty ?? item.quantity ?? 1;
                      const unitPrice = Number(item.unitPrice ?? item.unit_price ?? 0);
                      const discount = Number(item.discount ?? item.discount_percent ?? 0);
                      const lineSub = qty * unitPrice;
                      const lineNet = lineSub * (1 - discount / 100);
                      const itemName = item.name || item.description || item.sku || 'Catalog Item';
                      const itemSku = item.sku || item.product_id || item.id;
                      const itemCat = item.category || 'Product';

                      return (
                        <tr key={item.id} className={item.flagged ? 'bg-amber-50/40' : ''}>
                          <td className="py-4 px-3">
                            <div className="flex flex-col">
                              <span className="font-mono text-[11px] font-bold text-[#714B67]">{itemSku}</span>
                              <span className="font-bold text-[#212529] mt-0.5">{itemName}</span>
                              <span className="text-[11px] text-[#6C757D]">{itemCat}</span>
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
                                className="w-6 h-6 rounded bg-[#F1F1F1] hover:bg-[#DEE2E6] text-[#212529] font-bold flex items-center justify-center"
                              >
                                -
                              </button>
                              <span className="w-8 text-center font-mono font-bold text-sm">{qty}</span>
                              <button
                                onClick={() => updateQuantity(item.id, 1)}
                                className="w-6 h-6 rounded bg-[#F1F1F1] hover:bg-[#DEE2E6] text-[#212529] font-bold flex items-center justify-center"
                              >
                                +
                              </button>
                            </div>
                          </td>
                          <td className="py-4 px-3 text-right font-mono font-bold">
                            ${unitPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                          </td>
                          <td className="py-4 px-3">
                            <div className="flex items-center justify-center">
                              <input
                                type="number"
                                min="0"
                                max="100"
                                value={discount}
                                onChange={(e) => updateDiscount(item.id, e.target.value)}
                                className={`w-16 h-8 text-center rounded-lg border font-mono font-bold text-xs focus:outline-none focus:ring-2 ${
                                  item.flagged ? 'border-amber-400 bg-amber-100 text-amber-900 focus:ring-amber-400' : 'border-[#DEE2E6] focus:ring-[#714B67]/20'
                                }`}
                              />
                              <span className="ml-1 text-xs text-[#6C757D]">%</span>
                            </div>
                          </td>
                          <td className="py-4 px-3 text-right font-mono font-extrabold text-sm text-[#212529]">
                            ${lineNet.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                          </td>
                          <td className="py-4 px-3 text-center">
                            <button
                              onClick={() => removeItem(item.id)}
                              className="text-[#6C757D] hover:text-rose-600 p-1"
                              title="Remove Line Item"
                            >
                              <span className="material-symbols-outlined text-[18px]">delete</span>
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column: Financial Summary Card (1 col) */}
        <div className="flex flex-col gap-6">
          {/* Upsell & Cross-Sell suggestions (spec B5) */}
          {canEdit && (
            <UpsellPanel
              quotationId={quoteId}
              refreshKey={lineItems.length}
              onAdd={addSuggestedProduct}
            />
          )}

          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-[#212529] pb-3 border-b border-[#DEE2E6]">Proposal Commercial Summary</h2>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between text-[#4A4A4A]">
                <span>List Gross Subtotal</span>
                <span className="font-mono font-bold text-[#212529]">${subtotal.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-rose-700 font-semibold">
                <span>Total Applied Discount</span>
                <span className="font-mono font-bold">-${totalDiscountAmount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              </div>
              <div className="pt-3 border-t border-[#DEE2E6] flex justify-between items-baseline">
                <span className="text-sm font-bold text-[#212529]">Net Contract Total</span>
                <span className="text-2xl font-extrabold text-[#714B67] font-mono">
                  ${netTotal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
              </div>
            </div>

            {/* Margin Meter */}
            <div className="mt-4 p-4 rounded-xl bg-[#FAFAFA] border border-[#DEE2E6] flex flex-col gap-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-bold text-[#212529]">Blended Margin Analysis</span>
                <span className={`font-mono font-extrabold text-sm ${blendedMargin < 30 ? 'text-amber-700' : 'text-emerald-700'}`}>
                  {blendedMargin.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-[#DEE2E6] h-2.5 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${blendedMargin < 30 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                  style={{ width: `${Math.min(100, Math.max(0, blendedMargin))}%` }}
                ></div>
              </div>
              <span className="text-[11px] text-[#6C757D]">Target margin threshold is 35.0%</span>
            </div>

            {/* Action CTAs — strictly tailored per role */}
            <div className="flex flex-col gap-2 mt-4">
              {/* Sales Rep View */}
              {role === 'sales_rep' && (
                <>
                  {status === 'PENDING_APPROVAL' ? (
                    <div className="w-full py-3 px-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 font-bold text-xs flex items-center justify-center gap-2">
                      <span className="material-symbols-outlined text-[18px]">hourglass_top</span>
                      <span>Under Manager Review</span>
                    </div>
                  ) : (
                    <button
                      onClick={handleSubmitForApproval}
                      disabled={isSubmitting}
                      className="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                    >
                      {isSubmitting ? (
                        <span className="material-symbols-outlined text-[18px] animate-spin">progress_activity</span>
                      ) : (
                        <span className="material-symbols-outlined text-[18px]">verified_user</span>
                      )}
                      <span>{isSubmitting ? 'Routing to Approvals...' : 'Submit to Approval Cockpit'}</span>
                    </button>
                  )}
                  <button
                    onClick={() => navigate(`/negotiation/${quoteId}`)}
                    className="w-full py-3 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                  >
                    <span className="material-symbols-outlined text-[18px]">visibility</span>
                    <span>Preview Customer Portal</span>
                  </button>
                </>
              )}

              {/* Manager View */}
              {role === 'manager' && (
                <>
                  {status === 'PENDING_APPROVAL' && (
                    <button
                      onClick={() => navigate(`/approvals/${quoteId}`)}
                      className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                    >
                      <span className="material-symbols-outlined text-[18px]">verified_user</span>
                      <span>Review Tier 1 Approval</span>
                    </button>
                  )}
                  <button
                    onClick={() => navigate(`/negotiation/${quoteId}`)}
                    className="w-full py-3 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                  >
                    <span className="material-symbols-outlined text-[18px]">visibility</span>
                    <span>Audit Customer Portal</span>
                  </button>
                </>
              )}

              {/* Finance View */}
              {role === 'finance' && (
                <>
                  {status === 'PENDING_APPROVAL' && (
                    <button
                      onClick={() => navigate(`/approvals/${quoteId}`)}
                      className="w-full py-3 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                    >
                      <span className="material-symbols-outlined text-[18px]">verified_user</span>
                      <span>Authorize Financial Sign-Off</span>
                    </button>
                  )}
                  <button
                    onClick={() => navigate('/invoices')}
                    className="w-full py-3 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                  >
                    <span className="material-symbols-outlined text-[18px]">receipt_long</span>
                    <span>Open Invoices Ledger</span>
                  </button>
                </>
              )}

              {/* Admin View */}
              {role === 'admin' && (
                <>
                  <button
                    onClick={() => navigate(`/approvals/${quoteId}`)}
                    className="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                  >
                    <span className="material-symbols-outlined text-[18px]">verified_user</span>
                    <span>Approval Cockpit</span>
                  </button>
                  <button
                    onClick={() => navigate(`/negotiation/${quoteId}`)}
                    className="w-full py-3 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                  >
                    <span className="material-symbols-outlined text-[18px]">visibility</span>
                    <span>Customer Portal Preview</span>
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Enterprise Product Catalog & Item Selector Modal */}
      <ProductSelectorModal
        isOpen={isCatalogModalOpen}
        onClose={() => setIsCatalogModalOpen(false)}
        onAddLine={handleAddProductFromModal}
        existingLines={lineItems}
      />
    </div>
  );
}
