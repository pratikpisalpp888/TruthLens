import { Metadata } from "next"
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
