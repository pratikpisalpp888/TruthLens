'use client'

import { motion } from 'framer-motion'
import { Clock, Eye, AlertTriangle } from 'lucide-react'

export function ProblemStatement() {
  const problems = [
    {
      icon: <Clock className="w-8 h-8" />,
      title: 'Manual Delays',
      description: 'Loan verification takes days or weeks, slowing approvals and losing business',
      color: 'from-orange-500 to-red-500',
    },
    {
      icon: <Eye className="w-8 h-8" />,
      title: 'Invisible Fraud',
      description: 'Sophisticated fraud schemes slip through manual checks, costing millions',
      color: 'from-red-500 to-pink-500',
    },
    {
      icon: <AlertTriangle className="w-8 h-8" />,
      title: 'Document Mismatches',
      description: 'Forged or inconsistent documents go undetected in crowded application queues',
      color: 'from-yellow-500 to-orange-500',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
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
            The Fraud Problem is <span className="text-[#F58220]">Accelerating</span>
          </h2>
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            Banks face mounting pressure to approve loans faster, but traditional methods fail to catch sophisticated fraud schemes.
          </p>
        </motion.div>

        {/* Problem Cards */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          {problems.map((problem, i) => (
            <motion.div
              key={i}
              variants={itemVariants}
              className="bg-white rounded-xl shadow-lg p-8 border-t-4 border-[#F58220] hover:shadow-2xl transition-shadow duration-300"
            >
              <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${problem.color} flex items-center justify-center text-white mb-6`}>
                {problem.icon}
              </div>
              <h3 className="text-xl font-bold text-[#003D6B] mb-3">{problem.title}</h3>
              <p className="text-gray-700 leading-relaxed">{problem.description}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Key Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ delay: 0.6 }}
          className="mt-16 bg-gradient-to-r from-[#00AEEF]/10 to-[#F58220]/10 rounded-xl p-8 border border-[#FDB913]/30"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-[#00AEEF]">₹1.7L Cr</div>
              <p className="text-sm text-gray-700 mt-2">Fraud Loss Annually</p>
            </div>
            <div>
              <div className="text-3xl font-bold text-[#F58220]">5-7 Days</div>
              <p className="text-sm text-gray-700 mt-2">Average Approval Time</p>
            </div>
            <div>
              <div className="text-3xl font-bold text-[#003D6B]">30%</div>
              <p className="text-sm text-gray-700 mt-2">Applications with Issues</p>
            </div>
            <div>
              <div className="text-3xl font-bold text-[#FDB913]">100%</div>
              <p className="text-sm text-gray-700 mt-2">Manual Review Required</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
