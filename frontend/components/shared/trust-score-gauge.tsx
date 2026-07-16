interface TrustScoreGaugeProps {
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
