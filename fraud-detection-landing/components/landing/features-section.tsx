'use client'

import { motion } from 'framer-motion'
import { Brain, Zap, Shield, BarChart3, Lock, Users } from 'lucide-react'

interface Feature {
  icon: React.ReactNode
  title: string
  description: string
  color: 'orange' | 'blue' | 'yellow'
}

export function FeaturesSection() {
  const features: Feature[] = [
    {
      icon: <Brain className="w-6 h-6" />,
      title: 'Advanced AI Engine',
      description: 'Proprietary ML models trained on Indian banking fraud patterns for maximum accuracy.',
      color: 'orange',
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'Lightning Fast Detection',
      description: 'Sub-100ms response ensures fraudulent applications blocked instantly.',
      color: 'blue',
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: 'RBI & NPCI Compliant',
      description: 'Full compliance with Reserve Bank and NPCI guidelines for secure lending.',
      color: 'yellow',
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Real-Time Dashboard',
      description: 'Comprehensive analytics with actionable fraud insights and trends.',
      color: 'orange',
    },
    {
      icon: <Lock className="w-6 h-6" />,
      title: 'Bank-Grade Security',
      description: 'End-to-end encryption with zero-knowledge architecture for maximum privacy.',
      color: 'blue',
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: 'Expert Support',
      description: 'Dedicated banking specialists available for 24/7 implementation support.',
      color: 'yellow',
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

  const colorMap = {
    orange: {
      bg: 'bg-orange-50',
      icon: 'text-[#F58220]',
      border: 'border-[#F58220]',
    },
    blue: {
      bg: 'bg-blue-50',
      icon: 'text-[#00AEEF]',
      border: 'border-[#00AEEF]',
    },
    yellow: {
      bg: 'bg-yellow-50',
      icon: 'text-[#FDB913]',
      border: 'border-[#FDB913]',
    },
  }

  return (
    <section id="features" className="relative w-full bg-gradient-to-b from-[#F0F8FF] via-[#FFF8E7] to-[#FFF5E6] py-24 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold text-[#003D6B] mb-4">
            Built for <span className="text-[#F58220]">Excellence</span>
          </h2>
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            Everything you need to protect your lending operations with enterprise-grade fraud prevention.
          </p>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {features.map((feature, i) => {
            const colors = colorMap[feature.color]
            return (
              <motion.div
                key={i}
                variants={itemVariants}
                className={`${colors.bg} rounded-lg border-l-4 ${colors.border} p-6 hover:shadow-lg transition-shadow duration-300`}
              >
                <div className={`${colors.icon} mb-4`}>{feature.icon}</div>
                <h3 className="text-lg font-bold text-[#003D6B] mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-700">{feature.description}</p>
              </motion.div>
            )
          })}
        </motion.div>
      </div>

      {/* Wave Divider */}
      <svg
        viewBox="0 0 1440 80"
        preserveAspectRatio="none"
        className="w-full h-auto block absolute bottom-0 left-0"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M0,40 Q120,20 240,40 T480,40 T720,40 T960,40 T1200,40 T1440,40 L1440,80 L0,80 Z"
          fill="white"
        />
      </svg>
    </section>
  )
}
