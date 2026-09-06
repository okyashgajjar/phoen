import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function SubscriptionsView() {
  const navigate = useNavigate();

  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterTab, setFilterTab] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  // Modals & Action States
  const [upgradeTarget, setUpgradeTarget] = useState(null);
  const [additionalSeats, setAdditionalSeats] = useState(5);
  const [seatPrice, setSeatPrice] = useState(1200);

  const [cancelTarget, setCancelTarget] = useState(null);
  const [cancelReason, setCancelReason] = useState('Customer contract adjustment');

  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState(null);

  const showNotification = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await api.getSubscriptions();
      setSubscriptions(data || []);
    } catch (err) {
      console.error('Failed to load subscriptions:', err);
      showNotification('Failed to load subscriptions from database', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Filter logic
  const filteredSubscriptions = subscriptions.filter((sub) => {
    const status = (sub.status || '').toUpperCase();
    if (filterTab === 'ACTIVE' && (status === 'CANCELLED' || status === 'EXPIRED')) return false;
    if (filterTab === 'EXPIRING' && status !== 'EXPIRING') return false;
    if (filterTab === 'CANCELLED' && status !== 'CANCELLED') return false;

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchId = (sub.id || '').toLowerCase().includes(q);
      const matchAcc = (sub.account || sub.customer_name || '').toLowerCase().includes(q);
      const matchPlan = (sub.plan || sub.product_name || '').toLowerCase().includes(q);
      if (!matchId && !matchAcc && !matchPlan) return false;
    }
    return true;
  });

  // KPI Calculations
  const activeSubs = subscriptions.filter(s => (s.status || '').toUpperCase() !== 'CANCELLED');
  const totalARR = activeSubs.reduce((acc, curr) => acc + (Number(curr.annual_rate || curr.arr_raw || 0) || 45000), 0);
  const totalMRR = totalARR / 12;
  const countExpiring = subscriptions.filter(s => (s.status || '').toUpperCase() === 'EXPIRING').length;
  const countCancelled = subscriptions.filter(s => (s.status || '').toUpperCase() === 'CANCELLED').length;

  // Actions
  const handleUpgrade = async (e) => {
    e.preventDefault();
    if (!upgradeTarget) return;

    try {
      setSubmitting(true);
      const currentRate = Number(upgradeTarget.annual_rate || upgradeTarget.arr_raw || 45000);
      const rateDelta = Number(additionalSeats) * Number(seatPrice);
      const newAnnualRate = currentRate + rateDelta;

      await api.upgradeSubscription(upgradeTarget.id, {
        additional_seats: Number(additionalSeats),
        rate_increase: rateDelta,
        addon_name: `${additionalSeats} Enterprise Seats Expansion`,
        notes: `Expanded by ${additionalSeats} seats via Finance Manager console.`
      });

      showNotification(`Successfully added ${additionalSeats} seats to ${upgradeTarget.account}. New ARR: ₹${newAnnualRate.toLocaleString()}`);
      setUpgradeTarget(null);
      await loadData();
    } catch (err) {
      console.error('Failed to upgrade subscription:', err);
      showNotification('Failed to execute subscription expansion', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = async () => {
    if (!cancelTarget) return;

    try {
      setSubmitting(true);
      await api.cancelSubscription(cancelTarget.id);
      showNotification(`Subscription ${cancelTarget.id} for ${cancelTarget.account} marked as CANCELLED.`);
      setCancelTarget(null);
      await loadData();
    } catch (err) {
      console.error('Failed to cancel subscription:', err);
      showNotification('Failed to cancel subscription contract', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed bottom-6 right-6 z-50 px-5 py-3 rounded-xl shadow-2xl flex items-center gap-3 text-sm font-semibold transition-all transform animate-bounce ${
          toast.type === 'error' ? 'bg-rose-600 text-white' : 'bg-emerald-600 text-white'
        }`}>
          <span className="material-symbols-outlined text-lg">
            {toast.type === 'error' ? 'error' : 'check_circle'}
          </span>
          <span>{toast.message}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#6C757D] mb-1">
            <span>Finance & Accounts</span>
            <span>/</span>
            <span className="text-[#714B67]">Subscriptions & Recurring Contracts</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529]">Active Subscriptions & ARR</h1>
          <p className="text-sm text-[#4A4A4A] mt-1">
            Manage enterprise SaaS seat allocations, expansion add-ons, co-terming, and recurring revenue contracts.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/invoices')}
            className="flex items-center gap-2 px-4 h-11 rounded-xl bg-[#F6F1F5] text-[#714B67] hover:bg-[#EFE6ED] font-bold text-xs transition-all border border-[#714B67]/20"
          >
            <span className="material-symbols-outlined text-[18px]">receipt_long</span>
            <span>Invoices Ledger</span>
          </button>
          <button
            onClick={() => navigate('/fulfillment')}
            className="flex items-center gap-2 px-4 h-11 rounded-xl bg-[#FAFAFA] text-[#212529] hover:bg-[#DEE2E6] font-bold text-xs transition-all border border-[#DEE2E6]"
          >
            <span className="material-symbols-outlined text-[18px]">local_shipping</span>
            <span>Fulfillment Queue</span>
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Total Active ARR</span>
            <span className="p-2 rounded-xl bg-[#F8F4F7] text-[#714B67] material-symbols-outlined text-[20px]">trending_up</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">₹{totalARR.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</div>
            <div className="text-xs text-[#5C3D54] font-semibold mt-1">Annual Recurring Run-rate</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Contracted MRR</span>
            <span className="p-2 rounded-xl bg-emerald-50 text-emerald-600 material-symbols-outlined text-[20px]">calendar_month</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">₹{totalMRR.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</div>
            <div className="text-xs text-emerald-700 font-semibold mt-1">Monthly recurring cashflow</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Active Contracts</span>
            <span className="p-2 rounded-xl bg-[#F8F4F7] text-[#714B67] material-symbols-outlined text-[20px]">verified</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">{activeSubs.length} Accounts</div>
            <div className="text-xs text-[#5C3D54] font-semibold mt-1">Enterprise & Strategic plans</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Renewal Watch</span>
            <span className="p-2 rounded-xl bg-amber-50 text-amber-600 material-symbols-outlined text-[20px]">timelapse</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">{countExpiring} Renewals</div>
            <div className="text-xs text-amber-700 font-semibold mt-1">Within next 60 business days</div>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto">
          <button
            onClick={() => setFilterTab('ALL')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'ALL' ? 'bg-[#714B67] text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            All ({subscriptions.length})
          </button>
          <button
            onClick={() => setFilterTab('ACTIVE')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'ACTIVE' ? 'bg-emerald-600 text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Active Contracts ({activeSubs.length})
          </button>
          <button
            onClick={() => setFilterTab('EXPIRING')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'EXPIRING' ? 'bg-amber-600 text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Expiring Soon ({countExpiring})
          </button>
          <button
            onClick={() => setFilterTab('CANCELLED')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'CANCELLED' ? 'bg-slate-700 text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Cancelled ({countCancelled})
          </button>
        </div>

        <div className="relative w-full md:w-72">
          <span className="material-symbols-outlined absolute left-3 top-2.5 text-[#6C757D] text-[18px]">search</span>
          <input
            type="text"
            placeholder="Search account, plan, subscription..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] placeholder-[#6C757D] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
          />
        </div>
      </div>

      {/* Subscriptions Table */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-sm font-semibold text-[#6C757D]">
            <span className="material-symbols-outlined animate-spin text-3xl mb-2 text-[#714B67]">sync</span>
            <p>Loading real PostgreSQL subscription contracts...</p>
          </div>
        ) : filteredSubscriptions.length === 0 ? (
          <div className="p-12 text-center text-sm font-semibold text-[#6C757D]">
            <span className="material-symbols-outlined text-4xl mb-2 text-[#CED4DA]">inventory_2</span>
            <p>No subscriptions matching selected filters.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-[#FAFAFA] border-b border-[#DEE2E6] text-xs font-bold text-[#6C757D] uppercase tracking-wider">
                  <th className="py-3.5 px-4">Subscription ID</th>
                  <th className="py-3.5 px-4">Customer Account</th>
                  <th className="py-3.5 px-4">Plan & License</th>
                  <th className="py-3.5 px-4">Seats Allocated</th>
                  <th className="py-3.5 px-4">Contracted ARR</th>
                  <th className="py-3.5 px-4">Next Renewal</th>
                  <th className="py-3.5 px-4">Status</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#F1F1F1] text-xs font-medium text-[#212529]">
                {filteredSubscriptions.map((sub) => {
                  const status = (sub.status || '').toUpperCase();
                  const isCancelled = status === 'CANCELLED';
                  const isExpiring = status === 'EXPIRING';

                  return (
                    <tr key={sub.id} className="hover:bg-[#FAFAFA] transition-colors">
                      <td className="py-4 px-4 font-mono font-bold text-[#714B67]">
                        {sub.id}
                      </td>
                      <td className="py-4 px-4">
                        <div className="font-bold text-[#212529]">{sub.account || sub.customer_name}</div>
                        <div className="text-[11px] text-[#6C757D]">{sub.customer_id || 'Enterprise Client'}</div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="font-semibold text-[#212529]">{sub.plan || 'Enterprise AMC'}</div>
                        <div className="text-[11px] text-[#6C757D]">Co-termed License</div>
                      </td>
                      <td className="py-4 px-4">
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-lg bg-[#F8F4F7] text-[#5C3D54] font-mono font-bold text-[11px]">
                          <span className="material-symbols-outlined text-[13px]">groups</span>
                          {sub.seats || 25} Seats
                        </span>
                      </td>
                      <td className="py-4 px-4 font-mono">
                        <span className="font-extrabold text-[#212529] text-sm block">
                          {sub.arr || `₹${Number(sub.annual_rate || 45000).toLocaleString()}/yr`}
                        </span>
                        <span className="text-[11px] text-[#6C757D]">
                          {sub.mrr || `₹${Math.round(Number(sub.annual_rate || 45000)/12).toLocaleString()}/mo`}
                        </span>
                      </td>
                      <td className="py-4 px-4 font-mono text-[#4A4A4A]">
                        {sub.renewal || 'Dec 31, 2026'}
                      </td>
                      <td className="py-4 px-4">
                        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold ${
                          isCancelled
                            ? 'bg-slate-100 text-slate-700'
                            : isExpiring
                            ? 'bg-amber-100 text-amber-800'
                            : 'bg-emerald-100 text-emerald-800'
                        }`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${
                            isCancelled ? 'bg-slate-500' : isExpiring ? 'bg-amber-500' : 'bg-emerald-500'
                          }`} />
                          {sub.statusLabel || (isCancelled ? 'Cancelled' : isExpiring ? 'Expiring Soon' : 'Active')}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          {!isCancelled && (
                            <>
                              <button
                                onClick={() => {
                                  setUpgradeTarget(sub);
                                  setAdditionalSeats(5);
                                }}
                                className="px-3 py-1.5 rounded-lg bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs flex items-center gap-1 transition-all"
                                title="Expand seat quota and ARR"
                              >
                                <span className="material-symbols-outlined text-[14px]">upgrade</span>
                                <span>Upgrade</span>
                              </button>
                              <button
                                onClick={() => setCancelTarget(sub)}
                                className="px-2.5 py-1.5 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs flex items-center gap-1 transition-all"
                                title="Cancel recurring subscription"
                              >
                                <span className="material-symbols-outlined text-[14px]">cancel</span>
                              </button>
                            </>
                          )}
                          {isCancelled && (
                            <span className="text-[11px] font-semibold text-slate-400">Terminated</span>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Upgrade Seats Modal */}
      {upgradeTarget && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-2xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between pb-4 border-b border-[#DEE2E6]">
              <div className="flex items-center gap-2">
                <span className="p-2 rounded-xl bg-[#F8F4F7] text-[#714B67] material-symbols-outlined text-[20px]">upgrade</span>
                <h2 className="text-xl font-bold text-[#212529]">Upgrade Subscription Seats</h2>
              </div>
              <button
                onClick={() => setUpgradeTarget(null)}
                className="text-[#6C757D] hover:text-[#212529] p-1"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleUpgrade} className="flex flex-col gap-4 mt-5">
              <div className="p-3.5 bg-[#FAFAFA] rounded-xl border border-[#DEE2E6] text-xs">
                <div className="font-bold text-sm text-[#212529]">{upgradeTarget.account}</div>
                <div className="text-[#4A4A4A] mt-0.5">Plan: {upgradeTarget.plan}</div>
                <div className="text-[#4A4A4A]">Current Seats: <b className="text-[#212529] font-mono">{upgradeTarget.seats || 25}</b></div>
                <div className="text-[#4A4A4A]">Current ARR: <b className="text-[#212529] font-mono">₹{Number(upgradeTarget.annual_rate || 45000).toLocaleString()}</b></div>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                  Additional User Seats
                </label>
                <input
                  type="number"
                  min="1"
                  max="500"
                  value={additionalSeats}
                  onChange={(e) => setAdditionalSeats(e.target.value)}
                  className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-mono font-bold text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                  Rate Per Seat (Annual INR ₹)
                </label>
                <input
                  type="number"
                  min="100"
                  value={seatPrice}
                  onChange={(e) => setSeatPrice(e.target.value)}
                  className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-mono font-bold text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                  required
                />
              </div>

              {/* Expansion Summary */}
              <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-xs text-emerald-900">
                <div className="flex justify-between font-medium">
                  <span>Additional ARR:</span>
                  <span className="font-mono font-bold">+₹{(Number(additionalSeats) * Number(seatPrice)).toLocaleString()}</span>
                </div>
                <div className="flex justify-between font-extrabold mt-1 text-sm border-t border-emerald-300 pt-1">
                  <span>New Contract ARR:</span>
                  <span className="font-mono text-emerald-700">
                    ₹{(Number(upgradeTarget.annual_rate || 45000) + (Number(additionalSeats) * Number(seatPrice))).toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 mt-4 pt-4 border-t border-[#DEE2E6]">
                <button
                  type="button"
                  onClick={() => setUpgradeTarget(null)}
                  className="px-4 py-2.5 rounded-xl border border-[#DEE2E6] text-xs font-bold text-[#4A4A4A] hover:bg-[#F1F1F1]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2.5 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white text-xs font-bold shadow-md transition-all disabled:opacity-50 flex items-center gap-2"
                >
                  {submitting ? (
                    <>
                      <span className="material-symbols-outlined animate-spin text-[16px]">sync</span>
                      <span>Saving...</span>
                    </>
                  ) : (
                    <>
                      <span className="material-symbols-outlined text-[16px]">check</span>
                      <span>Confirm Expansion</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Cancel Subscription Modal */}
      {cancelTarget && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-2xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between pb-4 border-b border-[#DEE2E6]">
              <div className="flex items-center gap-2 text-rose-600">
                <span className="material-symbols-outlined text-[22px]">warning</span>
                <h2 className="text-xl font-bold text-[#212529]">Cancel Contract</h2>
              </div>
              <button
                onClick={() => setCancelTarget(null)}
                className="text-[#6C757D] hover:text-[#212529] p-1"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <div className="flex flex-col gap-4 mt-4">
              <p className="text-xs text-[#4A4A4A] leading-relaxed">
                Are you sure you want to cancel the active subscription contract for{' '}
                <b className="text-[#212529]">{cancelTarget.account}</b> ({cancelTarget.id})?
                This will deduct <b className="font-mono text-rose-600">₹{Number(cancelTarget.annual_rate || 45000).toLocaleString()}</b> from the portfolio ARR.
              </p>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                  Cancellation Reason / Audit Note
                </label>
                <textarea
                  rows="2"
                  value={cancelReason}
                  onChange={(e) => setCancelReason(e.target.value)}
                  className="w-full px-3 py-2 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] focus:outline-none focus:ring-2 focus:ring-rose-500"
                />
              </div>

              <div className="flex items-center justify-end gap-3 mt-4 pt-4 border-t border-[#DEE2E6]">
                <button
                  type="button"
                  onClick={() => setCancelTarget(null)}
                  className="px-4 py-2.5 rounded-xl border border-[#DEE2E6] text-xs font-bold text-[#4A4A4A] hover:bg-[#F1F1F1]"
                >
                  Keep Active
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  disabled={submitting}
                  className="px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold shadow-md transition-all disabled:opacity-50 flex items-center gap-2"
                >
                  {submitting ? (
                    <>
                      <span className="material-symbols-outlined animate-spin text-[16px]">sync</span>
                      <span>Processing...</span>
                    </>
                  ) : (
                    <>
                      <span className="material-symbols-outlined text-[16px]">delete_forever</span>
                      <span>Confirm Cancellation</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
