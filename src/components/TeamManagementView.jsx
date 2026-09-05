import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function TeamManagementView({  currentUser }) {
  const navigate = useNavigate();

  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);

  const [newUser, setNewUser] = useState({
    name: '',
    email: '',
    password: '',
    role: 'sales_rep',
  });
  const [createError, setCreateError] = useState('');
  const [createSuccess, setCreateSuccess] = useState('');

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const data = await api.getAllUsers();
      setUsers(data);
    } catch (err) {
      console.error('Failed to fetch users', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setCreateError('');
    setCreateSuccess('');
    try {
      await api.createUser(newUser);
      setCreateSuccess(`User ${newUser.name} created successfully!`);
      setNewUser({ name: '', email: '', password: '', role: 'sales_rep' });
      setIsCreating(false);
      fetchUsers();
    } catch (err) {
      setCreateError(err.message || 'Failed to create user');
    }
  };

  if (currentUser?.role !== 'admin') {
    return (
      <div className="p-8 text-center text-red-600 font-bold">
        Access Denied. Admins only.
      </div>
    );
  }

  return (
    <div className="max-w-[1440px] mx-auto p-4 lg:p-8 animate-in fade-in">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-extrabold text-[#0b1c30] tracking-tight">Team & User Management</h1>
          <p className="text-sm text-[#45464d] mt-1">Manage system access, roles, and employee accounts.</p>
        </div>
        <button
          onClick={() => setIsCreating(true)}
          className="flex items-center gap-2 px-4 py-2 bg-[#2563eb] text-white text-sm font-bold rounded-lg shadow-sm hover:bg-[#1d4ed8] transition-colors"
        >
          <span className="material-symbols-outlined text-[18px]">person_add</span>
          Add New User
        </button>
      </div>

      {isCreating && (
        <div className="mb-8 bg-white p-6 rounded-xl border border-[#e2e8f0] shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-[#0b1c30]">Create New Account</h2>
            <button onClick={() => setIsCreating(false)} className="text-[#76777d] hover:text-[#0b1c30]">
              <span className="material-symbols-outlined text-[20px]">close</span>
            </button>
          </div>
          <form onSubmit={handleCreateUser} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-[#45464d] mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  value={newUser.name}
                  onChange={e => setNewUser({ ...newUser, name: e.target.value })}
                  className="w-full h-10 px-3 rounded-lg border border-[#e2e8f0] focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb] text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#45464d] mb-1">Email Address</label>
                <input
                  type="email"
                  required
                  value={newUser.email}
                  onChange={e => setNewUser({ ...newUser, email: e.target.value })}
                  className="w-full h-10 px-3 rounded-lg border border-[#e2e8f0] focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb] text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#45464d] mb-1">Password</label>
                <input
                  type="password"
                  required
                  value={newUser.password}
                  onChange={e => setNewUser({ ...newUser, password: e.target.value })}
                  className="w-full h-10 px-3 rounded-lg border border-[#e2e8f0] focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb] text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#45464d] mb-1">System Role</label>
                <select
                  value={newUser.role}
                  onChange={e => setNewUser({ ...newUser, role: e.target.value })}
                  className="w-full h-10 px-3 rounded-lg border border-[#e2e8f0] focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb] text-sm"
                >
                  <option value="sales_rep">Sales Representative</option>
                  <option value="manager">Sales Manager</option>
                  <option value="finance">Finance Manager</option>
                  <option value="customer">Customer</option>
                </select>
              </div>
            </div>
            
            {createError && <p className="text-xs font-semibold text-red-600">{createError}</p>}
            
            <div className="pt-2">
              <button
                type="submit"
                className="px-6 py-2 bg-[#2563eb] text-white text-sm font-bold rounded-lg shadow-sm hover:bg-[#1d4ed8] transition-colors"
              >
                Create Account
              </button>
            </div>
          </form>
        </div>
      )}

      {createSuccess && (
        <div className="mb-6 p-4 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center gap-3 text-emerald-800">
          <span className="material-symbols-outlined text-emerald-600">check_circle</span>
          <span className="text-sm font-semibold">{createSuccess}</span>
        </div>
      )}

      <div className="bg-white rounded-xl border border-[#e2e8f0] shadow-[0_2px_12px_rgba(0,0,0,0.02)] overflow-hidden">
        <div className="p-4 border-b border-[#e2e8f0] bg-[#f8fafc]">
          <h2 className="font-bold text-[#0b1c30]">Active Users</h2>
        </div>
        
        {loading ? (
          <div className="p-12 flex justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2563eb]"></div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#45464d]">
              <thead className="bg-[#f8fafc] text-xs uppercase text-[#76777d] border-b border-[#e2e8f0]">
                <tr>
                  <th className="px-6 py-3 font-bold">User</th>
                  <th className="px-6 py-3 font-bold">Role</th>
                  <th className="px-6 py-3 font-bold">Tier/Status</th>
                  <th className="px-6 py-3 font-bold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#e2e8f0]">
                {users.map(user => (
                  <tr key={user.id} className="hover:bg-[#f8fafc] transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-700">
                          {user.name.charAt(0)}
                        </div>
                        <div>
                          <div className="font-bold text-[#0b1c30]">{user.name}</div>
                          <div className="text-xs text-[#76777d]">{user.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700">
                        {user.role.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-xs font-semibold">
                      {user.tier || 'Standard'}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button className="text-[#2563eb] hover:underline text-xs font-semibold">Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
