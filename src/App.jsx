import React, { useState } from 'react';
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

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [searchQuery, setSearchQuery] = useState('');
  const [isNewQuoteModalOpen, setIsNewQuoteModalOpen] = useState(false);

  const handleCreateQuote = (newQuote) => {
    // Navigate to Quotation Detail after creating draft
    setActiveTab('quote-detail');
  };

  return (
    <div className="min-h-screen bg-[#f8f9ff] text-[#0b1c30] flex flex-col antialiased">
      {/* Global Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenNewQuote={() => setIsNewQuoteModalOpen(true)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />

      {/* Main Content View Container */}
      <main className="pt-20 flex-1 w-full pb-16">
        {activeTab === 'dashboard' && (
          <DashboardView
            setActiveTab={setActiveTab}
            onOpenNewQuote={() => setIsNewQuoteModalOpen(true)}
          />
        )}
        {activeTab === 'quotations' && (
          <QuotationsView
            setActiveTab={setActiveTab}
            onOpenNewQuote={() => setIsNewQuoteModalOpen(true)}
          />
        )}
        {activeTab === 'quote-detail' && (
          <QuotationDetailView setActiveTab={setActiveTab} />
        )}
        {activeTab === 'approvals' && (
          <ApprovalCockpitView setActiveTab={setActiveTab} />
        )}
        {activeTab === 'catalog' && (
          <CatalogRulesView setActiveTab={setActiveTab} />
        )}
        {activeTab === 'negotiation' && (
          <NegotiationPortalView setActiveTab={setActiveTab} />
        )}
        {activeTab === 'fulfillment' && (
          <FulfillmentView setActiveTab={setActiveTab} />
        )}
        {activeTab === 'subscriptions' && (
          <SubscriptionsView setActiveTab={setActiveTab} />
        )}
        {activeTab === 'invoices' && (
          <InvoicesView setActiveTab={setActiveTab} />
        )}
        {activeTab === 'deal-health' && (
          <DealHealthView setActiveTab={setActiveTab} />
        )}
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
