'use client'

import { motion } from 'framer-motion'
import { FileSearch, ShieldAlert, GitCompareArrows, FileCheck2, Cpu } from 'lucide-react'
import { AnimatedFeatureCard } from '@/components/ui/feature-card-1'
import { SectionTitle } from '@/components/ui/section-title'

export function AgentsSection() {
  const agents = [
    { 
      index: "01",
      icon: <FileSearch className="w-14 h-14" strokeWidth={1.5} />, 
      name: 'Classifier', 
      role: 'Identifies document types and routes to specialized verifiers',
      color: "blue" as const
    },
    { 
      index: "02",
      icon: <ShieldAlert className="w-14 h-14" strokeWidth={1.5} />, 
      name: 'Forensic Investigator', 
      role: 'Runs multi-technique tamper detection and evidence collection',
      color: "rose" as const
    },
    { 
      index: "03",
      icon: <GitCompareArrows className="w-14 h-14" strokeWidth={1.5} />, 
      name: 'Cross-Reference', 
      role: 'Compares fields across documents and identifies inconsistencies',
      color: "purple" as const
    },
    { 
      index: "04",
      icon: <FileCheck2 className="w-14 h-14" strokeWidth={1.5} />, 
      name: 'Compliance', 
      role: 'Validates against RBI, DPDP, and PMLA regulations with citations',
      color: "teal" as const
    },
    { 
      index: "05",
      icon: <Cpu className="w-14 h-14" strokeWidth={1.5} />, 
      name: 'Decision', 
      role: 'Synthesizes findings into recommendations with explainable reasoning',
      color: "orange" as const
    },
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white relative overflow-hidden">
      {/* Decorative Brand Watermarks */}
      <div className="absolute top-10 -left-20 md:-left-40 opacity-[0.06] pointer-events-none select-none">
        <img 
          src="/canara-bank-icon-trans.png" 
          alt="" 
          className="w-72 md:w-[450px] lg:w-[500px] h-auto object-contain transform rotate-12 blur-[1px]" 
        />
      </div>
      <div className="absolute bottom-10 -right-20 md:-right-40 opacity-[0.08] pointer-events-none select-none">
        <img 
          src="/canara-bank-icon-trans.png" 
          alt="" 
          className="w-80 md:w-[500px] lg:w-[600px] h-auto object-contain transform -rotate-12 blur-[2px]" 
        />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <SectionTitle
          title="Agentic AI Architecture"
          subtitle="Five specialized agents collaborate autonomously through LangGraph orchestration."
          highlight="AI Architecture"
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
          {agents.map((agent, i) => (
            <div key={i} className="flex justify-center">
              <AnimatedFeatureCard
                index={agent.index}
                tag={agent.name}
                title={agent.role}
                icon={agent.icon}
                color={agent.color}
              />
            </div>
          ))}
        </div>
        
        <motion.div 
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
          className="mt-16 text-center text-slate-500 text-sm font-mono bg-slate-50 py-3 rounded-full max-w-xl mx-auto border border-slate-200"
        >
          Powered by CRAG + GraphRAG for verified, contextual AI responses
        </motion.div>
      </div>
    </section>
  )
}
