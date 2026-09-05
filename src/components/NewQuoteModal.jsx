import React, { useState } from 'react';

export default function NewQuoteModal({ isOpen, onClose, onCreated }) {
  const [accountName, setAccountName] = useState('');
  const [proposalTitle, setProposalTitle] = useState('');
  const [salesRep, setSalesRep] = useState('Sarah Jenkins');
  const [estimatedValue, setEstimatedValue] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onCreated({
      id: `Q-${Math.floor(1050 + Math.random() * 50)}`,
      account: accountName,
      title: proposalTitle,
      rep: salesRep,
      amount: Number(estimatedValue) || 25000,
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-2xl max-w-md w-full p-6 flex flex-col gap-5 animate-in zoom-in-95">
        <div className="flex items-center justify-between pb-3 border-b border-[#e2e8f0]">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-[#eff4ff] text-[#2563eb] flex items-center justify-center">
              <span className="material-symbols-outlined text-[20px]">add_circle</span>
            </div>
            <h3 className="text-lg font-bold text-[#0b1c30]">Create New Proposal</h3>
          </div>
          <button onClick={onClose} className="text-[#76777d] hover:text-[#0b1c30]">
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1">
            <label className="text-xs font-bold text-[#0b1c30]">Customer Account Name</label>
            <input
              type="text"
              required
              placeholder="e.g. Nexus Technology Partners"
              value={accountName}
              onChange={(e) => setAccountName(e.target.value)}
              className="p-3 rounded-xl border border-[#e2e8f0] text-sm text-[#0b1c30] placeholder:text-[#76777d] focus:outline-none focus:ring-2 focus:ring-[#2563eb]/20"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-bold text-[#0b1c30]">Proposal Name / Scope</label>
            <input
              type="text"
              required
              placeholder="e.g. FY26 Infrastructure & Cloud Suite"
              value={proposalTitle}
              onChange={(e) => setProposalTitle(e.target.value)}
              className="p-3 rounded-xl border border-[#e2e8f0] text-sm text-[#0b1c30] placeholder:text-[#76777d] focus:outline-none focus:ring-2 focus:ring-[#2563eb]/20"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-bold text-[#0b1c30]">Assigned Sales Representative</label>
            <select
              value={salesRep}
              onChange={(e) => setSalesRep(e.target.value)}
              className="p-3 rounded-xl border border-[#e2e8f0] text-sm text-[#0b1c30] focus:outline-none focus:ring-2 focus:ring-[#2563eb]/20 bg-white"
            >
              <option value="Sarah Jenkins">Sarah Jenkins (Sales Ops Lead)</option>
              <option value="Marcus Vance">Marcus Vance (Enterprise AE)</option>
              <option value="Rachel Torres">Rachel Torres (Account Executive)</option>
              <option value="David Chen">David Chen (Finance Admin)</option>
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-bold text-[#0b1c30]">Estimated Total Contract Value ($)</label>
            <input
              type="number"
              required
              placeholder="e.g. 45000"
              value={estimatedValue}
              onChange={(e) => setEstimatedValue(e.target.value)}
              className="p-3 rounded-xl border border-[#e2e8f0] text-sm font-mono text-[#0b1c30] placeholder:text-[#76777d] focus:outline-none focus:ring-2 focus:ring-[#2563eb]/20"
            />
          </div>

          <div className="flex items-center justify-end gap-3 mt-3 pt-3 border-t border-[#e2e8f0]">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 rounded-xl bg-[#eff4ff] text-[#0b1c30] font-bold text-xs"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2.5 rounded-xl bg-[#2563eb] hover:bg-[#1d4ed8] text-white font-bold text-xs shadow-md"
            >
              Initialize Quote Draft
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
