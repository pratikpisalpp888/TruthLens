import { Check } from 'lucide-react'

interface StepIndicatorProps {
  steps: { id: number; label: string }[]
  currentStep: number
}

export function StepIndicator({ steps, currentStep }: StepIndicatorProps) {
  return (
    <div className="w-full py-6 mb-8">
      <div className="flex items-center justify-between relative max-w-3xl mx-auto">
        <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-slate-100 rounded-full z-0"></div>
        <div 
          className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-primary transition-all duration-500 ease-out z-0 rounded-full"
          style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
        ></div>
        
        {steps.map((step) => {
          const isCompleted = step.id < currentStep
          const isCurrent = step.id === currentStep
          
          return (
            <div key={step.id} className="relative z-10 flex flex-col items-center gap-2">
              <div 
                className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm border-2 transition-all duration-300 shadow-sm
                  ${isCompleted ? 'bg-emerald-500 border-emerald-500 text-white' : 
                    isCurrent ? 'bg-primary border-primary text-white scale-110 shadow-primary/30' : 
                    'bg-white border-slate-200 text-slate-400'}`}
              >
                {isCompleted ? <Check className="w-5 h-5" /> : step.id}
              </div>
              <span className={`text-xs font-bold uppercase tracking-wider absolute -bottom-6 w-32 text-center
                ${isCurrent ? 'text-primary' : isCompleted ? 'text-emerald-600' : 'text-slate-400'}`}>
                {step.label}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
