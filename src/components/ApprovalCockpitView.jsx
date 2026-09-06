import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../api';

export default function ApprovalCockpitView({ currentUser }) {
  const navigate = useNavigate();
  const { id: paramId } = useParams();
  const [selectedQuoteId, setSelectedQuoteId] = useState(paramId || null);

  const [approvalState, setApprovalState] = useState('PENDING'); // PENDING, APPROVED, REJECTED
  const [comment, setComment] = useState('');
  const [overrideChecked, setOverrideChecked] = useState(false);
  const [chainData, setChainData] = useState(null);
  const [quotation, setQuotation] = useState(null);
  const [pendingQuotes, setPendingQuotes] = useState([]);

  const role = currentUser?.role || 'manager';
  const quoteId = paramId || selectedQuoteId || (pendingQuotes[0]?.id) || 'QT-0001';

  useEffect(() => {
    async function loadCockpit() {
      try {
        const pendings = await api.getPendingApprovals().catch(() => []);
        setPendingQuotes(pendings);

        const targetId = paramId || selectedQuoteId || (pendings.length > 0 ? pendings[0].id : 'QT-0001');
        if (!selectedQuoteId && pendings.length > 0 && !paramId) {
          setSelectedQuoteId(pendings[0].id);
        }

        const [chain, quote] = await Promise.all([
          api.getApprovalChain(targetId).catch(() => null),
          api.getQuotation(targetId).catch(() => null),
        ]);
        setChainData(chain);
        setQuotation(quote);

        if (quote) {
          if (quote.status === 'READY' || quote.status === 'APPROVED' || quote.status === 'WON') {
            setApprovalState('APPROVED');
          } else if (quote.status === 'REJECTED') {
            setApprovalState('REJECTED');
          } else {
            setApprovalState('PENDING');
          }
        }
      } catch (err) {
        console.error('Failed to load approval chain:', err);
      }
    }
    loadCockpit();
  }, [paramId, selectedQuoteId]);

  const handleApprove = async () => {
    try {
      await api.approveQuotation(quoteId, comment);
      setApprovalState('APPROVED');
    } catch (err) {
      console.error('Failed to approve:', err);
      alert(err.message || 'Failed to approve');
    }
  };

  const handleReject = async () => {
    try {
      await api.rejectQuotation(quoteId, comment);
      setApprovalState('REJECTED');
    } catch (err) {
      console.error('Failed to reject:', err);
      alert(err.message || 'Failed to reject');
    }
  };

  const getRoleHeader = () => {
    if (role === 'finance') {
      return {
        badge: 'Tier 2 Financial Sign-Off',
        badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-300',
        title: `Tier 2 Financial Clearance - Proposal ${quotation?.id || quoteId}`,
        subtitle: `Fiscal margin governance & payment term authorization for ${quotation?.account || 'Customer'}.`,
        certLabel: 'I certify that this quote satisfies corporate gross margin floor (minimum 25%) and customer credit clearance.'
      };
    } else if (role === 'admin') {
      return {
        badge: 'Administrative Clearance',
        badgeColor: 'bg-purple-100 text-purple-800 border-purple-300',
        title: `Governance & Policy Cockpit - Proposal ${quotation?.id || quoteId}`,
        subtitle: `System-wide approval routing audit and policy exception clearance for ${quotation?.account || 'Customer'}.`,
        certLabel: 'I certify executive policy override and compliance logging for this commercial proposal.'
      };
    } else {
      return {
        badge: 'Tier 1 Sales Operations',
        badgeColor: 'bg-amber-100 text-amber-800 border-amber-300',
        title: `Tier 1 Sales Manager Sign-Off - Proposal ${quotation?.id || quoteId}`,
        subtitle: `Evaluate discount exceptions and margin guardrails for ${quotation?.account || 'Customer'}.`,
        certLabel: 'I certify that this discount override is authorized under regional sales quota allowances.'
      };
    }
  };

  const roleInfo = getRoleHeader();

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#6C757D] mb-1">
            <button onClick={() => navigate('/quotations')} className="hover:text-[#714B67]">Quotations</button>
            <span>/</span>
            <button onClick={() => navigate(`/quote-detail/${quoteId}`)} className="hover:text-[#714B67]">{quotation?.id || quoteId}</button>
            <span>/</span>
            <span className="text-amber-800 font-bold">{roleInfo.badge}</span>
          </div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-extrabold text-[#212529]">{roleInfo.title}</h1>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${roleInfo.badgeColor}`}>
              {roleInfo.badge}
            </span>
          </div>
          <p className="text-sm text-[#4A4A4A] mt-1">
            {roleInfo.subtitle} (${quotation?.amount ? quotation.amount.toLocaleString() : '28,600'} net total).
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate(`/quote-detail/${quoteId}`)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">edit</span>
            <span>View Quote Details</span>
          </button>
        </div>
      </div>

      {/* Pending Quotes Switcher if multiple pending exist */}
      {pendingQuotes.length > 1 && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-white border border-[#DEE2E6] overflow-x-auto text-xs">
          <span className="font-bold text-[#6C757D] shrink-0">Pending Approvals Queue:</span>
          {pendingQuotes.map((pq) => (
            <button
              key={pq.id}
              onClick={() => navigate(`/approvals/${pq.id}`)}
              className={`px-3 py-1 rounded-lg font-mono font-bold transition-all shrink-0 ${
                pq.id === quoteId
                  ? 'bg-[#714B67] text-white shadow-xs'
                  : 'bg-[#F6F1F5] text-[#212529] hover:bg-[#EFE6ED]'
              }`}
            >
              {pq.id} ({pq.account})
            </button>
          ))}
        </div>
      )}

      {/* Approval Status Alert Banner */}
      {approvalState === 'APPROVED' && (
        <div className="rounded-2xl bg-emerald-50 border border-emerald-300 p-6 flex items-center gap-4 animate-in fade-in">
          <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined text-[28px]">verified</span>
          </div>
          <div>
            <h3 className="text-base font-bold text-emerald-900">Proposal {quotation?.id || quoteId} Successfully Approved!</h3>
            <p className="text-xs text-emerald-800 mt-1">
              Executive approval recorded. Quotation is now marked as Approved and ready to publish to the Customer Portal.
            </p>
          </div>
          <button
            onClick={() => navigate(`/negotiation/${quoteId}`)}
            className="ml-auto px-4 py-2.5 rounded-xl bg-emerald-800 text-white font-bold text-xs hover:bg-emerald-900 transition-colors"
          >
            Publish to Customer Portal
          </button>
        </div>
      )}

      {approvalState === 'REJECTED' && (
        <div className="rounded-2xl bg-rose-50 border border-rose-300 p-6 flex items-center gap-4 animate-in fade-in">
          <div className="w-12 h-12 rounded-xl bg-rose-600 text-white flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined text-[28px]">block</span>
          </div>
          <div>
            <h3 className="text-base font-bold text-rose-900">Proposal {quotation?.id || quoteId} Rejected</h3>
            <p className="text-xs text-rose-800 mt-1">
              Discount exception rejected. The quote has been returned to Sales Rep {quotation?.rep || 'Sales Rep'} for restructuring.
            </p>
          </div>
          <button
            onClick={() => navigate(`/quote-detail/${quoteId}`)}
            className="ml-auto px-4 py-2.5 rounded-xl bg-rose-800 text-white font-bold text-xs hover:bg-rose-900 transition-colors"
          >
            Modify Line Items
          </button>
        </div>
      )}

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Risk Analysis & Multi-tier Matrix */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          {/* Policy Exceptions Card */}
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-[#212529]">Triggered Policy Exception Guardrails</h2>
            <div className="space-y-3">
              {(chainData?.exceptions && chainData.exceptions.length > 0) ? (
                chainData.exceptions.map((ex, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3">
                      <span className="material-symbols-outlined text-amber-700 text-[22px] mt-0.5">warning</span>
                      <div>
                        <span className="text-xs font-bold text-amber-900 font-mono block">{ex.rule}</span>
                        <p className="text-xs text-amber-800 mt-0.5">{ex.description}</p>
                      </div>
                    </div>
                    {ex.overage && (
                      <span className="px-2.5 py-1 rounded bg-amber-200 text-amber-900 text-[11px] font-bold shrink-0">
                        {ex.overage}
                      </span>
                    )}
                  </div>
                ))
              ) : (
                <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold flex items-center gap-2">
                  <span className="material-symbols-outlined text-[20px]">check_circle</span>
                  <span>No policy guardrails violated. Proposal meets all standard margin and discount criteria.</span>
                </div>
              )}
            </div>
          </div>

          {/* Commercial Line Items Table */}
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-[#212529]">Commercial Proposal Line Items</h2>
                <p className="text-xs text-[#6C757D] mt-0.5">
                  Account: <span className="font-bold text-[#212529]">{quotation?.account || quotation?.customer_name || 'Customer'}</span> • Sales Rep: <span className="font-bold text-[#212529]">{quotation?.rep || 'Kavita Sharma'}</span>
                </p>
              </div>
              <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-[#F6F1F5] text-[#714B67]">
                {quotation?.lines?.length || 0} Configured Items
              </span>
            </div>

            <div className="overflow-x-auto border border-[#DEE2E6] rounded-xl">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#FAFAFA] text-[#4A4A4A] font-bold border-b border-[#DEE2E6]">
                  <tr>
                    <th className="p-3">#</th>
                    <th className="p-3">Item Description</th>
                    <th className="p-3 text-right">Qty</th>
                    <th className="p-3 text-right">Unit Price</th>
                    <th className="p-3 text-right">Discount</th>
                    <th className="p-3 text-right">Line Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#DEE2E6]">
                  {quotation?.lines && quotation.lines.length > 0 ? (
                    quotation.lines.map((line, idx) => {
                      const disc = line.discount || line.discount_percent || 0;
                      const isOver = disc > 15;
                      return (
                        <tr key={line.id || idx} className="hover:bg-[#FAFAFA]/80 transition-colors">
                          <td className="p-3 font-mono text-[#6C757D]">{line.line_number || idx + 1}</td>
                          <td className="p-3">
                            <div className="font-bold text-[#212529]">{line.name || line.description}</div>
                            <div className="text-[11px] font-mono text-[#6C757D]">{line.sku || line.category}</div>
                          </td>
                          <td className="p-3 text-right font-mono font-semibold text-[#212529]">{line.qty || line.quantity || 1}</td>
                          <td className="p-3 text-right font-mono text-[#4A4A4A]">₹{(line.unit_price || line.unitPrice || 0).toLocaleString()}</td>
                          <td className="p-3 text-right">
                            <span className={`inline-flex items-center gap-1 font-mono font-bold px-2 py-0.5 rounded ${
                              isOver ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-[#212529]'
                            }`}>
                              {disc}%
                              {isOver && (
                                <span className="material-symbols-outlined text-[14px]">warning</span>
                              )}
                            </span>
                          </td>
                          <td className="p-3 text-right font-mono font-bold text-[#212529]">₹{(line.line_total || 0).toLocaleString()}</td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan="6" className="p-6 text-center text-[#6C757D]">No line items found for this proposal.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Financial Summary */}
            <div className="bg-[#FAFAFA] p-4 rounded-xl border border-[#DEE2E6] flex flex-wrap items-center justify-between gap-4 text-xs">
              <div>
                <span className="text-[#6C757D]">Subtotal: </span>
                <span className="font-mono font-bold text-[#212529]">₹{(quotation?.subtotal || quotation?.amount || 0).toLocaleString()}</span>
              </div>
              <div>
                <span className="text-[#6C757D]">Total Discount: </span>
                <span className="font-mono font-bold text-rose-600">₹{(quotation?.discount_total || 0).toLocaleString()}</span>
              </div>
              <div>
                <span className="text-[#6C757D]">Taxes: </span>
                <span className="font-mono font-bold text-[#212529]">₹{(quotation?.tax_total || 0).toLocaleString()}</span>
              </div>
              <div className="text-sm">
                <span className="text-[#6C757D]">Net Total: </span>
                <span className="font-mono font-extrabold text-[#714B67]">₹{(quotation?.amount || quotation?.grand_total || 0).toLocaleString()}</span>
              </div>
            </div>
          </div>

          {/* Dynamic Multi-Tier Approval Matrix */}
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-[#212529]">Multi-Tier Governance Approval Hierarchy</h2>
            <div className="space-y-4">
              {chainData?.chain && chainData.chain.length > 0 ? (
                chainData.chain.map((step) => {
                  const isApproved = step.status === 'APPROVED' || (step.tier === 1 && approvalState === 'APPROVED');
                  const isRejected = step.status === 'REJECTED' || (step.tier === 1 && approvalState === 'REJECTED');
                  const isPending = step.status === 'PENDING' && approvalState === 'PENDING';

                  return (
                    <div
                      key={step.tier}
                      className={`p-4 rounded-xl border flex items-center justify-between transition-all ${
                        isApproved
                          ? 'border-emerald-200 bg-emerald-50/50'
                          : isRejected
                          ? 'border-rose-200 bg-rose-50/50'
                          : isPending
                          ? 'border-amber-300 bg-amber-50/50 ring-1 ring-amber-200'
                          : 'border-[#DEE2E6] bg-[#FAFAFA] opacity-70'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-xs text-white ${
                            isApproved
                              ? 'bg-emerald-600'
                              : isRejected
                              ? 'bg-rose-600'
                              : isPending
                              ? 'bg-[#212529]'
                              : 'bg-[#6C757D]'
                          }`}
                        >
                          {step.initials}
                        </div>
                        <div>
                          <span className="text-sm font-bold text-[#212529]">{step.name}</span>
                          <span className="text-xs text-[#6C757D] block">{step.role}</span>
                        </div>
                      </div>

                      <div>
                        {isApproved ? (
                          <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center gap-1">
                            <span className="material-symbols-outlined text-[16px]">check_circle</span>
                            {step.statusLabel || 'Approved'}
                          </span>
                        ) : isRejected ? (
                          <span className="px-3 py-1 rounded-full bg-rose-100 text-rose-800 text-xs font-bold flex items-center gap-1">
                            <span className="material-symbols-outlined text-[16px]">cancel</span>
                            {step.statusLabel || 'Rejected'}
                          </span>
                        ) : isPending ? (
                          <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold flex items-center gap-1 animate-pulse">
                            <span className="material-symbols-outlined text-[16px]">hourglass_bottom</span>
                            {step.statusLabel || 'Action Pending'}
                          </span>
                        ) : (
                          <span className="px-3 py-1 rounded-full bg-[#DEE2E6] text-[#6C757D] text-xs font-bold">
                            {step.statusLabel || 'Queued'}
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })
              ) : (
                <div className="p-4 rounded-xl border border-amber-200 bg-amber-50 text-amber-800 text-xs">
                  Loading approval hierarchy...
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right 1 Col: Decision Panel */}
        <div className="flex flex-col gap-6">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-[#212529]">Executive Review Decision</h2>

            <div className="flex flex-col gap-3">
              <label className="text-xs font-bold text-[#212529]">Review Comments & Governance Rationale</label>
              <textarea
                rows="4"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Enter rationale for discount exception approval or rejection feedback..."
                className="w-full p-3 rounded-xl border border-[#DEE2E6] text-xs text-[#212529] placeholder:text-[#6C757D] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20"
              ></textarea>

              <label className="flex items-start gap-2 cursor-pointer mt-2">
                <input
                  type="checkbox"
                  checked={overrideChecked}
                  onChange={(e) => setOverrideChecked(e.target.checked)}
                  className="mt-0.5 rounded border-[#DEE2E6] text-[#714B67] focus:ring-[#714B67]"
                />
                <span className="text-xs text-[#4A4A4A]">
                  {roleInfo.certLabel}
                </span>
              </label>

              <div className="flex flex-col gap-2 mt-4">
                <button
                  disabled={approvalState === 'APPROVED'}
                  onClick={handleApprove}
                  className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                >
                  <span className="material-symbols-outlined text-[18px]">check_circle</span>
                  <span>{role === 'finance' ? 'Approve & Release Financial Hold' : role === 'admin' ? 'Approve & Override Policy Gate' : 'Approve & Authorize Proposal'}</span>
                </button>
                <button
                  disabled={approvalState === 'REJECTED'}
                  onClick={handleReject}
                  className="w-full py-3 rounded-xl bg-rose-600 hover:bg-rose-700 disabled:opacity-50 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                >
                  <span className="material-symbols-outlined text-[18px]">cancel</span>
                  <span>Reject & Request Re-quote</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
