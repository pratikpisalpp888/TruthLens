'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { motion, AnimatePresence } from 'framer-motion'
import { Mail, Lock, Eye, EyeOff, Loader2, Shield, CheckCircle, ArrowLeft, Info, Fingerprint } from 'lucide-react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { useToast } from '@/hooks/use-toast'
import { useAuthStore } from '@/stores/auth-store'
import { apiClient } from '@/lib/api/client'

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  rememberMe: z.boolean().optional(),
})

type LoginFormValues = z.infer<typeof loginSchema>

export function LoginForm() {
  const router = useRouter()
  const { toast } = useToast()
  const login = useAuthStore(state => state.login)
  const [showPassword, setShowPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')
  const [activeDemo, setActiveDemo] = useState<'officer' | 'admin' | null>(null)

  const { register, handleSubmit, formState: { errors }, setValue } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '', password: '', rememberMe: false }
  })

  const onSubmit = async (data: LoginFormValues) => {
    setIsSubmitting(true)
    setErrorMsg('')
    try {
      const formData = new URLSearchParams()
      formData.append('username', data.email)
      formData.append('password', data.password)
      
      const response = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      
      const { access_token, user } = response.data
      
      login(user, access_token)
      
      toast({
        title: "Authentication Successful",
        description: "Welcome to your forensic workspace.",
        variant: "default",
      })
      
      if (user.role === 'admin') {
        router.push('/admin')
      } else {
        router.push('/dashboard')
      }
      
    } catch (err: any) {
      console.error(err)
      if (err.response?.status === 401) {
        setErrorMsg('Invalid credentials. Please verify your access.')
      } else {
        setErrorMsg('Secure connection failed. Please try again.')
      }
      setValue('password', '')
    } finally {
      setIsSubmitting(false)
    }
  }

  const fillCredentials = (role: 'officer' | 'admin') => {
    setActiveDemo(role)
    setValue('email', `${role}@truthlens.ai`)
    setValue('password', `${role}123`)
  }

  return (
    <div className="flex-1 flex flex-col justify-center px-6 py-8 sm:px-10 bg-white h-full relative overflow-y-auto">
      
      {/* Minimal Back Arrow */}
      <Link href="/" className="absolute top-6 left-6 w-10 h-10 rounded-full bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-400 hover:text-slate-800 hover:bg-slate-100 transition-colors shadow-sm z-10" title="Back to Home">
        <ArrowLeft className="w-5 h-5" />
      </Link>

      <div className="w-full max-w-[400px] mx-auto mt-4">
        {/* Mobile Logo */}
        <div className="lg:hidden flex items-center justify-center gap-2 mb-6">
          <div className="bg-primary p-2 rounded-xl shadow-md">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-black text-primary-900 tracking-tight">TruthLens</span>
        </div>

        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="mb-8 text-center lg:text-left">
          <h1 className="text-3xl font-black text-slate-900 tracking-tight mb-2">Welcome Back</h1>
          <p className="text-sm text-slate-500 font-medium">Authenticate to access your secure portal.</p>
        </motion.div>

        {/* Demo Credentials Box - Compact */}
        <motion.div 
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
          className="mb-8 p-4 bg-slate-50/80 border border-slate-200/60 rounded-xl backdrop-blur-sm"
        >
          <div className="flex items-center gap-2 text-slate-600 font-bold mb-3 text-[10px] uppercase tracking-wider">
            <Fingerprint className="w-3.5 h-3.5 text-primary-500" /> One-Click Access
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button 
              type="button"
              onClick={() => fillCredentials('officer')}
              className={`relative flex flex-col items-start p-2.5 rounded-lg border transition-all duration-300 text-left ${activeDemo === 'officer' ? 'bg-white border-primary-400 shadow-sm ring-1 ring-primary-400/20' : 'bg-white/50 border-slate-200 hover:bg-white hover:border-slate-300 shadow-sm'}`}
            >
              {activeDemo === 'officer' && <div className="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />}
              <span className={`text-[10px] font-bold uppercase tracking-wide mb-0.5 ${activeDemo === 'officer' ? 'text-primary-600' : 'text-slate-500'}`}>Credit Officer</span>
              <span className="text-xs font-mono text-slate-400">officer@truthlens.ai</span>
            </button>
            <button 
              type="button"
              onClick={() => fillCredentials('admin')}
              className={`relative flex flex-col items-start p-2.5 rounded-lg border transition-all duration-300 text-left ${activeDemo === 'admin' ? 'bg-white border-primary-400 shadow-sm ring-1 ring-primary-400/20' : 'bg-white/50 border-slate-200 hover:bg-white hover:border-slate-300 shadow-sm'}`}
            >
               {activeDemo === 'admin' && <div className="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />}
              <span className={`text-[10px] font-bold uppercase tracking-wide mb-0.5 ${activeDemo === 'admin' ? 'text-primary-600' : 'text-slate-500'}`}>System Admin</span>
              <span className="text-xs font-mono text-slate-400">admin@truthlens.ai</span>
            </button>
          </div>
        </motion.div>

        {/* Error Alert */}
        <AnimatePresence>
          {errorMsg && (
            <motion.div initial={{ opacity: 0, height: 0, marginBottom: 0 }} animate={{ opacity: 1, height: 'auto', marginBottom: 20 }} exit={{ opacity: 0, height: 0, marginBottom: 0 }} className="overflow-hidden">
              <div className="p-3 bg-red-50 border border-red-100 rounded-lg flex items-center gap-2 text-red-600 text-xs font-semibold">
                <Info className="w-4 h-4 shrink-0" />
                {errorMsg}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <motion.form 
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}
          onSubmit={handleSubmit(onSubmit)} className="space-y-5"
        >
          {/* Email */}
          <div className="space-y-1.5">
            <Label htmlFor="email" className="text-slate-700 font-bold text-xs">Corporate Email</Label>
            <div className="relative group">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none transition-colors group-focus-within:text-primary-500">
                <Mail className="h-4 w-4 text-slate-400 group-focus-within:text-primary-500 transition-colors" />
              </div>
              <Input
                id="email"
                type="email"
                placeholder="name@bank.com"
                className={`pl-10 h-11 bg-white border-slate-200 rounded-lg text-sm shadow-sm focus:bg-white focus:ring-2 focus:ring-primary-500/10 focus:border-primary-400 transition-all ${errors.email ? 'border-red-400 focus:border-red-400 focus:ring-red-400/20' : ''}`}
                {...register('email')}
              />
            </div>
            {errors.email && <p className="text-[11px] font-semibold text-red-500 mt-1 ml-1">{errors.email.message}</p>}
          </div>

          {/* Password */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <Label htmlFor="password" className="text-slate-700 font-bold text-xs">Security Key</Label>
              <Link href="/forgot-password" className="text-[11px] font-bold text-primary-600 hover:text-primary-700 hover:underline transition-colors">
                Reset
              </Link>
            </div>
            <div className="relative group">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Lock className="h-4 w-4 text-slate-400 group-focus-within:text-primary-500 transition-colors" />
              </div>
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                className={`pl-10 pr-10 h-11 bg-white border-slate-200 rounded-lg text-sm shadow-sm focus:bg-white focus:ring-2 focus:ring-primary-500/10 focus:border-primary-400 transition-all ${errors.password ? 'border-red-400 focus:border-red-400 focus:ring-red-400/20' : ''}`}
                {...register('password')}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-700 transition-colors"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
            {errors.password && <p className="text-[11px] font-semibold text-red-500 mt-1 ml-1">{errors.password.message}</p>}
          </div>

          {/* Submit */}
          <Button 
            type="submit" 
            disabled={isSubmitting} 
            className="w-full h-12 rounded-lg bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-600 hover:to-amber-500 text-primary-950 font-black text-sm shadow-md hover:shadow-lg hover:shadow-amber-500/20 transition-all duration-300 hover:-translate-y-0.5 mt-2"
          >
            {isSubmitting ? (
              <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Authenticating...</>
            ) : "Authenticate & Enter"}
          </Button>
        </motion.form>

        {/* Badges Footer */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }} className="mt-8 flex justify-center gap-4 text-[10px] font-bold uppercase tracking-wider text-slate-400">
          <div className="flex items-center gap-1"><Shield className="w-3 h-3 text-blue-500" /> Bank-grade</div>
          <div className="flex items-center gap-1"><Lock className="w-3 h-3 text-amber-500" /> AES-256</div>
          <div className="flex items-center gap-1"><CheckCircle className="w-3 h-3 text-emerald-500" /> DPDP</div>
        </motion.div>
        
      </div>
    </div>
  )
}
