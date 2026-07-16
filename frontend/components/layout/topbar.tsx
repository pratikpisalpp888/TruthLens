'use client'

import { Search, Bell, Sun, User as UserIcon } from 'lucide-react'
import { useAuthStore } from '@/stores/auth-store'

export function Topbar() {
  const user = useAuthStore(state => state.user)

  return (
    <header className="h-16 bg-white border-b border-slate-200 sticky top-0 z-30 flex items-center justify-between px-6">
      <div className="flex items-center gap-4 flex-1">
        {/* Global Search Placeholder */}
        <div className="hidden md:flex items-center max-w-md w-full bg-slate-50 border border-slate-200 rounded-full px-4 py-2 text-slate-400 focus-within:ring-2 focus-within:ring-primary/20 focus-within:border-primary transition-all">
          <Search className="w-4 h-4 mr-2" />
          <input 
            type="text" 
            placeholder="Search cases, documents, or applicants (Cmd+K)" 
            className="bg-transparent border-none outline-none text-sm w-full text-slate-700 placeholder:text-slate-400"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="text-slate-400 hover:text-slate-600 transition-colors relative">
          <Bell className="w-5 h-5" />
          <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
        </button>
        <button className="text-slate-400 hover:text-slate-600 transition-colors">
          <Sun className="w-5 h-5" />
        </button>
        
        <div className="h-8 w-px bg-slate-200 mx-2"></div>
        
        <div className="flex items-center gap-2 cursor-pointer hover:bg-slate-50 py-1 px-2 rounded-lg transition-colors">
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center border border-primary-200">
            <UserIcon className="w-4 h-4 text-primary-700" />
          </div>
        </div>
      </div>
    </header>
  )
}
