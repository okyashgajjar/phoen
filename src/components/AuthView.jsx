import React, { useState } from 'react';
import { api } from '../api';

export default function AuthView({ mode = 'login', onAuthSuccess, onBackToLanding }) {
  const [isLogin, setIsLogin] = useState(mode === 'login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resetModalOpen, setResetModalOpen] = useState(false);
  const [resetSuccess, setResetSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Both login and signup use api.login because our backend
      // dynamically provisions any arbitrary new email & password!
      await api.login(email.trim(), password);
      onAuthSuccess();
    } catch (err) {
      setError(err.message || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickPersona = async (personaEmail, personaPass = 'password') => {
    setEmail(personaEmail);
    setPassword(personaPass);
    setLoading(true);
    setError('');
    try {
      await api.login(personaEmail, personaPass);
      onAuthSuccess();
    } catch (err) {
      setError(err.message || 'Quick login failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] text-[#212529] font-sans antialiased flex flex-col justify-between py-10 px-4 sm:px-6 lg:px-8 relative selection:bg-[#714B67] selection:text-white">
      {/* Decorative Odoo background accents */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[500px] bg-gradient-to-b from-[#EFE6ED]/80 via-[#F8F4F7]/40 to-transparent rounded-full blur-3xl -z-10"></div>
        <div className="absolute bottom-10 right-10 w-80 h-80 bg-teal-50 rounded-full blur-3xl -z-10"></div>
        <div className="absolute top-20 left-10 w-80 h-80 bg-purple-50 rounded-full blur-3xl -z-10"></div>
      </div>

      {/* Top Navbar Brand Link */}
      <div className="max-w-md w-full mx-auto flex items-center justify-between z-10">
        <button
          onClick={onBackToLanding}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#6C757D] hover:text-[#714B67] transition-colors"
        >
          <span className="material-symbols-outlined text-[16px]">arrow_back</span>
          Back to Phoen.io
        </button>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[11px] font-bold text-emerald-800">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          PostgreSQL Cloud Live
        </div>
      </div>

      {/* Centered Odoo Login Card */}
      <div className="sm:mx-auto sm:w-full sm:max-w-md z-10 my-auto pt-6 pb-8">
        {/* Brand Header */}
        <div className="text-center mb-6">
          <div 
            onClick={onBackToLanding}
            className="inline-flex items-center gap-3 cursor-pointer group mb-3"
          >
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[#714B67] to-[#5C3D54] flex items-center justify-center shadow-lg shadow-[#714B67]/25 group-hover:scale-105 transition-transform">
              <span className="material-symbols-outlined text-white text-[26px]">view_quilt</span>
            </div>
            <div className="text-left">
              <span className="text-2xl font-extrabold tracking-tight text-[#212529] block leading-tight">
                Phoen
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider text-[#6C757D]">
                Enterprise Commercial Cloud
              </span>
            </div>
          </div>

          {/* Odoo Database Selector Pill */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-[#EFE6ED] border border-[#714B67]/20 text-xs font-mono text-[#714B67] mt-1 shadow-sm">
            <span className="material-symbols-outlined text-[14px]">database</span>
            <span>Database: <strong>phoen_prod</strong></span>
          </div>

          <h2 className="mt-4 text-xl font-extrabold text-[#212529]">
            {isLogin ? 'Sign in to your account' : 'Create Enterprise Workspace'}
          </h2>
          <p className="text-xs text-[#6C757D] mt-1">
            {isLogin ? 'Enter your commercial credentials below' : 'Get started with instant database self-provisioning'}
          </p>
        </div>

        {/* Login Form Container (Odoo Web Login Style) */}
        <div className="bg-white py-8 px-6 sm:px-8 shadow-xl rounded-2xl border border-[#DEE2E6]">
          {/* Flexible Login Notice Banner */}
          <div className="mb-6 p-3 rounded-xl bg-[#F8F4F7] border border-[#E0CEDB] flex items-start gap-2.5">
            <span className="material-symbols-outlined text-[#714B67] text-[18px] flex-shrink-0 mt-0.5">
              auto_awesome
            </span>
            <div className="text-xs text-[#5C3D54] leading-relaxed">
              <strong className="font-bold text-[#714B67]">Instant Access Enabled:</strong> You can enter <span className="underline font-semibold">ANY email and ANY password</span>. New emails will automatically connect and create your user profile in PostgreSQL!
            </div>
          </div>

          {error && (
            <div className="mb-6 p-3.5 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-2.5 animate-in fade-in duration-200">
              <span className="material-symbols-outlined text-rose-500 text-[18px] flex-shrink-0 mt-0.5">
                error
              </span>
              <div className="text-xs text-rose-800 font-medium leading-relaxed">
                {error}
              </div>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            {!isLogin && (
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#4A4A4A] mb-1.5">
                  Full Name
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <span className="material-symbols-outlined text-[18px]">person</span>
                  </div>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Rajiv Mehta"
                    className="block w-full pl-10 pr-3 py-2.5 text-sm border border-[#DEE2E6] rounded-xl focus:ring-2 focus:ring-[#714B67] focus:border-[#714B67] bg-[#F8F9FA] focus:bg-white transition-all placeholder:text-slate-400"
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-[#4A4A4A] mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <span className="material-symbols-outlined text-[18px]">mail</span>
                </div>
                <input
                  type="email"
                  required
                  autoFocus
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. kavita@phoen.io or your@email.com"
                  className="block w-full pl-10 pr-3 py-2.5 text-sm border border-[#DEE2E6] rounded-xl focus:ring-2 focus:ring-[#714B67] focus:border-[#714B67] bg-[#F8F9FA] focus:bg-white transition-all placeholder:text-slate-400"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-bold uppercase tracking-wider text-[#4A4A4A]">
                  Password
                </label>
                {isLogin && (
                  <button
                    type="button"
                    onClick={() => setResetModalOpen(true)}
                    className="text-xs font-semibold text-[#714B67] hover:underline"
                  >
                    Reset Password
                  </button>
                )}
              </div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <span className="material-symbols-outlined text-[18px]">lock</span>
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Any password accepted (e.g. password)"
                  className="block w-full pl-10 pr-10 py-2.5 text-sm border border-[#DEE2E6] rounded-xl focus:ring-2 focus:ring-[#714B67] focus:border-[#714B67] bg-[#F8F9FA] focus:bg-white transition-all placeholder:text-slate-400"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-[#714B67] transition-colors"
                >
                  <span className="material-symbols-outlined text-[18px]">
                    {showPassword ? 'visibility_off' : 'visibility'}
                  </span>
                </button>
              </div>
            </div>

            {isLogin && (
              <div className="flex items-center pt-1">
                <input
                  id="remember-me"
                  type="checkbox"
                  defaultChecked
                  className="h-4 w-4 text-[#714B67] focus:ring-[#714B67] border-slate-300 rounded cursor-pointer"
                />
                <label htmlFor="remember-me" className="ml-2 block text-xs text-[#6C757D] cursor-pointer">
                  Remember my session on this device
                </label>
              </div>
            )}

            <div className="pt-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-xl text-white font-bold text-sm bg-[#714B67] hover:bg-[#5C3D54] active:scale-[0.99] shadow-md shadow-[#714B67]/25 transition-all flex items-center justify-center gap-2 disabled:opacity-70 cursor-pointer"
              >
                {loading ? (
                  <>
                    <span className="material-symbols-outlined animate-spin text-[18px]">sync</span>
                    Authenticating...
                  </>
                ) : (
                  <>
                    <span>{isLogin ? 'Log in' : 'Create & Launch Workspace'}</span>
                    <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Quick Demo Personas (1-Click Instant Login) */}
          <div className="mt-8 pt-6 border-t border-[#DEE2E6]">
            <div className="text-center mb-3">
              <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">
                Or 1-Click Instant Demo Login
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              {/* Sales Rep */}
              <button
                type="button"
                disabled={loading}
                onClick={() => handleQuickPersona('kavita@phoen.io', 'password')}
                className="p-2.5 rounded-xl border border-[#E0CEDB] bg-[#F8F4F7] hover:bg-[#EFE6ED] text-left transition-all flex items-center gap-2.5 group cursor-pointer"
              >
                <div className="w-8 h-8 rounded-lg bg-[#714B67]/15 flex items-center justify-center text-[#714B67] flex-shrink-0 group-hover:scale-110 transition-transform">
                  <span className="material-symbols-outlined text-[18px]">badge</span>
                </div>
                <div className="overflow-hidden">
                  <span className="block text-xs font-bold text-[#212529] truncate">Kavita Sharma</span>
                  <span className="block text-[10px] text-[#714B67] font-semibold truncate">Sales Executive</span>
                </div>
              </button>

              {/* Sales Manager */}
              <button
                type="button"
                disabled={loading}
                onClick={() => handleQuickPersona('vikram@phoen.io', 'password')}
                className="p-2.5 rounded-xl border border-amber-200 bg-amber-50/70 hover:bg-amber-100 text-left transition-all flex items-center gap-2.5 group cursor-pointer"
              >
                <div className="w-8 h-8 rounded-lg bg-amber-200/60 flex items-center justify-center text-amber-800 flex-shrink-0 group-hover:scale-110 transition-transform">
                  <span className="material-symbols-outlined text-[18px]">verified_user</span>
                </div>
                <div className="overflow-hidden">
                  <span className="block text-xs font-bold text-[#212529] truncate">Vikramaditya S.</span>
                  <span className="block text-[10px] text-amber-800 font-semibold truncate">Sales Manager</span>
                </div>
              </button>

              {/* Finance Manager */}
              <button
                type="button"
                disabled={loading}
                onClick={() => handleQuickPersona('david@phoen.io', 'password')}
                className="p-2.5 rounded-xl border border-teal-200 bg-teal-50/70 hover:bg-teal-100 text-left transition-all flex items-center gap-2.5 group cursor-pointer"
              >
                <div className="w-8 h-8 rounded-lg bg-teal-200/60 flex items-center justify-center text-teal-800 flex-shrink-0 group-hover:scale-110 transition-transform">
                  <span className="material-symbols-outlined text-[18px]">receipt_long</span>
                </div>
                <div className="overflow-hidden">
                  <span className="block text-xs font-bold text-[#212529] truncate">David Chen</span>
                  <span className="block text-[10px] text-teal-800 font-semibold truncate">Finance Manager</span>
                </div>
              </button>

              {/* System Admin */}
              <button
                type="button"
                disabled={loading}
                onClick={() => handleQuickPersona('admin@phoen.io', 'password')}
                className="p-2.5 rounded-xl border border-purple-200 bg-purple-50/70 hover:bg-purple-100 text-left transition-all flex items-center gap-2.5 group cursor-pointer"
              >
                <div className="w-8 h-8 rounded-lg bg-purple-200/60 flex items-center justify-center text-purple-800 flex-shrink-0 group-hover:scale-110 transition-transform">
                  <span className="material-symbols-outlined text-[18px]">admin_panel_settings</span>
                </div>
                <div className="overflow-hidden">
                  <span className="block text-xs font-bold text-[#212529] truncate">Alex Admin</span>
                  <span className="block text-[10px] text-purple-800 font-semibold truncate">System Admin</span>
                </div>
              </button>
            </div>
          </div>

          {/* Mode Switch & Bottom Links */}
          <div className="mt-6 pt-4 border-t border-slate-100 text-center text-xs text-[#6C757D]">
            {isLogin ? (
              <span>
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setIsLogin(false); setError(''); }}
                  className="font-bold text-[#714B67] hover:underline cursor-pointer"
                >
                  Sign up for free
                </button>
              </span>
            ) : (
              <span>
                Already have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setIsLogin(true); setError(''); }}
                  className="font-bold text-[#714B67] hover:underline cursor-pointer"
                >
                  Sign in
                </button>
              </span>
            )}
          </div>
        </div>

        {/* Odoo Style Footer Details */}
        <div className="mt-6 text-center text-xs text-[#6C757D] space-y-2">
          <div className="flex items-center justify-center gap-4 text-[11px]">
            <a 
              href="#manage-db" 
              onClick={(e) => { e.preventDefault(); alert('Connected to PostgreSQL Database: phoen_prod\nHost: 127.0.0.1:5432\nDriver: psycopg2 / SQLAlchemy'); }}
              className="hover:text-[#714B67] underline"
            >
              Manage Databases
            </a>
            <span>•</span>
            <button 
              onClick={onBackToLanding}
              className="hover:text-[#714B67] underline cursor-pointer"
            >
              Phoen Home
            </button>
            <span>•</span>
            <span className="text-slate-400">v2.4-Enterprise</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Powered by Phoen • Odoo-Inspired Enterprise Architecture
          </p>
        </div>
      </div>

      {/* Reset Password Modal */}
      {resetModalOpen && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-in fade-in duration-150">
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-sm w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-[#212529]">Reset Password</h3>
              <button 
                onClick={() => { setResetModalOpen(false); setResetSuccess(false); }}
                className="text-slate-400 hover:text-slate-600 cursor-pointer"
              >
                <span className="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>
            {resetSuccess ? (
              <div className="p-3 bg-emerald-50 text-emerald-800 rounded-xl text-xs leading-relaxed">
                ✓ Password reset instruction: Flexible login is currently active. You can enter <strong>any password</strong> to log into your account directly!
              </div>
            ) : (
              <div className="space-y-4">
                <p className="text-xs text-[#6C757D]">
                  Enter your email address and we'll unlock your credentials instantly.
                </p>
                <input 
                  type="email" 
                  defaultValue={email}
                  placeholder="name@company.com"
                  className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#714B67]"
                />
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => setResetModalOpen(false)}
                    className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => setResetSuccess(true)}
                    className="px-4 py-1.5 text-xs font-bold bg-[#714B67] text-white rounded-lg hover:bg-[#5C3D54] cursor-pointer"
                  >
                    Send Reset Link
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Footer copyright */}
      <div className="text-center text-[11px] text-slate-400 z-10">
        © 2026 Phoen Inc. All rights reserved.
      </div>
    </div>
  );
}
