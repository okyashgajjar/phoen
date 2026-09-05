import React from 'react';

export default function SubscriptionsView({ setActiveTab }) {
  const subscriptions = [
    { id: 'SUB-9021', account: 'TechCorp Industries', plan: 'Enterprise Cloud Platform (1,000 Seats)', mrr: '$11,833/mo', arr: '$142,000/yr', renewal: 'Sept 04, 2027', status: 'ACTIVE' },
    { id: 'SUB-9018', account: 'Acme Corp', plan: 'Cloud Ops Annual License (100 Seats)', mrr: '$900/mo', arr: '$10,800/yr', renewal: 'Oct 05, 2027', status: 'PENDING_ONBOARDING' },
    { id: 'SUB-8994', account: 'Apex Dynamics', plan: 'Automation ERP Suite & API Nodes', mrr: '$5,229/mo', arr: '$62,750/yr', renewal: 'Nov 12, 2026', status: 'ACTIVE' },
    { id: 'SUB-8950', account: 'Cyberdyne Inc', plan: 'AI Analytics Data Warehouse', mrr: '$4,166/mo', arr: '$50,000/yr', renewal: 'Dec 01, 2026', status: 'UPCOMING_RENEWAL' },
  ];

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#76777d] mb-1">
            <span>Billing & Revenue</span>
            <span>/</span>
            <span className="text-[#2563eb]">Subscriptions & Recurring Contracts</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30]">Active Subscriptions & ARR</h1>
          <p className="text-sm text-[#45464d] mt-1">Manage SaaS license seat allocations, expansion add-ons, co-terming, and renewals.</p>
        </div>
      </div>

      {/* Subscriptions Grid */}
      <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#f8fafc] border-b border-[#e2e8f0] text-xs font-bold text-[#76777d] uppercase">
              <th className="py-3.5 px-4">Subscription ID</th>
              <th className="py-3.5 px-4">Customer Account</th>
              <th className="py-3.5 px-4">Plan & License</th>
              <th className="py-3.5 px-4">MRR / ARR</th>
              <th className="py-3.5 px-4">Renewal Date</th>
              <th className="py-3.5 px-4">Status</th>
              <th className="py-3.5 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#f1f5f9] text-xs font-medium text-[#0b1c30]">
            {subscriptions.map((sub) => (
              <tr key={sub.id} className="hover:bg-[#f8fafc] transition-colors">
                <td className="py-4 px-4 font-mono font-bold text-[#2563eb]">{sub.id}</td>
                <td className="py-4 px-4 font-bold">{sub.account}</td>
                <td className="py-4 px-4 text-[#45464d]">{sub.plan}</td>
                <td className="py-4 px-4 font-mono">
                  <span className="font-bold text-[#0b1c30]">{sub.arr}</span>
                  <span className="block text-[11px] text-[#76777d]">{sub.mrr}</span>
                </td>
                <td className="py-4 px-4 font-mono">{sub.renewal}</td>
                <td className="py-4 px-4">
                  <span className="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-bold">
                    {sub.status.replace('_', ' ')}
                  </span>
                </td>
                <td className="py-4 px-4 text-right">
                  <button
                    onClick={() => alert(`Expansion add-on module launched for ${sub.account}!`)}
                    className="px-3 py-1.5 rounded-lg bg-[#eff4ff] hover:bg-[#e5eeff] text-[#2563eb] font-bold text-xs"
                  >
                    Add Seats / Upgrade
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
