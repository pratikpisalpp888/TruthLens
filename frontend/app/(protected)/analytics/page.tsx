'use client'

import { useState } from 'react'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts'
import { Download, Calendar, Filter, FileText, Shield, TrendingDown, Clock, Target, Users, TrendingUp, Award, Zap, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'

const trendData = [
  { name: 'Jan', total: 800, fraud: 95 },
  { name: 'Feb', total: 950, fraud: 110 },
  { name: 'Mar', total: 1100, fraud: 130 },
  { name: 'Apr', total: 1050, fraud: 145 },
  { name: 'May', total: 1247, fraud: 153 }
]

const riskData = [
  { name: 'Low Risk', value: 65, color: '#10B981' },
  { name: 'Medium Risk', value: 25, color: '#F59E0B' },
  { name: 'High Risk', value: 8, color: '#EF4444' },
  { name: 'Critical', value: 2, color: '#7F1D1D' }
]

const docData = [
  { name: 'ITR', count: 1240 },
  { name: 'Sale Deed', count: 980 },
  { name: 'Bank Stmt', count: 1150 },
  { name: 'Aadhaar', count: 1200 },
  { name: 'PAN', count: 1247 }
]

const processingTimeData = [
  { time: '0-30s', cases: 150 },
  { time: '30-60s', cases: 450 },
  { time: '60-90s', cases: 500 },
  { time: '90-120s', cases: 100 },
  { time: '120s+', cases: 47 }
]

export default function AnalyticsDashboardPage() {
  const [dateRange, setDateRange] = useState('Last 30 Days')

  return (
    <div className="max-w-[1600px] mx-auto pb-20 space-y-6">
      
      {/* Header & Filter Bar */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Analytics Dashboard</h1>
          <p className="text-sm text-slate-500">Fraud detection insights and performance metrics</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="flex items-center bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 cursor-pointer">
            <Calendar className="w-4 h-4 text-slate-500 mr-2" />
            <select className="bg-transparent text-sm font-bold text-slate-700 outline-none cursor-pointer" value={dateRange} onChange={(e) => setDateRange(e.target.value)}>
              <option>Today</option>
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
              <option>Last 90 Days</option>
              <option>This Year</option>
            </select>
          </div>
          <Button variant="outline" className="border-slate-200 text-slate-700 shadow-sm"><Filter className="w-4 h-4 mr-2" /> Filters (2)</Button>
          <Button className="bg-primary hover:bg-primary-600 shadow-md text-white"><Download className="w-4 h-4 mr-2" /> Export</Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {[
          { title: 'Total Cases', value: '1,247', change: '+156', icon: FileText, color: 'blue' },
          { title: 'Fraud Rate', value: '12.3%', change: '-2.1%', icon: Shield, color: 'emerald' },
          { title: 'Money Saved', value: '₹47.8 Cr', change: '+₹8.2 Cr', icon: TrendingDown, color: 'emerald' },
          { title: 'Avg Time', value: '87s', change: '-5s', icon: Clock, color: 'emerald' },
          { title: 'Accuracy', value: '94.2%', change: '+1.3%', icon: Target, color: 'emerald' },
          { title: 'Active Officers', value: '23', sub: '18 online now', icon: Users, color: 'blue' }
        ].map((kpi, i) => (
          <div key={i} className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm hover:shadow-md transition-shadow group cursor-pointer relative overflow-hidden">
            <div className={`absolute top-0 right-0 w-16 h-16 bg-${kpi.color}-500/5 rounded-full blur-xl group-hover:bg-${kpi.color}-500/10 transition-colors`}></div>
            <div className="flex justify-between items-start mb-2 relative z-10">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">{kpi.title}</p>
              <kpi.icon className={`w-4 h-4 text-${kpi.color}-500`} />
            </div>
            <h3 className="text-2xl font-black text-slate-900 mb-1 relative z-10">{kpi.value}</h3>
            {kpi.change ? (
              <p className={`text-xs font-bold relative z-10 ${kpi.change.startsWith('+') && kpi.color === 'emerald' ? 'text-emerald-600' : kpi.change.startsWith('-') && kpi.color === 'emerald' ? 'text-emerald-600' : 'text-blue-600'}`}>
                {kpi.change} vs last month
              </p>
            ) : (
              <p className="text-xs text-slate-500 font-medium relative z-10">{kpi.sub}</p>
            )}
          </div>
        ))}
      </div>

      {/* Main Charts & Insights */}
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
        
        {/* Left Column (Charts) */}
        <div className="xl:col-span-3 space-y-6">
          
          {/* Main Trend Line Chart */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Fraud Detection Trends</h2>
                <p className="text-sm text-slate-500">Total cases vs flagged cases over time</p>
              </div>
            </div>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trendData}>
                  <defs>
                    <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.1}/>
                      <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorFraud" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#EF4444" stopOpacity={0.2}/>
                      <stop offset="95%" stopColor="#EF4444" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748B' }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748B' }} />
                  <Tooltip contentStyle={{ borderRadius: '8px', border: '1px solid #E2E8F0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                  <Legend iconType="circle" />
                  <Area type="monotone" dataKey="total" name="Total Cases" stroke="#3B82F6" strokeWidth={3} fillOpacity={1} fill="url(#colorTotal)" />
                  <Area type="monotone" dataKey="fraud" name="Fraud Detected" stroke="#EF4444" strokeWidth={3} fillOpacity={1} fill="url(#colorFraud)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Risk Distribution Donut */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
              <h2 className="text-lg font-bold text-slate-900 mb-6">Risk Category Distribution</h2>
              <div className="h-[250px] w-full relative">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={riskData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={2} dataKey="value" stroke="none">
                      {riskData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ borderRadius: '8px', border: '1px solid #E2E8F0' }} />
                  </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-3xl font-black text-slate-900">1.2K</span>
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Cases</span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-2 mt-4">
                {riskData.map(item => (
                  <div key={item.name} className="flex items-center gap-2 text-xs font-medium text-slate-700">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                    {item.name} ({item.value}%)
                  </div>
                ))}
              </div>
            </div>

            {/* Processing Time Histogram */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
              <h2 className="text-lg font-bold text-slate-900 mb-6">Processing Time Distribution</h2>
              <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={processingTimeData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                    <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748B' }} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748B' }} />
                    <Tooltip cursor={{ fill: '#F1F5F9' }} contentStyle={{ borderRadius: '8px', border: '1px solid #E2E8F0' }} />
                    <Bar dataKey="cases" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

          </div>
        </div>

        {/* Right Column (Insights Panel) */}
        <div className="space-y-6">
          <div className="bg-gradient-to-b from-slate-900 to-[#0B1121] rounded-2xl p-6 border border-slate-800 shadow-lg text-white">
            <h2 className="text-sm font-bold text-primary-400 uppercase tracking-wider mb-6 flex items-center gap-2">
              <Zap className="w-4 h-4" /> AI Insights
            </h2>
            
            <div className="space-y-4">
              
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-red-500/20 rounded-lg text-red-400 shrink-0"><TrendingUp className="w-4 h-4" /></div>
                  <div>
                    <h3 className="font-bold text-sm mb-1 text-slate-200">Emerging Pattern</h3>
                    <p className="text-xs text-slate-400 leading-relaxed mb-3">Income inflation via bank statement fabrication increased 23% this month.</p>
                    <Button size="sm" className="w-full bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 h-8 text-xs">Investigate Trend</Button>
                  </div>
                </div>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-amber-500/20 rounded-lg text-amber-400 shrink-0"><AlertCircle className="w-4 h-4" /></div>
                  <div>
                    <h3 className="font-bold text-sm mb-1 text-slate-200">System Optimization</h3>
                    <p className="text-xs text-slate-400 leading-relaxed">Average analysis time reduced by 5.2 seconds due to OCR caching.</p>
                  </div>
                </div>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400 shrink-0"><Award className="w-4 h-4" /></div>
                  <div>
                    <h3 className="font-bold text-sm mb-1 text-slate-200">Top Performer</h3>
                    <p className="text-xs text-slate-400 leading-relaxed">Rahul Sharma detected 12 fraud cases with 96% accuracy this month.</p>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
