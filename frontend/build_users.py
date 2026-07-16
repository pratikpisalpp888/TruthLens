import os

files = {
    "app/(protected)/admin/users/page.tsx": """'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { UserCircle, Search, Filter, Download, Plus, MoreVertical, ShieldAlert, Mail, Activity, Upload, X, Shield, Users } from 'lucide-react'
import { Button } from '@/components/ui/button'

const USERS_DATA = [
  { id: 'usr-1', name: 'Rahul Sharma', email: 'rahul@canara.bank', empId: 'EMP001', role: 'Officer', dept: 'Retail', branch: 'Pune Main', status: 'Active', cases: 245, lastLogin: '2 min ago' },
  { id: 'usr-2', name: 'Priya Verma', email: 'priya@canara.bank', empId: 'EMP002', role: 'Officer', dept: 'Retail', branch: 'Mumbai HO', status: 'Active', cases: 189, lastLogin: '15 min ago' },
  { id: 'usr-3', name: 'Admin User', email: 'admin@canara.bank', empId: 'EMP003', role: 'Admin', dept: 'IT', branch: 'Head Office', status: 'Active', cases: 0, lastLogin: '1 hour ago' },
  { id: 'usr-4', name: 'John Doe', email: 'john@canara.bank', empId: 'EMP004', role: 'Officer', dept: 'Retail', branch: 'Delhi Main', status: 'Inactive', cases: 87, lastLogin: '30 days ago' },
  { id: 'usr-5', name: 'Sanjay Gupta', email: 'sanjay@canara.bank', empId: 'EMP005', role: 'Officer', dept: 'Mortgage', branch: 'Bangalore East', status: 'Active', cases: 412, lastLogin: '5 mins ago' }
]

export default function UserManagementPage() {
  const [selectedUser, setSelectedUser] = useState<any>(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [search, setSearch] = useState('')

  return (
    <div className="max-w-[1600px] mx-auto pb-20 relative h-[calc(100vh-64px)] overflow-hidden flex flex-col">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-t-2xl shadow-sm border-b border-slate-200 shrink-0">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">User Management</h1>
          <p className="text-sm text-slate-500">Manage bank officers, admins, and their permissions</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="text-right mr-4 border-r border-slate-200 pr-4">
            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Total Active</p>
            <p className="text-lg font-black text-slate-900">21 / 23</p>
          </div>
          <Button variant="outline" className="border-slate-200 text-slate-700 shadow-sm"><Upload className="w-4 h-4 mr-2" /> Import</Button>
          <Button variant="outline" className="border-slate-200 text-slate-700 shadow-sm"><Download className="w-4 h-4 mr-2" /> Export</Button>
          <Button onClick={() => setShowAddModal(true)} className="bg-primary hover:bg-primary-600 shadow-md text-white"><Plus className="w-4 h-4 mr-2" /> Add User</Button>
        </div>
      </div>

      <div className="flex-1 bg-slate-50 flex flex-col overflow-hidden">
        
        {/* Toolbar */}
        <div className="p-4 border-b border-slate-200 bg-white flex justify-between items-center shrink-0">
          <div className="relative w-96">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input type="text" placeholder="Search by name, email, or EMP ID..." className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm outline-none focus:border-primary shadow-sm" value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>
          <div className="flex items-center gap-3">
            <select className="border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 outline-none">
              <option>All Roles</option>
              <option>Officers</option>
              <option>Admins</option>
            </select>
            <select className="border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 outline-none">
              <option>All Status</option>
              <option>Active</option>
              <option>Inactive</option>
            </select>
            <Button variant="outline" className="border-slate-200 text-slate-700 shadow-sm"><Filter className="w-4 h-4 mr-2" /> More Filters</Button>
          </div>
        </div>

        {/* Table */}
        <div className="flex-1 overflow-auto custom-scrollbar">
          <table className="w-full text-left border-collapse min-w-[1200px]">
            <thead className="bg-slate-100 text-xs uppercase tracking-wider text-slate-500 font-bold sticky top-0 z-10 border-b border-slate-200 shadow-sm">
              <tr>
                <th className="p-4 w-12"><input type="checkbox" className="rounded border-slate-300" /></th>
                <th className="p-4 w-72">User</th>
                <th className="p-4 w-32">EMP ID</th>
                <th className="p-4 w-32">Role</th>
                <th className="p-4 w-48">Branch</th>
                <th className="p-4 w-32">Status</th>
                <th className="p-4 w-32 text-right">Cases Handled</th>
                <th className="p-4 w-40 text-right">Last Login</th>
                <th className="p-4 w-16"></th>
              </tr>
            </thead>
            <tbody className="text-sm bg-white divide-y divide-slate-100">
              {USERS_DATA.map((user) => (
                <tr key={user.id} className="hover:bg-slate-50 transition-colors group cursor-pointer" onClick={() => setSelectedUser(user)}>
                  <td className="p-4" onClick={(e) => e.stopPropagation()}><input type="checkbox" className="rounded border-slate-300" /></td>
                  <td className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-slate-500"><UserCircle className="w-5 h-5" /></div>
                      <div>
                        <p className="font-bold text-slate-900">{user.name}</p>
                        <p className="text-xs text-slate-500">{user.email}</p>
                      </div>
                    </div>
                  </td>
                  <td className="p-4 font-mono text-xs text-slate-600">{user.empId}</td>
                  <td className="p-4">
                    <span className={`text-[10px] px-2 py-1 rounded uppercase font-bold tracking-wider ${user.role === 'Admin' ? 'bg-amber-100 text-amber-700 border border-amber-200' : 'bg-blue-100 text-blue-700 border border-blue-200'}`}>{user.role}</span>
                  </td>
                  <td className="p-4 text-slate-600">
                    <p>{user.branch}</p>
                    <p className="text-xs text-slate-400">{user.dept}</p>
                  </td>
                  <td className="p-4">
                    <span className={`flex items-center gap-1.5 text-xs font-bold ${user.status === 'Active' ? 'text-emerald-600' : 'text-red-600'}`}>
                      <div className={`w-2 h-2 rounded-full ${user.status === 'Active' ? 'bg-emerald-500' : 'bg-red-500'}`}></div> {user.status}
                    </span>
                  </td>
                  <td className="p-4 text-right font-bold text-slate-700">{user.cases}</td>
                  <td className="p-4 text-right text-xs text-slate-500">{user.lastLogin}</td>
                  <td className="p-4 text-right" onClick={(e) => e.stopPropagation()}>
                    <button className="p-1 hover:bg-slate-200 rounded text-slate-400 hover:text-slate-700"><MoreVertical className="w-5 h-5" /></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Slide-out User Profile */}
      <AnimatePresence>
        {selectedUser && (
          <motion.div 
            initial={{ x: '100%', opacity: 0 }} 
            animate={{ x: 0, opacity: 1 }} 
            exit={{ x: '100%', opacity: 0 }} 
            transition={{ type: "spring", damping: 25 }}
            className="absolute right-0 top-0 bottom-0 w-[500px] bg-white border-l border-slate-200 shadow-2xl z-20 flex flex-col"
          >
            <div className="p-6 border-b border-slate-200 bg-slate-900 text-white relative">
              <button onClick={() => setSelectedUser(null)} className="absolute top-4 right-4 p-2 hover:bg-slate-700 rounded-full text-slate-300 transition-colors">
                <X className="w-5 h-5" />
              </button>
              
              <div className="flex items-center gap-5 mt-4">
                <div className="w-16 h-16 rounded-full bg-slate-700 flex items-center justify-center border-2 border-slate-600">
                  <UserCircle className="w-10 h-10 text-slate-300" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold">{selectedUser.name}</h2>
                  <p className="text-slate-400 font-mono text-sm mb-2">{selectedUser.email} • {selectedUser.empId}</p>
                  <span className={`text-[10px] px-2 py-0.5 rounded uppercase font-bold tracking-wider ${selectedUser.role === 'Admin' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'}`}>{selectedUser.role}</span>
                </div>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              
              <section className="grid grid-cols-2 gap-4">
                <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Department</p>
                  <p className="font-bold text-slate-900">{selectedUser.dept}</p>
                </div>
                <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Branch</p>
                  <p className="font-bold text-slate-900">{selectedUser.branch}</p>
                </div>
              </section>

              <section>
                <h3 className="text-sm font-bold text-slate-900 mb-3 border-b border-slate-100 pb-2 flex items-center gap-2"><Activity className="w-4 h-4 text-slate-400" /> Recent Activity</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center text-sm border-b border-slate-50 pb-2">
                    <span className="text-slate-600">Cases Processed (Total)</span>
                    <span className="font-bold text-slate-900">{selectedUser.cases}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-b border-slate-50 pb-2">
                    <span className="text-slate-600">Fraud Detection Rate</span>
                    <span className="font-bold text-emerald-600">14.2%</span>
                  </div>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-slate-600">Last Active</span>
                    <span className="font-mono text-slate-500">{selectedUser.lastLogin}</span>
                  </div>
                </div>
              </section>

              <section>
                <h3 className="text-sm font-bold text-slate-900 mb-3 border-b border-slate-100 pb-2 flex items-center gap-2"><Shield className="w-4 h-4 text-slate-400" /> Security Controls</h3>
                <div className="space-y-3">
                  <Button variant="outline" className="w-full justify-start text-slate-700"><Mail className="w-4 h-4 mr-2" /> Send Password Reset Link</Button>
                  <Button variant="outline" className="w-full justify-start text-slate-700"><ShieldAlert className="w-4 h-4 mr-2" /> View Audit Trail for User</Button>
                  {selectedUser.status === 'Active' ? (
                    <Button variant="outline" className="w-full justify-start text-red-600 border-red-200 hover:bg-red-50"><X className="w-4 h-4 mr-2" /> Deactivate Account</Button>
                  ) : (
                    <Button variant="outline" className="w-full justify-start text-emerald-600 border-emerald-200 hover:bg-emerald-50"><X className="w-4 h-4 mr-2" /> Reactivate Account</Button>
                  )}
                </div>
              </section>

            </div>
            
            <div className="p-6 border-t border-slate-200 bg-slate-50 flex gap-3">
              <Button className="flex-1 bg-slate-900 hover:bg-slate-800 text-white">Edit Profile</Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Add User Modal Overlay */}
      {showAddModal && (
        <div className="absolute inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col max-h-full">
            <div className="p-6 border-b border-slate-200 flex justify-between items-center">
              <h2 className="text-xl font-bold text-slate-900">Add New User</h2>
              <button onClick={() => setShowAddModal(false)} className="p-2 hover:bg-slate-100 rounded-full"><X className="w-5 h-5 text-slate-500" /></button>
            </div>
            <div className="p-6 overflow-y-auto space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Full Name</label>
                  <input type="text" placeholder="e.g. Amit Kumar" className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Email Address</label>
                  <input type="email" placeholder="e.g. amit@canara.bank" className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Employee ID</label>
                  <input type="text" placeholder="e.g. EMP123" className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Role</label>
                  <select className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none">
                    <option>Officer</option>
                    <option>Administrator</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Department</label>
                  <input type="text" placeholder="e.g. Retail Loans" className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Branch</label>
                  <input type="text" placeholder="e.g. Mumbai HO" className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none" />
                </div>
              </div>
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 flex items-start gap-3 text-sm text-blue-900 mt-6">
                <Mail className="w-5 h-5 shrink-0 mt-0.5" />
                <p>An email will automatically be sent to the user with a secure link to set their password. The link will expire in 24 hours.</p>
              </div>
            </div>
            <div className="p-6 border-t border-slate-200 bg-slate-50 flex justify-end gap-3">
              <Button variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button className="bg-primary hover:bg-primary-600 text-white">Create User</Button>
            </div>
          </div>
        </div>
      )}

    </div>
  )
}
"""
}

def scaffold():
    for path, content in files.items():
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
if __name__ == "__main__":
    scaffold()
    print("Scaffolded User Management Page.")
