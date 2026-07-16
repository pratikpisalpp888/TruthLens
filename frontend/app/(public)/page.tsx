import { Navigation } from "@/components/landing/navigation"
import { HeroSection } from "@/components/landing/hero-section"
import { MetricsBar } from "@/components/landing/metrics-bar"
import { SolutionFlow } from "@/components/landing/solution-flow"
import { LayersSection } from "@/components/landing/layers-section"
import { AgentsSection } from "@/components/landing/agents-section"
import { CtaSection } from "@/components/landing/cta-section"
import { Footer } from "@/components/landing/footer"

export const metadata = {
  title: "TruthLens - AI-Powered Loan Document Fraud Detection",
  description: "Detect loan document fraud in 90 seconds with AI-powered forensic analysis. Seven intelligence layers, five AI agents, completely offline. Built for Indian banking.",
}

export default function LandingPage() {
  return (
    <>
      <Navigation />
      <main className="flex min-h-screen flex-col w-full">
        <HeroSection />
        <MetricsBar />
        <SolutionFlow />
        <LayersSection />
        <AgentsSection />
        <CtaSection />
      </main>
      <Footer />
    </>
  )
}