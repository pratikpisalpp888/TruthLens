import os

files = {
    "components/shared/step-indicator.tsx": """import { Check } from 'lucide-react'

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
""",
    "app/(protected)/cases/new/page.tsx": """'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, FileText, CreditCard, Calendar, Phone, Mail, ChevronRight, Save, Info } from 'lucide-react'
import { StepIndicator } from '@/components/shared/step-indicator'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const STEPS = [
  { id: 1, label: 'Applicant Details' },
  { id: 2, label: 'Loan Details' },
  { id: 3, label: 'Property Details' },
  { id: 4, label: 'Review & Submit' }
]

export default function NewCasePage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleNext = () => setCurrentStep(prev => Math.min(prev + 1, 4))
  const handleBack = () => setCurrentStep(prev => Math.max(prev - 1, 1))
  
  const handleSubmit = () => {
    setIsSubmitting(true)
    setTimeout(() => {
      // Mock submit
      router.push('/cases/TL-20250115-0847/upload')
    }, 1500)
  }

  const renderStep = () => {
    switch(currentStep) {
      case 1:
        return (
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Applicant Details</h2>
              <p className="text-sm text-slate-500">Basic information about the loan applicant</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label>Full Name *</Label>
                <Input placeholder="Rajesh Kumar Sharma" />
              </div>
              <div className="space-y-2 relative">
                <Label>PAN Number *</Label>
                <div className="relative">
                  <FileText className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input placeholder="ABCDE1234F" className="pl-10 uppercase" />
                </div>
              </div>
              <div className="space-y-2 relative">
                <Label>Aadhaar Number</Label>
                <div className="relative">
                  <CreditCard className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input placeholder="1234 5678 9012" className="pl-10" />
                </div>
              </div>
              <div className="space-y-2 relative">
                <Label>Date of Birth *</Label>
                <div className="relative">
                  <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input type="date" className="pl-10" />
                </div>
              </div>
              <div className="space-y-2 relative">
                <Label>Mobile Number *</Label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input placeholder="+91 98765 43210" className="pl-10" />
                </div>
              </div>
              <div className="space-y-2 relative">
                <Label>Email Address</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input type="email" placeholder="rajesh@example.com" className="pl-10" />
                </div>
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label>Full Address *</Label>
                <textarea className="w-full bg-white border border-slate-200 rounded-lg p-3 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none resize-none" rows={3} placeholder="Enter residential address..."></textarea>
              </div>
            </div>
          </motion.div>
        )
      case 2:
        return (
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Loan Application Details</h2>
              <p className="text-sm text-slate-500">Information about the loan being applied for</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label>Loan Type *</Label>
                <select className="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none">
                  <option>Home Loan</option>
                  <option>Personal Loan</option>
                  <option>Business Loan</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label>Loan Purpose *</Label>
                <select className="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none">
                  <option>Purchase</option>
                  <option>Construction</option>
                  <option>Renovation</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label>Loan Amount (₹) *</Label>
                <Input type="text" placeholder="45,00,000" defaultValue="45,00,000" />
                <p className="text-xs text-primary-600 font-medium">Forty-five Lakh Rupees</p>
              </div>
              <div className="space-y-2">
                <Label>Tenure (Years) *</Label>
                <Input type="number" placeholder="20" defaultValue="20" />
              </div>
              
              <div className="md:col-span-2 mt-4 bg-primary-50 rounded-xl p-5 border border-primary-100 flex justify-around">
                <div className="text-center">
                  <p className="text-xs font-semibold text-primary-700 uppercase mb-1">Monthly EMI</p>
                  <p className="text-2xl font-bold text-primary-900">₹40,436</p>
                </div>
                <div className="w-px bg-primary-200"></div>
                <div className="text-center">
                  <p className="text-xs font-semibold text-primary-700 uppercase mb-1">Total Interest</p>
                  <p className="text-2xl font-bold text-primary-900">₹51,04,640</p>
                </div>
              </div>
            </div>
          </motion.div>
        )
      case 3:
        return (
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Property Information</h2>
              <p className="text-sm text-slate-500">Details about the property involved in this loan</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label>Property Type *</Label>
                <select className="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none">
                  <option>Apartment/Flat</option>
                  <option>Independent House</option>
                  <option>Plot/Land</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label>Area (Sq.ft) *</Label>
                <Input type="number" placeholder="1200" />
              </div>
              <div className="space-y-2">
                <Label>Market Value (₹) *</Label>
                <Input type="text" placeholder="60,00,000" />
              </div>
              <div className="space-y-2">
                <Label>Survey Number *</Label>
                <Input placeholder="Sy. No. 45/2A" />
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label>Property Address *</Label>
                <textarea className="w-full bg-white border border-slate-200 rounded-lg p-3 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none resize-none" rows={3}></textarea>
              </div>
            </div>
          </motion.div>
        )
      case 4:
        return (
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Review & Submit</h2>
              <p className="text-sm text-slate-500">Verify all information before creating the case</p>
            </div>
            
            <div className="bg-slate-50 border border-slate-200 p-6 rounded-xl space-y-6">
              <div className="flex justify-between items-center border-b border-slate-200 pb-4">
                <h3 className="font-bold text-slate-800">Generated Case ID</h3>
                <span className="font-mono bg-white px-3 py-1 border border-slate-200 rounded font-bold text-primary-700">TL-20250115-XXXX</span>
              </div>
              
              <div className="space-y-3">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input type="checkbox" className="mt-1 rounded text-primary focus:ring-primary" defaultChecked />
                  <span className="text-sm text-slate-700 font-medium">I confirm all provided information is accurate to the best of my knowledge.</span>
                </label>
                <label className="flex items-start gap-3 cursor-pointer">
                  <input type="checkbox" className="mt-1 rounded text-primary focus:ring-primary" defaultChecked />
                  <span className="text-sm text-slate-700 font-medium">Applicant has explicitly consented to digital fraud analysis (DPDP Act compliance).</span>
                </label>
              </div>
            </div>
          </motion.div>
        )
    }
  }

  return (
    <div className="max-w-[1200px] mx-auto pb-16">
      {/* Header */}
      <div className="mb-6">
        <Link href="/cases" className="text-sm text-slate-500 hover:text-primary flex items-center font-medium transition-colors mb-4 w-max">
          <ArrowLeft className="w-4 h-4 mr-1" /> Back to Cases
        </Link>
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Create New Case</h1>
        <p className="text-slate-500 mt-1">Enter loan application details to start fraud analysis</p>
      </div>

      <StepIndicator steps={STEPS} currentStep={currentStep} />

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-8 mt-12">
        {/* Main Form Area */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8 min-h-[400px] relative">
          <AnimatePresence mode="wait">
            {renderStep()}
          </AnimatePresence>
          
          <div className="mt-12 pt-6 border-t border-slate-100 flex items-center justify-between">
            {currentStep > 1 ? (
              <Button variant="outline" onClick={handleBack} className="text-slate-600">
                Back
              </Button>
            ) : (
              <Button variant="ghost" className="text-slate-500 hover:text-slate-700">Cancel</Button>
            )}
            
            {currentStep < 4 ? (
              <Button onClick={handleNext} className="bg-primary hover:bg-primary-600 text-white shadow-sm ml-auto">
                Save & Continue <ChevronRight className="w-4 h-4 ml-1" />
              </Button>
            ) : (
              <Button onClick={handleSubmit} disabled={isSubmitting} className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-md ml-auto text-lg px-8 h-12">
                {isSubmitting ? 'Creating Case...' : 'Create Case & Upload Docs'}
              </Button>
            )}
          </div>
        </div>

        {/* Info Sidebar */}
        <div className="space-y-4">
          <div className="bg-blue-50 border border-blue-100 rounded-xl p-5">
            <div className="flex items-center gap-2 font-bold text-blue-900 mb-3">
              <Info className="w-5 h-5 text-blue-600" /> Form Tips
            </div>
            <ul className="space-y-3 text-sm text-blue-800/80 list-disc list-inside">
              <li>Ensure PAN is accurate as it's the primary key for fraud network matching.</li>
              <li>Values are auto-saved locally every 30 seconds.</li>
              <li>You will upload supporting documents in the next phase after creation.</li>
            </ul>
          </div>
          
          <Button variant="outline" className="w-full text-slate-600 border-slate-200">
            <Save className="w-4 h-4 mr-2 text-slate-400" /> Save as Draft
          </Button>
        </div>
      </div>
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
    print("Scaffolded New Case Creation page.")
