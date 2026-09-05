import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
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
import { api, getToken } from './api';

function AppContent() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMode, setAuthMode] = useState(null); // 'login' or 'signup'
  const [searchQuery, setSearchQuery] = useState('');
  const [isNewQuoteModalOpen, setIsNewQuoteModalOpen] = useState(false);
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

  const handleAuthSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleCreateQuote = (newQuote) => {
    navigate('/quote-detail');
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
    <div className="min-h-screen bg-[#f8f9ff] text-[#0b1c30] flex flex-col antialiased">
      {/* Global Navbar */}
      <Navbar
        currentUser={currentUser}
        apiStatus={apiStatus}
        onOpenNewQuote={() => setIsNewQuoteModalOpen(true)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />

      {/* Main Content View Container */}
      <main className="pt-20 flex-1 w-full pb-16">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardView onOpenNewQuote={() => setIsNewQuoteModalOpen(true)} />} />
          <Route path="/quotations" element={<QuotationsView onOpenNewQuote={() => setIsNewQuoteModalOpen(true)} />} />
          <Route path="/quote-detail" element={<QuotationDetailView />} />
          <Route path="/approvals" element={<ApprovalCockpitView />} />
          <Route path="/catalog" element={<CatalogRulesView />} />
          <Route path="/team" element={<TeamManagementView currentUser={currentUser} />} />
          <Route path="/negotiation" element={<NegotiationPortalView />} />
          <Route path="/fulfillment" element={<FulfillmentView />} />
          <Route path="/subscriptions" element={<SubscriptionsView />} />
          <Route path="/invoices" element={<InvoicesView />} />
          <Route path="/deal-health" element={<DealHealthView />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>

      {/* Create New Quote Modal */}
      <NewQuoteModal
        isOpen={isNewQuoteModalOpen}
        onClose={() => setIsNewQuoteModalOpen(false)}
        onCreated={handleCreateQuote}
      />

      {/* Global Footer */}
      <footer className="w-full bg-white border-t border-[#e2e8f0] py-6 px-4 lg:px-8 text-center text-xs text-[#76777d]">
        <div className="max-w-[1440px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-[#0b1c30]">Phoen</span>
            <span>•</span>
            <span>Enterprise CPQ & Revenue Operations Platform</span>
          </div>
          <div className="flex items-center gap-4">
            <a href="#" className="hover:text-[#2563eb]">Privacy Policy</a>
            <a href="#" className="hover:text-[#2563eb]">Compliance Audit</a>
            <a href="#" className="hover:text-[#2563eb]">API Documentation</a>
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
