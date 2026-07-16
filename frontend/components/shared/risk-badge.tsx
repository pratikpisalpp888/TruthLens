import { ShieldAlert, ShieldCheck, Shield } from 'lucide-react'

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
