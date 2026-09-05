import React from 'react';

export default function LandingView({ onNavigateToAuth }) {
  return (
    <div className="min-h-screen bg-slate-900 text-white font-sans overflow-hidden">
      {/* Dynamic Background */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-600 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob"></div>
        <div className="absolute top-40 -right-40 w-96 h-96 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-40 left-20 w-96 h-96 bg-indigo-600 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Nav */}
        <nav className="absolute top-0 w-full flex justify-between items-center py-6 px-4 md:px-12 backdrop-blur-md bg-slate-900/50 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
              <span className="material-symbols-outlined text-white text-xl">insights</span>
            </div>
            <span className="text-xl font-bold tracking-tight text-white">Phoen CPQ</span>
          </div>
          <div>
            <button 
              onClick={() => onNavigateToAuth('login')}
              className="text-sm font-semibold text-slate-300 hover:text-white mr-6 transition-colors"
            >
              Sign in
            </button>
            <button 
              onClick={() => onNavigateToAuth('signup')}
              className="text-sm font-semibold text-white bg-blue-600 hover:bg-blue-500 px-5 py-2.5 rounded-full shadow-lg shadow-blue-600/30 transition-all hover:scale-105 active:scale-95"
            >
              Get Started
            </button>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="text-center mt-24">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700 mb-8 backdrop-blur-sm">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            <span className="text-sm font-medium text-slate-300">Enterprise Edition v2.0 Live</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 leading-tight">
            Self-Governing <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">
              Revenue Operations
            </span>
          </h1>
          
          <p className="mt-4 max-w-2xl text-lg md:text-xl text-slate-400 mx-auto mb-10 leading-relaxed">
            Automate discount governance, multi-warehouse fulfillment, and hybrid billing all in one intelligent CPQ platform. Stop managing spreadsheets.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button 
              onClick={() => onNavigateToAuth('signup')}
              className="w-full sm:w-auto px-8 py-4 rounded-full bg-white text-slate-900 font-bold text-lg hover:bg-slate-100 transition-all hover:scale-105 shadow-[0_0_40px_-10px_rgba(255,255,255,0.4)] flex items-center justify-center gap-2"
            >
              Start Free Trial
              <span className="material-symbols-outlined text-[20px]">arrow_forward</span>
            </button>
            <button className="w-full sm:w-auto px-8 py-4 rounded-full bg-slate-800/80 text-white font-bold text-lg hover:bg-slate-700 transition-all flex items-center justify-center gap-2 border border-slate-600 backdrop-blur-sm">
              <span className="material-symbols-outlined text-[20px]">play_circle</span>
              View Demo
            </button>
          </div>
        </div>

        {/* Feature Highlights */}
        <div className="mt-32 grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
          <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-8 rounded-3xl hover:-translate-y-2 transition-transform duration-300">
            <div className="w-12 h-12 rounded-2xl bg-blue-500/20 flex items-center justify-center mb-6">
              <span className="material-symbols-outlined text-blue-400">gavel</span>
            </div>
            <h3 className="text-xl font-bold mb-3 text-white">Automated Governance</h3>
            <p className="text-slate-400 leading-relaxed">
              Instantly route quotations to the right stakeholders based on dynamic, blended margin risk scores.
            </p>
          </div>
          <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-8 rounded-3xl hover:-translate-y-2 transition-transform duration-300">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/20 flex items-center justify-center mb-6">
              <span className="material-symbols-outlined text-purple-400">local_shipping</span>
            </div>
            <h3 className="text-xl font-bold mb-3 text-white">Smart Split Fulfillment</h3>
            <p className="text-slate-400 leading-relaxed">
              Auto-split complex orders across multiple regional warehouses to minimize shipping costs and times.
            </p>
          </div>
          <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-8 rounded-3xl hover:-translate-y-2 transition-transform duration-300">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 flex items-center justify-center mb-6">
              <span className="material-symbols-outlined text-emerald-400">sync</span>
            </div>
            <h3 className="text-xl font-bold mb-3 text-white">Hybrid Billing</h3>
            <p className="text-slate-400 leading-relaxed">
              Seamlessly combine one-time hardware purchases with prorated SaaS subscriptions on a single quote.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
