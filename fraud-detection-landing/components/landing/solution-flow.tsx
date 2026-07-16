'use client'

import { motion } from 'framer-motion'
import { Upload, Zap, CheckCircle, ArrowRight } from 'lucide-react'

export function SolutionFlow() {
  const steps = [
    {
      icon: <Upload className="w-8 h-8" />,
      title: 'Upload Documents',
      description: 'Users securely upload loan applications and supporting documents to TruthLens',
      color: '#00AEEF',
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Intelligent Analysis',
      description: '7 intelligence layers analyze documents in parallel with advanced AI agents',
      color: '#F58220',
    },
    {
      icon: <CheckCircle className="w-8 h-8" />,
      title: 'Verdict in 90 Seconds',
      description: 'Receive comprehensive fraud analysis with risk score and detailed findings',
      color: '#FDB913',
    },
  ]

  return (
    <section className="relative w-full bg-gradient-to-b from-[#F5FAFE] to-white py-20 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold text-[#003D6B] mb-4">
            The TruthLens <span className="text-[#00AEEF]">Solution</span>
          </h2>
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            Detect fraud in 90 seconds with enterprise-grade accuracy. 100% offline, zero data transmission.
          </p>
        </motion.div>

        {/* Solution Flow Steps */}
        <div className="flex flex-col items-center gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-100px' }}
              transition={{ delay: index * 0.2 }}
              className="w-full"
            >
              <div className="flex items-start gap-6 md:gap-8">
                {/* Icon */}
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  className="flex-shrink-0 w-20 h-20 rounded-full flex items-center justify-center text-white font-bold text-2xl"
                  style={{ backgroundColor: step.color }}
                >
                  {step.icon}
                </motion.div>

                {/* Content */}
                <div className="flex-1 pt-2">
                  <h3 className="text-2xl font-bold text-[#003D6B] mb-2">{step.title}</h3>
                  <p className="text-gray-700 text-lg">{step.description}</p>
                </div>
              </div>

              {/* Arrow */}
              {index < steps.length - 1 && (
                <div className="ml-10 mt-6">
                  <motion.div
                    animate={{ y: [0, 8, 0] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="text-[#00AEEF]"
                  >
                    <ArrowRight className="w-6 h-6 rotate-90" />
                  </motion.div>
                </div>
              )}
            </motion.div>
          ))}
        </div>

        {/* Key Benefits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ delay: 0.6 }}
          className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <div className="bg-gradient-to-br from-[#00AEEF]/10 to-transparent rounded-lg p-6 border border-[#00AEEF]/20">
            <h4 className="font-bold text-[#00AEEF] mb-2">100% Offline</h4>
            <p className="text-sm text-gray-700">Zero data transmission. All analysis happens locally on-premise</p>
          </div>
          <div className="bg-gradient-to-br from-[#F58220]/10 to-transparent rounded-lg p-6 border border-[#F58220]/20">
            <h4 className="font-bold text-[#F58220] mb-2">7 Intelligence Layers</h4>
            <p className="text-sm text-gray-700">Document forensics, OCR, consistency checks, and fraud pattern matching</p>
          </div>
          <div className="bg-gradient-to-br from-[#FDB913]/10 to-transparent rounded-lg p-6 border border-[#FDB913]/20">
            <h4 className="font-bold text-[#FDB913] mb-2">90 Second Verdict</h4>
            <p className="text-sm text-gray-700">Instant fraud detection with confidence scores and detailed findings</p>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
