'use client'

import { motion } from 'framer-motion'
import { GitBranch } from 'lucide-react'

export function AIAgents() {
  const agents = [
    {
      name: 'Classifier Agent',
      description: 'Categorizes documents and application type for targeted analysis',
      tasks: ['Document Classification', 'Application Routing', 'Priority Assignment'],
    },
    {
      name: 'Investigator Agent',
      description: 'Deep dives into document authenticity and content verification',
      tasks: ['Forensic Analysis', 'OCR Extraction', 'Content Validation'],
    },
    {
      name: 'Cross-Reference Agent',
      description: 'Validates consistency across multiple documents and data sources',
      tasks: ['Cross-Document Matching', 'Consistency Checks', 'Data Reconciliation'],
    },
    {
      name: 'Compliance Agent',
      description: 'Ensures regulatory compliance and government record verification',
      tasks: ['ITR Verification', 'PAN Validation', 'CIBIL Integration'],
    },
    {
      name: 'Decision Agent',
      description: 'Synthesizes findings and generates final fraud verdict with confidence score',
      tasks: ['Risk Aggregation', 'Verdict Generation', 'Score Calculation'],
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6 },
    },
  }

  return (
    <section className="relative w-full bg-gradient-to-b from-[#F5FAFE] to-[#FFF8E7] py-20 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold text-[#003D6B] mb-4">
            AI Agent <span className="text-[#00AEEF]">Orchestration</span>
          </h2>
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            Five specialized AI agents work in concert to deliver comprehensive fraud analysis
          </p>
        </motion.div>

        {/* Agents Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-12"
        >
          {agents.map((agent, i) => (
            <motion.div
              key={i}
              variants={itemVariants}
              className="bg-white rounded-lg p-6 border-l-4 border-[#00AEEF] shadow-lg hover:shadow-xl transition-shadow duration-300"
            >
              <div className="flex items-start gap-3 mb-4">
                <div className="w-10 h-10 rounded-full bg-[#00AEEF]/10 flex items-center justify-center flex-shrink-0">
                  <GitBranch className="w-5 h-5 text-[#00AEEF]" />
                </div>
                <h3 className="font-bold text-[#003D6B] text-lg">{agent.name}</h3>
              </div>
              <p className="text-gray-700 text-sm mb-4">{agent.description}</p>
              <div className="space-y-2">
                {agent.tasks.map((task, j) => (
                  <div key={j} className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#F58220] mt-1.5 flex-shrink-0" />
                    <span className="text-xs text-gray-600">{task}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Orchestration Visualization */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ delay: 0.6 }}
          className="bg-gradient-to-r from-[#00AEEF]/10 to-[#F58220]/10 rounded-xl p-8 border border-[#00AEEF]/20"
        >
          <h3 className="font-bold text-[#003D6B] text-lg mb-4 text-center">Orchestration Workflow</h3>
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 flex-wrap">
            <div className="text-center">
              <div className="font-bold text-[#00AEEF]">Upload</div>
              <div className="text-xs text-gray-600">Documents</div>
            </div>
            <div className="text-2xl text-[#F58220] hidden md:block">→</div>
            <div className="text-center">
              <div className="font-bold text-[#00AEEF]">Classify</div>
              <div className="text-xs text-gray-600">& Route</div>
            </div>
            <div className="text-2xl text-[#F58220] hidden md:block">→</div>
            <div className="text-center">
              <div className="font-bold text-[#00AEEF]">Investigate</div>
              <div className="text-xs text-gray-600">Forensics</div>
            </div>
            <div className="text-2xl text-[#F58220] hidden md:block">→</div>
            <div className="text-center">
              <div className="font-bold text-[#00AEEF]">Cross-Check</div>
              <div className="text-xs text-gray-600">Consistency</div>
            </div>
            <div className="text-2xl text-[#F58220] hidden md:block">→</div>
            <div className="text-center">
              <div className="font-bold text-[#00AEEF]">Verify</div>
              <div className="text-xs text-gray-600">Compliance</div>
            </div>
            <div className="text-2xl text-[#F58220] hidden md:block">→</div>
            <div className="text-center">
              <div className="font-bold text-[#FDB913]">Verdict</div>
              <div className="text-xs text-gray-600">in 90s</div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
