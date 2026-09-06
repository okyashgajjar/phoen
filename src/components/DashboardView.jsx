import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function DashboardView({ currentUser, onOpenNewQuote }) {
  const navigate = useNavigate();

  const [kpis, setKpis] = useState(null);
  const [dealHealth, setDealHealth] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [kpiData, healthData] = await Promise.all([
          api.getDashboardKPIs().catch(() => null),
          api.getDealHealth().catch(() => null),
        ]);
        setKpis(kpiData);
        setDealHealth(healthData);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      }
    }
    loadData();
  }, []);

  const role = currentUser?.role || 'sales_rep';

  // ─── Dynamic Workspaces per Role ───
  const getModulesForRole = () => {
    switch (role) {
      case 'sales_rep':
        return [
          {
            id: 'quote-detail',
            title: 'Quotation Builder',
            desc: 'Configure line items, volume discount schedules, and contract terms in interactive CPQ.',
            icon: 'calculate',
            badge: 'Interactive CPQ',
            badgeColor: 'bg-[#EFE6ED] text-[#472F41]',
            tab: 'quote-detail',
          },
          {
            id: 'negotiation',
            title: 'Customer Negotiation Preview',
            desc: 'Preview client portals, inspect buyer engagement, and track counter-offers.',
            icon: 'handshake',
            badge: kpis ? `${kpis.negotiation_count || 2} active portals` : 'Live Portals',
            badgeColor: 'bg-emerald-100 text-emerald-800',
            tab: 'negotiation',
          },
          {
            id: 'quotations',
            title: 'My Proposals Pipeline',
            desc: 'Track and manage your commercial quotations across all deal stages.',
            icon: 'description',
            badge: kpis ? `${kpis.total_active_deals} personal deals` : 'Active',
            badgeColor: 'bg-slate-100 text-slate-800',
            tab: 'quotations',
          },
          {
            id: 'pending-approvals',
            title: 'Margin & Pending Review',
            desc: 'Monitor proposals undergoing supervisory discount and margin clearance.',
            icon: 'hourglass_top',
            badge: kpis ? `${kpis.pending_review_count} awaiting review` : 'Reviewing',
            badgeColor: 'bg-amber-100 text-amber-800',
            tab: 'quotations?status=PENDING_APPROVAL',
          },
        ];
      case 'manager':
        return [
          {
            id: 'approvals',
            title: 'Approval Cockpit (Tier 1)',
            desc: 'Review margin exceptions, multi-tier approvals, and policy overrides.',
            icon: 'verified_user',
            badge: kpis ? `${kpis.pending_review_count} pending` : '...',
            badgeColor: 'bg-amber-100 text-amber-800',
            tab: 'approvals',
          },
          {
            id: 'deal-health',
            title: 'Deal Health Sentinel',
            desc: 'Detect stalled quotes, discount outliers, and margin degradation.',
            icon: 'monitoring',
            badge: dealHealth ? `${dealHealth.health_score}% health` : 'Active',
            badgeColor: 'bg-rose-100 text-rose-800',
            tab: 'deal-health',
          },
          {
            id: 'quotations',
            title: 'Team Sales Pipeline',
            desc: 'Supervise all rep proposals, team pacing, and deal conversion stages.',
            icon: 'request_quote',
            badge: kpis ? `$${(kpis.total_pipeline / 1000).toFixed(0)}k pipeline` : 'Active',
            tab: 'quotations',
          },
        ];
      case 'finance':
        return [
          {
            id: 'governance',
            title: 'Discount Governance & Ceilings',
            desc: 'Configure Tier × Category discount caps, margin floors, and L0–L4 approval bands.',
            icon: 'tune',
            badge: 'Policy Ceilings',
            badgeColor: 'bg-purple-100 text-purple-800',
            tab: 'governance',
          },
          {
            id: 'reports',
            title: 'Executive Financial Reporting',
            desc: 'Deep dive into quotation conversions, revenue velocity, and discount leakages.',
            icon: 'analytics',
            badge: 'Realtime KPIs',
            badgeColor: 'bg-[#EFE6ED] text-[#472F41]',
            tab: 'reports',
          },
          {
            id: 'invoices',
            title: 'Invoices & Ledger',
            desc: 'Inspect customer billing invoices, payment statuses, and revenue ledger.',
            icon: 'receipt_long',
            badge: '56 Invoices',
            tab: 'invoices',
          },
          {
            id: 'subscriptions',
            title: 'Subscriptions & MRR',
            desc: 'Manage recurring billing schedules, contract renewals, and ARR schedules.',
            icon: 'autorenew',
            badge: '26 Contracts',
            tab: 'subscriptions',
          },
          {
            id: 'approvals',
            title: 'Financial Sign-Offs (Tier 2)',
            desc: 'Approve or reject high-discount exception quotes and payment terms.',
            icon: 'verified_user',
            badge: kpis ? `${kpis.pending_review_count} awaiting` : 'Pending Sign-Off',
            badgeColor: 'bg-amber-100 text-amber-800',
            tab: 'approvals',
          },
          {
            id: 'fulfillment',
            title: 'Fulfillment & Warehouse Splits',
            desc: 'Manage warehouse split allocations, manual overrides, and backorders.',
            icon: 'inventory',
            badge: '45 Orders',
            tab: 'fulfillment',
          },
        ];
      case 'admin':
      default:
        return [
          {
            id: 'catalog',
            title: 'Catalog & Rule Engine',
            desc: 'Manage CPQ pricing tiers, margin guardrails, and discount thresholds.',
            icon: 'rule',
            badge: '32 active rules',
            tab: 'catalog',
          },
          {
            id: 'team',
            title: 'Team Management & RBAC',
            desc: 'Provision sales reps, sales managers, and financial controllers.',
            icon: 'group',
            badge: '4 active roles',
            tab: 'team',
          },
          {
            id: 'approvals',
            title: 'Governance & Approval Routing',
            desc: 'Audit automated multi-tier escalation policies and approval events.',
            icon: 'account_tree',
            badge: 'Policy Engine',
            badgeColor: 'bg-[#EFE6ED] text-[#472F41]',
            tab: 'approvals',
          },
          {
            id: 'quotations',
            title: 'Global Pipeline Audit',
            desc: 'Platform-wide commercial visibility across all proposals and orders.',
            icon: 'request_quote',
            badge: kpis ? `${kpis.total_active_deals} active` : '...',
            tab: 'quotations',
          },
        ];
    }
  };

  const modules = getModulesForRole();

  // ─── Dynamic Priorities per Role ───
  const getPrioritiesForRole = () => {
    switch (role) {
      case 'sales_rep':
        return [
          {
            title: 'Draft Proposal for Globex Corp',
            desc: 'Customer requested 5x Phoenix Workstations with custom discount.',
            icon: 'edit_document',
            color: 'bg-[#F8F4F7]/80 border-[#E0CEDB] hover:border-[#A8809E] text-[#5C3D54]',
            badge: 'New Request',
            actionText: 'Draft in CPQ',
            action: () => (onOpenNewQuote ? onOpenNewQuote() : navigate('/quote-detail')),
          },
          {
            title: 'Review Customer Counter-Offer',
            desc: 'Global Logistics requested 2-year term lock ($62,000) on portal.',
            icon: 'question_answer',
            color: 'bg-emerald-50/80 border-emerald-200 hover:border-emerald-400 text-emerald-700',
            badge: 'Active Counter',
            actionText: 'Review Counter-Offer',
            action: () => navigate('/negotiation/Q-1040'),
          },
          {
            title: 'Check Proposal Margin Status',
            desc: 'Inspect approval progress on recently submitted quotes ($28,600).',
            icon: 'hourglass_top',
            color: 'bg-amber-50/80 border-amber-200 hover:border-amber-400 text-amber-700',
            badge: 'Under Review',
            actionText: 'Inspect Pending Deals',
            action: () => navigate('/quotations?status=PENDING_APPROVAL'),
          },
        ];
      case 'manager': {
        const topPending = dealHealth?.anomalies?.find(a => a.severity === 'HIGH') || dealHealth?.anomalies?.[0];
        const pendingDealId = topPending?.deal ? topPending.deal.split(' ')[0] : 'QT-0001';
        const pendingTitle = topPending
          ? `Sign-Off: ${topPending.deal}`
          : (kpis?.pending_review_count ? `Approve Proposals (${kpis.pending_review_count} Pending)` : 'Review Commercial Proposals');
        const pendingDesc = topPending
          ? `${topPending.issue} (${topPending.impact})`
          : 'Evaluate discount exceptions and blended margin floors for regional accounts.';

        const secondAnomaly = (dealHealth?.anomalies && dealHealth.anomalies.length > 1) ? dealHealth.anomalies[1] : topPending;
        const healthTitle = secondAnomaly
          ? `Deal Sentinel: ${secondAnomaly.deal}`
          : 'Deal Health Sentinel Active';
        const healthDesc = secondAnomaly
          ? `${secondAnomaly.issue} (${secondAnomaly.impact || 'Margin Risk'})`
          : 'Automated margin and discount monitoring active across sales pipeline.';

        return [
          {
            title: pendingTitle,
            desc: pendingDesc,
            icon: 'priority_high',
            color: 'bg-amber-50/70 border-amber-200 hover:border-amber-400 text-amber-700',
            badge: 'Tier 1 Review',
            actionText: 'Review in Cockpit',
            action: () => navigate(pendingDealId ? `/approvals/${pendingDealId}` : '/approvals'),
          },
          {
            title: healthTitle,
            desc: healthDesc,
            icon: 'warning',
            color: 'bg-rose-50/70 border-rose-200 hover:border-rose-400 text-rose-700',
            badge: 'Margin Risk',
            actionText: 'Investigate Sentinel',
            action: () => navigate('/deal-health'),
          },
          {
            title: 'Team Quota & Pacing Review',
            desc: `Inspect team performance across Kavita Sharma and regional accounts (₹${kpis?.total_pipeline ? (kpis.total_pipeline / 10000000).toFixed(2) + ' Cr' : '248.6 Cr'} pipeline).`,
            icon: 'trending_up',
            color: 'bg-[#F8F4F7]/70 border-[#E0CEDB] hover:border-[#A8809E] text-[#5C3D54]',
            badge: 'Team Pipeline',
            actionText: 'Inspect Pipeline',
            action: () => navigate('/quotations'),
          },
        ];
      }
      case 'finance':
        return [
          {
            title: 'Configure Tier Discount Ceilings',
            desc: 'Review Tier × Category discount limits, margin floors, and L0–L4 approval bands.',
            icon: 'tune',
            color: 'bg-purple-50/70 border-purple-200 hover:border-purple-400 text-purple-700',
            badge: 'Discount Policy',
            actionText: 'Manage Ceilings',
            action: () => navigate('/governance'),
          },
          {
            title: 'Executive Financial & Pipeline Reports',
            desc: 'Inspect quotation conversion velocity, win rates, and discount leakage metrics.',
            icon: 'analytics',
            color: 'bg-[#F8F4F7]/70 border-[#E0CEDB] hover:border-[#A8809E] text-[#5C3D54]',
            badge: 'Analytics',
            actionText: 'Open Reports',
            action: () => navigate('/reports'),
          },
          {
            title: 'Sign-off Tier 2 Margin Exceptions',
            desc: 'Review high-discount commercial proposals requiring Finance Controller sign-off.',
            icon: 'verified_user',
            color: 'bg-amber-50/70 border-amber-200 hover:border-amber-400 text-amber-700',
            badge: 'Tier 2 Governance',
            actionText: 'Review Sign-Offs',
            action: () => navigate('/approvals'),
          },
          {
            title: 'Audit Overdue Invoices & Collections',
            desc: 'Reconcile customer payment ledger and follow up on overdue billing schedules.',
            icon: 'receipt_long',
            color: 'bg-rose-50/70 border-rose-200 hover:border-rose-400 text-rose-700',
            badge: 'Receivables Audit',
            actionText: 'Open Ledger',
            action: () => navigate('/invoices'),
          },
        ];
      case 'admin':
      default:
        return [
          {
            title: 'Update Q4 Discount Ceilings',
            desc: 'Review hardware and cloud tier discount thresholds in rule engine.',
            icon: 'tune',
            color: 'bg-purple-50/70 border-purple-200 hover:border-purple-400 text-purple-700',
            action: () => navigate('/catalog'),
          },
          {
            title: 'User Role Provisioning & RBAC',
            desc: 'Audit access permissions and provision accounts for sales & finance.',
            icon: 'group',
            color: 'bg-[#F8F4F7]/70 border-[#E0CEDB] hover:border-[#A8809E] text-[#5C3D54]',
            action: () => navigate('/team'),
          },
          {
            title: 'Multi-Tier Routing Governance',
            desc: 'Inspect automated approval escalations and compliance logging.',
            icon: 'account_tree',
            color: 'bg-emerald-50/70 border-emerald-200 hover:border-emerald-400 text-emerald-700',
            action: () => navigate('/approvals'),
          },
        ];
    }
  };

  const priorities = getPrioritiesForRole();

  const recentActivity = [
    {
      id: 1,
      user: 'Kavita Sharma',
      avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80',
      action: 'submitted quote for commercial sign-off',
      target: 'QT-0001 (Arvind Industrial Systems)',
      time: '28 mins ago',
      amount: '$9,059,332',
      status: 'Pending L2 Review',
      statusBg: 'bg-amber-50 text-amber-800 border-amber-200',
    },
    {
      id: 2,
      user: 'Kavita Sharma',
      avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80',
      action: 'completed multi-warehouse split allocation',
      target: 'QT-0002 (Western Grid Technologies)',
      time: '2 hours ago',
      amount: '$8,099,520',
      status: 'Approved',
      statusBg: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    },
    {
      id: 3,
      user: 'Vikramaditya Singhania',
      avatar: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&auto=format&fit=crop&q=80',
      action: 'approved commercial discount override',
      target: 'QT-0003 (Torrential Health Sciences)',
      time: '4 hours ago',
      amount: '$27,036,750',
      status: 'Confirmed',
      statusBg: 'bg-[#F8F4F7] text-[#472F41] border-[#E0CEDB]',
    },
    {
      id: 4,
      user: 'David Chen',
      avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD6eGnNwcM2SWzLN7P5S_9fzAl71lAafDpxahswhQgzYLqqw_UYITDveOBT58W0KmwcQOrX4LYatjjzmk-y6DwcLx5R6RAk3k2dcTlzY52hxYLej98xxzfmBXfxl9rP__hIUR_nV7p524_UzAOEL4XkKSANGLIb6NcLx8gG654E6TSYV8JuaKRPE4Qdpu6MXyn18gJuHb1pLmcnJBQixHFZG3WZUz9Ina6EKZp_uqg8Z0hEccvcG-HL',
      action: 'verified invoice schedule & receivables',
      target: 'QT-0004 (Gujarat Precision Engineering)',
      time: '1 day ago',
      amount: '$2,105,733',
      status: 'Audit Verified',
      statusBg: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    },
  ];

  return (
    <div className="w-full max-w-[1440px] mx-auto px-4 lg:px-8 py-8 flex flex-col gap-8">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-white p-6 lg:p-8 shadow-sm border border-[#DEE2E6] flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div className="absolute -right-16 -top-16 w-80 h-80 rounded-full bg-[#714B67]/5 blur-3xl pointer-events-none"></div>
        <div className="relative flex flex-col gap-2.5 z-10">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#F6F1F5] text-[#003ea8] font-semibold text-xs">
              <span className="w-2 h-2 rounded-full bg-[#714B67] animate-pulse"></span>
              Live Commercial Operations
            </span>
            <span className="font-mono text-xs text-[#6C757D]">Q4 FY2025</span>
            {role === 'sales_rep' && (
              <span className="px-2.5 py-0.5 rounded-full bg-[#F8F4F7] text-[#5C3D54] text-xs font-bold border border-[#E0CEDB]">
                Sales Representative
              </span>
            )}
            {role === 'manager' && (
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200">
                Sales Manager & Approver
              </span>
            )}
            {role === 'finance' && (
              <span className="px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 text-xs font-bold border border-amber-200">
                Finance & Billing Controller
              </span>
            )}
            {role === 'admin' && (
              <span className="px-2.5 py-0.5 rounded-full bg-purple-50 text-purple-700 text-xs font-bold border border-purple-200">
                System Administrator
              </span>
            )}
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529] tracking-tight">
            Welcome back, {currentUser?.name ? currentUser.name.split(' ')[0] : 'Operator'}
          </h1>
          <p className="text-sm text-[#4A4A4A] max-w-2xl leading-relaxed">
            {role === 'sales_rep' &&
              'Configure proposals, check real-time margin guardrails, and engage buyers on client negotiation portals.'}
            {role === 'manager' &&
              'Supervise sales reps, evaluate multi-tier discount exceptions, and prevent pipeline margin degradation.'}
            {role === 'finance' &&
              'Audit quotation financials, sign off high-discount contracts, and post invoices to the commercial ledger.'}
            {role === 'admin' &&
              'Manage enterprise CPQ pricing rules, discount ceilings, user access permissions, and global commercial audit logs.'}
          </p>
        </div>

        {/* Role-tailored action buttons */}
        <div className="relative flex flex-wrap items-center gap-3 shrink-0 z-10">
          {role === 'sales_rep' && (
            <>
              <button
                onClick={onOpenNewQuote}
                className="group h-12 px-6 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-semibold text-sm shadow-md flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[20px] transition-transform group-hover:rotate-90">add</span>
                <span>New Quotation</span>
              </button>
              <button
                onClick={() => navigate('/quotations')}
                className="h-12 px-6 rounded-xl bg-white hover:bg-[#FAFAFA] text-[#212529] font-semibold text-sm border border-[#DEE2E6] shadow-sm flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[#6C757D] text-[20px]">request_quote</span>
                <span>My Pipeline</span>
              </button>
            </>
          )}

          {role === 'manager' && (
            <>
              <button
                onClick={() => navigate('/approvals')}
                className="h-12 px-6 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-semibold text-sm shadow-md flex items-center gap-2.5 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[20px]">verified_user</span>
                <span>Review Approvals</span>
                <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-white/20 text-white font-bold text-xs">
                  {kpis ? kpis.pending_review_count : '...'} pending
                </span>
              </button>
              <button
                onClick={() => navigate('/deal-health')}
                className="h-12 px-6 rounded-xl bg-white hover:bg-[#FAFAFA] text-[#212529] font-semibold text-sm border border-[#DEE2E6] shadow-sm flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[#6C757D] text-[20px]">monitoring</span>
                <span>Deal Health</span>
              </button>
            </>
          )}

          {role === 'finance' && (
            <>
              <button
                onClick={() => navigate('/governance')}
                className="h-12 px-5 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-semibold text-sm shadow-md flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[20px]">tune</span>
                <span>Discount Ceilings</span>
              </button>
              <button
                onClick={() => navigate('/reports')}
                className="h-12 px-5 rounded-xl bg-white hover:bg-[#FAFAFA] text-[#212529] font-semibold text-sm border border-[#DEE2E6] shadow-sm flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[#714B67] text-[20px]">analytics</span>
                <span>Financial Reports</span>
              </button>
              <button
                onClick={() => navigate('/approvals')}
                className="h-12 px-5 rounded-xl bg-white hover:bg-[#FAFAFA] text-[#212529] font-semibold text-sm border border-[#DEE2E6] shadow-sm flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[#6C757D] text-[20px]">verified_user</span>
                <span>Tier 2 Sign-Offs</span>
                <span className="inline-flex items-center px-1.5 py-0.5 rounded-full bg-amber-100 text-amber-800 font-bold text-[10px]">
                  {kpis ? kpis.pending_review_count : '...'}
                </span>
              </button>
              <button
                onClick={() => navigate('/invoices')}
                className="h-12 px-5 rounded-xl bg-white hover:bg-[#FAFAFA] text-[#212529] font-semibold text-sm border border-[#DEE2E6] shadow-sm flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[#6C757D] text-[20px]">receipt_long</span>
                <span>Invoices</span>
              </button>
            </>
          )}

          {role === 'admin' && (
            <>
              <button
                onClick={() => navigate('/catalog')}
                className="h-12 px-6 rounded-xl bg-[#714B67] hover:bg-[#5C3D54] text-white font-semibold text-sm shadow-md flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[20px]">tune</span>
                <span>Rule Engine & Catalog</span>
              </button>
              <button
                onClick={() => navigate('/team')}
                className="h-12 px-6 rounded-xl bg-white hover:bg-[#FAFAFA] text-[#212529] font-semibold text-sm border border-[#DEE2E6] shadow-sm flex items-center gap-2 transition-all active:scale-[0.98]"
              >
                <span className="material-symbols-outlined text-[#6C757D] text-[20px]">group</span>
                <span>Manage Team</span>
              </button>
            </>
          )}
        </div>
      </div>

      {/* 3-Step Guided Workflow Banner: Role-Specific Quote-to-Cash Operations */}
      <div className="rounded-2xl bg-gradient-to-r from-[#714B67]/10 via-[#F6F1F5] to-[#EFE6ED] p-6 shadow-sm border border-[#714B67]/20 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-4 shrink-0">
          <div className="w-12 h-12 rounded-xl bg-[#714B67] text-white flex items-center justify-center shadow-md">
            <span className="material-symbols-outlined text-[28px]">account_tree</span>
          </div>
          <div>
            <span className="font-bold text-base text-[#212529] block">Quote-to-Cash Operations</span>
            <span className="text-xs text-[#4A4A4A]">
              {role === 'sales_rep' && 'Your end-to-end sales cycle: Proposal drafting, margin check, and fulfillment'}
              {role === 'manager' && 'Your supervisory cycle: Team pipeline, Tier 1 margin approvals, and deal health sentinel'}
              {role === 'finance' && 'Your financial cycle: Multi-tier clearance, invoice ledger posting, and ARR subscriptions'}
              {role === 'admin' && 'Enterprise governance: Pricing rule configuration, approval routing, and audit logs'}
            </span>
          </div>
        </div>

        {/* 3 Steps tailored to the active role */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full md:max-w-2xl">
          {role === 'sales_rep' && (
            <>
              <div
                id="step-create-quote"
                onClick={() => (onOpenNewQuote ? onOpenNewQuote() : navigate('/quotations'))}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  1
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    1. Create Quote
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Pick customer & SKUs</span>
                </div>
              </div>
              <div
                id="step-automargin"
                onClick={() => navigate('/quotations')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  2
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    2. Automargin
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Margin guardrails</span>
                </div>
              </div>
              <div
                id="step-fulfill-invoice"
                onClick={() => navigate('/fulfillment')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  3
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    3. Fulfill & Track
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Warehouse dispatch</span>
                </div>
              </div>
            </>
          )}

          {role === 'manager' && (
            <>
              <div
                id="step-team-pipeline"
                onClick={() => navigate('/quotations')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  1
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    1. Team Pipeline
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Review rep proposals</span>
                </div>
              </div>
              <div
                id="step-tier1-approvals"
                onClick={() => navigate('/approvals')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  2
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    2. Tier 1 Approvals
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Sign off discount exceptions</span>
                </div>
              </div>
              <div
                id="step-deal-sentinel"
                onClick={() => navigate('/deal-health')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  3
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    3. Deal Sentinel
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Catch margin leakage</span>
                </div>
              </div>
            </>
          )}

          {role === 'finance' && (
            <>
              <div
                id="step-finance-discount"
                onClick={() => navigate('/governance')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  1
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    1. Discount Ceilings
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Tier & margin guardrails</span>
                </div>
              </div>
              <div
                id="step-finance-approval"
                onClick={() => navigate('/approvals')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  2
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    2. Tier 2 Sign-Off
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Authorize exceptions</span>
                </div>
              </div>
              <div
                id="step-finance-reports"
                onClick={() => navigate('/reports')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  3
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    3. Commercial Reports
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">P&L & discount leakage</span>
                </div>
              </div>
            </>
          )}

          {role === 'admin' && (
            <>
              <div
                id="step-admin-catalog"
                onClick={() => navigate('/catalog')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  1
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    1. Catalog & Ceilings
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Define discount rules</span>
                </div>
              </div>
              <div
                id="step-admin-governance"
                onClick={() => navigate('/approvals')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  2
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    2. Approval Routing
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">Multi-tier escalation policy</span>
                </div>
              </div>
              <div
                id="step-admin-team"
                onClick={() => navigate('/team')}
                className="flex items-center gap-3 bg-white/90 backdrop-blur-xs p-3 rounded-xl border border-[#DEE2E6] hover:border-[#714B67] hover:shadow-md cursor-pointer transition-all shadow-xs group"
              >
                <span className="w-7 h-7 rounded-full bg-[#E3D6E0] text-[#2B1D28] group-hover:bg-[#714B67] group-hover:text-white transition-colors flex items-center justify-center font-mono text-xs font-bold shrink-0">
                  3
                </span>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-bold text-[#212529] group-hover:text-[#714B67] transition-colors truncate">
                    3. RBAC & Access
                  </span>
                  <span className="text-[11px] text-[#4A4A4A] truncate">User provisioning</span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* KPI Cards Row — Role-Tailored */}
      <div className={`grid grid-cols-1 md:grid-cols-2 ${role === 'finance' ? 'xl:grid-cols-4' : 'lg:grid-cols-3'} gap-6`}>
        {role === 'sales_rep' && (
          <>
            {/* Sales Rep Card 1: My Active Proposals */}
            <div
              onClick={() => navigate('/quotations')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Personal Pipeline</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">My Proposals</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-[#F6F1F5] text-[#714B67] flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">request_quote</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">{kpis ? kpis.total_active_deals : '...'}</span>
                  <span className="text-sm text-[#4A4A4A]">active proposals</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xl font-bold text-[#212529] font-mono">
                    {kpis ? `₹${(kpis.total_pipeline / 10000000).toFixed(2)} Cr` : '...'}
                  </span>
                  <span className="inline-flex items-center gap-0.5 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold">
                    <span className="material-symbols-outlined text-[14px]">trending_up</span> +18% vs last mo
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Manage proposals <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">Drafts & Negotiating</span>
              </div>
            </div>

            {/* Sales Rep Card 2: Submitted Approvals */}
            <div
              onClick={() => navigate('/quotations?status=PENDING_APPROVAL')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-amber-400 hover:ring-2 hover:ring-amber-100 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Margin Status</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Pending Review</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">hourglass_top</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">{kpis ? kpis.pending_review_count : '...'}</span>
                  <span className="text-sm text-[#4A4A4A]">deals awaiting sign-off</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 text-xs font-semibold border border-amber-200">
                    <span className="material-symbols-outlined text-[14px]">info</span> Under manager review
                  </span>
                  <span className="text-xs text-[#6C757D]">Avg review: 42m</span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-amber-700 group-hover:underline flex items-center gap-1">
                  View pending proposals <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">Filtered Deals</span>
              </div>
            </div>

            {/* Sales Rep Card 3: Customer Portals Active */}
            <div
              onClick={() => navigate('/negotiation')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Buyer Engagement</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Customer Portals</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-[#F8F4F7] text-[#5C3D54] flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">handshake</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#5C3D54]">2</span>
                  <span className="text-sm text-[#4A4A4A]">live customer sessions</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 text-xs font-semibold border border-emerald-200">
                    <span className="material-symbols-outlined text-[14px]">check_circle</span> 1 ready to e-sign
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Open negotiation portals <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">Global Logistics & TechCorp</span>
              </div>
            </div>
          </>
        )}

        {role === 'manager' && (
          <>
            {/* Manager Card 1: Pending Approvals Queue */}
            <div
              onClick={() => navigate('/approvals')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Approval Cockpit</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Pending Approvals</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">hourglass_top</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">{kpis ? kpis.pending_review_count : '...'}</span>
                  <span className="text-sm text-[#4A4A4A]">quotations awaiting sign-off</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 text-xs font-semibold border border-amber-200">
                    <span className="material-symbols-outlined text-[14px]">priority_high</span> Action required
                  </span>
                  <span className="text-xs text-[#6C757D]">Avg review: 42m</span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Review pending queue <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">3 High • 1 Med</span>
              </div>
            </div>

            {/* Manager Card 2: Team Pipeline */}
            <div
              onClick={() => navigate('/quotations')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Team Pipeline</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5 font-sans">Open Proposals</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-[#F6F1F5] text-[#714B67] flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">request_quote</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">{kpis ? kpis.total_active_deals : '...'}</span>
                  <span className="text-sm text-[#4A4A4A]">across all sales reps</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xl font-bold text-[#212529] font-mono">
                    {kpis ? `₹${(kpis.total_pipeline / 10000000).toFixed(2)} Cr` : '...'}
                  </span>
                  <span className="inline-flex items-center gap-0.5 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold">
                    <span className="material-symbols-outlined text-[14px]">trending_up</span> +18% vs target
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Inspect team pipeline <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">4 active reps</span>
              </div>
            </div>

            {/* Manager Card 3: Deal Health Sentinel */}
            <div
              onClick={() => navigate('/deal-health')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-rose-400 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Deal Health Sentinel</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">At-Risk Deals</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-rose-50 text-rose-700 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">warning</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-rose-700">
                    {dealHealth ? (dealHealth.discount_anomalies_count ?? (dealHealth.anomalies ? dealHealth.anomalies.length : 0)) : '...'}
                  </span>
                  <span className="text-sm text-[#4A4A4A]">flagged items</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-800 text-xs font-semibold border border-rose-200">
                    <span className="material-symbols-outlined text-[14px]">error</span>
                    {dealHealth?.anomalies?.[0]?.deal || 'Risk Sentinel Active'}
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-rose-700 group-hover:underline flex items-center gap-1">
                  Fix deal guardrails <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">
                  {dealHealth?.health_score ? `${dealHealth.health_score}% health score` : 'Deal Health Active'}
                </span>
              </div>
            </div>
          </>
        )}

        {role === 'finance' && (
          <>
            {/* Finance Card 1: Discount Ceilings Matrix & Safeguards */}
            <div
              onClick={() => navigate('/governance')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-purple-400 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-purple-700">CPQ Pricing Rules</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Discount Ceilings</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-purple-50 text-purple-700 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">tune</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-purple-900">4 Tiers</span>
                  <span className="text-sm text-[#4A4A4A]">5 approval bands</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-purple-50 text-purple-800 text-xs font-semibold border border-purple-200">
                    <span className="material-symbols-outlined text-[14px]">shield</span> L0–L4 Policy Guardrails
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-purple-700 group-hover:underline flex items-center gap-1">
                  Configure ceilings matrix <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">Tier × Category Caps</span>
              </div>
            </div>

            {/* Finance Card 2: Commercial Reports & Pipeline Velocity */}
            <div
              onClick={() => navigate('/reports')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Executive Analytics</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Commercial Reports</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-[#F6F1F5] text-[#714B67] flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">analytics</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-3xl font-extrabold text-[#212529] font-mono">
                    {kpis?.total_pipeline ? `₹${(kpis.total_pipeline / 10000000).toFixed(1)} Cr` : '₹353.7 Cr'}
                  </span>
                  <span className="text-xs text-[#4A4A4A]">pipeline</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 text-xs font-semibold border border-emerald-200">
                    <span className="material-symbols-outlined text-[14px]">verified</span> 70.4% Win Rate
                  </span>
                  <span className="text-xs text-[#6C757D]">38 won deals</span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Open financial reporting <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">PDF / XLS Export</span>
              </div>
            </div>

            {/* Finance Card 3: Financial Sign-offs */}
            <div
              onClick={() => navigate('/approvals')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Financial Authority</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Tier 2 Clearance</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">verified_user</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">{kpis ? kpis.pending_review_count : '...'}</span>
                  <span className="text-sm text-[#4A4A4A]">margin exceptions awaiting sign-off</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 text-xs font-semibold border border-amber-200">
                    <span className="material-symbols-outlined text-[14px]">security</span> Finance sign-off required
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Authorize exceptions <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">Discount & Margin Audits</span>
              </div>
            </div>

            {/* Finance Card 4: Invoices & Receivables */}
            <div
              onClick={() => navigate('/invoices')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Ledger & Receivables</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Customer Invoices</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-rose-50 text-rose-700 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">receipt_long</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">$312,400</span>
                  <span className="text-sm text-[#4A4A4A]">total receivables</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xs font-semibold text-rose-700 bg-rose-50 px-2.5 py-0.5 rounded-full border border-rose-200">
                    2 overdue invoices
                  </span>
                  <span className="text-xs text-[#6C757D]">18 total ledger items</span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Open billing ledger <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">DSO: 28 days</span>
              </div>
            </div>
          </>
        )}

        {role === 'admin' && (
          <>
            {/* Admin Card 1: Catalog & Rule Engine */}
            <div
              onClick={() => navigate('/catalog')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Pricing Architecture</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Catalog & Rules</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-purple-50 text-purple-700 flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">rule</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">32</span>
                  <span className="text-sm text-[#4A4A4A]">active CPQ rules</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-purple-50 text-purple-800 text-xs font-semibold border border-purple-200">
                    <span className="material-symbols-outlined text-[14px]">tune</span> Ceilings & Bundles Configured
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Edit discount rules <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">7 Product Families</span>
              </div>
            </div>

            {/* Admin Card 2: Global Pipeline */}
            <div
              onClick={() => navigate('/quotations')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">System Pipeline</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Global Proposals</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-[#F6F1F5] text-[#714B67] flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">request_quote</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">{kpis ? kpis.total_active_deals : '...'}</span>
                  <span className="text-sm text-[#4A4A4A]">deals across system</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xl font-bold text-[#212529] font-mono">
                    {kpis ? `$${kpis.total_pipeline.toLocaleString()}` : '...'}
                  </span>
                  <span className="inline-flex items-center gap-0.5 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold">
                    <span className="material-symbols-outlined text-[14px]">check</span> All Reps Active
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Global pipeline audit <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">System Wide</span>
              </div>
            </div>

            {/* Admin Card 3: Governance & Multi-Tier Routing */}
            <div
              onClick={() => navigate('/approvals')}
              className="group rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between hover:shadow-md hover:border-[#714B67]/40 transition-all cursor-pointer"
            >
              <div>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Governance</span>
                    <h3 className="text-lg font-bold text-[#212529] mt-0.5">Multi-Tier Routing</h3>
                  </div>
                  <div className="w-11 h-11 rounded-xl bg-[#F8F4F7] text-[#5C3D54] flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">account_tree</span>
                  </div>
                </div>
                <div className="flex items-baseline gap-2 mb-2">
                  <span className="text-4xl font-extrabold text-[#212529]">{kpis ? kpis.pending_review_count : '...'}</span>
                  <span className="text-sm text-[#4A4A4A]">routed sign-offs</span>
                </div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 text-xs font-semibold border border-emerald-200">
                    <span className="material-symbols-outlined text-[14px]">verified</span> Zero SLA Breaches
                  </span>
                </div>
              </div>
              <div className="pt-4 border-t border-[#DEE2E6] flex items-center justify-between">
                <span className="text-sm font-bold text-[#714B67] group-hover:underline flex items-center gap-1">
                  Audit approval matrix <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </span>
                <span className="font-mono text-xs text-[#4A4A4A]">Manager + Finance</span>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Commercial Engine Modules Grid — Filtered strictly by role */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-[#212529]">Commercial Engine Workspaces</h2>
            <p className="text-xs text-[#4A4A4A]">
              Workspaces customized for your active role ({currentUser?.name} &bull; {role})
            </p>
          </div>
          <span className="text-xs text-[#6C757D] font-semibold hidden sm:inline">
            Click any workspace card to launch
          </span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {modules.map((m) => (
            <div
              key={m.id}
              onClick={() => {
                if (m.tab.startsWith('http')) {
                  window.open(m.tab, '_blank');
                } else {
                  navigate('/' + m.tab);
                }
              }}
              className="group rounded-2xl bg-white p-5 shadow-sm border border-[#DEE2E6] hover:shadow-lg hover:border-[#714B67] transition-all cursor-pointer flex flex-col justify-between hover:-translate-y-1 relative overflow-hidden"
            >
              <div className="flex flex-col gap-3">
                <div className="w-12 h-12 rounded-xl bg-[#F6F1F5] flex items-center justify-center text-[#714B67] group-hover:bg-[#714B67] group-hover:text-white transition-all shadow-xs">
                  <span className="material-symbols-outlined text-[26px]">{m.icon}</span>
                </div>
                <div>
                  <span className="text-sm font-bold text-[#212529] block group-hover:text-[#714B67] transition-colors">
                    {m.title}
                  </span>
                  <p className="text-xs text-[#4A4A4A] mt-1 leading-snug">{m.desc}</p>
                </div>
              </div>
              <div className="mt-4 pt-3 border-t border-[#F1F1F1] flex items-center justify-between text-xs font-semibold text-[#6C757D]">
                <span className={`px-2.5 py-0.5 rounded-full font-bold text-[11px] ${m.badgeColor || 'bg-[#F1F1F1] text-[#212529]'}`}>
                  {m.badge}
                </span>
                <span className="material-symbols-outlined text-[18px] group-hover:translate-x-1 transition-transform text-[#714B67]">
                  arrow_forward
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Activity Stream & Priority Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Commercial Activity */}
        <div className="lg:col-span-2 rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6]">
          <div className="flex items-center justify-between pb-4 mb-4 border-b border-[#DEE2E6]">
            <div>
              <h3 className="text-base font-bold text-[#212529]">Recent Commercial Activity</h3>
              <p className="text-xs text-[#6C757D]">Live audit trail of quote submissions, approvals, and rule updates</p>
            </div>
            <button onClick={() => navigate('/quotations')} className="text-xs font-bold text-[#714B67] hover:underline">
              View all history
            </button>
          </div>
          <div className="divide-y divide-[#F1F1F1]">
            {recentActivity.map((item) => (
              <div key={item.id} className="py-4 flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <img src={item.avatar} alt={item.user} className="w-10 h-10 rounded-full object-cover ring-2 ring-[#DEE2E6]" />
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-[#212529]">{item.user}</span>
                      <span className="text-xs text-[#4A4A4A]">{item.action}</span>
                    </div>
                    <span
                      className="text-xs font-semibold text-[#714B67] cursor-pointer hover:underline"
                      onClick={() => navigate('/quotations')}
                    >
                      {item.target}
                    </span>
                  </div>
                </div>
                <div className="flex flex-col items-end shrink-0">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${item.statusBg}`}>
                    {item.status}
                  </span>
                  <span className="text-[11px] text-[#6C757D] mt-1">{item.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Priority Quick Actions — Tailored per Role */}
        <div className="rounded-2xl bg-white p-6 shadow-sm border border-[#DEE2E6] flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-[#212529] mb-1">Commercial Priorities</h3>
            <p className="text-xs text-[#6C757D] mb-4">
              Recommended actions for {currentUser?.name || 'Operator'}
            </p>
            <div className="space-y-3">
              {priorities.map((p, idx) => (
                <div
                  key={idx}
                  onClick={p.action}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all flex flex-col gap-2 hover:shadow-md hover:-translate-y-0.5 ${p.color}`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="material-symbols-outlined text-[20px] shrink-0">{p.icon}</span>
                      <span className="text-xs font-bold block">{p.title}</span>
                    </div>
                    {p.badge && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/90 border border-current shadow-xs shrink-0">
                        {p.badge}
                      </span>
                    )}
                  </div>
                  <p className="text-[11px] opacity-90 leading-snug pl-7">{p.desc}</p>
                  <div className="pl-7 pt-1 flex items-center justify-between">
                    <span className="text-[11px] font-bold underline flex items-center gap-1">
                      <span>{p.actionText || 'Take Action'}</span>
                      <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <button
            onClick={() => {
              if (role === 'sales_rep') navigate('/quotations');
              else if (role === 'manager') navigate('/approvals');
              else if (role === 'finance') navigate('/invoices');
              else navigate('/catalog');
            }}
            className="w-full mt-4 py-2.5 rounded-xl bg-[#F6F1F5] hover:bg-[#EFE6ED] text-[#714B67] font-bold text-xs transition-colors flex items-center justify-center gap-1"
          >
            <span>
              {role === 'sales_rep' && 'Open All Proposals'}
              {role === 'manager' && 'Open Approval Cockpit'}
              {role === 'finance' && 'Open Invoice Ledger'}
              {role === 'admin' && 'Open Catalog & Engine'}
            </span>
            <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
          </button>
        </div>
      </div>
    </div>
  );
}
