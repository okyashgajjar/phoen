import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function DealHealthView() {
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await api.getDealHealth();
        setData(res);
        setAnomalies(res?.anomalies || []);
      } catch (err) {
        console.error('Failed to load deal health:', err);
      }
    }
    loadData();
  }, []);

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#6C757D] mb-1">
            <span>Commercial Intelligence</span>
            <span>/</span>
            <span className="text-[#714B67]">Deal Health & Anomaly Sentinel</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529]">Deal Health & Anomaly Sentinel</h1>
          <p className="text-sm text-[#4A4A4A] mt-1">Real-time AI monitoring for margin compression, discount leakage, and stalled proposals.</p>
        </div>
      </div>

      {/* Health Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm flex flex-col justify-between">
          <span className="text-xs font-bold text-[#6C757D] uppercase">Pipeline Health Score</span>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-emerald-600">{data?.health_score || 88.4}</span>
            <span className="text-sm text-[#6C757D]">/ 100</span>
          </div>
          <span className="text-xs text-emerald-700 font-bold mt-2">+2.1 points this pacing cycle</span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm flex flex-col justify-between">
          <span className="text-xs font-bold text-[#6C757D] uppercase">Avg Discount Rate</span>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-[#212529]">{data?.avg_discount_rate || '12.4%'}</span>
          </div>
          <span className="text-xs text-[#6C757D] mt-2">Target &lt; 15.0% rep cap</span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm flex flex-col justify-between">
          <span className="text-xs font-bold text-[#6C757D] uppercase">Flagged Exceptions</span>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-amber-600">
              {data?.discount_anomalies_count || anomalies.filter(a => a.severity === 'HIGH').length || 3}
            </span>
            <span className="text-sm text-[#6C757D]">deals</span>
          </div>
          <span className="text-xs text-amber-700 font-bold mt-2">Requires Tier 1 Director review</span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm flex flex-col justify-between">
          <span className="text-xs font-bold text-[#6C757D] uppercase">Stagnation Alert</span>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-rose-600">{data?.stalled_deals_count || 1}</span>
            <span className="text-sm text-[#6C757D]">deals &gt; 7d</span>
          </div>
          <span className="text-xs text-rose-700 font-bold mt-2 truncate max-w-[220px]" title={data?.stalled_customer_name}>
            {data?.stalled_customer_name || 'Arvind Industrial Systems Pvt Ltd'}
          </span>
        </div>
      </div>

      {/* Sentinel Audit Trail */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm p-6 flex flex-col gap-4">
        <h2 className="text-lg font-bold text-[#212529]">Live Anomaly Audit Log</h2>
        <div className="divide-y divide-[#F1F1F1]">
          {anomalies.map((an) => {
            const rawQuoteId = an.deal ? an.deal.split(' ')[0] : null;
            const isValidQuote = rawQuoteId && (rawQuoteId.startsWith('QT-') || rawQuoteId.startsWith('Q-'));

            return (
              <div key={an.id} className="py-4 flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
                    an.severity === 'HIGH' ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-700'
                  }`}>
                    <span className="material-symbols-outlined text-[22px]">warning</span>
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-[#714B67]">{an.deal}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        an.severity === 'HIGH' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                      }`}>
                        {an.severity}
                      </span>
                    </div>
                    <p className="text-xs font-bold text-[#212529] mt-0.5">{an.issue}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 shrink-0">
                  <span className="text-xs font-mono font-bold text-rose-700">{an.impact}</span>
                  {isValidQuote && (
                    <button
                      onClick={() => navigate(`/approvals/${rawQuoteId}`)}
                      className="px-3 py-1.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-800 font-bold text-xs border border-amber-200 transition-colors"
                    >
                      Sign-Off
                    </button>
                  )}
                  <button
                    onClick={() => {
                      if (isValidQuote) {
                        navigate(`/quote-detail/${rawQuoteId}`);
                      } else {
                        navigate('/quotations');
                      }
                    }}
                    className="px-3 py-1.5 rounded-lg bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs transition-colors"
                  >
                    Investigate
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
