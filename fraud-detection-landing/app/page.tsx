import { Header } from '@/components/landing/header'
import { HeroSection } from '@/components/landing/hero-section'
import { ProblemStatement } from '@/components/landing/problem-statement'
import { SolutionFlow } from '@/components/landing/solution-flow'
import { IntelligenceLayers } from '@/components/landing/intelligence-layers'
import { AIAgents } from '@/components/landing/ai-agents'
import { SampleAnalysis } from '@/components/landing/sample-analysis'
import { StatsStrip } from '@/components/landing/stats-strip'
import { TrustCompliance } from '@/components/landing/trust-compliance'
import { Footer } from '@/components/landing/footer'

export default function Page() {
  return (
    <main className="w-full bg-background">
      <Header />
      <HeroSection />
      <ProblemStatement />
      <SolutionFlow />
      <IntelligenceLayers />
      <AIAgents />
      <SampleAnalysis />
      <StatsStrip />
      <TrustCompliance />
      <Footer />
    </main>
  )
}
