'use client'

import { motion } from 'framer-motion'

export function IntelligenceLayers() {
  const layers = [
    {
      number: '1',
      title: 'Document Forensics',
      description: 'Advanced image analysis detects forgeries, tampering, and document authenticity',
      color: 'from-[#00AEEF]',
    },
    {
      number: '2',
      title: 'Multilingual OCR',
      description: 'Extracts text accurately from English, Hindi, and regional language documents',
      color: 'from-[#0099DD]',
    },
    {
      number: '3',
      title: 'Cross-Document Consistency',
      description: 'Validates consistency of data across multiple documents in the application',
      color: 'from-[#0088CC]',
    },
    {
      number: '4',
      title: 'ITR Verification',
      description: 'Verifies income claims against official Income Tax Returns and government records',
      color: 'from-[#0077BB]',
    },
    {
      number: '5',
      title: 'Fraud DNA Matching',
      description: 'Identifies fraud patterns and suspicious signatures matching known fraud cases',
      color: 'from-[#0066AA]',
    },
    {
      number: '6',
      title: 'Risk Intelligence',
      description: 'Analyzes applicant history, credit patterns, and financial behavior indicators',
      color: 'from-[#005599]',
    },
    {
      number: '7',
      title: 'Legal Evidence Ready',
      description: 'Generates audit-ready reports suitable for legal proceedings and compliance',
      color: 'from-[#003D6B]',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
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
    <section className="relative w-full bg-gradient-to-b from-white to-[#F5FAFE] py-20 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold text-[#003D6B] mb-4">
            7 Intelligence <span className="text-[#F58220]">Layers</span>
          </h2>
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            Our AI agents work in parallel across seven distinct fraud detection layers for comprehensive coverage
          </p>
        </motion.div>

        {/* Layers Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-7 gap-4"
        >
          {layers.map((layer, i) => (
            <motion.div
              key={i}
              variants={itemVariants}
              className={`bg-gradient-to-b ${layer.color} to-transparent rounded-lg p-6 text-white relative overflow-hidden group hover:shadow-xl transition-shadow duration-300`}
            >
              {/* Background accent */}
              <div className="absolute top-0 right-0 w-20 h-20 opacity-10 group-hover:opacity-20 transition-opacity">
                <div className="w-full h-full rounded-full bg-white" />
              </div>

              {/* Content */}
              <div className="relative z-10">
                <div className="text-4xl font-bold mb-3 opacity-80">{layer.number}</div>
                <h3 className="font-bold text-lg mb-2 line-clamp-2">{layer.title}</h3>
                <p className="text-sm opacity-90 leading-relaxed text-white/90">{layer.description}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Bottom message */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ delay: 0.8 }}
          className="mt-12 text-center"
        >
          <p className="text-gray-700 text-lg">
            All 7 layers work in parallel, analyzing documents simultaneously to deliver fraud verdicts in just 90 seconds
          </p>
        </motion.div>
      </div>
    </section>
  )
}
