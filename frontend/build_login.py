import os

components = {
    "components/auth/branding-panel.tsx": """'use client'

import { motion } from 'framer-motion'
import { Shield, Zap, Brain, FileCheck } from 'lucide-react'

export function BrandingPanel() {
  const features = [
    { icon: Zap, title: "90 Second Analysis", desc: "From upload to complete forensic report" },
    { icon: Shield, title: "Bank-Grade Security", desc: "AES-256 encryption, offline operation" },
    { icon: Brain, title: "Agentic AI", desc: "5 specialized agents analyze every case" },
    { icon: FileCheck, title: "Court-Ready Evidence", desc: "Auto-generated forensic reports" },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.15, delayChildren: 0.3 } },
  }

  const itemVariants = {
    hidden: { opacity: 0, x: 20 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.5 } },
  }

  return (
    <div className="hidden lg:flex w-full h-full bg-gradient-to-br from-primary-900 via-primary-800 to-primary-950 flex-col justify-between p-12 relative overflow-hidden">
      {/* Decorative abstract elements */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl transform translate-x-1/3 -translate-y-1/3 pointer-events-none"></div>
      <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-primary-950/80 to-transparent pointer-events-none z-0"></div>

      {/* Top Branding */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative z-10"
      >
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-white/10 p-2.5 rounded-xl border border-white/20 backdrop-blur-sm">
            <Shield className="w-8 h-8 text-amber-400" />
          </div>
          <span className="text-3xl font-black text-white tracking-tight">TruthLens</span>
        </div>
        <p className="text-primary-200 text-lg font-medium">AI-Powered Fraud Detection</p>
      </motion.div>

      {/* Middle Features */}
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10 max-w-md my-auto"
      >
        <h2 className="text-2xl font-bold text-white mb-8">Why TruthLens?</h2>
        <div className="space-y-6">
          {features.map((f, i) => {
            const Icon = f.icon
            return (
              <motion.div key={i} variants={itemVariants} className="flex gap-4 p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md hover:bg-white/10 transition-colors">
                <div className="w-12 h-12 rounded-full bg-primary-800/50 flex items-center justify-center shrink-0 border border-primary-700">
                  <Icon className="w-6 h-6 text-amber-400" />
                </div>
                <div>
                  <h3 className="font-semibold text-white text-lg">{f.title}</h3>
                  <p className="text-primary-200 text-sm mt-1">{f.desc}</p>
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>

      {/* Bottom Trust Indicators */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.8 }}
        className="relative z-10 flex items-center gap-3 pt-8 border-t border-white/10"
      >
        <div className="flex-1">
          <p className="text-xs text-primary-300 uppercase tracking-widest font-semibold mb-1">Built For</p>
          <p className="text-sm text-white font-medium">Canara Bank SuRaksha Hackathon</p>
        </div>
      </motion.div>
    </div>
  )
}
""",

    "components/auth/login-form.tsx": """'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-form-hooks' // will use react-hook-form
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { motion, AnimatePresence } from 'framer-motion'
import { Mail, Lock, Eye, EyeOff, Loader2, Shield, CheckCircle, ArrowLeft, Copy, Info } from 'lucide-react'
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
  const setAuth = useAuthStore(state => state.setAuth)
  const [showPassword, setShowPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '', password: '', rememberMe: false }
  })

  const onSubmit = async (data: LoginFormValues) => {
    setIsSubmitting(true)
    setErrorMsg('')
    try {
      // Mock API call for now (or real if backend is ready)
      const formData = new URLSearchParams()
      formData.append('username', data.email) // OAuth2 password flow uses username
      formData.append('password', data.password)
      
      const response = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      
      const { access_token, user } = response.data
      
      setAuth(access_token, user)
      
      toast({
        title: "Welcome back!",
        description: "Successfully signed into your account.",
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
        setErrorMsg('Invalid email or password. Please try again.')
      } else {
        setErrorMsg('Unable to connect to server. Please try again later.')
      }
      setValue('password', '')
    } finally {
      setIsSubmitting(false)
    }
  }

  const fillCredentials = (role: 'officer' | 'admin') => {
    setValue('email', `${role}@truthlens.ai`)
    setValue('password', `${role}123`)
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast({ title: "Copied to clipboard", duration: 2000 })
  }

  return (
    <div className="flex-1 flex flex-col justify-center px-6 py-12 sm:px-12 lg:px-24 bg-white h-full relative overflow-y-auto">
      
      {/* Back Link */}
      <Link href="/" className="absolute top-8 left-8 flex items-center text-sm font-medium text-slate-500 hover:text-primary transition-colors">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to Home
      </Link>

      <div className="w-full max-w-[420px] mx-auto">
        {/* Mobile Logo */}
        <div className="lg:hidden flex items-center gap-2 mb-8">
          <div className="bg-primary p-2 rounded-lg">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold text-primary-900 tracking-tight">TruthLens</span>
        </div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <h1 className="text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight mb-2">Welcome Back</h1>
          <p className="text-slate-500 mb-8">Sign in to access your fraud detection portal</p>
        </motion.div>

        {/* Demo Credentials Box */}
        <motion.div 
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
          className="mb-8 p-4 bg-blue-50/50 border border-primary-200 rounded-xl"
        >
          <div className="flex items-center gap-2 text-primary-800 font-semibold mb-3 text-sm">
            <Info className="w-4 h-4" /> Demo Credentials
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Button variant="outline" className="w-full h-auto py-2 flex flex-col gap-1 items-start text-left bg-white hover:bg-slate-50 border-primary-200 shadow-sm" onClick={() => fillCredentials('officer')} type="button">
              <span className="text-xs font-bold text-primary-600 uppercase">Officer</span>
              <span className="text-sm font-mono text-slate-700">officer@truthlens.ai</span>
            </Button>
            <Button variant="outline" className="w-full h-auto py-2 flex flex-col gap-1 items-start text-left bg-white hover:bg-slate-50 border-primary-200 shadow-sm" onClick={() => fillCredentials('admin')} type="button">
              <span className="text-xs font-bold text-primary-600 uppercase">Admin</span>
              <span className="text-sm font-mono text-slate-700">admin@truthlens.ai</span>
            </Button>
          </div>
        </motion.div>

        {/* Error Alert */}
        <AnimatePresence>
          {errorMsg && (
            <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="overflow-hidden mb-6">
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm font-medium">
                {errorMsg}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <motion.form 
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
          onSubmit={handleSubmit(onSubmit)} className="space-y-6"
        >
          {/* Email */}
          <div className="space-y-2 relative">
            <Label htmlFor="email" className="text-slate-700 font-medium">Email Address</Label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail className="h-5 w-5 text-slate-400" />
              </div>
              <Input
                id="email"
                type="email"
                placeholder="officer@bank.com"
                className={`pl-10 h-12 bg-slate-50 border-slate-200 focus:bg-white focus:ring-2 focus:ring-primary-500/20 transition-all ${errors.email ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : ''}`}
                {...register('email')}
              />
            </div>
            {errors.email && <p className="text-sm text-red-500 mt-1">{errors.email.message}</p>}
          </div>

          {/* Password */}
          <div className="space-y-2 relative">
            <Label htmlFor="password" className="text-slate-700 font-medium">Password</Label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-slate-400" />
              </div>
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                className={`pl-10 pr-10 h-12 bg-slate-50 border-slate-200 focus:bg-white focus:ring-2 focus:ring-primary-500/20 transition-all ${errors.password ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : ''}`}
                {...register('password')}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 transition-colors"
              >
                {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
            {errors.password && <p className="text-sm text-red-500 mt-1">{errors.password.message}</p>}
          </div>

          {/* Options */}
          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center space-x-2">
              <Checkbox id="remember" className="border-slate-300 data-[state=checked]:bg-primary" {...register('rememberMe')} />
              <Label htmlFor="remember" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-slate-600 cursor-pointer">
                Remember Me
              </Label>
            </div>
            <Link href="/forgot-password" className="text-sm font-medium text-primary-600 hover:text-primary-700 hover:underline transition-colors">
              Forgot Password?
            </Link>
          </div>

          {/* Submit */}
          <Button 
            type="submit" 
            disabled={isSubmitting} 
            className="w-full h-12 rounded-lg bg-gradient-to-r from-primary-700 to-primary-600 hover:from-primary-800 hover:to-primary-700 text-white font-bold text-lg shadow-lg hover:shadow-xl transition-all"
          >
            {isSubmitting ? (
              <><Loader2 className="mr-2 h-5 w-5 animate-spin" /> Signing in...</>
            ) : "Sign In"}
          </Button>
        </motion.form>

        {/* Badges Footer */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }} className="mt-12 flex justify-center gap-4 text-xs font-medium text-slate-400">
          <div className="flex items-center gap-1.5"><Shield className="w-3.5 h-3.5 text-primary-400" /> Bank-grade</div>
          <div className="w-1 h-1 rounded-full bg-slate-200"></div>
          <div className="flex items-center gap-1.5"><Lock className="w-3.5 h-3.5 text-amber-500" /> AES-256</div>
          <div className="w-1 h-1 rounded-full bg-slate-200"></div>
          <div className="flex items-center gap-1.5"><CheckCircle className="w-3.5 h-3.5 text-green-500" /> DPDP</div>
        </motion.div>
        
        <div className="mt-8 text-center text-sm text-slate-500">
          Not a registered user? <a href="#" className="font-medium text-slate-700 hover:underline">Contact administrator</a>
        </div>
      </div>
    </div>
  )
}
""",

    "app/(public)/login/page.tsx": """import { Metadata } from "next"
import { LoginForm } from "@/components/auth/login-form"
import { BrandingPanel } from "@/components/auth/branding-panel"

export const metadata: Metadata = {
  title: "Sign In - TruthLens",
  description: "Access your TruthLens fraud detection portal. Bank-grade security with AES-256 encryption.",
  robots: {
    index: false,
    follow: false,
  }
}

export default function LoginPage() {
  return (
    <main className="w-full h-screen min-h-[600px] flex overflow-hidden bg-white">
      {/* Left Column: Login Form */}
      <LoginForm />
      
      {/* Right Column: Branding Visuals */}
      <div className="hidden lg:block lg:w-1/2 h-full">
        <BrandingPanel />
      </div>
    </main>
  )
}
"""
}

def scaffold_login_components():
    for path, content in components.items():
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
if __name__ == "__main__":
    scaffold_login_components()
    print("Scaffolded Login components.")
