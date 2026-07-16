'use client'

import { useState, useEffect } from 'react'
import { useAuthStore } from '@/stores/auth-store'
import { StatCard } from '@/components/shared/stat-card'
import { ServiceStatusCard } from '@/components/admin/service-status-card'
import { Files, Users, ShieldCheck, Activity, Database, Layers, HardDrive, Brain, Fingerprint } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts'

export default function AdminDashboard() {
  const user = useAuthStore(state => state.user)
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])

  const lineData = [
    { name: 'Mon', total: 400, approved: 240, flagged: 100, rejected: 60 },
    { name: 'Tue', total: 300, approved: 139, flagged: 120, rejected: 41 },
    { name: 'Wed', total: 550, approved: 380, flagged: 100, rejected: 70 },
    { name: 'Thu', total: 480, approved: 300, flagged: 130, rejected: 50 },
    { name: 'Fri', total: 600, approved: 450, flagged: 90, rejected: 60 },
    { name: 'Sat', total: 200, approved: 150, flagged: 40, rejected: 10 },
    { name: 'Sun', total: 150, approved: 120, flagged: 20, rejected: 10 },
  ]

  const pieData = [
    { name: 'Low Risk', value: 65, color: '#10b981' },
    { name: 'Medium Risk', value: 25, color: '#f59e0b' },
    { name: 'High Risk', value: 10, color: '#ef4444' },
  ]
  
  const barData = [
    { name: 'ITR', value: 450 },
    { name: 'Sale Deed', value: 320 },
    { name: 'Bank Stmt', value: 280 },
    { name: 'Land Record', value: 200 },
    { name: 'PAN', value: 500 },
  ]

  const officers = [
    { name: 'Rahul Sharma', status: 'Online', casesToday: 12, totalCases: 245, avgTime: '87s', accuracy: '96%', rating: 5 },
    { name: 'Priya Verma', status: 'Online', casesToday: 15, totalCases: 189, avgTime: '91s', accuracy: '94%', rating: 5 },
    { name: 'Amit Patel', status: 'Offline', casesToday: 8, totalCases: 156, avgTime: '95s', accuracy: '91%', rating: 4 },
    { name: 'Neha Gupta', status: 'Online', casesToday: 10, totalCases: 134, avgTime: '89s', accuracy: '93%', rating: 4 },
  ]

  return (
    <div className="space-y-8 max-w-[1600px] mx-auto pb-10">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">
            Welcome back, {user?.full_name || 'Admin'}
          </h1>
          <p className="text-slate-500 mt-1">System Administrator • <span className="font-medium text-slate-700">{new Date().toLocaleString('en-US')}</span></p>
        </div>
        <div className="flex items-center gap-2 bg-emerald-50 text-emerald-700 px-4 py-2 rounded-full border border-emerald-100 font-semibold text-sm shadow-sm">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          System Healthy
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Total Cases (All Time)" value="1,247" change="+156 this week" trend="up" icon={Files} iconColor="text-blue-600" />
        <StatCard title="Active Officers" value="23" subtext="18 online now" icon={Users} iconColor="text-emerald-500" />
        <StatCard title="Fraud Prevented (Total)" value="₹47.8 Cr" subtext="Since deployment" icon={ShieldCheck} iconColor="text-amber-500" />
        <StatCard title="System Uptime" value="99.97%" subtext="All Systems Operational" icon={Activity} iconColor="text-primary-600" />
      </div>

      {mounted && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chart 1 */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h3 className="text-lg font-bold text-slate-900 mb-6">Case Analysis Trends (7 Days)</h3>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={lineData} margin={{ top: 5, right: 20, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                  <YAxis axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                  <RechartsTooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
                  <Legend iconType="circle" wrapperStyle={{fontSize: '12px'}} />
                  <Line type="monotone" dataKey="total" stroke="#3b82f6" strokeWidth={3} dot={{r: 4, strokeWidth: 2}} activeDot={{r: 6}} />
                  <Line type="monotone" dataKey="approved" stroke="#10b981" strokeWidth={2} />
                  <Line type="monotone" dataKey="flagged" stroke="#f59e0b" strokeWidth={2} />
                  <Line type="monotone" dataKey="rejected" stroke="#ef4444" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          {/* Chart 2 */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h3 className="text-lg font-bold text-slate-900 mb-6">Risk Category Distribution</h3>
            <div className="h-[300px] w-full flex justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value">
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                  <Legend verticalAlign="middle" align="right" layout="vertical" iconType="circle" />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          {/* Chart 3 */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm lg:col-span-2">
            <h3 className="text-lg font-bold text-slate-900 mb-6">Documents Processed by Type</h3>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#f1f5f9" />
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 13, fontWeight: 500}} width={100} />
                  <RechartsTooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
                  <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={24}>
                    {barData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#1E3A8A', '#2563EB', '#3B82F6', '#60A5FA', '#93C5FD'][index % 5]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {/* System Health Section */}
      <section>
        <h2 className="text-xl font-bold text-slate-900 mb-4">System Status</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          <ServiceStatusCard name="Backend API" status="healthy" icon={Activity} details={[{label: 'Response Time', value: '45ms'}]} />
          <ServiceStatusCard name="CockroachDB" status="healthy" icon={Database} details={[{label: 'Nodes Active', value: '5'}, {label: 'Storage', value: '12.4 GB'}]} />
          <ServiceStatusCard name="Qdrant Vector DB" status="healthy" icon={Layers} details={[{label: 'Collections', value: '2'}, {label: 'Vectors Indexed', value: '125,432'}]} />
          <ServiceStatusCard name="MinIO Storage" status="healthy" icon={HardDrive} details={[{label: 'Buckets', value: '3'}, {label: 'Storage Used', value: '2.3 GB'}]} />
          <ServiceStatusCard name="Ollama LLM" status="healthy" icon={Brain} details={[{label: 'Model Loaded', value: 'llama3.1:8b'}, {label: 'Avg Latency', value: '15s'}]} />
          <ServiceStatusCard name="Fraud Patterns" status="healthy" icon={Fingerprint} details={[{label: 'Patterns Loaded', value: '30'}, {label: 'Last Update', value: '2 days ago'}]} />
        </div>
      </section>

      {/* Team Performance Table */}
      <section className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-100">
          <h2 className="text-lg font-bold text-slate-900">Team Performance</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-500 bg-slate-50 uppercase font-semibold">
              <tr>
                <th className="px-6 py-4">Officer Name</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Cases Today</th>
                <th className="px-6 py-4">Total Cases</th>
                <th className="px-6 py-4">Avg Time</th>
                <th className="px-6 py-4">Accuracy</th>
                <th className="px-6 py-4">Rating</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {officers.map((o, i) => (
                <tr key={i} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4 font-bold text-slate-900 flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-xs">{o.name.charAt(0)}</div>
                    {o.name}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-1.5 text-slate-600">
                      <div className={`w-2 h-2 rounded-full ${o.status === 'Online' ? 'bg-emerald-500' : 'bg-slate-300'}`}></div>
                      {o.status}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-slate-700 font-medium">{o.casesToday}</td>
                  <td className="px-6 py-4 text-slate-700 font-medium">{o.totalCases}</td>
                  <td className="px-6 py-4 font-mono text-slate-600">{o.avgTime}</td>
                  <td className="px-6 py-4 text-emerald-600 font-bold">{o.accuracy}</td>
                  <td className="px-6 py-4 text-amber-400 tracking-widest text-lg">{'★'.repeat(o.rating)}{'☆'.repeat(5 - o.rating)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}
