import os

files = {
    "components/shared/stat-card.tsx": """import { motion } from 'framer-motion'
import { LucideIcon } from 'lucide-react'

interface StatCardProps {
  title: string
  value: string | number
  change?: string
  icon: LucideIcon
  iconColor?: string
  subtext?: string
  trend?: 'up' | 'down' | 'neutral'
  className?: string
  onClick?: () => void
}

export function StatCard({ title, value, change, icon: Icon, iconColor = 'text-primary', subtext, trend, className = '', onClick }: StatCardProps) {
  const trendColor = trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-slate-500'
  
  return (
    <motion.div 
      whileHover={{ y: -4, boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)' }}
      className={`bg-white rounded-xl p-6 shadow-sm border border-slate-100 transition-all ${onClick ? 'cursor-pointer' : ''} ${className}`}
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-full bg-slate-50 ${iconColor} bg-opacity-10`}>
          <Icon className={`w-6 h-6 ${iconColor}`} />
        </div>
        {change && (
          <span className={`text-xs font-semibold ${trendColor} bg-${trend === 'up' ? 'green' : 'red'}-50 px-2 py-1 rounded-full`}>
            {change}
          </span>
        )}
      </div>
      <h3 className="text-3xl font-bold text-slate-900 mb-1">{value}</h3>
      <p className="text-sm font-medium text-slate-500">{title}</p>
      {subtext && <p className="text-xs text-slate-400 mt-2">{subtext}</p>}
    </motion.div>
  )
}
""",
    "components/shared/risk-badge.tsx": """import { ShieldAlert, ShieldCheck, Shield } from 'lucide-react'

interface RiskBadgeProps {
  risk: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | string
  className?: string
}

export function RiskBadge({ risk, className = '' }: RiskBadgeProps) {
  const upperRisk = risk.toUpperCase()
  
  if (upperRisk === 'LOW') {
    return (
      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 ${className}`}>
        <ShieldCheck className="w-3.5 h-3.5" /> Low Risk
      </span>
    )
  }
  
  if (upperRisk === 'MEDIUM') {
    return (
      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800 ${className}`}>
        <Shield className="w-3.5 h-3.5" /> Medium Risk
      </span>
    )
  }
  
  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 ${className}`}>
      <ShieldAlert className="w-3.5 h-3.5" /> {upperRisk} RISK
    </span>
  )
}
""",
    "components/shared/status-badge.tsx": """interface StatusBadgeProps {
  status: string
  className?: string
}

export function StatusBadge({ status, className = '' }: StatusBadgeProps) {
  const normalized = status.toLowerCase()
  
  let bg = 'bg-slate-100'
  let text = 'text-slate-800'
  let dot = 'bg-slate-400'
  let isAnimated = false

  if (normalized.includes('analyzing') || normalized.includes('processing')) {
    bg = 'bg-blue-50'
    text = 'text-blue-700'
    dot = 'bg-blue-500'
    isAnimated = true
  } else if (normalized.includes('approved') || normalized.includes('analyzed')) {
    bg = 'bg-emerald-50'
    text = 'text-emerald-700'
    dot = 'bg-emerald-500'
  } else if (normalized.includes('flagged') || normalized.includes('rejected') || normalized.includes('error')) {
    bg = 'bg-red-50'
    text = 'text-red-700'
    dot = 'bg-red-500'
  } else if (normalized.includes('pending') || normalized.includes('needs')) {
    bg = 'bg-amber-50'
    text = 'text-amber-700'
    dot = 'bg-amber-500'
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${bg} ${text} ${className}`}>
      <span className="relative flex h-2 w-2">
        {isAnimated && <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${dot}`}></span>}
        <span className={`relative inline-flex rounded-full h-2 w-2 ${dot}`}></span>
      </span>
      {status}
    </span>
  )
}
""",
    "components/shared/trust-score-gauge.tsx": """interface TrustScoreGaugeProps {
  score: number | null
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
}

export function TrustScoreGauge({ score, size = 'md', showLabel = false }: TrustScoreGaugeProps) {
  const dimensions = {
    sm: { width: 40, strokeWidth: 3, text: 'text-xs' },
    md: { width: 64, strokeWidth: 4, text: 'text-sm' },
    lg: { width: 96, strokeWidth: 6, text: 'text-2xl' },
  }
  
  const dim = dimensions[size]
  const radius = (dim.width - dim.strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  
  if (score === null || score === undefined) {
    return (
      <div className={`flex items-center justify-center rounded-full bg-slate-100 text-slate-400 ${dim.text} font-medium`} style={{ width: dim.width, height: dim.width }}>
        -/-
      </div>
    )
  }
  
  const offset = circumference - (score / 100) * circumference
  
  let colorClass = 'text-green-500'
  let label = 'LOW RISK'
  if (score < 40) { colorClass = 'text-red-500'; label = 'HIGH RISK' }
  else if (score < 75) { colorClass = 'text-amber-500'; label = 'MEDIUM RISK' }

  return (
    <div className="flex flex-col items-center">
      <div className="relative flex items-center justify-center" style={{ width: dim.width, height: dim.width }}>
        {/* Background circle */}
        <svg className="transform -rotate-90 absolute" width={dim.width} height={dim.width}>
          <circle
            cx={dim.width / 2} cy={dim.width / 2} r={radius}
            fill="transparent"
            stroke="currentColor"
            strokeWidth={dim.strokeWidth}
            className="text-slate-100"
          />
        </svg>
        {/* Foreground circle */}
        <svg className="transform -rotate-90 absolute" width={dim.width} height={dim.width}>
          <circle
            cx={dim.width / 2} cy={dim.width / 2} r={radius}
            fill="transparent"
            stroke="currentColor"
            strokeWidth={dim.strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className={`${colorClass} transition-all duration-1000 ease-out`}
          />
        </svg>
        <span className={`font-bold text-slate-800 ${dim.text}`}>{score}</span>
      </div>
      {showLabel && <span className={`mt-2 text-xs font-bold tracking-wider ${colorClass}`}>{label}</span>}
    </div>
  )
}
""",
    "components/case/alert-card.tsx": """import { Clock, ExternalLink, AlertTriangle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'

interface AlertCardProps {
  caseId: string
  applicantName: string
  loanType: string
  loanAmount: string
  score: number
  risk: 'HIGH' | 'MEDIUM'
  findings: string[]
  timeAgo: string
}

export function AlertCard({ caseId, applicantName, loanType, loanAmount, score, risk, findings, timeAgo }: AlertCardProps) {
  const isHigh = risk === 'HIGH'
  
  return (
    <div className={`bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden relative flex flex-col md:flex-row`}>
      {/* Risk colored left border */}
      <div className={`w-1.5 md:w-2 absolute left-0 top-0 bottom-0 ${isHigh ? 'bg-red-500' : 'bg-amber-500'}`}></div>
      
      <div className="p-5 flex-1 flex flex-col md:flex-row gap-6 ml-2">
        {/* Main Info */}
        <div className="flex-1 space-y-3">
          <div className="flex justify-between items-start">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-mono text-slate-500">{caseId}</span>
                <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-${isHigh ? 'red' : 'amber'}-100 text-${isHigh ? 'red' : 'amber'}-700`}>
                  {risk} RISK
                </span>
              </div>
              <h3 className="text-lg font-bold text-slate-900">{applicantName}</h3>
              <p className="text-sm font-medium text-slate-600">{loanType} • {loanAmount}</p>
            </div>
          </div>
          
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
            <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2 flex items-center gap-1">
              <AlertTriangle className="w-3.5 h-3.5" /> Key Findings
            </h4>
            <ul className="text-sm text-slate-600 space-y-1.5 list-disc list-inside">
              {findings.map((finding, idx) => (
                <li key={idx}>{finding}</li>
              ))}
            </ul>
          </div>
        </div>
        
        {/* Score & Actions */}
        <div className="flex flex-row md:flex-col items-center md:items-end justify-between border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-6 min-w-[160px]">
          <div className="flex items-center gap-4 md:flex-col md:items-end md:gap-1 mb-4">
            <TrustScoreGauge score={score} size="md" />
            <div className="flex items-center gap-1 text-xs text-slate-400 mt-2">
              <Clock className="w-3.5 h-3.5" /> {timeAgo}
            </div>
          </div>
          
          <div className="flex flex-col gap-2 w-full md:w-auto">
            <Button size="sm" className="w-full bg-primary hover:bg-primary/90 text-white shadow-sm">
              Review Now
            </Button>
            <Button size="sm" variant="outline" className="w-full text-slate-600">
              View Details <ExternalLink className="w-3.5 h-3.5 ml-1" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
""",
    "components/admin/service-status-card.tsx": """import { motion } from 'framer-motion'
import { LucideIcon, CheckCircle2, AlertCircle, XCircle } from 'lucide-react'

interface ServiceStatusCardProps {
  name: string
  status: 'healthy' | 'degraded' | 'down'
  details: { label: string; value: string }[]
  icon: LucideIcon
}

export function ServiceStatusCard({ name, status, details, icon: Icon }: ServiceStatusCardProps) {
  let border = 'border-slate-200'
  let bg = 'bg-white'
  let StatusIcon = CheckCircle2
  let statusColor = 'text-emerald-500'
  let statusText = 'Healthy'

  if (status === 'degraded') {
    border = 'border-amber-200'
    bg = 'bg-amber-50'
    StatusIcon = AlertCircle
    statusColor = 'text-amber-500'
    statusText = 'Degraded'
  } else if (status === 'down') {
    border = 'border-red-200'
    bg = 'bg-red-50'
    StatusIcon = XCircle
    statusColor = 'text-red-500'
    statusText = 'Down'
  }

  return (
    <motion.div whileHover={{ y: -2 }} className={`rounded-xl p-5 border ${border} ${bg} shadow-sm transition-all`}>
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg bg-white shadow-sm border border-slate-100`}>
            <Icon className="w-5 h-5 text-slate-700" />
          </div>
          <h3 className="font-bold text-slate-900">{name}</h3>
        </div>
        <div className={`flex items-center gap-1.5 text-xs font-semibold ${statusColor} bg-white px-2 py-1 rounded-md shadow-sm border border-slate-100`}>
          <StatusIcon className="w-3.5 h-3.5" />
          {statusText}
        </div>
      </div>
      
      <div className="space-y-2 mt-4">
        {details.map((detail, idx) => (
          <div key={idx} className="flex justify-between items-center text-sm">
            <span className="text-slate-500">{detail.label}</span>
            <span className="font-medium text-slate-800">{detail.value}</span>
          </div>
        ))}
      </div>
    </motion.div>
  )
}
""",
    "components/layout/sidebar.tsx": """'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion } from 'framer-motion'
import { Shield, LayoutDashboard, Briefcase, PlusCircle, BarChart3, Fingerprint, Mic, Settings, Users, ClipboardList, LogOut, ChevronLeft, ChevronRight } from 'lucide-react'
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
    { label: 'Analytics', icon: BarChart3, href: '/analytics' },
    { label: 'Fraud Patterns', icon: Fingerprint, href: '/patterns' },
    { label: 'Voice Assistant', icon: Mic, href: '/voice' },
    { label: 'Settings', icon: Settings, href: '/settings' },
  ]

  const adminLinks = [
    { label: 'Admin Dashboard', icon: LayoutDashboard, href: '/admin' },
    { label: 'All Cases', icon: Briefcase, href: '/cases' },
    { label: 'Analytics', icon: BarChart3, href: '/analytics' },
    { label: 'Users', icon: Users, href: '/admin/users' },
    { label: 'Audit Logs', icon: ClipboardList, href: '/audit' },
    { label: 'Fraud Patterns', icon: Fingerprint, href: '/patterns' },
    { label: 'Settings', icon: Settings, href: '/settings' },
  ]

  const links = isAdmin ? adminLinks : officerLinks

  return (
    <motion.aside 
      initial={false}
      animate={{ width: collapsed ? 72 : 260 }}
      className="h-screen bg-white border-r border-slate-200 flex flex-col fixed left-0 top-0 z-40 transition-all duration-300"
    >
      {/* Brand */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-slate-100">
        <Link href={isAdmin ? '/admin' : '/dashboard'} className="flex items-center gap-2 overflow-hidden whitespace-nowrap">
          <div className="bg-primary p-1.5 rounded-lg shrink-0">
            <Shield className="w-5 h-5 text-white" />
          </div>
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
""",
    "components/layout/topbar.tsx": """'use client'

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
""",
    "app/(protected)/layout.tsx": """'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/stores/auth-store'
import { Sidebar } from '@/components/layout/sidebar'
import { Topbar } from '@/components/layout/topbar'
import { Mic } from 'lucide-react'
import { motion } from 'framer-motion'

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  const router = useRouter()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  if (!mounted || !isAuthenticated) return null // Prevent hydration flash

  return (
    <div className="min-h-screen bg-slate-50 flex">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-[72px] md:ml-[260px] transition-all duration-300">
        <Topbar />
        <main className="flex-1 p-6 overflow-x-hidden">
          {children}
        </main>
      </div>

      {/* Floating Voice Assistant Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-full shadow-lg shadow-blue-500/30 flex items-center justify-center z-50 group border border-blue-400/50"
      >
        <span className="absolute inset-0 rounded-full bg-blue-500 opacity-20 group-hover:animate-ping"></span>
        <Mic className="w-6 h-6 relative z-10" />
      </motion.button>
    </div>
  )
}
""",
    "app/(protected)/dashboard/page.tsx": """'use client'

import { motion } from 'framer-motion'
import { useAuthStore } from '@/stores/auth-store'
import { Briefcase, Clock, CheckCircle, Shield, PlusCircle, Upload, Mic, FileText, ChevronRight, MoreVertical } from 'lucide-react'
import { StatCard } from '@/components/shared/stat-card'
import { AlertCard } from '@/components/case/alert-card'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import { RiskBadge } from '@/components/shared/risk-badge'
import { StatusBadge } from '@/components/shared/status-badge'
import { Button } from '@/components/ui/button'

export default function OfficerDashboard() {
  const user = useAuthStore(state => state.user)
  
  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'
  const todayDate = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })

  // Mock data for UI
  const alerts = [
    { id: 'TL-20250115-0847', name: 'Rajesh Kumar', loan: 'Home Loan', amount: '₹45,00,000', score: 18, risk: 'HIGH' as const, findings: ['3 tampering indicators detected', '6 cross-document mismatches', 'Fraud DNA match found'], time: '3 hours ago' },
    { id: 'TL-20250115-0851', name: 'Sunita Devi', loan: 'Personal Loan', amount: '₹28,00,000', score: 62, risk: 'MEDIUM' as const, findings: ['Income mismatch in ITR', 'Suspicious metadata on PAN'], time: '5 hours ago' }
  ]

  const recentCases = [
    { id: 'TL-20250115-0847', name: 'Rajesh Kumar', loan: 'Home Loan', amount: '₹45,00,000', score: 18, risk: 'HIGH', status: 'Analyzed', time: '3h ago' },
    { id: 'TL-20250115-0851', name: 'Sunita Devi', loan: 'Personal Loan', amount: '₹28,00,000', score: 62, risk: 'MEDIUM', status: 'Analyzed', time: '5h ago' },
    { id: 'TL-20250115-0855', name: 'Amit Sharma', loan: 'Business Loan', amount: '₹75,00,000', score: null, risk: 'LOW', status: 'Analyzing', time: 'Now' },
    { id: 'TL-20250114-0834', name: 'Priya Patel', loan: 'Home Loan', amount: '₹52,00,000', score: 89, risk: 'LOW', status: 'Approved', time: '1d ago' },
    { id: 'TL-20250114-0828', name: 'Vikram Kumar', loan: 'Vehicle Loan', amount: '₹15,00,000', score: 91, risk: 'LOW', status: 'Approved', time: '1d ago' },
  ]

  return (
    <div className="space-y-8 max-w-[1600px] mx-auto pb-10">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">
            {greeting}, {user?.full_name || 'Officer'}
          </h1>
          <p className="text-slate-500 mt-1">{todayDate} • <span className="font-medium text-slate-700 capitalize">{user?.role || 'Credit Officer'}</span></p>
        </div>
        <Button className="bg-primary-700 hover:bg-primary-800 text-white rounded-lg shadow-sm">
          <PlusCircle className="w-4 h-4 mr-2" /> New Case
        </Button>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Assigned Cases" value="24" change="+3 this week" trend="up" icon={Briefcase} iconColor="text-blue-600" />
        <StatCard title="Pending Analysis" value="5" subtext="Awaiting your review" icon={Clock} iconColor="text-amber-500" />
        <StatCard title="Analyzed Today" value="12" subtext="3 flagged • 8 approved • 1 rejected" icon={CheckCircle} iconColor="text-emerald-500" />
        <StatCard title="Fraud Prevented (Month)" value="₹1.2 Cr" subtext="From 8 flagged cases" icon={Shield} iconColor="text-purple-600" className="bg-gradient-to-br from-white to-purple-50" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-8">
        
        {/* Main Content Column */}
        <div className="space-y-8">
          
          {/* Priority Alerts */}
          <section>
            <div className="flex justify-between items-end mb-4">
              <div>
                <h2 className="text-xl font-bold text-slate-900">Requires Your Attention</h2>
                <p className="text-sm text-slate-500">High-priority cases needing review</p>
              </div>
              <a href="#" className="text-sm font-medium text-primary hover:underline flex items-center">View All <ChevronRight className="w-4 h-4 ml-1" /></a>
            </div>
            <div className="flex flex-col gap-4">
              {alerts.map((alert) => (
                <AlertCard key={alert.id} caseId={alert.id} applicantName={alert.name} loanType={alert.loan} loanAmount={alert.amount} score={alert.score} risk={alert.risk} findings={alert.findings} timeAgo={alert.time} />
              ))}
            </div>
          </section>

          {/* Recent Cases Table */}
          <section className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center">
              <h2 className="text-lg font-bold text-slate-900">Your Recent Cases</h2>
              <Button variant="outline" size="sm" className="text-slate-600">View All Cases</Button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-slate-500 bg-slate-50 uppercase font-semibold">
                  <tr>
                    <th className="px-6 py-4">Case ID</th>
                    <th className="px-6 py-4">Applicant</th>
                    <th className="px-6 py-4">Amount</th>
                    <th className="px-6 py-4">Trust Score</th>
                    <th className="px-6 py-4">Risk</th>
                    <th className="px-6 py-4">Status</th>
                    <th className="px-6 py-4">Created</th>
                    <th className="px-6 py-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {recentCases.map((c, i) => (
                    <tr key={i} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 font-mono font-medium text-primary-700">{c.id}</td>
                      <td className="px-6 py-4 font-medium text-slate-900">{c.name}<div className="text-xs text-slate-500 font-normal">{c.loan}</div></td>
                      <td className="px-6 py-4 text-slate-700 font-medium">{c.amount}</td>
                      <td className="px-6 py-4"><TrustScoreGauge score={c.score} size="sm" /></td>
                      <td className="px-6 py-4"><RiskBadge risk={c.risk} /></td>
                      <td className="px-6 py-4"><StatusBadge status={c.status} /></td>
                      <td className="px-6 py-4 text-slate-500">{c.time}</td>
                      <td className="px-6 py-4 text-right">
                        <button className="text-slate-400 hover:text-slate-700 p-1"><MoreVertical className="w-5 h-5" /></button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          
          {/* Quick Actions */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <h2 className="text-base font-bold text-slate-900 mb-4">Quick Actions</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-3">
              {[
                { label: 'Create New Case', icon: PlusCircle, color: 'text-primary-600', bg: 'bg-primary-50' },
                { label: 'Upload Documents', icon: Upload, color: 'text-amber-600', bg: 'bg-amber-50' },
                { label: 'Voice Assistant', icon: Mic, color: 'text-purple-600', bg: 'bg-purple-50' },
                { label: 'Generate Report', icon: FileText, color: 'text-emerald-600', bg: 'bg-emerald-50' },
              ].map((act, i) => {
                const Icon = act.icon
                return (
                  <button key={i} className="flex items-center gap-3 p-3 rounded-lg border border-slate-100 hover:border-slate-300 hover:shadow-sm transition-all text-left group bg-white">
                    <div className={`p-2 rounded-md ${act.bg} group-hover:scale-110 transition-transform`}>
                      <Icon className={`w-4 h-4 ${act.color}`} />
                    </div>
                    <span className="font-semibold text-sm text-slate-700">{act.label}</span>
                  </button>
                )
              })}
            </div>
          </div>

          {/* Performance Sidebar */}
          <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl shadow-md border border-slate-700 p-6 text-white">
            <h2 className="text-base font-bold mb-6">Your Performance (This Month)</h2>
            <div className="space-y-5">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300">Cases Handled</span>
                  <span className="font-bold">87</span>
                </div>
                <div className="h-1.5 w-full bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-400 w-[75%] rounded-full"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300">Avg Analysis Time</span>
                  <span className="font-bold text-emerald-400">92s</span>
                </div>
                <div className="h-1.5 w-full bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-400 w-[95%] rounded-full"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300">Detection Accuracy</span>
                  <span className="font-bold">94%</span>
                </div>
                <div className="h-1.5 w-full bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full bg-amber-400 w-[94%] rounded-full"></div>
                </div>
              </div>
            </div>
            <a href="#" className="block text-center mt-6 text-xs text-slate-400 hover:text-white underline">Compare with team average</a>
          </div>
          
        </div>
      </div>
    </div>
  )
}
""",
    "app/(protected)/admin/page.tsx": """'use client'

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
    print("Scaffolded Phase 16 Dashboards and Components.")
