import { Clock, ExternalLink, AlertTriangle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import Link from 'next/link'

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
            <Link href={`/cases/${caseId}`} className="w-full">
              <Button size="sm" className="w-full bg-primary hover:bg-primary/90 text-white shadow-sm transition-all duration-300 hover:shadow-md">
                Review Now
              </Button>
            </Link>
            <Link href={`/cases/${caseId}`} className="w-full">
              <Button size="sm" variant="outline" className="w-full text-slate-600 hover:bg-slate-50 transition-colors">
                View Details <ExternalLink className="w-3.5 h-3.5 ml-1" />
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
