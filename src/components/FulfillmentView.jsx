import React, { useState } from 'react';

export default function FulfillmentView({ setActiveTab }) {
  const [orders, setOrders] = useState([
    {
      id: 'ORD-8821',
      account: 'Acme Corp',
      quoteId: 'Q-1042',
      date: 'Sept 05, 2026',
      itemsCount: 3,
      warehouse: 'US-East Central Hub (Virginia)',
      status: 'STOCK_RESERVED',
      statusLabel: 'Stock Reserved',
      serials: ['SN-HW-99401', 'SN-HW-99402', 'SN-HW-99403', 'SN-HW-99404'],
    },
    {
      id: 'ORD-8819',
      account: 'TechCorp Industries',
      quoteId: 'Q-1039',
      date: 'Sept 04, 2026',
      itemsCount: 8,
      warehouse: 'EU-West Hub (Frankfurt)',
      status: 'DISPATCHED',
      statusLabel: 'Dispatched & Tracking Enabled',
      serials: ['SN-HW-88102', 'SN-HW-88103'],
    },
    {
      id: 'ORD-8818',
      account: 'Apex Dynamics',
      quoteId: 'Q-1041',
      date: 'Sept 02, 2026',
      itemsCount: 6,
      warehouse: 'US-West Hub (Oregon)',
      status: 'DELIVERED',
      statusLabel: 'Delivered to Site',
      serials: ['SN-HW-77120'],
    },
  ]);

  const dispatchOrder = (id) => {
    setOrders((oList) =>
      oList.map((o) => (o.id === id ? { ...o, status: 'DISPATCHED', statusLabel: 'Dispatched & Tracking Enabled' } : o))
    );
  };

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#76777d] mb-1">
            <span>Operations</span>
            <span>/</span>
            <span className="text-[#2563eb]">Fulfillment & Stock Management</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30]">Order Fulfillment & Inventory</h1>
          <p className="text-sm text-[#45464d] mt-1">Track serial numbers, warehouse stock allocations, and delivery dispatches for confirmed contracts.</p>
        </div>
        <button
          onClick={() => alert('Inventory Scan & Serial Audit tool launched!')}
          className="flex items-center gap-2 px-5 h-11 rounded-xl bg-[#2563eb] text-white hover:bg-[#1d4ed8] font-bold text-xs shadow-md transition-all"
        >
          <span className="material-symbols-outlined text-[18px]">qr_code_scanner</span>
          <span>Scan Inventory Serial</span>
        </button>
      </div>

      {/* Orders List */}
      <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-6">
        <h2 className="text-lg font-bold text-[#0b1c30]">Active Fulfillment Queue</h2>
        <div className="divide-y divide-[#f1f5f9]">
          {orders.map((ord) => (
            <div key={ord.id} className="py-6 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-sm font-bold text-[#2563eb]">{ord.id}</span>
                  <span className="text-xs font-bold text-[#0b1c30]">{ord.account}</span>
                  <span className="text-xs text-[#76777d] font-mono">({ord.quoteId})</span>
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                    ord.status === 'STOCK_RESERVED' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
                  }`}>
                    {ord.statusLabel}
                  </span>
                </div>
                <span className="text-xs text-[#45464d]">Warehouse: <strong>{ord.warehouse}</strong> • Order Date: {ord.date}</span>
                <div className="flex items-center gap-2 mt-1 flex-wrap">
                  <span className="text-xs text-[#76777d]">Assigned Serials:</span>
                  {ord.serials.map((sn) => (
                    <span key={sn} className="px-2 py-0.5 rounded bg-[#eff4ff] text-xs font-mono font-bold text-[#0b1c30]">
                      {sn}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex items-center gap-3 shrink-0">
                {ord.status === 'STOCK_RESERVED' && (
                  <button
                    onClick={() => dispatchOrder(ord.id)}
                    className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md transition-all flex items-center gap-1.5"
                  >
                    <span className="material-symbols-outlined text-[18px]">local_shipping</span>
                    <span>Confirm Dispatch & Shipping</span>
                  </button>
                )}
                <button
                  onClick={() => setActiveTab('invoices')}
                  className="px-4 py-2.5 rounded-xl bg-[#eff4ff] hover:bg-[#e5eeff] text-[#2563eb] font-bold text-xs"
                >
                  View Invoice Ledger
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
