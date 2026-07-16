'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuthStore } from '@/stores/auth-store'
import { Sidebar } from '@/components/layout/sidebar'
import { Topbar } from '@/components/layout/topbar'
import { Mic } from 'lucide-react'
import { motion } from 'framer-motion'

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  const router = useRouter()
  const pathname = usePathname()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  if (!mounted || !isAuthenticated) return null // Prevent hydration flash

  const isAnalyzePage = pathname?.includes('/analyze') ?? false

  return (
    <div className="h-screen bg-slate-50 flex overflow-hidden font-sans">
      {!isAnalyzePage && <Sidebar />}
      <div className="flex-1 flex flex-col min-w-0 relative z-0 overflow-hidden">
        {!isAnalyzePage && <Topbar />}
        <main className={`flex-1 overflow-y-auto overflow-x-hidden ${isAnalyzePage ? '' : 'p-6 md:p-8'}`}>
          {children}
        </main>
      </div>
    </div>
  )
}
