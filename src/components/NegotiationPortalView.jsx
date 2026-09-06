import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../api';

export default function NegotiationPortalView({ currentUser }) {
  const navigate = useNavigate();
  const { id: paramId } = useParams();
  const [selectedQuoteId, setSelectedQuoteId] = useState(paramId || 'Q-1040');

  const [quotation, setQuotation] = useState(null);
  const [userQuotes, setUserQuotes] = useState([]);
  const [showSignModal, setShowSignModal] = useState(false);
  const [signatureName, setSignatureName] = useState('John Doe');
  const [signatureTitle, setSignatureTitle] = useState('VP Infrastructure');
  const [signedSuccess, setSignedSuccess] = useState(false);
  const [counterNote, setCounterNote] = useState('');
  const [counterSubmitted, setCounterSubmitted] = useState(false);
  const [isSigning, setIsSigning] = useState(false);
  const [isSubmittingCounter, setIsSubmittingCounter] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);
  const [toastMsg, setToastMsg] = useState('');
  const [downloadingPdf, setDownloadingPdf] = useState(false);

  const role = currentUser?.role || 'sales_rep';
  const isInternal = ['sales_rep', 'manager', 'admin', 'finance'].includes(role);

  useEffect(() => {
    if (paramId) {
      setSelectedQuoteId(paramId);
    }
  }, [paramId]);

  useEffect(() => {
    async function loadData() {
      try {
        const [quoteRes, allQuotes] = await Promise.all([
          api.getPortalQuote(selectedQuoteId).catch(() => api.getQuotation(selectedQuoteId)),
          api.getQuotations().catch(() => [])
        ]);
        setQuotation(quoteRes);
        setUserQuotes(allQuotes || []);
        if (quoteRes?.status === 'WON') {
          setSignedSuccess(true);
        } else {
          setSignedSuccess(false);
        }
      } catch (err) {
        console.error('Failed to load portal quote:', err);
      }
    }
    loadData();
  }, [selectedQuoteId]);

  const handleQuoteSelect = (newId) => {
    setSelectedQuoteId(newId);
    navigate(`/negotiation/${newId}`);
  };

  const handleCopyLink = () => {
    navigator.clipboard?.writeText(window.location.href);
    setCopiedLink(true);
    setToastMsg('Customer Portal Link copied to clipboard!');
    setTimeout(() => {
      setCopiedLink(false);
      setToastMsg('');
    }, 3000);
  };

  const handleDownloadPdf = async () => {
    try {
      setDownloadingPdf(true);
      const targetId = quotation?.id || quotation?.document_number || selectedQuoteId;
      await api.downloadQuotationPdf(targetId);
      setToastMsg(`Downloaded Phoen-Commercial-Proposal-${targetId}.pdf successfully.`);
      setTimeout(() => setToastMsg(''), 4000);
    } catch (err) {
      console.error('Failed to download proposal PDF:', err);
      setToastMsg('Failed to generate PDF: ' + (err.message || 'Unknown error'));
      setTimeout(() => setToastMsg(''), 4000);
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handleSignSubmit = async (e) => {
    e.preventDefault();
    try {
      setIsSigning(true);
      const res = await api.confirmQuote(selectedQuoteId);
      setSignedSuccess(true);
      setShowSignModal(false);
      if (res.quotation) {
        setQuotation(res.quotation);
      }
      setToastMsg('Agreement confirmed and executed successfully!');
      setTimeout(() => setToastMsg(''), 4000);
    } catch (err) {
      console.error('Failed to confirm quote:', err);
      alert(err.message || 'Failed to execute agreement');
    } finally {
      setIsSigning(false);
    }
  };

  const handleCounterSubmit = async () => {
    if (!counterNote.trim()) return;
    try {
      setIsSubmittingCounter(true);
      await api.submitCounterProposal(selectedQuoteId, counterNote);
      setCounterSubmitted(true);
      setToastMsg('Counter proposal note submitted to commercial operations!');
      setTimeout(() => setToastMsg(''), 4000);
    } catch (err) {
      console.error('Failed to submit counter proposal:', err);
      alert(err.message || 'Failed to submit comment');
    } finally {
      setIsSubmittingCounter(false);
    }
  };

  const formattedAmount = quotation?.amount
    ? Number(quotation.amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '62,000.00';

  return (
    <div className="w-full max-w-[1280px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Toast Notification */}
      {toastMsg && (
        <div className="fixed top-24 right-8 z-50 bg-[#212529] text-white px-5 py-3 rounded-xl shadow-2xl border border-slate-700 flex items-center gap-3 animate-in slide-in-from-top-4">
          <span className="material-symbols-outlined text-emerald-400 text-[20px]">check_circle</span>
          <span className="text-xs font-bold">{toastMsg}</span>
        </div>
      )}

      {/* Internal Sales Representative Preview Control Bar */}
      {isInternal && (
        <div className="bg-white p-4 rounded-2xl border border-[#DEE2E6] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#F8F4F7] text-[#714B67] flex items-center justify-center shrink-0">
              <span className="material-symbols-outlined text-[22px]">visibility</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-[#212529]">Customer Portal Preview Mode</span>
                <span className="px-2 py-0.5 rounded-full bg-[#EFE6ED] text-[#472F41] text-[10px] font-bold">
                  {role.replace('_', ' ').toUpperCase()} VIEW
                </span>
              </div>
              <p className="text-[11px] text-[#4A4A4A]">
                This is the live customer-facing agreement portal your clients interact with to review terms, submit counter-offers, and sign.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 flex-wrap shrink-0">
            {/* Proposal Switcher */}
            {userQuotes.length > 0 && (
              <div className="flex items-center gap-1.5 bg-[#F6F1F5] px-3 py-1.5 rounded-xl border border-[#DEE2E6]">
                <span className="text-[11px] font-bold text-[#6C757D]">Proposal:</span>
                <select
                  value={selectedQuoteId}
                  onChange={(e) => handleQuoteSelect(e.target.value)}
                  className="bg-transparent text-xs font-bold text-[#212529] focus:outline-none cursor-pointer"
                >
                  {userQuotes.map((q) => (
                    <option key={q.id} value={q.id}>
                      {q.id} ({q.account || 'Deal'} - ${(Number(q.amount) || 0).toLocaleString()})
                    </option>
                  ))}
                </select>
              </div>
            )}

            <button
              onClick={handleCopyLink}
              className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white hover:bg-[#FAFAFA] text-[#212529] font-bold text-xs border border-[#DEE2E6] shadow-xs transition-colors"
            >
              <span className="material-symbols-outlined text-[16px] text-[#714B67]">
                {copiedLink ? 'done' : 'link'}
              </span>
              <span>{copiedLink ? 'Copied!' : 'Copy Portal Link'}</span>
            </button>

            <button
              onClick={() => navigate(`/quote-detail/${selectedQuoteId}`)}
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-bold text-xs shadow-sm transition-all"
            >
              <span className="material-symbols-outlined text-[16px]">edit_document</span>
              <span>Edit in Quotation Builder</span>
            </button>
          </div>
        </div>
      )}

      {/* Customer Portal Header Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-[#212529] via-[#3F3B3D] to-[#212529] text-white p-8 shadow-md flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full bg-[#714B67] text-white text-xs font-bold uppercase tracking-wider">
              Official Commercial Agreement
            </span>
            <span className="font-mono text-xs text-slate-300">REF: {quotation?.id || selectedQuoteId}</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight">
            {quotation?.account ? `${quotation.account} Enterprise Proposal` : 'Enterprise Commercial Proposal'}
          </h1>
          <p className="text-sm text-slate-300">
            Prepared by Phoen Enterprise Revenue Operations Team &bull; Account Rep: {quotation?.rep || quotation?.created_by || 'Kavita Sharma'}
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={handleDownloadPdf}
            disabled={downloadingPdf}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs border border-white/20 transition-all disabled:opacity-60 shadow-sm"
          >
            <span className={`material-symbols-outlined text-[18px] ${downloadingPdf ? 'animate-spin' : ''}`}>
              {downloadingPdf ? 'sync' : 'picture_as_pdf'}
            </span>
            <span>{downloadingPdf ? 'Generating PDF…' : 'Download PDF'}</span>
          </button>
          {!signedSuccess ? (
            <button
              onClick={() => setShowSignModal(true)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs shadow-lg transition-all active:scale-[0.98]"
            >
              <span className="material-symbols-outlined text-[18px]">draw</span>
              <span>Accept & Sign Digitally</span>
            </button>
          ) : (
            <span className="px-4 py-2 rounded-xl bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-md">
              <span className="material-symbols-outlined text-[18px]">verified</span> Contract Executed
            </span>
          )}
        </div>
      </div>

      {signedSuccess && (
        <div className="rounded-2xl bg-emerald-50 border border-emerald-300 p-6 flex items-center gap-4 animate-in fade-in">
          <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined text-[28px]">task_alt</span>
          </div>
          <div>
            <h3 className="text-base font-bold text-emerald-900">Contract Successfully Signed & Legally Binding!</h3>
            <p className="text-xs text-emerald-800 mt-1">
              Executed by <strong>{signatureName}</strong> ({signatureTitle}) on {new Date().toLocaleDateString()}. Dispatched to Fulfillment and Billing queue.
            </p>
          </div>
          <button
            onClick={() => navigate('/quotations')}
            className="ml-auto px-4 py-2 rounded-xl bg-emerald-800 text-white font-bold text-xs hover:bg-emerald-900"
          >
            Return to Pipeline
          </button>
        </div>
      )}

      {/* Customer Counter-Offer & Negotiation Highlight Banner */}
      <div className="p-5 rounded-2xl bg-amber-50/90 border border-amber-300 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0 mt-0.5">
            <span className="material-symbols-outlined text-[22px]">forum</span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-amber-950 uppercase tracking-wider">Active Customer Counter-Offer</span>
              <span className="px-2 py-0.5 rounded-full bg-amber-200 text-amber-900 text-[10px] font-extrabold">IN NEGOTIATION</span>
            </div>
            <p className="text-xs text-amber-900 mt-1 font-medium leading-relaxed">
              {selectedQuoteId === 'Q-1040' 
                ? 'Global Logistics has requested a 2-year term lock with a 12% price guarantee on 8x Phoenix Core licenses ($62,000 total). Awaiting sales operations review.'
                : `Customer requested term review on proposal ${selectedQuoteId}. Ready for counter-discussion or formal line adjustments.`}
            </p>
          </div>
        </div>
        <button
          onClick={() => navigate(`/quote-detail/${selectedQuoteId}`)}
          className="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-xs transition-colors shrink-0 flex items-center gap-1.5"
        >
          <span>Adjust Terms in CPQ</span>
          <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
        </button>
      </div>

      {/* Main Proposal Body Card */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-8 flex flex-col gap-8">
        {/* Proposal Summary Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 p-6 rounded-xl bg-[#FAFAFA] border border-[#DEE2E6]">
          <div>
            <span className="text-xs font-bold text-[#6C757D] uppercase">Prepared For</span>
            <span className="block text-sm font-bold text-[#212529] mt-1">{quotation?.account || 'Customer Account'}</span>
            <span className="text-xs text-[#6C757D]">Attn: {signatureName}, {signatureTitle}</span>
          </div>
          <div>
            <span className="text-xs font-bold text-[#6C757D] uppercase">Proposal Scope</span>
            <span className="block text-sm font-bold text-[#212529] mt-1">{quotation?.title || 'Enterprise CPQ Contract'}</span>
            <span className="text-xs text-[#6C757D]">Valid for 30 days &bull; Net 30 Terms</span>
          </div>
          <div>
            <span className="text-xs font-bold text-[#6C757D] uppercase">Billing Schedule</span>
            <span className="block text-sm font-bold text-[#212529] mt-1">Annual Upfront</span>
            <span className="text-xs text-[#6C757D]">Automated Electronic Invoicing</span>
          </div>
          <div>
            <span className="text-xs font-bold text-[#6C757D] uppercase">Total Contract Value</span>
            <span className="block text-2xl font-extrabold text-[#714B67] font-mono mt-1">
              ${formattedAmount}
            </span>
            <span className="text-xs text-emerald-700 font-semibold">
              Status: {quotation?.statusLabel || quotation?.status || 'Active Negotiation'}
            </span>
          </div>
        </div>

        {/* Itemized Line Items Table */}
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-[#212529]">Itemized Scope of Supply</h2>
            <span className="text-xs text-[#6C757D]">All prices quoted in USD</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-[#FAFAFA] border-b border-[#DEE2E6] text-xs font-bold text-[#6C757D] uppercase">
                  <th className="py-3 px-4">Item & Description</th>
                  <th className="py-3 px-4 text-center">Qty</th>
                  <th className="py-3 px-4 text-right">List Price</th>
                  <th className="py-3 px-4 text-right">Net Price</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#F1F1F1] text-xs font-medium text-[#212529]">
                {quotation?.lines && quotation.lines.length > 0 ? (
                  quotation.lines.map((line, idx) => {
                    const qty = line.qty || line.quantity || 1;
                    const price = line.unitPrice || line.unit_price || 0;
                    const disc = line.discount || line.discount_percent || 0;
                    const net = qty * price * (1 - disc / 100);
                    return (
                      <tr key={line.id || idx}>
                        <td className="py-4 px-4">
                          <div className="font-bold text-sm">{line.name || line.sku}</div>
                          <span className="text-[11px] text-[#6C757D]">
                            {line.category || 'Product'} &bull; SKU: {line.sku || line.product_id}
                          </span>
                        </td>
                        <td className="py-4 px-4 text-center font-mono font-bold">{qty}</td>
                        <td className="py-4 px-4 text-right font-mono text-[#6C757D] line-through">
                          ${(qty * price).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </td>
                        <td className="py-4 px-4 text-right font-mono font-extrabold text-sm text-[#212529]">
                          ${net.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan="4" className="py-6 px-4 text-center text-xs text-[#6C757D]">
                      Loading itemized line items...
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Counter Offer & Discussion Thread */}
        <div className="pt-6 border-t border-[#DEE2E6] flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-[#212529]">Buyer & Seller Negotiation Thread</h3>
              <p className="text-xs text-[#6C757D]">Transparent audit trail of term modifications, requested discounts, and counter-proposals</p>
            </div>
            <span className="text-xs text-emerald-700 font-bold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              Live Channel
            </span>
          </div>

          {/* Conversation history items */}
          <div className="flex flex-col gap-3 p-4 rounded-xl bg-[#FAFAFA] border border-[#DEE2E6]">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-[#212529] text-white flex items-center justify-center font-bold text-xs shrink-0">
                {(quotation?.account || 'Client')
                  .split(' ')
                  .map((w) => w[0])
                  .slice(0, 2)
                  .join('')
                  .toUpperCase()}
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-[#212529]">
                    {quotation?.account ? `${quotation.account} Procurement` : 'Client Procurement'}
                  </span>
                  <span className="text-[10px] text-[#6C757D]">2 hours ago</span>
                </div>
                <p className="text-xs text-[#4A4A4A] mt-1 bg-white p-3 rounded-xl border border-[#DEE2E6]">
                  {(() => {
                    const lineWithMsg = quotation?.lines?.find(l => l.negotiation_data && l.negotiation_data.customer_message);
                    if (lineWithMsg && lineWithMsg.negotiation_data.customer_message) {
                      return `"${lineWithMsg.negotiation_data.customer_message}"`;
                    }
                    if (quotation?.notes) {
                      return `"${quotation.notes}"`;
                    }
                    return `"We have reviewed the commercial terms for ${quotation?.id || selectedQuoteId}. Requesting final account management approval for proposed pricing."`;
                  })()}
                </p>
              </div>
            </div>

            {counterSubmitted && (
              <div className="flex items-start gap-3 pl-6">
                <div className="w-8 h-8 rounded-full bg-[#714B67] text-white flex items-center justify-center font-bold text-xs shrink-0">
                  {(quotation?.rep || quotation?.created_by || 'KS')
                    .split(' ')
                    .map((w) => w[0])
                    .slice(0, 2)
                    .join('')
                    .toUpperCase()}
                </div>
                <div className="flex flex-col">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-[#212529]">
                      {quotation?.rep || quotation?.created_by || 'Kavita Sharma'} (Sales Operations)
                    </span>
                    <span className="text-[10px] text-[#6C757D]">Just now</span>
                  </div>
                  <p className="text-xs text-[#4A4A4A] mt-1 bg-[#F8F4F7]/70 p-3 rounded-xl border border-[#E0CEDB]">
                    "{counterNote}"
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Counter Offer Form */}
          {!counterSubmitted ? (
            <div className="flex flex-col gap-3">
              <label className="text-xs font-bold text-[#212529]">Submit Note or Counter-Offer to Negotiation Thread</label>
              <textarea
                rows="3"
                value={counterNote}
                onChange={(e) => setCounterNote(e.target.value)}
                placeholder="State your term adjustment, custom discount condition, or question..."
                className="w-full p-4 rounded-xl border border-[#DEE2E6] text-xs text-[#212529] placeholder:text-[#6C757D] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20"
              ></textarea>
              <button
                onClick={handleCounterSubmit}
                disabled={isSubmittingCounter || !counterNote.trim()}
                className="self-start px-5 py-2.5 rounded-xl bg-[#212529] hover:bg-[#3F3B3D] disabled:opacity-50 text-white font-bold text-xs transition-colors flex items-center gap-2 shadow-xs"
              >
                {isSubmittingCounter && <span className="material-symbols-outlined text-[16px] animate-spin">progress_activity</span>}
                <span>Post Note to Negotiation Thread</span>
              </button>
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-[#F8F4F7] border border-[#E0CEDB] text-xs text-[#33212E] font-medium flex items-center gap-2">
              <span className="material-symbols-outlined text-[18px]">info</span>
              <span>Your counter-note has been logged to the agreement thread.</span>
            </div>
          )}
        </div>
      </div>

      {/* Signature Modal */}
      {showSignModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-2xl max-w-lg w-full p-6 flex flex-col gap-5 animate-in zoom-in-95">
            <div className="flex items-center justify-between pb-3 border-b border-[#DEE2E6]">
              <h3 className="text-lg font-bold text-[#212529]">Digital Signature Execution</h3>
              <button onClick={() => setShowSignModal(false)} className="text-[#6C757D] hover:text-[#212529]">
                <span className="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <form onSubmit={handleSignSubmit} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1">
                <label className="text-xs font-bold text-[#212529]">Full Legal Name</label>
                <input
                  type="text"
                  required
                  value={signatureName}
                  onChange={(e) => setSignatureName(e.target.value)}
                  className="p-3 rounded-xl border border-[#DEE2E6] text-sm text-[#212529]"
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-xs font-bold text-[#212529]">Title / Designation</label>
                <input
                  type="text"
                  required
                  value={signatureTitle}
                  onChange={(e) => setSignatureTitle(e.target.value)}
                  className="p-3 rounded-xl border border-[#DEE2E6] text-sm text-[#212529]"
                />
              </div>

              <div className="p-4 rounded-xl bg-[#FAFAFA] border border-[#DEE2E6] flex flex-col gap-2">
                <span className="text-xs font-bold text-[#6C757D]">Digital Signature Preview</span>
                <div className="h-16 rounded-lg bg-white border border-[#CED4DA] flex items-center justify-center font-serif text-2xl italic text-[#714B67]">
                  {signatureName || 'Signature'}
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 mt-2">
                <button
                  type="button"
                  onClick={() => setShowSignModal(false)}
                  disabled={isSigning}
                  className="px-4 py-2.5 rounded-xl bg-[#F6F1F5] text-[#212529] font-bold text-xs"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSigning}
                  className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md flex items-center gap-2"
                >
                  {isSigning && <span className="material-symbols-outlined text-[16px] animate-spin">progress_activity</span>}
                  <span>Confirm & Execute Agreement (${formattedAmount})</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
