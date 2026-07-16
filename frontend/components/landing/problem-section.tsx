'use client'

import { motion } from 'framer-motion'
import { Clock, EyeOff, FileX } from 'lucide-react'

export function ProblemSection() {
  const problems = [
    {
      icon: Clock,
      title: 'Days, Not Seconds',
      description: 'Loan officers spend 3-7 days manually verifying documents for a single application, delaying genuine customers and overwhelming teams.',
    },
    {
      icon: EyeOff,
      title: 'Invisible to Human Eyes',
      description: 'Modern document tampering through PDF editors, metadata manipulation, and image forensics goes undetected without specialized forensic analysis.',
    },
    {
      icon: FileX,
      title: 'Isolated Verification',
      description: 'Documents are verified individually, missing the fraud that hides in mismatches between ITR income, bank statements, and property records.',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.2 } },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
  }

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white relative">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16 space-y-4"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-primary-900 tracking-tight">
            Manual Verification Cannot Scale
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            The three critical gaps in traditional loan underwriting that expose banks to sophisticated fraud rings.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-8"
        >
          {problems.map((problem, i) => {
            const Icon = problem.icon
            return (
              <motion.div
                key={i}
                variants={itemVariants}
                className="bg-white rounded-2xl p-8 border border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group"
              >
                <div className="w-14 h-14 rounded-full bg-amber-50 flex items-center justify-center mb-6 group-hover:bg-amber-100 transition-colors">
                  <Icon className="w-7 h-7 text-amber-500" />
                </div>
                <h3 className="text-xl font-bold text-primary-900 mb-4">{problem.title}</h3>
                <p className="text-slate-600 leading-relaxed">{problem.description}</p>
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
