/**
 * DealFlow360 API Service Layer
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
    const res = await request('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name, role: 'admin' }),
    });
    // The backend doesn't return an access_token on signup, so we login directly
    return api.login(email, password);
  },

  getMe: () => request('/auth/me'),

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

  submitQuotation: (quotationId) =>
    request(`/quotations/${quotationId}/submit`, { method: 'POST' }),

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

  // ─── Fulfillment ───
  getFulfillmentOrders: () => request('/fulfillment/orders'),

  getBackorders: () => request('/fulfillment/backorders'),

  // ─── Billing ───
  getInvoices: () => request('/billing/invoices'),

  getSubscriptions: () => request('/billing/subscriptions'),

  cancelSubscription: (scheduleId) =>
    request(`/billing/subscriptions/${scheduleId}/cancel`, { method: 'POST' }),

  // ─── Reports ───
  getDashboardKPIs: () => request('/reports/dashboard'),

  getDealHealth: () => request('/reports/deal-health'),

  getCatalogRules: () => request('/reports/catalog'),

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
};
