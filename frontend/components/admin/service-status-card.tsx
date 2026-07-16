import { motion } from 'framer-motion'
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
