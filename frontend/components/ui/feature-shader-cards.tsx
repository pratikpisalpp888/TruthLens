"use client"

import type React from "react"
import { motion } from "framer-motion"
import { Scan, Languages, GitCompare, FileText, Dna, BrainCircuit, Gavel } from 'lucide-react'
import { EvervaultCard } from "@/components/ui/evervault-card"
import { Badge } from "@/components/ui/badge"
import { SectionTitle } from "@/components/ui/section-title"

interface Feature {
  title: string
  description: string
  icon: React.ReactNode
  badge?: { text: string; variant: string } | null
  gradientFrom: string
  gradientTo: string
  iconColor: string
  iconBg: string
  iconBorder: string
  index: string
}

const features: Feature[] = [
  {
    title: 'Document Forensics',
    description: 'Error Level Analysis, metadata examination, font anomaly detection, compression analysis, and printer fingerprinting.',
    icon: <Scan className="w-12 h-12" strokeWidth={1.5} />,
    badge: null,
    gradientFrom: 'from-blue-500',
    gradientTo: 'to-cyan-600',
    iconColor: 'text-blue-600',
    iconBg: 'bg-blue-50',
    iconBorder: 'border-blue-200',
    index: '01'
  },
  {
    title: 'Multilingual OCR',
    description: 'PaddleOCR-powered extraction supporting six Indian languages with named entity recognition.',
    icon: <Languages className="w-12 h-12" strokeWidth={1.5} />,
    badge: null,
    gradientFrom: 'from-teal-500',
    gradientTo: 'to-emerald-600',
    iconColor: 'text-teal-600',
    iconBg: 'bg-teal-50',
    iconBorder: 'border-teal-200',
    index: '02'
  },
  {
    title: 'Cross-Document Consistency',
    description: 'Verifies the entire loan application as one truth, catching mismatches between documents that isolated checks miss.',
    icon: <GitCompare className="w-12 h-12" strokeWidth={1.5} />,
    badge: { text: 'Strongest Differentiator', variant: 'default' },
    gradientFrom: 'from-violet-500',
    gradientTo: 'to-purple-700',
    iconColor: 'text-violet-600',
    iconBg: 'bg-violet-50',
    iconBorder: 'border-violet-200',
    index: '03'
  },
  {
    title: 'ITR Special Verification',
    description: 'Five-sub-layer income tax validation covering format, computation, bank cross-reference, visual authentication, and behavioral analysis.',
    icon: <FileText className="w-12 h-12" strokeWidth={1.5} />,
    badge: { text: 'Organizer Focus', variant: 'secondary' },
    gradientFrom: 'from-amber-500',
    gradientTo: 'to-orange-600',
    iconColor: 'text-amber-600',
    iconBg: 'bg-amber-50',
    iconBorder: 'border-amber-200',
    index: '04'
  },
  {
    title: 'Fraud DNA Pattern Matching',
    description: 'Extracts forensic signatures and matches against historical fraud patterns using vector similarity and graph traversal.',
    icon: <Dna className="w-12 h-12" strokeWidth={1.5} />,
    badge: { text: 'Unique', variant: 'destructive' },
    gradientFrom: 'from-rose-500',
    gradientTo: 'to-red-600',
    iconColor: 'text-rose-600',
    iconBg: 'bg-rose-50',
    iconBorder: 'border-rose-200',
    index: '05'
  },
  {
    title: 'Risk Intelligence',
    description: 'Multi-dimensional fraud probability scoring with human-readable explanations and specific regulatory citations.',
    icon: <BrainCircuit className="w-12 h-12" strokeWidth={1.5} />,
    badge: null,
    gradientFrom: 'from-green-500',
    gradientTo: 'to-emerald-700',
    iconColor: 'text-green-600',
    iconBg: 'bg-green-50',
    iconBorder: 'border-green-200',
    index: '06'
  },
  {
    title: 'Legal Evidence & Audit',
    description: 'Auto-generated court-ready forensic packages with annotated documents, methodology, and chain-of-custody documentation.',
    icon: <Gavel className="w-12 h-12" strokeWidth={1.5} />,
    badge: null,
    gradientFrom: 'from-indigo-500',
    gradientTo: 'to-blue-700',
    iconColor: 'text-indigo-600',
    iconBg: 'bg-indigo-50',
    iconBorder: 'border-indigo-200',
    index: '07'
  }
]

export default function FeaturesCards() {
  return (
    <section className="py-24 px-4 bg-white overflow-hidden relative">
      <div className="max-w-7xl mx-auto relative z-10">
        <SectionTitle
          title="Seven Intelligence Layers"
          subtitle="Each layer catches what others miss, providing impenetrable verification powered by specialized AI agents."
          highlight="Intelligence Layers"
        />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const isCenter = index === features.length - 1 && features.length % 3 === 1

            return (
              <motion.div
                key={index}
                className={`${isCenter ? 'lg:col-start-2' : ''}`}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-60px" }}
                transition={{ duration: 0.6, delay: index * 0.08, ease: "easeOut" }}
              >
                {/* Card — no GlowCard, just clean white with shadow */}
                <div className="relative w-full h-full min-h-[380px] bg-white rounded-2xl flex flex-col overflow-hidden border border-slate-100 shadow-md hover:shadow-xl transition-shadow duration-300 hover:-translate-y-1 transition-transform">

                  {/* TOP: Evervault interactive area */}
                  <div className="relative flex-1 min-h-[220px] bg-slate-50 overflow-hidden rounded-t-2xl">
                    {/* Evervault handles the hover matrix + gradient reveal */}
                    <EvervaultCard
                      gradientFrom={feature.gradientFrom}
                      gradientTo={feature.gradientTo}
                      className="absolute inset-0 h-full w-full"
                    >
                      {/* SOLID colored icon circle — fully opaque, no transparency */}
                      <div
                        className={`w-28 h-28 rounded-full flex items-center justify-center shadow-lg border-[5px] bg-white ${feature.iconBorder} ${feature.iconColor}`}
                      >
                        {feature.icon}
                      </div>
                    </EvervaultCard>

                    {/* Index number */}
                    <div className="absolute top-4 left-4 font-mono text-sm font-bold text-slate-400 z-20">
                      {feature.index}
                    </div>

                    {/* Badge top right */}
                    {feature.badge && (
                      <div className="absolute top-4 right-4 z-20">
                        <Badge
                          className={`
                            ${feature.badge.variant === 'secondary'
                              ? 'bg-amber-50 text-amber-600 border-amber-200'
                              : feature.badge.variant === 'destructive'
                              ? 'bg-rose-50 text-rose-600 border-rose-200'
                              : 'bg-blue-50 text-blue-600 border-blue-200'}
                            px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider
                          `}
                        >
                          {feature.badge.text}
                        </Badge>
                      </div>
                    )}
                  </div>

                  {/* BOTTOM: Title + description */}
                  <div className="px-5 py-4 border-t border-slate-100 bg-white">
                    <h3 className="text-base font-bold text-slate-800 mb-1.5 tracking-tight">{feature.title}</h3>
                    <p className="text-xs text-slate-500 leading-relaxed">{feature.description}</p>
                  </div>

                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
