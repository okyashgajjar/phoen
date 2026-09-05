import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function DealHealthView({ setActiveTab }) {
  const [anomalies, setAnomalies] = useState([]);
  const [healthScore, setHealthScore] = useState(0);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await api.getDealHealth();
        setAnomalies(data.anomalies || []);
        setHealthScore(data.health_score || 0);
      } catch (err) {
        console.error('Failed to load deal health:', err);
      }
    }
    loadData();
  }, []);

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#76777d] mb-1">
            <span>Commercial Intelligence</span>
            <span>/</span>
            <span className="text-[#2563eb]">Deal Health & Anomaly Sentinel</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#0b1c30]">Deal Health & Anomaly Sentinel</h1>
          <p className="text-sm text-[#45464d] mt-1">Real-time AI monitoring for margin compression, discount leakage, and stalled proposals.</p>
        </div>
      </div>

      {/* Health Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm flex flex-col justify-between">
          <span className="text-xs font-bold text-[#76777d] uppercase">Pipeline Health Score</span>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-emerald-600">88.4</span>
            <span className="text-sm text-[#76777d]">/ 100</span>
          </div>
          <span className="text-xs text-emerald-700 font-bold mt-2">+2.1 points this week</span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm flex flex-col justify-between">
          <span className="text-xs font-bold text-[#76777d] uppercase">Avg Discount Rate</span>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-[#0b1c30]">12.4%</span>
          </div>
          <span className="text-xs text-[#76777d] mt-2">Target &lt; 15.0%</span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm flex flex-col justify-between">
          <span className="text-xs font-bold text-[#76777d] uppercase">Flagged Exceptions</span>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-amber-600">3</span>
            <span className="text-sm text-[#76777d]">deals</span>
          </div>
          <span className="text-xs text-amber-700 font-bold mt-2">Requires executive review</span>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-[#e2e8f0] shadow-sm flex flex-col justify-between">
          <span className="text-xs font-bold text-[#76777d] uppercase">Stagnation Alert</span>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-4xl font-extrabold text-rose-600">1</span>
            <span className="text-sm text-[#76777d]">deal &gt; 14d</span>
          </div>
          <span className="text-xs text-rose-700 font-bold mt-2">Cyberdyne Inc</span>
        </div>
      </div>

      {/* Sentinel Audit Trail */}
      <div className="bg-white rounded-2xl border border-[#e2e8f0] shadow-sm p-6 flex flex-col gap-4">
        <h2 className="text-lg font-bold text-[#0b1c30]">Live Anomaly Audit Log</h2>
        <div className="divide-y divide-[#f1f5f9]">
          {anomalies.map((an) => (
            <div key={an.id} className="py-4 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
                  an.severity === 'HIGH' ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-700'
                }`}>
                  <span className="material-symbols-outlined text-[22px]">warning</span>
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-[#2563eb]">{an.deal}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      an.severity === 'HIGH' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {an.severity}
                    </span>
                  </div>
                  <p className="text-xs font-bold text-[#0b1c30] mt-0.5">{an.issue}</p>
                </div>
              </div>
              <div className="flex items-center gap-4 shrink-0">
                <span className="text-xs font-mono font-bold text-rose-700">{an.impact}</span>
                <button
                  onClick={() => setActiveTab(an.deal.includes('Q-1042') ? 'approvals' : 'quotations')}
                  className="px-3 py-1.5 rounded-lg bg-[#eff4ff] hover:bg-[#e5eeff] text-[#2563eb] font-bold text-xs"
                >
                  Investigate
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
