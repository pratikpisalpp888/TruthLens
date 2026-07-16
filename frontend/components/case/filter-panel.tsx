'use client'

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
