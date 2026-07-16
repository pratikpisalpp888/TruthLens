interface StatusBadgeProps {
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
