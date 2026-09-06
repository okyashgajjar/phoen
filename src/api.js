/**
 * Phoen API Service Layer
 * Connects the React frontend to the FastAPI backend.
 */

const API_BASE = 'http://localhost:8000/api/v1';

// ─── Token management ───
export function getToken() {
  return localStorage.getItem('df360_token');
}

export function setToken(token) {
  localStorage.setItem('df360_token', token);
}

export function clearToken() {
  localStorage.removeItem('df360_token');
}

function authHeaders() {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { ...authHeaders(), ...(options.headers || {}) },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    let errorMessage = 'API Error';
    if (err.detail) {
      if (typeof err.detail === 'string') {
        errorMessage = err.detail;
      } else if (Array.isArray(err.detail)) {
        errorMessage = err.detail.map(e => e.msg || JSON.stringify(e)).join(', ');
      } else {
        errorMessage = JSON.stringify(err.detail);
      }
    }
    throw new Error(errorMessage);
  }
  return res.json();
}

// ─── Auth ───
export const api = {
  login: async (email, password) => {
    const res = await request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    if (res.access_token) {
      setToken(res.access_token);
    }
    return res;
  },

  signup: async (email, password, name) => {
    await request('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name, role: 'admin' }),
    });
    // The backend doesn't return an access_token on signup, so we login directly
    return api.login(email, password);
  },

  createUser: (userData) => request('/auth/users', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),

  updateUser: (userId, userData) => request(`/auth/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  }),

  deleteUser: (userId) => request(`/auth/users/${userId}`, {
    method: 'DELETE',
  }),

  getAllUsers: () => request('/auth/users/all'),

  getCustomers: () => request('/auth/customers'),

  getMe: () => request('/auth/me'),

  getHealth: async () => {
    try {
      const res = await fetch('http://localhost:8000/health');
      if (res.ok) {
        const data = await res.json();
        return data.status === 'ok';
      }
      return false;
    } catch {
      return false;
    }
  },

  // ─── Quotations ───
  getQuotations: () => request('/quotations/'),

  getQuotation: (id) => request(`/quotations/${id}`),

  createQuotation: (data) =>
    request('/quotations/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  addLine: (quotationId, lineData) =>
    request(`/quotations/${quotationId}/lines`, {
      method: 'POST',
      body: JSON.stringify(lineData),
    }),

  updateLine: (quotationId, lineId, data) =>
    request(`/quotations/${quotationId}/lines/${lineId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteLine: (quotationId, lineId) =>
    request(`/quotations/${quotationId}/lines/${lineId}`, {
      method: 'DELETE',
    }),

  submitQuotation: (quotationId) =>
    request(`/quotations/${quotationId}/submit`, { method: 'POST' }),

  // ─── Upsell / cross-sell panel (spec B5) ───
  getSuggestions: (quotationId, limit = 6) =>
    request(`/quotations/${quotationId}/suggestions?limit=${limit}`),

  getSuggestionImpact: (quotationId, productId) =>
    request(`/quotations/${quotationId}/suggestions/${productId}/impact`),

  // ─── Per-line discount risk breakdown (spec B4) ───
  getQuotationRisk: (quotationId) =>
    request(`/quotations/${quotationId}/risk`),

  // ─── Product catalog (spec A2, Screens 16 & 17) ───
  getCatalog: (filters = {}) => {
    const qs = new URLSearchParams(
      Object.entries(filters).filter(([, v]) => v !== '' && v != null)
    ).toString();
    return request(`/products/catalog${qs ? `?${qs}` : ''}`);
  },

  getProductDetail: (productId) => request(`/products/catalog/${productId}`),

  // ─── Approvals ───
  getPendingApprovals: () => request('/approvals/pending'),

  getApprovalChain: (quotationId) =>
    request(`/approvals/${quotationId}/chain`),

  approveQuotation: (quotationId, reason = '') =>
    request(`/approvals/${quotationId}/approve`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    }),

  rejectQuotation: (quotationId, reason = '') =>
    request(`/approvals/${quotationId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    }),

  getApprovalEvents: (quotationId) =>
    request(`/approvals/events/${quotationId}`),

  getRecentApprovalEvents: () => request('/approvals/events'),

  // ─── Fulfillment ───
  getFulfillmentOrders: () => request('/fulfillment/orders'),

  dispatchOrder: (orderId, dispatchData = {}) =>
    request(`/fulfillment/orders/${orderId}/dispatch`, {
      method: 'POST',
      body: JSON.stringify(dispatchData),
    }),

  downloadDeliveryChallan: async (orderId) => {
    const token = getToken();
    const res = await fetch(`${API_BASE}/fulfillment/orders/${orderId}/challan`, {
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
    if (!res.ok) throw new Error('Failed to download delivery challan');
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `CHALLAN-${orderId}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  getBackorders: () => request('/fulfillment/backorders'),

  // ─── Billing ───
  getInvoices: () => request('/billing/invoices'),

  createInvoice: (data) =>
    request('/billing/invoices', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  downloadInvoicePdf: async (invoiceId) => {
    const token = getToken();
    const res = await fetch(`${API_BASE}/billing/invoices/${invoiceId}/pdf`, {
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
    if (!res.ok) throw new Error('Failed to download invoice PDF');
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `INVOICE-${invoiceId}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  payInvoice: (invoiceId) =>
    request(`/billing/invoices/${invoiceId}/pay`, { method: 'POST' }),

  getSubscriptions: () => request('/billing/subscriptions'),

  upgradeSubscription: (scheduleId, data) =>
    request(`/billing/subscriptions/${scheduleId}/upgrade`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  cancelSubscription: (scheduleId) =>
    request(`/billing/subscriptions/${scheduleId}/cancel`, { method: 'POST' }),

  // ─── Reports ───
  getDashboardKPIs: () => request('/reports/dashboard'),

  getDealHealth: () => request('/reports/deal-health'),

  getCatalogRules: () => request('/reports/catalog'),

  createCatalogRule: (ruleData) => request('/reports/catalog/rules', {
    method: 'POST',
    body: JSON.stringify(ruleData),
  }),

  updateCatalogRule: (ruleId, data) => request(`/reports/catalog/rules/${ruleId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  deleteCatalogRule: (ruleId) => request(`/reports/catalog/rules/${ruleId}`, {
    method: 'DELETE',
  }),

  getAuditLogs: () => request('/reports/audit-logs'),

  // ─── Governance & Discounts ───
  getGovernanceConfig: () => request('/governance/config'),

  getGovernanceImpact: () => request('/governance/impact'),

  saveCeilings: (ceilings, reason = '') => request('/governance/ceilings', {
    method: 'PUT',
    body: JSON.stringify({ ceilings, reason }),
  }),

  saveApprovalChain: (bands, reason = '') => request('/governance/approval-chain', {
    method: 'PUT',
    body: JSON.stringify({ bands, reason }),
  }),

  // ─── Commercial Analytics & Reporting ───
  getAnalytics: (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.period) params.append('period', filters.period);
    if (filters.date_from) params.append('date_from', filters.date_from);
    if (filters.date_to) params.append('date_to', filters.date_to);
    if (filters.rep) params.append('rep', filters.rep);
    if (filters.approval_status) params.append('approval_status', filters.approval_status);
    if (filters.category_id) params.append('category_id', filters.category_id);
    if (filters.product_id) params.append('product_id', filters.product_id);
    const qs = params.toString();
    return request('/reports/analytics' + (qs ? '?' + qs : ''));
  },

  exportAnalytics: async (format, filters = {}) => {
    const token = getToken();
    const params = new URLSearchParams();
    if (filters.period) params.append('period', filters.period);
    if (filters.date_from) params.append('date_from', filters.date_from);
    if (filters.date_to) params.append('date_to', filters.date_to);
    if (filters.rep) params.append('rep', filters.rep);
    if (filters.approval_status) params.append('approval_status', filters.approval_status);
    if (filters.category_id) params.append('category_id', filters.category_id);
    if (filters.product_id) params.append('product_id', filters.product_id);
    const ext = format === 'pdf' ? 'pdf' : 'xlsx';
    const url = `${API_BASE}/reports/analytics/export.${ext}?${params.toString()}`;
    const res = await fetch(url, {
      headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    });
    if (!res.ok) throw new Error('Export failed: ' + res.statusText);
    const blob = await res.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = blobUrl;
    a.download = `phoen-report-${Date.now()}.${ext}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(blobUrl);
    document.body.removeChild(a);
  },

  // ─── Products ───
  getProducts: () => request('/products/'),

  // ─── Portal ───
  getPortalQuote: (quotationId) => request(`/portal/quotes/${quotationId}`),

  negotiateQuote: (quotationId, proposedDiscounts) =>
    request(`/portal/quotes/${quotationId}/negotiate`, {
      method: 'POST',
      body: JSON.stringify({ proposed_discounts: proposedDiscounts }),
    }),

  submitCounterProposal: (quotationId, note) =>
    request(`/portal/quotes/${quotationId}/counter`, {
      method: 'POST',
      body: JSON.stringify({ note }),
    }),

  confirmQuote: (quotationId) =>
    request(`/portal/quotes/${quotationId}/confirm`, { method: 'POST' }),

  downloadQuotationPdf: async (quotationId) => {
    const token = getToken();
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    let res = await fetch(`${API_BASE}/portal/quotes/${quotationId}/pdf`, {
      headers,
    });
    if (!res.ok) {
      res = await fetch(`${API_BASE}/quotations/${quotationId}/pdf`, {
        headers,
      });
    }
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || res.statusText || 'Proposal PDF generation failed');
    }
    const blob = await res.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = blobUrl;
    a.download = `Phoen-Commercial-Proposal-${quotationId}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(blobUrl);
    document.body.removeChild(a);
  },
};
