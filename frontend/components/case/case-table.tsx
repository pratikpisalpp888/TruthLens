'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { MoreVertical, Home, User, Briefcase, Car, GraduationCap, Loader2, RefreshCw, AlertCircle, PlusCircle, Trash2 } from 'lucide-react'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import { RiskBadge } from '@/components/shared/risk-badge'
import { StatusBadge } from '@/components/shared/status-badge'
import { Pagination } from '@/components/shared/pagination'
import { SearchBar } from '@/components/shared/search-bar'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu'
import { useAuthStore } from '@/stores/auth-store'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'

const LOAN_ICONS: Record<string, React.ElementType> = {
  'Home Loan': Home,
  'Personal Loan': User,
  'Business Loan': Briefcase,
  'Vehicle Loan': Car,
  'Education Loan': GraduationCap,
}

interface CaseRow {
  id: string
  case_number: string
  applicant_name: string
  loan_type: string
  loan_amount: number
  risk_score: number | null
  risk_category: string | null
  status: string
  created_at: string | null
}

interface CasesResponse {
  total: number
  cases: CaseRow[]
}

const PER_PAGE = 20

export function CaseTable() {
  const router = useRouter()
  const token = useAuthStore(state => state.token)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [data, setData] = useState<CasesResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchCases = useCallback(async () => {
    if (!token) return
    setLoading(true)
    setError('')
    try {
      const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const params = new URLSearchParams({
        skip: String((page - 1) * PER_PAGE),
        limit: String(PER_PAGE),
      })
      if (search) params.set('search', search)
      const res = await fetch(`${BASE}/api/v1/cases?${params}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) throw new Error(`Failed to load cases (${res.status})`)
      setData(await res.json())
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load cases')
    } finally {
      setLoading(false)
    }
  }, [token, page, search])

  useEffect(() => { fetchCases() }, [fetchCases])

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this case?')) return
    try {
      const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const res = await fetch(`${BASE}/api/v1/cases/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) throw new Error('Failed to delete')
      fetchCases()
    } catch (e) {
      alert('Failed to delete case')
    }
  }

  const formatAmount = (n: number) =>
    '₹' + new Intl.NumberFormat('en-IN').format(n)

  const timeAgo = (iso: string | null) => {
    if (!iso) return '—'
    const diff = Date.now() - new Date(iso).getTime()
    const mins = Math.floor(diff / 60000)
    if (mins < 60) return `${mins}m ago`
    const hrs = Math.floor(mins / 60)
    if (hrs < 24) return `${hrs}h ago`
    return `${Math.floor(hrs / 24)}d ago`
  }

  return (
    <div className="flex-1 flex flex-col bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="p-4 border-b border-slate-100 flex justify-between items-center gap-4 bg-slate-50/50">
        <SearchBar onSearch={(q) => { setSearch(q); setPage(1) }} placeholder="Search by case ID, applicant name..." />
        <div className="flex items-center gap-2">
          <button onClick={fetchCases} className="text-slate-400 hover:text-primary p-1.5 rounded-lg hover:bg-slate-100 transition-colors" title="Refresh">
            <RefreshCw className="w-4 h-4" />
          </button>
          <select className="text-sm border-slate-200 rounded-lg focus:ring-primary focus:border-primary px-2 py-1.5">
            <option>Newest First</option>
            <option>Highest Risk</option>
          </select>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex-1 flex items-center justify-center py-20">
          <div className="flex flex-col items-center gap-3">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
            <p className="text-sm text-slate-500 font-medium">Loading cases...</p>
          </div>
        </div>
      )}

      {/* Error */}
      {!loading && error && (
        <div className="flex-1 flex items-center justify-center py-20">
          <div className="flex flex-col items-center gap-3 text-center">
            <AlertCircle className="w-10 h-10 text-red-400" />
            <p className="text-sm font-semibold text-slate-700">{error}</p>
            <button onClick={fetchCases} className="text-xs text-primary font-semibold underline">Retry</button>
          </div>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && data?.cases.length === 0 && (
        <div className="flex-1 flex items-center justify-center py-24">
          <div className="flex flex-col items-center gap-4 text-center">
            <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center">
              <Briefcase className="w-8 h-8 text-slate-400" />
            </div>
            <div>
              <p className="font-bold text-slate-800 text-lg">No cases yet</p>
              <p className="text-sm text-slate-500 mt-1">Create your first loan case to get started.</p>
            </div>
            <Link href="/cases/new" className="flex items-center gap-2 bg-primary text-white font-semibold text-sm px-5 py-2.5 rounded-xl hover:bg-primary-600 transition-colors shadow-md">
              <PlusCircle className="w-4 h-4" /> Create New Case
            </Link>
          </div>
        </div>
      )}

      {/* Table */}
      {!loading && !error && data && data.cases.length > 0 && (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-500 bg-slate-50 uppercase font-semibold border-b border-slate-100 sticky top-0">
                <tr>
                  <th className="px-6 py-4"><input type="checkbox" className="rounded border-slate-300" /></th>
                  <th className="px-6 py-4">Case ID</th>
                  <th className="px-6 py-4">Applicant</th>
                  <th className="px-6 py-4">Loan Type</th>
                  <th className="px-6 py-4">Amount</th>
                  <th className="px-6 py-4">Trust Score</th>
                  <th className="px-6 py-4">Risk</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4">Created</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                <AnimatePresence>
                  {data.cases.map((c, i) => {
                    const Icon = LOAN_ICONS[c.loan_type] || Briefcase
                    return (
                      <motion.tr
                        key={c.id}
                        initial={{ opacity: 0, y: 6 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.04 }}
                        onClick={() => router.push(`/cases/${c.id}`)}
                        className="hover:bg-slate-50 transition-colors cursor-pointer group"
                      >
                        <td className="px-6 py-4" onClick={e => e.stopPropagation()}><input type="checkbox" className="rounded border-slate-300" /></td>
                        <td className="px-6 py-4 font-mono font-medium text-primary-700 text-xs">{c.case_number}</td>
                        <td className="px-6 py-4">
                          <div className="font-bold text-slate-900">{c.applicant_name}</div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-1.5 text-slate-700 font-medium">
                            <Icon className="w-4 h-4 text-slate-400" /> {c.loan_type}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-slate-900 font-semibold">{formatAmount(c.loan_amount)}</td>
                        <td className="px-6 py-4">
                          <TrustScoreGauge score={c.risk_score ?? null} size="sm" />
                        </td>
                        <td className="px-6 py-4">
                          <RiskBadge risk={(c.risk_category?.toUpperCase() || 'UNKNOWN') as 'HIGH' | 'MEDIUM' | 'LOW' | 'UNKNOWN'} />
                        </td>
                        <td className="px-6 py-4">
                          <StatusBadge status={c.status} />
                        </td>
                        <td className="px-6 py-4 text-slate-500">{timeAgo(c.created_at)}</td>
                        <td className="px-6 py-4 text-right" onClick={e => e.stopPropagation()}>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <button className="text-slate-400 hover:text-slate-700 p-1 rounded hover:bg-slate-100 transition-colors focus:outline-none">
                                <MoreVertical className="w-5 h-5" />
                              </button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuItem 
                                className="text-red-600 focus:bg-red-50 focus:text-red-700 cursor-pointer"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  handleDelete(c.id)
                                }}
                              >
                                <Trash2 className="w-4 h-4 mr-2" /> Delete Case
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </td>
                      </motion.tr>
                    )
                  })}
                </AnimatePresence>
              </tbody>
            </table>
          </div>
          <Pagination total={data.total} page={page} perPage={PER_PAGE} onPageChange={setPage} />
        </>
      )}
    </div>
  )
}
