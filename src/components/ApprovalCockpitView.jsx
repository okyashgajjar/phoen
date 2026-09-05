import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function ApprovalCockpitView({  }) {
  const navigate = useNavigate();

  const [approvalState, setApprovalState] = useState('PENDING'); // PENDING, APPROVED, REJECTED
  const [comment, setComment] = useState('');
  const [overrideChecked, setOverrideChecked] = useState(false);
  const [chainData, setChainData] = useState(null);

  useEffect(() => {
    async function loadChain() {
      try {
        const data = await api.getApprovalChain('Q-1042');
        setChainData(data);
      } catch (err) {
        console.error('Failed to load approval chain:', err);
      }
    }
    loadChain();
  }, []);

  const handleApprove = async () => {
    try {
      await api.approveQuotation('Q-1042', comment);
      setApprovalState('APPROVED');
    } catch (err) {
      console.error('Failed to approve:', err);
    }
  };

  const handleReject = async () => {
    try {
      await api.rejectQuotation('Q-1042', comment);
      setApprovalState('REJECTED');
    } catch (err) {
      console.error('Failed to reject:', err);
    }
  };

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#76777d] mb-1">
            <button onClick={() => navigate('/quotations')} className="hover:text-[#2563eb]">Quotations</button>
            <span>/</span>
            <button onClick={() => navigate('/quote-detail')} className="hover:text-[#2563eb]">Q-1042</button>
            <span>/</span>
            <span className="text-amber-800 font-bold">Approval Cockpit</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30]">Approval Cockpit - Proposal Q-1042</h1>
          <p className="text-sm text-[#45464d] mt-1">Multi-tier governance & policy exception review for Acme Corp ($28,600 net total).</p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/quote-detail')}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#eff4ff] hover:bg-[#e5eeff] text-[#2563eb] font-bold text-xs transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">edit</span>
            <span>Back to CPQ Editor</span>
          </button>
        </div>
      </div>

      {/* Approval Status Alert Banner */}
      {approvalState === 'APPROVED' && (
        <div className="rounded-2xl bg-emerald-50 border border-emerald-300 p-6 flex items-center gap-4 animate-in fade-in">
          <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined text-[28px]">verified</span>
          </div>
          <div>
            <h3 className="text-base font-bold text-emerald-900">Proposal Q-1042 Successfully Approved!</h3>
            <p className="text-xs text-emerald-800 mt-1">
              Executive override recorded by David Chen. Quotation is now marked as Approved and ready to publish to the Customer Portal.
            </p>
          </div>
          <button
            onClick={() => navigate('/negotiation')}
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
            <h3 className="text-base font-bold text-rose-900">Proposal Q-1042 Rejected</h3>
            <p className="text-xs text-rose-800 mt-1">
              Discount exception rejected. The quote has been returned to Sales Rep Marcus Vance for restructuring.
            </p>
          </div>
          <button
            onClick={() => navigate('/quote-detail')}
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
          <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-[#0b1c30]">Triggered Policy Exception Guardrails</h2>
            <div className="space-y-3">
              <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-start justify-between gap-4">
                <div className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-amber-700 text-[22px] mt-0.5">warning</span>
                  <div>
                    <span className="text-xs font-bold text-amber-900 font-mono block">RULE-104: Hardware Discount Limit</span>
                    <p className="text-xs text-amber-800 mt-0.5">
                      Item <strong>SKU-HW-709</strong> applied discount is <strong>18.0%</strong>. Maximum tier allowance for sales reps is <strong>15.0%</strong>.
                    </p>
                  </div>
                </div>
                <span className="px-2.5 py-1 rounded bg-amber-200 text-amber-900 text-[11px] font-bold shrink-0">
                  +3.0% Exception
                </span>
              </div>

              <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-start justify-between gap-4">
                <div className="flex items-start gap-3">
                  <span className="material-symbols-outlined text-amber-700 text-[22px] mt-0.5">trending_down</span>
                  <div>
                    <span className="text-xs font-bold text-amber-900 font-mono block">RULE-208: Blended Margin Floor</span>
                    <p className="text-xs text-amber-800 mt-0.5">
                      Proposal blended margin is <strong>28.2%</strong>. Standard enterprise target threshold is <strong>35.0%</strong>.
                    </p>
                  </div>
                </div>
                <span className="px-2.5 py-1 rounded bg-amber-200 text-amber-900 text-[11px] font-bold shrink-0">
                  -6.8% Below Floor
                </span>
              </div>
            </div>
          </div>

          {/* Multi-Tier Approval Matrix */}
          <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-[#0b1c30]">Multi-Tier Governance Approval Hierarchy</h2>
            <div className="space-y-4">
              {/* Tier 1 */}
              <div className="p-4 rounded-xl border border-emerald-200 bg-emerald-50/50 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-xs">
                    SJ
                  </div>
                  <div>
                    <span className="text-sm font-bold text-[#0b1c30]">Sarah Jenkins</span>
                    <span className="text-xs text-[#76777d] block">Sales Operations Lead (Tier 1)</span>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center gap-1">
                  <span className="material-symbols-outlined text-[16px]">check_circle</span> Approved (Auto-verified)
                </span>
              </div>

              {/* Tier 2 */}
              <div className={`p-4 rounded-xl border ${
                approvalState === 'APPROVED' ? 'border-emerald-200 bg-emerald-50/50' : 'border-amber-300 bg-amber-50/50'
              } flex items-center justify-between`}>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-[#0f172a] text-white flex items-center justify-center font-bold text-xs">
                    DC
                  </div>
                  <div>
                    <span className="text-sm font-bold text-[#0b1c30]">David Chen</span>
                    <span className="text-xs text-[#76777d] block">Finance Administrator (Tier 2 - Required)</span>
                  </div>
                </div>
                {approvalState === 'APPROVED' ? (
                  <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center gap-1">
                    <span className="material-symbols-outlined text-[16px]">check_circle</span> Approved
                  </span>
                ) : approvalState === 'REJECTED' ? (
                  <span className="px-3 py-1 rounded-full bg-rose-100 text-rose-800 text-xs font-bold flex items-center gap-1">
                    <span className="material-symbols-outlined text-[16px]">cancel</span> Rejected
                  </span>
                ) : (
                  <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold flex items-center gap-1 animate-pulse">
                    <span className="material-symbols-outlined text-[16px]">hourglass_bottom</span> Action Pending
                  </span>
                )}
              </div>

              {/* Tier 3 */}
              <div className="p-4 rounded-xl border border-[#e2e8f0] bg-[#f8fafc] flex items-center justify-between opacity-70">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-[#76777d] text-white flex items-center justify-center font-bold text-xs">
                    ER
                  </div>
                  <div>
                    <span className="text-sm font-bold text-[#0b1c30]">Elena Rostova</span>
                    <span className="text-xs text-[#76777d] block">VP Commercial Sales (Tier 3 - Escalation)</span>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-full bg-[#e2e8f0] text-[#76777d] text-xs font-bold">
                  Queued
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Right 1 Col: Decision Panel */}
        <div className="flex flex-col gap-6">
          <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-[#0b1c30]">Executive Review Decision</h2>

            <div className="flex flex-col gap-3">
              <label className="text-xs font-bold text-[#0b1c30]">Review Comments & Governance Rationale</label>
              <textarea
                rows="4"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Enter rationale for discount exception approval or rejection feedback..."
                className="w-full p-3 rounded-xl border border-[#e2e8f0] text-xs text-[#0b1c30] placeholder:text-[#76777d] focus:outline-none focus:ring-2 focus:ring-[#2563eb]/20"
              ></textarea>

              <label className="flex items-start gap-2 cursor-pointer mt-2">
                <input
                  type="checkbox"
                  checked={overrideChecked}
                  onChange={(e) => setOverrideChecked(e.target.checked)}
                  className="mt-0.5 rounded border-[#e2e8f0] text-[#2563eb] focus:ring-[#2563eb]"
                />
                <span className="text-xs text-[#45464d]">
                  I certify that this 18% hardware discount override is authorized under Q4 Strategic Growth budget.
                </span>
              </label>

              <div className="flex flex-col gap-2 mt-4">
                <button
                  disabled={approvalState === 'APPROVED'}
                  onClick={handleApprove}
                  className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
                >
                  <span className="material-symbols-outlined text-[18px]">check_circle</span>
                  <span>Approve & Authorize Proposal</span>
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
