import React, { useState } from 'react';

export default function NegotiationPortalView({ setActiveTab }) {
  const [showSignModal, setShowSignModal] = useState(false);
  const [signatureName, setSignatureName] = useState('John Doe');
  const [signatureTitle, setSignatureTitle] = useState('VP Infrastructure');
  const [signedSuccess, setSignedSuccess] = useState(false);
  const [counterNote, setCounterNote] = useState('');
  const [counterSubmitted, setCounterSubmitted] = useState(false);

  const handleSignSubmit = (e) => {
    e.preventDefault();
    setSignedSuccess(true);
    setShowSignModal(false);
  };

  return (
    <div className="w-full max-w-[1280px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Customer Portal Header Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-[#0f172a] to-[#1e293b] text-white p-8 shadow-md flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full bg-[#2563eb] text-white text-xs font-bold uppercase tracking-wider">
              Official Proposal
            </span>
            <span className="font-mono text-xs text-slate-300">REF: Q-1042</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight">Acme Corp Commercial Proposal</h1>
          <p className="text-sm text-slate-300">Prepared by Phoen Enterprise Revenue Operations Team</p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={() => alert('Downloading official PDF proposal document...')}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs border border-white/20 transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">picture_as_pdf</span>
            <span>Download PDF</span>
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
            <h3 className="text-base font-bold text-emerald-900">Contract Successfully Signed & Binding!</h3>
            <p className="text-xs text-emerald-800 mt-1">
              Signed by <strong>{signatureName}</strong> ({signatureTitle}) on {new Date().toLocaleDateString()}. Order dispatched to Fulfillment queue.
            </p>
          </div>
          <button
            onClick={() => setActiveTab('fulfillment')}
            className="ml-auto px-4 py-2 rounded-xl bg-emerald-800 text-white font-bold text-xs hover:bg-emerald-900"
          >
            Track Order Fulfillment
          </button>
        </div>
      )}

      {/* Main Proposal Body Card */}
      <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-8 flex flex-col gap-8">
        {/* Proposal Summary Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 p-6 rounded-xl bg-[#f8fafc] border border-[#e2e8f0]">
          <div>
            <span className="text-xs font-bold text-[#76777d] uppercase">Prepared For</span>
            <span className="block text-sm font-bold text-[#0b1c30] mt-1">Acme Corporation</span>
            <span className="text-xs text-[#76777d]">Attn: John Doe, VP Infrastructure</span>
          </div>
          <div>
            <span className="text-xs font-bold text-[#76777d] uppercase">Proposal Date</span>
            <span className="block text-sm font-bold text-[#0b1c30] mt-1">September 05, 2026</span>
            <span className="text-xs text-[#76777d]">Valid until Oct 05, 2026</span>
          </div>
          <div>
            <span className="text-xs font-bold text-[#76777d] uppercase">Payment Terms</span>
            <span className="block text-sm font-bold text-[#0b1c30] mt-1">Net 30 Days</span>
            <span className="text-xs text-[#76777d]">Annual Upfront Billing</span>
          </div>
          <div>
            <span className="text-xs font-bold text-[#76777d] uppercase">Total Contract Value</span>
            <span className="block text-2xl font-extrabold text-[#2563eb] font-mono mt-1">$28,600.00</span>
            <span className="text-xs text-emerald-700 font-semibold">Includes 18% Special Discount</span>
          </div>
        </div>

        {/* Itemized Line Items Table */}
        <div className="flex flex-col gap-4">
          <h2 className="text-base font-bold text-[#0b1c30]">Itemized Scope of Supply</h2>
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#f8fafc] border-b border-[#e2e8f0] text-xs font-bold text-[#76777d] uppercase">
                <th className="py-3 px-4">Item & Description</th>
                <th className="py-3 px-4 text-center">Qty</th>
                <th className="py-3 px-4 text-right">List Price</th>
                <th className="py-3 px-4 text-right">Net Price</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f1f5f9] text-xs font-medium text-[#0b1c30]">
              <tr>
                <td className="py-4 px-4">
                  <div className="font-bold text-sm">Server Rack Ultra 2U Enterprise Edition</div>
                  <span className="text-[11px] text-[#76777d]">Dual Xeon Scalable, 256GB RAM, 10GbE SFP+ Ports</span>
                </td>
                <td className="py-4 px-4 text-center font-mono font-bold">4</td>
                <td className="py-4 px-4 text-right font-mono text-[#76777d] line-through">$18,000.00</td>
                <td className="py-4 px-4 text-right font-mono font-extrabold text-sm">$14,760.00</td>
              </tr>
              <tr>
                <td className="py-4 px-4">
                  <div className="font-bold text-sm">Cloud Ops Platform Annual Seat License</div>
                  <span className="text-[11px] text-[#76777d]">100 Enterprise User Seats with SSO & Audit Logging</span>
                </td>
                <td className="py-4 px-4 text-center font-mono font-bold">100</td>
                <td className="py-4 px-4 text-right font-mono text-[#76777d] line-through">$12,000.00</td>
                <td className="py-4 px-4 text-right font-mono font-extrabold text-sm">$10,800.00</td>
              </tr>
              <tr>
                <td className="py-4 px-4">
                  <div className="font-bold text-sm">24/7 Dedicated Support SLA & TAM</div>
                  <span className="text-[11px] text-[#76777d]">1 Hour Response Time SLA with Dedicated Engineer</span>
                </td>
                <td className="py-4 px-4 text-center font-mono font-bold">1 Yr</td>
                <td className="py-4 px-4 text-right font-mono text-[#76777d]">$3,040.00</td>
                <td className="py-4 px-4 text-right font-mono font-extrabold text-sm">$3,040.00</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Counter Offer & Discussion Form */}
        <div className="pt-6 border-t border-[#e2e8f0] flex flex-col gap-4">
          <h3 className="text-base font-bold text-[#0b1c30]">Request Term Adjustment / Question</h3>
          {!counterSubmitted ? (
            <div className="flex flex-col gap-3">
              <textarea
                rows="3"
                value={counterNote}
                onChange={(e) => setCounterNote(e.target.value)}
                placeholder="Need a custom SLA modification or payment term adjustment? Send a note directly to Marcus Vance..."
                className="w-full p-4 rounded-xl border border-[#e2e8f0] text-xs text-[#0b1c30] placeholder:text-[#76777d] focus:outline-none focus:ring-2 focus:ring-[#2563eb]/20"
              ></textarea>
              <button
                onClick={() => {
                  if (counterNote.trim()) setCounterSubmitted(true);
                }}
                className="self-start px-5 py-2.5 rounded-xl bg-[#0f172a] hover:bg-[#1e293b] text-white font-bold text-xs transition-colors"
              >
                Submit Comment to Sales Operations
              </button>
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-blue-50 border border-blue-200 text-xs text-blue-900 font-medium">
              Your note has been submitted to Marcus Vance. We will notify you when the proposal is updated.
            </div>
          )}
        </div>
      </div>

      {/* Signature Modal */}
      {showSignModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-2xl max-w-lg w-full p-6 flex flex-col gap-5 animate-in zoom-in-95">
            <div className="flex items-center justify-between pb-3 border-b border-[#e2e8f0]">
              <h3 className="text-lg font-bold text-[#0b1c30]">Digital Signature Execution</h3>
              <button onClick={() => setShowSignModal(false)} className="text-[#76777d] hover:text-[#0b1c30]">
                <span className="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <form onSubmit={handleSignSubmit} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1">
                <label className="text-xs font-bold text-[#0b1c30]">Full Legal Name</label>
                <input
                  type="text"
                  required
                  value={signatureName}
                  onChange={(e) => setSignatureName(e.target.value)}
                  className="p-3 rounded-xl border border-[#e2e8f0] text-sm text-[#0b1c30]"
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-xs font-bold text-[#0b1c30]">Title / Designation</label>
                <input
                  type="text"
                  required
                  value={signatureTitle}
                  onChange={(e) => setSignatureTitle(e.target.value)}
                  className="p-3 rounded-xl border border-[#e2e8f0] text-sm text-[#0b1c30]"
                />
              </div>

              <div className="p-4 rounded-xl bg-[#f8fafc] border border-[#e2e8f0] flex flex-col gap-2">
                <span className="text-xs font-bold text-[#76777d]">Digital Signature Preview</span>
                <div className="h-16 rounded-lg bg-white border border-[#c6c6cd] flex items-center justify-center font-serif text-2xl italic text-[#2563eb]">
                  {signatureName || 'Signature'}
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 mt-2">
                <button
                  type="button"
                  onClick={() => setShowSignModal(false)}
                  className="px-4 py-2.5 rounded-xl bg-[#eff4ff] text-[#0b1c30] font-bold text-xs"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md"
                >
                  Confirm & Execute Agreement ($28,600.00)
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
