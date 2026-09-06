import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { api } from '../api';

/**
 * Upsell & Cross-Sell Panel — Powered by AI & Core Business Logic.
 *
 * Sits beside the quotation cart and shows a ranked suggestion list driven by
 * co-purchase history, hardware-to-SLA attachment rules, and variant tier upgrades.
 */

const BADGE_STYLES = {
  'Tier Upgrade': 'bg-amber-100 text-amber-900 border border-amber-300',
  'SLA Attachment': 'bg-purple-100 text-purple-900 border border-purple-300',
  'Deployment Service': 'bg-blue-100 text-blue-900 border border-blue-300',
  'Margin Booster': 'bg-emerald-100 text-emerald-900 border border-emerald-300',
  'Smart Accessory': 'bg-cyan-100 text-cyan-900 border border-cyan-300',
  'AI Smart Match': 'bg-[#EFE6ED] text-[#714B67] border border-[#D9C4D3]',
};

function formatINR(value) {
  if (value === null || value === undefined) return '—';
  return `₹${Number(value).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
}

export default function UpsellPanel({ quotationId, onAdd, refreshKey }) {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dismissed, setDismissed] = useState([]);
  const [impact, setImpact] = useState({});
  const [addingId, setAddingId] = useState(null);
  const [filterTab, setFilterTab] = useState('ALL'); // ALL, UPSELL, CROSS_SELL, ATTACHMENT

  const load = useCallback(async () => {
    if (!quotationId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.getSuggestions(quotationId, 8);
      setSuggestions(res.suggestions || []);
    } catch (err) {
      setError(err.message || 'Could not load suggestions');
    } finally {
      setLoading(false);
    }
  }, [quotationId]);

  useEffect(() => {
    load();
  }, [load, refreshKey]);

  const previewImpact = async (productId) => {
    if (impact[productId]) return;
    try {
      const res = await api.getSuggestionImpact(quotationId, productId);
      setImpact((prev) => ({ ...prev, [productId]: res }));
    } catch {
      /* preview is best-effort */
    }
  };

  const handleAdd = async (s) => {
    setAddingId(s.product_id);
    try {
      await onAdd?.(s);
      setDismissed((d) => [...d, s.product_id]);
    } finally {
      setAddingId(null);
    }
  };

  const visible = useMemo(() => {
    return suggestions
      .filter((s) => !dismissed.includes(s.product_id))
      .filter((s) => {
        if (filterTab === 'ALL') return true;
        if (filterTab === 'UPSELL') return s.type === 'UPSELL';
        if (filterTab === 'CROSS_SELL') return s.type === 'CROSS_SELL';
        if (filterTab === 'ATTACHMENT') return s.type === 'ATTACHMENT';
        return true;
      });
  }, [suggestions, dismissed, filterTab]);

  return (
    <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-5 flex flex-col gap-3.5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-[#212529] flex items-center gap-1.5">
            <span className="material-symbols-outlined text-[18px] text-[#714B67]">auto_awesome</span>
            AI Smart Upsell &amp; Attachments
          </h3>
          <p className="text-[11px] text-[#6C757D]">
            Driven by historical co-purchases &amp; margin logic
          </p>
        </div>
        <button
          onClick={load}
          className="text-[11px] font-bold text-[#714B67] hover:text-[#5C3D54] px-2.5 py-1 rounded-lg hover:bg-[#F8F4F7] transition-colors flex items-center gap-1"
        >
          <span className="material-symbols-outlined text-[14px]">refresh</span>
          Refresh
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-1 p-1 rounded-xl bg-[#F8F9FA] border border-[#DEE2E6] text-[10px] font-bold">
        <button
          onClick={() => setFilterTab('ALL')}
          className={`flex-1 py-1 rounded-lg transition-all ${
            filterTab === 'ALL' ? 'bg-white text-[#714B67] shadow-sm' : 'text-[#6C757D] hover:text-[#212529]'
          }`}
        >
          All ({suggestions.length})
        </button>
        <button
          onClick={() => setFilterTab('UPSELL')}
          className={`flex-1 py-1 rounded-lg transition-all ${
            filterTab === 'UPSELL' ? 'bg-white text-[#714B67] shadow-sm' : 'text-[#6C757D] hover:text-[#212529]'
          }`}
        >
          Tier Upgrades
        </button>
        <button
          onClick={() => setFilterTab('ATTACHMENT')}
          className={`flex-1 py-1 rounded-lg transition-all ${
            filterTab === 'ATTACHMENT' ? 'bg-white text-[#714B67] shadow-sm' : 'text-[#6C757D] hover:text-[#212529]'
          }`}
        >
          SLAs &amp; Services
        </button>
        <button
          onClick={() => setFilterTab('CROSS_SELL')}
          className={`flex-1 py-1 rounded-lg transition-all ${
            filterTab === 'CROSS_SELL' ? 'bg-white text-[#714B67] shadow-sm' : 'text-[#6C757D] hover:text-[#212529]'
          }`}
        >
          Add-ons
        </button>
      </div>

      {loading && (
        <div className="py-8 text-center text-xs text-[#6C757D] flex flex-col items-center gap-2">
          <span className="material-symbols-outlined animate-spin text-[20px] text-[#714B67]">sync</span>
          Analyzing cart items with AI recommendation rules…
        </div>
      )}

      {!loading && error && (
        <div className="py-3 px-3 rounded-xl bg-amber-50 border border-amber-200 text-[11px] text-amber-900">
          {error}
        </div>
      )}

      {!loading && !error && visible.length === 0 && (
        <div className="py-8 text-center text-xs text-[#6C757D] flex flex-col items-center gap-1">
          <span className="material-symbols-outlined text-[24px] text-[#ADB5BD]">verified</span>
          <span>No recommendations found matching current filter.</span>
        </div>
      )}

      {!loading &&
        !error &&
        visible.map((s) => {
          const badgeClass = BADGE_STYLES[s.ai_badge] || BADGE_STYLES['AI Smart Match'];
          const imp = impact[s.product_id];

          return (
            <div
              key={s.product_id}
              onMouseEnter={() => previewImpact(s.product_id)}
              className="border border-[#DEE2E6] rounded-xl p-3 flex flex-col gap-2.5 hover:border-[#C7A9BF] hover:bg-[#FAFAFA] transition-all relative group"
            >
              <div className="flex items-start justify-between gap-2">
                <span className="text-xs font-bold text-[#212529] leading-snug">{s.name}</span>
                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold shrink-0 ${badgeClass}`}>
                  {s.ai_badge || s.type}
                </span>
              </div>

              {/* AI Rationale Callout Box */}
              {s.ai_rationale && (
                <div className="p-2 rounded-lg bg-[#FAF5F8] border border-[#EADBDF] text-[11px] text-[#5C3D54] flex items-start gap-1.5 leading-snug">
                  <span className="material-symbols-outlined text-[14px] text-[#714B67] shrink-0 mt-0.5">
                    psychology
                  </span>
                  <span>{s.ai_rationale}</span>
                </div>
              )}

              {/* Pricing & Margin Delta */}
              <div className="flex items-center justify-between text-[11px] pt-0.5">
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-[#212529]">{formatINR(s.unit_price)}</span>
                  {s.is_recurring && (
                    <span className="text-[10px] text-[#6C757D] font-medium">/{s.billing_frequency?.toLowerCase() || 'yr'}</span>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-emerald-700 font-bold">+{s.margin_delta}% margin</span>
                  <span className="text-[10px] text-[#6C757D]">({(s.confidence * 100).toFixed(0)}% fit)</span>
                </div>
              </div>

              {/* Blended Margin Impact Preview */}
              {imp && (
                <div className="text-[10px] text-[#5C3D54] bg-[#F8F4F7] rounded-lg px-2.5 py-1.5 flex items-center justify-between">
                  <span>
                    Blended margin: {imp.order_margin_before}% → <strong>{imp.order_margin_after}%</strong>
                  </span>
                  <span className="font-bold text-emerald-700">
                    +{formatINR(imp.gross_profit_added)} profit
                  </span>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center gap-2 pt-1">
                <button
                  onClick={() => handleAdd(s)}
                  disabled={addingId === s.product_id}
                  className="flex-1 py-1.5 rounded-lg bg-[#714B67] hover:bg-[#5C3D54] disabled:opacity-60 text-white text-[11px] font-bold shadow-sm transition-colors flex items-center justify-center gap-1"
                >
                  <span className="material-symbols-outlined text-[14px]">add</span>
                  {addingId === s.product_id ? 'Adding…' : 'Add to Quote'}
                </button>
                <button
                  onClick={() => setDismissed((d) => [...d, s.product_id])}
                  className="px-2.5 py-1.5 rounded-lg border border-[#DEE2E6] text-[#6C757D] text-[11px] font-bold hover:bg-[#F1F1F1] transition-colors"
                >
                  Dismiss
                </button>
              </div>
            </div>
          );
        })}
    </div>
  );
}
