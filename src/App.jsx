import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import DashboardView from './components/DashboardView';
import QuotationsView from './components/QuotationsView';
import QuotationDetailView from './components/QuotationDetailView';
import ApprovalCockpitView from './components/ApprovalCockpitView';
import CatalogRulesView from './components/CatalogRulesView';
import NegotiationPortalView from './components/NegotiationPortalView';
import FulfillmentView from './components/FulfillmentView';
import SubscriptionsView from './components/SubscriptionsView';
import InvoicesView from './components/InvoicesView';
import DealHealthView from './components/DealHealthView';
import NewQuoteModal from './components/NewQuoteModal';
import LandingView from './components/LandingView';
import AuthView from './components/AuthView';
import TeamManagementView from './components/TeamManagementView';
import DiscountGovernanceView from './components/DiscountGovernanceView';
import ReportsView from './components/ReportsView';
import ProductCatalogView from './components/ProductCatalogView';
import RoleGuard from './components/RoleGuard';
import ArchitectureModal from './components/ArchitectureModal';
import { api, getToken, setToken } from './api';

function AppContent() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMode, setAuthMode] = useState(null); // 'login' or 'signup'
  const [searchQuery, setSearchQuery] = useState('');
  const [isNewQuoteModalOpen, setIsNewQuoteModalOpen] = useState(false);
  const [isArchitectureModalOpen, setIsArchitectureModalOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [apiStatus, setApiStatus] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      const token = getToken();
      if (token) {
        try {
          const user = await api.getMe();
          setCurrentUser(user);
          setIsAuthenticated(true);
        } catch (err) {
          console.error("Auth check failed", err);
          setIsAuthenticated(false);
        }
      }
    };
    checkAuth();

    const checkHealth = async () => {
      const isHealthy = await api.getHealth();
      setApiStatus(isHealthy);
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, [isAuthenticated]);

  const handleAuthSuccess = async () => {
    try {
      const user = await api.getMe();
      setCurrentUser(user);
      setIsAuthenticated(true);
      setAuthMode(null);
    } catch (err) {
      console.error("Failed to load user profile on auth success", err);
    }
  };

  const handleSwitchRole = async (email, password = 'password') => {
    try {
      const res = await api.login(email, password);
      if (res.access_token) {
        setToken(res.access_token);
        const user = await api.getMe();
        setCurrentUser(user);
        setIsAuthenticated(true);
        navigate('/dashboard');
      }
    } catch (err) {
      console.error("Role switch failed:", err);
    }
  };

  const handleCreateQuote = (newQuote) => {
    navigate(newQuote?.id ? `/quote-detail/${newQuote.id}` : '/quote-detail');
  };

  if (!isAuthenticated || !currentUser) {
    if (authMode) {
      return (
        <AuthView 
          mode={authMode} 
          onAuthSuccess={handleAuthSuccess} 
          onBackToLanding={() => setAuthMode(null)} 
        />
      );
    }
    return <LandingView onNavigateToAuth={(mode) => setAuthMode(mode)} />;
  }

  return (
    <div className="min-h-screen bg-[#F9F9F9] text-[#212529] flex flex-col antialiased">
      {/* Global Navbar */}
      <Navbar
        currentUser={currentUser}
        apiStatus={apiStatus}
        onOpenNewQuote={() => setIsNewQuoteModalOpen(true)}
        onSwitchRole={handleSwitchRole}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onOpenArchitecture={() => setIsArchitectureModalOpen(true)}
      />

      {/* Main Content View Container */}
      <main className="flex-1 w-full pb-16">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route 
            path="/dashboard" 
            element={
              <DashboardView 
                currentUser={currentUser} 
                onOpenNewQuote={() => setIsNewQuoteModalOpen(true)} 
              />
            } 
          />
          <Route 
            path="/quotations" 
            element={
              <RoleGuard allowedRoles={['sales_rep', 'manager', 'admin', 'finance']} currentUser={currentUser}>
                <QuotationsView currentUser={currentUser} onOpenNewQuote={() => setIsNewQuoteModalOpen(true)} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/quote-detail" 
            element={
              <RoleGuard allowedRoles={['sales_rep', 'manager', 'admin', 'finance']} currentUser={currentUser}>
                <QuotationDetailView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/quote-detail/:id" 
            element={
              <RoleGuard allowedRoles={['sales_rep', 'manager', 'admin', 'finance']} currentUser={currentUser}>
                <QuotationDetailView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/approvals" 
            element={
              <RoleGuard allowedRoles={['manager', 'finance', 'admin']} currentUser={currentUser}>
                <ApprovalCockpitView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/approvals/:id" 
            element={
              <RoleGuard allowedRoles={['manager', 'finance', 'admin']} currentUser={currentUser}>
                <ApprovalCockpitView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/catalog" 
            element={
              <RoleGuard allowedRoles={['admin']} currentUser={currentUser}>
                <CatalogRulesView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/reports" 
            element={
              <RoleGuard allowedRoles={['admin', 'manager', 'finance']} currentUser={currentUser}>
                <ReportsView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/products" 
            element={
              <RoleGuard allowedRoles={['admin', 'manager', 'finance', 'sales_rep']} currentUser={currentUser}>
                <ProductCatalogView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/products/:id" 
            element={
              <RoleGuard allowedRoles={['admin', 'manager', 'finance', 'sales_rep']} currentUser={currentUser}>
                <ProductCatalogView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/governance" 
            element={
              <RoleGuard allowedRoles={['admin', 'manager', 'finance']} currentUser={currentUser}>
                <DiscountGovernanceView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/team" 
            element={
              <RoleGuard allowedRoles={['admin']} currentUser={currentUser}>
                <TeamManagementView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/negotiation" 
            element={
              <RoleGuard allowedRoles={['sales_rep', 'manager', 'admin', 'customer']} currentUser={currentUser}>
                <NegotiationPortalView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/negotiation/:id" 
            element={
              <RoleGuard allowedRoles={['sales_rep', 'manager', 'admin', 'customer']} currentUser={currentUser}>
                <NegotiationPortalView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/fulfillment" 
            element={
              <RoleGuard allowedRoles={['finance', 'admin']} currentUser={currentUser}>
                <FulfillmentView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/subscriptions" 
            element={
              <RoleGuard allowedRoles={['finance', 'admin']} currentUser={currentUser}>
                <SubscriptionsView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/invoices" 
            element={
              <RoleGuard allowedRoles={['finance', 'admin']} currentUser={currentUser}>
                <InvoicesView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route 
            path="/deal-health" 
            element={
              <RoleGuard allowedRoles={['manager', 'admin']} currentUser={currentUser}>
                <DealHealthView currentUser={currentUser} />
              </RoleGuard>
            } 
          />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>

      {/* Create New Quote Modal */}
      <NewQuoteModal
        isOpen={isNewQuoteModalOpen}
        onClose={() => setIsNewQuoteModalOpen(false)}
        onCreated={handleCreateQuote}
      />

      {/* Evaluator Architecture & Benchmark Modal */}
      <ArchitectureModal
        isOpen={isArchitectureModalOpen}
        onClose={() => setIsArchitectureModalOpen(false)}
      />

      {/* Global Footer */}
      <footer className="w-full bg-white border-t border-[#DEE2E6] py-6 px-4 lg:px-8 text-center text-xs text-[#6C757D]">
        <div className="max-w-[1440px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-[#212529]">Phoen</span>
            <span>•</span>
            <span>Intelligent, Self-Governing Sales Operations</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="px-2 py-0.5 rounded-full bg-slate-100 font-mono text-[11px] font-bold text-slate-700">
              Active Role: {currentUser?.role?.replace('_', ' ').toUpperCase()}
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}
