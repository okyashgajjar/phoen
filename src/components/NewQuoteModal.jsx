import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function NewQuoteModal({ isOpen, onClose, onCreated }) {
  const [customerId, setCustomerId] = useState('');
  const [proposalTitle, setProposalTitle] = useState('');
  const [salesRep, setSalesRep] = useState('');
  const [estimatedValue, setEstimatedValue] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [submitError, setSubmitError] = useState('');
  
  const [customersList, setCustomersList] = useState([]);
  const [repsList, setRepsList] = useState([]);

  useEffect(() => {
    if (isOpen) {
      setSubmitError('');
      setIsLoadingData(true);
      Promise.allSettled([
        api.getCustomers(),
        api.getAllUsers(),
      ]).then(([custResult, userResult]) => {
        let loadedCustomers = [];
        let loadedReps = [];

        if (custResult.status === 'fulfilled' && Array.isArray(custResult.value)) {
          loadedCustomers = custResult.value;
        }

        if (userResult.status === 'fulfilled' && Array.isArray(userResult.value)) {
          // Extract sales reps and managers from database users
          loadedReps = userResult.value.filter(u => ['sales_rep', 'manager', 'admin'].includes(u.role));
          // If customer endpoint was empty, pick customers from users list
          const userCusts = userResult.value.filter(u => u.role === 'customer');
          if (loadedCustomers.length === 0 && userCusts.length > 0) {
            loadedCustomers = userCusts;
          }
        }

        setCustomersList(loadedCustomers);
        setRepsList(loadedReps);

        if (loadedCustomers.length > 0) {
          const firstCust = loadedCustomers[0];
          setCustomerId(firstCust.id);
        }

        if (loadedReps.length > 0) {
          setSalesRep(loadedReps[0].id);
        }
      }).catch((err) => {
        console.error("Failed to load database records for modal", err);
        setSubmitError("Failed to fetch customer records from the database.");
      }).finally(() => {
        setIsLoadingData(false);
      });
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');
    if (!customerId) {
      setSubmitError('Please select a customer account from the database.');
      return;
    }

    setIsSubmitting(true);
    try {
      const created = await api.createQuotation({
        customer_id: customerId,
        title: proposalTitle || 'New Commercial Proposal',
        sales_rep_id: salesRep || undefined,
        estimated_value: estimatedValue ? parseFloat(estimatedValue) : undefined,
      });
      onCreated(created);
      onClose();
    } catch (err) {
      console.error('Failed to create quotation:', err);
      setSubmitError(err.message || 'Failed to initialize proposal draft in database');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-2xl max-w-md w-full p-6 flex flex-col gap-5 animate-in zoom-in-95">
        <div className="flex items-center justify-between pb-3 border-b border-[#DEE2E6]">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-[#F6F1F5] text-[#714B67] flex items-center justify-center">
              <span className="material-symbols-outlined text-[20px]">add_circle</span>
            </div>
            <h3 className="text-lg font-bold text-[#212529]">Create New Proposal</h3>
          </div>
          <button onClick={onClose} className="text-[#6C757D] hover:text-[#212529]">
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {submitError && (
          <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold">
            {submitError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-[#212529]">Customer Account Name</label>
              <span className="text-[10px] text-[#6C757D] font-mono">
                {isLoadingData ? 'Fetching...' : `${customersList.length} database accounts`}
              </span>
            </div>
            <select
              required
              disabled={isLoadingData || customersList.length === 0}
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
              className="p-3 rounded-xl border border-[#DEE2E6] text-sm text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20 bg-white disabled:bg-[#FAFAFA]"
            >
              {customersList.length === 0 && (
                <option value="">{isLoadingData ? 'Loading from database...' : 'No database records found'}</option>
              )}
              {customersList.map(c => (
                <option key={c.id} value={c.id}>
                  {c.name || c.company_name} {c.tier ? `(${c.tier})` : ''}
                </option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-bold text-[#212529]">Proposal Name / Scope</label>
            <input
              type="text"
              required
              placeholder="e.g. FY26 Infrastructure & Cloud Suite"
              value={proposalTitle}
              onChange={(e) => setProposalTitle(e.target.value)}
              className="p-3 rounded-xl border border-[#DEE2E6] text-sm text-[#212529] placeholder:text-[#6C757D] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-bold text-[#212529]">Assigned Sales Representative</label>
            <select
              value={salesRep}
              disabled={isLoadingData || repsList.length === 0}
              onChange={(e) => setSalesRep(e.target.value)}
              className="p-3 rounded-xl border border-[#DEE2E6] text-sm text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20 bg-white disabled:bg-[#FAFAFA]"
            >
              {repsList.length === 0 && (
                <option value="">{isLoadingData ? 'Loading reps...' : 'No sales reps found'}</option>
              )}
              {repsList.map(s => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.role ? s.role.replace('_', ' ') : 'sales rep'})
                </option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-bold text-[#212529]">Estimated Total Contract Value ($)</label>
            <input
              type="number"
              required
              placeholder="e.g. 45000"
              value={estimatedValue}
              onChange={(e) => setEstimatedValue(e.target.value)}
              className="p-3 rounded-xl border border-[#DEE2E6] text-sm font-mono text-[#212529] placeholder:text-[#6C757D] focus:outline-none focus:ring-2 focus:ring-[#714B67]/20"
            />
          </div>

          <div className="flex items-center justify-end gap-3 mt-3 pt-3 border-t border-[#DEE2E6]">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2.5 rounded-xl bg-[#F6F1F5] text-[#212529] font-bold text-xs"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || isLoadingData}
              className="px-5 py-2.5 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-bold text-xs shadow-md transition-all flex items-center gap-2 disabled:opacity-50"
            >
              {isSubmitting && <span className="material-symbols-outlined text-[16px] animate-spin">progress_activity</span>}
              <span>{isSubmitting ? 'Creating...' : 'Initialize Quote Draft'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
