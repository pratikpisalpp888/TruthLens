'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { PlusCircle, Download, Loader2 } from 'lucide-react'
import { FilterPanel } from '@/components/case/filter-panel'
import { CaseTable } from '@/components/case/case-table'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/auth-store'

interface Stats {
  total: number
  analyzed_today: number
  pending: number
  high_risk: number
}

export default function CasesPage() {
  const token = useAuthStore(state => state.token)
  const [stats, setStats] = useState<Stats>({ total: 0, analyzed_today: 0, pending: 0, high_risk: 0 })
  const [statsLoading, setStatsLoading] = useState(true)

  useEffect(() => {
    async function loadStats() {
      if (!token) return
      try {
        const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        // Fetch total count using the cases API
        const res = await fetch(`${BASE}/api/v1/cases?limit=1`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (res.ok) {
          const data = await res.json()
          const total = data.total || 0
          // Fetch analyzed (status=analyzed)
          const analyzedRes = await fetch(`${BASE}/api/v1/cases?limit=1&status=analyzed`, {
            headers: { Authorization: `Bearer ${token}` }
          })
          const analyzedData = analyzedRes.ok ? await analyzedRes.json() : { total: 0 }
          // Fetch pending
          const pendingRes = await fetch(`${BASE}/api/v1/cases?limit=1&status=created`, {
            headers: { Authorization: `Bearer ${token}` }
          })
          const pendingData = pendingRes.ok ? await pendingRes.json() : { total: 0 }
          // Fetch high risk
          const highRiskRes = await fetch(`${BASE}/api/v1/cases?limit=1&risk_category=high`, {
            headers: { Authorization: `Bearer ${token}` }
          })
          const highRiskData = highRiskRes.ok ? await highRiskRes.json() : { total: 0 }

          setStats({
            total,
            analyzed_today: analyzedData.total || 0,
            pending: pendingData.total || 0,
            high_risk: highRiskData.total || 0,
          })
        }
      } catch (e) {
        console.error('Failed to load stats', e)
      } finally {
        setStatsLoading(false)
      }
    }
    loadStats()
  }, [token])

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-10">

      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-5">
        <div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight flex items-center gap-3">
            Cases
            {statsLoading ? (
              <span className="text-xs font-bold bg-slate-100 text-slate-500 px-3 py-1 rounded-full border border-slate-200 uppercase tracking-wide shadow-sm flex items-center gap-1.5">
                <Loader2 className="w-3 h-3 animate-spin" /> Loading
              </span>
            ) : (
              <span className="text-xs font-bold bg-primary-100 text-primary-700 px-3 py-1 rounded-full border border-primary-200 uppercase tracking-wide shadow-sm">
                {stats.total.toLocaleString()} total
              </span>
            )}
          </h1>
          <p className="text-slate-500 mt-1 font-medium text-sm">Manage and review all forensic loan applications</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" className="text-slate-700 font-semibold shadow-sm border-slate-200 hover:bg-slate-50 transition-all rounded-xl h-11 px-5">
            <Download className="w-4 h-4 mr-2 text-slate-500" /> Export
          </Button>
          <Link href="/cases/new">
            <Button className="bg-gradient-to-r from-primary-700 to-primary-600 hover:from-primary-800 hover:to-primary-700 text-white font-bold shadow-md hover:shadow-lg transition-all rounded-xl h-11 px-6">
              <PlusCircle className="w-5 h-5 mr-2" /> New Case
            </Button>
          </Link>
        </div>
      </div>

      {/* Mini Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-white/70 backdrop-blur-md p-3 rounded-2xl shadow-sm border border-slate-200/60">
        {[
          { label: 'Total Cases', value: statsLoading ? '…' : stats.total.toLocaleString(), color: 'bg-blue-50 text-blue-700 border-blue-100', dot: 'bg-blue-500' },
          { label: 'Analyzed', value: statsLoading ? '…' : stats.analyzed_today.toLocaleString(), color: 'bg-emerald-50 text-emerald-700 border-emerald-100', dot: 'bg-emerald-500' },
          { label: 'Pending Review', value: statsLoading ? '…' : stats.pending.toLocaleString(), color: 'bg-amber-50 text-amber-700 border-amber-100', dot: 'bg-amber-500' },
          { label: 'High Risk', value: statsLoading ? '…' : stats.high_risk.toLocaleString(), color: 'bg-red-50 text-red-700 border-red-100', dot: 'bg-red-500' },
        ].map((s, i) => (
          <div key={i} className={`px-4 py-3 rounded-xl border ${s.color} cursor-pointer hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-between`}>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${s.dot} shadow-sm`} />
              <span className="text-[11px] font-bold uppercase tracking-wider opacity-80">{s.label}</span>
            </div>
            <span className="text-xl font-black">{s.value}</span>
          </div>
        ))}
      </div>

      <div className="flex flex-col md:flex-row gap-6">
        <FilterPanel />
        <CaseTable />
      </div>
    </div>
  )
}
