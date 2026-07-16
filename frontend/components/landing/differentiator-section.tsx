'use client'

import { motion } from 'framer-motion'
import { Check, X } from 'lucide-react'

export function DifferentiatorSection() {
  const comparison = [
    { label: 'Document Scope', trad: 'Single-document verification', truth: 'Cross-document intelligence' },
    { label: 'Data Privacy', trad: 'Cloud-dependent AI', truth: 'Completely offline operation' },
    { label: 'Explainability', trad: 'Black-box decisions', truth: 'Explainable AI with regulatory citations' },
    { label: 'Localization', trad: 'Generic fraud detection', truth: 'Indian document context and languages' },
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-primary-900 mb-4 tracking-tight">
            Not Another AI Tool
          </h2>
          <p className="text-lg text-slate-600">
            Purpose-built for Indian banking underwriting.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden"
        >
          {/* Header Row */}
          <div className="grid grid-cols-2 md:grid-cols-[1fr_1fr_1fr] bg-slate-50 border-b border-border p-6 font-bold text-sm uppercase tracking-wider text-slate-500">
            <div className="hidden md:block">Capabilities</div>
            <div className="text-center">Traditional Tools</div>
            <div className="text-center text-primary-700">TruthLens</div>
          </div>
          
          {/* Body Rows */}
          <div className="divide-y divide-border">
            {comparison.map((row, i) => (
              <div key={i} className="grid grid-cols-2 md:grid-cols-[1fr_1fr_1fr] p-6 items-center hover:bg-slate-50 transition-colors">
                <div className="hidden md:block font-medium text-slate-700">{row.label}</div>
                <div className="flex flex-col md:flex-row items-center gap-3 text-center md:text-left text-slate-500 justify-center">
                  <X className="w-5 h-5 text-red-400 shrink-0" />
                  <span className="text-sm">{row.trad}</span>
                </div>
                <div className="flex flex-col md:flex-row items-center gap-3 text-center md:text-left text-primary-900 font-medium justify-center bg-primary-50 py-3 px-4 rounded-xl">
                  <Check className="w-5 h-5 text-green-500 shrink-0" />
                  <span className="text-sm">{row.truth}</span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
