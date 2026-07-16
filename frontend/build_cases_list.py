import os

files = {
    "components/shared/search-bar.tsx": """'use client'

import { Search, X } from 'lucide-react'
import { useState, useEffect } from 'react'

interface SearchBarProps {
  placeholder?: string
  onSearch: (value: string) => void
}

export function SearchBar({ placeholder = "Search...", onSearch }: SearchBarProps) {
  const [value, setValue] = useState('')

  useEffect(() => {
    const handler = setTimeout(() => {
      onSearch(value)
    }, 300)
    return () => clearTimeout(handler)
  }, [value, onSearch])

  return (
    <div className="relative w-full max-w-md flex items-center">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Search className={`w-4 h-4 text-slate-400 ${value ? 'text-primary animate-pulse' : ''}`} />
      </div>
      <input
        type="text"
        className="block w-full pl-10 pr-10 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all"
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      {value && (
        <button 
          onClick={() => setValue('')} 
          className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
        >
          <X className="w-4 h-4" />
        </button>
      )}
      {!value && (
        <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
          <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono text-slate-400 bg-slate-100 border border-slate-200 rounded">⌘K</kbd>
        </div>
      )}
    </div>
  )
}
""",
    "components/shared/pagination.tsx": """'use client'

import { ChevronLeft, ChevronRight } from 'lucide-react'

interface PaginationProps {
  total: number
  page: number
  perPage: number
  onPageChange: (page: number) => void
}

export function Pagination({ total, page, perPage, onPageChange }: PaginationProps) {
  const totalPages = Math.ceil(total / perPage)
  const start = (page - 1) * perPage + 1
  const end = Math.min(page * perPage, total)

  return (
    <div className="flex items-center justify-between px-4 py-3 border-t border-slate-200 bg-white">
      <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p className="text-sm text-slate-700">
            Showing <span className="font-medium">{start}</span> to <span className="font-medium">{end}</span> of{' '}
            <span className="font-medium">{total}</span> results
          </p>
        </div>
        <div>
          <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button
              onClick={() => onPageChange(page - 1)}
              disabled={page === 1}
              className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-slate-300 bg-white text-sm font-medium text-slate-500 hover:bg-slate-50 disabled:opacity-50"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
            <span className="relative inline-flex items-center px-4 py-2 border border-slate-300 bg-white text-sm font-medium text-slate-700">
              Page {page} of {totalPages}
            </span>
            <button
              onClick={() => onPageChange(page + 1)}
              disabled={page === totalPages}
              className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-slate-300 bg-white text-sm font-medium text-slate-500 hover:bg-slate-50 disabled:opacity-50"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </nav>
        </div>
      </div>
    </div>
  )
}
""",
    "components/case/filter-panel.tsx": """'use client'

import { Filter, X } from 'lucide-react'

export function FilterPanel() {
  return (
    <div className="w-full md:w-64 bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex flex-col gap-6">
      <div className="flex justify-between items-center pb-3 border-b border-slate-100">
        <h3 className="font-bold text-slate-900 flex items-center gap-2"><Filter className="w-4 h-4" /> Filters</h3>
        <button className="text-xs text-primary hover:underline font-medium">Clear All</button>
      </div>

      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-slate-700">Risk Category</h4>
        <div className="space-y-2">
          {['Low Risk', 'Medium Risk', 'High Risk', 'Critical'].map(r => (
            <label key={r} className="flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
              <input type="checkbox" className="rounded border-slate-300 text-primary focus:ring-primary" />
              {r}
            </label>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-slate-700">Status</h4>
        <select className="w-full text-sm border-slate-200 rounded-lg focus:ring-primary focus:border-primary">
          <option>All Statuses</option>
          <option>Analyzing</option>
          <option>Analyzed</option>
          <option>Approved</option>
          <option>Flagged</option>
        </select>
      </div>
      
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-slate-700">Loan Type</h4>
        <div className="space-y-2">
          {['Home Loan', 'Personal Loan', 'Business Loan'].map(r => (
            <label key={r} className="flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
              <input type="checkbox" className="rounded border-slate-300 text-primary focus:ring-primary" />
              {r}
            </label>
          ))}
        </div>
      </div>
    </div>
  )
}
""",
    "components/case/case-table.tsx": """'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { MoreVertical, ExternalLink, Eye, FileText, Download, Trash2, Home, User, Briefcase, Car } from 'lucide-react'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import { RiskBadge } from '@/components/shared/risk-badge'
import { StatusBadge } from '@/components/shared/status-badge'
import { Pagination } from '@/components/shared/pagination'
import { SearchBar } from '@/components/shared/search-bar'

const MOCK_CASES = [
  { id: 'TL-20250115-0847', name: 'Rajesh Kumar', pan: 'ABCXXXXF', type: 'Home Loan', icon: Home, amount: '₹45,00,000', docs: 8, score: 18, risk: 'HIGH', status: 'Analyzed', officer: 'Rahul S.', time: '3h ago' },
  { id: 'TL-20250115-0851', name: 'Sunita Devi', pan: 'XYZXXXXA', type: 'Personal Loan', icon: User, amount: '₹28,00,000', docs: 4, score: 62, risk: 'MEDIUM', status: 'Analyzing', officer: 'Rahul S.', time: '5h ago' },
  { id: 'TL-20250114-0834', name: 'Priya Patel', pan: 'PQRXXXXM', type: 'Business Loan', icon: Briefcase, amount: '₹52,00,000', docs: 12, score: 89, risk: 'LOW', status: 'Approved', officer: 'Rahul S.', time: '1d ago' },
  { id: 'TL-20250114-0828', name: 'Vikram Singh', pan: 'LMNXXXXP', type: 'Vehicle Loan', icon: Car, amount: '₹15,00,000', docs: 5, score: 91, risk: 'LOW', status: 'Approved', officer: 'Neha G.', time: '1d ago' },
]

export function CaseTable() {
  const router = useRouter()
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  
  const handleRowClick = (id: string) => {
    router.push(`/cases/${id}`)
  }

  return (
    <div className="flex-1 flex flex-col bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      
      <div className="p-4 border-b border-slate-100 flex justify-between items-center gap-4 bg-slate-50/50">
        <SearchBar onSearch={setSearch} placeholder="Search by case ID, applicant name, PAN..." />
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-500 font-medium">Sort by:</span>
          <select className="text-sm border-slate-200 rounded-lg focus:ring-primary focus:border-primary">
            <option>Newest First</option>
            <option>Highest Risk</option>
            <option>Loan Amount (High-Low)</option>
          </select>
        </div>
      </div>

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
            {MOCK_CASES.map((c, i) => {
              const Icon = c.icon
              return (
                <tr key={i} onClick={() => handleRowClick(c.id)} className="hover:bg-slate-50 transition-colors cursor-pointer group">
                  <td className="px-6 py-4" onClick={e => e.stopPropagation()}><input type="checkbox" className="rounded border-slate-300" /></td>
                  <td className="px-6 py-4 font-mono font-medium text-primary-700">{c.id}</td>
                  <td className="px-6 py-4">
                    <div className="font-bold text-slate-900">{c.name}</div>
                    <div className="text-xs text-slate-500">{c.pan}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-1.5 text-slate-700 font-medium">
                      <Icon className="w-4 h-4 text-slate-400" /> {c.type}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-slate-900 font-semibold">{c.amount}</td>
                  <td className="px-6 py-4"><TrustScoreGauge score={c.score} size="sm" /></td>
                  <td className="px-6 py-4"><RiskBadge risk={c.risk} /></td>
                  <td className="px-6 py-4"><StatusBadge status={c.status} /></td>
                  <td className="px-6 py-4 text-slate-500">{c.time}</td>
                  <td className="px-6 py-4 text-right" onClick={e => e.stopPropagation()}>
                    <button className="text-slate-400 hover:text-slate-700 p-1 rounded hover:bg-slate-100 transition-colors">
                      <MoreVertical className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      
      <Pagination total={1247} page={page} perPage={25} onPageChange={setPage} />
    </div>
  )
}
""",
    "app/(protected)/cases/page.tsx": """'use client'

import Link from 'next/link'
import { PlusCircle, Upload, Download, List, LayoutGrid, Activity } from 'lucide-react'
import { FilterPanel } from '@/components/case/filter-panel'
import { CaseTable } from '@/components/case/case-table'
import { Button } from '@/components/ui/button'

export default function CasesPage() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-10">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
            Cases
            <span className="text-sm font-semibold bg-primary-100 text-primary-700 px-3 py-1 rounded-full border border-primary-200">1,247 total</span>
          </h1>
          <p className="text-slate-500 mt-1">Manage and review all loan applications</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" className="text-slate-700 shadow-sm">
            <Download className="w-4 h-4 mr-2" /> Export
          </Button>
          <Link href="/cases/new">
            <Button className="bg-gradient-to-r from-primary-700 to-primary-600 hover:from-primary-800 hover:to-primary-700 text-white shadow-md">
              <PlusCircle className="w-4 h-4 mr-2" /> New Case
            </Button>
          </Link>
        </div>
      </div>

      {/* Mini Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-white p-2 rounded-xl shadow-sm border border-slate-200">
        {[
          { label: 'Total Cases', value: '1,247', color: 'bg-blue-50 text-blue-700' },
          { label: 'Analyzed Today', value: '45', color: 'bg-emerald-50 text-emerald-700' },
          { label: 'Pending Review', value: '12', color: 'bg-amber-50 text-amber-700' },
          { label: 'High Risk', value: '23', color: 'bg-red-50 text-red-700' },
        ].map((s, i) => (
          <div key={i} className={`px-4 py-3 rounded-lg ${s.color} cursor-pointer hover:opacity-80 transition-opacity flex items-center justify-between`}>
            <span className="text-sm font-semibold">{s.label}</span>
            <span className="text-xl font-bold">{s.value}</span>
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
    print("Scaffolded Cases List page.")
