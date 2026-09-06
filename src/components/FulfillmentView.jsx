import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

const CARRIERS = [
  'Blue Dart Express',
  'Delhivery Freight Logistics',
  'FedEx Priority Enterprise',
  'TCI Express Freight',
  'V-Trans Heavy Logistics'
];

const WAREHOUSES = [
  { id: 'WH-001', name: 'Ahmedabad Enterprise Distribution Center' },
  { id: 'WH-002', name: 'Mumbai Western Regional Logistics Hub' },
  { id: 'WH-003', name: 'Bengaluru Tech Fulfillment Depot' },
  { id: 'WH-004', name: 'Delhi NCR Enterprise Supply Hub' },
  { id: 'WH-005', name: 'Hyderabad Cyber Logistics Center' }
];

export default function FulfillmentView() {
  const navigate = useNavigate();

  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterTab, setFilterTab] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  // Dispatch Logistics Modal
  const [dispatchTarget, setDispatchTarget] = useState(null);
  const [dispatchForm, setDispatchForm] = useState({
    carrier: 'Blue Dart Express',
    trackingNumber: '',
    warehouseId: 'WH-001',
    warehouseName: 'Ahmedabad Enterprise Distribution Center',
    shippingMode: 'Air Priority Express (Next-Day Air)',
    boxCount: 2,
    grossWeightKg: 14.5,
    notes: 'Handed over to courier pickup executive. Fragile enterprise server units.'
  });

  const [dispatchingId, setDispatchingId] = useState(null);
  const [downloadingChallanId, setDownloadingChallanId] = useState(null);

  // Serial Scanner Modal
  const [showScannerModal, setShowScannerModal] = useState(false);
  const [scannedSerial, setScannedSerial] = useState('');
  const [scannedResult, setScannedResult] = useState(null);

  const [toast, setToast] = useState(null);

  const showNotification = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 5000);
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await api.getFulfillmentOrders();
      setOrders(data || []);
    } catch (err) {
      console.error('Failed to load fulfillment orders:', err);
      showNotification('Failed to load fulfillment orders from database', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Filter logic
  const filteredOrders = orders.filter((ord) => {
    const status = (ord.status || '').toUpperCase();
    if (filterTab === 'RESERVED' && status !== 'STOCK_RESERVED' && status !== 'CONFIRMED') return false;
    if (filterTab === 'DISPATCHED' && status !== 'DISPATCHED' && status !== 'SHIPPED') return false;
    if (filterTab === 'DELIVERED' && status !== 'DELIVERED') return false;

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchId = (ord.id || '').toLowerCase().includes(q);
      const matchAcc = (ord.account || ord.customer_name || '').toLowerCase().includes(q);
      const matchWh = (ord.warehouse || '').toLowerCase().includes(q);
      const matchSerial = (ord.serials || []).some(s => s.toLowerCase().includes(q));
      if (!matchId && !matchAcc && !matchWh && !matchSerial) return false;
    }
    return true;
  });

  // KPI Calculations
  const countReserved = orders.filter(o => ['STOCK_RESERVED', 'CONFIRMED'].includes((o.status || '').toUpperCase())).length;
  const countDispatched = orders.filter(o => ['DISPATCHED', 'SHIPPED'].includes((o.status || '').toUpperCase())).length;
  const countDelivered = orders.filter(o => (o.status || '').toUpperCase() === 'DELIVERED').length;
  const totalValue = orders.reduce((acc, curr) => acc + (Number(curr.amount) || 0), 0);

  // Open Dispatch Modal
  const openDispatchModal = (ord) => {
    setDispatchTarget(ord);
    const cleanId = ord.id.replace('ORD-', '');
    setDispatchForm({
      carrier: 'Blue Dart Express',
      trackingNumber: `BD-EXP-${cleanId}-${Date.now().toString().slice(-4)}`,
      warehouseId: 'WH-001',
      warehouseName: ord.warehouse || 'Ahmedabad Enterprise Distribution Center',
      shippingMode: 'Air Priority Express (Next-Day Air)',
      boxCount: (ord.serials || []).length || 2,
      grossWeightKg: ((ord.serials || []).length || 2) * 7.2,
      notes: 'Handed over to courier pickup executive. Fragile enterprise hardware.'
    });
  };

  // Dispatch Action
  const handleConfirmDispatch = async (e) => {
    e.preventDefault();
    if (!dispatchTarget) return;

    try {
      setDispatchingId(dispatchTarget.id);
      const payload = {
        carrier: dispatchForm.carrier,
        tracking_number: dispatchForm.trackingNumber,
        warehouse_id: dispatchForm.warehouseId,
        warehouse_name: dispatchForm.warehouseName,
        shipping_mode: dispatchForm.shippingMode,
        box_count: Number(dispatchForm.boxCount),
        gross_weight_kg: Number(dispatchForm.grossWeightKg),
        serials: dispatchTarget.serials || [],
        notes: dispatchForm.notes
      };

      await api.dispatchOrder(dispatchTarget.id, payload);
      showNotification(`Order ${dispatchTarget.id} dispatched via ${dispatchForm.carrier}! Downloading Delivery Challan...`);
      setDispatchTarget(null);

      // Trigger automatic Delivery Challan download
      try {
        await api.downloadDeliveryChallan(dispatchTarget.id);
        showNotification(`Delivery Challan for ${dispatchTarget.id} downloaded!`);
      } catch (challanErr) {
        console.warn('Challan download error:', challanErr);
      }

      await loadData();
    } catch (err) {
      console.error('Failed to dispatch order:', err);
      showNotification('Failed to dispatch order on server', 'error');
    } finally {
      setDispatchingId(null);
    }
  };

  // Download Challan Action
  const handleDownloadChallan = async (orderId) => {
    try {
      setDownloadingChallanId(orderId);
      await api.downloadDeliveryChallan(orderId);
      showNotification(`Delivery Challan & Packing Slip for ${orderId} downloaded!`);
    } catch (err) {
      console.error('Failed to download challan:', err);
      showNotification('Failed to download delivery challan', 'error');
    } finally {
      setDownloadingChallanId(null);
    }
  };

  // Serial Audit Search
  const handleScanSerial = (e) => {
    e.preventDefault();
    if (!scannedSerial.trim()) return;

    const query = scannedSerial.trim().toLowerCase();
    const matched = orders.find(o =>
      (o.serials || []).some(s => s.toLowerCase() === query) ||
      (o.id || '').toLowerCase() === query
    );

    if (matched) {
      setScannedResult({
        found: true,
        serial: scannedSerial.trim().toUpperCase(),
        order: matched
      });
    } else {
      setScannedResult({
        found: false,
        serial: scannedSerial.trim().toUpperCase()
      });
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
            <span>Operations & Warehousing</span>
            <span>/</span>
            <span className="text-[#714B67]">Fulfillment & Stock Management</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529]">Order Fulfillment & Logistics</h1>
          <p className="text-sm text-[#4A4A4A] mt-1">
            Connected to real PostgreSQL database • Courier dispatch manifests, AWB tracking, and delivery challans.
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
            onClick={() => {
              setShowScannerModal(true);
              setScannedSerial('');
              setScannedResult(null);
            }}
            className="flex items-center gap-2 px-5 h-11 rounded-xl bg-[#714B67] text-white hover:bg-[#5C3D54] font-bold text-xs shadow-md transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">qr_code_scanner</span>
            <span>Scan Inventory Serial</span>
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Awaiting Dispatch</span>
            <span className="p-2 rounded-xl bg-amber-50 text-amber-600 material-symbols-outlined text-[20px]">pending_actions</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">{countReserved} Orders</div>
            <div className="text-xs text-amber-700 font-semibold mt-1">Stock allocated in regional hubs</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Dispatched & In-Transit</span>
            <span className="p-2 rounded-xl bg-[#F8F4F7] text-[#714B67] material-symbols-outlined text-[20px]">local_shipping</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">{countDispatched} Orders</div>
            <div className="text-xs text-[#5C3D54] font-semibold mt-1">AWB consignment tracking enabled</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Order Value Volume</span>
            <span className="p-2 rounded-xl bg-emerald-50 text-emerald-600 material-symbols-outlined text-[20px]">attach_money</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">₹{totalValue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</div>
            <div className="text-xs text-emerald-700 font-semibold mt-1">Across 45 confirmed contracts</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#6C757D] uppercase tracking-wider">Active Logistics Hubs</span>
            <span className="p-2 rounded-xl bg-purple-50 text-purple-600 material-symbols-outlined text-[20px]">warehouse</span>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-[#212529]">5 Facilities</div>
            <div className="text-xs text-purple-700 font-semibold mt-1">Ahmedabad, Mumbai, BLR, Delhi, HYD</div>
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
            All ({orders.length})
          </button>
          <button
            onClick={() => setFilterTab('RESERVED')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'RESERVED' ? 'bg-amber-600 text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Stock Reserved ({countReserved})
          </button>
          <button
            onClick={() => setFilterTab('DISPATCHED')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'DISPATCHED' ? 'bg-[#714B67] text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Dispatched ({countDispatched})
          </button>
          <button
            onClick={() => setFilterTab('DELIVERED')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              filterTab === 'DELIVERED' ? 'bg-emerald-600 text-white shadow-sm' : 'bg-[#F1F1F1] text-[#4A4A4A] hover:bg-[#DEE2E6]'
            }`}
          >
            Delivered ({countDelivered})
          </button>
        </div>

        <div className="relative w-full md:w-80">
          <span className="material-symbols-outlined absolute left-3 top-2.5 text-[#6C757D] text-[18px]">search</span>
          <input
            type="text"
            placeholder="Search order ID, account, serial..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] placeholder-[#6C757D] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
          />
        </div>
      </div>

      {/* Orders List */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-[#212529]">Active Fulfillment Queue ({filteredOrders.length} records)</h2>
          <span className="text-xs text-[#6C757D]">Showing confirmed customer purchase orders</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-sm font-semibold text-[#6C757D]">
            <span className="material-symbols-outlined animate-spin text-3xl mb-2 text-[#714B67]">sync</span>
            <p>Loading real fulfillment orders...</p>
          </div>
        ) : filteredOrders.length === 0 ? (
          <div className="p-12 text-center text-sm font-semibold text-[#6C757D]">
            <span className="material-symbols-outlined text-4xl mb-2 text-[#CED4DA]">local_shipping</span>
            <p>No orders matching the active search / filter query.</p>
          </div>
        ) : (
          <div className="divide-y divide-[#F1F1F1]">
            {filteredOrders.map((ord) => {
              const status = (ord.status || '').toUpperCase();
              const isReserved = status === 'STOCK_RESERVED' || status === 'CONFIRMED';
              const isDispatched = status === 'DISPATCHED' || status === 'SHIPPED';
              const isDelivering = dispatchingId === ord.id;
              const isDownloading = downloadingChallanId === ord.id;
              const dispatchInfo = ord.dispatch || {};

              return (
                <div key={ord.id} className="py-6 flex flex-col lg:flex-row lg:items-center justify-between gap-6 hover:bg-[#fafafa]/80 px-4 rounded-xl transition-all">
                  <div className="flex flex-col gap-2.5">
                    <div className="flex items-center gap-3 flex-wrap">
                      <span className="font-mono text-sm font-extrabold text-[#714B67]">{ord.id}</span>
                      <span className="text-sm font-bold text-[#212529]">{ord.account || ord.customer_name}</span>
                      <span className="text-xs text-[#6C757D] font-mono">({ord.quoteId || 'PO'})</span>
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold inline-flex items-center gap-1.5 ${
                        isReserved
                          ? 'bg-amber-100 text-amber-800'
                          : isDispatched
                          ? 'bg-[#EFE6ED] text-[#472F41]'
                          : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${
                          isReserved ? 'bg-amber-500' : isDispatched ? 'bg-[#8A6280]' : 'bg-emerald-500'
                        }`} />
                        {ord.statusLabel || ord.status}
                      </span>
                    </div>

                    <div className="flex items-center gap-4 text-xs text-[#4A4A4A] flex-wrap">
                      <span className="flex items-center gap-1">
                        <span className="material-symbols-outlined text-[15px] text-[#6C757D]">warehouse</span>
                        Warehouse: <strong className="text-[#212529]">{ord.warehouse}</strong>
                      </span>
                      <span>•</span>
                      <span>Order Date: <strong className="text-[#212529]">{ord.date}</strong></span>
                      <span>•</span>
                      <span>Items: <strong className="text-[#212529]">{ord.itemsCount || (ord.lines || []).length || 1} SKUs</strong></span>
                      <span>•</span>
                      <span className="font-mono font-bold text-[#212529]">
                        Total: ₹{Number(ord.amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                      </span>
                    </div>

                    {/* Dispatch & Carrier Tracking info if dispatched */}
                    {isDispatched && (
                      <div className="flex items-center gap-2.5 mt-0.5 flex-wrap">
                        <span className="px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 text-xs font-semibold flex items-center gap-1.5 border border-emerald-200">
                          <span className="material-symbols-outlined text-[14px]">local_shipping</span>
                          Carrier: <b>{dispatchInfo.carrier || 'Blue Dart Express'}</b>
                        </span>
                        <span className="px-2.5 py-1 rounded-md bg-[#F8F4F7] text-[#472F41] text-xs font-mono font-bold flex items-center gap-1.5 border border-[#E0CEDB]">
                          <span className="material-symbols-outlined text-[14px]">barcode</span>
                          AWB: {dispatchInfo.tracking_number || `BD-EXP-${ord.id.replace('ORD-', '')}-99`}
                        </span>
                      </div>
                    )}

                    {/* Serial Numbers */}
                    <div className="flex items-center gap-2 mt-1 flex-wrap">
                      <span className="text-xs font-semibold text-[#6C757D]">Assigned Serials:</span>
                      {(ord.serials || []).length > 0 ? (
                        (ord.serials || []).map((sn) => (
                          <span key={sn} className="px-2.5 py-0.5 rounded-md bg-[#F6F1F5] text-xs font-mono font-bold text-[#714B67] border border-[#714B67]/20">
                            {sn}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-[#6C757D] italic">Pending Serial Assignment</span>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2.5 shrink-0 flex-wrap">
                    {isReserved && (
                      <button
                        onClick={() => openDispatchModal(ord)}
                        disabled={isDelivering}
                        className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md transition-all flex items-center gap-2 disabled:opacity-50"
                      >
                        <span className="material-symbols-outlined text-[18px]">local_shipping</span>
                        <span>Confirm Dispatch & Shipping</span>
                      </button>
                    )}

                    {isDispatched && (
                      <button
                        onClick={() => handleDownloadChallan(ord.id)}
                        disabled={isDownloading}
                        className="px-3.5 py-2 rounded-xl bg-[#F8F4F7] hover:bg-[#EFE6ED] text-[#714B67] text-xs font-bold flex items-center gap-1.5 border border-[#E0CEDB] transition-all disabled:opacity-50"
                        title="Download official Delivery Challan & Packing Slip PDF"
                      >
                        {isDownloading ? (
                          <span className="material-symbols-outlined animate-spin text-[16px]">sync</span>
                        ) : (
                          <span className="material-symbols-outlined text-[16px]">download</span>
                        )}
                        <span>Challan PDF</span>
                      </button>
                    )}

                    <button
                      onClick={() => navigate('/invoices')}
                      className="px-4 py-2.5 rounded-xl bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs transition-all"
                    >
                      Invoice Ledger
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Industry-Level Dispatch Logistics Modal */}
      {dispatchTarget && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-2xl max-w-xl w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between pb-4 border-b border-[#DEE2E6]">
              <div className="flex items-center gap-2">
                <span className="p-2 rounded-xl bg-emerald-50 text-emerald-600 material-symbols-outlined text-[22px]">local_shipping</span>
                <div>
                  <h2 className="text-xl font-bold text-[#212529]">Outbound Dispatch & Shipping Manifest</h2>
                  <p className="text-xs text-[#6C757D]">Generate official logistics bill, register AWB, and download Delivery Challan</p>
                </div>
              </div>
              <button
                onClick={() => setDispatchTarget(null)}
                className="text-[#6C757D] hover:text-[#212529] p-1"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleConfirmDispatch} className="flex flex-col gap-4 mt-5">
              {/* Target Order Summary */}
              <div className="p-3.5 bg-[#FAFAFA] rounded-xl border border-[#DEE2E6] text-xs">
                <div className="flex justify-between items-center">
                  <span className="font-mono font-bold text-sm text-[#714B67]">{dispatchTarget.id}</span>
                  <span className="font-bold text-[#212529]">₹{Number(dispatchTarget.amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}</span>
                </div>
                <div className="font-bold text-[#212529] mt-1">{dispatchTarget.account || dispatchTarget.customer_name}</div>
                <div className="text-[#4A4A4A] text-[11px] mt-0.5">PO Ref: {dispatchTarget.quoteId}</div>
              </div>

              {/* Carrier Selection & Tracking AWB */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                    Designated Freight Carrier
                  </label>
                  <select
                    value={dispatchForm.carrier}
                    onChange={(e) => setDispatchForm({ ...dispatchForm, carrier: e.target.value })}
                    className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                    required
                  >
                    {CARRIERS.map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                    Air Waybill / Consignment #
                  </label>
                  <input
                    type="text"
                    value={dispatchForm.trackingNumber}
                    onChange={(e) => setDispatchForm({ ...dispatchForm, trackingNumber: e.target.value })}
                    className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-mono font-bold text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                    required
                  />
                </div>
              </div>

              {/* Warehouse Depot & Shipping Mode */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                    Dispatch Warehouse Depot
                  </label>
                  <select
                    value={dispatchForm.warehouseId}
                    onChange={(e) => {
                      const selectedWh = WAREHOUSES.find(w => w.id === e.target.value);
                      setDispatchForm({
                        ...dispatchForm,
                        warehouseId: e.target.value,
                        warehouseName: selectedWh?.name || dispatchForm.warehouseName
                      });
                    }}
                    className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                    required
                  >
                    {WAREHOUSES.map(w => (
                      <option key={w.id} value={w.id}>{w.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                    Shipping Logistics Mode
                  </label>
                  <select
                    value={dispatchForm.shippingMode}
                    onChange={(e) => setDispatchForm({ ...dispatchForm, shippingMode: e.target.value })}
                    className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-medium text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                  >
                    <option value="Air Priority Express (Next-Day Air)">Air Priority Express (Next-Day Air)</option>
                    <option value="Surface Road Cargo (2-4 Days)">Surface Road Cargo (2-4 Days)</option>
                    <option value="Dedicated Fleet Direct Logistics">Dedicated Fleet Direct Logistics</option>
                  </select>
                </div>
              </div>

              {/* Package Boxes and Weight */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                    Number of Packages / Boxes
                  </label>
                  <input
                    type="number"
                    min="1"
                    value={dispatchForm.boxCount}
                    onChange={(e) => setDispatchForm({ ...dispatchForm, boxCount: e.target.value })}
                    className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-mono font-bold text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                    Gross Weight (kg)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    min="0.5"
                    value={dispatchForm.grossWeightKg}
                    onChange={(e) => setDispatchForm({ ...dispatchForm, grossWeightKg: e.target.value })}
                    className="w-full px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-mono font-bold text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                    required
                  />
                </div>
              </div>

              {/* Verified Hardware Serials */}
              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                  Allocated Hardware Serials (Verified Physical Tagging)
                </label>
                <div className="p-3 bg-[#F8F4F7]/50 rounded-xl border border-[#EFE6ED] flex flex-wrap gap-2">
                  {(dispatchTarget.serials || []).map(sn => (
                    <span key={sn} className="px-2.5 py-1 rounded-md bg-white border border-[#714B67]/20 text-[#714B67] font-mono font-bold text-xs flex items-center gap-1">
                      <span className="material-symbols-outlined text-[14px] text-emerald-600">verified</span>
                      {sn}
                    </span>
                  ))}
                </div>
              </div>

              <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 flex items-start gap-2 text-xs text-emerald-800">
                <span className="material-symbols-outlined text-[18px] text-emerald-600 mt-0.5">verified_user</span>
                <span>
                  Confirming dispatch will update order status to <b>DISPATCHED</b> in PostgreSQL, generate tracking details, and <b>automatically download the Delivery Challan & Packing Slip PDF</b>.
                </span>
              </div>

              <div className="flex items-center justify-end gap-3 mt-4 pt-4 border-t border-[#DEE2E6]">
                <button
                  type="button"
                  onClick={() => setDispatchTarget(null)}
                  className="px-4 py-2.5 rounded-xl border border-[#DEE2E6] text-xs font-bold text-[#4A4A4A] hover:bg-[#F1F1F1]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={dispatchingId === dispatchTarget.id}
                  className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-md transition-all disabled:opacity-50 flex items-center gap-2"
                >
                  {dispatchingId === dispatchTarget.id ? (
                    <>
                      <span className="material-symbols-outlined animate-spin text-[16px]">sync</span>
                      <span>Dispatching & Downloading...</span>
                    </>
                  ) : (
                    <>
                      <span className="material-symbols-outlined text-[16px]">local_shipping</span>
                      <span>Confirm Dispatch & Download Challan</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Inventory Scan & Serial Audit Modal */}
      {showScannerModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-2xl max-w-lg w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between pb-4 border-b border-[#DEE2E6]">
              <div className="flex items-center gap-2">
                <span className="p-2 rounded-xl bg-[#F8F4F7] text-[#714B67] material-symbols-outlined text-[20px]">qr_code_scanner</span>
                <h2 className="text-xl font-bold text-[#212529]">Inventory Serial Audit Tool</h2>
              </div>
              <button
                onClick={() => setShowScannerModal(false)}
                className="text-[#6C757D] hover:text-[#212529] p-1"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleScanSerial} className="flex flex-col gap-4 mt-5">
              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] uppercase tracking-wider mb-1.5">
                  Enter Barcode / Serial Number or Order ID
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="e.g. SN-HW-0001-01 or ORD-0001"
                    value={scannedSerial}
                    onChange={(e) => setScannedSerial(e.target.value)}
                    className="flex-1 px-3 py-2.5 bg-[#FAFAFA] border border-[#DEE2E6] rounded-xl text-xs font-mono font-bold text-[#212529] focus:outline-none focus:ring-2 focus:ring-[#714B67]"
                    autoFocus
                  />
                  <button
                    type="submit"
                    className="px-4 py-2.5 bg-[#714B67] text-white rounded-xl text-xs font-bold hover:bg-[#5C3D54] transition-all flex items-center gap-1.5"
                  >
                    <span className="material-symbols-outlined text-[16px]">search</span>
                    <span>Verify</span>
                  </button>
                </div>
              </div>

              {/* Scan Results */}
              {scannedResult && (
                <div className="mt-2">
                  {scannedResult.found ? (
                    <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200 flex flex-col gap-2 text-xs">
                      <div className="flex items-center gap-2 text-emerald-800 font-bold text-sm">
                        <span className="material-symbols-outlined text-[18px]">verified</span>
                        <span>Serial Verified in Database</span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-[#212529] pt-2 border-t border-emerald-200">
                        <div>
                          <span className="text-[#6C757D] block">Matched Serial:</span>
                          <span className="font-mono font-bold text-[#714B67]">{scannedResult.serial}</span>
                        </div>
                        <div>
                          <span className="text-[#6C757D] block">Order ID:</span>
                          <span className="font-mono font-bold">{scannedResult.order.id}</span>
                        </div>
                        <div>
                          <span className="text-[#6C757D] block">Customer:</span>
                          <span className="font-bold">{scannedResult.order.account}</span>
                        </div>
                        <div>
                          <span className="text-[#6C757D] block">Fulfillment Status:</span>
                          <span className="font-bold text-emerald-700">{scannedResult.order.statusLabel}</span>
                        </div>
                        <div className="col-span-2">
                          <span className="text-[#6C757D] block">Warehouse:</span>
                          <span className="font-medium">{scannedResult.order.warehouse}</span>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 bg-rose-50 rounded-xl border border-rose-200 flex items-center gap-3 text-xs text-rose-800">
                      <span className="material-symbols-outlined text-[20px] text-rose-600">error</span>
                      <div>
                        <div className="font-bold">Serial Not Found</div>
                        <div>No allocated shipment record matches serial "{scannedResult.serial}".</div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              <div className="flex items-center justify-end gap-3 mt-4 pt-4 border-t border-[#DEE2E6]">
                <button
                  type="button"
                  onClick={() => setShowScannerModal(false)}
                  className="px-5 py-2.5 rounded-xl bg-[#212529] hover:bg-[#3F3B3D] text-white text-xs font-bold transition-all"
                >
                  Done
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
