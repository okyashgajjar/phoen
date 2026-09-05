import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function NewQuoteModal({ isOpen, onClose, onCreated }) {
  const [accountName, setAccountName] = useState('');
  const [proposalTitle, setProposalTitle] = useState('');
  const [salesRep, setSalesRep] = useState('');
  const [estimatedValue, setEstimatedValue] = useState('');
  
  const [users, setUsers] = useState([]);

  useEffect(() => {
    if (isOpen) {
      api.getAllUsers()
        .then(data => {
          setUsers(data);
          const reps = data.filter(u => u.role === 'sales_rep');
          if (reps.length > 0) setSalesRep(reps[0].name);
          const customers = data.filter(u => u.role === 'customer');
          if (customers.length > 0) setAccountName(customers[0].name);
        })
        .catch(err => console.error("Failed to load users for modal", err));
    }
  }, [isOpen]);

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

  const customerUsers = users.filter(u => u.role === 'customer');
  const salesRepUsers = users.filter(u => ['sales_rep', 'manager'].includes(u.role));

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
            <select
              required
              value={accountName}
              onChange={(e) => setAccountName(e.target.value)}
              className="p-3 rounded-xl border border-[#e2e8f0] text-sm text-[#0b1c30] focus:outline-none focus:ring-2 focus:ring-[#2563eb]/20 bg-white"
            >
              {customerUsers.length === 0 && <option value="">No customers available</option>}
              {customerUsers.map(c => (
                <option key={c.id} value={c.name}>{c.name}</option>
              ))}
            </select>
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
              {salesRepUsers.length === 0 && <option value="">No sales reps available</option>}
              {salesRepUsers.map(s => (
                <option key={s.id} value={s.name}>{s.name} ({s.role.replace('_', ' ')})</option>
              ))}
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
