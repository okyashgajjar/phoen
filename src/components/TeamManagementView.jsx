import React, { useState, useEffect, useMemo } from 'react';
import { api } from '../api';

export default function TeamManagementView({ currentUser }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Search & Filter
  const [searchQuery, setSearchQuery] = useState('');
  const [roleFilter, setRoleFilter] = useState('ALL');

  // Modals state
  const [isCreating, setIsCreating] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [deleteConfirmUser, setDeleteConfirmUser] = useState(null);

  // Forms
  const [newUser, setNewUser] = useState({
    name: '',
    email: '',
    password: '',
    role: 'sales_rep',
    tier: 'Enterprise',
  });

  const [editForm, setEditForm] = useState({
    name: '',
    email: '',
    role: 'sales_rep',
    tier: 'Enterprise',
    status: 'ACTIVE',
  });

  const [notification, setNotification] = useState(null);

  const showNotification = (msg, type = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const data = await api.getAllUsers();
      setUsers(data || []);
    } catch (err) {
      console.error('Failed to fetch users', err);
      showNotification('Failed to fetch users: ' + (err.message || 'Error'), 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // Create User
  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      await api.createUser(newUser);
      showNotification(`Account for ${newUser.name} created successfully!`, 'success');
      setNewUser({ name: '', email: '', password: '', role: 'sales_rep', tier: 'Enterprise' });
      setIsCreating(false);
      fetchUsers();
    } catch (err) {
      showNotification(err.message || 'Failed to create user', 'error');
    }
  };

  // Open Edit Modal
  const openEditModal = (user) => {
    setEditingUser(user);
    setEditForm({
      name: user.name || '',
      email: user.email || '',
      role: user.role || 'sales_rep',
      tier: user.tier || 'Enterprise',
      status: user.status || 'ACTIVE',
    });
  };

  // Update User
  const handleUpdateUser = async (e) => {
    e.preventDefault();
    if (!editingUser) return;

    try {
      await api.updateUser(editingUser.id, editForm);
      showNotification(`User ${editForm.name} updated successfully!`, 'success');
      setEditingUser(null);
      fetchUsers();
    } catch (err) {
      showNotification(err.message || 'Failed to update user', 'error');
    }
  };

  // Delete / Deactivate User
  const handleDeleteUser = async () => {
    if (!deleteConfirmUser) return;
    try {
      await api.deleteUser(deleteConfirmUser.id);
      showNotification(`User ${deleteConfirmUser.name} removed from system.`, 'success');
      setDeleteConfirmUser(null);
      fetchUsers();
    } catch (err) {
      showNotification(err.message || 'Failed to delete user', 'error');
    }
  };

  // Filtered Users
  const filteredUsers = useMemo(() => {
    return users.filter((u) => {
      const matchesRole = roleFilter === 'ALL' || u.role === roleFilter;
      const matchesSearch =
        !searchQuery ||
        (u.name && u.name.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (u.email && u.email.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (u.id && u.id.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchesRole && matchesSearch;
    });
  }, [users, roleFilter, searchQuery]);

  // Metric counts
  const adminCount = users.filter((u) => u.role === 'admin').length;
  const repCount = users.filter((u) => u.role === 'sales_rep').length;
  const managerCount = users.filter((u) => u.role === 'manager').length;
  const financeCount = users.filter((u) => u.role === 'finance').length;

  if (currentUser?.role !== 'admin') {
    return (
      <div className="p-12 text-center text-rose-600 font-bold max-w-lg mx-auto bg-white rounded-2xl border border-rose-200 mt-12 shadow-sm">
        <span className="material-symbols-outlined text-4xl mb-2">lock</span>
        <h2 className="text-xl font-extrabold text-[#212529]">Access Restricted</h2>
        <p className="text-sm text-[#6C757D] mt-1">
          You must be signed in as a System Administrator to access User Governance and RBAC Management.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-[1440px] mx-auto p-4 lg:p-8 animate-in fade-in space-y-6">
      {/* Toast Notification */}
      {notification && (
        <div
          className={`fixed top-5 right-5 z-50 px-5 py-3 rounded-xl shadow-lg border flex items-center gap-3 text-sm font-semibold transition-all ${
            notification.type === 'error'
              ? 'bg-rose-50 border-rose-200 text-rose-800'
              : 'bg-emerald-50 border-emerald-200 text-emerald-800'
          }`}
        >
          <span className="material-symbols-outlined text-lg">
            {notification.type === 'error' ? 'error' : 'check_circle'}
          </span>
          <span>{notification.msg}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#6C757D] mb-1">
            <span>CPQ Administration</span>
            <span>/</span>
            <span className="text-[#714B67]">Identity & Access Governance</span>
          </div>
          <h1 className="text-3xl font-extrabold text-[#212529] tracking-tight">Team & User Governance</h1>
          <p className="text-sm text-[#4A4A4A] mt-1">
            Manage system access credentials, role-based authorization matrices, and commercial tier permissions.
          </p>
        </div>
        <button
          onClick={() => setIsCreating(true)}
          className="flex items-center gap-2 px-5 h-11 bg-[#714B67] text-white text-xs font-bold rounded-xl shadow-md hover:bg-[#5C3D54] transition-all hover:scale-[1.02]"
        >
          <span className="material-symbols-outlined text-[18px]">person_add</span>
          Add New User
        </button>
      </div>

      {/* Stats Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Total Accounts</span>
            <div className="text-2xl font-extrabold text-[#212529] mt-1">{users.length} Users</div>
            <span className="text-xs text-emerald-600 font-medium">Enterprise & Internal</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#F8F4F7] flex items-center justify-center text-[#714B67]">
            <span className="material-symbols-outlined text-2xl">group</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Sales Reps</span>
            <div className="text-2xl font-extrabold text-[#212529] mt-1">{repCount} Reps</div>
            <span className="text-xs text-slate-500 font-medium">Commercial CPQ Access</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#F8F4F7] flex items-center justify-center text-[#714B67]">
            <span className="material-symbols-outlined text-2xl">badge</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">Managers & Finance</span>
            <div className="text-2xl font-extrabold text-[#212529] mt-1">{managerCount + financeCount} Approvers</div>
            <span className="text-xs text-amber-600 font-medium">{managerCount} Sales Mgr • {financeCount} Finance</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center text-amber-600">
            <span className="material-symbols-outlined text-2xl">how_to_reg</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#DEE2E6] shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6C757D]">System Admins</span>
            <div className="text-2xl font-extrabold text-[#212529] mt-1">{adminCount} Admins</div>
            <span className="text-xs text-emerald-600 font-medium">Full Matrix Governance</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600">
            <span className="material-symbols-outlined text-2xl">admin_panel_settings</span>
          </div>
        </div>
      </div>

      {/* Create User Form Section */}
      {isCreating && (
        <div className="bg-white p-6 rounded-2xl border border-[#DEE2E6] shadow-sm animate-in slide-in-from-top-4 duration-200">
          <div className="flex items-center justify-between mb-4 border-b border-[#DEE2E6] pb-3">
            <div>
              <h2 className="text-lg font-bold text-[#212529]">Provision New Account</h2>
              <p className="text-xs text-[#6C757D] mt-0.5">Directly registers the identity with audit logging.</p>
            </div>
            <button onClick={() => setIsCreating(false)} className="text-[#6C757D] hover:text-[#212529]">
              <span className="material-symbols-outlined text-[22px]">close</span>
            </button>
          </div>

          <form onSubmit={handleCreateUser} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Rachel Torres"
                  value={newUser.name}
                  onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67] text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Email Address</label>
                <input
                  type="email"
                  required
                  placeholder="user@phoen.io"
                  value={newUser.email}
                  onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67] text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Password</label>
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={newUser.password}
                  onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67] text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">System Role</label>
                <select
                  value={newUser.role}
                  onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67] text-sm"
                >
                  <option value="sales_rep">Sales Representative</option>
                  <option value="manager">Sales Manager</option>
                  <option value="finance">Finance Manager</option>
                  <option value="admin">System Administrator</option>
                  <option value="customer">Client Customer</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Commercial Tier</label>
                <select
                  value={newUser.tier}
                  onChange={(e) => setNewUser({ ...newUser, tier: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67] text-sm"
                >
                  <option value="Enterprise">Enterprise</option>
                  <option value="Strategic">Strategic</option>
                  <option value="Standard">Standard</option>
                  <option value="Gold">Gold</option>
                  <option value="Silver">Silver</option>
                  <option value="Bronze">Bronze</option>
                </select>
              </div>
            </div>

            <div className="pt-3 flex items-center justify-end gap-3 border-t border-[#DEE2E6]">
              <button
                type="button"
                onClick={() => setIsCreating(false)}
                className="px-4 py-2 text-xs font-bold text-[#6C757D] hover:text-[#212529]"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-6 py-2.5 bg-[#714B67] text-white text-xs font-bold rounded-xl shadow-sm hover:bg-[#5C3D54] transition-all"
              >
                Create & Authorize Account
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Main Table Container */}
      <div className="bg-white rounded-2xl border border-[#DEE2E6] shadow-sm overflow-hidden">
        {/* Filter Controls */}
        <div className="p-4 border-b border-[#DEE2E6] bg-[#FAFAFA] flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            {[
              { id: 'ALL', label: 'All Roles' },
              { id: 'sales_rep', label: 'Sales Reps' },
              { id: 'manager', label: 'Managers' },
              { id: 'finance', label: 'Finance' },
              { id: 'admin', label: 'Admins' },
              { id: 'customer', label: 'Customers' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setRoleFilter(tab.id)}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  roleFilter === tab.id
                    ? 'bg-[#212529] text-white'
                    : 'bg-white border border-[#DEE2E6] text-[#4A4A4A] hover:bg-slate-100'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="relative w-full md:w-72">
            <span className="material-symbols-outlined absolute left-3 top-2.5 text-[#6C757D] text-lg">
              search
            </span>
            <input
              type="text"
              placeholder="Search user name or email..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full h-10 pl-9 pr-3 rounded-xl border border-[#DEE2E6] text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
            />
          </div>
        </div>

        {loading ? (
          <div className="p-16 flex flex-col items-center justify-center gap-3">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#714B67]"></div>
            <span className="text-xs text-[#6C757D] font-semibold">Loading system users...</span>
          </div>
        ) : filteredUsers.length === 0 ? (
          <div className="p-12 text-center text-sm text-[#6C757D]">
            No user accounts match the selected criteria.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#4A4A4A]">
              <thead className="bg-[#FAFAFA] text-xs uppercase text-[#6C757D] border-b border-[#DEE2E6]">
                <tr>
                  <th className="px-6 py-3.5 font-bold">User Identity</th>
                  <th className="px-6 py-3.5 font-bold">Role & Permissions</th>
                  <th className="px-6 py-3.5 font-bold">Assigned Tier</th>
                  <th className="px-6 py-3.5 font-bold">Status</th>
                  <th className="px-6 py-3.5 font-bold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#DEE2E6]">
                {filteredUsers.map((user) => (
                  <tr key={user.id} className="hover:bg-[#FAFAFA] transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-xl bg-[#F8F4F7] text-[#714B67] flex items-center justify-center font-extrabold text-sm border border-[#EFE6ED]">
                          {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
                        </div>
                        <div>
                          <div className="font-bold text-[#212529]">{user.name}</div>
                          <div className="text-xs text-[#6C757D] font-mono">{user.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider ${
                          user.role === 'admin'
                            ? 'bg-purple-50 text-purple-700 border border-purple-200'
                            : user.role === 'manager'
                            ? 'bg-[#F8F4F7] text-[#5C3D54] border border-[#E0CEDB]'
                            : user.role === 'finance'
                            ? 'bg-amber-50 text-amber-700 border border-amber-200'
                            : user.role === 'customer'
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : 'bg-slate-100 text-slate-700 border border-slate-200'
                        }`}
                      >
                        {user.role.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-xs font-semibold text-[#212529]">
                      <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                        {user.tier || 'Enterprise'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold ${
                          user.status === 'INACTIVE'
                            ? 'bg-rose-50 text-rose-700'
                            : 'bg-emerald-50 text-emerald-700'
                        }`}
                      >
                        {user.status || 'ACTIVE'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => openEditModal(user)}
                          className="px-3 py-1.5 rounded-lg border border-[#DEE2E6] bg-white text-xs font-bold text-[#714B67] hover:bg-[#F8F4F7] hover:border-[#E0CEDB] transition-all flex items-center gap-1"
                        >
                          <span className="material-symbols-outlined text-sm">edit</span>
                          Edit
                        </button>
                        {user.id !== currentUser.id && user.id !== 'admin_1' && user.id !== 'alex_admin' && (
                          <button
                            onClick={() => setDeleteConfirmUser(user)}
                            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                            title="Deactivate / Delete"
                          >
                            <span className="material-symbols-outlined text-[18px]">delete</span>
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal: Edit User */}
      {editingUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
          <div className="bg-white w-full max-w-md rounded-2xl shadow-xl border border-[#DEE2E6] overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-6 border-b border-[#DEE2E6] flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-[#212529]">Edit User Account</h3>
                <p className="text-xs text-[#6C757D] mt-0.5">Modify role, tier, and status permissions.</p>
              </div>
              <button onClick={() => setEditingUser(null)} className="text-slate-400 hover:text-slate-700">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleUpdateUser} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  value={editForm.name}
                  onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Email Address</label>
                <input
                  type="email"
                  required
                  value={editForm.email}
                  onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">System Role</label>
                  <select
                    value={editForm.role}
                    onChange={(e) => setEditForm({ ...editForm, role: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  >
                    <option value="sales_rep">Sales Representative</option>
                    <option value="manager">Sales Manager</option>
                    <option value="finance">Finance Manager</option>
                    <option value="admin">System Administrator</option>
                    <option value="customer">Customer</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Commercial Tier</label>
                  <select
                    value={editForm.tier}
                    onChange={(e) => setEditForm({ ...editForm, tier: e.target.value })}
                    className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                  >
                    <option value="Enterprise">Enterprise</option>
                    <option value="Strategic">Strategic</option>
                    <option value="Standard">Standard</option>
                    <option value="Gold">Gold</option>
                    <option value="Silver">Silver</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#4A4A4A] mb-1">Account Status</label>
                <select
                  value={editForm.status}
                  onChange={(e) => setEditForm({ ...editForm, status: e.target.value })}
                  className="w-full h-10 px-3 rounded-xl border border-[#DEE2E6] text-sm focus:ring-2 focus:ring-[#714B67]/20 focus:border-[#714B67]"
                >
                  <option value="ACTIVE">ACTIVE</option>
                  <option value="INACTIVE">INACTIVE</option>
                </select>
              </div>

              <div className="pt-4 flex items-center justify-end gap-3 border-t border-[#DEE2E6]">
                <button
                  type="button"
                  onClick={() => setEditingUser(null)}
                  className="px-4 py-2 text-xs font-bold text-[#6C757D] hover:text-[#212529]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-[#714B67] text-white text-xs font-bold hover:bg-[#5C3D54] shadow-sm transition-all"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Delete User Confirmation */}
      {deleteConfirmUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
          <div className="bg-white w-full max-w-md rounded-2xl shadow-xl border border-[#DEE2E6] p-6 animate-in zoom-in-95 duration-200">
            <div className="flex items-center gap-3 text-rose-600 mb-3">
              <span className="material-symbols-outlined text-2xl">warning</span>
              <h3 className="text-lg font-bold text-[#212529]">Deactivate User Account</h3>
            </div>
            <p className="text-sm text-[#4A4A4A]">
              Are you sure you want to remove <strong className="text-[#212529]">{deleteConfirmUser.name}</strong> ({deleteConfirmUser.email})? This action will be recorded in the system audit log.
            </p>
            <div className="mt-6 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setDeleteConfirmUser(null)}
                className="px-4 py-2 text-xs font-bold text-[#6C757D] hover:text-[#212529]"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDeleteUser}
                className="px-5 py-2.5 rounded-xl bg-rose-600 text-white text-xs font-bold hover:bg-rose-700 shadow-sm transition-all"
              >
                Confirm Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
