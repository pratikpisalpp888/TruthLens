'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, FileText, CreditCard, Calendar, Phone, Mail, ChevronRight, Save, Info, Loader2 } from 'lucide-react'
import { StepIndicator } from '@/components/shared/step-indicator'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuthStore } from '@/stores/auth-store'

const STEPS = [
  { id: 1, label: 'Applicant Details' },
  { id: 2, label: 'Loan Details' },
  { id: 3, label: 'Property Details' },
  { id: 4, label: 'Review & Submit' }
]

export default function NewCasePage() {
  const router = useRouter()
  const token = useAuthStore(state => state.token)
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  // Form state
  const [form, setForm] = useState({
    // Step 1
    full_name: '',
    pan_number: '',
    aadhaar: '',
    dob: '',
    mobile: '',
    email: '',
    address: '',
    // Step 2
    loan_type: 'Home Loan',
    loan_purpose: 'Purchase',
    loan_amount: '',
    tenure_years: '',
    // Step 3
    property_type: 'Apartment/Flat',
    area_sqft: '',
    market_value: '',
    survey_number: '',
    property_address: '',
  })

  const set = (field: string, value: string) => setForm(prev => ({ ...prev, [field]: value }))

  const loanAmountNum = parseFloat((form.loan_amount || '0').replace(/,/g, '')) || 0
  const tenureMonths = (parseInt(form.tenure_years) || 0) * 12
  const rate = 0.085 / 12
  const emi = tenureMonths > 0
    ? Math.round(loanAmountNum * rate * Math.pow(1 + rate, tenureMonths) / (Math.pow(1 + rate, tenureMonths) - 1))
    : 0
  const totalInterest = emi * tenureMonths - loanAmountNum

  const handleNext = () => setCurrentStep(prev => Math.min(prev + 1, 4))
  const handleBack = () => setCurrentStep(prev => Math.max(prev - 1, 1))

  const handleSubmit = async () => {
    if (!token) return
    setIsSubmitting(true)
    setError('')
    try {
      const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const res = await fetch(`${BASE}/api/v1/cases`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({
          applicant_name: form.full_name,
          pan_number: form.pan_number,
          loan_type: form.loan_type,
          loan_amount: loanAmountNum,
          loan_purpose: form.loan_purpose,
          tenure_years: parseInt(form.tenure_years) || 0,
          mobile: form.mobile,
          email: form.email,
          address: form.address,
          property_type: form.property_type,
        }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Failed to create case')
      }
      const data = await res.json()
      router.push(`/cases/${data.id}/upload`)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
      setIsSubmitting(false)
    }
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
                <Input value={form.full_name} onChange={e => set('full_name', e.target.value)} placeholder="e.g. Ravi Shankar" />
              </div>
              <div className="space-y-2 relative">
                <Label>PAN Number *</Label>
                <div className="relative">
                  <FileText className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input value={form.pan_number} onChange={e => set('pan_number', e.target.value.toUpperCase())} placeholder="ABCDE1234F" className="pl-10 uppercase" />
                </div>
              </div>
              <div className="space-y-2 relative">
                <Label>Aadhaar Number</Label>
                <div className="relative">
                  <CreditCard className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input value={form.aadhaar} onChange={e => set('aadhaar', e.target.value)} placeholder="1234 5678 9012" className="pl-10" />
                </div>
              </div>
              <div className="space-y-2 relative">
                <Label>Date of Birth *</Label>
                <div className="relative">
                  <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input type="date" value={form.dob} onChange={e => set('dob', e.target.value)} className="pl-10" />
                </div>
              </div>
              <div className="space-y-2 relative">
                <Label>Mobile Number *</Label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input value={form.mobile} onChange={e => set('mobile', e.target.value)} placeholder="+91 98765 43210" className="pl-10" />
                </div>
              </div>
              <div className="space-y-2 relative">
                <Label>Email Address</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <Input type="email" value={form.email} onChange={e => set('email', e.target.value)} placeholder="ravi@example.com" className="pl-10" />
                </div>
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label>Full Address *</Label>
                <textarea value={form.address} onChange={e => set('address', e.target.value)} className="w-full bg-white border border-slate-200 rounded-lg p-3 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none resize-none" rows={3} placeholder="Enter residential address..." />
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
                <select value={form.loan_type} onChange={e => set('loan_type', e.target.value)} className="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none">
                  <option>Home Loan</option>
                  <option>Personal Loan</option>
                  <option>Business Loan</option>
                  <option>Vehicle Loan</option>
                  <option>Education Loan</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label>Loan Purpose *</Label>
                <select value={form.loan_purpose} onChange={e => set('loan_purpose', e.target.value)} className="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none">
                  <option>Purchase</option>
                  <option>Construction</option>
                  <option>Renovation</option>
                  <option>Refinance</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label>Loan Amount (₹) *</Label>
                <Input type="text" value={form.loan_amount} onChange={e => set('loan_amount', e.target.value)} placeholder="45,00,000" />
                {loanAmountNum > 0 && (
                  <p className="text-xs text-primary-600 font-medium">
                    {new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(loanAmountNum)}
                  </p>
                )}
              </div>
              <div className="space-y-2">
                <Label>Tenure (Years) *</Label>
                <Input type="number" value={form.tenure_years} onChange={e => set('tenure_years', e.target.value)} placeholder="20" min="1" max="30" />
              </div>

              {emi > 0 && (
                <div className="md:col-span-2 mt-4 bg-primary-50 rounded-xl p-5 border border-primary-100 flex justify-around">
                  <div className="text-center">
                    <p className="text-xs font-semibold text-primary-700 uppercase mb-1">Monthly EMI</p>
                    <p className="text-2xl font-bold text-primary-900">₹{emi.toLocaleString('en-IN')}</p>
                  </div>
                  <div className="w-px bg-primary-200" />
                  <div className="text-center">
                    <p className="text-xs font-semibold text-primary-700 uppercase mb-1">Total Interest</p>
                    <p className="text-2xl font-bold text-primary-900">₹{Math.round(totalInterest).toLocaleString('en-IN')}</p>
                  </div>
                </div>
              )}
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
                <select value={form.property_type} onChange={e => set('property_type', e.target.value)} className="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none">
                  <option>Apartment/Flat</option>
                  <option>Independent House</option>
                  <option>Plot/Land</option>
                  <option>Commercial Property</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label>Area (Sq.ft) *</Label>
                <Input type="number" value={form.area_sqft} onChange={e => set('area_sqft', e.target.value)} placeholder="1200" />
              </div>
              <div className="space-y-2">
                <Label>Market Value (₹) *</Label>
                <Input type="text" value={form.market_value} onChange={e => set('market_value', e.target.value)} placeholder="60,00,000" />
              </div>
              <div className="space-y-2">
                <Label>Survey Number *</Label>
                <Input value={form.survey_number} onChange={e => set('survey_number', e.target.value)} placeholder="Sy. No. 45/2A" />
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label>Property Address *</Label>
                <textarea value={form.property_address} onChange={e => set('property_address', e.target.value)} className="w-full bg-white border border-slate-200 rounded-lg p-3 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none resize-none" rows={3} />
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
            <div className="bg-slate-50 border border-slate-200 p-6 rounded-xl space-y-5">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><span className="text-slate-500">Applicant Name:</span><span className="ml-2 font-bold text-slate-900">{form.full_name || '—'}</span></div>
                <div><span className="text-slate-500">PAN:</span><span className="ml-2 font-mono font-bold text-slate-900">{form.pan_number || '—'}</span></div>
                <div><span className="text-slate-500">Loan Type:</span><span className="ml-2 font-bold text-slate-900">{form.loan_type}</span></div>
                <div><span className="text-slate-500">Amount:</span><span className="ml-2 font-bold text-slate-900">₹{form.loan_amount || '—'}</span></div>
                <div><span className="text-slate-500">Tenure:</span><span className="ml-2 font-bold text-slate-900">{form.tenure_years || '—'} years</span></div>
                <div><span className="text-slate-500">Property:</span><span className="ml-2 font-bold text-slate-900">{form.property_type}</span></div>
              </div>
              <div className="space-y-3 pt-4 border-t border-slate-200">
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
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-lg font-medium">{error}</div>
            )}
          </motion.div>
        )
    }
  }

  return (
    <div className="max-w-[1200px] mx-auto pb-16">
      <div className="mb-6">
        <Link href="/cases" className="text-sm text-slate-500 hover:text-primary flex items-center font-medium transition-colors mb-4 w-max">
          <ArrowLeft className="w-4 h-4 mr-1" /> Back to Cases
        </Link>
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Create New Case</h1>
        <p className="text-slate-500 mt-1">Enter loan application details to start fraud analysis</p>
      </div>

      <StepIndicator steps={STEPS} currentStep={currentStep} />

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-8 mt-12">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8 min-h-[400px] relative">
          <AnimatePresence mode="wait">
            {renderStep()}
          </AnimatePresence>

          <div className="mt-12 pt-6 border-t border-slate-100 flex items-center justify-between">
            {currentStep > 1 ? (
              <Button variant="outline" onClick={handleBack} className="text-slate-600">Back</Button>
            ) : (
              <Button variant="ghost" asChild className="text-slate-500 hover:text-slate-700"><Link href="/cases">Cancel</Link></Button>
            )}

            {currentStep < 4 ? (
              <Button onClick={handleNext} className="bg-primary hover:bg-primary-600 text-white shadow-sm ml-auto">
                Save & Continue <ChevronRight className="w-4 h-4 ml-1" />
              </Button>
            ) : (
              <Button onClick={handleSubmit} disabled={isSubmitting || !form.full_name} className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-md ml-auto text-lg px-8 h-12 gap-2">
                {isSubmitting ? <><Loader2 className="w-5 h-5 animate-spin" /> Creating Case...</> : 'Create Case & Upload Docs'}
              </Button>
            )}
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-blue-50 border border-blue-100 rounded-xl p-5">
            <div className="flex items-center gap-2 font-bold text-blue-900 mb-3">
              <Info className="w-5 h-5 text-blue-600" /> Form Tips
            </div>
            <ul className="space-y-3 text-sm text-blue-800/80 list-disc list-inside">
              <li>Ensure PAN is accurate — it&apos;s the primary key for fraud network matching.</li>
              <li>All required fields are sent to the backend on submission.</li>
              <li>You will upload supporting documents in the next step.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
