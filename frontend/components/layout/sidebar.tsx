'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion } from 'framer-motion'
import { Shield, LayoutDashboard, Briefcase, PlusCircle, BarChart3, Fingerprint, Settings, Users, ClipboardList, LogOut, ChevronLeft, ChevronRight } from 'lucide-react'
import { useAuthStore } from '@/stores/auth-store'

export function Sidebar() {
  const pathname = usePathname()
  const [collapsed, setCollapsed] = useState(false)
  const { user, logout } = useAuthStore()
  const isAdmin = user?.role === 'admin'

  const officerLinks = [
    { label: 'Dashboard', icon: LayoutDashboard, href: '/dashboard' },
    { label: 'My Cases', icon: Briefcase, href: '/cases' },
    { label: 'New Case', icon: PlusCircle, href: '/cases/new' },
    { label: 'ITR Intelligence', icon: Shield, href: '/itr-analysis' },
  ]

  const adminLinks = [
    { label: 'Admin Dashboard', icon: LayoutDashboard, href: '/admin' },
    { label: 'All Cases', icon: Briefcase, href: '/cases' },
    { label: 'Users', icon: Users, href: '/admin/users' },
    { label: 'Audit Logs', icon: ClipboardList, href: '/audit' },
  ]

  const links = isAdmin ? adminLinks : officerLinks

  return (
    <motion.aside 
      initial={false}
      animate={{ width: collapsed ? 72 : 260 }}
      className="h-screen bg-white border-r border-slate-200 flex flex-col z-40 transition-all duration-300 shrink-0"
    >
      {/* Brand */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-slate-100">
        <Link href={isAdmin ? '/admin' : '/dashboard'} className="flex items-center gap-2 overflow-hidden whitespace-nowrap">
          {!collapsed && <span className="text-xl font-bold text-primary-900 tracking-tight">TruthLens</span>}
        </Link>
        <button onClick={() => setCollapsed(!collapsed)} className="text-slate-400 hover:text-primary transition-colors hidden md:block">
          {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
        </button>
      </div>

      {/* Nav Links */}
      <div className="flex-1 overflow-y-auto py-6 px-3 space-y-1">
        {links.map((link) => {
          const isActive = pathname === link.href || (link.href !== '/dashboard' && link.href !== '/admin' && pathname.startsWith(link.href))
          const Icon = link.icon
          
          return (
            <Link key={link.href} href={link.href} title={collapsed ? link.label : ''} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${isActive ? 'bg-primary-50 text-primary-700 font-semibold' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 font-medium'}`}>
              <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-primary-600' : 'text-slate-400'}`} />
              {!collapsed && <span>{link.label}</span>}
            </Link>
          )
        })}
      </div>

      {/* User Profile */}
      <div className="p-4 border-t border-slate-100">
        <div className={`flex items-center ${collapsed ? 'justify-center' : 'justify-between'}`}>
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="w-9 h-9 rounded-full bg-amber-100 flex items-center justify-center shrink-0 border border-amber-200">
              <span className="text-amber-700 font-bold text-sm">
                {user?.full_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
              </span>
            </div>
            {!collapsed && (
              <div className="whitespace-nowrap overflow-hidden">
                <p className="text-sm font-bold text-slate-800 truncate">{user?.full_name || user?.email || 'User'}</p>
                <p className="text-xs text-slate-500 capitalize">{user?.role}</p>
              </div>
            )}
          </div>
          {!collapsed && (
            <button onClick={logout} className="text-slate-400 hover:text-red-500 transition-colors p-2" title="Logout">
              <LogOut className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </motion.aside>
  )
}
