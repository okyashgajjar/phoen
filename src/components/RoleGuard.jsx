import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function RoleGuard({ children, allowedRoles, currentUser }) {
  const navigate = useNavigate();

  if (!currentUser) {
    return null;
  }

  const userRole = currentUser.role || 'sales_rep';

  if (!allowedRoles.includes(userRole)) {
    return (
      <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-16 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-2xl border border-red-200 shadow-xl p-8 flex flex-col items-center text-center gap-4 animate-in zoom-in-95">
          <div className="w-16 h-16 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center">
            <span className="material-symbols-outlined text-[36px]">lock</span>
          </div>
          <div>
            <h2 className="text-xl font-bold text-[#212529]">Access Restricted</h2>
            <p className="text-xs text-[#6C757D] mt-1.5">
              Your current role (<strong className="capitalize text-[#212529]">{userRole.replace('_', ' ')}</strong>) does not have permission to access this operational workspace.
            </p>
          </div>
          <div className="p-3 w-full rounded-xl bg-slate-50 border border-slate-200 text-left text-xs text-[#4A4A4A]">
            <span className="font-semibold block text-[#212529] mb-1">Required Permissions:</span>
            <div className="flex flex-wrap gap-1.5">
              {allowedRoles.map((r) => (
                <span key={r} className="px-2 py-0.5 rounded-full bg-white border border-slate-300 font-mono text-[11px] capitalize">
                  {r.replace('_', ' ')}
                </span>
              ))}
            </div>
          </div>
          <button
            onClick={() => navigate('/dashboard')}
            className="w-full py-3 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2"
          >
            <span className="material-symbols-outlined text-[16px]">arrow_back</span>
            <span>Return to My Dashboard</span>
          </button>
        </div>
      </div>
    );
  }

  return children;
}
