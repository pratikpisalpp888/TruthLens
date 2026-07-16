import { motion } from 'framer-motion'
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

export function StatCard({ title, value, change, icon: Icon, iconColor = 'text-primary-400', subtext, trend, className = '', onClick }: StatCardProps) {
  const trendColor = trend === 'up' ? 'text-emerald-400' : trend === 'down' ? 'text-rose-400' : 'text-slate-400'
  const trendBg = trend === 'up' ? 'bg-emerald-500/10' : trend === 'down' ? 'bg-rose-500/10' : 'bg-slate-500/10'
  
  return (
    <motion.div 
      whileHover={{ y: -6, scale: 1.02 }}
      className={`relative overflow-hidden rounded-2xl p-6 shadow-xl shadow-slate-900/5 border border-white/10 backdrop-blur-md transition-all duration-300 ${onClick ? 'cursor-pointer' : ''} ${className || 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900'}`}
      onClick={onClick}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-50" />
      <div className="relative z-10">
        <div className="flex justify-between items-start mb-5">
          <div className={`p-3.5 rounded-xl bg-white/10 shadow-inner backdrop-blur-md border border-white/5`}>
            <Icon className={`w-6 h-6 ${iconColor}`} />
          </div>
          {change && (
            <span className={`text-xs font-bold ${trendColor} ${trendBg} px-2.5 py-1.5 rounded-full border border-white/5 shadow-sm flex items-center gap-1`}>
              {change}
            </span>
          )}
        </div>
        <h3 className="text-4xl font-extrabold text-white tracking-tight mb-2 drop-shadow-sm">{value}</h3>
        <p className="text-sm font-semibold text-slate-300">{title}</p>
        {subtext && <p className="text-xs text-slate-400 mt-2.5 font-medium">{subtext}</p>}
      </div>
    </motion.div>
  )
}
